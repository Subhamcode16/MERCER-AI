"use client";

import React, { useState } from "react";
import { 
  Cpu, 
  Clock, 
  ShieldCheck, 
  CheckCircle2, 
  Layers, 
  Play, 
  Lock,
  Sparkles,
  Info
} from "lucide-react";
import type { TeamRoutine, TeamSkill } from "@/lib/teamFixtures";

interface SkillsRoutinesViewProps {
  skills: TeamSkill[];
  routines: TeamRoutine[];
}

export function SkillsRoutinesView({ skills, routines }: SkillsRoutinesViewProps) {
  const [activeSection, setActiveSection] = useState<'skills' | 'routines'>('skills');

  return (
    <div className="space-y-8 animate-in fade-in duration-200">
      
      {/* Overview & Governance Alert */}
      <div className="p-6 rounded-2xl bg-[#111113]/80 border border-white/10 space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <Cpu className="w-5 h-5 text-[#E1D4C0]" />
              <h2 className="text-lg font-serif text-white font-medium">Governed Skills & Automated Routines</h2>
            </div>
            <p className="text-xs text-white/50 font-light">
              Reusable computational capabilities and scheduled organizational cadences operated under strict human boundaries.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setActiveSection('skills')}
              className={`px-4 py-2 rounded-xl text-xs font-mono transition-all border ${
                activeSection === 'skills'
                  ? "bg-[#E1D4C0] text-[#0A0A0A] font-bold border-[#E1D4C0]"
                  : "bg-white/[0.02] text-white/50 border-white/5 hover:text-white"
              }`}
            >
              Governed Skills ({skills.length})
            </button>
            <button
              onClick={() => setActiveSection('routines')}
              className={`px-4 py-2 rounded-xl text-xs font-mono transition-all border ${
                activeSection === 'routines'
                  ? "bg-[#E1D4C0] text-[#0A0A0A] font-bold border-[#E1D4C0]"
                  : "bg-white/[0.02] text-white/50 border-white/5 hover:text-white"
              }`}
            >
              Automated Routines ({routines.length})
            </button>
          </div>
        </div>

        <div className="p-3.5 rounded-xl bg-black/40 border border-white/5 flex items-center justify-between text-xs text-white/60">
          <div className="flex items-center gap-2">
            <Lock className="w-4 h-4 text-amber-400" />
            <span>Invariants: <strong className="text-white">Skill &ne; Authority</strong> &bull; <strong className="text-white">Routine &ne; Execution Permission</strong></span>
          </div>
          <span className="text-[10px] font-mono text-white/40">Zero Self-Authorization</span>
        </div>
      </div>

      {/* SECTION 1: Skills Catalog */}
      {activeSection === 'skills' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {skills.map((skill) => (
            <div
              key={skill.id}
              className="p-5 rounded-2xl bg-[#111113]/90 border border-white/10 space-y-4 hover:border-white/20 transition-all flex flex-col justify-between"
            >
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-mono text-purple-300 bg-purple-500/10 border border-purple-500/20 px-2 py-0.5 rounded">
                    {skill.category}
                  </span>
                  <span className="text-[10px] font-mono text-white/40">{skill.version}</span>
                </div>
                <h3 className="text-sm font-medium text-white">{skill.name}</h3>
                <p className="text-xs text-white/60 font-light leading-relaxed">{skill.governanceScope}</p>
              </div>

              <div className="pt-3 border-t border-white/5 flex items-center justify-between text-[11px] font-mono text-white/40">
                <span>Owner: <strong className="text-white/80">{skill.owner}</strong></span>
                <span>{skill.usageCount} Operations Executed</span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* SECTION 2: Automated Routines */}
      {activeSection === 'routines' && (
        <div className="space-y-4">
          {routines.map((routine) => (
            <div
              key={routine.id}
              className="p-5 rounded-2xl bg-[#111113]/90 border border-white/10 flex flex-col md:flex-row md:items-center justify-between gap-4 hover:border-white/20 transition-all"
            >
              <div className="space-y-1.5 max-w-xl">
                <div className="flex items-center gap-2.5">
                  <h3 className="text-sm font-medium text-white">{routine.name}</h3>
                  <span className="px-2 py-0.5 rounded text-[9px] font-mono bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                    {routine.status.toUpperCase()}
                  </span>
                </div>
                <p className="text-xs text-white/60 font-light">{routine.purpose}</p>
                <div className="flex items-center gap-3 text-[10px] font-mono text-white/40 pt-0.5">
                  <span>Trigger: {routine.triggerCadence}</span>
                  <span>•</span>
                  <span>Last Run: {routine.lastRun}</span>
                  <span>•</span>
                  <span>Owner: {routine.owner}</span>
                </div>
              </div>

              <div className="flex items-center gap-2">
                <span className="text-[10px] font-mono text-white/40 px-3 py-1.5 rounded-xl bg-white/[0.02] border border-white/5">
                  Auto-Governed
                </span>
              </div>
            </div>
          ))}
        </div>
      )}

    </div>
  );
}
