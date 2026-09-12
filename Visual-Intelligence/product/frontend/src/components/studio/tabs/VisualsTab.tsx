"use client";

import React, { useState } from "react";
import { 
  Palette, 
  Camera, 
  SunMedium, 
  Layers, 
  Sparkles, 
  CheckCircle2, 
  Sliders, 
  Maximize2,
  Image as ImageIcon,
  Activity,
  ArrowRight,
  ShieldCheck,
  RefreshCw
} from "lucide-react";
import type { CampaignStudioModel, ShotFamily, VisualStudy } from "@/lib/campaignStudioFixtures";

interface VisualsTabProps {
  campaign: CampaignStudioModel;
  onNavigateTab: (tab: 'overview' | 'intelligence' | 'directions' | 'visuals' | 'assets' | 'review' | 'production' | 'outcomes') => void;
}

export function VisualsTab({ campaign, onNavigateTab }: VisualsTabProps) {
  const [selectedFamily, setSelectedFamily] = useState<ShotFamily | 'All'>('All');
  const [activeStudy, setActiveStudy] = useState<VisualStudy>(campaign.visualStudies[0]);
  const [isSimulatingPhysics, setIsSimulatingPhysics] = useState(false);
  const [focalLength, setFocalLength] = useState("85mm");
  const [apertureVal, setApertureVal] = useState("f/2.0");

  const shotFamilies: ShotFamily[] = ['Hero', 'Detail', 'Portrait', 'Product', 'Editorial', 'Social'];

  const filteredStudies = selectedFamily === 'All'
    ? campaign.visualStudies
    : campaign.visualStudies.filter(s => s.shotFamily === selectedFamily);

  const handleRunPhysicsSimulation = () => {
    setIsSimulatingPhysics(true);
    setTimeout(() => setIsSimulatingPhysics(false), 1200);
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-200">
      
      {/* Surface Header & Shot Families Filter */}
      <div className="p-6 rounded-2xl bg-[#111113]/80 border border-white/10 space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <Palette className="w-5 h-5 text-[#E1D4C0]" />
              <h2 className="text-lg font-serif text-white font-medium">Visual Development Workspace</h2>
            </div>
            <p className="text-xs text-white/50 font-light">
              Interactive design studio for optical camera setups, textile drape physics simulations, and colorimetric palettes.
            </p>
          </div>

          {/* Shot Families Toolbar */}
          <div className="flex items-center gap-1.5 flex-wrap">
            <button
              onClick={() => setSelectedFamily('All')}
              className={`px-3 py-1.5 rounded-lg text-xs font-mono transition-all border ${
                selectedFamily === 'All'
                  ? "bg-[#E1D4C0] text-[#0A0A0A] font-bold border-[#E1D4C0]"
                  : "bg-white/[0.02] text-white/50 border-white/5 hover:text-white"
              }`}
            >
              All Shots
            </button>
            {shotFamilies.map((fam) => (
              <button
                key={fam}
                onClick={() => setSelectedFamily(fam)}
                className={`px-3 py-1.5 rounded-lg text-xs font-mono transition-all border ${
                  selectedFamily === fam
                    ? "bg-[#E1D4C0] text-[#0A0A0A] font-bold border-[#E1D4C0]"
                    : "bg-white/[0.02] text-white/50 border-white/5 hover:text-white"
                }`}
              >
                {fam}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Main Interactive Studio Canvas Split */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left: Visual Canvas & Simulation Stage */}
        <div className="lg:col-span-7 space-y-4">
          
          {/* Active Visual Study Canvas */}
          <div className="relative aspect-[4/3] rounded-2xl bg-gradient-to-br from-[#18181C] via-[#0E0E10] to-black border border-white/10 overflow-hidden flex flex-col items-center justify-center p-8 group">
            
            {/* Background Grid & Shader Ambient Glow */}
            <div className="absolute inset-0 bg-[radial-gradient(#E1D4C0_1px,transparent_1px)] [background-size:24px_24px] opacity-10 pointer-events-none" />
            <div className="absolute -top-24 -right-24 w-72 h-72 bg-amber-500/10 rounded-full blur-3xl pointer-events-none" />

            {/* Specimen Graphical Representation */}
            <div className="relative z-10 flex flex-col items-center justify-center space-y-4 text-center">
              <div className="w-32 h-32 rounded-2xl border border-[#E1D4C0]/30 bg-black/60 backdrop-blur-md flex items-center justify-center shadow-2xl relative overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-tr from-[#D4AF37]/20 via-transparent to-transparent" />
                <svg viewBox="0 0 100 100" className="w-20 h-20 stroke-[#E1D4C0] fill-none stroke-[1.5]">
                  <path d="M 30 20 L 70 20 L 62 85 L 35 85 Z" className="fill-[#E1D4C0]/10" />
                  <path d="M 40 20 Q 50 40 35 85 M 48 20 Q 50 45 48 85 M 58 20 Q 50 40 62 85" />
                </svg>
              </div>

              <div>
                <h3 className="text-base font-serif text-white">{activeStudy.title}</h3>
                <span className="text-[10px] font-mono text-[#E1D4C0] uppercase tracking-widest">{activeStudy.shotFamily} &bull; {activeStudy.aspectRatio}</span>
              </div>
            </div>

            {/* Canvas HUD Overlays */}
            <div className="absolute top-4 left-4 px-2.5 py-1 rounded-lg bg-black/60 border border-white/10 text-[10px] font-mono text-white/70 backdrop-blur-sm">
              OPTICS: {focalLength} · {apertureVal}
            </div>

            <div className="absolute top-4 right-4 px-2.5 py-1 rounded-lg bg-black/60 border border-white/10 text-[10px] font-mono text-emerald-400 backdrop-blur-sm flex items-center gap-1.5">
              <ShieldCheck className="w-3 h-3" /> DNA FIT: {activeStudy.dnaAdherenceScore}%
            </div>

            <div className="absolute bottom-4 left-4 right-4 flex items-center justify-between text-[10px] font-mono text-white/50 bg-black/60 backdrop-blur-sm px-3 py-2 rounded-xl border border-white/10">
              <span className="truncate max-w-[200px]">{activeStudy.lightingShader}</span>
              <button
                onClick={handleRunPhysicsSimulation}
                className="px-2.5 py-1 rounded-lg bg-[#E1D4C0]/10 hover:bg-[#E1D4C0]/20 text-[#E1D4C0] border border-[#E1D4C0]/30 transition-colors flex items-center gap-1"
              >
                <RefreshCw className={`w-3 h-3 ${isSimulatingPhysics ? 'animate-spin' : ''}`} />
                <span>Simulate Drape</span>
              </button>
            </div>

          </div>

          {/* Studies Selector Carousel */}
          <div className="grid grid-cols-3 gap-3">
            {filteredStudies.map((study) => (
              <div
                key={study.id}
                onClick={() => setActiveStudy(study)}
                className={`p-3 rounded-xl border cursor-pointer transition-all ${
                  activeStudy.id === study.id
                    ? "bg-[#E1D4C0]/10 border-[#E1D4C0]/50"
                    : "bg-[#111113]/60 border-white/5 hover:border-white/20"
                }`}
              >
                <div className="text-[9px] font-mono text-white/40 uppercase">{study.shotFamily}</div>
                <div className="text-xs font-medium text-white truncate mt-0.5">{study.title}</div>
              </div>
            ))}
          </div>

        </div>

        {/* Right: Optical & Material Parameter Controls */}
        <div className="lg:col-span-5 space-y-4">
          
          {/* Camera & Optics Controls */}
          <div className="p-5 rounded-2xl bg-[#111113]/90 border border-white/10 space-y-4">
            <div className="flex items-center justify-between border-b border-white/5 pb-2.5">
              <h4 className="text-xs font-medium text-white flex items-center gap-2">
                <Camera className="w-4 h-4 text-[#E1D4C0]" /> Optical Camera & Sensor Settings
              </h4>
              <span className="text-[10px] font-mono text-white/40">Full Frame 35mm</span>
            </div>

            <div className="space-y-3 text-xs">
              <div className="space-y-1">
                <div className="flex items-center justify-between text-[11px] text-white/60 font-mono">
                  <span>Focal Length</span>
                  <span className="text-[#E1D4C0]">{focalLength}</span>
                </div>
                <div className="grid grid-cols-4 gap-1.5">
                  {['24mm', '35mm', '50mm', '85mm'].map(f => (
                    <button
                      key={f}
                      onClick={() => setFocalLength(f)}
                      className={`py-1.5 rounded-lg text-[10px] font-mono border transition-all ${
                        focalLength === f ? 'bg-[#E1D4C0] text-black font-bold border-[#E1D4C0]' : 'bg-white/[0.02] text-white/60 border-white/5'
                      }`}
                    >
                      {f}
                    </button>
                  ))}
                </div>
              </div>

              <div className="space-y-1">
                <div className="flex items-center justify-between text-[11px] text-white/60 font-mono">
                  <span>Aperture</span>
                  <span className="text-[#E1D4C0]">{apertureVal}</span>
                </div>
                <div className="grid grid-cols-4 gap-1.5">
                  {['f/1.4', 'f/2.0', 'f/2.8', 'f/5.6'].map(a => (
                    <button
                      key={a}
                      onClick={() => setApertureVal(a)}
                      className={`py-1.5 rounded-lg text-[10px] font-mono border transition-all ${
                        apertureVal === a ? 'bg-[#E1D4C0] text-black font-bold border-[#E1D4C0]' : 'bg-white/[0.02] text-white/60 border-white/5'
                      }`}
                    >
                      {a}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Textile Physics Parameters */}
          <div className="p-5 rounded-2xl bg-[#111113]/90 border border-white/10 space-y-4">
            <div className="flex items-center justify-between border-b border-white/5 pb-2.5">
              <h4 className="text-xs font-medium text-white flex items-center gap-2">
                <Activity className="w-4 h-4 text-emerald-400" /> Textile Drape Physics Engine
              </h4>
              <span className="text-[10px] font-mono text-emerald-400">CALIBRATED</span>
            </div>

            <div className="space-y-2 text-xs">
              <div className="flex items-center justify-between text-white/70 py-1 border-b border-white/5">
                <span className="text-white/40 font-mono">Material:</span>
                <span className="font-medium text-white">{activeStudy.drapePhysics.material}</span>
              </div>
              <div className="flex items-center justify-between text-white/70 py-1 border-b border-white/5">
                <span className="text-white/40 font-mono">Shearing Stiffness:</span>
                <span className="font-mono text-[#E1D4C0]">{activeStudy.drapePhysics.shearingStiffness} N/m</span>
              </div>
              <div className="flex items-center justify-between text-white/70 py-1 border-b border-white/5">
                <span className="text-white/40 font-mono">Bending Modulus:</span>
                <span className="font-mono text-[#E1D4C0]">{activeStudy.drapePhysics.bendingModulus} mN·m</span>
              </div>
            </div>
          </div>

          {/* Color Palette Mathematics */}
          <div className="p-5 rounded-2xl bg-[#111113]/90 border border-white/10 space-y-4">
            <div className="flex items-center justify-between border-b border-white/5 pb-2.5">
              <h4 className="text-xs font-medium text-white flex items-center gap-2">
                <Palette className="w-4 h-4 text-purple-300" /> Colorimetric Palette Breakdown
              </h4>
              <span className="text-[10px] font-mono text-white/40">sRGB &bull; CMYK</span>
            </div>

            <div className="grid grid-cols-4 gap-2">
              {activeStudy.colorPalette.map((col, idx) => (
                <div key={idx} className="p-2.5 rounded-xl bg-white/[0.02] border border-white/5 space-y-1.5 text-center">
                  <div 
                    className="w-full h-8 rounded-lg border border-white/10 shadow-sm"
                    style={{ backgroundColor: col.hex }}
                  />
                  <div className="text-[10px] font-mono font-medium text-white truncate">{col.name}</div>
                  <div className="text-[9px] font-mono text-white/40">{col.weight}</div>
                </div>
              ))}
            </div>
          </div>

        </div>

      </div>

    </div>
  );
}
