"use client";

import React, { useState } from "react";
import { GitCompare, ShieldCheck, History, ArrowRight, CheckCircle2 } from "lucide-react";

export const AssetLineageDiff: React.FC = () => {
  const [diffPosition, setDiffPosition] = useState<number>(50);

  return (
    <div className="absolute inset-0 pointer-events-none flex flex-col justify-between p-4 z-20">
      {/* Top Header */}
      <div className="pointer-events-auto flex items-center justify-between bg-black/85 backdrop-blur-md border border-amber-500/20 rounded-lg px-4 py-2.5 text-xs text-white">
        <div className="flex items-center gap-2">
          <GitCompare className="w-4 h-4 text-amber-400" />
          <span className="font-mono font-semibold tracking-wider text-amber-200">CRYPTOGRAPHIC ASSET LINEAGE & VERSION DIFF</span>
        </div>

        <div className="flex items-center gap-2 font-mono text-[11px] text-amber-300 bg-amber-500/10 border border-amber-500/30 px-2.5 py-0.5 rounded">
          <ShieldCheck className="w-3.5 h-3.5 text-amber-400" />
          <span>SHA-256 Verified: 0x7f9a...c3b1</span>
        </div>
      </div>

      {/* Center Visual Comparison Split Indicator */}
      <div className="flex-1 flex items-center justify-center my-2 relative">
        <div className="w-[360px] h-[400px] rounded-xl border border-white/20 relative overflow-hidden bg-neutral-950 flex">
          {/* Version A Label (Left) */}
          <div className="w-1/2 h-full border-r border-amber-400/50 bg-neutral-900/50 p-3 flex flex-col justify-between">
            <div className="font-mono text-[10px] text-neutral-400 uppercase">Version v1.2 (Prompt Iteration)</div>
            <div className="text-center font-mono text-xs text-amber-400">Warm Tone Baseline</div>
          </div>
          {/* Version B Label (Right) */}
          <div className="w-1/2 h-full bg-neutral-900/20 p-3 flex flex-col justify-between">
            <div className="font-mono text-[10px] text-neutral-400 uppercase text-right">Version v2.0 (Kinetic Cut)</div>
            <div className="text-center font-mono text-xs text-emerald-400">Asymmetric Dynamic Crop</div>
          </div>

          {/* Interactive Split Bar */}
          <div
            className="absolute top-0 bottom-0 w-0.5 bg-amber-400 shadow-[0_0_10px_#f59e0b] pointer-events-auto cursor-ew-resize flex items-center justify-center"
            style={{ left: `${diffPosition}%` }}
          >
            <div className="w-5 h-5 rounded-full bg-black border border-amber-400 flex items-center justify-center text-[9px] font-mono text-amber-400">
              <>⇄</>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Lineage Breadcrumb */}
      <div className="pointer-events-auto bg-black/85 backdrop-blur-md border border-white/10 rounded-lg p-3 text-xs text-white flex items-center justify-between">
        <div className="flex items-center gap-2 font-mono text-[11px] text-neutral-300">
          <History className="w-3.5 h-3.5 text-neutral-400" />
          <span>GEN_BASE</span>
          <ArrowRight className="w-3 h-3 text-neutral-500" />
          <span>PROMPT_SYNTH_v1.2</span>
          <ArrowRight className="w-3 h-3 text-neutral-500" />
          <span className="text-amber-400 font-semibold">KINETIC_CROP_v2.0 (Current)</span>
        </div>
        <div className="flex items-center gap-1.5 font-mono text-[11px] text-emerald-400">
          <CheckCircle2 className="w-3.5 h-3.5" />
          <span>Ledger Block #104 Immutable</span>
        </div>
      </div>
    </div>
  );
};
