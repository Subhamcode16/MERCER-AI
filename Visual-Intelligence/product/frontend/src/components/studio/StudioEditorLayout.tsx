"use client";
import React, { useState } from 'react';
import { ControlPanel } from './ControlPanel';
import { AssetCanvas } from './AssetCanvas';
import { IntelligenceFeed } from './IntelligenceFeed';

interface StudioEditorLayoutProps {
  campaign: any;
  onGenerate: (modelId: string, params: any) => void;
  isGenerating: boolean;
}

export function StudioEditorLayout({ campaign, onGenerate, isGenerating }: StudioEditorLayoutProps) {
  const [activeModel, setActiveModel] = useState('Nano Banana Lite');
  const [activePose, setActivePose] = useState('Editorial Stance');
  const [activeScene, setActiveScene] = useState('Minimalist Beige Studio');
  
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

      {/* CENTER PANE: Asset Canvas */}
      <div className="flex-1 flex flex-col min-w-0 bg-background relative">
        <AssetCanvas campaign={campaign} isGenerating={isGenerating} />
      </div>

      {/* RIGHT PANE: Intelligence Feed & Chat */}
      <div className="w-96 flex-shrink-0 border-l border-border bg-card flex flex-col">
        <IntelligenceFeed campaign={campaign} />
      </div>
    </div>
  );
}