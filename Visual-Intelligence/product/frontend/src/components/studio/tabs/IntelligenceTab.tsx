"use client";

import React, { useState } from "react";
import { 
  Brain, 
  Database, 
  HelpCircle, 
  ShieldAlert, 
  CheckCircle2, 
  Filter, 
  Layers, 
  Sparkles,
  ExternalLink,
  ChevronRight,
  TrendingUp,
  Sliders
} from "lucide-react";
import type { CampaignStudioModel, EpistemicStatus, IntelligenceItem } from "@/lib/campaignStudioFixtures";

interface IntelligenceTabProps {
  campaign: CampaignStudioModel;
}

export function IntelligenceTab({ campaign }: IntelligenceTabProps) {
  const [selectedStatus, setSelectedStatus] = useState<string>('All');
  const [activeItem, setActiveItem] = useState<IntelligenceItem | null>(campaign.intelligence[0] || null);

  const getStatusBadge = (status: EpistemicStatus) => {
    switch (status) {
      case 'Observed':
        return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
      case 'Supported':
        return 'bg-blue-500/10 text-blue-400 border-blue-500/30';
      case 'Experimental':
        return 'bg-amber-500/10 text-amber-300 border-amber-500/30';
      case 'Correlated':
        return 'bg-purple-500/10 text-purple-300 border-purple-500/30';
      case 'Unknown':
      default:
        return 'bg-zinc-500/10 text-zinc-400 border-zinc-500/30 border-dashed';
    }
  };

  const filteredItems = selectedStatus === 'All' 
    ? campaign.intelligence 
    : campaign.intelligence.filter(item => item.epistemicStatus === selectedStatus);

  return (
    <div className="space-y-8 animate-in fade-in duration-200">
      
      {/* Surface Header & Epistemic Banner */}
      <div className="p-6 rounded-2xl bg-[#111113]/80 border border-white/10 space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <Brain className="w-5 h-5 text-[#E1D4C0]" />
              <h2 className="text-lg font-serif text-white font-medium">Pre-Generation Creative Intelligence</h2>
            </div>
            <p className="text-xs text-white/50 font-light">
              Rigorous empirical signals, physics boundaries, and epistemic statuses formulated prior to creative synthesis.
            </p>
          </div>

          {/* Epistemic Status Invariant Legend */}
          <div className="flex items-center gap-1.5 flex-wrap">
            {['All', 'Observed', 'Supported', 'Experimental', 'Correlated', 'Unknown'].map((status) => (
              <button
                key={status}
                onClick={() => setSelectedStatus(status)}
                className={`px-2.5 py-1 rounded-lg text-[10px] font-mono transition-all border ${
                  selectedStatus === status
                    ? "bg-[#E1D4C0] text-[#0A0A0A] font-bold border-[#E1D4C0]"
                    : "bg-white/[0.02] text-white/50 border-white/5 hover:text-white"
                }`}
              >
                {status}
              </button>
            ))}
          </div>
        </div>

        <div className="p-3.5 rounded-xl bg-black/40 border border-white/5 flex items-center justify-between text-xs text-white/60">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            <span>Invariant Guard: <strong className="text-white">Model Output &ne; Truth</strong> &bull; <strong className="text-white">Unknown Must Survive</strong></span>
          </div>
          <span className="text-[10px] font-mono text-white/40">Zero Certainty Fabrication Policy</span>
        </div>
      </div>

      {/* Intelligence Explorer Split-View */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left: Intelligence Items List */}
        <div className="lg:col-span-5 space-y-3">
          {filteredItems.map((item) => {
            const isSelected = activeItem?.id === item.id;
            return (
              <div
                key={item.id}
                onClick={() => setActiveItem(item)}
                className={`p-4 rounded-xl border transition-all cursor-pointer space-y-2 ${
                  isSelected
                    ? "bg-[#E1D4C0]/10 border-[#E1D4C0]/40 shadow-lg"
                    : "bg-[#111113]/60 border-white/5 hover:border-white/10 hover:bg-[#111113]"
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-mono text-white/40 uppercase tracking-wider">{item.category}</span>
                  <span className={`px-2 py-0.5 rounded text-[9px] font-mono border ${getStatusBadge(item.epistemicStatus)}`}>
                    {item.epistemicStatus.toUpperCase()}
                  </span>
                </div>
                <h4 className="text-sm font-medium text-white">{item.title}</h4>
                <p className="text-xs text-white/60 line-clamp-2 font-light">{item.summary}</p>
              </div>
            );
          })}
        </div>

        {/* Right: Deep Provenance & Tension Inspection Pane */}
        <div className="lg:col-span-7">
          {activeItem ? (
            <div className="p-6 rounded-2xl bg-[#111113]/90 border border-[#E1D4C0]/20 space-y-6 sticky top-24">
              
              {/* Header */}
              <div className="flex items-start justify-between gap-4 border-b border-white/5 pb-4">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] font-mono uppercase text-[#E1D4C0]">{activeItem.category}</span>
                    <span className="text-white/20 text-xs">•</span>
                    <span className={`px-2 py-0.5 rounded text-[9px] font-mono border ${getStatusBadge(activeItem.epistemicStatus)}`}>
                      {activeItem.epistemicStatus} ({Math.round(activeItem.confidenceScore * 100)}% Confidence)
                    </span>
                  </div>
                  <h3 className="text-base font-serif text-white font-medium">{activeItem.title}</h3>
                </div>
              </div>

              {/* Summary Description */}
              <div className="space-y-1.5">
                <span className="text-[10px] font-mono uppercase text-white/40 tracking-wider">Empirical Finding / Signal</span>
                <p className="text-xs text-white/90 leading-relaxed font-light">{activeItem.summary}</p>
              </div>

              {/* Evidence & Provenance Affordance */}
              <div className="p-4 rounded-xl bg-white/[0.02] border border-white/5 space-y-2">
                <span className="text-[10px] font-mono uppercase text-white/40 tracking-wider flex items-center gap-1.5">
                  <Database className="w-3 h-3 text-[#E1D4C0]" /> Provenance & Data Origin
                </span>
                <p className="text-xs text-[#E1D4C0] font-mono">{activeItem.evidenceSource}</p>
              </div>

              {/* Tension / Trade-off Alert if present */}
              {activeItem.tensionNote && (
                <div className="p-4 rounded-xl bg-amber-500/[0.05] border border-amber-500/20 space-y-1 text-xs">
                  <div className="flex items-center gap-1.5 text-amber-300 font-semibold text-[11px]">
                    <ShieldAlert className="w-3.5 h-3.5 text-amber-400" /> Strategic Tension / Physical Constraint
                  </div>
                  <p className="text-amber-200/80 font-light">{activeItem.tensionNote}</p>
                </div>
              )}

              {/* Actionable Implication for Generation */}
              <div className="p-4 rounded-xl bg-emerald-500/[0.04] border border-emerald-500/20 space-y-1 text-xs">
                <span className="text-[10px] font-mono uppercase text-emerald-400 tracking-wider">
                  &rarr; Downstream Synthesis Constraint
                </span>
                <p className="text-white/90 font-light">{activeItem.actionableImplication}</p>
              </div>

            </div>
          ) : (
            <div className="p-12 text-center text-white/40 border border-white/5 rounded-2xl bg-[#111113]/40">
              Select an intelligence signal to inspect evidence.
            </div>
          )}
        </div>

      </div>

    </div>
  );
}
