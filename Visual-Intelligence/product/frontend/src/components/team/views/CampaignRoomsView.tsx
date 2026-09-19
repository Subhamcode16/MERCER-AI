"use client";

import React from "react";
import Link from "next/link";
import { 
  FolderGit2, 
  ArrowRight, 
  Users, 
  AlertCircle, 
  ExternalLink,
  Layers,
  Sparkles,
  GitCommit
} from "lucide-react";
import type { CampaignRoom } from "@/lib/teamFixtures";

interface CampaignRoomsViewProps {
  rooms: CampaignRoom[];
}

export function CampaignRoomsView({ rooms }: CampaignRoomsViewProps) {
  return (
    <div className="space-y-8 animate-in fade-in duration-200">
      
      {/* Overview Banner */}
      <div className="p-6 rounded-2xl bg-card border border-border space-y-1 shadow-sm">
        <h2 className="text-base font-serif text-foreground font-medium flex items-center gap-2">
          <FolderGit2 className="w-4 h-4 text-primary" /> Active Campaign Collaborative Rooms
        </h2>
        <p className="text-xs text-muted-foreground font-light">
          Contextual workspaces connecting the digital creative workforce directly to active Campaign Studio initiatives.
        </p>
      </div>

      {/* Campaign Rooms Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {rooms.map((room) => (
          <div
            key={room.id}
            className="p-6 rounded-2xl bg-card border border-border space-y-6 hover:border-primary/40 transition-all flex flex-col justify-between shadow-sm"
          >
            {/* Header */}
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-mono tracking-widest uppercase text-primary bg-primary/10 border border-primary/20 px-2 py-0.5 rounded font-semibold">
                  {room.brand}
                </span>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-purple-500/10 text-purple-600 dark:text-purple-300 border border-purple-500/20 font-medium">
                  PHASE: {room.phase.toUpperCase()}
                </span>
              </div>

              <h3 className="text-lg font-serif text-foreground font-medium">{room.campaignName}</h3>
            </div>

            {/* Active Crew & Handoffs */}
            <div className="space-y-3 text-xs">
              <div className="p-3.5 rounded-xl bg-muted/30 border border-border space-y-2">
                <span className="text-[10px] font-mono text-muted-foreground uppercase tracking-wider flex items-center gap-1.5 font-medium">
                  <Users className="w-3.5 h-3.5 text-primary" /> Assigned Creative Crew:
                </span>
                <div className="flex items-center gap-2 flex-wrap">
                  {room.activeCoworkers.map((worker) => (
                    <div 
                      key={worker.id}
                      className="flex items-center gap-1.5 px-2 py-1 rounded-lg bg-background border border-border text-[11px] shadow-xs"
                    >
                      <span className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: worker.avatarColor }} />
                      <span className="text-foreground font-medium">{worker.name}</span>
                      <span className="text-muted-foreground text-[10px]">({worker.role.split(' ')[0]})</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Attention / Human Decision Required Alert if any */}
              {room.humanDecisionRequired && (
                <div className="p-3 rounded-xl bg-amber-500/[0.08] border border-amber-500/20 flex items-start gap-2.5 text-xs text-amber-900 dark:text-amber-200/90">
                  <AlertCircle className="w-4 h-4 text-amber-600 dark:text-amber-400 shrink-0 mt-0.5" />
                  <div>
                    <span className="font-semibold text-amber-700 dark:text-amber-300 text-[11px]">Human Decision Required:</span>
                    <p className="font-light mt-0.5">{room.humanDecisionRequired}</p>
                  </div>
                </div>
              )}
            </div>

            {/* Footer Deep Link Action */}
            <div className="pt-2 border-t border-border flex items-center justify-between">
              <span className="text-[11px] font-mono text-muted-foreground">
                {room.currentHandoffsCount} Active Handoffs
              </span>

              <Link
                href={room.studioLink}
                className="px-4 py-2 rounded-xl bg-primary text-primary-foreground font-semibold text-xs hover:opacity-90 transition-opacity flex items-center gap-1.5"
              >
                <span>Open in Campaign Studio</span>
                <ExternalLink className="w-3.5 h-3.5" />
              </Link>
            </div>
          </div>
        ))}
      </div>

    </div>
  );
}
