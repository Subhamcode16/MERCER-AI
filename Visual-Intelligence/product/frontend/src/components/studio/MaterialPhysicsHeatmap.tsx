"use client";

import React, { useState } from "react";
import { Activity, Flame, ShieldAlert, Cpu, RefreshCw } from "lucide-react";

export const MaterialPhysicsHeatmap: React.FC = () => {
  const [activeLayer, setActiveLayer] = useState<"tension" | "shear" | "gravity">("tension");
  const [drapeCompliance, setDrapeCompliance] = useState<number>(98.4);

  return (
    <div className="absolute inset-0 pointer-events-none flex flex-col justify-between p-4 z-20">
      {/* Top Controls Bar */}
      <div className="pointer-events-auto flex items-center justify-between bg-black/85 backdrop-blur-md border border-cyan-500/20 rounded-lg px-4 py-2.5 text-xs text-white">
        <div className="flex items-center gap-2">
          <Activity className="w-4 h-4 text-cyan-400 animate-pulse" />
          <span className="font-mono font-semibold tracking-wider text-cyan-200">TACTILE MATERIAL PHYSICS SIMULATOR</span>
        </div>

        <div className="flex items-center gap-1 bg-neutral-900 border border-white/5 rounded p-0.5">
          <button
            onClick={() => setActiveLayer("tension")}
            className={`px-2.5 py-1 rounded transition-colors ${
              activeLayer === "tension" ? "bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 font-medium" : "text-neutral-400 hover:text-white"
            }`}
          >
            Stress-Strain Tension
          </button>
          <button
            onClick={() => setActiveLayer("shear")}
            className={`px-2.5 py-1 rounded transition-colors ${
              activeLayer === "shear" ? "bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 font-medium" : "text-neutral-400 hover:text-white"
            }`}
          >
            Shear Stiffness
          </button>
          <button
            onClick={() => setActiveLayer("gravity")}
            className={`px-2.5 py-1 rounded transition-colors ${
              activeLayer === "gravity" ? "bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 font-medium" : "text-neutral-400 hover:text-white"
            }`}
          >
            Gravity Vector Drape
          </button>
        </div>

        <div className="flex items-center gap-2 font-mono text-[11px] text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-2 py-0.5 rounded">
          <span>Physical Fidelity: <strong>{drapeCompliance}%</strong></span>
        </div>
      </div>

      {/* Heatmap Colormap Visualization Gradient Overlay */}
      <div className="flex-1 flex items-center justify-center my-4 relative">
        <div className="w-[320px] h-[400px] rounded-xl border border-cyan-500/30 bg-gradient-to-b from-cyan-500/10 via-amber-500/15 to-red-500/10 relative overflow-hidden flex items-center justify-center">
          {/* Wireframe Mesh Lines */}
          <div className="absolute inset-0 bg-[radial-gradient(#00f2fe_1px,transparent_1px)] [background-size:16px_16px] opacity-30" />
          
          <div className="text-center font-mono text-xs text-neutral-300 z-10 bg-black/60 backdrop-blur-sm p-3 rounded-lg border border-white/10">
            <Flame className="w-5 h-5 text-amber-400 mx-auto mb-1" />
            <div className="text-white font-semibold uppercase tracking-wider">
              {activeLayer === "tension" ? "Tension Heatmap Active" : activeLayer === "shear" ? "Shear Resistance Map" : "Gravity Fall Velocity"}
            </div>
            <div className="text-[10px] text-neutral-400 mt-0.5">Micro-Fiber Silk Satin • 18 Momme</div>
          </div>
        </div>
      </div>

      {/* Bottom Physics Parameters HUD */}
      <div className="pointer-events-auto bg-black/85 backdrop-blur-md border border-white/10 rounded-lg p-3 text-xs text-white grid grid-cols-4 gap-4">
        <div>
          <div className="text-neutral-400 text-[10px] uppercase font-mono">Bending Rigidity</div>
          <div className="font-mono text-cyan-400 font-semibold mt-0.5">2.41 μN·m</div>
        </div>
        <div>
          <div className="text-neutral-400 text-[10px] uppercase font-mono">Shear Modulus (G)</div>
          <div className="font-mono text-emerald-400 font-semibold mt-0.5">18.5 N/m</div>
        </div>
        <div>
          <div className="text-neutral-400 text-[10px] uppercase font-mono">Friction Coeff (μ)</div>
          <div className="font-mono text-amber-400 font-semibold mt-0.5">0.18 (Low Slip)</div>
        </div>
        <div>
          <div className="text-neutral-400 text-[10px] uppercase font-mono">Collision Penetrations</div>
          <div className="font-mono text-emerald-400 font-semibold mt-0.5">0 (Valid Boundary)</div>
        </div>
      </div>
    </div>
  );
};
