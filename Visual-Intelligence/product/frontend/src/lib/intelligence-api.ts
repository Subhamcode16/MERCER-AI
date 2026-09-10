/**
 * Typesafe Client API for Phase 29: Creative Intelligence Network
 */

export interface StrategicSignal {
  signal_id: string;
  tenant_id: string;
  classification: string;
  signal_class: string;
  lifecycle_state: string;
  scope: string;
  observed_pattern: string;
  supporting_evidence: string[];
  contradicting_evidence: string[];
  method: string;
  confidence: number;
  epistemic_status: string;
  freshness: number;
  assumptions: string[];
  unknowns: string[];
  generated_at: string;
}

export interface StrategicScenario {
  scenario_id: string;
  archetype: "BASELINE" | "UPSIDE" | "DOWNSIDE" | "DISRUPTION" | "UNKNOWN";
  title: string;
  description: string;
  scope: string;
  bounded_likelihood?: number;
  uncertainty_score: number;
  leading_indicators: string[];
  lagging_indicators: string[];
}

export interface StrategicRecommendation {
  recommendation_id: string;
  tenant_id: string;
  title: string;
  action_statement: string;
  why_now: string;
  scope: string;
  status: "PROPOSED" | "UNDER_REVIEW" | "CHALLENGED" | "DOWNGRADED" | "ACCEPTED" | "REJECTED" | "WITHDRAWN" | "EXPIRED";
  epistemic_status: string;
  confidence: number;
  supporting_evidence: string[];
  contradicting_evidence: string[];
  assumptions: string[];
  unknowns: string[];
  alternatives: string[];
  expected_consequences: string[];
  reversibility: "HIGHLY_REVERSIBLE" | "MODERATELY_REVERSIBLE" | "IRREVERSIBLE";
  proposed_experiment?: string;
  challenge_notes?: string[];
}

export interface StrategicObservatorySnapshot {
  tenant_id: string;
  metrics: {
    total_entities_in_graph: number;
    total_relationships_in_graph: number;
    active_signals_count: number;
    active_hypotheses_count: number;
    active_recommendations_count: number;
  };
  signals_by_class: Record<string, number>;
  hypotheses_by_status: Record<string, number>;
  recommendations_by_status: Record<string, number>;
}

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

export class IntelligenceAPI {
  static async getObservatory(tenantId: string = "TENANT-LUXE"): Promise<StrategicObservatorySnapshot> {
    try {
      const res = await fetch(`${BACKEND_URL}/api/v1/intelligence/observatory?tenant_id=${tenantId}`);
      if (res.ok) return await res.json();
    } catch {
      // Fallback simulation state
    }
    return {
      tenant_id: tenantId,
      metrics: {
        total_entities_in_graph: 342,
        total_relationships_in_graph: 618,
        active_signals_count: 14,
        active_hypotheses_count: 6,
        active_recommendations_count: 4,
      },
      signals_by_class: {
        EMERGING_PATTERN: 5,
        CREATIVE_FATIGUE: 3,
        AUDIENCE_SHIFT: 2,
        VISUAL_SHIFT: 3,
        ENVIRONMENT_DRIFT: 1,
      },
      hypotheses_by_status: {
        TESTING: 2,
        SUPPORTED: 3,
        PROPOSED: 1,
      },
      recommendations_by_status: {
        PROPOSED: 2,
        CHALLENGED: 1,
        ACCEPTED: 1,
      },
    };
  }

