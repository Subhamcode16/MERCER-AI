"use client";

import React, { useState } from "react";
import Link from "next/link";
import { 
  Sparkles, 
  Plus, 
  FileText, 
  Layers, 
  History, 
  ArrowRight, 
  Target, 
  Compass, 
  CheckCircle2,
  Folder,
  Sliders,
  Eye,
  ShieldCheck,
  Send
} from "lucide-react";
import { 
  INITIAL_CAMPAIGN_FIXTURE, 
  type CampaignStudioModel 
} from "@/lib/campaignStudioFixtures";
import { 
  CampaignStudioHeader, 
  type StudioTabId 
} from "@/components/studio/CampaignStudioHeader";
import { AskVyrenModal } from "@/components/studio/AskVyrenModal";
import { PersistentAskVyrenBar } from "@/components/studio/PersistentAskVyrenBar";
import { OverviewTab } from "@/components/studio/tabs/OverviewTab";
import { DirectionsTab } from "@/components/studio/tabs/DirectionsTab";
import { VisualsTab } from "@/components/studio/tabs/VisualsTab";
import { ReviewTab } from "@/components/studio/tabs/ReviewTab";
import { ProductionTab } from "@/components/studio/tabs/ProductionTab";
import { OutcomesTab } from "@/components/studio/tabs/OutcomesTab";

