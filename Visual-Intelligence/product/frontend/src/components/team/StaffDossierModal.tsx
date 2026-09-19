"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  StaffDossier,
  AgentId,
  DEPARTMENT_NAMES,
} from "./types";
import { AgentAvatar } from "./AgentAvatar";
import {
  X,
  Sparkles,
  Cpu,
  Wrench,
  BookOpen,
  Terminal,
  ShieldCheck,
  CheckCircle2,
  Copy,
  Layers,
} from "lucide-react";

interface StaffDossierModalProps {
  dossier: StaffDossier | null;
  agentId?: AgentId;
  isOpen: boolean;
  onClose: () => void;
}

type TabType = "overview" | "skills" | "system_prompt" | "tools";

export const StaffDossierModal: React.FC<StaffDossierModalProps> = ({
  dossier,
  agentId,
  isOpen,
  onClose,
}) => {
  const [activeTab, setActiveTab] = useState<TabType>("overview");
  const [copiedPrompt, setCopiedPrompt] = useState(false);

  if (!isOpen || !dossier) return null;

  const handleCopyPrompt = () => {
    navigator.clipboard.writeText(dossier.system_instruction);
    setCopiedPrompt(true);
    setTimeout(() => setCopiedPrompt(false), 2000);
  };

  const authorityBadgeStyles =
    dossier.authority_class === "PROPOSE"
      ? "border-amber-500/30 text-amber-300 bg-amber-500/10"
      : dossier.authority_class === "CRITIQUE"
      ? "border-rose-500/30 text-rose-300 bg-rose-500/10"
      : dossier.authority_class === "REVIEW"
      ? "border-emerald-500/30 text-emerald-300 bg-emerald-500/10"
      : "border-indigo-500/30 text-indigo-300 bg-indigo-500/10";

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 md:p-10">
        {/* Backdrop */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={onClose}
          className="absolute inset-0 bg-black/80 backdrop-blur-md"
        />

        {/* Modal Container */}
        <motion.div
          initial={{ scale: 0.95, opacity: 0, y: 16 }}
          animate={{ scale: 1, opacity: 1, y: 0 }}
          exit={{ scale: 0.95, opacity: 0, y: 16 }}
          transition={{ duration: 0.25, ease: [0.22, 1, 0.36, 1] }}
          className="relative w-full max-w-3xl max-h-[85vh] bg-card border border-border rounded-2xl shadow-2xl overflow-hidden flex flex-col backdrop-blur-2xl text-left z-10"
        >
          {/* Header Glow Bar */}
          <div className="absolute top-0 left-0 right-0 h-[1px] bg-gradient-to-r from-transparent via-primary/40 to-transparent" />

          {/* Modal Header */}
          <div className="px-6 py-5 border-b border-border flex items-center justify-between shrink-0 bg-muted/20">
            <div className="flex items-center gap-4 min-w-0">
              <AgentAvatar
                agentId={(agentId || dossier.staff_id.replace("_01", "").replace(/_/g, "-")) as AgentId}
                size="lg"
              />
              <div className="flex flex-col min-w-0">
                <div className="flex items-center gap-2.5 flex-wrap">
                  <h2 className="font-serif text-lg text-foreground font-light tracking-wide truncate">
                    {dossier.name}
                  </h2>
                  <span className="text-[10px] font-mono text-muted-foreground">
                    {dossier.handle}
                  </span>
                  <span
                    className={`text-[8px] font-mono tracking-wider uppercase px-2 py-0.5 rounded border ${authorityBadgeStyles}`}
                  >
                    {dossier.authority_class}
                  </span>
                </div>
                <p className="text-[11px] font-sans text-muted-foreground tracking-wide mt-0.5 truncate">
                  {dossier.title} • {DEPARTMENT_NAMES[dossier.department] || dossier.department}
                </p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              {/* Target Model Route Badge */}
              <div className="hidden sm:flex items-center gap-1.5 bg-muted border border-border px-2.5 py-1 rounded-full text-[9px] font-mono text-foreground/80">
                <Cpu size={11} className="text-primary" />
                <span>{dossier.target_model}</span>
              </div>

              <button
                onClick={onClose}
                className="w-8 h-8 rounded-full border border-border flex items-center justify-center text-muted-foreground hover:text-foreground hover:bg-muted/50 transition-colors cursor-pointer"
                title="Close Dossier"
              >
                <X size={16} />
              </button>
            </div>
          </div>

          {/* Tab Navigation */}
          <div className="px-6 pt-3 border-b border-border flex gap-2 shrink-0 bg-muted/30">
            <button
              onClick={() => setActiveTab("overview")}
              className={`px-3 py-2 text-[10px] font-mono uppercase tracking-wider flex items-center gap-1.5 border-b-2 transition-all cursor-pointer ${
                activeTab === "overview"
                  ? "border-primary text-primary font-medium"
                  : "border-transparent text-muted-foreground hover:text-foreground"
              }`}
            >
              <BookOpen size={12} />
              Overview & Bio
            </button>
            <button
              onClick={() => setActiveTab("skills")}
              className={`px-3 py-2 text-[10px] font-mono uppercase tracking-wider flex items-center gap-1.5 border-b-2 transition-all cursor-pointer ${
                activeTab === "skills"
                  ? "border-primary text-primary font-medium"
                  : "border-transparent text-muted-foreground hover:text-foreground"
              }`}
            >
              <Sparkles size={12} />
              Skills & Capabilities ({dossier.primary_skills.length})
            </button>
            <button
              onClick={() => setActiveTab("system_prompt")}
              className={`px-3 py-2 text-[10px] font-mono uppercase tracking-wider flex items-center gap-1.5 border-b-2 transition-all cursor-pointer ${
                activeTab === "system_prompt"
                  ? "border-primary text-primary font-medium"
                  : "border-transparent text-muted-foreground hover:text-foreground"
              }`}
            >
              <Terminal size={12} />
              System Directives
            </button>
            <button
              onClick={() => setActiveTab("tools")}
              className={`px-3 py-2 text-[10px] font-mono uppercase tracking-wider flex items-center gap-1.5 border-b-2 transition-all cursor-pointer ${
                activeTab === "tools"
                  ? "border-primary text-primary font-medium"
                  : "border-transparent text-muted-foreground hover:text-foreground"
              }`}
            >
              <Wrench size={12} />
              Bound Tools ({dossier.bound_tools.length})
            </button>
          </div>

          {/* Modal Body */}
          <div className="p-6 overflow-y-auto space-y-6">
            {/* OVERVIEW TAB */}
            {activeTab === "overview" && (
              <div className="space-y-6">
                {/* Executive Bio */}
                <div className="bg-muted/20 border border-border rounded-xl p-4">
                  <h4 className="text-[9px] font-mono tracking-widest text-primary uppercase mb-2 flex items-center gap-1.5 font-semibold">
                    <ShieldCheck size={12} />
                    Executive Identity & Scoping
                  </h4>
                  <p className="text-xs font-sans text-foreground/80 leading-relaxed font-light">
                    {dossier.bio}
                  </p>
                </div>

                {/* Knowledge Domains Grid */}
                <div>
                  <h4 className="text-[9px] font-mono tracking-widest text-muted-foreground uppercase mb-3 flex items-center gap-1.5">
                    <Layers size={11} />
                    Knowledge Domains & Expertise
                  </h4>
                  <div className="flex flex-wrap gap-2">
                    {dossier.knowledge_domains.map((domain, i) => (
                      <span
                        key={i}
                        className="text-[9.5px] font-mono bg-muted border border-border px-2.5 py-1 rounded-md text-foreground/80"
                      >
                        {domain}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Authority & Governance Scoping */}
                <div className="border border-border rounded-xl p-4 bg-muted/10 flex flex-col gap-2">
                  <div className="flex justify-between items-center">
                    <span className="text-[9px] font-mono text-muted-foreground uppercase">
                      Authority Boundary
                    </span>
                    <span className={`text-[8.5px] font-mono uppercase px-2 py-0.5 rounded border ${authorityBadgeStyles}`}>
                      Class {dossier.authority_class}
                    </span>
                  </div>
                  <p className="text-[10.5px] font-sans text-muted-foreground font-light">
                    {dossier.authority_class === "PROPOSE"
                      ? "Authorized to synthesize, formulate, and propose creative artifacts, shot lists, briefs, and copy for downstream review."
                      : dossier.authority_class === "CRITIQUE"
                      ? "Mandated to inspect artifacts for aesthetic flaws, style drift, and hallucinations with prescriptive remediation."
                      : dossier.authority_class === "REVIEW"
                      ? "Independent gatekeeper holding final scoring and approval authority before production asset release."
                      : "Observational authority: monitors telemetry, cultural signals, and data without mutating creative state."}
                  </p>
                </div>
              </div>
            )}

            {/* SKILLS TAB */}
            {activeTab === "skills" && (
              <div className="space-y-6">
                {/* Primary Skills List */}
                <div>
                  <h4 className="text-[9px] font-mono tracking-widest text-primary uppercase mb-3 flex items-center gap-1.5 font-semibold">
                    <Sparkles size={12} />
                    Primary Mastery Skills
                  </h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {dossier.primary_skills.map((skill) => (
                      <div
                        key={skill.skill_id}
                        className="bg-card border border-border rounded-xl p-3.5 flex flex-col gap-2 hover:border-primary/40 transition-all shadow-sm"
                      >
                        <div className="flex justify-between items-start gap-2">
                          <span className="text-xs font-serif text-foreground font-medium">
                            {skill.name}
                          </span>
                          <span className="text-[7.5px] font-mono tracking-wider uppercase px-1.5 py-0.5 rounded bg-primary/10 border border-primary/20 text-primary">
                            {skill.proficiency_level}
                          </span>
                        </div>
                        <p className="text-[10.5px] font-sans text-muted-foreground font-light leading-relaxed">
                          {skill.description}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Capabilities Badges */}
                <div>
                  <h4 className="text-[9px] font-mono tracking-widest text-muted-foreground uppercase mb-3">
                    Registered Workflow Capabilities
                  </h4>
                  <div className="flex flex-wrap gap-2">
                    {dossier.capabilities.map((cap, i) => (
                      <span
                        key={i}
                        className="text-[9px] font-mono bg-muted border border-border px-2 py-1 rounded text-foreground/80"
                      >
                        ⚡ {cap}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* SYSTEM PROMPT TAB */}
            {activeTab === "system_prompt" && (
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-[9px] font-mono tracking-widest text-primary uppercase flex items-center gap-1.5 font-semibold">
                    <Terminal size={12} />
                    Governed Reasoning Directive
                  </span>
                  <button
                    onClick={handleCopyPrompt}
                    className="flex items-center gap-1.5 text-[9px] font-mono text-muted-foreground hover:text-foreground transition-colors cursor-pointer bg-muted px-2 py-1 rounded border border-border"
                  >
                    {copiedPrompt ? (
                      <>
                        <CheckCircle2 size={11} className="text-emerald-500" />
                        <span className="text-emerald-500">Copied</span>
                      </>
                    ) : (
                      <>
                        <Copy size={11} />
                        <span>Copy Directive</span>
                      </>
                    )}
                  </button>
                </div>

                <div className="bg-muted/40 border border-border rounded-xl p-4 font-mono text-[11px] text-emerald-600 dark:text-emerald-400 leading-relaxed overflow-x-auto whitespace-pre-wrap select-text">
                  {dossier.system_instruction}
                </div>
              </div>
            )}

            {/* BOUND TOOLS TAB */}
            {activeTab === "tools" && (
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-[9px] font-mono tracking-widest text-primary uppercase flex items-center gap-1.5 font-semibold">
                    <Wrench size={12} />
                    Active Tool Bindings
                  </span>
                  <span className="text-[8.5px] font-mono text-muted-foreground">
                    Phase 21 Model Function Calling
                  </span>
                </div>

                <div className="space-y-3">
                  {dossier.bound_tools.map((tool) => (
                    <div
                      key={tool.tool_id}
                      className="bg-card border border-border rounded-xl p-4 flex flex-col gap-2.5 hover:border-primary/40 transition-all shadow-sm"
                    >
                      <div className="flex justify-between items-baseline">
                        <span className="text-xs font-mono text-foreground font-medium">
                          {tool.tool_name}
                        </span>
                        <span className="text-[8px] font-mono text-muted-foreground">
                          {tool.tool_id}
                        </span>
                      </div>
                      <p className="text-[11px] font-sans text-muted-foreground font-light leading-relaxed">
                        {tool.description}
                      </p>
                      <div className="flex items-center gap-2 pt-1 border-t border-border">
                        <span className="text-[8px] font-mono text-muted-foreground uppercase">
                          Schema Keys:
                        </span>
                        <div className="flex flex-wrap gap-1.5">
                          {tool.input_schema_keys.map((k, i) => (
                            <span
                              key={i}
                              className="text-[8px] font-mono bg-muted border border-border px-1.5 py-0.5 rounded text-foreground/70"
                            >
                              {k}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Modal Footer */}
          <div className="px-6 py-3 border-t border-border bg-muted/20 flex justify-between items-center text-[9px] font-mono text-muted-foreground shrink-0">
            <span>Identity Version {dossier.version}</span>
            <button
              onClick={onClose}
              className="px-4 py-1.5 rounded-lg bg-muted hover:bg-muted/80 text-foreground transition-colors cursor-pointer border border-border"
            >
              Close
            </button>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
};
