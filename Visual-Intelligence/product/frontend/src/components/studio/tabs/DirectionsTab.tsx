"use client";

import React, { useState } from "react";
import { 
  Compass, 
  CheckCircle2, 
  Lock, 
  Sparkles, 
  ArrowRight,
  RefreshCw,
  Eye,
  Sliders,
  Check,
  ChevronDown,
  ChevronUp,
  MessageSquare
} from "lucide-react";
import type { CampaignStudioModel, CreativeDirection } from "@/lib/campaignStudioFixtures";

interface DirectionsTabProps {
  campaign: CampaignStudioModel;
  onSelectDirection: (directionId: string) => void;
  onNavigateTab: (tab: any) => void;
}

export function DirectionsTab({ campaign, onSelectDirection, onNavigateTab }: DirectionsTabProps) {
  // Step state within the Create flow: 'brief' | 'confirmation' | 'working' | 'reveal' | 'locked'
  const [createStep, setCreateStep] = useState<'confirmation' | 'working' | 'reveal' | 'locked'>('reveal');
  const [selectedDirectionId, setSelectedDirectionId] = useState<string>(
    campaign.directions.find(d => d.decisionStatus === 'selected')?.id || 'dir-01'
  );
  const [showWorkingDetails, setShowWorkingDetails] = useState(false);

  const selectedDirection = campaign.directions.find(d => d.id === selectedDirectionId) || campaign.directions[0];

  const handleConfirmUnderstanding = () => {
    setCreateStep('working');
    setTimeout(() => {
      setCreateStep('reveal');
    }, 1800);
  };

  const handleSelectAndLock = (dirId: string) => {
    setSelectedDirectionId(dirId);
    onSelectDirection(dirId);
    setCreateStep('locked');
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-200 pb-20 max-w-6xl mx-auto">
      
      {/* 1. Step Indicator / Journey Bar */}
      <div className="flex items-center justify-between border-b border-white/5 pb-4">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-xl bg-[#E1D4C0]/10 text-[#E1D4C0] border border-[#E1D4C0]/20 flex items-center justify-center">
            <Sparkles className="w-4 h-4" />
          </div>
          <div>
            <span className="text-[10px] font-mono tracking-widest uppercase text-[#E1D4C0]">Creative Discovery</span>
            <h2 className="text-lg font-serif text-white font-normal">Formulate &amp; Select Creative Direction</h2>
          </div>
        </div>

        <div className="flex items-center gap-2 text-xs font-mono">
          <button
            onClick={() => setCreateStep('confirmation')}
            className={`px-3 py-1 rounded-lg border transition-colors ${
              createStep === 'confirmation' ? 'bg-[#E1D4C0]/20 text-[#E1D4C0] border-[#E1D4C0]/30' : 'bg-white/[0.02] text-white/40 border-white/5'
            }`}
          >
            1. Understanding
          </button>
          <span className="text-white/20">&rarr;</span>
          <button
            onClick={() => setCreateStep('reveal')}
            className={`px-3 py-1 rounded-lg border transition-colors ${
              createStep === 'reveal' || createStep === 'locked' ? 'bg-[#E1D4C0]/20 text-[#E1D4C0] border-[#E1D4C0]/30' : 'bg-white/[0.02] text-white/40 border-white/5'
            }`}
          >
            2. Creative Reveal
          </button>
        </div>
      </div>

      {/* STEP 1: Understanding Confirmation */}
      {createStep === 'confirmation' && (
        <div className="p-8 rounded-3xl bg-[#121214]/90 border border-white/10 space-y-6 animate-in fade-in duration-300">
          <div className="space-y-1">
            <span className="text-[10px] font-mono tracking-widest uppercase text-[#E1D4C0]">Human Confirmation Gate</span>
            <h3 className="text-2xl font-serif text-white font-light">I think I understand.</h3>
            <p className="text-xs text-white/50 font-light">
              Here is my structured synthesis of your strategic intent and brand constraints:
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-light">
            <div className="p-4 rounded-xl bg-white/[0.02] border border-white/5 space-y-1">
              <span className="text-[10px] font-mono uppercase text-white/40">Objective</span>
              <p className="text-white/90">{campaign.objective}</p>
            </div>

            <div className="p-4 rounded-xl bg-white/[0.02] border border-white/5 space-y-1">
              <span className="text-[10px] font-mono uppercase text-white/40">Target Audience</span>
              <p className="text-white/90">{campaign.audience}</p>
            </div>

            <div className="p-4 rounded-xl bg-white/[0.02] border border-white/5 space-y-1">
              <span className="text-[10px] font-mono uppercase text-white/40">Primary Outcome</span>
              <p className="text-emerald-400 font-mono">+24% High-intent engagement &amp; purchase conversion</p>
            </div>

            <div className="p-4 rounded-xl bg-white/[0.02] border border-white/5 space-y-1">
              <span className="text-[10px] font-mono uppercase text-white/40">Creative Tension</span>
              <p className="text-amber-300/90">Heritage authenticity vs contemporary architectural restraint</p>
            </div>
          </div>

          <div className="pt-4 border-t border-white/5 flex items-center justify-between">
            <div className="text-xs text-white/50 font-light">
              Does this sound right?
            </div>
            <div className="flex items-center gap-3">
              <button
                onClick={() => setCreateStep('confirmation')}
                className="px-4 py-2 rounded-xl text-xs text-white/60 hover:text-white border border-white/5 hover:bg-white/5 transition-colors"
              >
                Change something
              </button>
              <button
                onClick={handleConfirmUnderstanding}
                className="px-5 py-2.5 rounded-xl bg-[#E1D4C0] text-[#0A0A0A] font-semibold text-xs hover:opacity-90 transition-opacity flex items-center gap-2"
              >
                <span>Yes, explore directions</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        </div>
      )}

      {/* STEP 1.5: Working State Progress */}
      {createStep === 'working' && (
        <div className="p-12 rounded-3xl bg-[#121214]/90 border border-white/10 text-center space-y-6 animate-in fade-in duration-300">
          <div className="w-12 h-12 rounded-2xl bg-[#E1D4C0]/10 text-[#E1D4C0] border border-[#E1D4C0]/20 flex items-center justify-center mx-auto animate-spin">
            <RefreshCw className="w-6 h-6" />
          </div>

          <div className="space-y-2">
            <h3 className="text-xl font-serif text-white">VYREN is formulating creative territories...</h3>
            <p className="text-xs text-white/40 font-light">Synthesizing Visual DNA tokens, textile physics, and comparative audience signals.</p>
          </div>

          <div className="max-w-md mx-auto space-y-2.5 text-xs text-left bg-black/40 p-4 rounded-2xl border border-white/5">
            <div className="flex items-center justify-between text-emerald-400">
              <span>Understanding the opportunity</span>
              <Check className="w-3.5 h-3.5" />
            </div>
            <div className="flex items-center justify-between text-emerald-400">
              <span>Reading brand context</span>
              <Check className="w-3.5 h-3.5" />
            </div>
            <div className="flex items-center justify-between text-emerald-400">
              <span>Checking Visual DNA</span>
              <Check className="w-3.5 h-3.5" />
            </div>
            <div className="flex items-center justify-between text-emerald-400">
              <span>Studying relevant evidence</span>
              <Check className="w-3.5 h-3.5" />
            </div>
            <div className="flex items-center justify-between text-[#E1D4C0] animate-pulse">
              <span>Exploring creative territories...</span>
              <RefreshCw className="w-3 h-3 animate-spin" />
            </div>
          </div>
        </div>
      )}

      {/* STEP 2: Creative Reveal — 3 Distinct Territories */}
      {(createStep === 'reveal' || createStep === 'locked') && (
        <div className="space-y-6 animate-in fade-in duration-300">
          
          <div className="space-y-1">
            <h3 className="text-2xl font-serif text-white font-light">
              I found three promising creative territories.
            </h3>
            <p className="text-xs text-white/50 font-light">
              Each territory represents a distinct visual hypothesis. Choose a direction to lock and develop into production assets.
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {campaign.directions.map((dir) => {
              const isSelected = selectedDirectionId === dir.id;

              return (
                <div
                  key={dir.id}
                  className={`rounded-3xl border p-7 flex flex-col justify-between space-y-6 transition-all duration-300 relative ${
                    isSelected
                      ? "bg-gradient-to-b from-[#18181C] to-[#101012] border-[#E1D4C0] shadow-[0_0_40px_rgba(225,212,192,0.15)] ring-1 ring-[#E1D4C0]/40"
                      : "bg-[#111113]/80 border-white/10 hover:border-white/20 hover:bg-[#141417]"
                  }`}
                >
                  {/* Top Badges */}
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-[10px] font-mono tracking-widest text-[#E1D4C0] font-bold">
                        TERRITORY {dir.tag}
                      </span>
                      <span className="text-[10px] font-mono px-2.5 py-0.5 rounded-full bg-[#E1D4C0]/10 text-[#E1D4C0] border border-[#E1D4C0]/20">
                        {dir.distinctivenessScore}% DISTINCT
                      </span>
                    </div>

                    <div>
                      <h4 className="text-2xl font-serif text-white font-normal">{dir.title}</h4>
                      <p className="text-xs text-white/50 font-light mt-1">{dir.subtitle}</p>
                    </div>
                  </div>

                  {/* Core Idea, Narrative & Visual World */}
                  <div className="space-y-4 text-xs font-light flex-1">
                    <div className="p-4 rounded-2xl bg-white/[0.02] border border-white/5 space-y-1">
                      <span className="text-[9px] font-mono uppercase text-[#E1D4C0]/70">The Idea</span>
                      <p className="text-white/90 leading-relaxed">{dir.coreIdea}</p>
                    </div>

                    <div className="p-4 rounded-2xl bg-white/[0.02] border border-white/5 space-y-1">
                      <span className="text-[9px] font-mono uppercase text-purple-300/70">Why VYREN believes it works</span>
                      <p className="text-white/70 leading-relaxed">{dir.audienceRationale || dir.narrative}</p>
                    </div>

                    <div className="space-y-1.5 pt-1">
                      <span className="text-[9px] font-mono uppercase text-white/40">Visual World</span>
                      <ul className="list-disc list-inside space-y-1 text-white/60 text-[11px]">
                        <li>Lighting: {dir.lighting}</li>
                        <li>Composition: {dir.composition}</li>
                        <li>Material: {dir.materialTreatment}</li>
                      </ul>
                    </div>

                    {dir.risksAndTensions.length > 0 && (
                      <div className="p-3 rounded-xl bg-amber-500/[0.04] border border-amber-500/20 text-[10.5px] text-amber-300/80 space-y-0.5">
                        <span className="font-semibold uppercase font-mono text-[9px]">Calculated Risk:</span>
                        <p className="font-light">{dir.risksAndTensions[0]}</p>
                      </div>
                    )}
                  </div>

                  {/* Primary Action Button */}
                  <div className="pt-2 border-t border-white/5">
                    {isSelected && createStep === 'locked' ? (
                      <div className="w-full py-3 rounded-2xl bg-[#E1D4C0] text-[#0A0A0A] font-bold text-xs flex items-center justify-center gap-2 shadow-lg">
                        <Lock className="w-3.5 h-3.5" />
                        <span>DIRECTION LOCKED</span>
                      </div>
                    ) : (
                      <button
                        onClick={() => handleSelectAndLock(dir.id)}
                        className={`w-full py-3 rounded-2xl font-semibold text-xs transition-all flex items-center justify-center gap-2 ${
                          isSelected
                            ? "bg-[#E1D4C0] text-[#0A0A0A] shadow-md hover:opacity-90"
                            : "bg-white/[0.06] hover:bg-white/10 text-white border border-white/10"
                        }`}
                      >
                        <CheckCircle2 className="w-3.5 h-3.5" />
                        <span>{isSelected ? "Lock & Develop This Direction" : "Select This Direction"}</span>
                      </button>
                    )}
                  </div>

                </div>
              );
            })}
          </div>

          {/* Locked Direction Continuous Transition Banner */}
          {createStep === 'locked' && (
            <div className="p-6 rounded-3xl bg-gradient-to-r from-emerald-950/20 via-[#141418] to-black border border-emerald-500/30 flex flex-col sm:flex-row sm:items-center justify-between gap-4 animate-in slide-in-from-bottom-3 duration-300">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                  <span className="text-white font-medium text-sm">
                    {selectedDirection.title} locked as campaign direction.
                  </span>
                </div>
                <p className="text-xs text-white/50 font-light">
                  VYREN is ready with 4 multi-surface asset studies: Hero, Detail, Social, and Editorial.
                </p>
              </div>

              <button
                onClick={() => onNavigateTab('visuals')}
                className="px-5 py-2.5 rounded-xl bg-[#E1D4C0] text-[#0A0A0A] font-semibold text-xs hover:opacity-90 transition-opacity flex items-center gap-2 shrink-0 self-start sm:self-auto"
              >
                <span>Enter Visual Development</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          )}

        </div>
      )}

    </div>
  );
}
