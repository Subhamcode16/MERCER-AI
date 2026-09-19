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
        <div className="fixed bottom-8 right-8 z-50 p-4 rounded-xl bg-card border border-emerald-500/40 text-emerald-600 dark:text-emerald-300 shadow-2xl flex items-center gap-3 text-xs animate-in slide-in-from-bottom-3 duration-200">
          <CheckCircle2 className="w-4 h-4 text-emerald-500 dark:text-emerald-400" />
          <span>{notification}</span>
        </div>
      )}

      {/* Header Banner */}
      <div className="flex items-center justify-between border-b border-border pb-4">
        <div className="space-y-0.5">
          <span className="text-[10px] font-mono tracking-widest uppercase text-primary font-bold">Review &amp; Authority</span>
          <h2 className="text-xl font-serif text-foreground font-normal">Creative &amp; Technical Sign-Off</h2>
        </div>

        <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-700 dark:text-amber-300 text-xs font-mono font-medium">
          <Lock className="w-3.5 h-3.5 text-amber-500 dark:text-amber-400" />
          <span>VYREN recommends &bull; You decide</span>
        </div>
      </div>

      {/* Primary Review Card */}
      <div className="p-8 rounded-3xl bg-card border border-border space-y-6 shadow-sm">
        
        {/* Review Outcome Headline */}
        <div className="space-y-1.5">
          <div className="flex items-center gap-2 text-xs text-muted-foreground">
            <Sparkles className="w-4 h-4 text-primary" />
            <span>VYREN reviewed this campaign set.</span>
          </div>
          <h3 className="text-2xl font-serif text-foreground font-light flex items-center gap-3">
            <span>Looks ready with one advisory issue.</span>
            {!humanApproved && !revisionRequested && (
              <span className="text-[10px] font-mono px-2.5 py-0.5 rounded-full bg-amber-500/15 text-amber-700 dark:text-amber-300 border border-amber-500/30 font-semibold">
                ACTION REQUIRED
              </span>
            )}
            {humanApproved && (
              <span className="text-[10px] font-mono px-2.5 py-0.5 rounded-full bg-emerald-500/15 text-emerald-700 dark:text-emerald-300 border border-emerald-500/30 font-semibold">
                APPROVED
              </span>
            )}
          </h3>
        </div>

        {/* What VYREN Noticed */}
        <div className="p-5 rounded-2xl bg-muted/40 border border-border space-y-3 text-xs">
          <span className="text-[10px] font-mono uppercase tracking-widest text-muted-foreground/70">
            What VYREN Noticed
          </span>
          <ul className="space-y-2 text-foreground/90 font-light">
            <li className="flex items-start gap-2.5">
              <span className="w-1.5 h-1.5 rounded-full bg-amber-500 mt-1.5 shrink-0" />
              <span>Shadow detail in the Banarasi brocade drape may compress slightly in physical 300 DPI CMYK print.</span>
            </li>
            <li className="flex items-start gap-2.5">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 mt-1.5 shrink-0" />
              <span>Digital social variations (9:16) and web editorial (4:5) are completely compliant with Visual DNA lighting tokens.</span>
            </li>
          </ul>
        </div>

        {/* What VYREN Recommends */}
        <div className="p-5 rounded-2xl bg-primary/5 border border-primary/20 space-y-1.5 text-xs">
          <span className="text-[10px] font-mono uppercase tracking-widest text-primary font-bold">
            VYREN Recommendation
          </span>
          <p className="text-foreground font-light text-[13px]">
            Run one print-safe tonal revision to lift shadow threshold for OOH &amp; Print while keeping digital hero assets unchanged.
          </p>
        </div>

        {/* Action Buttons: Explicit Human Approval Gate */}
        <div className="pt-4 border-t border-border flex flex-col sm:flex-row items-center justify-between gap-4">
          <button
            onClick={() => setShowFullAudit(true)}
            className="text-xs text-muted-foreground hover:text-foreground font-mono flex items-center gap-1 transition-colors"
          >
            <span>View full cryptographic audit &amp; policy proofs</span>
            <ChevronRight className="w-3.5 h-3.5" />
          </button>

          <div className="flex items-center gap-3 w-full sm:w-auto">
            <button
              onClick={handleRequestRevision}
              className="flex-1 sm:flex-none px-5 py-2.5 rounded-xl bg-accent/60 hover:bg-accent text-accent-foreground text-xs font-medium border border-border transition-colors flex items-center justify-center gap-2"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>Ask for Print-Safe Revision</span>
            </button>

            <button
              onClick={handleApprove}
              className="flex-1 sm:flex-none px-6 py-2.5 rounded-xl bg-primary text-primary-foreground font-semibold text-xs hover:opacity-90 transition-opacity flex items-center justify-center gap-2 shadow-sm"
            >
              <CheckCircle2 className="w-4 h-4" />
              <span>Approve All for Production</span>
            </button>
          </div>
        </div>

      </div>

      {/* Production Readiness Continuous Link */}
      {humanApproved && (
        <div className="p-6 rounded-3xl bg-card border border-emerald-500/30 flex flex-col sm:flex-row sm:items-center justify-between gap-4 animate-in slide-in-from-bottom-2 shadow-sm">
          <div className="space-y-0.5">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-500 dark:text-emerald-400" />
              <span className="text-foreground font-medium text-sm">Campaign approved for release</span>
            </div>
            <p className="text-xs text-muted-foreground font-light">All assets signed off by Elena Vance. Ready for multichannel deployment.</p>
          </div>

          <button
            onClick={() => onNavigateTab('ship')}
            className="px-5 py-2.5 rounded-xl bg-primary text-primary-foreground font-semibold text-xs hover:opacity-90 transition-opacity flex items-center gap-2 self-start sm:self-auto shrink-0 shadow-sm"
          >
            <span>Proceed to Ship</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>
      )}

      {/* Cryptographic Audit Drawer (Layer 3 Progressive Disclosure) */}
      {showFullAudit && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-background/80 backdrop-blur-md animate-in fade-in duration-150">
          <div className="w-full max-w-xl rounded-3xl bg-card border border-border p-6 space-y-5 shadow-2xl">
            <div className="flex items-center justify-between border-b border-border pb-3">
              <div className="flex items-center gap-2">
                <FileCheck className="w-4 h-4 text-emerald-500 dark:text-emerald-400" />
                <h3 className="text-base font-serif text-foreground">Cryptographic Verification &amp; Audit Trail</h3>
              </div>
              <button
                onClick={() => setShowFullAudit(false)}
                className="p-1 rounded-lg text-muted-foreground hover:text-foreground hover:bg-accent"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="space-y-3 text-xs font-mono text-muted-foreground">
              <div className="p-3 rounded-xl bg-muted/40 border border-border space-y-1">
                <span className="text-[10px] text-muted-foreground/70 uppercase">Decision Authority</span>
                <p className="text-foreground">Elena Vance (Human Owner) &bull; Role: Creative Director</p>
              </div>
              <div className="p-3 rounded-xl bg-muted/40 border border-border space-y-1">
                <span className="text-[10px] text-muted-foreground/70 uppercase">Ledger Merkle Root Hash</span>
                <p className="text-emerald-500 dark:text-emerald-400 text-[11px] truncate font-semibold">0x7f884a1e9b82c3d5f1a0e9d8c7b6a5f4e3d2c1b0a9f8e7d6c5b4a3f2e1d0c9b8</p>
              </div>
              <div className="p-3 rounded-xl bg-muted/40 border border-border space-y-1">
                <span className="text-[10px] text-muted-foreground/70 uppercase">Policy Invariant</span>
                <p className="text-foreground">No autonomous AI self-deployment permitted. Compliant.</p>
              </div>
            </div>

            <div className="pt-2 flex justify-end">
              <button
                onClick={() => setShowFullAudit(false)}
                className="px-4 py-2 rounded-xl bg-primary text-primary-foreground hover:opacity-90 text-xs font-medium shadow-sm"
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
