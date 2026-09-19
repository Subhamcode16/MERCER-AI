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
      <div className="p-6 rounded-2xl bg-card border border-border space-y-4 shadow-sm">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <Layers className="w-5 h-5 text-primary" />
              <h2 className="text-lg font-serif text-foreground font-medium">Digital Asset Registry & Provenance</h2>
            </div>
            <p className="text-xs text-muted-foreground font-light">
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
                    ? "bg-primary text-primary-foreground font-bold border-primary shadow-sm"
                    : "bg-muted/40 text-muted-foreground border-border hover:text-foreground hover:bg-accent"
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
                    ? "bg-card border-primary shadow-md"
                    : "bg-card/70 border-border hover:border-border/80 hover:bg-card"
                }`}
              >
                {/* Visual Thumbnail Specimen Container */}
                <div className="aspect-[4/3] rounded-xl bg-muted/60 border border-border flex flex-col items-center justify-center p-4 relative group">
                  <div className="w-16 h-16 rounded-xl border border-primary/20 bg-card flex items-center justify-center text-primary shadow-sm">
                    <Layers className="w-8 h-8 opacity-80" />
                  </div>
                  <div className="absolute top-2.5 left-2.5 px-2 py-0.5 rounded bg-card/90 border border-border text-[9px] font-mono text-foreground backdrop-blur-md shadow-sm">
                    {asset.aspectRatio} &bull; {asset.version}
                  </div>
                  <div className={`absolute top-2.5 right-2.5 px-2 py-0.5 rounded text-[9px] font-mono border ${getStatusBadge(asset.status)}`}>
                    {asset.status.toUpperCase()}
                  </div>
                </div>

                {/* Title & Channel Details */}
                <div className="space-y-1">
                  <h4 className="text-sm font-medium text-foreground line-clamp-1">{asset.title}</h4>
                  <div className="flex items-center justify-between text-[10px] font-mono text-muted-foreground">
                    <span>{asset.channel}</span>
                    <span>{asset.shotFamily}</span>
                  </div>
                </div>

                {/* Spec Summary & Human Approval */}
                <div className="p-2.5 rounded-lg bg-muted/40 border border-border flex items-center justify-between text-[10px] font-mono">
                  <span className="text-muted-foreground truncate max-w-[180px]">{asset.specSummary}</span>
                  {asset.humanApproval.approvedBy ? (
                    <span className="text-emerald-600 dark:text-emerald-400 flex items-center gap-1 font-semibold">
                      <CheckCircle2 className="w-3 h-3" /> Signed
                    </span>
                  ) : (
                    <span className="text-amber-700 dark:text-amber-400 flex items-center gap-1 font-semibold">
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
            <div className="p-6 rounded-2xl bg-card border border-border space-y-6 sticky top-24 shadow-sm">
              
              <div className="space-y-1 border-b border-border pb-4">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-mono uppercase text-primary font-bold">Asset Lineage Inspector</span>
                  <span className={`px-2 py-0.5 rounded text-[9px] font-mono border ${getStatusBadge(selectedAsset.status)}`}>
                    {selectedAsset.status}
                  </span>
                </div>
                <h3 className="text-sm font-serif text-foreground font-medium">{selectedAsset.title}</h3>
              </div>

              {/* Lineage Hash & Chain of Custody */}
              <div className="space-y-2 text-xs">
                <span className="text-[10px] font-mono uppercase text-muted-foreground/70 tracking-wider flex items-center gap-1.5">
                  <GitCommit className="w-3 h-3 text-primary" /> Cryptographic Provenance Hash
                </span>
                <div className="p-3 rounded-xl bg-muted/40 border border-border font-mono text-[11px] text-emerald-600 dark:text-emerald-400 break-all font-semibold">
                  SHA-256: {selectedAsset.lineageHash}
                </div>
              </div>

              {/* Human Decision Record */}
              <div className="p-4 rounded-xl bg-muted/40 border border-border space-y-2 text-xs">
                <span className="text-[10px] font-mono uppercase text-muted-foreground/70 tracking-wider">Human Decision Sign-off</span>
                {selectedAsset.humanApproval.approvedBy ? (
                  <div className="space-y-1 text-foreground/90">
                    <p><span className="text-muted-foreground font-mono">Approved By:</span> {selectedAsset.humanApproval.approvedBy}</p>
                    <p><span className="text-muted-foreground font-mono">Timestamp:</span> {selectedAsset.humanApproval.approvedAt}</p>
                    {selectedAsset.humanApproval.notes && (
                      <p className="text-[11px] text-muted-foreground font-light italic mt-1">"{selectedAsset.humanApproval.notes}"</p>
                    )}
                  </div>
                ) : (
                  <div className="space-y-2">
                    <p className="text-amber-800 dark:text-amber-300 font-light text-[11px]">Asset currently awaiting human sign-off in the Review Gate.</p>
                    <button
                      onClick={() => onNavigateTab('review')}
                      className="w-full py-1.5 rounded-lg bg-primary text-primary-foreground font-semibold text-[11px] transition-opacity hover:opacity-90 shadow-sm"
                    >
                      Go to Review Gate &rarr;
                    </button>
                  </div>
                )}
              </div>

              {/* Export Specifications */}
              <div className="space-y-1.5 text-xs text-muted-foreground">
                <span className="text-[10px] font-mono uppercase text-muted-foreground/70 tracking-wider">Delivery Specs</span>
                <div className="p-3 rounded-xl bg-muted/40 border border-border space-y-1 text-[11px] font-mono">
                  <div>Channel: {selectedAsset.channel}</div>
                  <div>Aspect: {selectedAsset.aspectRatio}</div>
                  <div>Resolution: {selectedAsset.specSummary}</div>
                </div>
              </div>

            </div>
          ) : (
            <div className="p-12 text-center text-muted-foreground border border-border rounded-2xl bg-card">
              Select an asset to view lineage and proof details.
            </div>
          )}
        </div>

      </div>

    </div>
  );
}
