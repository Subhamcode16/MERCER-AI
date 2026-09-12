// ============================================================================
// ❖ VYREN CAMPAIGN STUDIO — DOMAIN MODELS & CENTRALIZED MOCK FIXTURES
// ============================================================================

export type EpistemicStatus = 
  | 'Observed' 
  | 'Supported' 
  | 'Experimental' 
  | 'Correlated' 
  | 'Unknown';

export type AssetApprovalState = 
  | 'Draft' 
  | 'In Review' 
  | 'Approved' 
  | 'Rejected' 
  | 'Superseded' 
  | 'Production Ready';

export type ShotFamily = 
  | 'Hero' 
  | 'Detail' 
  | 'Portrait' 
  | 'Product' 
  | 'Editorial' 
  | 'Social';

export interface WorkerContribution {
  id: string;
  name: string;
  role: string;
  avatarColor: string;
  currentTask: string;
  recentContribution: string;
  nextHandoff: string;
  status: 'active' | 'evaluating' | 'idle' | 'awaiting_human_gate';
}

export interface IntelligenceItem {
  id: string;
  category: 'Audience Signal' | 'Brand Context' | 'Textile Physics' | 'Optical Lighting' | 'Strategic Tension';
  title: string;
  summary: string;
  epistemicStatus: EpistemicStatus;
  confidenceScore: number;
  evidenceSource: string;
  tensionNote?: string;
  actionableImplication: string;
}

export interface CreativeDirection {
  id: string;
  tag: '01' | '02' | '03';
  title: string;
  archetype: 'Controlled Evolution' | 'Contemporary Reinterpretation' | 'Controlled Departure';
  subtitle: string;
  coreIdea: string;
  narrative: string;
  visualLanguage: string;
  composition: string;
  lighting: string;
  materialTreatment: string;
  audienceRationale: string;
  brandAlignmentScore: number;
  distinctivenessScore: number;
  risksAndTensions: string[];
  evidencePillars: string[];
  decisionStatus: 'draft' | 'selected' | 'refined' | 'rejected';
  badge: string;
}

export interface VisualStudy {
  id: string;
  shotFamily: ShotFamily;
  title: string;
  aspectRatio: '16:9' | '4:5' | '9:16' | '1:1';
  lensSpec: string;
  aperture: string;
  lightingShader: string;
  drapePhysics: {
    material: string;
    shearingStiffness: number;
    bendingModulus: number;
    gravityInfluence: string;
  };
  colorPalette: {
    hex: string;
    name: string;
    weight: string;
  }[];
  imageUrl: string;
  dnaAdherenceScore: number;
  notes: string;
}

export interface StudioAsset {
  id: string;
  title: string;
  directionId: string;
  shotFamily: ShotFamily;
  version: string;
  channel: 'Instagram 9:16' | 'Editorial 4:5' | 'Print Catalog 300DPI' | 'OOH Billboard 4K';
  aspectRatio: string;
  status: AssetApprovalState;
  humanApproval: {
    approvedBy?: string;
    approvedAt?: string;
    notes?: string;
  };
  lineageHash: string;
  previewUrl: string;
  specSummary: string;
}

export interface StudioReview {
  id: string;
  assetId: string;
  aiCritique: {
    visualAlignment: number;
    brandDnaScore: number;
    campaignFit: number;
    technicalReadiness: number;
    detectedIssues: string[];
    evidenceNotes: string;
  };
  humanDecision: {
    state: 'Pending Human Decision' | 'Approved' | 'Revision Requested' | 'Rejected';
    decisionMaker?: string;
    timestamp?: string;
    instructions?: string;
  };
}

export interface StudioProductionDeliverable {
  channel: string;
  format: string;
  resolution: string;
  colorSpace: 'sRGB' | 'Display P3' | 'CMYK (FOGRA39)';
  dpi: number;
  assetsReady: number;
  totalRequired: number;
  readinessStatus: 'Ready' | 'Packaging' | 'Awaiting Asset Approval' | 'Blocked';
}

export interface StudioOutcome {
  metric: string;
  observedLift: string;
  counterfactualBaseline: string;
  attributionConfidence: number;
  epistemicNote: string;
  survivingUnknowns: string[];
  learningCandidates: string[];
}

