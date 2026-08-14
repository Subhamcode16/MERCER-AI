"use client";

import React from "react";
import { AGENT_PROFILES, AgentId } from "./types";
import { AgentAvatar } from "./AgentAvatar";
import { motion, AnimatePresence } from "framer-motion";

interface MentionAutocompleteProps {
  filterText: string;
  onSelect: (handle: string) => void;
  onClose: () => void;
}

export const MentionAutocomplete: React.FC<MentionAutocompleteProps> = ({
  filterText,
  onSelect,
  onClose,
}) => {
  const query = filterText.toLowerCase().replace("@", "");
  const profiles = Object.values(AGENT_PROFILES).filter(
    (p) =>
      p.name.toLowerCase().includes(query) ||
      p.handle.toLowerCase().includes(query) ||
      p.abbreviation.toLowerCase().includes(query)
  );

  if (profiles.length === 0) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0, y: 10, scale: 0.98 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        exit={{ opacity: 0, y: 10, scale: 0.98 }}
        transition={{ duration: 0.15 }}
        className="absolute bottom-full left-0 mb-2 w-72 bg-[#0C0C0E]/95 border border-[#E1D4C0]/25 rounded-2xl p-2 shadow-2xl backdrop-blur-xl z-50 overflow-hidden"
      >
        <div className="px-3 py-1.5 border-b border-white/5 flex justify-between items-center mb-1">
          <span className="text-[8.5px] font-mono tracking-widest uppercase text-white/40">
            Mention Agent
          </span>
          <span className="text-[8px] font-mono text-[#E1D4C0]/50">
            {profiles.length} available
          </span>
        </div>

        <div className="max-h-48 overflow-y-auto scrollbar-none flex flex-col gap-1">
          {profiles.map((p) => (
            <button
              key={p.id}
              onClick={() => onSelect(p.handle)}
              className="flex items-center gap-3 p-2 rounded-xl hover:bg-white/5 text-left transition-colors cursor-pointer w-full group"
            >
              <AgentAvatar agentId={p.id} size="sm" showStatusDot={false} />
              <div className="flex flex-col min-w-0 flex-1">
                <span className="text-[10px] font-mono font-medium text-[#E1D4C0] group-hover:text-white truncate">
                  {p.handle}
                </span>
                <span className="text-[8.5px] font-sans text-white/30 truncate">
                  {p.role}
                </span>
              </div>
            </button>
          ))}
        </div>
      </motion.div>
    </AnimatePresence>
  );
};
