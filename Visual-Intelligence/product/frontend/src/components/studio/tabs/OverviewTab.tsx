"use client";

import React, { useState } from "react";
import { 
  Target, 
  Brain, 
  Sparkles, 
  AlertCircle, 
  ArrowRight, 
  CheckCircle2, 
  Lock, 
  Layers, 
  ChevronRight,
  Eye,
  Sliders,
  HelpCircle,
  X
} from "lucide-react";
import type { CampaignStudioModel } from "@/lib/campaignStudioFixtures";

interface OverviewTabProps {
  campaign: CampaignStudioModel;
  onNavigateTab: (tab: any) => void;
}

export function OverviewTab({ campaign, onNavigateTab }: OverviewTabProps) {
  const [isReasoningOpen, setIsReasoningOpen] = useState(false);

  return (
    <div className="space-y-8 animate-in fade-in duration-200 pb-20">
      
      {/* 4 Core Human Invariant Questions Bento Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        {/* Question 1: What are we trying to achieve? */}
        <div className="p-7 rounded-2xl bg-[#111113]/80 border border-white/10 space-y-4 relative overflow-hidden group hover:border-[#E1D4C0]/30 transition-all">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-xl bg-[#E1D4C0]/10 text-[#E1D4C0] border border-[#E1D4C0]/20 flex items-center justify-center">
                <Target className="w-4 h-4" />
              </div>
              <div>
                <span className="text-[10px] font-mono uppercase tracking-widest text-[#E1D4C0]/80">Objective</span>
                <h3 className="text-base font-serif text-white font-normal">What are we trying to achieve?</h3>
              </div>
            </div>
            <span className="text-[9px] font-mono px-2 py-0.5 rounded bg-white/5 text-white/50 border border-white/5">
              INTENT
            </span>
          </div>

          <div className="space-y-3 text-xs">
            <div className="p-4 rounded-xl bg-white/[0.02] border border-white/5 space-y-1.5">
              <p className="text-white/90 text-sm font-serif leading-relaxed">
                "{campaign.objective}"
              </p>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div className="p-3 rounded-xl bg-white/[0.02] border border-white/5 space-y-1">
                <span className="text-[10px] font-mono text-white/40 uppercase">Target Audience</span>
                <p className="text-white/80 font-medium truncate">{campaign.audience}</p>
              </div>
              <div className="p-3 rounded-xl bg-white/[0.02] border border-white/5 space-y-1">
                <span className="text-[10px] font-mono text-white/40 uppercase">Release Channels</span>
                <p className="text-[#E1D4C0] font-mono font-medium">{campaign.channels.length} Surfaces Ready</p>
              </div>
            </div>
          </div>
        </div>

        {/* Question 2: What does VYREN understand? */}
        <div className="p-7 rounded-2xl bg-[#111113]/80 border border-white/10 space-y-4 relative overflow-hidden group hover:border-[#E1D4C0]/30 transition-all">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-xl bg-purple-500/10 text-purple-300 border border-purple-500/20 flex items-center justify-center">
                <Brain className="w-4 h-4" />
              </div>
              <div>
                <span className="text-[10px] font-mono uppercase tracking-widest text-purple-400">Synthesis</span>
                <h3 className="text-base font-serif text-white font-normal">What does VYREN understand?</h3>
              </div>
            </div>
            <button 
              onClick={() => setIsReasoningOpen(true)}
              className="text-[11px] font-medium text-[#E1D4C0] hover:underline flex items-center gap-1 transition-colors"
            >
              <span>View reasoning</span>
              <ArrowRight className="w-3 h-3" />
            </button>
          </div>

          <div className="space-y-3 text-xs">
            <div className="p-4 rounded-xl bg-white/[0.02] border border-white/5 space-y-2">
              <p className="text-white/90 leading-relaxed font-light text-[12.5px]">
                Modernized heritage silhouettes show a <strong className="text-emerald-400 font-medium">strong audience signal (+24.2% engagement)</strong>, while dark cinematic lighting remains an unresolved hypothesis.
              </p>
            </div>

            <div className="flex items-center justify-between p-3 rounded-xl bg-white/[0.02] border border-white/5">
              <span className="text-white/70">Textile Physics & Drape Constraints</span>
              <span className="px-2 py-0.5 rounded text-[9px] font-mono bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                LOCKED TO DNA
              </span>
            </div>
          </div>
        </div>

        {/* Question 3: What are we making? */}
        <div className="p-7 rounded-2xl bg-[#111113]/80 border border-white/10 space-y-4 relative overflow-hidden group hover:border-[#E1D4C0]/30 transition-all">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-xl bg-amber-500/10 text-[#E1D4C0] border border-amber-500/20 flex items-center justify-center">
                <Sparkles className="w-4 h-4" />
              </div>
              <div>
                <span className="text-[10px] font-mono uppercase tracking-widest text-[#E1D4C0]">Creative World</span>
                <h3 className="text-base font-serif text-white font-normal">What are we making?</h3>
              </div>
            </div>
            <button 
              onClick={() => onNavigateTab('create')}
              className="text-[11px] font-medium text-[#E1D4C0] hover:underline flex items-center gap-1 transition-colors"
            >
              <span>Explore Visuals</span>
              <ArrowRight className="w-3 h-3" />
            </button>
          </div>

          <div className="space-y-3 text-xs">
            <div className="p-3.5 rounded-xl bg-white/[0.02] border border-white/5 flex items-center justify-between">
              <div>
                <div className="text-white font-medium text-[13px]">Direction: Modern Sovereign</div>
                <p className="text-white/50 text-[11px] font-light mt-0.5">
                  Architectural precision × contemporary restraint × tungsten edge light
                </p>
              </div>
              <span className="px-2.5 py-1 rounded-full text-[10px] font-mono bg-[#E1D4C0]/10 text-[#E1D4C0] border border-[#E1D4C0]/20 shrink-0">
                96% DISTINCT
              </span>
            </div>

            <div className="grid grid-cols-3 gap-2">
              <div className="p-2.5 rounded-lg bg-white/[0.02] border border-white/5 text-center">
                <div className="text-[10px] text-white/40 font-mono">Hero Shot</div>
                <div className="text-white text-xs font-medium mt-0.5">3 Variations</div>
              </div>
              <div className="p-2.5 rounded-lg bg-white/[0.02] border border-white/5 text-center">
                <div className="text-[10px] text-white/40 font-mono">Detail Close-Up</div>
                <div className="text-white text-xs font-medium mt-0.5">4 Studies</div>
              </div>
              <div className="p-2.5 rounded-lg bg-white/[0.02] border border-white/5 text-center">
                <div className="text-[10px] text-white/40 font-mono">Motion Story</div>
                <div className="text-white text-xs font-medium mt-0.5">3 Renders</div>
              </div>
            </div>
          </div>
        </div>

        {/* Question 4: What needs me? */}
        <div className="p-7 rounded-2xl bg-[#111113]/80 border border-white/10 space-y-4 relative overflow-hidden group hover:border-[#E1D4C0]/30 transition-all">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-xl bg-rose-500/10 text-rose-300 border border-rose-500/20 flex items-center justify-center">
                <AlertCircle className="w-4 h-4" />
              </div>
              <div>
                <span className="text-[10px] font-mono uppercase tracking-widest text-rose-400">Human Authority</span>
                <h3 className="text-base font-serif text-white font-normal">What needs me?</h3>
              </div>
            </div>
            <span className="text-[9px] font-mono px-2 py-0.5 rounded bg-rose-500/10 text-rose-400 border border-rose-500/20">
              1 DECISION PENDING
            </span>
          </div>

          <div className="space-y-3 text-xs">
            <div className="p-4 rounded-xl bg-rose-950/10 border border-rose-500/20 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-rose-300 font-medium text-xs">Hero Asset #03 Approval</span>
                <span className="text-[9px] font-mono text-white/40">Print Editorial</span>
              </div>
              <p className="text-white/70 font-light text-[11.5px]">
                VYREN flagged shadow compression on 300 DPI CMYK. Choose whether to approve as-is or generate a print-safe revision.
              </p>
              <div className="flex items-center gap-2 pt-1">
                <button 
                  onClick={() => onNavigateTab('review')}
                  className="px-3 py-1.5 rounded-lg bg-white/10 hover:bg-white/20 text-white text-[11px] font-medium transition-colors flex items-center gap-1"
                >
                  <span>Review Decision</span>
                  <ArrowRight className="w-3 h-3" />
                </button>
              </div>
            </div>
          </div>
        </div>

      </div>

      {/* Progressive Disclosure Reasoning Modal */}
      {isReasoningOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md">
          <div className="w-full max-w-xl rounded-2xl bg-[#141416] border border-white/10 p-6 space-y-5 shadow-2xl animate-in zoom-in-95 duration-150">
            <div className="flex items-center justify-between border-b border-white/5 pb-3">
              <div className="flex items-center gap-2">
                <Brain className="w-4 h-4 text-purple-400" />
                <h3 className="text-base font-serif text-white">VYREN Understanding &amp; Evidence Trace</h3>
              </div>
              <button 
                onClick={() => setIsReasoningOpen(false)}
                className="p-1 rounded-lg text-white/40 hover:text-white hover:bg-white/5"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="space-y-4 text-xs">
              <div className="space-y-1.5">
                <h4 className="text-[10px] font-mono uppercase tracking-widest text-[#E1D4C0]">1. Observed Evidence</h4>
                <p className="text-white/80 font-light leading-relaxed">
                  Analysis of past 90-day campaign cohort demonstrates that architectural framing increases high-intent buyer dwell time by +24.2% compared to traditional ornate backgrounds.
                </p>
              </div>

              <div className="space-y-1.5">
                <h4 className="text-[10px] font-mono uppercase tracking-widest text-purple-400">2. Epistemic Unknowns</h4>
                <p className="text-white/80 font-light leading-relaxed">
                  The causal conversion lift of pure Chiaroscuro lighting in European physical boutiques is currently unknown and preserved without false certainty.
                </p>
              </div>

              <div className="space-y-1.5">
                <h4 className="text-[10px] font-mono uppercase tracking-widest text-emerald-400">3. Human Sign-Off Invariant</h4>
                <p className="text-white/80 font-light leading-relaxed">
                  VYREN acts exclusively as an advisor and generator. No asset will be dispatched to ad networks or print vendors without explicit human confirmation.
                </p>
              </div>
            </div>

            <div className="pt-2 flex justify-end">
              <button
                onClick={() => setIsReasoningOpen(false)}
                className="px-4 py-2 rounded-xl bg-white/10 hover:bg-white/20 text-white text-xs font-medium"
              >
                Close Trace
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Contextual Coworker Status Strip */}
      <div className="p-5 rounded-2xl bg-gradient-to-r from-[#141417] via-[#101012] to-black border border-white/10 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-center gap-3.5">
          <div className="w-10 h-10 rounded-xl bg-[#E1D4C0]/10 text-[#E1D4C0] border border-[#E1D4C0]/20 flex items-center justify-center font-serif text-sm font-medium">
            MV
          </div>
          <div className="space-y-0.5">
            <div className="flex items-center gap-2">
              <h4 className="text-xs font-medium text-white">Marcus Vance (AI Creative Director)</h4>
              <span className="text-[9px] font-mono px-1.5 py-0.2 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                ACTIVE
              </span>
            </div>
            <p className="text-xs text-white/50 font-light">
              "I've synthesized 3 distinct creative territories aligned with your luxury bridal objective. Ready to develop visuals whenever you are."
            </p>
          </div>
        </div>

        <button 
          onClick={() => onNavigateTab('create')}
          className="px-4 py-2 rounded-xl bg-[#E1D4C0] text-[#0A0A0A] font-semibold text-xs hover:opacity-90 transition-opacity flex items-center gap-2 self-start sm:self-auto shrink-0"
        >
          <span>Enter Creative Room</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </button>
      </div>

    </div>
  );
}