export interface CampaignStudioModel {
  id: string;
  name: string;
  brand: string;
  objective: string;
  audience: string;
  channels: string[];
  status: 'In Development' | 'In Review' | 'Production Ready' | 'Active Live';
  humanOwner: {
    name: string;
    role: string;
    avatar: string;
    hasFinalAuthority: boolean;
  };
  activeCrew: WorkerContribution[];
  lockedDecisions: {
    id: string;
    title: string;
    decidedBy: string;
    timestamp: string;
    cryptographicProof: string;
  }[];
  prioritizedActions: {
    id: string;
    title: string;
    severity: 'High' | 'Medium' | 'Low';
    assignedTo: string;
    dueTimeline: string;
  }[];
  intelligence: IntelligenceItem[];
  directions: CreativeDirection[];
  visualStudies: VisualStudy[];
  assets: StudioAsset[];
  reviews: StudioReview[];
  productionDeliverables: StudioProductionDeliverable[];
  outcomes: StudioOutcome[];
}

// ============================================================================
// FLAGSHIP MOCK CAMPAIGN FIXTURE
// ============================================================================

export const INITIAL_CAMPAIGN_FIXTURE: CampaignStudioModel = {
  id: "camp-aw2026-sovereign",
  name: "Autumn/Winter 2026: The Modern Sovereign",
  brand: "Sovereign Atelier",
  objective: "Accelerate high-intent Next-Gen luxury bridal acquisition across digital editorial and high-impact physical surfaces.",
  audience: "Next-Gen Luxury Patrons (Ages 24–36), High-Aesthetic Global Diaspora",
  channels: ["Instagram 9:16", "Editorial 4:5", "Print Catalog 300DPI", "OOH Billboard 4K"],
  status: "In Development",
  humanOwner: {
    name: "Elena Vance",
    role: "Human Creative Director & Account Lead",
    avatar: "EV",
    hasFinalAuthority: true
  },
  activeCrew: [
    {
      id: "worker-cd",
      name: "Marcus Vance",
      role: "AI Creative Director",
      avatarColor: "#E1D4C0",
      currentTask: "Refining Direction 02 visual narrative & architectural lighting balance",
      recentContribution: "Synthesized 3 comparative creative direction hypotheses with trade-off matrices",
      nextHandoff: "Submitting Direction 02 to Human Decision Gate for formal lock",
      status: "active"
    },
    {
      id: "worker-vi",
      name: "Aura-7",
      role: "Visual DNA Intelligence",
      avatarColor: "#A78BFA",
      currentTask: "Validating Banarasi zari micro-sheen reflection angles against optical shaders",
      recentContribution: "Enforced 38% shearing stiffness constraint on heavy brocade drape simulation",
      nextHandoff: "Calibrating 4K OOH render lighting shaders with CMYK color profile",
      status: "active"
    },
    {
      id: "worker-strat",
      name: "Dr. K. Mercer",
      role: "Lead Strategic Analyst",
      avatarColor: "#34D399",
      currentTask: "Tracking audience resonance signals and Bayesian attribution lifts",
      recentContribution: "Mapped 4 correlated audience tension vectors from diaspora engagement data",
      nextHandoff: "Preparing counterfactual simulation report for post-launch learning",
      status: "evaluating"
    },
    {
      id: "worker-prod",
      name: "Cortex Producer",
      role: "Technical Production Supervisor",
      avatarColor: "#60A5FA",
      currentTask: "Packaging 300 DPI FOGRA39 CMYK plates for print catalog export",
      recentContribution: "Verified zero-distortion asset lineage proof for 14 active deliverables",
      nextHandoff: "Awaiting final human sign-off on Hero Portrait asset variation #03",
      status: "awaiting_human_gate"
    }
  ],
  lockedDecisions: [
    {
      id: "dec-01",
      title: "Archetype selection: Direction 02 (Contemporary Reinterpretation) locked as primary campaign baseline",
      decidedBy: "Elena Vance (Creative Director)",
      timestamp: "2026-09-12 18:40 UTC",
      cryptographicProof: "0x8f19c3b01a7d...39e1"
    },
    {
      id: "dec-02",
      title: "Lighting Constraint: Tungsten directional key + Ethereal rim wrap locked to preserve Zari metallic micro-contrast",
      decidedBy: "Elena Vance (Creative Director)",
      timestamp: "2026-09-12 19:15 UTC",
      cryptographicProof: "0x4e29b191c94b...77f2"
    },
    {
      id: "dec-03",
      title: "Banned Visual Pattern: Cold fluorescent daylight washes strictly prohibited across all shot families",
      decidedBy: "Elena Vance (Creative Director)",
      timestamp: "2026-09-12 20:00 UTC",
      cryptographicProof: "0x1b93f019a8c2...11d8"
    }
  ],
  prioritizedActions: [
    {
      id: "act-01",
      title: "Review & approve Hero Asset #03 (Editorial 4:5 Portrait) for print packaging",
      severity: "High",
      assignedTo: "Elena Vance (Human Owner)",
      dueTimeline: "Immediate Action"
    },
    {
      id: "act-02",
      title: "Evaluate Tension #02: Heritage architectural backdrop vs. modern minimalist jewelry focus",
      severity: "Medium",
      assignedTo: "Creative Team",
      dueTimeline: "Next Sprint"
    },
    {
      id: "act-03",
      title: "Confirm CMYK ink density tolerance with physical print vendor",
      severity: "Low",
      assignedTo: "Cortex Producer",
      dueTimeline: "Pre-Flight"
    }
  ],
  intelligence: [
    {
      id: "intel-01",
      category: "Audience Signal",
      title: "Demand for Modernized Heritage Silhouettes",
      summary: "Diaspora luxury buyers demonstrate 3.4x higher organic save rates for structural, unembellished drapes paired with heritage gold textiles over traditional heavy silhouettes.",
      epistemicStatus: "Observed",
      confidenceScore: 0.94,
      evidenceSource: "Meta Ads & Shopify Conversion Cohorts Q2-Q3 2026",
      actionableImplication: "Prioritize architectural drape folds over busy multi-layer styling in hero shots."
    },
    {
      id: "intel-02",
      category: "Textile Physics",
      title: "Pure Mulberry Silk & Real Zari Weave Resistance",
      summary: "Physical drape simulations confirm Banarasi brocade maintains high resistance to wind-blown flutter, collapsing into stiff parabolic folds when subjected to virtual wind.",
      epistemicStatus: "Supported",
      confidenceScore: 0.98,
      evidenceSource: "VYREN Material Physics Engine v4 (Shearing Stiffness: 38.4 N/m)",
      tensionNote: "Attempting dynamic wind-blown poses will cause unrealistic geometric distortion.",
      actionableImplication: "Enforce static column and architectural waterfall drape configurations."
    },
    {
      id: "intel-03",
      category: "Optical Lighting",
      title: "Warm Tungsten Rim vs. Specular Glare",
      summary: "2800K Tungsten rim lighting with a 15-degree wrap angle highlights metallic micro-threads without blowing out raw sensor dynamic range in 4K resolution.",
      epistemicStatus: "Experimental",
      confidenceScore: 0.89,
      evidenceSource: "Studio Optical Shader Benchmark #704",
      actionableImplication: "Lock key-to-rim ratio at 1:2.4 across all portrait compositions."
    },
    {
      id: "intel-04",
      category: "Strategic Tension",
      title: "Heritage Fort Architecture vs. Minimalist Subject Focus",
      summary: "Intricate sandstone lattice backgrounds compete visually with high-frequency Zari pattern details if depth-of-field exceeds f/4.0.",
      epistemicStatus: "Correlated",
      confidenceScore: 0.82,
      evidenceSource: "Visual Attention Heatmap Model v2",
      tensionNote: "Heritage context adds cultural prestige but risks reducing eye dwell time on garment details.",
      actionableImplication: "Lock lens aperture to f/1.8–f/2.8 to enforce clean optical subject separation."
    },
    {
      id: "intel-05",
      category: "Brand Context",
      title: "Long-term Impact of Dark Moody Aesthetics",
      summary: "Whether moody chiaroscuro lighting reduces broad commercial click-through on lower-funnel social retargeting remains an unresolved empirical question.",
      epistemicStatus: "Unknown",
      confidenceScore: 0.50,
      evidenceSource: "Unresolved Epistemic Boundary — Pending Multivariant A/B Cohort Test",
      actionableImplication: "Keep 2 clean diffused-light social variants in reserve until live attribution signals confirm."
    }
  ],
  directions: [
    {
      id: "dir-01",
      tag: "01",
      title: "The Regal Lineage",
      archetype: "Controlled Evolution",
      subtitle: "Unwavering Heritage & Aristocratic Grandeur",
      coreIdea: "Celebrate classic ceremonial prestige through timeless royal symmetry, heavy golden brocades, and solemn palace architecture.",
      narrative: "A quiet, untouchable sovereign standing in high-relief stone courtyards, embodying generational heritage that requires no explanation.",
      visualLanguage: "Monumental central symmetry, deep umber and gold palette, structured column drapes, dignified posture.",
      composition: "Static geometric center framing, wide focal depth (f/5.6), sandstone arches framing the subject.",
      lighting: "Golden Hour sunset warmth (3200K) with soft atmospheric dust motes.",
      materialTreatment: "Heavy 450 GSM Banarasi silk with uncut gold bullion embroidery, rigid cascading folds.",
      audienceRationale: "Appeals strongly to traditional patriarchs and ceremonial bridal occasions with zero risk of cultural dissonance.",
      brandAlignmentScore: 92,
      distinctivenessScore: 78,
      risksAndTensions: ["May feel overly conventional or dated to younger international diaspora buyers."],
      evidencePillars: ["Historical campaign benchmarks show steady 3.1% baseline conversion."],
      decisionStatus: "draft",
      badge: "TRADITIONAL PILLAR"
    },
    {
      id: "dir-02",
      tag: "02",
      title: "The Sovereign Modernist",
      archetype: "Contemporary Reinterpretation",
      subtitle: "Architectural Precision & Contemporary Splendor",
      coreIdea: "Strip away baroque excess to reveal the stark, razor-sharp sculptural geometry of Indian handloom in modernist architectural spaces.",
      narrative: "The modern woman as sovereign of her own empire: unhurried, razor-sharp, pairing generational textile depth with brutalist concrete and warm raw bronze.",
      visualLanguage: "Asymmetrical tension, negative space dominance, high micro-contrast, stark monolithic forms.",
      composition: "Low-angle hero perspectives, tight optical depth-of-field (f/2.0), severe vertical lines.",
      lighting: "High-contrast Chiaroscuro key light + 2800K Tungsten edge rim wrap cutting against velvet dark shadows.",
      materialTreatment: "High-sheen hand-woven zari silk draped in architectural geometric angles with zero ornament clutter.",
      audienceRationale: "Captures the elusive next-gen luxury consumer looking for modern distinction without discarding artisanal identity.",
      brandAlignmentScore: 98,
      distinctivenessScore: 96,
      risksAndTensions: ["Requires uncompromising lighting execution to prevent shadow crushing on digital feeds."],
      evidencePillars: ["Observed +65.6% net creative lift in prototype diaspora micro-tests."],
      decisionStatus: "selected",
      badge: "HUMAN LOCKED ★"
    },
    {
      id: "dir-03",
      tag: "03",
      title: "Solar Avant-Garde",
      archetype: "Controlled Departure",
      subtitle: "Surreal Optical Geometries & Metallic Refraction",
      coreIdea: "Propel ancient handloom into speculative haute couture through mirrored obsidian pedestals and prismatic sunlight refraction.",
      narrative: "An ethereal future where ancient heritage textiles exist as sacred technological armor in celestial, dreamlike topographies.",
      visualLanguage: "Hyper-specular reflections, liquid metal refractions, surreal floating fabric folds, chromatic aberration.",
      composition: "Extreme Dutch angles, dynamic kinetic framing, ultra-wide 24mm perspective.",
      lighting: "Moody violet rim light + sharp specular laser-cut solar reflections.",
      materialTreatment: "Iridescent metallic weave treated with liquid-like anti-gravity folds.",
      audienceRationale: "Designed for high-impact social viral distinctiveness and fashion editorial magazine covers.",
      brandAlignmentScore: 76,
      distinctivenessScore: 99,
      risksAndTensions: ["High risk of alienating conservative bridal clientele; physics violations if not carefully regulated."],
      evidencePillars: ["High engagement velocity (+42% share rate) on speculative 9:16 reels."],
      decisionStatus: "draft",
      badge: "EXPERIMENTAL DEPARTURE"
    }
  ],
  visualStudies: [
    {
      id: "study-01",
      shotFamily: "Hero",
      title: "Monolithic Sovereign Standing",
      aspectRatio: "4:5",
      lensSpec: "85mm f/1.8 Prime",
      aperture: "f/2.0",
      lightingShader: "Chiaroscuro Tungsten Rim (Shader #402)",
      drapePhysics: {
        material: "Mulberry Silk Brocade (420 GSM)",
        shearingStiffness: 38.4,
        bendingModulus: 44.1,
        gravityInfluence: "Direct Vertical Fall"
      },
      colorPalette: [
        { hex: "#0D0D0E", name: "Obsidian Velvet", weight: "55%" },
        { hex: "#D4AF37", name: "Imperial Gold Zari", weight: "25%" },
        { hex: "#4A151B", name: "Deep Garnet", weight: "15%" },
        { hex: "#E1D4C0", name: "Warm Ivory Highlight", weight: "5%" }
      ],
      imageUrl: "/assets/study_hero_portrait.jpg",
      dnaAdherenceScore: 98,
      notes: "Primary editorial visual anchor. Emphasizes clean neck silhouette and heavy zari pallu geometry."
    },
    {
      id: "study-02",
      shotFamily: "Detail",
      title: "Micro-Weave Zari Macro Study",
      aspectRatio: "1:1",
      lensSpec: "100mm Macro f/2.8",
      aperture: "f/3.2",
      lightingShader: "Specular Directional Grazing Light",
      drapePhysics: {
        material: "Gold Bullion Thread Weave",
        shearingStiffness: 52.0,
        bendingModulus: 60.0,
        gravityInfluence: "Surface Tension Anchor"
      },
      colorPalette: [
        { hex: "#D4AF37", name: "Antique Zari", weight: "60%" },
        { hex: "#1A1A1A", name: "Charcoal Shadow", weight: "30%" },
        { hex: "#8C2B32", name: "Ruby Warp Thread", weight: "10%" }
      ],
      imageUrl: "/assets/study_macro_detail.jpg",
      dnaAdherenceScore: 99,
      notes: "Exposes the authentic hand-loomed imperfections and gold thread density for luxury validation."
    },
    {
      id: "study-03",
      shotFamily: "Social",
      title: "Vertical 9:16 Kinetic Drape Reveal",
      aspectRatio: "9:16",
      lensSpec: "35mm Cine Anamorphic",
      aperture: "f/2.4",
      lightingShader: "Dual Rim Wrap (Tungsten 2800K + Cyan 6500K Ambient)",
      drapePhysics: {
        material: "Mulberry Silk Brocade",
        shearingStiffness: 38.4,
        bendingModulus: 44.1,
        gravityInfluence: "Controlled Slow Descent"
      },
      colorPalette: [
        { hex: "#080808", name: "Deep Studio Black", weight: "60%" },
        { hex: "#E1D4C0", name: "Ivory Sheen", weight: "25%" },
        { hex: "#B8860B", name: "Dark Goldenrod", weight: "15%" }
      ],
      imageUrl: "/assets/study_social_916.jpg",
      dnaAdherenceScore: 95,
      notes: "Optimized for mobile viewing. High eye-level contrast stops social feed scroll."
    }
  ],
  assets: [
    {
      id: "asset-01",
      title: "The Modern Sovereign — Hero Editorial Cover",
      directionId: "dir-02",
      shotFamily: "Hero",
      version: "v2.4",
      channel: "Editorial 4:5",
      aspectRatio: "4:5",
      status: "Approved",
      humanApproval: {
        approvedBy: "Elena Vance",
        approvedAt: "2026-09-12 21:05 UTC",
        notes: "Flawless lighting and textile drape fidelity. Approved for Vogue & Harper's Bazaar placement."
      },
      lineageHash: "0x7a82b9...31f0",
      previewUrl: "/assets/asset_hero_approved.jpg",
      specSummary: "4000x5000 px · Display P3 · 300 DPI"
    },
    {
      id: "asset-02",
      title: "Zari Micro-Weave Craftsmanship Detail",
      directionId: "dir-02",
      shotFamily: "Detail",
      version: "v1.8",
      channel: "Print Catalog 300DPI",
      aspectRatio: "1:1",
      status: "Approved",
      humanApproval: {
        approvedBy: "Elena Vance",
        approvedAt: "2026-09-12 21:10 UTC",
        notes: "Color profile matched FOGRA39 CMYK plates perfectly."
      },
      lineageHash: "0x1d44c8...90a2",
      previewUrl: "/assets/asset_macro_approved.jpg",
      specSummary: "3600x3600 px · CMYK (FOGRA39) · 300 DPI"
    },
    {
      id: "asset-03",
      title: "Architectural Pallu Silhouette — OOH Billboard",
      directionId: "dir-02",
      shotFamily: "Editorial",
      version: "v3.0",
      channel: "OOH Billboard 4K",
      aspectRatio: "16:9",
      status: "In Review",
      humanApproval: {},
      lineageHash: "0x9c31fa...88d4",
      previewUrl: "/assets/asset_ooh_review.jpg",
      specSummary: "7680x4320 px · 4K UHD Master · sRGB"
    },
    {
      id: "asset-04",
      title: "Reels Drape Reveal — Kinetic Story variation B",
      directionId: "dir-02",
      shotFamily: "Social",
      version: "v1.2",
      channel: "Instagram 9:16",
      aspectRatio: "9:16",
      status: "Production Ready",
      humanApproval: {
        approvedBy: "Elena Vance",
        approvedAt: "2026-09-12 21:20 UTC"
      },
      lineageHash: "0x33b8a1...55e9",
      previewUrl: "/assets/asset_story_ready.jpg",
      specSummary: "2160x3840 px · 60fps MP4 Master"
    }
  ],
  reviews: [
    {
      id: "rev-01",
      assetId: "asset-03",
      aiCritique: {
        visualAlignment: 94,
        brandDnaScore: 98,
        campaignFit: 96,
        technicalReadiness: 92,
        detectedIssues: [
          "Minor shadow banding in deep obsidian quadrant at 4K scale — recommend 16-bit dither pass.",
          "Zari highlight specular sharpness exceeds web standard, but fits 300 DPI print tolerance."
        ],
        evidenceNotes: "AI Critique generated against Brand DNA Policy #AW26-Sovereign-v2."
      },
      humanDecision: {
        state: "Pending Human Decision",
        instructions: "Awaiting final human zoom check on left-hand fold drape before locking billboard export."
      }
    }
  ],
  productionDeliverables: [
    {
      channel: "Instagram Stories & Reels",
      format: "MP4 / H.264",
      resolution: "2160 x 3840 (9:16)",
      colorSpace: "sRGB",
      dpi: 72,
      assetsReady: 4,
      totalRequired: 4,
      readinessStatus: "Ready"
    },
    {
      channel: "Editorial Print Spreads",
      format: "TIFF / CMYK Uncompressed",
      resolution: "4800 x 6000 (4:5)",
      colorSpace: "CMYK (FOGRA39)",
      dpi: 300,
      assetsReady: 3,
      totalRequired: 4,
      readinessStatus: "Packaging"
    },
    {
      channel: "OOH Digital Billboard Network",
      format: "ProRes 4444 Master",
      resolution: "7680 x 4320 (16:9)",
      colorSpace: "Display P3",
      dpi: 300,
      assetsReady: 1,
      totalRequired: 2,
      readinessStatus: "Awaiting Asset Approval"
    }
  ],
  outcomes: [
    {
      metric: "Observed High-Intent CTR",
      observedLift: "+24.2%",
      counterfactualBaseline: "1.85% (Industry Baseline 1.49%)",
      attributionConfidence: 0.94,
      epistemicNote: "Observed across 12,400 audited impressions in London & NYC diaspora cohorts.",
      survivingUnknowns: [
        "Long-term post-click brand recall persistence beyond 90-day window",
        "Cross-surface cannibalization between Instagram 9:16 and Print Lookbook"
      ],
      learningCandidates: [
        "Architectural low-key lighting with tungsten rim produces 1.7x higher average dwell time than daylight setups.",
        "Highlighting hand-loomed gold weave details directly in the first 2 seconds increases save rate by 38%."
      ]
    },
    {
      metric: "Observed Brand Distinctiveness Lift",
      observedLift: "+18.5%",
      counterfactualBaseline: "72.4 (Generic Category Benchmark)",
      attributionConfidence: 0.88,
      epistemicNote: "Measured via visual recall testing and proprietary Distinctiveness Vector score.",
      survivingUnknowns: [
        "Resonance velocity in domestic tier-2 bridal markets",
        "Competitor imitation latency for asymmetric architectural folds"
      ],
      learningCandidates: [
        "Banning traditional ornate background props increases perception of high-ticket luxury exclusivity."
      ]
    }
  ]
};
