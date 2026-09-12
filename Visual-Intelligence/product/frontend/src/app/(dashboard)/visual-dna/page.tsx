"use client";

import { useState } from "react";
import Link from "next/link";
import { 
  Dna, 
  Layers, 
  Palette, 
  SunMedium, 
  Sparkles, 
  Eye, 
  Sliders, 
  CheckCircle2, 
  ArrowRight,
  ShieldCheck,
  RotateCw
} from "lucide-react";

export default function VisualDnaPage() {
  const [activeCategory, setActiveCategory] = useState<"all" | "palettes" | "physics" | "optics" | "typography">("all");

  return (
    <div className="h-full overflow-y-auto bg-[#0A0A0A] text-white/90 p-8 lg:p-12 scrollbar-thin scrollbar-thumb-white/10">
      <div className="max-w-6xl mx-auto space-y-10">
        
        {/* Header */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-6 border-b border-white/5">
          <div>
            <div className="flex items-center gap-2">
              <Dna className="w-5 h-5 text-[#E1D4C0]" />
              <h1 className="text-2xl font-serif text-white font-light">VYREN Visual DNA</h1>
            </div>
            <p className="text-xs text-white/50 font-light mt-1">
              The aesthetic genome: Material drape physics, optical lighting setups, color mathematics, and typographic tokens.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <span className="inline-flex items-center px-3 py-1 rounded-full text-[10px] font-mono tracking-wider bg-purple-500/10 text-purple-300 border border-purple-500/20">
              <ShieldCheck className="w-3 h-3 mr-1.5" /> 14 Physics Shaders Active
            </span>
          </div>
        </div>

        {/* Category Filters */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => setActiveCategory("all")}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-medium transition-colors ${
              activeCategory === "all" ? "bg-white/10 text-white" : "text-white/40 hover:text-white"
            }`}
          >
            All DNA Tokens
          </button>
          <button
            onClick={() => setActiveCategory("palettes")}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-medium transition-colors ${
              activeCategory === "palettes" ? "bg-white/10 text-white" : "text-white/40 hover:text-white"
            }`}
          >
            Color Mathematics
          </button>
          <button
            onClick={() => setActiveCategory("physics")}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-medium transition-colors ${
              activeCategory === "physics" ? "bg-white/10 text-white" : "text-white/40 hover:text-white"
            }`}
          >
            Textile & Drape Physics
          </button>
          <button
            onClick={() => setActiveCategory("optics")}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-medium transition-colors ${
              activeCategory === "optics" ? "bg-white/10 text-white" : "text-white/40 hover:text-white"
            }`}
          >
            Optical Lighting Shaders
          </button>
          <button
            onClick={() => setActiveCategory("typography")}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-medium transition-colors ${
              activeCategory === "typography" ? "bg-white/10 text-white" : "text-white/40 hover:text-white"
            }`}
          >
            Typography & Structure
          </button>
        </div>

        {/* Section 1: Color Mathematics */}
        {(activeCategory === "all" || activeCategory === "palettes") && (
          <div className="rounded-2xl border border-white/10 bg-[#111111]/80 p-6 space-y-6">
            <div className="flex items-center justify-between">
              <h3 className="text-base font-medium text-white flex items-center gap-2">
                <Palette className="w-4 h-4 text-[#E1D4C0]" /> Calibrated Color Tokens
              </h3>
              <span className="text-[10px] text-white/40 font-mono">WCAG AAA COMPLIANT</span>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <div className="p-4 rounded-xl bg-white/[0.02] border border-white/5 space-y-2">
                <div className="h-16 rounded-lg bg-[#0F0D0A] border border-white/10" />
                <div className="text-xs font-medium text-white">Obsidian Heritage</div>
                <div className="text-[10px] text-white/40 font-mono">#0F0D0A • Primary Background</div>
              </div>

              <div className="p-4 rounded-xl bg-white/[0.02] border border-white/5 space-y-2">
                <div className="h-16 rounded-lg bg-[#E1D4C0] border border-white/10" />
                <div className="text-xs font-medium text-white">Warm Raw Linen</div>
                <div className="text-[10px] text-white/40 font-mono">#E1D4C0 • Accent & Highlight</div>
              </div>

              <div className="p-4 rounded-xl bg-white/[0.02] border border-white/5 space-y-2">
                <div className="h-16 rounded-lg bg-[#8A3324] border border-white/10" />
                <div className="text-xs font-medium text-white">Sindoor Vermilion</div>
                <div className="text-[10px] text-white/40 font-mono">#8A3324 • Secondary Warmth</div>
              </div>

              <div className="p-4 rounded-xl bg-white/[0.02] border border-white/5 space-y-2">
                <div className="h-16 rounded-lg bg-[#D4AF37] border border-white/10" />
                <div className="text-xs font-medium text-white">Zari Metallic Gold</div>
                <div className="text-[10px] text-white/40 font-mono">#D4AF37 • Brocade Threading</div>
              </div>
            </div>
          </div>
        )}

        {/* Section 2: Textile & Drape Physics */}
        {(activeCategory === "all" || activeCategory === "physics") && (
          <div className="rounded-2xl border border-white/10 bg-[#111111]/80 p-6 space-y-6">
            <h3 className="text-base font-medium text-white flex items-center gap-2">
              <Layers className="w-4 h-4 text-purple-400" /> Textile Drape & Material Physics
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-xs">
              <div className="p-4 rounded-xl bg-white/[0.02] border border-white/5 space-y-3">
                <div className="flex items-center justify-between font-medium text-white">
                  <span>Banarasi Pure Katan Silk</span>
                  <span className="text-[10px] text-emerald-400 font-mono">CALIBRATED</span>
                </div>
                <p className="text-[11px] text-white/60 font-light">
                  Heavy stiffness coefficient (0.88), micro-roughness (0.12), anisotropic metallic zari weft specular reflection.
                </p>
                <div className="pt-2 border-t border-white/5 text-[10px] text-white/40 font-mono">
                  DENSITY: 180 g/m² • BENDING: High
                </div>
              </div>

              <div className="p-4 rounded-xl bg-white/[0.02] border border-white/5 space-y-3">
                <div className="flex items-center justify-between font-medium text-white">
                  <span>Chanderi Sheer Organza</span>
                  <span className="text-[10px] text-emerald-400 font-mono">CALIBRATED</span>
                </div>
                <p className="text-[11px] text-white/60 font-light">
                  Ultra-light translucent gossamer drape, subtle subsurface scattering, wind velocity response index (0.94).
                </p>
                <div className="pt-2 border-t border-white/5 text-[10px] text-white/40 font-mono">
                  DENSITY: 45 g/m² • BENDING: Low
                </div>
              </div>

              <div className="p-4 rounded-xl bg-white/[0.02] border border-white/5 space-y-3">
                <div className="flex items-center justify-between font-medium text-white">
                  <span>Raw Khadi Structured Cotton</span>
                  <span className="text-[10px] text-emerald-400 font-mono">CALIBRATED</span>
                </div>
                <p className="text-[11px] text-white/60 font-light">
                  Matte diffuse absorption, organic slub texture bump mapping, structured crisp architectural fold geometry.
                </p>
                <div className="pt-2 border-t border-white/5 text-[10px] text-white/40 font-mono">
                  DENSITY: 220 g/m² • BENDING: Medium
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Section 3: Optical Lighting Shaders */}
        {(activeCategory === "all" || activeCategory === "optics") && (
          <div className="rounded-2xl border border-white/10 bg-[#111111]/80 p-6 space-y-6">
            <h3 className="text-base font-medium text-white flex items-center gap-2">
              <SunMedium className="w-4 h-4 text-amber-400" /> Optical Lighting & Camera Setups
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-xs">
              <div className="p-4 rounded-xl bg-white/[0.02] border border-white/5 space-y-2">
                <div className="font-medium text-white">Editorial Chiaroscuro Profile</div>
                <p className="text-[11px] text-white/60 font-light">
                  Key light: 3200K Tungsten Fresnel at 45° angle. Fill light: 0.15 ratio diffuse ambient. Rim light: Sharp warm gold grazing.
                </p>
              </div>

              <div className="p-4 rounded-xl bg-white/[0.02] border border-white/5 space-y-2">
                <div className="font-medium text-white">Atmospheric Golden Hour Profile</div>
                <p className="text-[11px] text-white/60 font-light">
                  Low-angle 2800K directional sun simulation with atmospheric particulate volumetric haze and gentle lens bloom.
                </p>
              </div>
            </div>
          </div>
        )}

      </div>
    </div>
  );
}
