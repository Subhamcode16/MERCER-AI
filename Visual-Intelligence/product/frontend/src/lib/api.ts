import { supabase } from './supabase';

const API_URL = process.env.NEXT_PUBLIC_API_URL || '';

// ── Retryable HTTP status codes (transient infra / backend not ready) ─────────
const RETRYABLE_STATUSES = new Set([500, 502, 503, 504]);
const MAX_RETRIES = 3;
const RETRY_BASE_MS = 800;

// ── Typed API error — carries HTTP status so callers can branch precisely ─────
export class ApiError extends Error {
  readonly status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/**
 * Core API Client for Mercer AI
 *
 * Features:
 * - Automatically attaches the Supabase JWT token to requests.
 * - Retries network-level failures (ECONNREFUSED, backend not started) and
 *   transient 5xx responses with exponential backoff (800ms → 1.6s → 3.2s).
 * - Throws a typed `ApiError` with `.status` so callers can distinguish
 *   infrastructure errors (500/503) from auth errors (401/403) without
 *   fragile string matching.
 */
export async function apiFetch(
  endpoint: string,
  options: RequestInit = {},
  _attempt = 0
): Promise<any> {
  // 1. Setup headers
  const headers = new Headers(options.headers || {});
  // Do NOT set Content-Type for FormData — the browser sets it with the
  // multipart boundary automatically. Setting it manually breaks file uploads.
  if (!(options.body instanceof FormData)) {
    headers.set('Content-Type', 'application/json');
  }

  // 2. Get token (prefer explicit header, fallback to session)
  if (!headers.has('Authorization')) {
    const { data: { session } } = await supabase.auth.getSession();
    const token = session?.access_token;
    if (token) {
      headers.set('Authorization', `Bearer ${token}`);
    }
  }

  // 3. Execute fetch — retry on network-level failure (backend not ready yet)
  let response: Response;
  try {
    response = await fetch(`${API_URL}${endpoint}`, {
      ...options,
      headers,
    });
  } catch (fetchErr: any) {
    if (_attempt < MAX_RETRIES) {
      await sleep(RETRY_BASE_MS * Math.pow(2, _attempt));
      return apiFetch(endpoint, options, _attempt + 1);
    }
    // Exhausted retries — surface as a connection error (status 0)
    throw new ApiError(
      `Unable to connect to the backend server. Please ensure it is running.`,
      0
    );
  }

  // 4. Retry on transient server errors before throwing
  if (!response.ok && RETRYABLE_STATUSES.has(response.status) && _attempt < MAX_RETRIES) {
    await sleep(RETRY_BASE_MS * Math.pow(2, _attempt));
    return apiFetch(endpoint, options, _attempt + 1);
  }

  // 5. Handle non-retryable errors
  if (!response.ok) {
    let errorMessage = `HTTP ${response.status}`;
    try {
      const errorData = await response.json();
      errorMessage = errorData.detail || errorMessage;
    } catch {
      errorMessage = response.statusText || errorMessage;
    }
    throw new ApiError(errorMessage, response.status);
  }

  return response.json();
}
