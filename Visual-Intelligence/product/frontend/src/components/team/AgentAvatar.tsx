"use client";

import React from "react";
import { AGENT_PROFILES, AgentId } from "./types";

interface AgentAvatarProps {
  agentId: AgentId;
  size?: "sm" | "md" | "lg";
  showStatusDot?: boolean;
}

export const AgentAvatar: React.FC<AgentAvatarProps> = ({
  agentId,
  size = "md",
  showStatusDot = true,
}) => {
  const profile = AGENT_PROFILES[agentId] || {
    abbreviation: "AG",
    gradient: "from-[#E1D4C0]/20 to-[#E1D4C0]/40",
  };

  const sizeClasses = {
    sm: "w-6 h-6 text-[9px]",
    md: "w-8 h-8 text-[11px]",
    lg: "w-10 h-10 text-[13px]",
  };

  const dotSizes = {
    sm: "w-1.5 h-1.5",
    md: "w-2 h-2",
    lg: "w-2.5 h-2.5",
  };

  return (
    <div className="relative shrink-0 inline-flex items-center justify-center">
      <div
        className={`${sizeClasses[size]} rounded-full bg-gradient-to-br ${profile.gradient} border border-[#E1D4C0]/30 flex items-center justify-center font-mono font-bold text-[#E1D4C0] shadow-md select-none`}
      >
        {profile.abbreviation}
      </div>
      {showStatusDot && (
        <span
          className={`absolute bottom-0 right-0 ${dotSizes[size]} rounded-full bg-emerald-400 border border-black animate-pulse`}
        />
      )}
    </div>
  );
};
