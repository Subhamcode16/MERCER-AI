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
    <div className="h-full overflow-y-auto bg-background text-foreground p-8 lg:p-12 scrollbar-thin">
      <div className="max-w-6xl mx-auto space-y-10">
        
        {/* Header */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-6 border-b border-border">
          <div>
            <div className="flex items-center gap-2">
              <Dna className="w-5 h-5 text-primary" />
              <h1 className="text-2xl font-serif text-foreground font-light">VYREN Visual DNA</h1>
            </div>
            <p className="text-xs text-muted-foreground font-light mt-1">
              The aesthetic genome: Material drape physics, optical lighting setups, color mathematics, and typographic tokens.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <span className="inline-flex items-center px-3 py-1 rounded-full text-[10px] font-mono tracking-wider bg-purple-500/10 text-purple-700 dark:text-purple-300 border border-purple-500/20 font-medium">
              <ShieldCheck className="w-3 h-3 mr-1.5" /> 14 Physics Shaders Active
            </span>
          </div>
        </div>

        {/* Category Filters */}
        <div className="flex items-center gap-2 flex-wrap">
          <button
            onClick={() => setActiveCategory("all")}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-medium transition-colors cursor-pointer ${
              activeCategory === "all" ? "bg-primary text-primary-foreground font-semibold" : "bg-muted text-muted-foreground hover:text-foreground"
            }`}
          >
            All DNA Tokens
          </button>
          <button
            onClick={() => setActiveCategory("palettes")}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-medium transition-colors cursor-pointer ${
              activeCategory === "palettes" ? "bg-primary text-primary-foreground font-semibold" : "bg-muted text-muted-foreground hover:text-foreground"
            }`}
          >
            Color Mathematics
          </button>
          <button
            onClick={() => setActiveCategory("physics")}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-medium transition-colors cursor-pointer ${
              activeCategory === "physics" ? "bg-primary text-primary-foreground font-semibold" : "bg-muted text-muted-foreground hover:text-foreground"
            }`}
          >
            Textile & Drape Physics
          </button>
          <button
            onClick={() => setActiveCategory("optics")}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-medium transition-colors cursor-pointer ${
              activeCategory === "optics" ? "bg-primary text-primary-foreground font-semibold" : "bg-muted text-muted-foreground hover:text-foreground"
            }`}
          >
            Optical Lighting Shaders
          </button>
          <button
            onClick={() => setActiveCategory("typography")}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-medium transition-colors cursor-pointer ${
              activeCategory === "typography" ? "bg-primary text-primary-foreground font-semibold" : "bg-muted text-muted-foreground hover:text-foreground"
            }`}
          >
            Typography & Structure
          </button>
        </div>

        {/* Section 1: Color Mathematics */}
        {(activeCategory === "all" || activeCategory === "palettes") && (
          <div className="rounded-2xl border border-border bg-card p-6 space-y-6 shadow-sm">
            <div className="flex items-center justify-between">
              <h3 className="text-base font-medium text-foreground flex items-center gap-2">
                <Palette className="w-4 h-4 text-primary" /> Calibrated Color Tokens
              </h3>
              <span className="text-[10px] text-muted-foreground font-mono">WCAG AAA COMPLIANT</span>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <div className="p-4 rounded-xl bg-muted/30 border border-border space-y-2">
                <div className="h-16 rounded-lg bg-[#0F0D0A] border border-border" />
                <div className="text-xs font-medium text-foreground">Obsidian Heritage</div>
                <div className="text-[10px] text-muted-foreground font-mono">#0F0D0A • Primary Background</div>
              </div>

              <div className="p-4 rounded-xl bg-muted/30 border border-border space-y-2">
                <div className="h-16 rounded-lg bg-[#E1D4C0] border border-border" />
                <div className="text-xs font-medium text-foreground">Warm Raw Linen</div>
                <div className="text-[10px] text-muted-foreground font-mono">#E1D4C0 • Accent & Highlight</div>
              </div>

              <div className="p-4 rounded-xl bg-muted/30 border border-border space-y-2">
                <div className="h-16 rounded-lg bg-[#8A3324] border border-border" />
                <div className="text-xs font-medium text-foreground">Sindoor Vermilion</div>
                <div className="text-[10px] text-muted-foreground font-mono">#8A3324 • Secondary Warmth</div>
              </div>

              <div className="p-4 rounded-xl bg-muted/30 border border-border space-y-2">
                <div className="h-16 rounded-lg bg-[#D4AF37] border border-border" />
                <div className="text-xs font-medium text-foreground">Zari Metallic Gold</div>
                <div className="text-[10px] text-muted-foreground font-mono">#D4AF37 • Brocade Threading</div>
              </div>
            </div>
          </div>
        )}

        {/* Section 2: Textile & Drape Physics */}
        {(activeCategory === "all" || activeCategory === "physics") && (
          <div className="rounded-2xl border border-border bg-card p-6 space-y-6 shadow-sm">
            <h3 className="text-base font-medium text-foreground flex items-center gap-2">
              <Layers className="w-4 h-4 text-purple-600 dark:text-purple-400" /> Textile Drape & Material Physics
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-xs">
              <div className="p-4 rounded-xl bg-muted/30 border border-border space-y-3">
                <div className="flex items-center justify-between font-medium text-foreground">
                  <span>Banarasi Pure Katan Silk</span>
                  <span className="text-[10px] text-emerald-600 dark:text-emerald-400 font-mono font-medium">CALIBRATED</span>
                </div>
                <p className="text-[11px] text-muted-foreground font-light">
                  Heavy stiffness coefficient (0.88), micro-roughness (0.12), anisotropic metallic zari weft specular reflection.
                </p>
                <div className="pt-2 border-t border-border text-[10px] text-muted-foreground font-mono">
                  DENSITY: 180 g/m² • BENDING: High
                </div>
              </div>

              <div className="p-4 rounded-xl bg-muted/30 border border-border space-y-3">
                <div className="flex items-center justify-between font-medium text-foreground">
                  <span>Chanderi Sheer Organza</span>
                  <span className="text-[10px] text-emerald-600 dark:text-emerald-400 font-mono font-medium">CALIBRATED</span>
                </div>
                <p className="text-[11px] text-muted-foreground font-light">
                  Ultra-light translucent gossamer drape, subtle subsurface scattering, wind velocity response index (0.94).
                </p>
                <div className="pt-2 border-t border-border text-[10px] text-muted-foreground font-mono">
                  DENSITY: 45 g/m² • BENDING: Low
                </div>
              </div>

              <div className="p-4 rounded-xl bg-muted/30 border border-border space-y-3">
                <div className="flex items-center justify-between font-medium text-foreground">
                  <span>Raw Khadi Structured Cotton</span>
                  <span className="text-[10px] text-emerald-600 dark:text-emerald-400 font-mono font-medium">CALIBRATED</span>
                </div>
                <p className="text-[11px] text-muted-foreground font-light">
                  Matte diffuse absorption, organic slub texture bump mapping, structured crisp architectural fold geometry.
                </p>
                <div className="pt-2 border-t border-border text-[10px] text-muted-foreground font-mono">
                  DENSITY: 220 g/m² • BENDING: Medium
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Section 3: Optical Lighting Shaders */}
        {(activeCategory === "all" || activeCategory === "optics") && (
          <div className="rounded-2xl border border-border bg-card p-6 space-y-6 shadow-sm">
            <h3 className="text-base font-medium text-foreground flex items-center gap-2">
              <SunMedium className="w-4 h-4 text-amber-600 dark:text-amber-400" /> Optical Lighting & Camera Setups
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-xs">
              <div className="p-4 rounded-xl bg-muted/30 border border-border space-y-2">
                <div className="font-medium text-foreground">Editorial Chiaroscuro Profile</div>
                <p className="text-[11px] text-muted-foreground font-light">
                  Key light: 3200K Tungsten Fresnel at 45° angle. Fill light: 0.15 ratio diffuse ambient. Rim light: Sharp warm gold grazing.
                </p>
              </div>

              <div className="p-4 rounded-xl bg-muted/30 border border-border space-y-2">
                <div className="font-medium text-foreground">Atmospheric Golden Hour Profile</div>
                <p className="text-[11px] text-muted-foreground font-light">
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
