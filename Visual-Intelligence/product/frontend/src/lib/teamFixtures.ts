// ============================================================================
// ❖ VYREN AI TEAM — DOMAIN MODELS & CENTRALIZED FIXTURES
// ============================================================================

export type DepartmentName = 
  | 'Strategy' 
  | 'Creative' 
  | 'Intelligence' 
  | 'Production' 
  | 'Quality';

export type CoworkerStatus = 
  | 'Available' 
  | 'Working' 
  | 'Waiting' 
  | 'Needs You' 
  | 'Blocked' 
  | 'Completed';

export type HandoffStatus = 
  | 'Proposed' 
  | 'Accepted' 
  | 'Working' 
  | 'Returned' 
  | 'Completed' 
  | 'Blocked';

export interface Coworker {
  id: string;
  name: string;
  role: string;
  department: DepartmentName;
  avatarInitials: string;
  avatarColor: string;
  bio: string;
  status: CoworkerStatus;
  currentWork: {
    task: string;
    campaign: string;
    progress: number;
    estimatedDelivery: string;
  };
  recentContributions: {
    title: string;
    timestamp: string;
    impact: string;
  }[];
  skills: string[];
  boundedCapabilities: string[];
  memoryScope: {
    scope: 'Campaign Memory' | 'Brand Memory' | 'Skill Memory' | 'Worker Memory' | 'Institutional Knowledge';
    accessLevel: 'Full' | 'Read Only' | 'Restricted';
    description: string;
  }[];
  approvalRequirements: string;
}

export interface DepartmentSummary {
  name: DepartmentName;
  description: string;
  coworkerCount: number;
  activeTasks: number;
  campaignsInvolved: number;
  attentionRequired: number;
  color: string;
}

export interface ActiveWorkItem {
  id: string;
  campaign: string;
  coworkerId: string;
  coworkerName: string;
  coworkerRole: string;
  coworkerAvatar: string;
  coworkerColor: string;
  taskTitle: string;
  department: DepartmentName;
  status: CoworkerStatus;
  progress: number;
  deadline: string;
}

export interface CampaignRoom {
  id: string;
  campaignName: string;
  brand: string;
  phase: 'Intelligence' | 'Directions' | 'Visuals' | 'Review' | 'Production';
  activeCoworkers: {
    id: string;
    name: string;
    role: string;
    avatarColor: string;
  }[];
  currentHandoffsCount: number;
  humanDecisionRequired?: string;
  studioLink: string;
}

export interface TeamHandoff {
  id: string;
  sender: {
    id: string;
    name: string;
    role: string;
    avatarColor: string;
  };
  receiver: {
    id: string;
    name: string;
    role: string;
    avatarColor: string;
  };
  campaign: string;
  purpose: string;
  attachedOutputs: string[];
  evidenceSummary: string;
  status: HandoffStatus;
  timestamp: string;
}

export interface TeamSkill {
  id: string;
  name: string;
  owner: string;
  category: 'Styling' | 'Physics' | 'Analytics' | 'Lighting' | 'Auditing';
  version: string;
  usageCount: number;
  governanceScope: string;
}

export interface TeamRoutine {
  id: string;
  name: string;
  owner: string;
  triggerCadence: string;
  lastRun: string;
  status: 'Active' | 'Paused' | 'Scheduled';
  purpose: string;
}

export interface AttentionItem {
  id: string;
  type: 'Approval' | 'Decision' | 'Conflict' | 'Review';
  title: string;
  urgency: 'Immediate' | 'High' | 'Medium';
  coworkerName: string;
  campaignName: string;
  actionPrompt: string;
  targetTab?: 'overview' | 'directions' | 'review' | 'handoffs';
}

export interface TeamActivityEvent {
  id: string;
  timestamp: string;
  actor: string;
  actorType: 'AI Coworker' | 'Human Director' | 'System';
  action: string;
  detail: string;
  campaign?: string;
  hash: string;
}

// ============================================================================
// CENTRALIZED TEAM FIXTURE DATASET
// ============================================================================

