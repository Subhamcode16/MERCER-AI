"use client";

import React, { useState } from "react";
import { 
  Sparkles, 
  ShieldCheck, 
  Users, 
  HelpCircle, 
  Layers, 
  ChevronRight,
  CheckCircle2,
  Clock,
  Lock,
  ArrowUpRight
} from "lucide-react";
import type { CampaignStudioModel, WorkerContribution } from "@/lib/campaignStudioFixtures";

export type StudioTabId = 
  | 'overview' 
  | 'intelligence' 
  | 'directions' 
  | 'visuals' 
  | 'assets' 
  | 'review' 
  | 'production' 
  | 'outcomes';

interface CampaignStudioHeaderProps {
  campaign: CampaignStudioModel;
  activeTab: StudioTabId;
  onSelectTab: (tab: StudioTabId) => void;
  onOpenAskVyren: () => void;
  onBackToOverview?: () => void;
}

export function CampaignStudioHeader({
  campaign,
  activeTab,
  onSelectTab,
  onOpenAskVyren,
}: CampaignStudioHeaderProps) {
  const [hoveredWorker, setHoveredWorker] = useState<WorkerContribution | null>(null);

  const tabs: { id: StudioTabId; label: string; badge?: string }[] = [
    { id: 'overview', label: 'Overview' },
    { id: 'intelligence', label: 'Intelligence', badge: `${campaign.intelligence.length}` },
    { id: 'directions', label: 'Directions', badge: `${campaign.directions.length}` },
    { id: 'visuals', label: 'Visuals', badge: `${campaign.visualStudies.length}` },
    { id: 'assets', label: 'Assets', badge: `${campaign.assets.length}` },
    { id: 'review', label: 'Review', badge: `${campaign.reviews.length}` },
    { id: 'production', label: 'Production' },
    { id: 'outcomes', label: 'Outcomes' }
  ];

  return (
    <div className="border-b border-white/10 bg-[#0D0D0E]/90 backdrop-blur-md sticky top-0 z-30">
      {/* Top Utility & Identity Bar */}
      <div className="px-6 py-4 flex flex-col lg:flex-row lg:items-center justify-between gap-4 border-b border-white/5">
        
        {/* Left: Brand, Campaign Title & Status */}
        <div className="space-y-1.5 max-w-2xl">
          <div className="flex items-center gap-2.5 flex-wrap">
            <span className="text-[10px] font-mono tracking-widest uppercase text-[#E1D4C0]/70 bg-[#E1D4C0]/10 border border-[#E1D4C0]/20 px-2 py-0.5 rounded">
              {campaign.brand}
            </span>
            <span className="text-white/20 text-xs">•</span>
            <h1 className="text-lg font-serif text-white font-normal tracking-wide">
              {campaign.name}
            </h1>
            <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[9px] font-mono tracking-wider bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
              {campaign.status.toUpperCase()}
            </span>
          </div>

          <p className="text-xs text-white/50 font-light line-clamp-1">
            <span className="text-white/70 font-medium">Objective:</span> {campaign.objective}
          </p>
        </div>

        {/* Right: Human Authority & Active Crew HUD */}
        <div className="flex items-center gap-4 flex-wrap self-start lg:self-auto">
          
          {/* Human Decision Maker Authority Badge */}
          <div className="flex items-center gap-2.5 px-3 py-1.5 rounded-xl bg-white/[0.03] border border-white/10 text-xs">
            <div className="w-6 h-6 rounded-full bg-amber-500/20 text-[#E1D4C0] border border-amber-500/30 flex items-center justify-center text-[10px] font-mono font-medium">
              {campaign.humanOwner.avatar}
            </div>
            <div className="text-left leading-tight">
              <div className="text-white/90 text-[11px] font-medium flex items-center gap-1">
                {campaign.humanOwner.name}
                <Lock className="w-3 h-3 text-[#E1D4C0]" />
              </div>
              <div className="text-[9px] text-white/40 font-mono">
                Sole Strategic Authority
              </div>
            </div>
          </div>

          {/* Active AI Crew HUD */}
          <div className="relative flex items-center gap-1 px-2.5 py-1.5 rounded-xl bg-white/[0.02] border border-white/5">
            <span className="text-[9px] font-mono uppercase tracking-wider text-white/40 mr-1.5 hidden sm:inline">
              Active Crew:
            </span>
            <div className="flex -space-x-1.5">
              {campaign.activeCrew.map((worker) => (
                <button
                  key={worker.id}
                  onMouseEnter={() => setHoveredWorker(worker)}
                  onMouseLeave={() => setHoveredWorker(null)}
                  className="relative group focus:outline-none"
                >
                  <div 
                    className="w-6 h-6 rounded-full border border-black/80 flex items-center justify-center text-[9px] font-mono font-bold transition-transform hover:scale-110 shadow-sm"
                    style={{ backgroundColor: `${worker.avatarColor}20`, color: worker.avatarColor }}
                  >
                    {worker.name[0]}
                  </div>
                  {worker.status === 'active' && (
                    <span className="absolute bottom-0 right-0 w-2 h-2 rounded-full bg-emerald-400 border border-black" />
                  )}
                  {worker.status === 'awaiting_human_gate' && (
                    <span className="absolute bottom-0 right-0 w-2 h-2 rounded-full bg-amber-400 border border-black" />
                  )}
                </button>
              ))}
            </div>

            {/* Expandable Hover Tooltip for Active AI Worker */}
            {hoveredWorker && (
              <div className="absolute right-0 top-11 w-72 p-3 rounded-xl bg-[#141416] border border-white/10 shadow-2xl z-50 text-xs space-y-2 pointer-events-none animate-in fade-in zoom-in-95 duration-150">
                <div className="flex items-center justify-between border-b border-white/5 pb-1.5">
                  <span className="font-medium text-white">{hoveredWorker.name}</span>
                  <span className="text-[9px] font-mono text-[#E1D4C0]">{hoveredWorker.role}</span>
                </div>
                <div className="space-y-1 text-[11px] text-white/70">
                  <p><span className="text-white/40 font-mono">Current:</span> {hoveredWorker.currentTask}</p>
                  <p><span className="text-white/40 font-mono">Recent:</span> {hoveredWorker.recentContribution}</p>
                </div>
                <div className="text-[10px] font-mono text-emerald-400/90 pt-1 border-t border-white/5 flex items-center gap-1">
                  <span>&rarr;</span> {hoveredWorker.nextHandoff}
                </div>
              </div>
            )}
          </div>

          {/* Ask VYREN Entry Trigger */}
          <button
            onClick={onOpenAskVyren}
            className="px-3 py-1.5 rounded-xl bg-gradient-to-r from-amber-500/10 to-amber-600/20 hover:from-amber-500/20 hover:to-amber-600/30 text-[#E1D4C0] border border-[#E1D4C0]/30 text-xs font-medium flex items-center gap-1.5 transition-all shadow-lg hover:border-[#E1D4C0]/60"
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>Ask VYREN</span>
          </button>
        </div>
      </div>

      {/* Internal 8-Tab Lifecycle Navigation */}
      <div className="px-6 flex items-center gap-1 overflow-x-auto scrollbar-none py-1.5">
        {tabs.map((tab) => {
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => onSelectTab(tab.id)}
              className={`px-3.5 py-2 rounded-lg text-xs font-medium transition-all flex items-center gap-2 whitespace-nowrap relative ${
                isActive
                  ? "text-[#E1D4C0] bg-white/[0.06] shadow-inner font-semibold"
                  : "text-white/50 hover:text-white hover:bg-white/[0.02]"
              }`}
            >
              <span>{tab.label}</span>
              {tab.badge && (
                <span className={`text-[9px] font-mono px-1.5 py-0.2 rounded-full ${
                  isActive
                    ? "bg-[#E1D4C0]/20 text-[#E1D4C0] border border-[#E1D4C0]/30"
                    : "bg-white/5 text-white/40"
                }`}>
                  {tab.badge}
                </span>
              )}
              {isActive && (
                <div className="absolute bottom-0 left-2 right-2 h-0.5 bg-[#E1D4C0] rounded-full shadow-[0_0_8px_rgba(225,212,192,0.8)]" />
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
}
