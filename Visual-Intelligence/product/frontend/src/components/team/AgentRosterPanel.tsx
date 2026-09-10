import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  AGENT_PROFILES,
  BrandDnaData,
  AgentId,
  AgentTaskInfo,
  DEPARTMENT_NAMES,
  Department,
  AgentProfile,
  StaffDossier,
  DEFAULT_STAFF_DOSSIERS,
} from "./types";
import { AgentAvatar } from "./AgentAvatar";
import { StaffDossierModal } from "./StaffDossierModal";
import { Users, ChevronRight, ChevronDown, Image as ImageIcon, ShieldCheck, Layers, FileText } from "lucide-react";
import LoadingState from "../ui/loading-state";

interface AgentRosterPanelProps {
  brandDna: BrandDnaData | null;
  generatedAssets: { url: string; label: string }[];
  agentTasks?: Record<string, AgentTaskInfo>;
}

export const AgentRosterPanel: React.FC<AgentRosterPanelProps> = ({
  brandDna,
  generatedAssets,
  agentTasks = {},
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [dossierModalOpen, setDossierModalOpen] = useState(false);
  const [selectedDossier, setSelectedDossier] = useState<StaffDossier | null>(null);
  const [selectedAgentId, setSelectedAgentId] = useState<AgentId | undefined>(undefined);
  const [dossiersMap, setDossiersMap] = useState<Record<string, StaffDossier>>(DEFAULT_STAFF_DOSSIERS);

  // Fetch dynamic dossiers from backend if available
  useEffect(() => {
    fetch("/api/team/workforce/dossiers")
      .then((res) => res.ok ? res.json() : null)
      .then((data) => {
        if (data?.dossiers && Array.isArray(data.dossiers)) {
          const map: Record<string, StaffDossier> = {};
          data.dossiers.forEach((d: StaffDossier) => {
            map[d.staff_id] = d;
            if (d.handle) map[d.handle] = d;
          });
          setDossiersMap((prev) => ({ ...prev, ...map }));
        }
      })
      .catch(() => {
        // Fallback gracefully to default bundled dossiers
      });
  }, []);

  const [openDepts, setOpenDepts] = useState<Record<Department, boolean>>({
    STRATEGY: true,
    CREATIVE: true,
    INTELLIGENCE: true,
    CONTENT: false,
    QUALITY: true,
  });

  const toggleDept = (dept: Department) => {
    setOpenDepts((prev) => ({ ...prev, [dept]: !prev[dept] }));
  };

  const openDossierForAgent = (agent: AgentProfile) => {
    // Resolve dossier by handle or by sanitized id
    const cleanHandle = agent.handle.replace("@", "");
    const cleanId = agent.id.replace(/-/g, "_") + "_01";
    
    const dossier =
      dossiersMap[cleanHandle] ||
      dossiersMap[agent.handle] ||
      dossiersMap[cleanId] ||
      dossiersMap[agent.id] ||
      DEFAULT_STAFF_DOSSIERS[cleanHandle] ||
      DEFAULT_STAFF_DOSSIERS[cleanId] ||
      Object.values(dossiersMap).find((d) => d.role.toLowerCase() === agent.role.toLowerCase()) ||
      null;

    if (dossier) {
      setSelectedDossier(dossier);
      setSelectedAgentId(agent.id);
      setDossierModalOpen(true);
    }
  };


  // Group unique agents by department
  const depts: Department[] = ['STRATEGY', 'CREATIVE', 'INTELLIGENCE', 'CONTENT', 'QUALITY'];
  
  // Deduplicate agents by handle
  const uniqueAgents = Object.values(AGENT_PROFILES).reduce<AgentProfile[]>((acc, agent) => {
    if (!acc.some((a) => a.handle === agent.handle)) {
      acc.push(agent);
    }
    return acc;
  }, []);

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
          {uniqueAgents.map((p) => {
            const task = agentTasks[p.id];
            const isProcessing = task?.status === "processing";
            return (
              <button
                key={p.id}
                onClick={() => openDossierForAgent(p)}
                className={`relative hover:scale-110 transition-transform cursor-pointer rounded-full ${
                  isProcessing ? "ring-2 ring-[#E1D4C0] ring-offset-2 ring-offset-black" : ""
                }`}
                title={`Inspect Dossier: ${p.handle} [${p.authority}] — ${p.role}`}
              >
                <AgentAvatar agentId={p.id as AgentId} size="sm" />
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
            animate={{ width: 340, opacity: 1 }}
            exit={{ width: 0, opacity: 0 }}
            transition={{ duration: 0.3, ease: [0.22, 1, 0.36, 1] }}
            className="h-full border-l border-white/5 bg-[#0C0C0E]/95 flex flex-col shrink-0 overflow-y-auto px-6 py-8 gap-6 backdrop-blur-xl shadow-2xl relative text-left"
          >
            <div className="flex justify-between items-center pb-2 border-b border-white/5">
              <span className="text-[9px] font-mono tracking-widest text-[#E1D4C0] uppercase font-bold flex items-center gap-2">
                <Users size={12} />
                Governed Workforce Roster
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

            {/* Department Accordions & Active Staff Queue */}
            <div className="flex flex-col gap-3">
              <span className="text-[8px] font-mono tracking-widest text-white/30 uppercase flex items-center gap-1.5">
                <Layers size={10} />
                Department Accordions & Staff
              </span>

              <div className="flex flex-col gap-3">
                {depts.map((dept) => {
                  const isDeptOpen = openDepts[dept];
                  const deptStaff = uniqueAgents.filter((a) => a.department === dept);

                  return (
                    <div
                      key={dept}
                      className="border border-white/10 rounded-xl overflow-hidden bg-white/[0.01]"
                    >
                      {/* Department Accordion Header */}
                      <button
                        onClick={() => toggleDept(dept)}
                        className="w-full px-3 py-2.5 flex items-center justify-between bg-white/[0.02] hover:bg-white/[0.04] transition-colors cursor-pointer border-b border-white/5"
                      >
                        <span className="text-[9px] font-mono font-semibold tracking-wider text-[#E1D4C0] uppercase flex items-center gap-1.5">
                          {DEPARTMENT_NAMES[dept]}
                        </span>
                        <div className="flex items-center gap-2">
                          <span className="text-[8px] font-mono text-white/30 bg-white/5 px-1.5 py-0.5 rounded">
                            {deptStaff.length} Staff
                          </span>
                          {isDeptOpen ? (
                            <ChevronDown size={12} className="text-white/40" />
                          ) : (
                            <ChevronRight size={12} className="text-white/40" />
                          )}
                        </div>
                      </button>

                      {/* Staff Cards inside Department */}
                      {isDeptOpen && (
                        <div className="p-2 flex flex-col gap-2 bg-black/20">
                          {deptStaff.map((agent) => {
                            const task = agentTasks[agent.id] || { status: "idle" };
                            const isProcessing = task.status === "processing";
                            const isCompleted = task.status === "completed";

                            const authorityBadgeColor =
                              agent.authority === "PROPOSE"
                                ? "border-amber-500/30 text-amber-300 bg-amber-500/10"
                                : agent.authority === "CRITIQUE"
                                ? "border-rose-500/30 text-rose-300 bg-rose-500/10"
                                : agent.authority === "REVIEW"
                                ? "border-emerald-500/30 text-emerald-300 bg-emerald-500/10"
                                : "border-indigo-500/30 text-indigo-300 bg-indigo-500/10";

                            return (
                              <button
                                key={agent.id}
                                onClick={() => openDossierForAgent(agent)}
                                className={`w-full text-left flex flex-col gap-1.5 bg-white/[0.01] hover:bg-white/[0.04] border p-2.5 rounded-lg transition-all cursor-pointer group ${
                                  isProcessing
                                    ? "border-[#E1D4C0]/40 bg-[#E1D4C0]/[0.02]"
                                    : isCompleted
                                    ? "border-emerald-500/20 bg-emerald-500/[0.01]"
                                    : "border-white/5 hover:border-[#E1D4C0]/30"
                                }`}
                              >
                                <div className="flex items-center justify-between w-full">
                                  <div className="flex items-center gap-2 min-w-0">
                                    <AgentAvatar agentId={agent.id as AgentId} size="sm" />
                                    <div className="flex flex-col min-w-0">
                                      <div className="flex items-center gap-1">
                                        <span className="text-[9px] font-mono text-white/90 group-hover:text-[#E1D4C0] font-medium truncate transition-colors">
                                          {agent.handle}
                                        </span>
                                        <FileText size={9} className="text-white/20 group-hover:text-[#E1D4C0]/70 shrink-0" />
                                      </div>
                                      <span className="text-[7.5px] font-sans text-white/40 truncate">
                                        {agent.role}
                                      </span>
                                    </div>
                                  </div>

                                  <div className="flex items-center gap-1">
                                    {/* Authority Tag */}
                                    <span
                                      className={`text-[6.5px] font-mono tracking-wider uppercase px-1 py-0.5 rounded border ${authorityBadgeColor}`}
                                      title={`Authority Class: ${agent.authority}`}
                                    >
                                      {agent.authority}
                                    </span>

                                    {/* Status Badge */}
                                    <span
                                      className={`text-[6.5px] font-mono tracking-wider uppercase px-1 py-0.5 rounded border ${
                                        isProcessing
                                          ? "bg-purple-500/10 border-purple-500/30 text-purple-300 animate-pulse"
                                          : isCompleted
                                          ? "bg-emerald-500/10 border-emerald-500/30 text-emerald-400"
                                          : "bg-white/5 border-white/10 text-white/30"
                                      }`}
                                    >
                                      {isProcessing ? "Run" : isCompleted ? "Done" : "Idle"}
                                    </span>
                                  </div>
                                </div>

                                {/* Current Task Detail */}
                                {task.currentTask && (
                                  <div className="pl-7 mt-0.5">
                                    {isProcessing ? (
                                      <LoadingState label={task.currentTask} variant="Drive" />
                                    ) : (
                                      <p className="text-[7.5px] font-mono text-emerald-400/80 truncate">
                                        ✓ {task.currentTask}
                                      </p>
                                    )}
                                  </div>
                                )}
                              </button>
                            );
                          })}
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

      {/* Staff Dossier Modal */}
      <StaffDossierModal
        isOpen={dossierModalOpen}
        onClose={() => setDossierModalOpen(false)}
        dossier={selectedDossier}
        agentId={selectedAgentId}
      />
    </div>
  );
};

