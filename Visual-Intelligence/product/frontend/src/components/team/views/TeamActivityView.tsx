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
        return 'bg-amber-500/15 text-[#E1D4C0] border-amber-500/30';
      case 'AI Coworker':
        return 'bg-purple-500/10 text-purple-300 border-purple-500/30';
      case 'System':
      default:
        return 'bg-blue-500/10 text-blue-300 border-blue-500/30';
    }
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-200">
      
      {/* Overview Banner */}
      <div className="p-6 rounded-2xl bg-[#111113]/80 border border-white/10 space-y-1">
        <h2 className="text-base font-serif text-white font-medium flex items-center gap-2">
          <Activity className="w-4 h-4 text-[#E1D4C0]" /> Organizational History & Audit Stream
        </h2>
        <p className="text-xs text-white/50 font-light">
          Tamper-evident record of decisions, coworker handoffs, policy enforcement gates, and human sign-offs.
        </p>
      </div>

      {/* Activity Timeline List */}
      <div className="space-y-3">
        {activity.map((event) => (
          <div
            key={event.id}
            className="p-5 rounded-2xl bg-[#111113]/90 border border-white/10 flex flex-col md:flex-row md:items-center justify-between gap-4 hover:border-white/20 transition-all"
          >
            {/* Left Detail */}
            <div className="space-y-1.5 max-w-2xl">
              <div className="flex items-center gap-2.5 flex-wrap">
                <span className={`px-2 py-0.5 rounded text-[9px] font-mono border ${getActorBadge(event.actorType)}`}>
                  {event.actorType.toUpperCase()}
                </span>
                <span className="text-xs font-semibold text-white">{event.actor}</span>
                <span className="text-white/20 text-xs">•</span>
                <span className="text-xs font-medium text-[#E1D4C0]">{event.action}</span>
                {event.campaign && (
                  <>
                    <span className="text-white/20 text-xs">•</span>
                    <span className="text-[10px] font-mono text-white/40">{event.campaign}</span>
                  </>
                )}
              </div>

              <p className="text-xs text-white/80 font-light leading-relaxed">{event.detail}</p>
            </div>

            {/* Right Hash & Timestamp */}
            <div className="flex items-center gap-4 text-xs font-mono text-white/40 self-start md:self-auto shrink-0">
              <div className="flex items-center gap-1.5 text-[10px] text-emerald-400/80">
                <GitCommit className="w-3 h-3 text-[#E1D4C0]" />
                <span>{event.hash}</span>
              </div>
              <span className="text-[11px] text-white/30">{event.timestamp}</span>
            </div>
          </div>
        ))}
      </div>

    </div>
  );
}
