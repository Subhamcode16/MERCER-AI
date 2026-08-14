"use client";

import React from "react";
import { motion } from "framer-motion";
import { AgentAvatar } from "./AgentAvatar";
import { AGENT_PROFILES, AgentId } from "./types";
import LoadingState from "../ui/loading-state";

interface TypingIndicatorProps {
  agentId: AgentId;
}

export const TypingIndicator: React.FC<TypingIndicatorProps> = ({ agentId }) => {
  const profile = AGENT_PROFILES[agentId];

  return (
    <motion.div
      initial={{ opacity: 0, y: 5 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0 }}
      className="flex items-center gap-3 px-2 self-start my-2"
    >
      <AgentAvatar agentId={agentId} size="sm" />
      <div className="flex items-center gap-2 bg-[#0C0C0E]/80 border border-white/10 px-4 py-2 rounded-2xl">
        <span className="text-[10px] font-mono text-[#E1D4C0]/70 font-medium">
          {profile?.handle || agentId}
        </span>
        <div className="flex items-center ml-2">
          <LoadingState label="Thinking" variant="Drive" />
        </div>
      </div>
    </motion.div>
  );
};
