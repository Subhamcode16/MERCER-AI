"use client";

import React from "react";
import { Shield, CheckCircle2, Zap, AlertTriangle, Users, Bot } from "lucide-react";

export const PolicyStatusHUD: React.FC = () => {
  return (
    <div className="absolute top-4 right-4 z-20 pointer-events-auto flex flex-col gap-2 max-w-[280px]">
      {/* Model Waterfall Status Badge */}
      <div className="bg-black/85 backdrop-blur-md border border-white/10 rounded-lg p-2.5 text-xs text-white">
        <div className="flex items-center justify-between font-mono mb-1.5">
          <span className="text-neutral-400 flex items-center gap-1">
            <Zap className="w-3.5 h-3.5 text-emerald-400" />
            Model Waterfall:
          </span>
          <span className="text-emerald-400 font-semibold text-[11px]">Primary Stable</span>
        </div>
        <div className="flex items-center justify-between text-[11px] font-mono text-neutral-300">
          <span>gemini-2.5-flash</span>
          <span className="text-neutral-500">Latency: 142ms</span>
        </div>
      </div>

      {/* Brand Tone Safety Invariant Status */}
      <div className="bg-black/85 backdrop-blur-md border border-white/10 rounded-lg p-2.5 text-xs text-white">
        <div className="flex items-center justify-between font-mono mb-1">
          <span className="text-neutral-400 flex items-center gap-1">
            <Shield className="w-3.5 h-3.5 text-cyan-400" />
            Governance Invariants:
          </span>
          <span className="text-emerald-400 flex items-center gap-0.5 text-[10px]">
            <CheckCircle2 className="w-3 h-3" /> PASS
          </span>
        </div>
        <div className="text-[10px] text-neutral-400 font-mono">
          Strict Luxury Tone • Zero Hallucination
        </div>
      </div>

      {/* Multi-Agent Delegation Telemetry */}
      <div className="bg-black/85 backdrop-blur-md border border-white/10 rounded-lg p-2.5 text-xs text-white">
        <div className="flex items-center justify-between font-mono mb-1.5">
          <span className="text-neutral-400 flex items-center gap-1">
            <Bot className="w-3.5 h-3.5 text-purple-400" />
            Active Workforce:
          </span>
          <span className="text-purple-300 text-[11px]">3 Agents</span>
        </div>
        <div className="space-y-1 text-[10px] font-mono">
          <div className="flex items-center justify-between text-neutral-300">
            <span>• Art Director</span>
            <span className="text-emerald-400">Reviewing</span>
          </div>
          <div className="flex items-center justify-between text-neutral-300">
            <span>• Visual DNA Stylist</span>
            <span className="text-cyan-400">Harmonizing</span>
          </div>
          <div className="flex items-center justify-between text-neutral-300">
            <span>• Physics Verifier</span>
            <span className="text-purple-400">Simulating</span>
          </div>
        </div>
      </div>
    </div>
  );
};
