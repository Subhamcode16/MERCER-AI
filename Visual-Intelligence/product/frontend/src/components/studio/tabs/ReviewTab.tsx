"use client";

import React, { useState } from "react";
import { 
  ShieldCheck, 
  CheckCircle2, 
  AlertTriangle, 
  XCircle, 
  MessageSquare, 
  ArrowRight,
  Lock,
  GitCommit,
  Sliders,
  Scale,
  Sparkles
} from "lucide-react";
import type { CampaignStudioModel, StudioReview } from "@/lib/campaignStudioFixtures";

interface ReviewTabProps {
  campaign: CampaignStudioModel;
  onNavigateTab: (tab: 'overview' | 'intelligence' | 'directions' | 'visuals' | 'assets' | 'review' | 'production' | 'outcomes') => void;
}

export function ReviewTab({ campaign, onNavigateTab }: ReviewTabProps) {
  const [reviews, setReviews] = useState<StudioReview[]>(campaign.reviews);
  const [activeReviewIndex, setActiveReviewIndex] = useState(0);
  const [commentText, setCommentText] = useState("");
  const [notification, setNotification] = useState<string | null>(null);

  const activeReview = reviews[activeReviewIndex] || reviews[0];
  const targetAsset = campaign.assets.find(a => a.id === activeReview?.assetId) || campaign.assets[2];

  const handleHumanDecision = (decision: 'Approved' | 'Revision Requested' | 'Rejected') => {
    setReviews(prev => prev.map((r, idx) => {
      if (idx === activeReviewIndex) {
        return {
          ...r,
          humanDecision: {
            state: decision,
            decisionMaker: campaign.humanOwner.name,
            timestamp: new Date().toISOString().replace('T', ' ').slice(0, 19) + ' UTC',
            instructions: commentText || `Human decision recorded: ${decision}`
          }
        };
      }
      return r;
    }));
    setNotification(`Human Decision Gate Executed: Asset marked as "${decision}".`);
    setCommentText("");
    setTimeout(() => setNotification(null), 4000);
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-200">
      
      {/* Toast Notification */}
      {notification && (
        <div className="fixed bottom-8 right-8 z-50 p-4 rounded-xl bg-[#141416] border border-emerald-500/40 text-emerald-300 shadow-2xl flex items-center gap-3 text-xs animate-in slide-in-from-bottom-3 duration-200">
          <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          <span>{notification}</span>
        </div>
      )}

      {/* Surface Header & Invariant Alert */}
      <div className="p-6 rounded-2xl bg-[#111113]/80 border border-white/10 space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <ShieldCheck className="w-5 h-5 text-[#E1D4C0]" />
              <h2 className="text-lg font-serif text-white font-medium">Review & Governance Gate</h2>
            </div>
            <p className="text-xs text-white/50 font-light">
              Strict architectural separation between automated AI Critique and explicit Human Decision Authority.
            </p>
          </div>

          <div className="px-3 py-1.5 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-300 text-xs font-mono flex items-center gap-2">
            <Lock className="w-3.5 h-3.5 text-amber-400" />
            <span>AI Critique &ne; Human Approval</span>
          </div>
        </div>
      </div>

      {/* Main Review Split: AI Scorecard vs Human Approval Terminal */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left: AI Automated Critique Scorecards */}
        <div className="lg:col-span-6 space-y-4">
          <div className="p-6 rounded-2xl bg-[#111113]/90 border border-white/10 space-y-6">
            
            <div className="flex items-center justify-between border-b border-white/5 pb-3">
              <div className="flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-purple-400" />
                <h3 className="text-sm font-medium text-white">AI Automated Critique Scorecard</h3>
              </div>
              <span className="text-[10px] font-mono text-purple-300 bg-purple-500/10 border border-purple-500/20 px-2 py-0.5 rounded">
                ADVISORY AUDIT
              </span>
            </div>

            {/* Metric Score Bars */}
            <div className="space-y-3 text-xs">
              <div className="space-y-1">
                <div className="flex justify-between font-mono text-[11px]">
                  <span className="text-white/60">Visual & Lighting Alignment</span>
                  <span className="text-[#E1D4C0] font-semibold">{activeReview.aiCritique.visualAlignment}%</span>
                </div>
                <div className="h-1.5 w-full bg-white/5 rounded-full overflow-hidden">
                  <div className="h-full bg-[#E1D4C0] rounded-full" style={{ width: `${activeReview.aiCritique.visualAlignment}%` }} />
                </div>
              </div>

              <div className="space-y-1">
                <div className="flex justify-between font-mono text-[11px]">
                  <span className="text-white/60">Brand DNA Adherence</span>
                  <span className="text-emerald-400 font-semibold">{activeReview.aiCritique.brandDnaScore}%</span>
                </div>
                <div className="h-1.5 w-full bg-white/5 rounded-full overflow-hidden">
                  <div className="h-full bg-emerald-400 rounded-full" style={{ width: `${activeReview.aiCritique.brandDnaScore}%` }} />
                </div>
              </div>

              <div className="space-y-1">
                <div className="flex justify-between font-mono text-[11px]">
                  <span className="text-white/60">Campaign Strategic Fit</span>
                  <span className="text-blue-400 font-semibold">{activeReview.aiCritique.campaignFit}%</span>
                </div>
                <div className="h-1.5 w-full bg-white/5 rounded-full overflow-hidden">
                  <div className="h-full bg-blue-400 rounded-full" style={{ width: `${activeReview.aiCritique.campaignFit}%` }} />
                </div>
              </div>

              <div className="space-y-1">
                <div className="flex justify-between font-mono text-[11px]">
                  <span className="text-white/60">Technical CMYK & Resolution Readiness</span>
                  <span className="text-purple-400 font-semibold">{activeReview.aiCritique.technicalReadiness}%</span>
                </div>
                <div className="h-1.5 w-full bg-white/5 rounded-full overflow-hidden">
                  <div className="h-full bg-purple-400 rounded-full" style={{ width: `${activeReview.aiCritique.technicalReadiness}%` }} />
                </div>
              </div>
            </div>

            {/* AI Detected Issues */}
            <div className="p-4 rounded-xl bg-white/[0.02] border border-white/5 space-y-2">
              <span className="text-[10px] font-mono uppercase text-white/40 tracking-wider flex items-center gap-1.5">
                <AlertTriangle className="w-3.5 h-3.5 text-amber-400" /> Detected Advisory Anomalies
              </span>
              <ul className="space-y-1.5 text-xs text-white/70">
                {activeReview.aiCritique.detectedIssues.map((issue, idx) => (
                  <li key={idx} className="flex items-start gap-2">
                    <span className="text-[#E1D4C0] font-mono">•</span>
                    <span className="font-light">{issue}</span>
                  </li>
                ))}
              </ul>
            </div>

          </div>
        </div>

        {/* Right: Human Decision Terminal */}
        <div className="lg:col-span-6 space-y-4">
          <div className="p-6 rounded-2xl bg-[#111113]/90 border border-[#E1D4C0]/30 space-y-6">
            
            <div className="flex items-center justify-between border-b border-white/5 pb-3">
              <div className="flex items-center gap-2">
                <Lock className="w-4 h-4 text-[#E1D4C0]" />
                <h3 className="text-sm font-medium text-white">Human Approval Terminal</h3>
              </div>
              <span className="text-[10px] font-mono text-amber-300 bg-amber-500/10 border border-amber-500/20 px-2 py-0.5 rounded">
                SOLE EXECUTION AUTHORITY
              </span>
            </div>

            {/* Target Asset Preview Info */}
            <div className="p-4 rounded-xl bg-white/[0.02] border border-white/5 space-y-1 text-xs">
              <span className="text-[10px] font-mono text-white/40 uppercase">Specimen Under Review</span>
              <h4 className="text-sm font-medium text-white">{targetAsset.title}</h4>
              <p className="text-[11px] font-mono text-white/50">{targetAsset.channel} &bull; {targetAsset.version} &bull; {targetAsset.specSummary}</p>
            </div>

            {/* Current Human Decision State */}
            <div className="p-4 rounded-xl bg-black/60 border border-white/5 space-y-1 text-xs">
              <span className="text-[10px] font-mono uppercase text-white/40">Current Decision State</span>
              <div className="flex items-center gap-2">
                <span className="text-base font-medium text-white">{activeReview.humanDecision.state}</span>
                {activeReview.humanDecision.decisionMaker && (
                  <span className="text-[10px] font-mono text-emerald-400">by {activeReview.humanDecision.decisionMaker}</span>
                )}
              </div>
              {activeReview.humanDecision.instructions && (
                <p className="text-[11px] text-white/60 font-light italic pt-1">
                  "{activeReview.humanDecision.instructions}"
                </p>
              )}
            </div>

            {/* Comment / Revision Note Input */}
            <div className="space-y-2">
              <label className="text-[10px] font-mono uppercase text-white/40 tracking-wider">
                Human Directive / Review Comment:
              </label>
              <textarea
                value={commentText}
                onChange={(e) => setCommentText(e.target.value)}
                placeholder="Enter revision requirements or approval rationale..."
                rows={3}
                className="w-full p-3 rounded-xl bg-white/[0.02] border border-white/10 text-xs text-white placeholder-white/30 focus:outline-none focus:border-[#E1D4C0]/50"
              />
            </div>

            {/* Action Buttons: Explicit Human Gate */}
            <div className="grid grid-cols-3 gap-3 pt-2">
              <button
                onClick={() => handleHumanDecision('Approved')}
                className="py-2.5 rounded-xl bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-300 border border-emerald-500/40 text-xs font-semibold flex items-center justify-center gap-1.5 transition-colors shadow-lg"
              >
                <CheckCircle2 className="w-3.5 h-3.5" />
                <span>Approve</span>
              </button>

              <button
                onClick={() => handleHumanDecision('Revision Requested')}
                className="py-2.5 rounded-xl bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 border border-amber-500/40 text-xs font-semibold flex items-center justify-center gap-1.5 transition-colors"
              >
                <AlertTriangle className="w-3.5 h-3.5" />
                <span>Revise</span>
              </button>

              <button
                onClick={() => handleHumanDecision('Rejected')}
                className="py-2.5 rounded-xl bg-rose-500/20 hover:bg-rose-500/30 text-rose-300 border border-rose-500/40 text-xs font-semibold flex items-center justify-center gap-1.5 transition-colors"
              >
                <XCircle className="w-3.5 h-3.5" />
                <span>Reject</span>
              </button>
            </div>

          </div>
        </div>

      </div>

    </div>
  );
}