export default function CampaignStudioPage() {
  // Campaign State: activeCampaign is loaded by default or null for empty state
  const [activeCampaign, setActiveCampaign] = useState<CampaignStudioModel | null>(INITIAL_CAMPAIGN_FIXTURE);
  const [activeTab, setActiveTab] = useState<StudioTabId>('overview');
  const [isAskVyrenOpen, setIsAskVyrenOpen] = useState(false);
  const [conversationalPrompt, setConversationalPrompt] = useState("");
  const [isCreateDrawerOpen, setIsCreateDrawerOpen] = useState(false);
  const [newCampaignName, setNewCampaignName] = useState("");
  const [newCampaignObjective, setNewCampaignObjective] = useState("");

  const handleStartFromConversationalPrompt = (promptText: string) => {
    if (!promptText.trim()) return;
    const newCamp: CampaignStudioModel = {
      ...INITIAL_CAMPAIGN_FIXTURE,
      id: `camp-${Date.now()}`,
      name: promptText.length > 40 ? promptText.slice(0, 40) + "..." : promptText,
      objective: promptText.trim(),
      status: "In Development",
      lockedDecisions: [],
      prioritizedActions: [
        {
          id: `act-${Date.now()}`,
          title: "Select primary Creative Direction",
          severity: "High",
          assignedTo: "Elena Vance (Human Owner)",
          dueTimeline: "Sprint 01"
        }
      ]
    };
    setActiveCampaign(newCamp);
    setActiveTab('create');
    setConversationalPrompt("");
  };

  const handleStartNewCampaign = () => {
    if (!newCampaignName.trim()) return;
    const newCamp: CampaignStudioModel = {
      ...INITIAL_CAMPAIGN_FIXTURE,
      id: `camp-${Date.now()}`,
      name: newCampaignName.trim(),
      objective: newCampaignObjective.trim() || "Define and launch high-impact omnichannel brand creative.",
      status: "In Development",
      lockedDecisions: [],
      prioritizedActions: [
        {
          id: `act-${Date.now()}`,
          title: "Select primary Creative Direction",
          severity: "High",
          assignedTo: "Elena Vance (Human Owner)",
          dueTimeline: "Sprint 01"
        }
      ]
    };
    setActiveCampaign(newCamp);
    setActiveTab('overview');
    setIsCreateDrawerOpen(false);
    setNewCampaignName("");
    setNewCampaignObjective("");
  };

  return (
    <div className="min-h-screen bg-[#0A0A0A] text-white/90 flex flex-col relative">
      
      {/* Ask VYREN Bounded Intelligence Modal */}
      {activeCampaign && (
        <AskVyrenModal
          isOpen={isAskVyrenOpen}
          onClose={() => setIsAskVyrenOpen(false)}
          campaign={activeCampaign}
        />
      )}

      {/* STATE 1: Empty / Genesis Hub ("What are we creating?") */}
      {!activeCampaign ? (
        <div className="flex-1 p-8 lg:p-12 flex flex-col justify-center max-w-5xl mx-auto w-full space-y-10 animate-in fade-in duration-300">
          
          {/* Hero Header */}
          <div className="space-y-3 text-center max-w-2xl mx-auto">
            <span className="text-[10px] font-mono tracking-widest uppercase text-[#E1D4C0] bg-[#E1D4C0]/10 border border-[#E1D4C0]/20 px-3 py-1 rounded-full">
              CAMPAIGN STUDIO &bull; CREATIVE OPERATING SYSTEM
            </span>
            <h1 className="text-3xl lg:text-5xl font-serif text-white font-light tracking-tight mt-2">
              What are we creating?
            </h1>
            <p className="text-xs text-white/50 font-light leading-relaxed">
              Tell VYREN your vision or launch goal in plain language. VYREN connects brand context, Visual DNA, audience intelligence, and multi-surface asset production.
            </p>
          </div>

          {/* Large Conversational Input Surface */}
          <div className="p-2 rounded-3xl bg-[#121214]/90 border border-white/10 shadow-2xl focus-within:border-[#E1D4C0]/50 transition-all max-w-3xl mx-auto w-full">
            <div className="flex items-center gap-3 p-4 bg-black/50 rounded-2xl border border-white/5">
              <div className="w-9 h-9 rounded-xl bg-[#E1D4C0]/10 text-[#E1D4C0] flex items-center justify-center shrink-0">
                <Sparkles className="w-5 h-5" />
              </div>

              <input
                type="text"
                value={conversationalPrompt}
                onChange={(e) => setConversationalPrompt(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && conversationalPrompt.trim()) {
                    handleStartFromConversationalPrompt(conversationalPrompt);
                  }
                }}
                placeholder="Tell VYREN what you want to make... (e.g. 'Launch our winter luxury bridal collection')"
                className="flex-1 bg-transparent text-sm text-white placeholder-white/40 focus:outline-none font-light"
              />

              <button
                onClick={() => handleStartFromConversationalPrompt(conversationalPrompt)}
                disabled={!conversationalPrompt.trim()}
                className="px-5 py-2.5 rounded-xl bg-[#E1D4C0] text-[#0A0A0A] font-semibold text-xs hover:opacity-90 disabled:opacity-40 transition-opacity flex items-center gap-1.5 shrink-0 shadow-lg"
              >
                <span>Develop</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>

            {/* Quick Inspiration Pills */}
            <div className="flex items-center gap-2 overflow-x-auto scrollbar-none px-4 py-2.5">
              <span className="text-[10px] font-mono text-white/30 uppercase tracking-widest shrink-0">Try:</span>
              {[
                "Launch our winter collection with contemporary heritage restraint",
                "Create a social campaign that makes the brand feel more architectural",
                "Explore high-intent Gen Z luxury bridal campaign",
              ].map((pill, idx) => (
                <button
                  key={idx}
                  onClick={() => handleStartFromConversationalPrompt(pill)}
                  className="text-[11px] text-white/60 hover:text-[#E1D4C0] bg-white/[0.03] hover:bg-white/[0.07] border border-white/5 hover:border-[#E1D4C0]/30 px-3 py-1 rounded-full whitespace-nowrap transition-all flex items-center gap-1 shrink-0"
                >
                  <span>{pill}</span>
                  <ArrowRight className="w-2.5 h-2.5 opacity-40" />
                </button>
              ))}
            </div>
          </div>

          {/* 4 Strategic Genesis Pathways */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-3xl mx-auto w-full">
            
            {/* Pathway 1: Start a Campaign */}
            <div 
              onClick={() => setIsCreateDrawerOpen(true)}
              className="p-5 rounded-2xl bg-[#111113]/80 border border-white/10 hover:border-[#E1D4C0]/40 transition-all cursor-pointer group space-y-2"
            >
              <div className="w-8 h-8 rounded-xl bg-[#E1D4C0]/10 text-[#E1D4C0] border border-[#E1D4C0]/20 flex items-center justify-center group-hover:scale-105 transition-transform">
                <Plus className="w-4 h-4" />
              </div>
              <div>
                <h3 className="text-sm font-serif text-white group-hover:text-[#E1D4C0] transition-colors">Start a Campaign</h3>
                <p className="text-xs text-white/50 font-light mt-0.5">
                  Full creative cycle from strategic objective through omnichannel delivery.
                </p>
              </div>
            </div>

            {/* Pathway 2: Start from a Creative Brief */}
            <div 
              onClick={() => {
                setActiveCampaign(INITIAL_CAMPAIGN_FIXTURE);
                setActiveTab('create');
              }}
              className="p-5 rounded-2xl bg-[#111113]/80 border border-white/10 hover:border-[#E1D4C0]/40 transition-all cursor-pointer group space-y-2"
            >
              <div className="w-8 h-8 rounded-xl bg-purple-500/10 text-purple-300 border border-purple-500/20 flex items-center justify-center group-hover:scale-105 transition-transform">
                <FileText className="w-4 h-4" />
              </div>
              <div>
                <h3 className="text-sm font-serif text-white group-hover:text-purple-300 transition-colors">Start from a Brief</h3>
                <p className="text-xs text-white/50 font-light mt-0.5">
                  Ingest agency brief and extract structured campaign intelligence.
                </p>
              </div>
            </div>

            {/* Pathway 3: Continue an Active Initiative */}
            <div 
              onClick={() => {
                setActiveCampaign(INITIAL_CAMPAIGN_FIXTURE);
                setActiveTab('overview');
              }}
              className="p-5 rounded-2xl bg-[#111113]/80 border border-white/10 hover:border-[#E1D4C0]/40 transition-all cursor-pointer group space-y-2"
            >
              <div className="w-8 h-8 rounded-xl bg-blue-500/10 text-blue-300 border border-blue-500/20 flex items-center justify-center group-hover:scale-105 transition-transform">
                <Layers className="w-4 h-4" />
              </div>
              <div>
                <h3 className="text-sm font-serif text-white group-hover:text-blue-300 transition-colors">Continue an Initiative</h3>
                <p className="text-xs text-white/50 font-light mt-0.5">
                  Resume active development on "The Modern Sovereign".
                </p>
              </div>
            </div>

            {/* Pathway 4: Explore Previous Campaign */}
            <div 
              onClick={() => {
                setActiveCampaign(INITIAL_CAMPAIGN_FIXTURE);
                setActiveTab('learn');
              }}
              className="p-5 rounded-2xl bg-[#111113]/80 border border-white/10 hover:border-[#E1D4C0]/40 transition-all cursor-pointer group space-y-2"
            >
              <div className="w-8 h-8 rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 flex items-center justify-center group-hover:scale-105 transition-transform">
                <History className="w-4 h-4" />
              </div>
              <div>
                <h3 className="text-sm font-serif text-white group-hover:text-emerald-400 transition-colors">Explore Previous Campaign</h3>
                <p className="text-xs text-white/50 font-light mt-0.5">
                  Review historical outcomes and learnings from past launches.
                </p>
              </div>
            </div>

          </div>

          {/* Creation Modal Drawer */}
          {isCreateDrawerOpen && (
            <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md">
              <div className="w-full max-w-md rounded-2xl bg-[#141416] border border-white/10 p-6 space-y-5 shadow-2xl">
                <div className="space-y-1">
                  <h3 className="text-base font-serif text-white">Initialize New Campaign</h3>
                  <p className="text-xs text-white/50 font-light">Set campaign name and primary strategic objective.</p>
                </div>

                <div className="space-y-3 text-xs">
                  <div className="space-y-1">
                    <label className="text-white/60 font-mono text-[10px] uppercase">Campaign Name</label>
                    <input
                      type="text"
                      value={newCampaignName}
                      onChange={(e) => setNewCampaignName(e.target.value)}
                      placeholder="e.g. Spring/Summer 2027: Raw Solitude"
                      className="w-full p-2.5 rounded-xl bg-white/[0.03] border border-white/10 text-white placeholder-white/30 focus:outline-none focus:border-[#E1D4C0]/50"
                    />
                  </div>

                  <div className="space-y-1">
                    <label className="text-white/60 font-mono text-[10px] uppercase">Strategic Objective</label>
                    <textarea
                      value={newCampaignObjective}
                      onChange={(e) => setNewCampaignObjective(e.target.value)}
                      placeholder="e.g. Expand high-end minimalist silk outerwear line into European luxury boutiques."
                      rows={3}
                      className="w-full p-2.5 rounded-xl bg-white/[0.03] border border-white/10 text-white placeholder-white/30 focus:outline-none focus:border-[#E1D4C0]/50"
                    />
                  </div>
                </div>

                <div className="flex items-center justify-end gap-2 pt-2">
                  <button
                    onClick={() => setIsCreateDrawerOpen(false)}
                    className="px-3.5 py-2 rounded-xl text-xs text-white/60 hover:text-white"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={handleStartNewCampaign}
                    className="px-4 py-2 rounded-xl bg-[#E1D4C0] text-[#0A0A0A] font-semibold text-xs hover:opacity-90 transition-opacity"
                  >
                    Initialize Workspace
                  </button>
                </div>
              </div>
            </div>
          )}

        </div>
      ) : (
        /* STATE 2: Canonical 5-Stage Creative Room Active Workspace */
        <div className="flex-1 flex flex-col">
          
          {/* Top Campaign Header & Crew HUD */}
          <CampaignStudioHeader
            campaign={activeCampaign}
            activeTab={activeTab}
            onSelectTab={(tab) => setActiveTab(tab)}
            onOpenAskVyren={() => setIsAskVyrenOpen(true)}
            onBackToOverview={() => setActiveCampaign(null)}
          />

          {/* Main Stage Viewport */}
          <div className="flex-1 p-6 lg:p-10 max-w-7xl mx-auto w-full">
            {activeTab === 'overview' && (
              <OverviewTab 
                campaign={activeCampaign} 
                onNavigateTab={(tab) => setActiveTab(tab)} 
              />
            )}

            {(activeTab === 'create' || activeTab === 'directions' || activeTab === 'intelligence') && (
              <DirectionsTab 
                campaign={activeCampaign}
                onSelectDirection={(dirId) => {
                  setActiveCampaign(prev => prev ? {
                    ...prev,
                    directions: prev.directions.map(d => d.id === dirId ? { ...d, decisionStatus: 'selected' } : { ...d, decisionStatus: 'draft' })
                  } : null);
                }}
                onNavigateTab={(tab) => setActiveTab(tab)}
              />
            )}

            {activeTab === 'visuals' && (
              <VisualsTab 
                campaign={activeCampaign} 
                onNavigateTab={(tab) => setActiveTab(tab)} 
              />
            )}

            {(activeTab === 'review' || activeTab === 'assets') && (
              <ReviewTab 
                campaign={activeCampaign} 
                onNavigateTab={(tab) => setActiveTab(tab)} 
              />
            )}

            {(activeTab === 'ship' || activeTab === 'production') && (
              <ProductionTab 
                campaign={activeCampaign} 
                onNavigateTab={(tab) => setActiveTab(tab)} 
              />
            )}

            {(activeTab === 'learn' || activeTab === 'outcomes') && (
              <OutcomesTab 
                campaign={activeCampaign} 
                onNavigateTab={(tab) => setActiveTab(tab)} 
              />
            )}
          </div>

          {/* Persistent Floating Creative Command Bar */}
          <PersistentAskVyrenBar
            campaign={activeCampaign}
            activeStage={activeTab}
            onOpenAskVyrenModal={(query) => {
              setIsAskVyrenOpen(true);
            }}
          />

        </div>
      )}

    </div>
  );
}
