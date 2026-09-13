"use client";

import React, { useState } from "react";
import { 
  TrendingUp, 
  Brain, 
  CheckCircle2, 
  HelpCircle, 
  ArrowRight,
  Sparkles,
  RefreshCw,
  Plus
} from "lucide-react";
import type { CampaignStudioModel, StudioOutcome } from "@/lib/campaignStudioFixtures";

interface OutcomesTabProps {
  campaign: CampaignStudioModel;
  onNavigateTab?: (tab: any) => void;
}

export function OutcomesTab({ campaign, onNavigateTab }: OutcomesTabProps) {
  const [notification, setNotification] = useState<string | null>(null);

  const handleApplyLearnings = () => {
    setNotification("Learning commited to Organizational Memory. New campaigns will prioritize architectural drape tokens.");
    setTimeout(() => setNotification(null), 4500);
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-200 pb-20 max-w-4xl mx-auto">
      
      {/* Toast Notification */}
      {notification && (
        <div className="fixed bottom-8 right-8 z-50 p-4 rounded-xl bg-[#141416] border border-emerald-500/40 text-emerald-300 shadow-2xl flex items-center gap-3 text-xs animate-in slide-in-from-bottom-3 duration-200">
          <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          <span>{notification}</span>
        </div>
      )}

      {/* Header */}
      <div className="space-y-1 border-b border-white/5 pb-4">
        <span className="text-[10px] font-mono tracking-widest uppercase text-[#E1D4C0]">Closed-Loop Memory</span>
        <h2 className="text-2xl font-serif text-white font-light">Here's what happened.</h2>
        <p className="text-xs text-white/50 font-light">
          Observed market performance, what VYREN learned, and preserved epistemic unknowns.
        </p>
      </div>

      {/* Observed Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        <div className="p-7 rounded-3xl bg-[#121214]/90 border border-white/10 space-y-3">
          <span className="text-[10px] font-mono uppercase tracking-widest text-white/40">
            High-Intent Engagement
          </span>
          <div className="text-4xl font-serif text-emerald-400 font-light">
            +24.2%
          </div>
          <p className="text-xs text-white/60 font-light">
            Observed lift across younger luxury buyer demographic vs traditional heritage baseline.
          </p>
        </div>

        <div className="p-7 rounded-3xl bg-[#121214]/90 border border-white/10 space-y-3">
          <span className="text-[10px] font-mono uppercase tracking-widest text-white/40">
            Brand Distinctiveness
          </span>
          <div className="text-4xl font-serif text-[#E1D4C0] font-light">
            +18.5%
          </div>
          <p className="text-xs text-white/60 font-light">
            Observed increase in brand recall and aesthetic differentiation in post-campaign surveys.
          </p>
        </div>

      </div>

      {/* What VYREN Learned vs What Remains Unknown */}
      <div className="p-8 rounded-3xl bg-[#121214]/90 border border-white/10 space-y-6 shadow-2xl">
        
        {/* Section 1: What VYREN Learned */}
        <div className="space-y-2.5">
          <div className="flex items-center gap-2">
            <Brain className="w-4 h-4 text-purple-400" />
            <h3 className="text-base font-serif text-white">What VYREN learned</h3>
          </div>
          <div className="p-4 rounded-2xl bg-white/[0.02] border border-white/5 text-xs text-white/80 font-light leading-relaxed">
            Modernized architectural heritage presentation strongly resonates with younger high-intent bridal buyers. Stripping away ornate clutter elevates perceived craftsmanship and price elasticity.
          </div>
        </div>

        {/* Section 2: What Remains Unknown */}
        <div className="space-y-2.5">
          <div className="flex items-center gap-2">
            <HelpCircle className="w-4 h-4 text-amber-400" />
            <h3 className="text-base font-serif text-white">What remains unknown</h3>
          </div>
          <div className="p-4 rounded-2xl bg-amber-500/[0.03] border border-amber-500/20 text-xs text-amber-200/80 font-light leading-relaxed">
            We do not yet know whether this distinctiveness lift persists past 90 days or translates identically to European retail flagship conversions without localized physical tests.
          </div>
        </div>

        {/* Primary CTA: Use this learning */}
        <div className="pt-4 border-t border-white/5 flex flex-col sm:flex-row items-center justify-between gap-4">
          <span className="text-xs text-white/40 font-light">
            Accumulated learning makes your future campaigns smarter and more distinctive.
          </span>

          <button
            onClick={handleApplyLearnings}
            className="px-6 py-2.5 rounded-xl bg-[#E1D4C0] text-[#0A0A0A] font-semibold text-xs hover:opacity-90 transition-opacity flex items-center gap-2 shadow-lg shrink-0"
          >
            <span>Use this learning for next campaign</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>

      </div>

    </div>
  );
}
