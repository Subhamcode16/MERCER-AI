"use client";

import React from "react";
import { 
  Users, 
  Sparkles, 
  AlertCircle, 
  CheckCircle2, 
  ArrowRight, 
  Layers,
  ChevronRight,
  ShieldAlert,
  Lock
} from "lucide-react";
import type { AttentionItem, DepartmentSummary } from "@/lib/teamFixtures";

export type TeamTabId = 
  | 'roster' 
  | 'active-work' 
  | 'campaign-rooms' 
  | 'conversations' 
  | 'handoffs' 
  | 'skills-routines' 
  | 'activity';

interface TeamHeaderProps {
  activeTab: TeamTabId;
  onSelectTab: (tab: TeamTabId) => void;
  departments: DepartmentSummary[];
  attentionItems: AttentionItem[];
  onResolveAttention: (itemId: string) => void;
}

export function TeamHeader({
  activeTab,
  onSelectTab,
  departments,
  attentionItems,
  onResolveAttention
}: TeamHeaderProps) {
  const tabs: { id: TeamTabId; label: string; badge?: string }[] = [
    { id: 'roster', label: 'My Team' },
    { id: 'active-work', label: 'Active Work' },
    { id: 'campaign-rooms', label: 'Campaign Rooms', badge: '2' },
    { id: 'conversations', label: 'Conversations' },
    { id: 'handoffs', label: 'Handoffs', badge: '3' },
    { id: 'skills-routines', label: 'Skills & Routines' },
    { id: 'activity', label: 'Activity Feed' }
  ];

  return (
    <div className="border-b border-border/40 bg-card/80 backdrop-blur-md sticky top-0 z-30 space-y-4 pt-6 transition-colors duration-200">
      
      {/* Title & Department Summary Pill */}
      <div className="px-6 lg:px-10 flex flex-col lg:flex-row lg:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-xl bg-primary/10 border border-primary/20 flex items-center justify-center text-primary">
              <Users className="w-4 h-4" />
            </div>
            <div>
              <h1 className="text-xl font-serif text-foreground font-medium tracking-wide">
                AI Team
              </h1>
              <p className="text-[11px] text-muted-foreground font-light">
                Your persistent digital creative organization &bull; Strategy, Creative, Intelligence & Production
              </p>
            </div>
          </div>
        </div>

        {/* Department Micro-Pills */}
        <div className="flex items-center gap-2 flex-wrap">
          {departments.map((dept) => (
            <div 
              key={dept.name}
              className="px-2.5 py-1 rounded-xl bg-accent/30 border border-border/40 flex items-center gap-2 text-[10px] font-mono text-muted-foreground"
            >
              <span className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: dept.color }} />
              <span className="text-foreground/90 font-medium">{dept.name}</span>
              <span className="text-muted-foreground/70">({dept.coworkerCount})</span>
            </div>
          ))}
        </div>
      </div>

      {/* Prominent Attention Required Priority Strip (If any pending actions) */}
      {attentionItems.length > 0 && (
        <div className="px-6 lg:px-10">
          <div className="p-4 rounded-2xl bg-rose-500/10 border border-rose-500/25 flex flex-col md:flex-row md:items-center justify-between gap-4 backdrop-blur-sm">
            <div className="flex items-start gap-3">
              <div className="w-7 h-7 rounded-lg bg-rose-500/20 text-rose-500 dark:text-rose-300 border border-rose-500/30 flex items-center justify-center shrink-0 mt-0.5">
                <AlertCircle className="w-4 h-4" />
              </div>
              <div className="space-y-0.5">
                <div className="flex items-center gap-2">
                  <span className="text-[10px] font-mono uppercase tracking-wider text-rose-600 dark:text-rose-400 font-bold">
                    Human Attention Required ({attentionItems.length})
                  </span>
                  <span className="text-muted-foreground/40 text-xs">•</span>
                  <span className="text-xs text-foreground/90 font-medium">{attentionItems[0].title}</span>
                </div>
                <p className="text-xs text-muted-foreground font-light">
                  {attentionItems[0].coworkerName} &bull; {attentionItems[0].campaignName}: {attentionItems[0].actionPrompt}
                </p>
              </div>
            </div>

            <div className="flex items-center gap-2 self-start md:self-auto shrink-0">
              <button
                onClick={() => onResolveAttention(attentionItems[0].id)}
                className="px-3.5 py-1.5 rounded-xl bg-rose-500/20 hover:bg-rose-500/30 text-rose-700 dark:text-rose-200 border border-rose-500/40 text-xs font-semibold transition-colors flex items-center gap-1.5 cursor-pointer"
              >
                <CheckCircle2 className="w-3.5 h-3.5" />
                <span>Resolve Gate</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Internal Segmented Tabs Bar */}
      <div className="px-6 lg:px-10 flex items-center gap-1 overflow-x-auto scrollbar-none pb-2">
        {tabs.map((tab) => {
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => onSelectTab(tab.id)}
              className={`px-4 py-2 rounded-lg text-xs font-medium transition-all flex items-center gap-2 whitespace-nowrap relative cursor-pointer ${
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