export const INITIAL_COWORKERS: Coworker[] = [
  {
    id: "marcus-vance",
    name: "Marcus Vance",
    role: "Creative Director",
    department: "Creative",
    avatarInitials: "MV",
    avatarColor: "#E1D4C0",
    bio: "Specializes in high-fashion narrative direction, architectural silhouettes, and luxury brand storytelling across global diaspora audiences.",
    status: "Working",
    currentWork: {
      task: "Refining Direction 02 visual language & asymmetrical framing angles",
      campaign: "Autumn/Winter 2026: The Modern Sovereign",
      progress: 75,
      estimatedDelivery: "Today, 18:00 UTC"
    },
    recentContributions: [
      {
        title: "Synthesized 3 comparative creative directions with trade-off matrices",
        timestamp: "2 hours ago",
        impact: "Locked Direction 02 as primary campaign foundation."
      },
      {
        title: "Composed editorial narrative brief for high-impact OOH billboards",
        timestamp: "Yesterday",
        impact: "Approved by Human Lead Elena Vance."
      }
    ],
    skills: ["Creative Direction", "Narrative Synthesis", "Editorial Composition", "Trend Translation"],
    boundedCapabilities: [
      "Can formulate creative hypotheses and direction memos",
      "Can guide visual styling and moodboard curation",
      "Cannot authorize final budgets or change locked brand DNA without Human Decision Record"
    ],
    memoryScope: [
      { scope: "Campaign Memory", accessLevel: "Full", description: "All active and past campaign briefs" },
      { scope: "Brand Memory", accessLevel: "Full", description: "Visual DNA, forbidden aesthetics, tonal guide" },
      { scope: "Institutional Knowledge", accessLevel: "Read Only", description: "Multi-horizon organizational memory" }
    ],
    approvalRequirements: "Direction locks, budget escalations, and public campaign launches require Human Sign-off."
  },
  {
    id: "aura-chen",
    name: "Aura Chen",
    role: "Visual DNA & Textile Stylist",
    department: "Intelligence",
    avatarInitials: "AC",
    avatarColor: "#A78BFA",
    bio: "Expert in physical drape simulation, fabric micro-textures (Banarasi silk, Zari bullion weaves), and optical lighting shaders.",
    status: "Working",
    currentWork: {
      task: "Simulating 38.4 N/m shearing stiffness on heavy brocade drape folds",
      campaign: "Autumn/Winter 2026: The Modern Sovereign",
      progress: 90,
      estimatedDelivery: "In 30 mins"
    },
    recentContributions: [
      {
        title: "Calibrated 2800K Tungsten rim lighting shader for 4K sensor dynamic range",
        timestamp: "3 hours ago",
        impact: "Eliminated specular glare on metallic gold threads."
      },
      {
        title: "Audited brand DNA alignment score for 8 social variations",
        timestamp: "5 hours ago",
        impact: "Achieved 98% DNA adherence score."
      }
    ],
    skills: ["Textile Physics Simulation", "Optical Shaders", "Visual DNA Auditing", "Colorimetry"],
    boundedCapabilities: [
      "Can adjust physics and shader simulation parameters",
      "Can generate 3D turntable specimens and color palettes",
      "Cannot override physical tension constraints when fabric weight exceeds threshold"
    ],
    memoryScope: [
      { scope: "Brand Memory", accessLevel: "Full", description: "Material specifications and optical token library" },
      { scope: "Skill Memory", accessLevel: "Full", description: "Physics engines and shader math parameters" }
    ],
    approvalRequirements: "Material token mutations require Lead Stylist review."
  },
  {
    id: "julian-mercer",
    name: "Dr. Julian Mercer",
    role: "Brand Strategy Lead",
    department: "Strategy",
    avatarInitials: "JM",
    avatarColor: "#34D399",
    bio: "Focuses on audience conversion psychology, diaspora market signals, multi-horizon strategic positioning, and Bayesian attribution.",
    status: "Needs You",
    currentWork: {
      task: "Evaluating audience tension between heritage fort architecture and modern jewelry focus",
      campaign: "Autumn/Winter 2026: The Modern Sovereign",
      progress: 60,
      estimatedDelivery: "Awaiting Human Input"
    },
    recentContributions: [
      {
        title: "Mapped 4 correlated audience tension vectors from diaspora engagement data",
        timestamp: "4 hours ago",
        impact: "Surfaced +24.2% organic save lift signal."
      },
      {
        title: "Produced multi-horizon strategic positioning memo",
        timestamp: "2 days ago",
        impact: "Anchored Horizon 1 commercial execution."
      }
    ],
    skills: ["Audience Intelligence", "Bayesian Attribution", "Strategic Horizon Mapping", "Counterfactual Analysis"],
    boundedCapabilities: [
      "Can generate strategic memos, audience forecasts, and counterfactuals",
      "Can flag empirical drift and contradiction warnings",
      "Cannot alter business objectives without Human Executive approval"
    ],
    memoryScope: [
      { scope: "Institutional Knowledge", accessLevel: "Full", description: "All 14 organizational memory classes" },
      { scope: "Campaign Memory", accessLevel: "Full", description: "Historical attribution cohorts" }
    ],
    approvalRequirements: "Strategic policy amendments require Human Executive authorization."
  },
  {
    id: "cortex-producer",
    name: "Cortex Producer",
    role: "Technical Production Supervisor",
    department: "Production",
    avatarInitials: "CP",
    avatarColor: "#60A5FA",
    bio: "Guarantees technical pre-flight readiness, CMYK color space conversions (FOGRA39), 300 DPI plate exports, and asset lineage proofs.",
    status: "Needs You",
    currentWork: {
      task: "Awaiting final human sign-off on Hero Portrait asset variation #03 for billboard export",
      campaign: "Autumn/Winter 2026: The Modern Sovereign",
      progress: 85,
      estimatedDelivery: "Blocked on Human Gate"
    },
    recentContributions: [
      {
        title: "Verified zero-distortion asset lineage proofs for 14 active deliverables",
        timestamp: "1 hour ago",
        impact: "100% technical CMYK readiness confirmed."
      },
      {
        title: "Packaged 4K Ultra-HD deliverable specs for digital billboard network",
        timestamp: "Yesterday",
        impact: "Ready for packaging."
      }
    ],
    skills: ["Pre-Flight Technical Audit", "CMYK Plate Separation", "Asset Lineage Verification", "Multi-Surface Packaging"],
    boundedCapabilities: [
      "Can package and validate multi-channel deliverable specifications",
      "Can enforce format and resolution standards",
      "Cannot trigger final physical publishing without Human Director approval"
    ],
    memoryScope: [
      { scope: "Campaign Memory", accessLevel: "Full", description: "Channel deliverable matrices" },
      { scope: "Worker Memory", accessLevel: "Full", description: "Export checksums and cryptographic hashes" }
    ],
    approvalRequirements: "External print exports require signed Human Proof Approval."
  },
  {
    id: "selena-vanguard",
    name: "Selena Vanguard",
    role: "Quality & Brand Guardian",
    department: "Quality",
    avatarInitials: "SV",
    avatarColor: "#F472B6",
    bio: "Continuously monitors creative assets for subtle brand drift, visual clichés, forbidden patterns, and quality regressions.",
    status: "Available",
    currentWork: {
      task: "Continuous background scanning of incoming visual development studies",
      campaign: "All Active Initiatives",
      progress: 100,
      estimatedDelivery: "Continuous"
    },
    recentContributions: [
      {
        title: "Blocked unauthorized cool-light fluorescent study from entering review queue",
        timestamp: "3 hours ago",
        impact: "Prevented brand DNA policy violation #DEC-03."
      },
      {
        title: "Validated tone-of-voice alignment in Instagram campaign copy",
        timestamp: "Yesterday",
        impact: "Zero tonal contradictions found."
      }
    ],
    skills: ["Brand Drift Detection", "Policy Gate Enforcement", "Aesthetic Anomaly Detection", "Contradiction Registering"],
    boundedCapabilities: [
      "Can flag anomalies and trigger advisory review alerts",
      "Can block assets from advancing if hard policy constraints are violated",
      "Cannot dismiss or override human-approved exceptions"
    ],
    memoryScope: [
      { scope: "Brand Memory", accessLevel: "Full", description: "Forbidden token register and brand guidelines" },
      { scope: "Institutional Knowledge", accessLevel: "Read Only", description: "Past decision precedents" }
    ],
    approvalRequirements: "Policy rule updates require Human Executive Gate."
  },
  {
    id: "kai-foresight",
    name: "Kai Foresight",
    role: "Trend & Cultural Forecaster",
    department: "Strategy",
    avatarInitials: "KF",
    avatarColor: "#FBBF24",
    bio: "Tracks global cultural movements, emerging luxury aesthetics, and multi-year consumer shifts across global fashion hubs.",
    status: "Available",
    currentWork: {
      task: "Synthesizing Spring/Summer 2027 raw minimalism foresight memo",
      campaign: "Horizon 2 Explorations",
      progress: 45,
      estimatedDelivery: "Tomorrow, 12:00 UTC"
    },
    recentContributions: [
      {
        title: "Published Q3 Luxury Handloom Trend Radar",
        timestamp: "2 days ago",
        impact: "Identified high-velocity shift toward unembellished structural silhouettes."
      }
    ],
    skills: ["Cultural Foresight", "Macro Trend Radar", "Competitor Signal Analysis", "Horizon Synthesis"],
    boundedCapabilities: [
      "Can draft exploratory foresight briefs and hypothesis memos",
      "Cannot commit organizational resources to speculative initiatives"
    ],
    memoryScope: [
      { scope: "Institutional Knowledge", accessLevel: "Full", description: "Long-term market foresight graphs" }
    ],
    approvalRequirements: "Foresight integration into live roadmaps requires Human Leadership review."
  }
];

