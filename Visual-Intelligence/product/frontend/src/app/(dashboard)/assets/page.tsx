"use client";

import { useState } from "react";
import Link from "next/link";
import { 
  Box, 
  RotateCw, 
  Layers, 
  Download, 
  Eye, 
  Filter, 
  Search, 
  CheckCircle2, 
  Sparkles,
  ArrowRight
} from "lucide-react";
import { DigitalHumanTurntable } from "@/components/studio/DigitalHumanTurntable";
import { AssetLineageDiff } from "@/components/studio/AssetLineageDiff";

export default function AssetsPage() {
  const [activeTab, setActiveTab] = useState<"library" | "turntable" | "lineage">("library");

  const assets = [
    {
      id: "AST-2026-001",
      title: "Royal Heritage Banarasi Saree (Emerald & Gold)",
      type: "3D Turntable + 4K Render",
      status: "Production Approved",
      size: "42.8 MB",
      dimensions: "4096 x 5120",
      drapeShader: "Banarasi Pure Katan",
      updated: "Yesterday"
    },
    {
      id: "AST-2026-002",
      title: "Chanderi Gossamer Veil Portrait (Atmospheric)",
      type: "Editorial Hero Image",
      status: "Production Approved",
      size: "18.4 MB",
      dimensions: "3840 x 2160",
      drapeShader: "Chanderi Sheer",
      updated: "2 days ago"
    },
    {
      id: "AST-2026-003",
      title: "Raw Khadi Minimalist Coat Silhouette",
      type: "Lookbook Asset",
      status: "In Review",
      size: "24.1 MB",
      dimensions: "3000 x 4000",
      drapeShader: "Raw Khadi Cotton",
      updated: "4 days ago"
    }
  ];

  return (
    <div className="h-full overflow-y-auto bg-[#0A0A0A] text-white/90 p-8 lg:p-12 scrollbar-thin scrollbar-thumb-white/10">
      <div className="max-w-6xl mx-auto space-y-10">
        
        {/* Header */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-6 border-b border-white/5">
          <div>
            <div className="flex items-center gap-2">
              <Box className="w-5 h-5 text-[#E1D4C0]" />
              <h1 className="text-2xl font-serif text-white font-light">Digital Assets & Turntable</h1>
            </div>
            <p className="text-xs text-white/50 font-light mt-1">
              Explore 360° digital human models, physical textile simulations, and immutable cryptographic asset lineage.
            </p>
          </div>

          <Link
            href="/studio"
            className="px-4 py-2 rounded-xl bg-[#E1D4C0] text-[#0A0A0A] text-xs font-semibold hover:opacity-90 transition-opacity flex items-center gap-2"
          >
            <Sparkles className="w-4 h-4" /> Synthesize New Asset
          </Link>
        </div>

        {/* Tab Navigation */}
        <div className="flex items-center gap-2 border-b border-white/10 pb-px text-xs font-medium">
          <button
            onClick={() => setActiveTab("library")}
            className={`pb-3 px-3 transition-colors relative ${
              activeTab === "library" ? "text-[#E1D4C0]" : "text-white/40 hover:text-white"
            }`}
          >
            Asset Library
            {activeTab === "library" && <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-[#E1D4C0]" />}
          </button>

          <button
            onClick={() => setActiveTab("turntable")}
            className={`pb-3 px-3 transition-colors relative ${
              activeTab === "turntable" ? "text-[#E1D4C0]" : "text-white/40 hover:text-white"
            }`}
          >
            3D Turntable View
            {activeTab === "turntable" && <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-[#E1D4C0]" />}
          </button>

          <button
            onClick={() => setActiveTab("lineage")}
            className={`pb-3 px-3 transition-colors relative ${
              activeTab === "lineage" ? "text-[#E1D4C0]" : "text-white/40 hover:text-white"
            }`}
          >
            Asset Lineage Diff
            {activeTab === "lineage" && <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-[#E1D4C0]" />}
          </button>
        </div>

        {/* Tab 1: Asset Library */}
        {activeTab === "library" && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {assets.map((a) => (
              <div 
                key={a.id}
                className="rounded-2xl border border-white/10 bg-[#111111]/80 hover:bg-[#151515] p-5 space-y-4 transition-all hover:border-[#E1D4C0]/40 flex flex-col justify-between"
              >
                <div className="space-y-3">
                  <div className="aspect-[4/3] rounded-xl bg-black/60 border border-white/5 flex items-center justify-center text-white/30 relative overflow-hidden group">
                    <Box className="w-10 h-10 group-hover:scale-110 transition-transform text-[#E1D4C0]/60" />
                    <span className="absolute bottom-2 right-2 px-2 py-0.5 rounded text-[9px] font-mono bg-black/80 text-white/60 border border-white/10">
                      {a.dimensions}
                    </span>
                  </div>

                  <div>
                    <div className="text-[10px] text-white/40 font-mono">{a.type}</div>
                    <h4 className="text-sm font-medium text-white mt-0.5 leading-snug">{a.title}</h4>
                  </div>

                  <div className="text-[11px] text-white/50 space-y-1 pt-1">
                    <div>Shader: <span className="text-white/80 font-mono">{a.drapeShader}</span></div>
                    <div>Size: <span className="text-white/80 font-mono">{a.size}</span></div>
                  </div>
                </div>

                <div className="pt-3 border-t border-white/5 flex items-center justify-between text-xs">
                  <span className="text-[10px] text-emerald-400 font-mono">{a.status}</span>
                  <button 
                    onClick={() => setActiveTab("turntable")}
                    className="text-[11px] text-[#E1D4C0] hover:underline flex items-center gap-1 font-medium"
                  >
                    View 3D <ArrowRight className="w-3 h-3" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Tab 2: 3D Turntable */}
        {activeTab === "turntable" && (
          <div className="rounded-2xl border border-white/10 bg-[#111111]/80 p-6 space-y-6">
            <h3 className="text-base font-medium text-white flex items-center gap-2">
              <RotateCw className="w-4 h-4 text-[#E1D4C0]" /> Real-Time 360° Digital Human Turntable
            </h3>
            <DigitalHumanTurntable />
          </div>
        )}

        {/* Tab 3: Lineage Diff */}
        {activeTab === "lineage" && (
          <div className="rounded-2xl border border-white/10 bg-[#111111]/80 p-6 space-y-6">
            <h3 className="text-base font-medium text-white flex items-center gap-2">
              <Layers className="w-4 h-4 text-purple-400" /> Immutable Cryptographic Asset Lineage Diff
            </h3>
            <AssetLineageDiff />
          </div>
        )}

      </div>
    </div>
  );
}
