"use client";

import React, { useState } from "react";
import { 
  Layers, 
  CheckCircle2, 
  Clock, 
  XCircle, 
  RotateCw, 
  GitCommit, 
  Filter, 
  ShieldCheck, 
  Eye, 
  Sliders,
  ExternalLink,
  Download
} from "lucide-react";
import type { AssetApprovalState, CampaignStudioModel, ShotFamily, StudioAsset } from "@/lib/campaignStudioFixtures";

interface AssetsTabProps {
  campaign: CampaignStudioModel;
  onNavigateTab: (tab: 'overview' | 'intelligence' | 'directions' | 'visuals' | 'assets' | 'review' | 'production' | 'outcomes') => void;
}

export function AssetsTab({ campaign, onNavigateTab }: AssetsTabProps) {
  const [selectedStatus, setSelectedStatus] = useState<string>('All');
  const [selectedAsset, setSelectedAsset] = useState<StudioAsset | null>(campaign.assets[0] || null);

  const getStatusBadge = (status: AssetApprovalState) => {
    switch (status) {
      case 'Approved':
      case 'Production Ready':
        return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
      case 'In Review':
        return 'bg-amber-500/10 text-amber-300 border-amber-500/30';
      case 'Draft':
        return 'bg-blue-500/10 text-blue-400 border-blue-500/30';
      case 'Rejected':
        return 'bg-rose-500/10 text-rose-300 border-rose-500/30';
      case 'Superseded':
      default:
        return 'bg-zinc-500/10 text-zinc-400 border-zinc-500/30';
    }
  };

  const filteredAssets = selectedStatus === 'All'
    ? campaign.assets
    : campaign.assets.filter(a => a.status === selectedStatus);

  return (
    <div className="space-y-8 animate-in fade-in duration-200">
      
      {/* Surface Header & Multi-Dimensional Filter */}
      <div className="p-6 rounded-2xl bg-[#111113]/80 border border-white/10 space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <Layers className="w-5 h-5 text-[#E1D4C0]" />
              <h2 className="text-lg font-serif text-white font-medium">Digital Asset Registry & Provenance</h2>
            </div>
            <p className="text-xs text-white/50 font-light">
              Every asset is cryptographically bound to its campaign direction, shot family, version, and human approval status.
            </p>
          </div>

          {/* Status Filter */}
          <div className="flex items-center gap-1.5 flex-wrap">
            {['All', 'Approved', 'In Review', 'Production Ready', 'Draft'].map((st) => (
              <button
                key={st}
                onClick={() => setSelectedStatus(st)}
                className={`px-3 py-1.5 rounded-lg text-xs font-mono transition-all border ${
                  selectedStatus === st
                    ? "bg-[#E1D4C0] text-[#0A0A0A] font-bold border-[#E1D4C0]"
                    : "bg-white/[0.02] text-white/50 border-white/5 hover:text-white"
                }`}
              >
                {st}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Asset Grid & Lineage Split */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left: Asset Cards Grid */}
        <div className="lg:col-span-8 grid grid-cols-1 sm:grid-cols-2 gap-4">
          {filteredAssets.map((asset) => {
            const isSelected = selectedAsset?.id === asset.id;
            return (
              <div
                key={asset.id}
                onClick={() => setSelectedAsset(asset)}
                className={`p-5 rounded-2xl border transition-all cursor-pointer space-y-4 relative overflow-hidden ${
                  isSelected
                    ? "bg-[#141417] border-[#E1D4C0] shadow-xl"
                    : "bg-[#111113]/60 border-white/5 hover:border-white/20"
                }`}
              >
                {/* Visual Thumbnail Specimen Container */}
                <div className="aspect-[4/3] rounded-xl bg-black/60 border border-white/5 flex flex-col items-center justify-center p-4 relative group">
                  <div className="w-16 h-16 rounded-xl border border-[#E1D4C0]/20 bg-white/[0.02] flex items-center justify-center text-[#E1D4C0]">
                    <Layers className="w-8 h-8 opacity-60" />
                  </div>
                  <div className="absolute top-2.5 left-2.5 px-2 py-0.5 rounded bg-black/70 border border-white/10 text-[9px] font-mono text-white/70">
                    {asset.aspectRatio} &bull; {asset.version}
                  </div>
                  <div className={`absolute top-2.5 right-2.5 px-2 py-0.5 rounded text-[9px] font-mono border ${getStatusBadge(asset.status)}`}>
                    {asset.status.toUpperCase()}
                  </div>
                </div>

                {/* Title & Channel Details */}
                <div className="space-y-1">
                  <h4 className="text-sm font-medium text-white line-clamp-1">{asset.title}</h4>
                  <div className="flex items-center justify-between text-[10px] font-mono text-white/40">
                    <span>{asset.channel}</span>
                    <span>{asset.shotFamily}</span>
                  </div>
                </div>

                {/* Spec Summary & Human Approval */}
                <div className="p-2.5 rounded-lg bg-white/[0.02] border border-white/5 flex items-center justify-between text-[10px] font-mono">
                  <span className="text-white/60 truncate max-w-[180px]">{asset.specSummary}</span>
                  {asset.humanApproval.approvedBy ? (
                    <span className="text-emerald-400 flex items-center gap-1">
                      <CheckCircle2 className="w-3 h-3" /> Signed
                    </span>
                  ) : (
                    <span className="text-amber-400 flex items-center gap-1">
                      <Clock className="w-3 h-3" /> In Review
                    </span>
                  )}
                </div>
              </div>
            );
          })}
        </div>

        {/* Right: Asset Lineage & Cryptographic Proof Drawer */}
        <div className="lg:col-span-4">
          {selectedAsset ? (
            <div className="p-6 rounded-2xl bg-[#111113]/90 border border-[#E1D4C0]/20 space-y-6 sticky top-24">
              
              <div className="space-y-1 border-b border-white/5 pb-4">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-mono uppercase text-[#E1D4C0]">Asset Lineage Inspector</span>
                  <span className={`px-2 py-0.5 rounded text-[9px] font-mono border ${getStatusBadge(selectedAsset.status)}`}>
                    {selectedAsset.status}
                  </span>
                </div>
                <h3 className="text-sm font-serif text-white font-medium">{selectedAsset.title}</h3>
              </div>

              {/* Lineage Hash & Chain of Custody */}
              <div className="space-y-2 text-xs">
                <span className="text-[10px] font-mono uppercase text-white/40 tracking-wider flex items-center gap-1.5">
                  <GitCommit className="w-3 h-3 text-[#E1D4C0]" /> Cryptographic Provenance Hash
                </span>
                <div className="p-3 rounded-xl bg-black/60 border border-white/5 font-mono text-[11px] text-emerald-400/90 break-all">
                  SHA-256: {selectedAsset.lineageHash}
                </div>
              </div>

              {/* Human Decision Record */}
              <div className="p-4 rounded-xl bg-white/[0.02] border border-white/5 space-y-2 text-xs">
                <span className="text-[10px] font-mono uppercase text-white/40 tracking-wider">Human Decision Sign-off</span>
                {selectedAsset.humanApproval.approvedBy ? (
                  <div className="space-y-1 text-white/80">
                    <p><span className="text-white/40 font-mono">Approved By:</span> {selectedAsset.humanApproval.approvedBy}</p>
                    <p><span className="text-white/40 font-mono">Timestamp:</span> {selectedAsset.humanApproval.approvedAt}</p>
                    {selectedAsset.humanApproval.notes && (
                      <p className="text-[11px] text-white/60 font-light italic mt-1">"{selectedAsset.humanApproval.notes}"</p>
                    )}
                  </div>
                ) : (
                  <div className="space-y-2">
                    <p className="text-amber-300/80 font-light text-[11px]">Asset currently awaiting human sign-off in the Review Gate.</p>
                    <button
                      onClick={() => onNavigateTab('review')}
                      className="w-full py-1.5 rounded-lg bg-[#E1D4C0] text-[#0A0A0A] font-semibold text-[11px] transition-opacity hover:opacity-90"
                    >
                      Go to Review Gate &rarr;
                    </button>
                  </div>
                )}
              </div>

              {/* Export Specifications */}
              <div className="space-y-1.5 text-xs text-white/60">
                <span className="text-[10px] font-mono uppercase text-white/40 tracking-wider">Delivery Specs</span>
                <div className="p-3 rounded-xl bg-white/[0.02] border border-white/5 space-y-1 text-[11px] font-mono">
                  <div>Channel: {selectedAsset.channel}</div>
                  <div>Aspect: {selectedAsset.aspectRatio}</div>
                  <div>Resolution: {selectedAsset.specSummary}</div>
                </div>
              </div>

            </div>
          ) : (
            <div className="p-12 text-center text-white/40 border border-white/5 rounded-2xl bg-[#111113]/40">
              Select an asset to view lineage and proof details.
            </div>
          )}
        </div>

      </div>

    </div>
  );
}
