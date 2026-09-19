"use client";

import React from "react";
import { 
  GitCommit, 
  ArrowRight, 
  CheckCircle2, 
  Clock, 
  AlertCircle, 
  FileText, 
  Layers, 
  ShieldCheck,
  Lock
} from "lucide-react";
import type { HandoffStatus, TeamHandoff } from "@/lib/teamFixtures";

interface HandoffsViewProps {
  handoffs: TeamHandoff[];
}

export function HandoffsView({ handoffs }: HandoffsViewProps) {
  const getStatusBadge = (status: HandoffStatus) => {
    switch (status) {
      case 'Completed':
        return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
      case 'Working':
        return 'bg-blue-500/10 text-blue-400 border-blue-500/30';
      case 'Proposed':
        return 'bg-amber-500/10 text-amber-300 border-amber-500/30';
      case 'Blocked':
      case 'Returned':
      default:
        return 'bg-rose-500/10 text-rose-300 border-rose-500/30';
    }
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-200">
      
      {/* Overview & Invariant Alert */}
      <div className="p-6 rounded-2xl bg-card border border-border space-y-4 shadow-sm">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <GitCommit className="w-5 h-5 text-primary" />
              <h2 className="text-lg font-serif text-foreground font-medium">Inter-Coworker Creative Handoffs</h2>
            </div>
            <p className="text-xs text-muted-foreground font-light">
              Transparent, accountable handoff chains tracking work transitions, evidence payloads, and output states.
            </p>
          </div>

          <div className="px-3 py-1.5 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-700 dark:text-amber-300 text-xs font-mono flex items-center gap-2">
            <Lock className="w-3.5 h-3.5 text-amber-600 dark:text-amber-400" />
            <span>Collaboration &ne; Privilege Transfer</span>
          </div>
        </div>
      </div>

      {/* Handoffs Pipeline Cards */}
      <div className="space-y-4">
        {handoffs.map((hoff) => (
          <div
            key={hoff.id}
            className="p-6 rounded-2xl bg-card border border-border space-y-5 hover:border-primary/40 transition-all shadow-sm"
          >
            {/* Header: Sender -> Receiver */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-border pb-4">
              
              <div className="flex items-center gap-3 flex-wrap">
                {/* Sender */}
                <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-muted/40 border border-border text-xs">
                  <span className="w-2 h-2 rounded-full" style={{ backgroundColor: hoff.sender.avatarColor }} />
                  <span className="text-foreground font-medium">{hoff.sender.name}</span>
                  <span className="text-muted-foreground text-[10px]">({hoff.sender.role.split(' ')[0]})</span>
                </div>

                <div className="text-muted-foreground/60 text-xs flex items-center gap-1 font-mono">
                  &rarr;
                </div>

                {/* Receiver */}
                <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-muted/40 border border-border text-xs">
                  <span className="w-2 h-2 rounded-full" style={{ backgroundColor: hoff.receiver.avatarColor }} />
                  <span className="text-foreground font-medium">{hoff.receiver.name}</span>
                  <span className="text-muted-foreground text-[10px]">({hoff.receiver.role.split(' ')[0]})</span>
                </div>
              </div>

              {/* Status & Timestamp */}
              <div className="flex items-center gap-3">
                <span className={`px-2.5 py-0.5 rounded text-[10px] font-mono border font-medium ${getStatusBadge(hoff.status)}`}>
                  {hoff.status.toUpperCase()}
                </span>
                <span className="text-[11px] font-mono text-muted-foreground">{hoff.timestamp}</span>
              </div>

            </div>

            {/* Purpose & Attached Outputs */}
            <div className="space-y-3 text-xs">
              <div className="space-y-1">
                <span className="text-[10px] font-mono text-muted-foreground uppercase tracking-wider">Handoff Purpose</span>
                <p className="text-foreground/90 leading-relaxed font-light">{hoff.purpose}</p>
              </div>

              {/* Attached Outputs Matrix */}
              <div className="p-3.5 rounded-xl bg-muted/30 border border-border space-y-1.5">
                <span className="text-[10px] font-mono text-muted-foreground uppercase tracking-wider flex items-center gap-1.5 font-medium">
                  <FileText className="w-3 h-3 text-primary" /> Attached Creative Outputs & Evidence
                </span>
                <div className="flex items-center gap-2 flex-wrap pt-1">
                  {hoff.attachedOutputs.map((out, oIdx) => (
                    <span key={oIdx} className="px-2.5 py-1 rounded-lg bg-background border border-border text-[11px] font-mono text-primary shadow-xs">
                      {out}
                    </span>
                  ))}
                </div>
                <p className="text-[11px] text-muted-foreground font-light pt-1 italic">
                  "{hoff.evidenceSummary}"
                </p>
              </div>
            </div>

          </div>
        ))}
      </div>

    </div>
  );
}
