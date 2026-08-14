export type PageState = 'greeting' | 'onboarding' | 'workspace';

export type AgentId = 
  | 'brand-dna'
  | 'material-dna'
  | 'image-decomposer'
  | 'art-director'
  | 'strategist'
  | 'renderer'
  | 'validator'
  | 'copywriter';

export type AgentTaskStatus = 'idle' | 'processing' | 'completed';

export interface AgentProfile {
  id: AgentId;
  name: string;
  handle: string;
  abbreviation: string;
  gradient: string;
  role: string;
}

export const AGENT_PROFILES: Record<AgentId, AgentProfile> = {
  'brand-dna': {
    id: 'brand-dna',
    name: 'Brand DNA',
    handle: '@Brand-DNA',
    abbreviation: 'BR',
    gradient: 'from-amber-600 to-amber-900',
    role: 'Account Guard & Brand Alignment',
  },
  'material-dna': {
    id: 'material-dna',
    name: 'Material DNA',
    handle: '@Material-DNA',
    abbreviation: 'MD',
    gradient: 'from-indigo-600 to-indigo-900',
    role: 'Textile & Weave Specimen Analyzer',
  },
  'image-decomposer': {
    id: 'image-decomposer',
    name: 'Visual DNA',
    handle: '@Visual-DNA',
    abbreviation: 'VD',
    gradient: 'from-purple-600 to-purple-900',
    role: 'Photographic & Lighting Decomposer',
  },
  'art-director': {
    id: 'art-director',
    name: 'Art Director',
    handle: '@Art-Director',
    abbreviation: 'AD',
    gradient: 'from-rose-600 to-rose-900',
    role: 'Shot Setup & Composition Director',
  },
  'strategist': {
    id: 'strategist',
    name: 'Campaign Strategist',
    handle: '@Campaign-Strategist',
    abbreviation: 'CS',
    gradient: 'from-orange-600 to-orange-900',
    role: 'Sequence & Shot List Planner',
  },
  'renderer': {
    id: 'renderer',
    name: 'Synthesizer',
    handle: '@Synthesizer',
    abbreviation: 'SY',
    gradient: 'from-blue-600 to-blue-900',
    role: 'High-Fidelity Visual Renderer',
  },
  'validator': {
    id: 'validator',
    name: 'Quality Validator',
    handle: '@Quality-Validator',
    abbreviation: 'QV',
    gradient: 'from-teal-600 to-teal-900',
    role: 'Physics & Distortion Quality Guard',
  },
  'copywriter': {
    id: 'copywriter',
    name: 'Creative Copywriter',
    handle: '@Creative-Copywriter',
    abbreviation: 'CC',
    gradient: 'from-emerald-600 to-emerald-900',
    role: 'Editorial & Narrative Copywriter',
  },
};

export interface ChatMessage {
  id: string;
  sender: 'user' | AgentId;
  senderName: string;
  avatarColor?: string;
  time: string;
  text?: string;
  isRead?: boolean;
  dnaCard?: {
    title: string;
    details: Record<string, string>;
    bullet?: string;
  };
  photoCard?: {
    title: string;
    description: string;
    images: { label: string; url: string }[];
  };
  qualityCard?: {
    status: 'PASSED' | 'FLAGGED';
    actions: string[];
  };
  imageCard?: {
    url: string;
    prompt: string;
    caption?: string;
  };
}

export interface BrandDnaData {
  account: string;
  archetype: string;
  voice: string;
  palette: string[];
  customRules?: string;
}

export interface AgentTaskInfo {
  status: AgentTaskStatus;
  currentTask?: string;
}

export interface ChatSession {
  id: string;
  name: string;
  messages: ChatMessage[];
}

export interface CampaignFolder {
  id: string;
  name: string;
  sessions: ChatSession[];
  assets: { url: string; label: string }[];
}
