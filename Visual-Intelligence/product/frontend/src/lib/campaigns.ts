/**
 * Campaign API Client
 * Typed wrappers for all /api/campaigns endpoints.
 * The backend is at http://localhost:8000 (set via NEXT_PUBLIC_API_URL).
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// --- Types (mirrors backend Pydantic models) ---

export interface CampaignSummary {
  id: string;
  name: string;
  has_material: boolean;
  created_at: string;
}

export interface MemoryNode {
  type: 'observation' | 'reasoning' | 'conclusion';
  content: string;
  timestamp: string;
}

export interface ConfidenceField {
  value: string | string[];
  confidence: number;
}

export interface ProductDNA {
  material: ConfidenceField;
  weaving_technique: ConfidenceField;
  primary_features: ConfidenceField;
  cultural_context?: ConfidenceField;
  raw_claims?: Record<string, unknown>[];
}

export interface FullCampaign {
  id: string;
  name: string;
  material_path: string | null;
  memory_stream: MemoryNode[];
  identity: {
    product_dna: ProductDNA | null;
  };
  planning: {
    creative_objective: string;
    proposed_direction_title: string | null;
    proposed_direction_body: string | null;
    selected_background: string | null;
    selected_pose: string | null;
    selected_lighting: string | null;
    recommendations: Record<string, { value: string, reason: string }> | null;
  };
  execution: {
    moodboard_brief: string | null;
    asset_states: {
      id: string;
      prompt: string;
      status: string;
      image_url: string | null;
    }[];
  };
  created_at: string;
  updated_at: string;
}

// --- API Functions ---

async function baseFetch<T>(path: string, options: RequestInit = {}): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, options);
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || 'API error');
  }
  return res.json();
}

/** GET /api/campaigns — list all campaign folders */
export async function listCampaigns(): Promise<CampaignSummary[]> {
  return baseFetch('/api/campaigns');
}

/** POST /api/campaigns — create a new campaign folder by name */
export async function createCampaign(name: string): Promise<CampaignSummary> {
  return baseFetch('/api/campaigns', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name }),
  });
}

/** GET /api/campaigns/{id} — get full campaign state (restores workspace) */
export async function getCampaign(id: string): Promise<FullCampaign> {
  return baseFetch(`/api/campaigns/${id}`);
}

/** PATCH /api/campaigns/{id} — rename a campaign folder */
export async function renameCampaign(id: string, name: string): Promise<CampaignSummary> {
  return baseFetch(`/api/campaigns/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name }),
  });
}

/** DELETE /api/campaigns/{id} — delete a campaign and its assets */
export async function deleteCampaign(id: string): Promise<void> {
  await baseFetch(`/api/campaigns/${id}`, { method: 'DELETE' });
}

/** PATCH /api/campaigns/{id}/options — update custom art direction options */
export async function updateCampaignOptions(
  id: string,
  options: { background: string; pose: string; lighting: string }
): Promise<FullCampaign> {
  return baseFetch(`/api/campaigns/${id}/options`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(options),
  });
}

/** POST /api/campaigns/{id}/material — upload image file (multipart) */
export async function uploadMaterial(id: string, file: File): Promise<{ status: string; material_path: string }> {
  const form = new FormData();
  form.append('file', file);
  return baseFetch(`/api/campaigns/${id}/material`, {
    method: 'POST',
    body: form,
    // NOTE: Do NOT set Content-Type header — browser sets it with boundary automatically for FormData
  });
}

/** POST /api/campaigns/{id}/analyze — trigger Gemini Vision analysis (starts background job) */
export async function analyzeMaterial(id: string): Promise<{ status: string; message: string }> {
  return baseFetch(`/api/campaigns/${id}/analyze`, { method: 'POST' });
}

/** POST /api/campaigns/{id}/generate — trigger Prompt Engine RAG generation (starts background job) */
export async function generateCampaign(id: string): Promise<{ status: string; message: string }> {
  return baseFetch(`/api/campaigns/${id}/generate`, { method: 'POST' });
}

/** Returns the public URL to serve a campaign's material image via the backend static server */
export function getMaterialUrl(material_path: string): string {
  // Backend serves data/ folder as /static/
  // e.g. data/assets/campaign_abc/material.jpg → /static/assets/campaign_abc/material.jpg
  const relative = material_path.replace(/\\/g, '/').replace(/^data\//, '');
  return `${API_URL}/static/${relative}`;
}
