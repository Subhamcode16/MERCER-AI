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
      <div className="p-6 rounded-2xl bg-card border border-border space-y-4 shadow-sm">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <Cpu className="w-5 h-5 text-primary" />
              <h2 className="text-lg font-serif text-foreground font-medium">Governed Skills & Automated Routines</h2>
            </div>
            <p className="text-xs text-muted-foreground font-light">
              Reusable computational capabilities and scheduled organizational cadences operated under strict human boundaries.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setActiveSection('skills')}
              className={`px-4 py-2 rounded-xl text-xs font-mono transition-all border shadow-xs ${
                activeSection === 'skills'
                  ? "bg-primary text-primary-foreground font-bold border-primary"
                  : "bg-muted/40 text-muted-foreground border-border hover:text-foreground hover:bg-muted"
              }`}
            >
              Governed Skills ({skills.length})
            </button>
            <button
              onClick={() => setActiveSection('routines')}
              className={`px-4 py-2 rounded-xl text-xs font-mono transition-all border shadow-xs ${
                activeSection === 'routines'
                  ? "bg-primary text-primary-foreground font-bold border-primary"
                  : "bg-muted/40 text-muted-foreground border-border hover:text-foreground hover:bg-muted"
              }`}
            >
              Automated Routines ({routines.length})
            </button>
          </div>
        </div>

        <div className="p-3.5 rounded-xl bg-muted/30 border border-border flex items-center justify-between text-xs text-muted-foreground">
          <div className="flex items-center gap-2">
            <Lock className="w-4 h-4 text-amber-600 dark:text-amber-400" />
            <span>Invariants: <strong className="text-foreground">Skill &ne; Authority</strong> &bull; <strong className="text-foreground">Routine &ne; Execution Permission</strong></span>
          </div>
          <span className="text-[10px] font-mono text-muted-foreground">Zero Self-Authorization</span>
        </div>
      </div>

      {/* SECTION 1: Skills Catalog */}
      {activeSection === 'skills' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {skills.map((skill) => (
            <div
              key={skill.id}
              className="p-5 rounded-2xl bg-card border border-border space-y-4 hover:border-primary/40 transition-all flex flex-col justify-between shadow-sm"
            >
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-mono text-purple-700 dark:text-purple-300 bg-purple-500/10 border border-purple-500/20 px-2 py-0.5 rounded font-medium">
                    {skill.category}
                  </span>
                  <span className="text-[10px] font-mono text-muted-foreground">{skill.version}</span>
                </div>
                <h3 className="text-sm font-medium text-foreground">{skill.name}</h3>
                <p className="text-xs text-muted-foreground font-light leading-relaxed">{skill.governanceScope}</p>
              </div>

              <div className="pt-3 border-t border-border flex items-center justify-between text-[11px] font-mono text-muted-foreground">
                <span>Owner: <strong className="text-foreground/80">{skill.owner}</strong></span>
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
              className="p-5 rounded-2xl bg-card border border-border flex flex-col md:flex-row md:items-center justify-between gap-4 hover:border-primary/40 transition-all shadow-sm"
            >
              <div className="space-y-1.5 max-w-xl">
                <div className="flex items-center gap-2.5">
                  <h3 className="text-sm font-medium text-foreground">{routine.name}</h3>
                  <span className="px-2 py-0.5 rounded text-[9px] font-mono bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 border border-emerald-500/20 font-medium">
                    {routine.status.toUpperCase()}
                  </span>
                </div>
                <p className="text-xs text-muted-foreground font-light">{routine.purpose}</p>
                <div className="flex items-center gap-3 text-[10px] font-mono text-muted-foreground pt-0.5">
                  <span>Trigger: {routine.triggerCadence}</span>
                  <span>•</span>
                  <span>Last Run: {routine.lastRun}</span>
                  <span>•</span>
                  <span>Owner: {routine.owner}</span>
                </div>
              </div>

              <div className="flex items-center gap-2">
                <span className="text-[10px] font-mono text-muted-foreground px-3 py-1.5 rounded-xl bg-muted border border-border">
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
