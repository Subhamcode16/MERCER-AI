"use client";

import { useState } from "react";
import Link from "next/link";
import { 
  Target, 
  Plus, 
  Sparkles, 
  Layers, 
  TrendingUp, 
  ArrowRight, 
  Eye, 
  BarChart3, 
  Sliders, 
  Zap, 
  CheckCircle2,
  RefreshCw
} from "lucide-react";

export default function CampaignsPage() {
  const [activeTab, setActiveTab] = useState<"campaigns" | "outcomes" | "attribution">("campaigns");

  return (
    <div className="h-full overflow-y-auto bg-[#0A0A0A] text-white/90 p-8 lg:p-12 scrollbar-thin scrollbar-thumb-white/10">
      <div className="max-w-6xl mx-auto space-y-10">
        
        {/* Header */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-6 border-b border-white/5">
          <div>
            <div className="flex items-center gap-2">
              <Target className="w-5 h-5 text-[#E1D4C0]" />
              <h1 className="text-2xl font-serif text-white font-light">Omnichannel Campaigns</h1>
            </div>
            <p className="text-xs text-white/50 font-light mt-1">
              Objective &rarr; Creative Direction &rarr; Multi-Surface Asset Generation &rarr; Closed-Loop Outcome Learning.
            </p>
          </div>

          <Link
            href="/studio"
            className="px-4 py-2 rounded-xl bg-[#E1D4C0] text-[#0A0A0A] text-xs font-semibold hover:opacity-90 transition-opacity flex items-center gap-2"
          >
            <Plus className="w-4 h-4" /> Launch New Campaign
          </Link>
        </div>

        {/* Tab Navigation */}
        <div className="flex items-center gap-2 border-b border-white/10 pb-px text-xs font-medium">
          <button
            onClick={() => setActiveTab("campaigns")}
            className={`pb-3 px-3 transition-colors relative ${
              activeTab === "campaigns" ? "text-[#E1D4C0]" : "text-white/40 hover:text-white"
            }`}
          >
            Active Campaigns
            {activeTab === "campaigns" && <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-[#E1D4C0]" />}
          </button>

          <button
            onClick={() => setActiveTab("outcomes")}
            className={`pb-3 px-3 transition-colors relative ${
              activeTab === "outcomes" ? "text-[#E1D4C0]" : "text-white/40 hover:text-white"
            }`}
          >
            Outcome Intelligence & Counterfactuals
            {activeTab === "outcomes" && <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-[#E1D4C0]" />}
          </button>

          <button
            onClick={() => setActiveTab("attribution")}
            className={`pb-3 px-3 transition-colors relative ${
              activeTab === "attribution" ? "text-[#E1D4C0]" : "text-white/40 hover:text-white"
            }`}
          >
            Attribution Radar & Calibration
            {activeTab === "attribution" && <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-[#E1D4C0]" />}
          </button>
        </div>

        {/* Tab 1: Active Campaigns */}
        {activeTab === "campaigns" && (
          <div className="space-y-6">
            
            {/* Campaign 1: Autumn/Winter 2026 */}
            <div className="rounded-2xl border border-white/10 bg-[#111111]/80 p-6 space-y-6 hover:border-[#E1D4C0]/30 transition-all">
              <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
                <div>
                  <div className="flex items-center gap-2">
                    <h3 className="text-lg font-medium text-white">Autumn/Winter 2026: The Modern Sovereign</h3>
                    <span className="px-2 py-0.5 rounded text-[9px] font-mono tracking-wider bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                      LIVE IN PRODUCTION
                    </span>
                  </div>
                  <p className="text-xs text-white/50 font-light mt-0.5">
                    Objective: High-intent Gen Z luxury bridal acquisition across Instagram, Print Editorial & OOH Billboard surfaces.
                  </p>
                </div>

                <Link
                  href="/studio"
                  className="px-3.5 py-1.5 rounded-lg bg-white/[0.05] hover:bg-white/10 text-xs text-white/80 hover:text-white transition-colors flex items-center gap-1.5"
                >
                  Manage in Studio <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              </div>

              {/* Multi-Surface Matrix Preview */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs">
                <div className="p-3.5 rounded-xl bg-white/[0.02] border border-white/5 space-y-1">
                  <div className="text-[10px] text-white/40 font-mono uppercase">Social (9:16 Story)</div>
                  <div className="text-white font-medium">8 Variations Active</div>
                  <div className="text-[10px] text-emerald-400 font-mono">+24.2% CTR</div>
                </div>

                <div className="p-3.5 rounded-xl bg-white/[0.02] border border-white/5 space-y-1">
                  <div className="text-[10px] text-white/40 font-mono uppercase">Editorial (4:5 Feed)</div>
                  <div className="text-white font-medium">6 Variations Active</div>
                  <div className="text-[10px] text-emerald-400 font-mono">+18.5% Engagement</div>
                </div>

                <div className="p-3.5 rounded-xl bg-white/[0.02] border border-white/5 space-y-1">
                  <div className="text-[10px] text-white/40 font-mono uppercase">Print / Catalog</div>
                  <div className="text-white font-medium">300 DPI CMYK Ready</div>
                  <div className="text-[10px] text-[#E1D4C0] font-mono">Export Approved</div>
                </div>

                <div className="p-3.5 rounded-xl bg-white/[0.02] border border-white/5 space-y-1">
                  <div className="text-[10px] text-white/40 font-mono uppercase">OOH Billboard (16:9)</div>
                  <div className="text-white font-medium">4K Ultra Resolution</div>
                  <div className="text-[10px] text-[#E1D4C0] font-mono">Rendered</div>
                </div>
              </div>
            </div>

          </div>
        )}

        {/* Tab 2: Outcomes & Counterfactuals */}
        {activeTab === "outcomes" && (
          <div className="rounded-2xl border border-white/10 bg-[#111111]/80 p-6 space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-base font-medium text-white flex items-center gap-2">
                  <TrendingUp className="w-4 h-4 text-emerald-400" /> Counterfactual Performance Simulation
                </h3>
                <p className="text-xs text-white/50 font-light mt-0.5">
                  Analyzing why specific creative variations outperformed and what would happen if lighting or drape tokens were modified.
                </p>
              </div>

              <span className="px-2.5 py-1 rounded-full text-[10px] font-mono bg-purple-500/10 text-purple-300 border border-purple-500/20">
                MODEL: Causal Impact v2
              </span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
              <div className="p-4 rounded-xl bg-white/[0.02] border border-white/5 space-y-2">
                <div className="text-white/40 text-[10px] font-mono uppercase">Observed Conversion Rate</div>
                <div className="text-2xl font-serif text-emerald-400">4.82%</div>
                <p className="text-[11px] text-white/60">Tungsten rim lighting + Banarasi gold brocade close-up</p>
              </div>

              <div className="p-4 rounded-xl bg-white/[0.02] border border-white/5 space-y-2">
                <div className="text-white/40 text-[10px] font-mono uppercase">Counterfactual Baseline (Cool Light)</div>
                <div className="text-2xl font-serif text-white/40">2.91%</div>
                <p className="text-[11px] text-white/60">Standard cool fluorescent daylight setup</p>
              </div>

              <div className="p-4 rounded-xl bg-white/[0.02] border border-white/5 space-y-2">
                <div className="text-white/40 text-[10px] font-mono uppercase">Net Creative Lift</div>
                <div className="text-2xl font-serif text-[#E1D4C0]">+65.6%</div>
                <p className="text-[11px] text-emerald-400 font-mono">Attributable to Visual DNA Lighting Token</p>
              </div>
            </div>
          </div>
        )}

        {/* Tab 3: Attribution Radar */}
        {activeTab === "attribution" && (
          <div className="rounded-2xl border border-white/10 bg-[#111111]/80 p-6 space-y-6">
            <h3 className="text-base font-medium text-white flex items-center gap-2">
              <BarChart3 className="w-4 h-4 text-blue-400" /> Channel Calibration & Attribution Radar
            </h3>
            <p className="text-xs text-white/50 font-light">
              Multi-touch Bayesian attribution connecting top-of-funnel creative assets to downstream commercial outcomes.
            </p>

            <div className="p-8 border border-white/5 rounded-xl bg-black/40 text-center space-y-3">
              <div className="w-12 h-12 rounded-full bg-blue-500/10 text-blue-400 flex items-center justify-center mx-auto">
                <Sliders className="w-6 h-6" />
              </div>
              <div className="text-sm font-medium text-white">Attribution Radar Synchronized</div>
              <p className="text-xs text-white/40 max-w-md mx-auto font-light">
                Connected to Shopify, Meta Ads, and Google Analytics 4. Closed-loop learning continuously feeds future campaign generation in Creative Studio.
              </p>
            </div>
          </div>
        )}

      </div>
    </div>
  );
}
