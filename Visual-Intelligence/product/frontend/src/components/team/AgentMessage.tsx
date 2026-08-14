"use client";

import React from "react";
import { motion } from "framer-motion";
import { AgentAvatar } from "./AgentAvatar";
import { AGENT_PROFILES, AgentId } from "./types";

interface AgentMessageProps {
  sender: AgentId;
  time: string;
  text?: string;
  children?: React.ReactNode;
}

export const AgentMessage: React.FC<AgentMessageProps> = ({
  sender,
  time,
  text,
  children,
}) => {
  const profile = AGENT_PROFILES[sender];

  return (
    <motion.div
      initial={{ opacity: 0, y: 12, filter: "blur(4px)" }}
      animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
      transition={{ duration: 0.45, ease: [0.215, 0.61, 0.355, 1] }}
      className="flex flex-col items-start w-full"
    >
      {/* Header with avatar, handle, and time */}
      <div className="flex items-center gap-2.5 mb-1.5 px-1">
        <AgentAvatar agentId={sender} size="sm" />
        <span className="text-[11px] font-mono text-[#E1D4C0] font-medium tracking-wide">
          {profile?.handle || sender}
        </span>
        <span className="text-[9px] font-mono text-white/30">{time}</span>
      </div>

      {/* Narrative Message Bubble */}
      {text && (
        <div className="bg-[#0C0C0E]/90 border border-white/10 rounded-2xl px-5 py-3 max-w-lg text-left shadow-lg backdrop-blur-md">
          <p className="text-[12px] font-sans text-white/85 leading-relaxed font-light whitespace-pre-wrap">
            {text}
          </p>
        </div>
      )}

      {/* Structured Card Slot */}
      {children}
    </motion.div>
  );
};