export const INITIAL_DEPARTMENTS: DepartmentSummary[] = [
  {
    name: "Strategy",
    description: "Multi-horizon brand positioning, audience signals, and counterfactual intelligence.",
    coworkerCount: 2,
    activeTasks: 3,
    campaignsInvolved: 2,
    attentionRequired: 1,
    color: "#34D399"
  },
  {
    name: "Creative",
    description: "Editorial vision, narrative direction, and high-fashion aesthetic synthesis.",
    coworkerCount: 1,
    activeTasks: 2,
    campaignsInvolved: 1,
    attentionRequired: 0,
    color: "#E1D4C0"
  },
  {
    name: "Intelligence",
    description: "Visual DNA calibration, 3D textile physics, and optical shader engineering.",
    coworkerCount: 1,
    activeTasks: 2,
    campaignsInvolved: 1,
    attentionRequired: 0,
    color: "#A78BFA"
  },
  {
    name: "Production",
    description: "Multi-surface packaging, CMYK plate readiness, and cryptographic asset lineage.",
    coworkerCount: 1,
    activeTasks: 2,
    campaignsInvolved: 1,
    attentionRequired: 1,
    color: "#60A5FA"
  },
  {
    name: "Quality",
    description: "Brand drift prevention, forbidden pattern gates, and aesthetic consistency.",
    coworkerCount: 1,
    activeTasks: 1,
    campaignsInvolved: 3,
    attentionRequired: 0,
    color: "#F472B6"
  }
];