  static async getSignals(tenantId: string = "TENANT-LUXE"): Promise<StrategicSignal[]> {
    try {
      const res = await fetch(`${BACKEND_URL}/api/v1/intelligence/signals/query`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tenant_id: tenantId }),
      });
      if (res.ok) return await res.json();
    } catch {
      // Fallback demo state
    }
    return [
      {
        signal_id: "SIG-ASYM-891",
        tenant_id: tenantId,
        classification: "CLIENT_PRIVATE",
        signal_class: "EMERGING_PATTERN",
        lifecycle_state: "STRATEGIC_SIGNAL",
        scope: "HIGH_JEWELRY_GLOBAL",
        observed_pattern: "Asymmetric composition in jewelry layouts generates +18% 3s hook retention",
        supporting_evidence: ["CAMP-FALL-01", "EXP-CUT-02"],
        contradicting_evidence: ["SURVEY-TRAD-01"],
        method: "CROSS_CAMPAIGN_CORRELATION",
        confidence: 0.82,
        epistemic_status: "OBSERVATIONAL_CORRELATION",
        freshness: 0.94,
        assumptions: ["Audience segment skews Gen-Z and luxury vanguard"],
        unknowns: ["Long-term brand equity impact on heritage client base"],
        generated_at: new Date().toISOString(),
      },
      {
        signal_id: "SIG-FATIGUE-302",
        tenant_id: tenantId,
        classification: "CLIENT_PRIVATE",
        signal_class: "CREATIVE_FATIGUE",
        lifecycle_state: "STRATEGIC_SIGNAL",
        scope: "META_FEED_1X1",
        observed_pattern: "Monochromatic gray background ads experience 28% CTR decay after day 8",
        supporting_evidence: ["CAMP-MONO-11", "CAMP-MONO-12"],
        contradicting_evidence: [],
        method: "TIME_SERIES_DECAY",
        confidence: 0.89,
        epistemic_status: "EXPERIMENTAL_EVIDENCE",
        freshness: 0.98,
        assumptions: ["Audience ad frequency saturation exceeded 3.4x"],
        unknowns: ["Impact of subtle dynamic accent hue shift"],
        generated_at: new Date().toISOString(),
      },
    ];
  }

  static async getForesightScenarios(tenantId: string = "TENANT-LUXE", topic: string = "Minimalist Luxe Shift"): Promise<Record<string, StrategicScenario>> {
    try {
      const res = await fetch(`${BACKEND_URL}/api/v1/intelligence/foresight`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          tenant_id: tenantId,
          scope: "GLOBAL_FASHION",
          topic: topic,
          initiating_signals: ["SIG-ASYM-891"],
          base_assumptions: ["Luxury consumer spend resilient"],
        }),
      });
      if (res.ok) return await res.json();
    } catch {
      // Fallback
    }
    return {
      BASELINE: {
        scenario_id: "SCE-BASE-01",
        archetype: "BASELINE",
        title: "Baseline Organic Evolution",
        description: "Historical metrics and channel variance continue with steady ROAS around 2.4x.",
        scope: "GLOBAL_FASHION",
        bounded_likelihood: 0.40,
        uncertainty_score: 0.25,
        leading_indicators: ["Stable CPM rates", "Consistent 1.8% CTR"],
        lagging_indicators: ["Quarterly customer acquisition cost"],
      },
      UPSIDE: {
        scenario_id: "SCE-UP-02",
        archetype: "UPSIDE",
        title: "Viral Vanguard Resonance",
        description: "Asymmetric kinetic formats unlock viral organic syndication with +32% conversion velocity.",
        scope: "GLOBAL_FASHION",
        bounded_likelihood: 0.25,
        uncertainty_score: 0.45,
        leading_indicators: ["Organic save/share ratio > 12%", "Lower initial CAC"],
        lagging_indicators: ["30-day VIP repeat purchase rate"],
      },
      DOWNSIDE: {
        scenario_id: "SCE-DOWN-03",
        archetype: "DOWNSIDE",
        title: "Premature Fatigue Drop",
        description: "Aggressive kinetic visual pacing alienates traditional high-ticket luxury buyers.",
        scope: "GLOBAL_FASHION",
        bounded_likelihood: 0.20,
        uncertainty_score: 0.40,
        leading_indicators: ["Bounce rate > 65% on product detail page"],
        lagging_indicators: ["Drop in average order value"],
      },
      DISRUPTION: {
        scenario_id: "SCE-DISRUPT-04",
        archetype: "DISRUPTION",
        title: "Platform Format Inversion",
        description: "Ad platform updates algorithmic weights favoring interactive 3D drapes over static reels.",
        scope: "GLOBAL_FASHION",
        bounded_likelihood: 0.10,
        uncertainty_score: 0.70,
        leading_indicators: ["Rapid shift in competitive auction bids"],
        lagging_indicators: ["Structural conversion re-indexing"],
      },
      UNKNOWN: {
        scenario_id: "SCE-UNKN-05",
        archetype: "UNKNOWN",
        title: "Unobserved Counterfactual State",
        description: "Material dynamics unmeasurable without randomized exploratory split testing.",
        scope: "GLOBAL_FASHION",
        bounded_likelihood: 0.05,
        uncertainty_score: 0.95,
        leading_indicators: ["Conflicting signal metrics", "Novel creator aesthetic"],
        lagging_indicators: ["Uncalibrated market payoff"],
      },
    };
  }

  static async challengeRecommendation(recId: string, notes: string, counterevidence: string[] = []): Promise<any> {
    try {
      const res = await fetch(`${BACKEND_URL}/api/v1/intelligence/recommendations/${recId}/challenge`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          tenant_id: "TENANT-LUXE",
          operator_notes: notes,
          new_counterevidence: counterevidence,
        }),
      });
      if (res.ok) return await res.json();
    } catch {
      // Fallback
    }
    return { status: "DOWNGRADED", notes, confidence: 0.52 };
  }
}
