"use client";

import React, { useState } from "react";
import { 
  Printer, 
  CheckCircle2, 
  Clock, 
  Layers, 
  AlertCircle, 
  ShieldCheck, 
  FileText, 
  Sliders,
  Download,
  Info
} from "lucide-react";
import type { CampaignStudioModel, StudioProductionDeliverable } from "@/lib/campaignStudioFixtures";

interface ProductionTabProps {
  campaign: CampaignStudioModel;
  onNavigateTab: (tab: 'overview' | 'intelligence' | 'directions' | 'visuals' | 'assets' | 'review' | 'production' | 'outcomes') => void;
}

export function ProductionTab({ campaign, onNavigateTab }: ProductionTabProps) {
  const [deliverables, setDeliverables] = useState<StudioProductionDeliverable[]>(campaign.productionDeliverables);
  const [downloadModalInfo, setDownloadModalInfo] = useState<string | null>(null);

  const getStatusBadge = (status: StudioProductionDeliverable['readinessStatus']) => {
    switch (status) {
      case 'Ready':
        return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
      case 'Packaging':
        return 'bg-blue-500/10 text-blue-400 border-blue-500/30';
      case 'Awaiting Asset Approval':
        return 'bg-amber-500/10 text-amber-300 border-amber-500/30';
      case 'Blocked':
      default:
        return 'bg-rose-500/10 text-rose-300 border-rose-500/30';
    }
  };

  const handleExportClick = (del: StudioProductionDeliverable) => {
    setDownloadModalInfo(`Export Package Prepared: ${del.channel} (${del.format}, ${del.colorSpace}). Deliverable manifest generated with cryptographic audit hash.`);
    setTimeout(() => setDownloadModalInfo(null), 4000);
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-200">
      
      {/* Toast Notification */}
      {downloadModalInfo && (
        <div className="fixed bottom-8 right-8 z-50 p-4 rounded-xl bg-[#141416] border border-emerald-500/40 text-emerald-300 shadow-2xl flex items-center gap-3 text-xs animate-in slide-in-from-bottom-3 duration-200">
          <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          <span>{downloadModalInfo}</span>
        </div>
      )}

      {/* Surface Header & Compliance Notice */}
      <div className="p-6 rounded-2xl bg-[#111113]/80 border border-white/10 space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <Printer className="w-5 h-5 text-[#E1D4C0]" />
              <h2 className="text-lg font-serif text-white font-medium">Production Deliverables & Channel Packaging</h2>
            </div>
            <p className="text-xs text-white/50 font-light">
              Approved omnichannel assets validated against target print profiles and digital feed specifications.
            </p>
          </div>

          <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-white/[0.03] border border-white/10 text-[10px] font-mono text-white/50">
            <Info className="w-3.5 h-3.5 text-[#E1D4C0]" />
            <span>Pre-Flight Technical Gate Active</span>
          </div>
        </div>
      </div>

      {/* Deliverables Matrix */}
      <div className="space-y-4">
        {deliverables.map((del, idx) => (
          <div
            key={idx}
            className="p-6 rounded-2xl bg-[#111113]/90 border border-white/10 flex flex-col md:flex-row md:items-center justify-between gap-6 hover:border-white/20 transition-all"
          >
            {/* Left Channel & Format Specs */}
            <div className="space-y-2 max-w-md">
              <div className="flex items-center gap-2.5">
                <h3 className="text-base font-medium text-white">{del.channel}</h3>
                <span className={`px-2 py-0.5 rounded text-[9px] font-mono border ${getStatusBadge(del.readinessStatus)}`}>
                  {del.readinessStatus.toUpperCase()}
                </span>
              </div>

              <div className="flex items-center gap-4 text-xs font-mono text-white/50 flex-wrap">
                <span>Format: <strong className="text-white/80">{del.format}</strong></span>
                <span>•</span>
                <span>Resolution: <strong className="text-white/80">{del.resolution}</strong></span>
                <span>•</span>
                <span>Color: <strong className="text-[#E1D4C0]">{del.colorSpace}</strong></span>
                <span>•</span>
                <span>DPI: <strong className="text-white/80">{del.dpi}</strong></span>
              </div>
            </div>

            {/* Middle Progress Bar */}
            <div className="space-y-1.5 w-full md:w-48">
              <div className="flex justify-between text-[10px] font-mono text-white/40">
                <span>Asset Readiness</span>
                <span className="text-white">{del.assetsReady} / {del.totalRequired} Ready</span>
              </div>
              <div className="h-1.5 w-full bg-white/5 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-emerald-400 rounded-full" 
                  style={{ width: `${(del.assetsReady / del.totalRequired) * 100}%` }}
                />
              </div>
            </div>

            {/* Right Export Action */}
            <div className="flex items-center gap-2 self-start md:self-auto shrink-0">
              {del.readinessStatus === 'Ready' ? (
                <button
                  onClick={() => handleExportClick(del)}
                  className="px-4 py-2 rounded-xl bg-[#E1D4C0] text-[#0A0A0A] font-semibold text-xs hover:opacity-90 transition-opacity flex items-center gap-2 shadow-lg"
                >
                  <Download className="w-3.5 h-3.5" />
                  <span>Download Package</span>
                </button>
              ) : (
                <button
                  onClick={() => onNavigateTab('review')}
                  className="px-4 py-2 rounded-xl bg-white/[0.04] hover:bg-white/10 text-white/70 hover:text-white border border-white/10 text-xs font-medium transition-colors"
                >
                  Complete Approvals &rarr;
                </button>
              )}
            </div>
          </div>
        ))}
      </div>

    </div>
  );
}
