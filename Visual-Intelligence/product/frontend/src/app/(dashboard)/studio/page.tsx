"use client";

import React, { useState, useEffect } from "react";
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
  ShieldCheck
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
import { OverviewTab } from "@/components/studio/tabs/OverviewTab";
import { IntelligenceTab } from "@/components/studio/tabs/IntelligenceTab";
import { DirectionsTab } from "@/components/studio/tabs/DirectionsTab";
import { VisualsTab } from "@/components/studio/tabs/VisualsTab";
import { AssetsTab } from "@/components/studio/tabs/AssetsTab";
import { ReviewTab } from "@/components/studio/tabs/ReviewTab";
import { ProductionTab } from "@/components/studio/tabs/ProductionTab";
import { OutcomesTab } from "@/components/studio/tabs/OutcomesTab";

export default function CampaignStudioPage() {
  // Campaign State: activeCampaign is loaded by default or null for empty state
  const [activeCampaign, setActiveCampaign] = useState<CampaignStudioModel | null>(INITIAL_CAMPAIGN_FIXTURE);
  const [activeTab, setActiveTab] = useState<StudioTabId>('overview');
  const [isAskVyrenOpen, setIsAskVyrenOpen] = useState(false);
  const [isCreateDrawerOpen, setIsCreateDrawerOpen] = useState(false);
  const [newCampaignName, setNewCampaignName] = useState("");
  const [newCampaignObjective, setNewCampaignObjective] = useState("");

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
    <div className="min-h-screen bg-[#0A0A0A] text-white/90 flex flex-col">
      
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
          <div className="space-y-2 text-center max-w-2xl mx-auto">
            <span className="text-[10px] font-mono tracking-widest uppercase text-[#E1D4C0] bg-[#E1D4C0]/10 border border-[#E1D4C0]/20 px-3 py-1 rounded-full">
              CAMPAIGN STUDIO &bull; CREATIVE WORKSPACE
            </span>
            <h1 className="text-3xl lg:text-4xl font-serif text-white font-light tracking-tight mt-2">
              What are we creating?
            </h1>
            <p className="text-xs text-white/50 font-light leading-relaxed">
              Campaign Studio is VYREN's end-to-end creative operating system. Formulate strategic intelligence, explore comparative directions, and synthesize production-ready assets.
            </p>
          </div>

          {/* 4 Strategic Genesis Pathways */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            
            {/* Pathway 1: Start a Campaign */}
            <div 
              onClick={() => setIsCreateDrawerOpen(true)}
              className="p-6 rounded-2xl bg-[#111113]/80 border border-white/10 hover:border-[#E1D4C0]/40 transition-all cursor-pointer group space-y-3"
            >
              <div className="w-10 h-10 rounded-xl bg-[#E1D4C0]/10 text-[#E1D4C0] border border-[#E1D4C0]/20 flex items-center justify-center group-hover:scale-105 transition-transform">
                <Plus className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-base font-serif text-white group-hover:text-[#E1D4C0] transition-colors">Start a Campaign</h3>
                <p className="text-xs text-white/50 font-light mt-0.5">
                  Launch a full creative cycle from strategic objective through omnichannel delivery.
                </p>
              </div>
            </div>

            {/* Pathway 2: Start from a Creative Brief */}
            <div 
              onClick={() => {
                setActiveCampaign(INITIAL_CAMPAIGN_FIXTURE);
                setActiveTab('intelligence');
              }}
              className="p-6 rounded-2xl bg-[#111113]/80 border border-white/10 hover:border-[#E1D4C0]/40 transition-all cursor-pointer group space-y-3"
            >
              <div className="w-10 h-10 rounded-xl bg-purple-500/10 text-purple-300 border border-purple-500/20 flex items-center justify-center group-hover:scale-105 transition-transform">
                <FileText className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-base font-serif text-white group-hover:text-purple-300 transition-colors">Start from a Brief</h3>
                <p className="text-xs text-white/50 font-light mt-0.5">
                  Ingest an existing agency creative brief and extract structured campaign intelligence.
                </p>
              </div>
            </div>

            {/* Pathway 3: Continue an Active Initiative */}
            <div 
              onClick={() => {
                setActiveCampaign(INITIAL_CAMPAIGN_FIXTURE);
                setActiveTab('overview');
              }}
              className="p-6 rounded-2xl bg-[#111113]/80 border border-white/10 hover:border-[#E1D4C0]/40 transition-all cursor-pointer group space-y-3"
            >
              <div className="w-10 h-10 rounded-xl bg-blue-500/10 text-blue-300 border border-blue-500/20 flex items-center justify-center group-hover:scale-105 transition-transform">
                <Layers className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-base font-serif text-white group-hover:text-blue-300 transition-colors">Continue an Initiative</h3>
                <p className="text-xs text-white/50 font-light mt-0.5">
                  Resume active development on "Autumn/Winter 2026: The Modern Sovereign".
                </p>
              </div>
            </div>

            {/* Pathway 4: Explore Previous Campaign */}
            <div 
              onClick={() => {
                setActiveCampaign(INITIAL_CAMPAIGN_FIXTURE);
                setActiveTab('outcomes');
              }}
              className="p-6 rounded-2xl bg-[#111113]/80 border border-white/10 hover:border-[#E1D4C0]/40 transition-all cursor-pointer group space-y-3"
            >
              <div className="w-10 h-10 rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 flex items-center justify-center group-hover:scale-105 transition-transform">
                <History className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-base font-serif text-white group-hover:text-emerald-400 transition-colors">Explore Previous Campaign</h3>
                <p className="text-xs text-white/50 font-light mt-0.5">
                  Review historical outcome attribution and organizational learnings from past launches.
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
        /* STATE 2: Full 8-Tab Campaign Studio Active Workspace */
        <div className="flex-1 flex flex-col">
          
          {/* Top Campaign Header & Crew HUD */}
          <CampaignStudioHeader
            campaign={activeCampaign}
            activeTab={activeTab}
            onSelectTab={(tab) => setActiveTab(tab)}
            onOpenAskVyren={() => setIsAskVyrenOpen(true)}
            onBackToOverview={() => setActiveCampaign(null)}
          />

          {/* Tab Subsystem Workspace Viewport */}
          <div className="flex-1 p-6 lg:p-10 max-w-7xl mx-auto w-full">
            {activeTab === 'overview' && (
              <OverviewTab 
                campaign={activeCampaign} 
                onNavigateTab={(tab) => setActiveTab(tab)} 
              />
            )}

            {activeTab === 'intelligence' && (
              <IntelligenceTab 
                campaign={activeCampaign} 
              />
            )}

            {activeTab === 'directions' && (
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

            {activeTab === 'assets' && (
              <AssetsTab 
                campaign={activeCampaign} 
                onNavigateTab={(tab) => setActiveTab(tab)}
              />
            )}

            {activeTab === 'review' && (
              <ReviewTab 
                campaign={activeCampaign} 
                onNavigateTab={(tab) => setActiveTab(tab)}
              />
            )}

            {activeTab === 'production' && (
              <ProductionTab 
                campaign={activeCampaign} 
                onNavigateTab={(tab) => setActiveTab(tab)}
              />
            )}

            {activeTab === 'outcomes' && (
              <OutcomesTab 
                campaign={activeCampaign} 
              />
            )}
          </div>

        </div>
      )}

    </div>
  );
}