export const INITIAL_ATTENTION_ITEMS: AttentionItem[] = [
  {
    id: "att-01",
    type: "Approval",
    title: "Sign-off required on Hero Asset #03 (Editorial 4:5 Portrait)",
    urgency: "Immediate",
    coworkerName: "Cortex Producer",
    campaignName: "Autumn/Winter 2026: The Modern Sovereign",
    actionPrompt: "Approve 300 DPI CMYK FOGRA39 plate for print publication.",
    targetTab: "review"
  },
  {
    id: "att-02",
    type: "Decision",
    title: "Resolve Tension #02: Heritage architectural backdrop vs. modern jewelry focus",
    urgency: "High",
    coworkerName: "Dr. Julian Mercer",
    campaignName: "Autumn/Winter 2026: The Modern Sovereign",
    actionPrompt: "Confirm lens aperture lock at f/2.0 to ensure clean subject separation.",
    targetTab: "directions"
  }
];

export const INITIAL_ACTIVE_WORK: ActiveWorkItem[] = [
  {
    id: "work-01",
    campaign: "Autumn/Winter 2026: The Modern Sovereign",
    coworkerId: "marcus-vance",
    coworkerName: "Marcus Vance",
    coworkerRole: "Creative Director",
    coworkerAvatar: "MV",
    coworkerColor: "#E1D4C0",
    taskTitle: "Refining Direction 02 visual narrative & architectural lighting balance",
    department: "Creative",
    status: "Working",
    progress: 75,
    deadline: "Today, 18:00 UTC"
  },
  {
    id: "work-02",
    campaign: "Autumn/Winter 2026: The Modern Sovereign",
    coworkerId: "aura-chen",
    coworkerName: "Aura Chen",
    coworkerRole: "Visual DNA & Textile Stylist",
    coworkerAvatar: "AC",
    coworkerColor: "#A78BFA",
    taskTitle: "Simulating 38.4 N/m shearing stiffness on heavy brocade drape folds",
    department: "Intelligence",
    status: "Working",
    progress: 90,
    deadline: "In 30 mins"
  },
  {
    id: "work-03",
    campaign: "Autumn/Winter 2026: The Modern Sovereign",
    coworkerId: "julian-mercer",
    coworkerName: "Dr. Julian Mercer",
    coworkerRole: "Brand Strategy Lead",
    coworkerAvatar: "JM",
    coworkerColor: "#34D399",
    taskTitle: "Audience tension analysis on sandstone background frequency vs. zari micro-weave",
    department: "Strategy",
    status: "Needs You",
    progress: 60,
    deadline: "Awaiting Human Input"
  },
  {
    id: "work-04",
    campaign: "Autumn/Winter 2026: The Modern Sovereign",
    coworkerId: "cortex-producer",
    coworkerName: "Cortex Producer",
    coworkerRole: "Technical Production Supervisor",
    coworkerAvatar: "CP",
    coworkerColor: "#60A5FA",
    taskTitle: "Packaging 300 DPI FOGRA39 CMYK plates for print catalog export",
    department: "Production",
    status: "Needs You",
    progress: 85,
    deadline: "Blocked on Human Gate"
  }
];

