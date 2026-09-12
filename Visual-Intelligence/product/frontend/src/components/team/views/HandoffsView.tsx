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
      <div className="p-6 rounded-2xl bg-[#111113]/80 border border-white/10 space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <GitCommit className="w-5 h-5 text-[#E1D4C0]" />
              <h2 className="text-lg font-serif text-white font-medium">Inter-Coworker Creative Handoffs</h2>
            </div>
            <p className="text-xs text-white/50 font-light">
              Transparent, accountable handoff chains tracking work transitions, evidence payloads, and output states.
            </p>
          </div>

          <div className="px-3 py-1.5 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-300 text-xs font-mono flex items-center gap-2">
            <Lock className="w-3.5 h-3.5 text-amber-400" />
            <span>Collaboration &ne; Privilege Transfer</span>
          </div>
        </div>
      </div>

      {/* Handoffs Pipeline Cards */}
      <div className="space-y-4">
        {handoffs.map((hoff) => (
          <div
            key={hoff.id}
            className="p-6 rounded-2xl bg-[#111113]/90 border border-white/10 space-y-5 hover:border-[#E1D4C0]/30 transition-all"
          >
            {/* Header: Sender -> Receiver */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-white/5 pb-4">
              
              <div className="flex items-center gap-3 flex-wrap">
                {/* Sender */}
                <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-white/[0.02] border border-white/5 text-xs">
                  <span className="w-2 h-2 rounded-full" style={{ backgroundColor: hoff.sender.avatarColor }} />
                  <span className="text-white font-medium">{hoff.sender.name}</span>
                  <span className="text-white/40 text-[10px]">({hoff.sender.role.split(' ')[0]})</span>
                </div>

                <div className="text-white/30 text-xs flex items-center gap-1 font-mono">
                  &rarr;
                </div>

                {/* Receiver */}
                <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-white/[0.02] border border-white/5 text-xs">
                  <span className="w-2 h-2 rounded-full" style={{ backgroundColor: hoff.receiver.avatarColor }} />
                  <span className="text-white font-medium">{hoff.receiver.name}</span>
                  <span className="text-white/40 text-[10px]">({hoff.receiver.role.split(' ')[0]})</span>
                </div>
              </div>

              {/* Status & Timestamp */}
              <div className="flex items-center gap-3">
                <span className={`px-2.5 py-0.5 rounded text-[10px] font-mono border ${getStatusBadge(hoff.status)}`}>
                  {hoff.status.toUpperCase()}
                </span>
                <span className="text-[11px] font-mono text-white/40">{hoff.timestamp}</span>
              </div>

            </div>

            {/* Purpose & Attached Outputs */}
            <div className="space-y-3 text-xs">
              <div className="space-y-1">
                <span className="text-[10px] font-mono text-white/40 uppercase tracking-wider">Handoff Purpose</span>
                <p className="text-white/90 leading-relaxed font-light">{hoff.purpose}</p>
              </div>

              {/* Attached Outputs Matrix */}
              <div className="p-3.5 rounded-xl bg-white/[0.02] border border-white/5 space-y-1.5">
                <span className="text-[10px] font-mono text-white/40 uppercase tracking-wider flex items-center gap-1.5">
                  <FileText className="w-3 h-3 text-[#E1D4C0]" /> Attached Creative Outputs & Evidence
                </span>
                <div className="flex items-center gap-2 flex-wrap pt-1">
                  {hoff.attachedOutputs.map((out, oIdx) => (
                    <span key={oIdx} className="px-2.5 py-1 rounded-lg bg-black/60 border border-white/10 text-[11px] font-mono text-[#E1D4C0]">
                      {out}
                    </span>
                  ))}
                </div>
                <p className="text-[11px] text-white/60 font-light pt-1 italic">
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
