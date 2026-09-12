"use client";

import React from "react";
import { 
  Target, 
  Brain, 
  Lock, 
  AlertCircle, 
  ArrowRight, 
  CheckCircle2, 
  Sparkles, 
  Layers, 
  ShieldCheck,
  ChevronRight,
  Eye,
  Sliders
} from "lucide-react";
import type { CampaignStudioModel } from "@/lib/campaignStudioFixtures";

interface OverviewTabProps {
  campaign: CampaignStudioModel;
  onNavigateTab: (tab: 'overview' | 'intelligence' | 'directions' | 'visuals' | 'assets' | 'review' | 'production' | 'outcomes') => void;
}

export function OverviewTab({ campaign, onNavigateTab }: OverviewTabProps) {
  return (
    <div className="space-y-8 animate-in fade-in duration-200">
      
      {/* 4 Core Invariant Questions Bento Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        {/* Card 1: What are we making? */}
        <div className="p-6 rounded-2xl bg-[#111113]/80 border border-white/10 space-y-4 relative overflow-hidden group hover:border-[#E1D4C0]/30 transition-all">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-xl bg-amber-500/10 text-[#E1D4C0] border border-amber-500/20 flex items-center justify-center">
                <Target className="w-4 h-4" />
              </div>
              <div>
                <span className="text-[10px] font-mono uppercase tracking-widest text-[#E1D4C0]">Question 01</span>
                <h3 className="text-base font-serif text-white font-medium">What are we making?</h3>
              </div>
            </div>
            <span className="text-[9px] font-mono px-2 py-0.5 rounded bg-white/5 text-white/50 border border-white/5">
              SCOPE
            </span>
          </div>

          <div className="space-y-3 text-xs">
            <div className="p-3.5 rounded-xl bg-white/[0.02] border border-white/5 space-y-1">
              <span className="text-[10px] font-mono text-white/40 uppercase">Strategic Objective</span>
              <p className="text-white/90 leading-relaxed font-light">{campaign.objective}</p>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div className="p-3 rounded-xl bg-white/[0.02] border border-white/5 space-y-1">
                <span className="text-[10px] font-mono text-white/40 uppercase">Target Audience</span>
                <p className="text-white/80 font-medium truncate">{campaign.audience}</p>
              </div>
              <div className="p-3 rounded-xl bg-white/[0.02] border border-white/5 space-y-1">
                <span className="text-[10px] font-mono text-white/40 uppercase">Active Channels</span>
                <p className="text-[#E1D4C0] font-mono font-medium">{campaign.channels.length} Surfaces Synchronized</p>
              </div>
            </div>
          </div>
        </div>

        {/* Card 2: What does VYREN understand? */}
        <div className="p-6 rounded-2xl bg-[#111113]/80 border border-white/10 space-y-4 relative overflow-hidden group hover:border-[#E1D4C0]/30 transition-all">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-xl bg-purple-500/10 text-purple-300 border border-purple-500/20 flex items-center justify-center">
                <Brain className="w-4 h-4" />
              </div>
              <div>
                <span className="text-[10px] font-mono uppercase tracking-widest text-purple-400">Question 02</span>
                <h3 className="text-base font-serif text-white font-medium">What does VYREN understand?</h3>
              </div>
            </div>
            <button 
              onClick={() => onNavigateTab('intelligence')}
              className="text-[10px] font-mono text-[#E1D4C0] hover:underline flex items-center gap-1"
            >
              Inspect Intelligence <ChevronRight className="w-3 h-3" />
            </button>
          </div>

          <div className="space-y-2.5 text-xs">
            <div className="flex items-center justify-between p-3 rounded-xl bg-white/[0.02] border border-white/5">
              <span className="text-white/70">Textile Physics Calibration (Brocade Shearing)</span>
              <span className="px-2 py-0.5 rounded text-[9px] font-mono bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                SUPPORTED (38.4 N/m)
              </span>
            </div>

            <div className="flex items-center justify-between p-3 rounded-xl bg-white/[0.02] border border-white/5">
              <span className="text-white/70">Audience Signal (Structural Minimalist Drapes)</span>
              <span className="px-2 py-0.5 rounded text-[9px] font-mono bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                OBSERVED (+24.2% LIFT)
              </span>
            </div>

            <div className="flex items-center justify-between p-3 rounded-xl bg-white/[0.02] border border-white/5">
              <span className="text-white/70">Lower-Funnel Chiaroscuro Conversion Elasticity</span>
              <span className="px-2 py-0.5 rounded text-[9px] font-mono bg-zinc-500/10 text-zinc-400 border border-zinc-500/20">
                UNKNOWN (SURVIVING)
              </span>
            </div>
          </div>
        </div>

        {/* Card 3: What has been decided? */}
        <div className="p-6 rounded-2xl bg-[#111113]/80 border border-white/10 space-y-4 relative overflow-hidden group hover:border-[#E1D4C0]/30 transition-all">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-xl bg-emerald-500/10 text-emerald-300 border border-emerald-500/20 flex items-center justify-center">
                <Lock className="w-4 h-4" />
              </div>
              <div>
                <span className="text-[10px] font-mono uppercase tracking-widest text-emerald-400">Question 03</span>
                <h3 className="text-base font-serif text-white font-medium">What has been decided?</h3>
              </div>
            </div>
            <span className="text-[9px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              {campaign.lockedDecisions.length} LOCKED POLICIES
            </span>
          </div>

          <div className="space-y-2.5 text-xs">
            {campaign.lockedDecisions.map((dec) => (
              <div key={dec.id} className="p-3 rounded-xl bg-white/[0.02] border border-white/5 space-y-1">
                <div className="flex items-center justify-between text-[10px] font-mono text-white/40">
                  <span>{dec.decidedBy}</span>
                  <span>{dec.timestamp}</span>
                </div>
                <p className="text-white/90 font-light">{dec.title}</p>
                <div className="text-[9px] font-mono text-emerald-400/70 truncate">Proof: {dec.cryptographicProof}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Card 4: What needs my attention? */}
        <div className="p-6 rounded-2xl bg-[#111113]/80 border border-white/10 space-y-4 relative overflow-hidden group hover:border-[#E1D4C0]/30 transition-all">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-xl bg-rose-500/10 text-rose-300 border border-rose-500/20 flex items-center justify-center">
                <AlertCircle className="w-4 h-4" />
              </div>
              <div>
                <span className="text-[10px] font-mono uppercase tracking-widest text-rose-400">Question 04</span>
                <h3 className="text-base font-serif text-white font-medium">What needs my attention?</h3>
              </div>
            </div>
            <span className="text-[9px] font-mono px-2 py-0.5 rounded bg-rose-500/10 text-rose-400 border border-rose-500/20">
              HUMAN GATES
            </span>
          </div>

          <div className="space-y-2.5 text-xs">
            {campaign.prioritizedActions.map((action) => (
              <div key={action.id} className="p-3 rounded-xl bg-white/[0.02] border border-white/5 flex items-center justify-between gap-3">
                <div className="space-y-0.5">
                  <div className="flex items-center gap-2">
                    <span className={`px-1.5 py-0.2 rounded text-[9px] font-mono ${
                      action.severity === 'High' ? 'bg-rose-500/20 text-rose-300' : 'bg-amber-500/20 text-amber-300'
                    }`}>
                      {action.severity}
                    </span>
                    <span className="text-white font-medium">{action.title}</span>
                  </div>
                  <span className="text-[10px] text-white/40 font-mono">Assigned: {action.assignedTo} &bull; {action.dueTimeline}</span>
                </div>
                <button 
                  onClick={() => onNavigateTab('review')}
                  className="px-2.5 py-1 rounded-lg bg-white/5 hover:bg-white/10 text-[10px] font-mono text-[#E1D4C0] shrink-0"
                >
                  Review
                </button>
              </div>
            ))}
          </div>
        </div>

      </div>

      {/* Contextual Coworker Status Card */}
      <div className="p-5 rounded-2xl bg-gradient-to-r from-purple-950/20 via-black to-black border border-purple-500/20 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-center gap-3.5">
          <div className="w-10 h-10 rounded-xl bg-purple-500/10 text-purple-300 border border-purple-500/30 flex items-center justify-center font-serif text-sm font-medium">
            MV
          </div>
          <div className="space-y-0.5">
            <div className="flex items-center gap-2">
              <h4 className="text-xs font-medium text-white">Marcus Vance (AI Creative Director)</h4>
              <span className="text-[9px] font-mono px-1.5 py-0.2 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                ACTIVE IN WORKSPACE
              </span>
            </div>
            <p className="text-xs text-white/50 font-light">
              "Direction 02 is locked. I've orchestrated 3 visual development studies and 4 multichannel deliverables awaiting your final sign-off."
            </p>
          </div>
        </div>

        <button 
          onClick={() => onNavigateTab('directions')}
          className="px-4 py-2 rounded-xl bg-[#E1D4C0] text-[#0A0A0A] font-semibold text-xs hover:opacity-90 transition-opacity flex items-center gap-2 self-start sm:self-auto shrink-0"
        >
          <span>Open Creative Directions</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </button>
      </div>

    </div>
  );
}