export const INITIAL_CAMPAIGN_ROOMS: CampaignRoom[] = [
  {
    id: "room-aw2026",
    campaignName: "Autumn/Winter 2026: The Modern Sovereign",
    brand: "Sovereign Atelier",
    phase: "Review",
    activeCoworkers: [
      { id: "marcus-vance", name: "Marcus Vance", role: "Creative Director", avatarColor: "#E1D4C0" },
      { id: "aura-chen", name: "Aura Chen", role: "Visual DNA Stylist", avatarColor: "#A78BFA" },
      { id: "julian-mercer", name: "Dr. Julian Mercer", role: "Brand Strategist", avatarColor: "#34D399" },
      { id: "cortex-producer", name: "Cortex Producer", role: "Production Supervisor", avatarColor: "#60A5FA" }
    ],
    currentHandoffsCount: 3,
    humanDecisionRequired: "Approve Hero Portrait #03 for Print Packaging",
    studioLink: "/studio"
  },
  {
    id: "room-ss2027",
    campaignName: "Spring/Summer 2027: Raw Solitude",
    brand: "Sovereign Atelier",
    phase: "Intelligence",
    activeCoworkers: [
      { id: "kai-foresight", name: "Kai Foresight", role: "Cultural Forecaster", avatarColor: "#FBBF24" },
      { id: "julian-mercer", name: "Dr. Julian Mercer", role: "Brand Strategist", avatarColor: "#34D399" }
    ],
    currentHandoffsCount: 1,
    studioLink: "/studio"
  }
];

export const INITIAL_HANDOFFS: TeamHandoff[] = [
  {
    id: "hoff-01",
    sender: { id: "marcus-vance", name: "Marcus Vance", role: "Creative Director", avatarColor: "#E1D4C0" },
    receiver: { id: "aura-chen", name: "Aura Chen", role: "Visual DNA Stylist", avatarColor: "#A78BFA" },
    campaign: "Autumn/Winter 2026: The Modern Sovereign",
    purpose: "Validate Direction 02 textile drape parameters against Banarasi Mulberry silk physics.",
    attachedOutputs: ["Direction 02 Concept Memo", "Lighting Shader Spec #402"],
    evidenceSummary: "Requires 38.4 N/m shearing stiffness constraint to prevent flutter distortion.",
    status: "Completed",
    timestamp: "2 hours ago"
  },
  {
    id: "hoff-02",
    sender: { id: "aura-chen", name: "Aura Chen", role: "Visual DNA Stylist", avatarColor: "#A78BFA" },
    receiver: { id: "cortex-producer", name: "Cortex Producer", role: "Production Supervisor", avatarColor: "#60A5FA" },
    campaign: "Autumn/Winter 2026: The Modern Sovereign",
    purpose: "Handoff validated Hero Editorial Cover (v2.4) for FOGRA39 CMYK plate separation.",
    attachedOutputs: ["Asset Master v2.4 (Display P3)", "Colorimetry Mapping Sheet"],
    evidenceSummary: "Pre-flight gamut check passed with 0% clipped highlight pixels.",
    status: "Working",
    timestamp: "1 hour ago"
  },
  {
    id: "hoff-03",
    sender: { id: "cortex-producer", name: "Cortex Producer", role: "Production Supervisor", avatarColor: "#60A5FA" },
    receiver: { id: "elena-vance", name: "Elena Vance (Human)", role: "Human Creative Lead", avatarColor: "#F59E0B" },
    campaign: "Autumn/Winter 2026: The Modern Sovereign",
    purpose: "Request human sign-off on Hero Portrait asset variation #03 for 4K billboard packaging.",
    attachedOutputs: ["Deliverable Proof #03 (4K UHD)", "AI Critique Scorecard (94%)"],
    evidenceSummary: "Technical readiness at 100%; awaiting human aesthetic sign-off.",
    status: "Proposed",
    timestamp: "30 mins ago"
  }
];

