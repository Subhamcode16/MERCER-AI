"use client";

import React, { useState } from "react";
import { 
  ShieldCheck, 
  CheckCircle2, 
  AlertTriangle, 
  Lock, 
  ArrowRight,
  MessageSquare,
  Sparkles,
  FileCheck,
  ChevronRight,
  X,
  RotateCcw
} from "lucide-react";
import type { CampaignStudioModel, StudioReview } from "@/lib/campaignStudioFixtures";

interface ReviewTabProps {
  campaign: CampaignStudioModel;
  onNavigateTab: (tab: any) => void;
}

export function ReviewTab({ campaign, onNavigateTab }: ReviewTabProps) {
  const [humanApproved, setHumanApproved] = useState(false);
  const [revisionRequested, setRevisionRequested] = useState(false);
  const [showFullAudit, setShowFullAudit] = useState(false);
  const [notification, setNotification] = useState<string | null>(null);

  const handleApprove = () => {
    setHumanApproved(true);
    setRevisionRequested(false);
    setNotification("Asset approved for production by Human Owner (Elena Vance).");
    setTimeout(() => setNotification(null), 4000);
  };

  const handleRequestRevision = () => {
    setRevisionRequested(true);
    setHumanApproved(false);
    setNotification("Print-safe revision requested. VYREN will synthesize shadow-lift variation.");
    setTimeout(() => setNotification(null), 4000);
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

      {/* Header Banner */}
      <div className="flex items-center justify-between border-b border-white/5 pb-4">
        <div className="space-y-0.5">
          <span className="text-[10px] font-mono tracking-widest uppercase text-[#E1D4C0]">Review &amp; Authority</span>
          <h2 className="text-xl font-serif text-white font-normal">Creative &amp; Technical Sign-Off</h2>
        </div>

        <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-300 text-xs font-mono">
          <Lock className="w-3.5 h-3.5 text-amber-400" />
          <span>VYREN recommends &bull; You decide</span>
        </div>
      </div>

      {/* Primary Review Card */}
      <div className="p-8 rounded-3xl bg-[#121214]/90 border border-white/10 space-y-6 shadow-2xl">
        
        {/* Review Outcome Headline */}
        <div className="space-y-1.5">
          <div className="flex items-center gap-2 text-xs text-white/50">
            <Sparkles className="w-4 h-4 text-[#E1D4C0]" />
            <span>VYREN reviewed this campaign set.</span>
          </div>
          <h3 className="text-2xl font-serif text-white font-light flex items-center gap-3">
            <span>Looks ready with one advisory issue.</span>
            {!humanApproved && !revisionRequested && (
              <span className="text-[10px] font-mono px-2.5 py-0.5 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/30">
                ACTION REQUIRED
              </span>
            )}
            {humanApproved && (
              <span className="text-[10px] font-mono px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                APPROVED
              </span>
            )}
          </h3>
        </div>

        {/* What VYREN Noticed */}
        <div className="p-5 rounded-2xl bg-white/[0.02] border border-white/5 space-y-3 text-xs">
          <span className="text-[10px] font-mono uppercase tracking-widest text-white/40">
            What VYREN Noticed
          </span>
          <ul className="space-y-2 text-white/80 font-light">
            <li className="flex items-start gap-2.5">
              <span className="w-1.5 h-1.5 rounded-full bg-amber-400 mt-1.5 shrink-0" />
              <span>Shadow detail in the Banarasi brocade drape may compress slightly in physical 300 DPI CMYK print.</span>
            </li>
            <li className="flex items-start gap-2.5">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 mt-1.5 shrink-0" />
              <span>Digital social variations (9:16) and web editorial (4:5) are completely compliant with Visual DNA lighting tokens.</span>
            </li>
          </ul>
        </div>

        {/* What VYREN Recommends */}
        <div className="p-5 rounded-2xl bg-[#E1D4C0]/5 border border-[#E1D4C0]/20 space-y-1.5 text-xs">
          <span className="text-[10px] font-mono uppercase tracking-widest text-[#E1D4C0]">
            VYREN Recommendation
          </span>
          <p className="text-white/90 font-light text-[13px]">
            Run one print-safe tonal revision to lift shadow threshold for OOH &amp; Print while keeping digital hero assets unchanged.
          </p>
        </div>

        {/* Action Buttons: Explicit Human Approval Gate */}
        <div className="pt-4 border-t border-white/5 flex flex-col sm:flex-row items-center justify-between gap-4">
          <button
            onClick={() => setShowFullAudit(true)}
            className="text-xs text-white/40 hover:text-white font-mono flex items-center gap-1 transition-colors"
          >
            <span>View full cryptographic audit &amp; policy proofs</span>
            <ChevronRight className="w-3.5 h-3.5" />
          </button>

          <div className="flex items-center gap-3 w-full sm:w-auto">
            <button
              onClick={handleRequestRevision}
              className="flex-1 sm:flex-none px-5 py-2.5 rounded-xl bg-white/[0.05] hover:bg-white/10 text-white text-xs font-medium border border-white/10 transition-colors flex items-center justify-center gap-2"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>Ask for Print-Safe Revision</span>
            </button>

            <button
              onClick={handleApprove}
              className="flex-1 sm:flex-none px-6 py-2.5 rounded-xl bg-[#E1D4C0] text-[#0A0A0A] font-semibold text-xs hover:opacity-90 transition-opacity flex items-center justify-center gap-2 shadow-lg"
            >
              <CheckCircle2 className="w-4 h-4" />
              <span>Approve All for Production</span>
            </button>
          </div>
        </div>

      </div>

      {/* Production Readiness Continuous Link */}
      {humanApproved && (
        <div className="p-6 rounded-3xl bg-gradient-to-r from-emerald-950/20 via-[#121214] to-black border border-emerald-500/30 flex flex-col sm:flex-row sm:items-center justify-between gap-4 animate-in slide-in-from-bottom-2">
          <div className="space-y-0.5">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span className="text-white font-medium text-sm">Campaign approved for release</span>
            </div>
            <p className="text-xs text-white/50 font-light">All assets signed off by Elena Vance. Ready for multichannel deployment.</p>
          </div>

          <button
            onClick={() => onNavigateTab('ship')}
            className="px-5 py-2.5 rounded-xl bg-[#E1D4C0] text-[#0A0A0A] font-semibold text-xs hover:opacity-90 transition-opacity flex items-center gap-2 self-start sm:self-auto shrink-0"
          >
            <span>Proceed to Ship</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>
      )}

      {/* Cryptographic Audit Drawer (Layer 3 Progressive Disclosure) */}
      {showFullAudit && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-md animate-in fade-in duration-150">
          <div className="w-full max-w-xl rounded-3xl bg-[#141416] border border-white/10 p-6 space-y-5 shadow-2xl">
            <div className="flex items-center justify-between border-b border-white/5 pb-3">
              <div className="flex items-center gap-2">
                <FileCheck className="w-4 h-4 text-emerald-400" />
                <h3 className="text-base font-serif text-white">Cryptographic Verification &amp; Audit Trail</h3>
              </div>
              <button
                onClick={() => setShowFullAudit(false)}
                className="p-1 rounded-lg text-white/40 hover:text-white hover:bg-white/5"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="space-y-3 text-xs font-mono text-white/70">
              <div className="p-3 rounded-xl bg-white/[0.02] border border-white/5 space-y-1">
                <span className="text-[10px] text-white/40 uppercase">Decision Authority</span>
                <p className="text-white">Elena Vance (Human Owner) &bull; Role: Creative Director</p>
              </div>
              <div className="p-3 rounded-xl bg-white/[0.02] border border-white/5 space-y-1">
                <span className="text-[10px] text-white/40 uppercase">Ledger Merkle Root Hash</span>
                <p className="text-emerald-400 text-[11px] truncate">0x7f884a1e9b82c3d5f1a0e9d8c7b6a5f4e3d2c1b0a9f8e7d6c5b4a3f2e1d0c9b8</p>
              </div>
              <div className="p-3 rounded-xl bg-white/[0.02] border border-white/5 space-y-1">
                <span className="text-[10px] text-white/40 uppercase">Policy Invariant</span>
                <p className="text-white">No autonomous AI self-deployment permitted. Compliant.</p>
              </div>
            </div>

            <div className="pt-2 flex justify-end">
              <button
                onClick={() => setShowFullAudit(false)}
                className="px-4 py-2 rounded-xl bg-white/10 hover:bg-white/20 text-white text-xs font-medium"
              >
                Close Audit View
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}
