"use client";

import React, { useState } from "react";
import { 
  Palette, 
  Sparkles, 
  CheckCircle2, 
  ArrowRight,
  Sliders,
  Maximize2,
  RefreshCw,
  Sun,
  ShieldCheck,
  ChevronRight,
  Send,
  Layers,
  Camera,
  Activity,
  X
} from "lucide-react";
import type { CampaignStudioModel, VisualStudy } from "@/lib/campaignStudioFixtures";

interface VisualsTabProps {
  campaign: CampaignStudioModel;
  onNavigateTab: (tab: any) => void;
}

export function VisualsTab({ campaign, onNavigateTab }: VisualsTabProps) {
  const [selectedShot, setSelectedShot] = useState<string>("HERO");
  const [activeStudy, setActiveStudy] = useState<VisualStudy>(campaign.visualStudies[0]);
  
  // Intuitive Creative Sliders
  const [lightingVal, setLightingVal] = useState(65); // 0: Cinematic -> 100: Editorial
  const [compositionVal, setCompositionVal] = useState(30); // 0: Minimal -> 100: Dramatic
  const [materialVal, setMaterialVal] = useState(80); // 0: Matte -> 100: Reflective
  const [atmosphereVal, setAtmosphereVal] = useState(50); // 0: Pure Studio -> 100: Atmospheric

  const [nlCommand, setNlCommand] = useState("");
  const [isApplyingTweak, setIsApplyingTweak] = useState(false);
  const [showAdvancedControls, setShowAdvancedControls] = useState(false);
  const [feedbackNotice, setFeedbackNotice] = useState<string | null>(null);

  const shots = [
    { id: "HERO", label: "HERO", desc: "Main Campaign Anchor (16:9 / 4:5)" },
    { id: "DETAIL", label: "DETAIL", desc: "Brocade & Weave Close-Up (1:1)" },
    { id: "SOCIAL", label: "SOCIAL", desc: "Vertical Motion Story (9:16)" },
    { id: "EDITORIAL", label: "EDITORIAL", desc: "Atmospheric Print Spread (4:5)" }
  ];

  const handleApplyNlCommand = (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!nlCommand.trim()) return;

    setIsApplyingTweak(true);
    setTimeout(() => {
      setIsApplyingTweak(false);
      setFeedbackNotice(`VYREN adjusted lighting, lens angle, and drape tension to: "${nlCommand}"`);
      setNlCommand("");
      setTimeout(() => setFeedbackNotice(null), 4500);
    }, 1200);
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-200 pb-20 max-w-7xl mx-auto">
      
      {/* 1. Shot Selector Tabs */}
      <div className="flex items-center justify-between border-b border-white/5 pb-4">
        <div className="flex items-center gap-2">
          {shots.map((shot) => (
            <button
              key={shot.id}
              onClick={() => setSelectedShot(shot.id)}
              className={`px-4 py-2 rounded-xl text-xs font-medium transition-all ${
                selectedShot === shot.id
                  ? "bg-[#E1D4C0] text-[#0A0A0A] font-semibold shadow-md"
                  : "bg-white/[0.03] text-white/50 hover:text-white hover:bg-white/[0.07]"
              }`}
            >
              <span>{shot.label}</span>
            </button>
          ))}
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => onNavigateTab('review')}
            className="px-4 py-2 rounded-xl bg-white/[0.06] hover:bg-white/10 text-white text-xs font-medium transition-colors flex items-center gap-1.5"
          >
            <span>Proceed to Review</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* Feedback Toast */}
      {feedbackNotice && (
        <div className="p-3.5 rounded-xl bg-[#141416] border border-[#E1D4C0]/40 text-[#E1D4C0] text-xs flex items-center gap-2.5 animate-in slide-in-from-top-2">
          <Sparkles className="w-4 h-4 text-[#E1D4C0] shrink-0 animate-pulse" />
          <span>{feedbackNotice}</span>
        </div>
      )}

      {/* 2. Dominant Visual Studio Canvas */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        
        {/* Left: Large Visual Canvas (7 Cols) */}
        <div className="lg:col-span-8 space-y-4">
          <div className="relative aspect-[16/10] rounded-3xl bg-gradient-to-br from-[#18181D] via-[#0E0E10] to-black border border-white/10 overflow-hidden flex flex-col items-center justify-center p-8 group shadow-2xl">
            
            {/* Ambient Shader Glow */}
            <div className="absolute inset-0 bg-[radial-gradient(#E1D4C0_1px,transparent_1px)] [background-size:28px_28px] opacity-10 pointer-events-none" />
            <div 
              className="absolute -top-20 -right-20 w-80 h-80 rounded-full blur-3xl pointer-events-none transition-all duration-700" 
              style={{ backgroundColor: `rgba(225, 212, 192, ${lightingVal / 600})` }}
            />

            {/* Specimen Visual Centerpiece */}
            <div className="relative z-10 flex flex-col items-center justify-center space-y-4 text-center">
              <div className="w-44 h-44 rounded-3xl border border-[#E1D4C0]/40 bg-black/70 backdrop-blur-xl flex items-center justify-center shadow-2xl relative overflow-hidden transition-transform duration-500 group-hover:scale-105">
                <div className="absolute inset-0 bg-gradient-to-tr from-[#D4AF37]/25 via-transparent to-transparent" />
                <svg viewBox="0 0 100 100" className="w-28 h-28 stroke-[#E1D4C0] fill-none stroke-[1.5]">
                  <path d="M 30 20 L 70 20 L 62 85 L 35 85 Z" className="fill-[#E1D4C0]/10" />
                  <path d="M 40 20 Q 50 40 35 85 M 48 20 Q 50 45 48 85 M 58 20 Q 50 40 62 85" />
                </svg>
              </div>

              <div>
                <span className="text-[10px] font-mono uppercase tracking-widest text-[#E1D4C0]">
                  Modern Sovereign &bull; {selectedShot} SHOT
                </span>
                <h3 className="text-xl font-serif text-white mt-0.5">{activeStudy.title}</h3>
              </div>
            </div>

            {/* Canvas Badges */}
            <div className="absolute top-4 left-4 px-3 py-1.5 rounded-xl bg-black/70 border border-white/10 text-[11px] font-mono text-white/80 backdrop-blur-md">
              DNA COMPLIANCE: 98%
            </div>

            <div className="absolute top-4 right-4 px-3 py-1.5 rounded-xl bg-black/70 border border-white/10 text-[11px] font-mono text-emerald-400 backdrop-blur-md flex items-center gap-1.5">
              <ShieldCheck className="w-3.5 h-3.5" /> PRINT-SAFE
            </div>

            {/* Canvas Bottom Strip */}
            <div className="absolute bottom-4 left-4 right-4 flex items-center justify-between text-xs text-white/60 bg-black/70 backdrop-blur-md px-4 py-2.5 rounded-2xl border border-white/10">
              <span className="truncate">{activeStudy.lightingShader}</span>
              <button
                onClick={() => setShowAdvancedControls(true)}
                className="text-[11px] text-[#E1D4C0] hover:underline font-medium flex items-center gap-1 shrink-0 ml-2"
              >
                <span>Advanced optical controls</span>
                <ChevronRight className="w-3 h-3" />
              </button>
            </div>

          </div>

          {/* Natural Language Creative Control Box */}
          <form onSubmit={handleApplyNlCommand} className="p-4 rounded-2xl bg-[#111113]/90 border border-white/10 flex items-center gap-3">
            <div className="w-8 h-8 rounded-xl bg-[#E1D4C0]/10 text-[#E1D4C0] flex items-center justify-center shrink-0">
              <Sparkles className="w-4 h-4" />
            </div>
            <input
              type="text"
              value={nlCommand}
              onChange={(e) => setNlCommand(e.target.value)}
              placeholder='Describe creative adjustments in plain language... (e.g. "Make the hero more commanding")'
              className="flex-1 bg-transparent text-xs text-white placeholder-white/40 focus:outline-none font-light"
            />
            <button
              type="submit"
              disabled={isApplyingTweak || !nlCommand.trim()}
              className="px-4 py-2 rounded-xl bg-[#E1D4C0] text-[#0A0A0A] font-semibold text-xs hover:opacity-90 disabled:opacity-40 transition-opacity flex items-center gap-1.5"
            >
              {isApplyingTweak ? (
                <>
                  <RefreshCw className="w-3 h-3 animate-spin" />
                  <span>Synthesizing...</span>
                </>
              ) : (
                <>
                  <span>Adjust</span>
                  <Send className="w-3 h-3" />
                </>
              )}
            </button>
          </form>
        </div>

        {/* Right: Simple Intuitive Creative Sliders (4 Cols) */}
        <div className="lg:col-span-4 space-y-4">
          <div className="p-6 rounded-3xl bg-[#111113]/90 border border-white/10 space-y-6">
            <div className="space-y-1 border-b border-white/5 pb-3">
              <h4 className="text-sm font-serif text-white">Creative Tuning Controls</h4>
              <p className="text-[11px] text-white/40 font-light">
                Directly modulate aesthetic atmosphere. VYREN translates these into camera, lighting, and physics constraints.
              </p>
            </div>

            {/* Slider 1: Lighting */}
            <div className="space-y-2">
              <div className="flex items-center justify-between text-xs">
                <span className="text-white font-medium">Lighting Tone</span>
                <span className="text-[#E1D4C0] font-mono text-[11px]">
                  {lightingVal < 40 ? "Cinematic Dramatic" : lightingVal > 70 ? "Editorial High-Key" : "Balanced Chiaroscuro"}
                </span>
              </div>
              <input
                type="range"
                min="0"
                max="100"
                value={lightingVal}
                onChange={(e) => setLightingVal(Number(e.target.value))}
                className="w-full h-1.5 bg-white/10 rounded-lg appearance-none cursor-pointer accent-[#E1D4C0]"
              />
              <div className="flex justify-between text-[9px] font-mono uppercase text-white/30">
                <span>Cinematic</span>
                <span>Editorial</span>
              </div>
            </div>

            {/* Slider 2: Composition */}
            <div className="space-y-2">
              <div className="flex items-center justify-between text-xs">
                <span className="text-white font-medium">Composition</span>
                <span className="text-[#E1D4C0] font-mono text-[11px]">
                  {compositionVal < 40 ? "Minimal Architectural" : "Dynamic Angles"}
                </span>
              </div>
              <input
                type="range"
                min="0"
                max="100"
                value={compositionVal}
                onChange={(e) => setCompositionVal(Number(e.target.value))}
                className="w-full h-1.5 bg-white/10 rounded-lg appearance-none cursor-pointer accent-[#E1D4C0]"
              />
              <div className="flex justify-between text-[9px] font-mono uppercase text-white/30">
                <span>Minimal</span>
                <span>Dramatic</span>
              </div>
            </div>

            {/* Slider 3: Material Sheen */}
            <div className="space-y-2">
              <div className="flex items-center justify-between text-xs">
                <span className="text-white font-medium">Material Sheen</span>
                <span className="text-[#E1D4C0] font-mono text-[11px]">
                  {materialVal > 60 ? "Reflective Gold Zari" : "Soft Matte Silk"}
                </span>
              </div>
              <input
                type="range"
                min="0"
                max="100"
                value={materialVal}
                onChange={(e) => setMaterialVal(Number(e.target.value))}
                className="w-full h-1.5 bg-white/10 rounded-lg appearance-none cursor-pointer accent-[#E1D4C0]"
              />
              <div className="flex justify-between text-[9px] font-mono uppercase text-white/30">
                <span>Matte</span>
                <span>Reflective</span>
              </div>
            </div>

            {/* Slider 4: Atmosphere */}
            <div className="space-y-2">
              <div className="flex items-center justify-between text-xs">
                <span className="text-white font-medium">Atmospheric Depth</span>
                <span className="text-[#E1D4C0] font-mono text-[11px]">
                  {atmosphereVal > 50 ? "Warm Tungsten Haze" : "Crisp Minimal Studio"}
                </span>
              </div>
              <input
                type="range"
                min="0"
                max="100"
                value={atmosphereVal}
                onChange={(e) => setAtmosphereVal(Number(e.target.value))}
                className="w-full h-1.5 bg-white/10 rounded-lg appearance-none cursor-pointer accent-[#E1D4C0]"
              />
              <div className="flex justify-between text-[9px] font-mono uppercase text-white/30">
                <span>Clean Studio</span>
                <span>Atmospheric</span>
              </div>
            </div>

          </div>
        </div>

      </div>

      {/* Advanced Optical & Physics Modal (Layer 3 Progressive Disclosure) */}
      {showAdvancedControls && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-md animate-in fade-in duration-150">
          <div className="w-full max-w-2xl rounded-3xl bg-[#141416] border border-white/10 p-6 space-y-5 shadow-2xl">
            <div className="flex items-center justify-between border-b border-white/5 pb-3">
              <div className="flex items-center gap-2">
                <Camera className="w-4 h-4 text-[#E1D4C0]" />
                <h3 className="text-base font-serif text-white">Advanced Optical &amp; Physical Specifications</h3>
              </div>
              <button
                onClick={() => setShowAdvancedControls(false)}
                className="p-1 rounded-lg text-white/40 hover:text-white hover:bg-white/5"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="grid grid-cols-2 gap-4 text-xs">
              <div className="p-3.5 rounded-xl bg-white/[0.02] border border-white/5 space-y-1">
                <span className="text-[10px] font-mono uppercase text-white/40">Sensor &amp; Lens Setup</span>
                <p className="text-white">Full Frame 35mm &bull; 85mm Prime @ f/2.0</p>
              </div>
              <div className="p-3.5 rounded-xl bg-white/[0.02] border border-white/5 space-y-1">
                <span className="text-[10px] font-mono uppercase text-white/40">Textile Modulus</span>
                <p className="text-emerald-400 font-mono">38.4 N/m (Banarasi Brocade Shearing)</p>
              </div>
              <div className="p-3.5 rounded-xl bg-white/[0.02] border border-white/5 space-y-1">
                <span className="text-[10px] font-mono uppercase text-white/40">Colorimetry</span>
                <p className="text-white">Wide Gamut DCI-P3 calibrated for 300 DPI CMYK</p>
              </div>
              <div className="p-3.5 rounded-xl bg-white/[0.02] border border-white/5 space-y-1">
                <span className="text-[10px] font-mono uppercase text-white/40">Lighting Shader</span>
                <p className="text-white">Warm Tungsten Key + Soft Fill Rim (2800K)</p>
              </div>
            </div>

            <div className="pt-2 flex justify-end">
              <button
                onClick={() => setShowAdvancedControls(false)}
                className="px-4 py-2 rounded-xl bg-white/10 hover:bg-white/20 text-white text-xs font-medium"
              >
                Close Specifications
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}
