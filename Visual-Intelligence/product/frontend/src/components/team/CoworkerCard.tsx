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
      className="p-5 rounded-2xl bg-card border border-border hover:border-primary/40 transition-all duration-300 flex flex-col justify-between space-y-4 cursor-pointer group hover:bg-card shadow-sm relative overflow-hidden"
    >
      {/* Top Identity & Status */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div 
              className="w-11 h-11 rounded-2xl flex items-center justify-center font-serif text-sm font-semibold border border-border shadow-xs group-hover:scale-105 transition-transform"
              style={{ backgroundColor: `${coworker.avatarColor}20`, color: coworker.avatarColor }}
            >
              {coworker.avatarInitials}
            </div>
            <div>
              <h3 className="text-sm font-medium text-foreground group-hover:text-primary transition-colors flex items-center gap-1.5">
                {coworker.name}
              </h3>
              <p className="text-[11px] text-muted-foreground font-light">{coworker.role}</p>
            </div>
          </div>

          <span className={`px-2.5 py-1 rounded-full text-[9px] font-mono tracking-wider border flex items-center gap-1.5 ${statusInfo.class}`}>
            <span className={`w-1.5 h-1.5 rounded-full ${statusInfo.dot}`} />
            {statusInfo.label.toUpperCase()}
          </span>
        </div>

        {/* Short Bio */}
        <p className="text-xs text-muted-foreground font-light line-clamp-2 leading-relaxed">
          {coworker.bio}
        </p>
      </div>

      {/* Current Task & Campaign Pill */}
      <div className="space-y-2 pt-2 border-t border-border/40 text-xs">
        <div className="p-3 rounded-xl bg-muted/40 border border-border space-y-1.5">
          <div className="flex items-center justify-between text-[10px] font-mono text-muted-foreground/70">
            <span className="uppercase truncate max-w-[150px]">{coworker.currentWork.campaign}</span>
            <span className="text-primary font-semibold">{coworker.currentWork.progress}%</span>
          </div>
          <p className="text-[11px] text-foreground font-light line-clamp-1">
            {coworker.currentWork.task}
          </p>
          <div className="h-1 w-full bg-muted rounded-full overflow-hidden">
            <div 
              className="h-full rounded-full transition-all duration-500" 
              style={{ width: `${coworker.currentWork.progress}%`, backgroundColor: coworker.avatarColor }}
            />
          </div>
        </div>
      </div>

      {/* Footer Action Strip */}
      <div className="flex items-center justify-between pt-1 text-[11px] text-muted-foreground font-mono">
        <span className="text-[10px] text-muted-foreground/60 uppercase">{coworker.department}</span>
        
        <div className="flex items-center gap-2">
          <button
            onClick={(e) => {
              e.stopPropagation();
              onOpenChat(coworker);
            }}
            className="px-2.5 py-1 rounded-lg bg-accent/50 hover:bg-accent text-accent-foreground border border-border/50 transition-colors flex items-center gap-1 cursor-pointer"
          >
            <MessageSquare className="w-3 h-3 text-primary" />
            <span>Chat</span>
          </button>
          
          <span className="text-primary group-hover:translate-x-1 transition-transform flex items-center gap-0.5 font-medium">
            Profile <ArrowRight className="w-3 h-3" />
          </span>
        </div>
      </div>
    </div>
  );
}
