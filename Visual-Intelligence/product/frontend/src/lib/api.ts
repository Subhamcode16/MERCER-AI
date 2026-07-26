import { supabase } from './supabase';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Core API Client for Mercer AI
 * Automatically attaches the Supabase JWT token to requests.
 */
export async function apiFetch(endpoint: string, options: RequestInit = {}) {
  // 1. Setup headers
  const headers = new Headers(options.headers || {});
  headers.set('Content-Type', 'application/json');

  // 2. Get token (prefer explicit header, fallback to session)
  if (!headers.has('Authorization')) {
    const { data: { session } } = await supabase.auth.getSession();
    const token = session?.access_token;
    if (token) {
      headers.set('Authorization', `Bearer ${token}`);
    }
  }

  // 3. Execute fetch
  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
  });

  // 4. Handle errors gracefully
  if (!response.ok) {
    let errorMessage = 'An API error occurred';
    try {
      const errorData = await response.json();
      errorMessage = errorData.detail || errorMessage;
    } catch (e) {
      errorMessage = response.statusText;
    }
    throw new Error(errorMessage);
  }

  return response.json();
}
