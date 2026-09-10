"use client";

import React, { useState } from "react";
import { Layers, Maximize, Smartphone, Monitor, Square, Palette, Sliders } from "lucide-react";

export type AspectRatioMode = "1:1" | "9:16" | "16:9";

export const VisualDNAOverlay: React.FC = () => {
  const [aspectRatio, setAspectRatio] = useState<AspectRatioMode>("9:16");
  const [showSafeZones, setShowSafeZones] = useState<boolean>(true);
  const [showColorMap, setShowColorMap] = useState<boolean>(true);

  return (
    <div className="absolute inset-0 pointer-events-none flex flex-col justify-between p-4 z-20">
      {/* Top Controls Bar */}
      <div className="pointer-events-auto flex items-center justify-between bg-black/80 backdrop-blur-md border border-white/10 rounded-lg px-4 py-2 text-xs text-white">
        <div className="flex items-center gap-2">
          <Layers className="w-4 h-4 text-emerald-400" />
          <span className="font-mono font-semibold tracking-wider text-neutral-300">VISUAL DNA SAFE-ZONE HUD</span>
        </div>

        {/* Aspect Ratio Selector */}
        <div className="flex items-center gap-1 bg-neutral-900 border border-white/5 rounded p-0.5">
          <button
            onClick={() => setAspectRatio("9:16")}
            className={`flex items-center gap-1 px-2 py-1 rounded transition-colors ${
              aspectRatio === "9:16" ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30" : "text-neutral-400 hover:text-white"
            }`}
          >
            <Smartphone className="w-3.5 h-3.5" />
            <span>9:16 (Reel/TikTok)</span>
          </button>
          <button
            onClick={() => setAspectRatio("1:1")}
            className={`flex items-center gap-1 px-2 py-1 rounded transition-colors ${
              aspectRatio === "1:1" ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30" : "text-neutral-400 hover:text-white"
            }`}
          >
            <Square className="w-3.5 h-3.5" />
            <span>1:1 (Meta Feed)</span>
          </button>
          <button
            onClick={() => setAspectRatio("16:9")}
            className={`flex items-center gap-1 px-2 py-1 rounded transition-colors ${
              aspectRatio === "16:9" ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30" : "text-neutral-400 hover:text-white"
            }`}
          >
            <Monitor className="w-3.5 h-3.5" />
            <span>16:9 (Landscape)</span>
          </button>
        </div>

        {/* Toggles */}
        <div className="flex items-center gap-3">
          <label className="flex items-center gap-1.5 cursor-pointer text-neutral-400 hover:text-white">
            <input
              type="checkbox"
              checked={showSafeZones}
              onChange={(e) => setShowSafeZones(e.target.checked)}
              className="rounded bg-neutral-800 border-white/10 text-emerald-500 focus:ring-0"
            />
            <span>Safe Margins</span>
          </label>
          <label className="flex items-center gap-1.5 cursor-pointer text-neutral-400 hover:text-white">
            <input
              type="checkbox"
              checked={showColorMap}
              onChange={(e) => setShowColorMap(e.target.checked)}
              className="rounded bg-neutral-800 border-white/10 text-emerald-500 focus:ring-0"
            />
            <span>Palette Entropy</span>
          </label>
        </div>
      </div>

      {/* Center Safe-Zone Overlay Frame */}
      <div className="flex-1 flex items-center justify-center my-2">
        <div
          className={`relative border-2 border-dashed transition-all duration-300 ${
            aspectRatio === "9:16"
              ? "w-[240px] h-[426px] border-emerald-500/40"
              : aspectRatio === "1:1"
              ? "w-[340px] h-[340px] border-cyan-500/40"
              : "w-[480px] h-[270px] border-amber-500/40"
          }`}
        >
          {showSafeZones && (
            <>
              {/* Top Header Safe Zone */}
              <div className="absolute top-0 inset-x-0 h-10 border-b border-red-500/30 bg-red-500/5 flex items-center justify-center">
                <span className="text-[10px] font-mono text-red-400/80">AVOID UI OVERLAY (TOP SAFE ZONE)</span>
              </div>
              {/* Bottom CTA Safe Zone */}
              <div className="absolute bottom-0 inset-x-0 h-16 border-t border-red-500/30 bg-red-500/5 flex items-center justify-center">
                <span className="text-[10px] font-mono text-red-400/80">RESERVED FOR CAPTION & CTA</span>
              </div>
              {/* Center Focus Crosshair */}
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="w-8 h-8 border border-white/20 rounded-full flex items-center justify-center">
                  <div className="w-1.5 h-1.5 bg-emerald-400 rounded-full animate-ping" />
                </div>
              </div>
            </>
          )}
        </div>
      </div>

      {/* Bottom Visual DNA Metrics Bar */}
      {showColorMap && (
        <div className="pointer-events-auto bg-black/80 backdrop-blur-md border border-white/10 rounded-lg p-3 text-xs text-white flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-1.5">
              <Palette className="w-3.5 h-3.5 text-indigo-400" />
              <span className="text-neutral-400">Palette Tokens:</span>
              <div className="flex items-center gap-1">
                <span className="w-3 h-3 rounded-full bg-[#1A1A1A] border border-white/20" title="Obsidian Black (45%)" />
                <span className="w-3 h-3 rounded-full bg-[#C29B38] border border-white/20" title="Champagne Gold (30%)" />
                <span className="w-3 h-3 rounded-full bg-[#EAEAEA] border border-white/20" title="Pearl White (25%)" />
              </div>
            </div>
            <div className="h-3 w-px bg-white/10" />
            <div className="flex items-center gap-1.5 font-mono">
              <span className="text-neutral-400">Entropy Score:</span>
              <span className="text-emerald-400 font-semibold">0.84 (Optimal Harmony)</span>
            </div>
          </div>
          <div className="flex items-center gap-2 font-mono text-[11px] text-neutral-400">
            <span>Visual Density: <strong className="text-white">38%</strong></span>
            <span>•</span>
            <span>Typographic Weight: <strong className="text-white">Minimal Serif</strong></span>
          </div>
        </div>
      )}
    </div>
  );
};
