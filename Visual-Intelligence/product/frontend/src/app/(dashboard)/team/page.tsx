"use client";

import React, { useState } from "react";
import { 
  INITIAL_COWORKERS, 
  INITIAL_DEPARTMENTS, 
  INITIAL_ATTENTION_ITEMS, 
  INITIAL_ACTIVE_WORK, 
  INITIAL_CAMPAIGN_ROOMS, 
  INITIAL_HANDOFFS, 
  INITIAL_SKILLS, 
  INITIAL_ROUTINES, 
  INITIAL_ACTIVITY,
  type Coworker,
  type AttentionItem
} from "@/lib/teamFixtures";
import { TeamHeader, type TeamTabId } from "@/components/team/TeamHeader";
import { CoworkerDrawer } from "@/components/team/CoworkerDrawer";
import { MyTeamView } from "@/components/team/views/MyTeamView";
import { ActiveWorkView } from "@/components/team/views/ActiveWorkView";
import { CampaignRoomsView } from "@/components/team/views/CampaignRoomsView";
import { ConversationsView } from "@/components/team/views/ConversationsView";
import { HandoffsView } from "@/components/team/views/HandoffsView";
import { SkillsRoutinesView } from "@/components/team/views/SkillsRoutinesView";
import { TeamActivityView } from "@/components/team/views/TeamActivityView";

export default function TeamPage() {
  const [activeTab, setActiveTab] = useState<TeamTabId>('roster');
  const [coworkers, setCoworkers] = useState<Coworker[]>(INITIAL_COWORKERS);
  const [departments] = useState(INITIAL_DEPARTMENTS);
  const [attentionItems, setAttentionItems] = useState<AttentionItem[]>(INITIAL_ATTENTION_ITEMS);
  const [activeWork] = useState(INITIAL_ACTIVE_WORK);
  const [campaignRooms] = useState(INITIAL_CAMPAIGN_ROOMS);
  const [handoffs] = useState(INITIAL_HANDOFFS);
  const [skills] = useState(INITIAL_SKILLS);
  const [routines] = useState(INITIAL_ROUTINES);
  const [activity] = useState(INITIAL_ACTIVITY);

  // Selected Coworker for Drawer
  const [selectedCoworker, setSelectedCoworker] = useState<Coworker | null>(null);

  const handleResolveAttention = (itemId: string) => {
    setAttentionItems(prev => prev.filter(i => i.id !== itemId));
  };

  const handleSelectCoworkerById = (coworkerId: string) => {
    const found = coworkers.find(c => c.id === coworkerId);
    if (found) setSelectedCoworker(found);
  };

  return (
    <div className="min-h-screen bg-[#0A0A0A] text-white/90 flex flex-col">
      
      {/* Slide-over Coworker Detail & Chat Drawer */}
      <CoworkerDrawer
        coworker={selectedCoworker}
        onClose={() => setSelectedCoworker(null)}
      />

      {/* Team Top Header & Segmented Navigation */}
      <TeamHeader
        activeTab={activeTab}
        onSelectTab={(tab) => setActiveTab(tab)}
        departments={departments}
        attentionItems={attentionItems}
        onResolveAttention={handleResolveAttention}
      />

      {/* Main Viewport Content Area */}
      <div className="flex-1 p-6 lg:p-10 max-w-7xl mx-auto w-full">
        {activeTab === 'roster' && (
          <MyTeamView
            coworkers={coworkers}
            onSelectCoworker={(coworker) => setSelectedCoworker(coworker)}
            onOpenChat={(coworker) => setSelectedCoworker(coworker)}
          />
        )}

        {activeTab === 'active-work' && (
          <ActiveWorkView
            activeWork={activeWork}
            onSelectCoworkerById={handleSelectCoworkerById}
          />
        )}

        {activeTab === 'campaign-rooms' && (
          <CampaignRoomsView
            rooms={campaignRooms}
          />
        )}

        {activeTab === 'conversations' && (
          <ConversationsView
            coworkers={coworkers}
          />
        )}

        {activeTab === 'handoffs' && (
          <HandoffsView
            handoffs={handoffs}
          />
        )}

        {activeTab === 'skills-routines' && (
          <SkillsRoutinesView
            skills={skills}
            routines={routines}
          />
        )}

        {activeTab === 'activity' && (
          <TeamActivityView
            activity={activity}
          />
        )}
      </div>

    </div>
  );
}
