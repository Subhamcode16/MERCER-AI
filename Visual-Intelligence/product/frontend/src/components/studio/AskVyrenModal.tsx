"use client";

import React, { useState } from "react";
import { 
  Sparkles, 
  X, 
  Search, 
  ShieldAlert, 
  CheckCircle2, 
  HelpCircle, 
  ArrowRight,
  Database,
  Layers,
  FileText
} from "lucide-react";
import type { CampaignStudioModel } from "@/lib/campaignStudioFixtures";

interface AskVyrenModalProps {
  isOpen: boolean;
  onClose: () => void;
  campaign: CampaignStudioModel;
}

export function AskVyrenModal({ isOpen, onClose, campaign }: AskVyrenModalProps) {
  const [selectedPrompt, setSelectedPrompt] = useState<string | null>(null);
  const [customQuery, setCustomQuery] = useState("");
  const [responseView, setResponseView] = useState<{
    title: string;
    summary: string;
    epistemicStatus: string;
    evidence: string[];
    governanceNote: string;
  } | null>(null);

  if (!isOpen) return null;

  const presetQueries = [
    {
      id: 'q1',
      question: "Why was Direction 02 (The Sovereign Modernist) recommended?",
      response: {
        title: "Recommendation Rationale: Direction 02",
        summary: "Direction 02 achieved the optimal Pareto frontier between Brand DNA preservation (98%) and Diaspora distinctiveness lift (+65.6%). It avoids traditional ornate clutter while honoring authentic gold zari craftsmanship.",
        epistemicStatus: "Supported (High Confidence)",
        evidence: [
          "Historical conversion cohort data Q2-Q3 2026 (Shopify/Meta ads)",
          "Material Physics Simulation #402 confirming 38.4 N/m brocade drape stiffness",
          "Visual attention heatmaps showing 3.4x higher dwell time on architectural folds"
        ],
        governanceNote: "Recommendation only. Human authority Elena Vance formally locked this direction under Decision #DEC-01."
      }
    },
    {
      id: 'q2',
      question: "Show supporting evidence for audience signals.",
      response: {
        title: "Audience Signal Evidence Ledger",
        summary: "Data derived from 12,400 audited impressions in London and NYC diaspora luxury buyers reveals a strong pivot towards structural, architectural minimalism over traditional ceremonial heavy embroidery.",
        epistemicStatus: "Observed (Empirical Metric)",
        evidence: [
          "Meta Ads organic save rate: +24.2% lift on architectural drape variations",
          "Customer interview cohorts: 78% indicated high affinity for unembellished silhouettes",
          "Shopify average order value: +34% higher on modern reinterpretations"
        ],
        governanceNote: "Observed correlations do not guarantee absolute causal lift in unmeasured secondary markets."
      }
    },
    {
      id: 'q3',
      question: "What remains unknown in this campaign?",
      response: {
        title: "Surviving Epistemic Unknowns",
        summary: "In accordance with VYREN Invariant 'Unknown Must Survive', two key strategic vectors remain unverified prior to live production rollout.",
        epistemicStatus: "Unknown (Unresolved Boundary)",
        evidence: [
          "Unknown 01: Long-term post-click brand recall persistence beyond the 90-day window",
          "Unknown 02: Cross-surface cannibalization between Instagram 9:16 and Print Lookbook placements",
          "Unknown 03: Lower-funnel conversion elasticity under extreme low-key chiaroscuro lighting"
        ],
        governanceNote: "These unknowns are preserved as open hypotheses for post-launch attribution analysis."
      }
    },
    {
      id: 'q4',
      question: "Develop alternatives without changing locked constraints.",
      response: {
        title: "Bounded Alternative Generation",
        summary: "Within the locked constraints of Tungsten 2800K lighting and Mulberry Silk brocade, two alternate shot framings are mathematically viable without violating brand DNA.",
        epistemicStatus: "Experimental Model Output",
        evidence: [
          "Alternative A: Severe Dutch Angle (15°) with static central drape anchor",
          "Alternative B: Monolithic macro crop highlighting weave imperfections with f/2.8 lens"
        ],
        governanceNote: "Alternative exploration preserves all locked policy gates (#DEC-01, #DEC-02, #DEC-03)."
      }
    }
  ];

  const handleSelectPreset = (preset: typeof presetQueries[0]) => {
    setSelectedPrompt(preset.id);
    setResponseView(preset.response);
  };

  const handleCustomSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!customQuery.trim()) return;
    setSelectedPrompt('custom');
    setResponseView({
      title: `Analysis for: "${customQuery}"`,
      summary: `VYREN Creative Intelligence analyzed your request against campaign "${campaign.name}" and locked brand policies.`,
      epistemicStatus: "Supported by Active Memory",
      evidence: [
        `Aligned with locked Decision #DEC-01 (${campaign.directions.find(d => d.decisionStatus === 'selected')?.title})`,
        `Checked against 14 active organizational memory classes`,
        `Preserved 3 locked brand constraints`
      ],
      governanceNote: "Model recommendations require explicit human approval before altering production parameters."
    });
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-in fade-in duration-150">
      <div className="relative w-full max-w-3xl rounded-2xl bg-[#111113] border border-white/10 shadow-2xl overflow-hidden flex flex-col max-h-[85vh]">
        
        {/* Header */}
        <div className="px-6 py-4 border-b border-white/5 flex items-center justify-between bg-white/[0.02]">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-xl bg-[#E1D4C0]/10 border border-[#E1D4C0]/20 flex items-center justify-center text-[#E1D4C0]">
              <Sparkles className="w-4 h-4" />
            </div>
            <div>
              <h2 className="text-sm font-medium text-white">Ask VYREN Intelligence</h2>
              <p className="text-[10px] font-mono text-white/40">Bounded evidence & provenance queries for {campaign.name}</p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="w-7 h-7 rounded-lg border border-white/5 flex items-center justify-center text-white/40 hover:text-white hover:bg-white/5 transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Content Body */}
        <div className="p-6 overflow-y-auto space-y-6 flex-1 scrollbar-thin scrollbar-thumb-white/10">
          
          {/* Preset Prompts Matrix */}
          <div className="space-y-2">
            <label className="text-[10px] font-mono uppercase tracking-wider text-white/40">
              Select a Bounded Inquiry:
            </label>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
              {presetQueries.map((q) => (
                <button
                  key={q.id}
                  onClick={() => handleSelectPreset(q)}
                  className={`p-3 rounded-xl text-left text-xs transition-all border ${
                    selectedPrompt === q.id
                      ? "bg-[#E1D4C0]/10 border-[#E1D4C0]/40 text-[#E1D4C0]"
                      : "bg-white/[0.02] border-white/5 text-white/70 hover:bg-white/[0.05] hover:text-white"
                  }`}
                >
                  <p className="font-medium leading-snug">{q.question}</p>
                </button>
              ))}
            </div>
          </div>

          {/* Response Evidence Card */}
          {responseView && (
            <div className="p-5 rounded-2xl bg-black/60 border border-[#E1D4C0]/20 space-y-4 animate-in fade-in slide-in-from-bottom-2 duration-200">
              <div className="flex items-center justify-between border-b border-white/5 pb-2.5">
                <h3 className="text-sm font-medium text-white flex items-center gap-2">
                  <FileText className="w-4 h-4 text-[#E1D4C0]" />
                  {responseView.title}
                </h3>
                <span className="px-2 py-0.5 rounded text-[9px] font-mono bg-blue-500/10 text-blue-400 border border-blue-500/20">
                  {responseView.epistemicStatus}
                </span>
              </div>

              <p className="text-xs text-white/80 leading-relaxed font-light">
                {responseView.summary}
              </p>

              {/* Evidence Pillars */}
              <div className="space-y-1.5 pt-1">
                <span className="text-[10px] font-mono uppercase tracking-wider text-white/40 flex items-center gap-1.5">
                  <Database className="w-3 h-3 text-[#E1D4C0]" /> Decision-Relevant Evidence:
                </span>
                <ul className="space-y-1 text-xs text-white/60">
                  {responseView.evidence.map((ev, idx) => (
                    <li key={idx} className="flex items-start gap-2">
                      <span className="text-[#E1D4C0] text-[10px] font-mono mt-0.5">•</span>
                      <span>{ev}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Governance Invariant Alert */}
              <div className="p-3 rounded-xl bg-amber-500/[0.05] border border-amber-500/20 flex items-start gap-2.5 text-[11px] text-amber-200/80">
                <ShieldAlert className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
                <p><span className="font-semibold text-amber-300">Governance Gate:</span> {responseView.governanceNote}</p>
              </div>
            </div>
          )}

          {/* Custom Query Input Box */}
          <form onSubmit={handleCustomSubmit} className="space-y-2">
            <label className="text-[10px] font-mono uppercase tracking-wider text-white/40">
              Or Ask a Bounded Campaign Question:
            </label>
            <div className="flex items-center gap-2">
              <div className="relative flex-1">
                <Search className="w-4 h-4 text-white/40 absolute left-3.5 top-1/2 -translate-y-1/2" />
                <input
                  type="text"
                  value={customQuery}
                  onChange={(e) => setCustomQuery(e.target.value)}
                  placeholder="e.g. Compare Direction 01 and 03 lighting parameters..."
                  className="w-full pl-9 pr-4 py-2.5 rounded-xl bg-white/[0.03] border border-white/10 text-xs text-white placeholder-white/30 focus:outline-none focus:border-[#E1D4C0]/50"
                />
              </div>
              <button
                type="submit"
                className="px-4 py-2.5 rounded-xl bg-[#E1D4C0] text-[#0A0A0A] font-semibold text-xs hover:opacity-90 transition-opacity shrink-0 flex items-center gap-1.5"
              >
                <span>Ask</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </form>

        </div>

        {/* Footer */}
        <div className="px-6 py-3 border-t border-white/5 bg-white/[0.01] flex items-center justify-between text-[10px] font-mono text-white/30">
          <span>Invariants: Model Output &ne; Truth &bull; Recommendation &ne; Decision</span>
          <span>Tenant Isolated &bull; Cryptographic Audit Proof</span>
        </div>

      </div>
    </div>
  );
}
