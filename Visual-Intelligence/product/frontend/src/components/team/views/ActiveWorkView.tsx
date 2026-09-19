"use client";

import React from "react";
import { 
  Layers, 
  Clock, 
  ArrowRight, 
  CheckCircle2, 
  AlertCircle,
  Sparkles,
  ExternalLink
} from "lucide-react";
import type { ActiveWorkItem, Coworker } from "@/lib/teamFixtures";

interface ActiveWorkViewProps {
  activeWork: ActiveWorkItem[];
  onSelectCoworkerById: (coworkerId: string) => void;
}

export function ActiveWorkView({ activeWork, onSelectCoworkerById }: ActiveWorkViewProps) {
  // Group work items by campaign
  const campaigns = Array.from(new Set(activeWork.map(w => w.campaign)));

  return (
    <div className="space-y-8 animate-in fade-in duration-200">
      
      {/* Overview Banner */}
      <div className="p-6 rounded-2xl bg-card border border-border space-y-1 shadow-sm">
        <h2 className="text-base font-serif text-foreground font-medium flex items-center gap-2">
          <Layers className="w-4 h-4 text-primary" /> Active Organizational Workload
        </h2>
        <p className="text-xs text-muted-foreground font-light">
          Structured view of ongoing creative tasks grouped by campaign initiatives and responsible coworkers.
        </p>
      </div>

      {/* Campaign Task Groups */}
      <div className="space-y-6">
        {campaigns.map((campName) => {
          const items = activeWork.filter(w => w.campaign === campName);
          return (
            <div key={campName} className="p-6 rounded-2xl bg-card border border-border space-y-5 shadow-sm">
              
              {/* Campaign Header */}
              <div className="flex items-center justify-between border-b border-border pb-3">
                <div className="flex items-center gap-2.5">
                  <span className="text-[10px] font-mono tracking-wider uppercase text-primary bg-primary/10 border border-primary/20 px-2.5 py-0.5 rounded font-semibold">
                    CAMPAIGN
                  </span>
                  <h3 className="text-base font-serif text-foreground">{campName}</h3>
                </div>
                <span className="text-[11px] font-mono text-muted-foreground">{items.length} Active Workstreams</span>
              </div>

              {/* Work Items Table / Grid */}
              <div className="space-y-3">
                {items.map((item) => (
                  <div
                    key={item.id}
                    onClick={() => onSelectCoworkerById(item.coworkerId)}
                    className="p-4 rounded-xl bg-muted/30 border border-border hover:border-primary/40 hover:bg-muted/50 transition-all cursor-pointer flex flex-col md:flex-row md:items-center justify-between gap-4 group shadow-xs"
                  >
                    {/* Coworker & Task */}
                    <div className="flex items-start gap-3.5 max-w-xl">
                      <div 
                        className="w-10 h-10 rounded-xl flex items-center justify-center font-serif text-xs font-semibold border border-border shrink-0 shadow-xs"
                        style={{ backgroundColor: `${item.coworkerColor}20`, color: item.coworkerColor }}
                      >
                        {item.coworkerAvatar}
                      </div>

                      <div className="space-y-0.5">
                        <div className="flex items-center gap-2">
                          <span className="text-xs font-medium text-foreground group-hover:text-primary transition-colors">
                            {item.coworkerName}
                          </span>
                          <span className="text-muted-foreground/40 text-xs">•</span>
                          <span className="text-[10px] font-mono text-muted-foreground">{item.coworkerRole}</span>
                        </div>
                        <p className="text-xs text-foreground/80 font-light">{item.taskTitle}</p>
                      </div>
                    </div>

                    {/* Progress & Status */}
                    <div className="flex items-center gap-6 self-start md:self-auto shrink-0 text-xs font-mono">
                      <div className="w-32 space-y-1">
                        <div className="flex justify-between text-[10px] text-muted-foreground">
                          <span>Progress</span>
                          <span className="text-foreground font-medium">{item.progress}%</span>
                        </div>
                        <div className="h-1.5 w-full bg-muted rounded-full overflow-hidden">
                          <div 
                            className="h-full rounded-full" 
                            style={{ width: `${item.progress}%`, backgroundColor: item.coworkerColor }}
                          />
                        </div>
                      </div>

                      <div className="text-right">
                        <span className={`px-2 py-0.5 rounded text-[9px] font-medium ${
                          item.status === 'Needs You'
                            ? 'bg-rose-500/10 text-rose-600 dark:text-rose-300 border border-rose-500/30'
                            : 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20'
                        }`}>
                          {item.status.toUpperCase()}
                        </span>
                        <div className="text-[9px] text-muted-foreground mt-1">{item.deadline}</div>
                      </div>

                      <span className="text-primary group-hover:translate-x-1 transition-transform">
                        <ArrowRight className="w-3.5 h-3.5" />
                      </span>
                    </div>

                  </div>
                ))}
              </div>

            </div>
          );
        })}
      </div>

    </div>
  );
}
