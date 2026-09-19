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
        <div className="fixed bottom-8 right-8 z-50 p-4 rounded-xl bg-card border border-emerald-500/40 text-emerald-600 dark:text-emerald-300 shadow-2xl flex items-center gap-3 text-xs animate-in slide-in-from-bottom-3 duration-200">
          <CheckCircle2 className="w-4 h-4 text-emerald-500 dark:text-emerald-400" />
          <span>{notification}</span>
        </div>
      )}

      {/* Primary Header */}
      <div className="space-y-1 border-b border-border pb-4">
        <span className="text-[10px] font-mono tracking-widest uppercase text-primary font-bold">Multi-Surface Release</span>
        <h2 className="text-2xl font-serif text-foreground font-light">Are we ready to ship?</h2>
        <p className="text-xs text-muted-foreground font-light">
          Campaign assets are packaged for target surface dimensions, color spaces, and publishing formats.
        </p>
      </div>

      {/* Surface Status Card */}
      <div className="p-8 rounded-3xl bg-card border border-border space-y-6 shadow-sm">
        
        <div className="flex items-center justify-between">
          <h3 className="text-base font-serif text-foreground">Campaign Multi-Surface Status</h3>
          <span className="text-xs font-mono text-emerald-600 dark:text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-2.5 py-0.5 rounded-full font-semibold">
            3 OF 4 SURFACES READY
          </span>
        </div>

        {/* Surface Rows */}
        <div className="divide-y divide-border text-xs">
          
          {/* Surface 1: Instagram */}
          <div className="py-4 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-6 h-6 rounded-full bg-emerald-500/15 text-emerald-600 dark:text-emerald-400 flex items-center justify-center font-bold text-xs">
                ✓
              </div>
              <div>
                <span className="text-foreground font-medium">Instagram Stories &amp; Reels (9:16)</span>
                <p className="text-muted-foreground text-[11px] font-light">8 video &amp; motion variations formatted</p>
              </div>
            </div>
            <button
              onClick={() => setSelectedSpecs(deliverables[0])}
              className="text-[11px] text-primary hover:underline font-mono"
            >
              View specs &rarr;
            </button>
          </div>

          {/* Surface 2: Editorial */}
          <div className="py-4 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-6 h-6 rounded-full bg-emerald-500/15 text-emerald-600 dark:text-emerald-400 flex items-center justify-center font-bold text-xs">
                ✓
              </div>
              <div>
                <span className="text-foreground font-medium">Web Editorial &amp; Lookbook (4:5)</span>
                <p className="text-muted-foreground text-[11px] font-light">6 high-resolution lookbook stills</p>
              </div>
            </div>
            <button
              onClick={() => setSelectedSpecs(deliverables[1])}
              className="text-[11px] text-primary hover:underline font-mono"
            >
              View specs &rarr;
            </button>
          </div>

          {/* Surface 3: Print Catalog */}
          <div className="py-4 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-6 h-6 rounded-full bg-emerald-500/15 text-emerald-600 dark:text-emerald-400 flex items-center justify-center font-bold text-xs">
                ✓
              </div>
              <div>
                <span className="text-foreground font-medium">Print Catalog &amp; Brochure</span>
                <p className="text-muted-foreground text-[11px] font-light">300 DPI CMYK TIFF spreads</p>
              </div>
            </div>
            <button
              onClick={() => setSelectedSpecs(deliverables[2])}
              className="text-[11px] text-primary hover:underline font-mono"
            >
              View specs &rarr;
            </button>
          </div>

          {/* Surface 4: OOH Billboard (Action Needed) */}
          <div className="py-4 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-6 h-6 rounded-full bg-amber-500/15 text-amber-700 dark:text-amber-300 flex items-center justify-center font-bold text-xs">
                ⚠
              </div>
              <div>
                <span className="text-foreground font-medium">OOH Billboard (16:9 4K)</span>
                <p className="text-amber-700 dark:text-amber-300 text-[11px] font-light">1 human approval needed on shadow compression</p>
              </div>
            </div>
            <button
              onClick={() => onNavigateTab('review')}
              className="px-3 py-1 rounded-lg bg-amber-500/20 text-amber-700 dark:text-amber-300 text-[11px] font-medium hover:bg-amber-500/30 transition-colors"
            >
              Approve Asset &rarr;
            </button>
          </div>

        </div>

        {/* Global Release Action */}
        <div className="pt-4 border-t border-border flex items-center justify-between">
          <p className="text-xs text-muted-foreground font-light">
            Once all channels are ready, you can deploy and track live audience metrics.
          </p>

          <button
            onClick={handleExportAll}
            disabled={isDeploying}
            className="px-6 py-2.5 rounded-xl bg-primary text-primary-foreground font-semibold text-xs hover:opacity-90 transition-opacity flex items-center gap-2 shadow-sm"
          >
            <Download className="w-4 h-4" />
            <span>{isDeploying ? "Packaging Bundle..." : "Download Release Package"}</span>
          </button>
        </div>

      </div>

      {/* Specifications Modal (Layer 3 Progressive Disclosure) */}
      {selectedSpecs && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-background/80 backdrop-blur-md animate-in fade-in duration-150">
          <div className="w-full max-w-lg rounded-3xl bg-card border border-border p-6 space-y-5 shadow-2xl">
            <div className="flex items-center justify-between border-b border-border pb-3">
              <div className="flex items-center gap-2">
                <FileCheck className="w-4 h-4 text-primary" />
                <h3 className="text-base font-serif text-foreground">{selectedSpecs.channel} Export Specifications</h3>
              </div>
              <button
                onClick={() => setSelectedSpecs(null)}
                className="p-1 rounded-lg text-muted-foreground hover:text-foreground hover:bg-accent"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="space-y-3 text-xs font-mono text-muted-foreground">
              <div className="flex justify-between p-3 rounded-xl bg-muted/40 border border-border">
                <span className="text-muted-foreground/70">Resolution</span>
                <span className="text-foreground">{selectedSpecs.resolution}</span>
              </div>
              <div className="flex justify-between p-3 rounded-xl bg-muted/40 border border-border">
                <span className="text-muted-foreground/70">File Format</span>
                <span className="text-foreground">{selectedSpecs.format}</span>
              </div>
              <div className="flex justify-between p-3 rounded-xl bg-muted/40 border border-border">
                <span className="text-muted-foreground/70">Color Profile</span>
                <span className="text-primary font-semibold">{selectedSpecs.colorSpace}</span>
              </div>
              <div className="flex justify-between p-3 rounded-xl bg-muted/40 border border-border">
                <span className="text-muted-foreground/70">Target DPI</span>
                <span className="text-foreground">{selectedSpecs.dpi}</span>
              </div>
            </div>

            <div className="pt-2 flex justify-end">
              <button
                onClick={() => setSelectedSpecs(null)}
                className="px-4 py-2 rounded-xl bg-primary text-primary-foreground hover:opacity-90 text-xs font-medium shadow-sm"
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
