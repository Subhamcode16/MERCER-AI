"use client";

import React, { useState } from "react";
import { 
  Printer, 
  CheckCircle2, 
  AlertCircle, 
  Download, 
  ArrowRight,
  Sparkles,
  ChevronRight,
  X,
  FileCheck,
  Send
} from "lucide-react";
import type { CampaignStudioModel, StudioProductionDeliverable } from "@/lib/campaignStudioFixtures";

interface ProductionTabProps {
  campaign: CampaignStudioModel;
  onNavigateTab: (tab: any) => void;
}

export function ProductionTab({ campaign, onNavigateTab }: ProductionTabProps) {
  const [deliverables] = useState<StudioProductionDeliverable[]>(campaign.productionDeliverables);
  const [selectedSpecs, setSelectedSpecs] = useState<StudioProductionDeliverable | null>(null);
  const [notification, setNotification] = useState<string | null>(null);
  const [isDeploying, setIsDeploying] = useState(false);

  const handleExportAll = () => {
    setIsDeploying(true);
    setTimeout(() => {
      setIsDeploying(false);
      setNotification("All approved assets exported and packaged into production release bundle.");
      setTimeout(() => setNotification(null), 4500);
    }, 1500);
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-200 pb-20 max-w-4xl mx-auto">
      
      {/* Toast Notification */}
      {notification && (
        <div className="fixed bottom-8 right-8 z-50 p-4 rounded-xl bg-[#141416] border border-emerald-500/40 text-emerald-300 shadow-2xl flex items-center gap-3 text-xs animate-in slide-in-from-bottom-3 duration-200">
          <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          <span>{notification}</span>
        </div>
      )}

      {/* Primary Header */}
      <div className="space-y-1 border-b border-white/5 pb-4">
        <span className="text-[10px] font-mono tracking-widest uppercase text-[#E1D4C0]">Multi-Surface Release</span>
        <h2 className="text-2xl font-serif text-white font-light">Are we ready to ship?</h2>
        <p className="text-xs text-white/50 font-light">
          Campaign assets are packaged for target surface dimensions, color spaces, and publishing formats.
        </p>
      </div>

      {/* Surface Status Card */}
      <div className="p-8 rounded-3xl bg-[#121214]/90 border border-white/10 space-y-6 shadow-2xl">
        
        <div className="flex items-center justify-between">
          <h3 className="text-base font-serif text-white">Campaign Multi-Surface Status</h3>
          <span className="text-xs font-mono text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-2.5 py-0.5 rounded-full">
            3 OF 4 SURFACES READY
          </span>
        </div>

        {/* Surface Rows */}
        <div className="divide-y divide-white/5 text-xs">
          
          {/* Surface 1: Instagram */}
          <div className="py-4 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-6 h-6 rounded-full bg-emerald-500/10 text-emerald-400 flex items-center justify-center font-bold text-xs">
                ✓
              </div>
              <div>
                <span className="text-white font-medium">Instagram Stories &amp; Reels (9:16)</span>
                <p className="text-white/40 text-[11px] font-light">8 video &amp; motion variations formatted</p>
              </div>
            </div>
            <button
              onClick={() => setSelectedSpecs(deliverables[0])}
              className="text-[11px] text-[#E1D4C0] hover:underline font-mono"
            >
              View specs &rarr;
            </button>
          </div>

          {/* Surface 2: Editorial */}
          <div className="py-4 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-6 h-6 rounded-full bg-emerald-500/10 text-emerald-400 flex items-center justify-center font-bold text-xs">
                ✓
              </div>
              <div>
                <span className="text-white font-medium">Web Editorial &amp; Lookbook (4:5)</span>
                <p className="text-white/40 text-[11px] font-light">6 high-resolution lookbook stills</p>
              </div>
            </div>
            <button
              onClick={() => setSelectedSpecs(deliverables[1])}
              className="text-[11px] text-[#E1D4C0] hover:underline font-mono"
            >
              View specs &rarr;
            </button>
          </div>

          {/* Surface 3: Print Catalog */}
          <div className="py-4 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-6 h-6 rounded-full bg-emerald-500/10 text-emerald-400 flex items-center justify-center font-bold text-xs">
                ✓
              </div>
              <div>
                <span className="text-white font-medium">Print Catalog &amp; Brochure</span>
                <p className="text-white/40 text-[11px] font-light">300 DPI CMYK TIFF spreads</p>
              </div>
            </div>
            <button
              onClick={() => setSelectedSpecs(deliverables[2])}
              className="text-[11px] text-[#E1D4C0] hover:underline font-mono"
            >
              View specs &rarr;
            </button>
          </div>

          {/* Surface 4: OOH Billboard (Action Needed) */}
          <div className="py-4 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-6 h-6 rounded-full bg-amber-500/10 text-amber-300 flex items-center justify-center font-bold text-xs">
                ⚠
              </div>
              <div>
                <span className="text-white font-medium">OOH Billboard (16:9 4K)</span>
                <p className="text-amber-300/80 text-[11px] font-light">1 human approval needed on shadow compression</p>
              </div>
            </div>
            <button
              onClick={() => onNavigateTab('review')}
              className="px-3 py-1 rounded-lg bg-amber-500/20 text-amber-300 text-[11px] font-medium hover:bg-amber-500/30 transition-colors"
            >
              Approve Asset &rarr;
            </button>
          </div>

        </div>

        {/* Global Release Action */}
        <div className="pt-4 border-t border-white/5 flex items-center justify-between">
          <p className="text-xs text-white/50 font-light">
            Once all channels are ready, you can deploy and track live audience metrics.
          </p>

          <button
            onClick={handleExportAll}
            disabled={isDeploying}
            className="px-6 py-2.5 rounded-xl bg-[#E1D4C0] text-[#0A0A0A] font-semibold text-xs hover:opacity-90 transition-opacity flex items-center gap-2 shadow-lg"
          >
            <Download className="w-4 h-4" />
            <span>{isDeploying ? "Packaging Bundle..." : "Download Release Package"}</span>
          </button>
        </div>

      </div>

      {/* Specifications Modal (Layer 3 Progressive Disclosure) */}
      {selectedSpecs && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-md animate-in fade-in duration-150">
          <div className="w-full max-w-lg rounded-3xl bg-[#141416] border border-white/10 p-6 space-y-5 shadow-2xl">
            <div className="flex items-center justify-between border-b border-white/5 pb-3">
              <div className="flex items-center gap-2">
                <FileCheck className="w-4 h-4 text-[#E1D4C0]" />
                <h3 className="text-base font-serif text-white">{selectedSpecs.channel} Export Specifications</h3>
              </div>
              <button
                onClick={() => setSelectedSpecs(null)}
                className="p-1 rounded-lg text-white/40 hover:text-white hover:bg-white/5"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="space-y-3 text-xs font-mono text-white/70">
              <div className="flex justify-between p-3 rounded-xl bg-white/[0.02] border border-white/5">
                <span className="text-white/40">Resolution</span>
                <span className="text-white">{selectedSpecs.resolution}</span>
              </div>
              <div className="flex justify-between p-3 rounded-xl bg-white/[0.02] border border-white/5">
                <span className="text-white/40">File Format</span>
                <span className="text-white">{selectedSpecs.format}</span>
              </div>
              <div className="flex justify-between p-3 rounded-xl bg-white/[0.02] border border-white/5">
                <span className="text-white/40">Color Profile</span>
                <span className="text-[#E1D4C0]">{selectedSpecs.colorSpace}</span>
              </div>
              <div className="flex justify-between p-3 rounded-xl bg-white/[0.02] border border-white/5">
                <span className="text-white/40">Target DPI</span>
                <span className="text-white">{selectedSpecs.dpi}</span>
              </div>
            </div>

            <div className="pt-2 flex justify-end">
              <button
                onClick={() => setSelectedSpecs(null)}
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
