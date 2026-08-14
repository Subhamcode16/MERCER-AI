"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { AGENT_PROFILES, BrandDnaData, AgentId, AgentTaskInfo } from "./types";
import { AgentAvatar } from "./AgentAvatar";
import { Users, ChevronRight, Image as ImageIcon, ShieldCheck } from "lucide-react";
import LoadingState from "../ui/loading-state";

interface AgentRosterPanelProps {
  brandDna: BrandDnaData | null;
  generatedAssets: { url: string; label: string }[];
  agentTasks?: Record<AgentId, AgentTaskInfo>;
}

export const AgentRosterPanel: React.FC<AgentRosterPanelProps> = ({
  brandDna,
  generatedAssets,
  agentTasks = {},
}) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="relative h-full flex shrink-0 z-30">
      {/* Collapsed Icon Bar */}
      <div className="w-12 h-full border-l border-white/5 bg-[#0C0C0E]/90 flex flex-col items-center py-6 gap-6 shrink-0 z-40">
        <button
          onClick={() => setIsOpen(!isOpen)}
          className={`w-8 h-8 rounded-xl flex items-center justify-center transition-all cursor-pointer ${
            isOpen
              ? "bg-[#E1D4C0] text-black shadow-lg"
              : "bg-white/5 text-white/50 hover:text-white hover:bg-white/10"
          }`}
          title={isOpen ? "Collapse Panel" : "Expand Agent Roster"}
        >
          <Users size={16} />
        </button>

        <div className="w-full h-[1px] bg-white/5" />

        {/* Collapsed Avatar Icons Stack */}
        <div className="flex flex-col gap-2 overflow-y-auto scrollbar-none py-2 items-center">
          {Object.values(AGENT_PROFILES).map((p) => {
            const task = agentTasks[p.id];
            const isProcessing = task?.status === "processing";
            return (
              <button
                key={p.id}
                onClick={() => setIsOpen(true)}
                className={`relative hover:scale-110 transition-transform cursor-pointer rounded-full ${
                  isProcessing ? "ring-2 ring-[#E1D4C0] ring-offset-2 ring-offset-black" : ""
                }`}
                title={`${p.handle} — ${p.role}`}
              >
                <AgentAvatar agentId={p.id} size="sm" />
              </button>
            );
          })}
        </div>
      </div>

      {/* Expanded Sliding Panel */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ width: 0, opacity: 0 }}
            animate={{ width: 320, opacity: 1 }}
            exit={{ width: 0, opacity: 0 }}
            transition={{ duration: 0.3, ease: [0.22, 1, 0.36, 1] }}
            className="h-full border-l border-white/5 bg-[#0C0C0E]/95 flex flex-col shrink-0 overflow-y-auto px-6 py-8 gap-8 backdrop-blur-xl shadow-2xl relative text-left"
          >
            <div className="flex justify-between items-center pb-2 border-b border-white/5">
              <span className="text-[9px] font-mono tracking-widest text-[#E1D4C0] uppercase font-bold flex items-center gap-2">
                <Users size={12} />
                Cooperative Roster
              </span>
              <button
                onClick={() => setIsOpen(false)}
                className="w-6 h-6 rounded-full border border-white/10 flex items-center justify-center text-white/40 hover:text-white hover:bg-white/5 transition-colors cursor-pointer"
              >
                <ChevronRight size={14} />
              </button>
            </div>

            {/* Brand Profile Details */}
            <div className="flex flex-col gap-3">
              <div className="flex justify-between items-baseline">
                <span className="text-[8px] font-mono tracking-widest text-white/30 uppercase">
                  Brand DNA Profile
                </span>
                <span className="text-[8px] font-mono text-emerald-400/80 uppercase flex items-center gap-1">
                  <ShieldCheck size={10} /> Active
                </span>
              </div>

              {brandDna ? (
                <div className="relative rounded-2xl border border-[#E1D4C0]/15 bg-white/[0.01] p-4 overflow-hidden shadow-xl">
                  <div className="absolute top-0 left-0 right-0 h-[1px] bg-gradient-to-r from-transparent via-[#E1D4C0]/20 to-transparent" />
                  <h3 className="font-serif text-[12px] text-[#E1D4C0] font-light leading-snug tracking-wide mb-2">
                    {brandDna.account}
                  </h3>

                  <div className="space-y-2 font-mono text-[8.5px]">
                    <div className="flex flex-col">
                      <span className="text-white/20 uppercase tracking-widest">
                        Archetype
                      </span>
                      <span className="text-[#E1D4C0]/85 font-light mt-0.5">
                        {brandDna.archetype}
                      </span>
                    </div>
                    <div className="flex flex-col">
                      <span className="text-white/20 uppercase tracking-widest">
                        Voice & Tone
                      </span>
                      <span className="text-[#E1D4C0]/85 font-light mt-0.5">
                        {brandDna.voice}
                      </span>
                    </div>
                    {brandDna.palette && (
                      <div className="flex flex-col">
                        <span className="text-white/20 uppercase tracking-widest">
                          Palette Tokens
                        </span>
                        <div className="flex gap-1.5 mt-1">
                          {brandDna.palette.map((color, i) => (
                            <div
                              key={i}
                              className="flex items-center gap-1 bg-white/5 border border-white/10 px-1.5 py-0.5 rounded"
                            >
                              <span
                                className="w-1.5 h-1.5 rounded-full shrink-0"
                                style={{ backgroundColor: color }}
                              />
                              <span className="text-[7.5px] uppercase tracking-wide text-white/40">
                                {color}
                              </span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              ) : (
                <div className="border border-dashed border-white/10 rounded-xl p-4 text-center">
                  <span className="text-[8.5px] font-mono text-white/30 uppercase">
                    No Brand DNA Scoped
                  </span>
                </div>
              )}
            </div>

            {/* Active Agents Roster + Live Task Cards */}
            <div className="flex flex-col gap-3">
              <span className="text-[8px] font-mono tracking-widest text-white/30 uppercase">
                Specialist Agents & Task Queue
              </span>
              <div className="flex flex-col gap-2">
                {Object.values(AGENT_PROFILES).map((agent) => {
                  const task = agentTasks[agent.id] || { status: "idle" };
                  const isProcessing = task.status === "processing";
                  const isCompleted = task.status === "completed";

                  return (
                    <div
                      key={agent.id}
                      className={`flex flex-col gap-1.5 bg-white/[0.01] border p-3 rounded-xl transition-all ${
                        isProcessing
                          ? "border-[#E1D4C0]/40 bg-[#E1D4C0]/[0.02]"
                          : isCompleted
                          ? "border-emerald-500/20 bg-emerald-500/[0.01]"
                          : "border-white/5"
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2 min-w-0">
                          <AgentAvatar agentId={agent.id} size="sm" />
                          <span className="text-[9.5px] font-mono text-white/80 tracking-wide font-medium truncate">
                            {agent.handle}
                          </span>
                        </div>

                        {/* Status Badge */}
                        <span
                          className={`text-[7px] font-mono tracking-wider uppercase px-1.5 py-0.5 rounded border ${
                            isProcessing
                              ? "bg-purple-500/10 border-purple-500/30 text-purple-300 animate-pulse"
                              : isCompleted
                              ? "bg-emerald-500/10 border-emerald-500/30 text-emerald-400"
                              : "bg-white/5 border-white/10 text-white/30"
                          }`}
                        >
                          {isProcessing ? "Processing" : isCompleted ? "Done" : "Idle"}
                        </span>
                      </div>

                      {/* Current Task Detail */}
                      {task.currentTask && (
                        <div className="pl-8 mt-1">
                          {isProcessing ? (
                            <LoadingState label={task.currentTask} variant="Drive" />
                          ) : (
                            <p className="text-[8px] font-mono text-emerald-400/80 truncate">
                              ✓ {task.currentTask}
                            </p>
                          )}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Campaign Assets library */}
            <div className="flex flex-col gap-3">
              <span className="text-[8px] font-mono tracking-widest text-white/30 uppercase">
                Generated Vault ({generatedAssets.length})
              </span>
              {generatedAssets.length === 0 ? (
                <div className="border border-dashed border-white/10 rounded-2xl p-6 text-center">
                  <ImageIcon className="w-5 h-5 text-white/10 mx-auto mb-2" />
                  <p className="text-[8.5px] font-mono tracking-wider text-white/30 uppercase">
                    Vault Empty
                  </p>
                </div>
              ) : (
                <div className="grid grid-cols-2 gap-2">
                  {generatedAssets.map((asset, i) => (
                    <div
                      key={i}
                      className="aspect-square bg-white/5 border border-white/10 rounded-xl overflow-hidden relative group cursor-pointer hover:border-[#E1D4C0]/40 transition-all duration-300"
                    >
                      <img
                        src={asset.url}
                        alt="output"
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                      />
                    </div>
                  ))}
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};