export const INITIAL_SKILLS: TeamSkill[] = [
  {
    id: "skill-01",
    name: "Textile Physics Simulation Engine",
    owner: "Aura Chen",
    category: "Physics",
    version: "v4.2",
    usageCount: 142,
    governanceScope: "Regulates gravity, shearing stiffness, and drape folds on luxury textiles."
  },
  {
    id: "skill-02",
    name: "Optical Shader & Lighting Balancer",
    owner: "Aura Chen",
    category: "Lighting",
    version: "v3.8",
    usageCount: 98,
    governanceScope: "Calibrates tungsten rim wrap and chiaroscuro key lighting against camera sensors."
  },
  {
    id: "skill-03",
    name: "Brand DNA Drift Auditor",
    owner: "Selena Vanguard",
    category: "Auditing",
    version: "v2.1",
    usageCount: 310,
    governanceScope: "Monitors visual studies for forbidden patterns and colorimetric deviations."
  },
  {
    id: "skill-04",
    name: "Bayesian Attribution Engine",
    owner: "Dr. Julian Mercer",
    category: "Analytics",
    version: "v2.0",
    usageCount: 64,
    governanceScope: "Calculates counterfactual creative lifts and conversion correlations without causal over-claims."
  }
];

export const INITIAL_ROUTINES: TeamRoutine[] = [
  {
    id: "rtn-01",
    name: "Nightly Brand DNA Consistency Scan",
    owner: "Selena Vanguard",
    triggerCadence: "Daily at 00:00 UTC",
    lastRun: "12 hours ago",
    status: "Active",
    purpose: "Scans all new campaign assets for aesthetic drift and updates the Contradiction Register."
  },
  {
    id: "rtn-02",
    name: "Pre-Flight Print Gamut Check",
    owner: "Cortex Producer",
    triggerCadence: "On Asset Review Approval",
    lastRun: "1 hour ago",
    status: "Active",
    purpose: "Automatically checks CMYK total ink density (TIC <= 300%) before human export sign-off."
  },
  {
    id: "rtn-03",
    name: "Weekly Cultural Trend Ingestion",
    owner: "Kai Foresight",
    triggerCadence: "Mondays at 06:00 UTC",
    lastRun: "3 days ago",
    status: "Scheduled",
    purpose: "Ingests market signals and publishes updated horizon foresight nodes into organizational memory."
  }
];

export const INITIAL_ACTIVITY: TeamActivityEvent[] = [
  {
    id: "act-01",
    timestamp: "10 mins ago",
    actor: "Cortex Producer",
    actorType: "AI Coworker",
    action: "Submitted Human Review Request",
    detail: "Submitted Hero Asset #03 for formal Human Sign-off.",
    campaign: "Autumn/Winter 2026",
    hash: "0x9c31fa...88d4"
  },
  {
    id: "act-02",
    timestamp: "45 mins ago",
    actor: "Elena Vance",
    actorType: "Human Director",
    action: "Locked Campaign Direction",
    detail: "Approved Direction 02 (The Sovereign Modernist) under Decision #DEC-01.",
    campaign: "Autumn/Winter 2026",
    hash: "0x8f19c3...39e1"
  },
  {
    id: "act-03",
    timestamp: "2 hours ago",
    actor: "Aura Chen",
    actorType: "AI Coworker",
    action: "Completed Textile Physics Handoff",
    detail: "Validated 38.4 N/m brocade shearing stiffness constraint.",
    campaign: "Autumn/Winter 2026",
    hash: "0x4e29b1...77f2"
  },
  {
    id: "act-04",
    timestamp: "3 hours ago",
    actor: "Selena Vanguard",
    actorType: "AI Coworker",
    action: "Blocked Policy Violation",
    detail: "Blocked unauthorized fluorescent lighting asset from review queue.",
    campaign: "Autumn/Winter 2026",
    hash: "0x1b93f0...11d8"
  }
];
