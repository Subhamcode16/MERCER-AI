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
  | 'create' 
  | 'review' 
  | 'ship' 
  | 'learn'
  | 'visuals'
  | 'intelligence'
  | 'directions'
  | 'assets'
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

  // Canonical 5-Stage Creative Room Navigation
  const tabs: { id: StudioTabId; label: string; badge?: string }[] = [
    { id: 'overview', label: 'Overview' },
    { id: 'create', label: 'Create & Develop', badge: `${campaign.directions.length + campaign.visualStudies.length}` },
    { id: 'review', label: 'Review & Sign-Off', badge: `${campaign.reviews.length}` },
    { id: 'ship', label: 'Ship & Release' },
    { id: 'learn', label: 'Learn & Memory' }
  ];

  return (
    <div className="border-b border-border/40 bg-card/80 backdrop-blur-md sticky top-0 z-30 transition-colors duration-200">
      {/* Top Utility & Identity Bar */}
      <div className="px-6 py-4 flex flex-col lg:flex-row lg:items-center justify-between gap-4 border-b border-border/20">
        
        {/* Left: Brand, Campaign Title & Status */}
        <div className="space-y-1.5 max-w-2xl">
          <div className="flex items-center gap-2.5 flex-wrap">
            <span className="text-[10px] font-mono tracking-widest uppercase text-primary/80 bg-primary/10 border border-primary/20 px-2 py-0.5 rounded">
              {campaign.brand}
            </span>
            <span className="text-muted-foreground/30 text-xs">•</span>
            <h1 className="text-lg font-serif text-foreground font-normal tracking-wide">
              {campaign.name}
            </h1>
            <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[9px] font-mono tracking-wider bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
              {campaign.status.toUpperCase()}
            </span>
          </div>

          <p className="text-xs text-muted-foreground font-light line-clamp-1">
            <span className="text-foreground/80 font-medium">Objective:</span> {campaign.objective}
          </p>
        </div>

        {/* Right: Human Authority & Active Crew HUD */}
        <div className="flex items-center gap-4 flex-wrap self-start lg:self-auto">
          
          {/* Human Decision Maker Authority Badge */}
          <div className="flex items-center gap-2.5 px-3 py-1.5 rounded-xl bg-accent/30 border border-border/40 text-xs">
            <div className="w-6 h-6 rounded-full bg-amber-500/20 text-amber-600 dark:text-amber-300 border border-amber-500/30 flex items-center justify-center text-[10px] font-mono font-medium">
              {campaign.humanOwner.avatar}
            </div>
            <div className="text-left leading-tight">
              <div className="text-foreground text-[11px] font-medium flex items-center gap-1">
                {campaign.humanOwner.name}
                <Lock className="w-3 h-3 text-primary" />
              </div>
              <div className="text-[9px] text-muted-foreground font-mono">
                Sole Strategic Authority
              </div>
            </div>
          </div>

          {/* Active AI Crew HUD */}
          <div className="relative flex items-center gap-1 px-2.5 py-1.5 rounded-xl bg-accent/20 border border-border/40">
            <span className="text-[9px] font-mono uppercase tracking-wider text-muted-foreground mr-1.5 hidden sm:inline">
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
                    className="w-6 h-6 rounded-full border border-background flex items-center justify-center text-[9px] font-mono font-bold transition-transform hover:scale-110 shadow-xs"
                    style={{ backgroundColor: `${worker.avatarColor}20`, color: worker.avatarColor }}
                  >
                    {worker.name[0]}
                  </div>
                  {worker.status === 'active' && (
                    <span className="absolute bottom-0 right-0 w-2 h-2 rounded-full bg-emerald-500 border border-background" />
                  )}
                  {worker.status === 'awaiting_human_gate' && (
                    <span className="absolute bottom-0 right-0 w-2 h-2 rounded-full bg-amber-500 border border-background" />
                  )}
                </button>
              ))}
            </div>

            {/* Expandable Hover Tooltip for Active AI Worker */}
            {hoveredWorker && (
              <div className="absolute right-0 top-11 w-72 p-3 rounded-xl bg-card border border-border shadow-xl z-50 text-xs space-y-2 pointer-events-none animate-in fade-in zoom-in-95 duration-150">
                <div className="flex items-center justify-between border-b border-border/40 pb-1.5">
                  <span className="font-medium text-foreground">{hoveredWorker.name}</span>
                  <span className="text-[9px] font-mono text-primary">{hoveredWorker.role}</span>
                </div>
                <div className="space-y-1 text-[11px] text-foreground/80">
                  <p><span className="text-muted-foreground font-mono">Current:</span> {hoveredWorker.currentTask}</p>
                  <p><span className="text-muted-foreground font-mono">Recent:</span> {hoveredWorker.recentContribution}</p>
                </div>
                <div className="text-[10px] font-mono text-emerald-600 dark:text-emerald-400 pt-1 border-t border-border/40 flex items-center gap-1">
                  <span>&rarr;</span> {hoveredWorker.nextHandoff}
                </div>
              </div>
            )}
          </div>

          {/* Ask VYREN Entry Trigger */}
          <button
            onClick={onOpenAskVyren}
            className="px-3 py-1.5 rounded-xl bg-primary/10 hover:bg-primary/20 text-primary border border-primary/30 text-xs font-medium flex items-center gap-1.5 transition-all shadow-xs hover:border-primary/60 cursor-pointer"
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>Ask VYREN</span>
          </button>
        </div>
      </div>

      {/* Internal 5-Tab Lifecycle Navigation */}
      <div className="px-6 flex items-center gap-1 overflow-x-auto scrollbar-none py-1.5">
        {tabs.map((tab) => {
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => onSelectTab(tab.id)}
              className={`px-3.5 py-2 rounded-lg text-xs font-medium transition-all flex items-center gap-2 whitespace-nowrap relative cursor-pointer ${
                isActive
                  ? "text-primary bg-accent/60 shadow-xs font-semibold"
                  : "text-muted-foreground hover:text-foreground hover:bg-accent/30"
              }`}
            >
              <span>{tab.label}</span>
              {tab.badge && (
                <span className={`text-[9px] font-mono px-1.5 py-0.2 rounded-full ${
                  isActive
                    ? "bg-primary/15 text-primary border border-primary/25"
                    : "bg-muted text-muted-foreground"
                }`}>
                  {tab.badge}
                </span>
              )}
              {isActive && (
                <div className="absolute bottom-0 left-2 right-2 h-0.5 bg-primary rounded-full shadow-[0_0_8px_rgba(var(--primary),0.6)]" />
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
}

