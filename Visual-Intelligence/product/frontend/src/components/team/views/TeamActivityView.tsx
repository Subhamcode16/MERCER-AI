"use client";

import React from "react";
import { 
  Activity, 
  GitCommit, 
  CheckCircle2, 
  ShieldCheck, 
  Lock, 
  User, 
  Sparkles,
  Layers
} from "lucide-react";
import type { TeamActivityEvent } from "@/lib/teamFixtures";

interface TeamActivityViewProps {
  activity: TeamActivityEvent[];
}

export function TeamActivityView({ activity }: TeamActivityViewProps) {
  const getActorBadge = (type: TeamActivityEvent['actorType']) => {
    switch (type) {
      case 'Human Director':
        return 'bg-primary/15 text-primary border-primary/30';
      case 'AI Coworker':
        return 'bg-purple-500/10 text-purple-700 dark:text-purple-300 border-purple-500/30';
      case 'System':
      default:
        return 'bg-blue-500/10 text-blue-700 dark:text-blue-300 border-blue-500/30';
    }
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-200">
      
      {/* Overview Banner */}
      <div className="p-6 rounded-2xl bg-card border border-border space-y-1 shadow-sm">
        <h2 className="text-base font-serif text-foreground font-medium flex items-center gap-2">
          <Activity className="w-4 h-4 text-primary" /> Organizational History & Audit Stream
        </h2>
        <p className="text-xs text-muted-foreground font-light">
          Tamper-evident record of decisions, coworker handoffs, policy enforcement gates, and human sign-offs.
        </p>
      </div>

      {/* Activity Timeline List */}
      <div className="space-y-3">
        {activity.map((event) => (
          <div
            key={event.id}
            className="p-5 rounded-2xl bg-card border border-border flex flex-col md:flex-row md:items-center justify-between gap-4 hover:border-primary/40 transition-all shadow-sm"
          >
            {/* Left Detail */}
            <div className="space-y-1.5 max-w-2xl">
              <div className="flex items-center gap-2.5 flex-wrap">
                <span className={`px-2 py-0.5 rounded text-[9px] font-mono border font-medium ${getActorBadge(event.actorType)}`}>
                  {event.actorType.toUpperCase()}
                </span>
                <span className="text-xs font-semibold text-foreground">{event.actor}</span>
                <span className="text-muted-foreground/40 text-xs">•</span>
                <span className="text-xs font-medium text-primary">{event.action}</span>
                {event.campaign && (
                  <>
                    <span className="text-muted-foreground/40 text-xs">•</span>
                    <span className="text-[10px] font-mono text-muted-foreground">{event.campaign}</span>
                  </>
                )}
              </div>

              <p className="text-xs text-foreground/80 font-light leading-relaxed">{event.detail}</p>
            </div>

            {/* Right Hash & Timestamp */}
            <div className="flex items-center gap-4 text-xs font-mono text-muted-foreground self-start md:self-auto shrink-0">
              <div className="flex items-center gap-1.5 text-[10px] text-emerald-600 dark:text-emerald-400/80">
                <GitCommit className="w-3 h-3 text-primary" />
                <span>{event.hash}</span>
              </div>
              <span className="text-[11px] text-muted-foreground/70">{event.timestamp}</span>
            </div>
          </div>
        ))}
      </div>

    </div>
  );
}
