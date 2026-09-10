"use client";

import React, { useState } from 'react';
import { ControlPanel } from './ControlPanel';
import { AssetCanvas } from './AssetCanvas';
import { IntelligenceFeed } from './IntelligenceFeed';
import { VisualDNAOverlay } from './VisualDNAOverlay';
import { MaterialPhysicsHeatmap } from './MaterialPhysicsHeatmap';
import { DigitalHumanTurntable } from './DigitalHumanTurntable';
import { AssetLineageDiff } from './AssetLineageDiff';
import { PolicyStatusHUD } from './PolicyStatusHUD';
import { Layers, Activity, UserCheck, GitCompare, EyeOff } from 'lucide-react';

interface StudioEditorLayoutProps {
  campaign: any;
  onGenerate: (modelId: string, params: any) => void;
  isGenerating: boolean;
}

export type ActiveHUDTool = "none" | "visual_dna" | "material_physics" | "digital_human" | "asset_diff";

export function StudioEditorLayout({ campaign, onGenerate, isGenerating }: StudioEditorLayoutProps) {
  const [activeModel, setActiveModel] = useState('Nano Banana Lite');
  const [activePose, setActivePose] = useState('Editorial Stance');
  const [activeScene, setActiveScene] = useState('Minimalist Beige Studio');
  const [activeHUD, setActiveHUD] = useState<ActiveHUDTool>("none");

  return (
    <div className="flex h-[calc(100vh-4rem)] w-full overflow-hidden bg-background text-foreground">
      {/* LEFT PANE: Control Panel */}
      <div className="w-80 flex-shrink-0 border-r border-border bg-card overflow-y-auto">
        <ControlPanel 
          campaign={campaign}
          activeModel={activeModel}
          setActiveModel={setActiveModel}
          activePose={activePose}
          setActivePose={setActivePose}
          activeScene={activeScene}
          setActiveScene={setActiveScene}
          onGenerate={() => onGenerate(activeModel, { pose: activePose, scene: activeScene })}
          isGenerating={isGenerating}
        />
      </div>

      {/* CENTER PANE: Asset Canvas with Active HUD Overlay */}
      <div className="flex-1 flex flex-col min-w-0 bg-background relative overflow-hidden">
        {/* HUD Switcher Toolbar */}
        <div className="absolute top-4 left-4 z-30 flex items-center gap-1.5 bg-black/80 backdrop-blur-md border border-white/10 rounded-lg p-1 text-xs">
          <button
            onClick={() => setActiveHUD("none")}
            className={`px-2.5 py-1 rounded flex items-center gap-1 transition-colors ${
              activeHUD === "none" ? "bg-neutral-800 text-white font-medium" : "text-neutral-400 hover:text-white"
            }`}
            title="Clean View"
          >
            <EyeOff className="w-3.5 h-3.5" />
            <span>Clean View</span>
          </button>
          <button
            onClick={() => setActiveHUD("visual_dna")}
            className={`px-2.5 py-1 rounded flex items-center gap-1 transition-colors ${
              activeHUD === "visual_dna" ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 font-medium" : "text-neutral-400 hover:text-white"
            }`}
            title="Visual DNA & Safe-Zones"
          >
            <Layers className="w-3.5 h-3.5 text-emerald-400" />
            <span>Visual DNA</span>
          </button>
          <button
            onClick={() => setActiveHUD("material_physics")}
            className={`px-2.5 py-1 rounded flex items-center gap-1 transition-colors ${
              activeHUD === "material_physics" ? "bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 font-medium" : "text-neutral-400 hover:text-white"
            }`}
            title="Physics Drape Heatmap"
          >
            <Activity className="w-3.5 h-3.5 text-cyan-400" />
            <span>Physics</span>
          </button>
          <button
            onClick={() => setActiveHUD("digital_human")}
            className={`px-2.5 py-1 rounded flex items-center gap-1 transition-colors ${
              activeHUD === "digital_human" ? "bg-purple-500/20 text-purple-300 border border-purple-500/30 font-medium" : "text-neutral-400 hover:text-white"
            }`}
            title="360 Turntable"
          >
            <UserCheck className="w-3.5 h-3.5 text-purple-400" />
            <span>360° Human</span>
          </button>
          <button
            onClick={() => setActiveHUD("asset_diff")}
            className={`px-2.5 py-1 rounded flex items-center gap-1 transition-colors ${
              activeHUD === "asset_diff" ? "bg-amber-500/20 text-amber-300 border border-amber-500/30 font-medium" : "text-neutral-400 hover:text-white"
            }`}
            title="Lineage Diff"
          >
            <GitCompare className="w-3.5 h-3.5 text-amber-400" />
            <span>Asset Diff</span>
          </button>
        </div>

        {/* Real-time Policy & Multi-Agent Telemetry */}
        <PolicyStatusHUD />

        {/* Dynamic Overlays */}
        {activeHUD === "visual_dna" && <VisualDNAOverlay />}
        {activeHUD === "material_physics" && <MaterialPhysicsHeatmap />}
        {activeHUD === "digital_human" && <DigitalHumanTurntable />}
        {activeHUD === "asset_diff" && <AssetLineageDiff />}

        {/* Main Canvas Base */}
        <AssetCanvas campaign={campaign} isGenerating={isGenerating} />
      </div>

      {/* RIGHT PANE: Intelligence Feed & Chat */}
      <div className="w-96 flex-shrink-0 border-l border-border bg-card flex flex-col">
        <IntelligenceFeed campaign={campaign} />
      </div>
    </div>
  );
}