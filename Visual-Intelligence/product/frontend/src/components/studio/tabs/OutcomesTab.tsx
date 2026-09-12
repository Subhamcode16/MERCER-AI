"use client";

import React, { useState } from "react";
import { 
  TrendingUp, 
  BarChart3, 
  ShieldAlert, 
  Brain, 
  CheckCircle2, 
  HelpCircle, 
  Sliders, 
  Layers,
  ArrowUpRight
} from "lucide-react";
import type { CampaignStudioModel, StudioOutcome } from "@/lib/campaignStudioFixtures";

interface OutcomesTabProps {
  campaign: CampaignStudioModel;
}

export function OutcomesTab({ campaign }: OutcomesTabProps) {
  const [outcomes, setOutcomes] = useState<StudioOutcome[]>(campaign.outcomes);

  return (
    <div className="space-y-8 animate-in fade-in duration-200">
      
      {/* Surface Header & Epistemic Caution Banner */}
      <div className="p-6 rounded-2xl bg-[#111113]/80 border border-white/10 space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-emerald-400" />
              <h2 className="text-lg font-serif text-white font-medium">Outcome Intelligence & Attribution Lift</h2>
            </div>
            <p className="text-xs text-white/50 font-light">
              Empirical market observations, Bayesian attribution confidence, and candidate learnings for organizational memory.
            </p>
          </div>

          <span className="px-3 py-1.5 rounded-xl bg-purple-500/10 border border-purple-500/20 text-purple-300 text-xs font-mono">
            Bayesian Counterfactual Model v2
          </span>
        </div>

        <div className="p-3.5 rounded-xl bg-black/40 border border-white/5 flex items-center justify-between text-xs text-white/60">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-400" />
            <span>Strict Terminology: <strong className="text-white">Observed Lift</strong> used in place of unsupported causal claims.</span>
          </div>
          <span className="text-[10px] font-mono text-white/40">Epistemic Truth Guard Active</span>
        </div>
      </div>

      {/* Outcome Lift Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {outcomes.map((out, idx) => (
          <div
            key={idx}
            className="p-6 rounded-2xl bg-[#111113]/90 border border-white/10 space-y-6 hover:border-emerald-500/30 transition-all"
          >
            {/* Header & Main Metric */}
            <div className="flex items-start justify-between">
              <div className="space-y-1">
                <span className="text-[10px] font-mono uppercase text-white/40 tracking-wider">Audited Metric</span>
                <h3 className="text-base font-serif text-white font-medium">{out.metric}</h3>
              </div>
              <div className="text-right">
                <div className="text-3xl font-serif text-emerald-400 font-normal">{out.observedLift}</div>
                <span className="text-[10px] font-mono text-emerald-400/70">OBSERVED LIFT</span>
              </div>
            </div>

            {/* Counterfactual Comparison */}
            <div className="p-3.5 rounded-xl bg-white/[0.02] border border-white/5 space-y-1 text-xs">
              <div className="flex items-center justify-between text-[10px] font-mono text-white/40">
                <span>Counterfactual Baseline</span>
                <span>Confidence: {Math.round(out.attributionConfidence * 100)}%</span>
              </div>
              <p className="text-white/80 font-mono font-medium">{out.counterfactualBaseline}</p>
              <p className="text-[11px] text-white/50 font-light">{out.epistemicNote}</p>
            </div>

            {/* Surviving Unknowns & Learning Candidates */}
            <div className="space-y-3 text-xs">
              
              {/* Learning Candidates */}
              <div className="space-y-1.5">
                <span className="text-[10px] font-mono uppercase text-purple-300 tracking-wider flex items-center gap-1.5">
                  <Brain className="w-3 h-3 text-purple-400" /> Organizational Learning Candidates
                </span>
                <ul className="space-y-1 text-white/70">
                  {out.learningCandidates.map((learn, lIdx) => (
                    <li key={lIdx} className="flex items-start gap-2 text-[11px]">
                      <span className="text-purple-400 font-mono">•</span>
                      <span className="font-light">{learn}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Surviving Unknowns */}
              <div className="space-y-1.5 pt-2 border-t border-white/5">
                <span className="text-[10px] font-mono uppercase text-amber-300 tracking-wider flex items-center gap-1.5">
                  <HelpCircle className="w-3 h-3 text-amber-400" /> Surviving Epistemic Unknowns
                </span>
                <ul className="space-y-1 text-white/60">
                  {out.survivingUnknowns.map((unk, uIdx) => (
                    <li key={uIdx} className="flex items-start gap-2 text-[11px]">
                      <span className="text-amber-400 font-mono">•</span>
                      <span className="font-light">{unk}</span>
                    </li>
                  ))}
                </ul>
              </div>

            </div>

          </div>
        ))}
      </div>

    </div>
  );
}
