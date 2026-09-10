"use client";

import React from "react";
import { AGENT_PROFILES, AgentId, DEPARTMENT_HANDLES, DEPARTMENT_NAMES, Department } from "./types";
import { AgentAvatar } from "./AgentAvatar";
import { motion, AnimatePresence } from "framer-motion";
import { Layers } from "lucide-react";

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

  // Department mentions
  const depts = (Object.keys(DEPARTMENT_HANDLES) as Department[]).filter((d) =>
    DEPARTMENT_HANDLES[d].toLowerCase().includes(query) ||
    DEPARTMENT_NAMES[d].toLowerCase().includes(query)
  );

  // Staff mentions (unique handles)
  const staffList = Object.values(AGENT_PROFILES).filter((p, index, self) =>
    index === self.findIndex((t) => t.handle === p.handle)
  );
  const profiles = staffList.filter(
    (p) =>
      p.name.toLowerCase().includes(query) ||
      p.handle.toLowerCase().includes(query) ||
      p.abbreviation.toLowerCase().includes(query) ||
      p.role.toLowerCase().includes(query)
  );

  if (depts.length === 0 && profiles.length === 0) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0, y: 10, scale: 0.98 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        exit={{ opacity: 0, y: 10, scale: 0.98 }}
        transition={{ duration: 0.15 }}
        className="absolute bottom-full left-0 mb-2 w-80 bg-[#0C0C0E]/95 border border-[#E1D4C0]/25 rounded-2xl p-2 shadow-2xl backdrop-blur-xl z-50 overflow-hidden"
      >
        <div className="px-3 py-1.5 border-b border-white/5 flex justify-between items-center mb-1">
          <span className="text-[8.5px] font-mono tracking-widest uppercase text-white/40">
            Mention Workforce / Department
          </span>
          <span className="text-[8px] font-mono text-[#E1D4C0]/50">
            {depts.length + profiles.length} options
          </span>
        </div>

        <div className="max-h-56 overflow-y-auto scrollbar-none flex flex-col gap-1">
          {/* Department Handles */}
          {depts.map((d) => (
            <button
              key={`dept-${d}`}
              onClick={() => onSelect(DEPARTMENT_HANDLES[d])}
              className="flex items-center gap-3 p-2 rounded-xl bg-amber-500/5 border border-amber-500/10 hover:bg-amber-500/10 text-left transition-colors cursor-pointer w-full group"
            >
              <div className="w-6 h-6 rounded-lg bg-amber-500/20 text-amber-300 flex items-center justify-center font-mono text-[9px] font-bold shrink-0">
                <Layers size={12} />
              </div>
              <div className="flex flex-col min-w-0 flex-1">
                <span className="text-[10px] font-mono font-bold text-amber-200 group-hover:text-white truncate">
                  {DEPARTMENT_HANDLES[d]}
                </span>
                <span className="text-[8px] font-sans text-amber-200/60 truncate">
                  {DEPARTMENT_NAMES[d]} (All Department Staff)
                </span>
              </div>
            </button>
          ))}

          {/* Individual Staff Profiles */}
          {profiles.map((p) => (
            <button
              key={p.id}
              onClick={() => onSelect(p.handle)}
              className="flex items-center gap-3 p-2 rounded-xl hover:bg-white/5 text-left transition-colors cursor-pointer w-full group"
            >
              <AgentAvatar agentId={p.id as AgentId} size="sm" showStatusDot={false} />
              <div className="flex flex-col min-w-0 flex-1">
                <div className="flex items-center justify-between">
                  <span className="text-[9.5px] font-mono font-medium text-[#E1D4C0] group-hover:text-white truncate">
                    {p.handle}
                  </span>
                  <span className="text-[7px] font-mono text-white/30 border border-white/10 px-1 py-0.2 rounded">
                    {p.authority}
                  </span>
                </div>
                <span className="text-[8px] font-sans text-white/30 truncate">
                  {p.name} — {p.role}
                </span>
              </div>
            </button>
          ))}
        </div>
      </motion.div>
    </AnimatePresence>
  );
};

