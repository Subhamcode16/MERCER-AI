"use client";

import React from "react";
import { 
  CheckCircle2, 
  Clock, 
  AlertCircle, 
  PauseCircle, 
  ArrowRight, 
  Sparkles,
  Layers,
  MessageSquare
} from "lucide-react";
import type { Coworker, CoworkerStatus } from "@/lib/teamFixtures";

interface CoworkerCardProps {
  coworker: Coworker;
  onSelect: (coworker: Coworker) => void;
  onOpenChat: (coworker: Coworker) => void;
}

export function CoworkerCard({ coworker, onSelect, onOpenChat }: CoworkerCardProps) {
  const getStatusBadge = (status: CoworkerStatus) => {
    switch (status) {
      case 'Working':
        return {
          label: 'Working',
          class: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30',
          dot: 'bg-emerald-400 animate-pulse'
        };
      case 'Needs You':
        return {
          label: 'Needs You',
          class: 'bg-rose-500/15 text-rose-300 border-rose-500/30 font-bold',
          dot: 'bg-rose-400 animate-ping'
        };
      case 'Waiting':
        return {
          label: 'Waiting',
          class: 'bg-amber-500/10 text-amber-300 border-amber-500/30',
          dot: 'bg-amber-400'
        };
      case 'Available':
        return {
          label: 'Available',
          class: 'bg-blue-500/10 text-blue-300 border-blue-500/30',
          dot: 'bg-blue-400'
        };
      case 'Blocked':
        return {
          label: 'Blocked',
          class: 'bg-zinc-500/20 text-zinc-400 border-zinc-500/30',
          dot: 'bg-zinc-400'
        };
      default:
        return {
          label: status,
          class: 'bg-white/5 text-white/40 border-white/10',
          dot: 'bg-white/40'
        };
    }
  };

  const statusInfo = getStatusBadge(coworker.status);

  return (
    <div 
      onClick={() => onSelect(coworker)}
      className="p-5 rounded-2xl bg-[#111113]/80 border border-white/10 hover:border-[#E1D4C0]/40 transition-all duration-300 flex flex-col justify-between space-y-4 cursor-pointer group hover:bg-[#141417] shadow-lg relative overflow-hidden"
    >
      {/* Top Identity & Status */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div 
              className="w-11 h-11 rounded-2xl flex items-center justify-center font-serif text-sm font-semibold border border-black/60 shadow-md group-hover:scale-105 transition-transform"
              style={{ backgroundColor: `${coworker.avatarColor}20`, color: coworker.avatarColor }}
            >
              {coworker.avatarInitials}
            </div>
            <div>
              <h3 className="text-sm font-medium text-white group-hover:text-[#E1D4C0] transition-colors flex items-center gap-1.5">
                {coworker.name}
              </h3>
              <p className="text-[11px] text-white/50 font-light">{coworker.role}</p>
            </div>
          </div>

          <span className={`px-2.5 py-1 rounded-full text-[9px] font-mono tracking-wider border flex items-center gap-1.5 ${statusInfo.class}`}>
            <span className={`w-1.5 h-1.5 rounded-full ${statusInfo.dot}`} />
            {statusInfo.label.toUpperCase()}
          </span>
        </div>

        {/* Short Bio */}
        <p className="text-xs text-white/60 font-light line-clamp-2 leading-relaxed">
          {coworker.bio}
        </p>
      </div>

      {/* Current Task & Campaign Pill */}
      <div className="space-y-2 pt-2 border-t border-white/5 text-xs">
        <div className="p-3 rounded-xl bg-white/[0.02] border border-white/5 space-y-1.5">
          <div className="flex items-center justify-between text-[10px] font-mono text-white/40">
            <span className="uppercase truncate max-w-[150px]">{coworker.currentWork.campaign}</span>
            <span className="text-[#E1D4C0]">{coworker.currentWork.progress}%</span>
          </div>
          <p className="text-[11px] text-white/90 font-light line-clamp-1">
            {coworker.currentWork.task}
          </p>
          <div className="h-1 w-full bg-white/5 rounded-full overflow-hidden">
            <div 
              className="h-full rounded-full transition-all duration-500" 
              style={{ width: `${coworker.currentWork.progress}%`, backgroundColor: coworker.avatarColor }}
            />
          </div>
        </div>
      </div>

      {/* Footer Action Strip */}
      <div className="flex items-center justify-between pt-1 text-[11px] text-white/40 font-mono">
        <span className="text-[10px] text-white/30 uppercase">{coworker.department}</span>
        
        <div className="flex items-center gap-2">
          <button
            onClick={(e) => {
              e.stopPropagation();
              onOpenChat(coworker);
            }}
            className="px-2.5 py-1 rounded-lg bg-white/[0.03] hover:bg-white/10 text-white/60 hover:text-white border border-white/5 transition-colors flex items-center gap-1"
          >
            <MessageSquare className="w-3 h-3" />
            <span>Chat</span>
          </button>
          
          <span className="text-[#E1D4C0] group-hover:translate-x-1 transition-transform flex items-center gap-0.5">
            Profile <ArrowRight className="w-3 h-3" />
          </span>
        </div>
      </div>
    </div>
  );
}
