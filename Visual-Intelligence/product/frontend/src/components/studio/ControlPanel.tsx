"use client";
import React from 'react';
import { Settings2, Camera, Layers, Wand2 } from 'lucide-react';

export function ControlPanel({ campaign, activeModel, setActiveModel, activePose, setActivePose, activeScene, setActiveScene, onGenerate, isGenerating }: any) {
  return (
    <div className="flex flex-col h-full">
      <div className="p-4 border-b border-border flex items-center gap-2">
        <Settings2 className="w-5 h-5 text-muted-foreground" />
        <h2 className="text-sm font-medium tracking-wide uppercase">Director Controls</h2>
      </div>
      
      <div className="p-6 space-y-8 flex-1">
        {/* Model Selection */}
        <div className="space-y-3">
          <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Model Pipeline</label>
          <select 
            className="w-full bg-background border border-border rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-ring"
            value={activeModel}
            onChange={(e) => setActiveModel(e.target.value)}
          >
            <option value="Nano Banana Lite">Nano Banana Lite (Normal)</option>
            <option value="Nano Banana Pro">Nano Banana Pro (Pro)</option>
            <option value="Seedream V5 pro">Seedream V5 Pro (Pro)</option>
            <option value="GPT Image 2">GPT Image 2 (Normal)</option>
            <option value="Recraft V4.1 Pro">Recraft V4.1 Pro (Pro)</option>
          </select>
        </div>

        {/* Pose Selection */}
        <div className="space-y-3">
          <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Subject Pose</label>
          <div className="grid grid-cols-2 gap-2">
            {['Editorial Stance', 'Back Glance', 'Dynamic Walk', 'Seated Profile'].map((pose) => (
              <button
                key={pose}
                onClick={() => setActivePose(pose)}
                className={`text-xs px-3 py-2 border rounded-md transition-colors ${activePose === pose ? 'bg-primary text-primary-foreground border-primary' : 'border-border hover:bg-muted text-muted-foreground'}`}
              >
                {pose}
              </button>
            ))}
          </div>
        </div>

        {/* Scene Selection */}
        <div className="space-y-3">
          <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Set Design</label>
          <select 
            className="w-full bg-background border border-border rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-ring"
            value={activeScene}
            onChange={(e) => setActiveScene(e.target.value)}
          >
            <option value="Minimalist Beige Studio">Minimalist Beige Studio</option>
            <option value="Urban Concrete">Urban Concrete</option>
            <option value="Sunset Desert">Sunset Desert</option>
            <option value="Neon Cyberpunk">Neon Cyberpunk</option>
          </select>
        </div>
      </div>
      
      <div className="p-4 border-t border-border mt-auto">
        <button 
          onClick={onGenerate}
          disabled={isGenerating}
          className="w-full bg-primary text-primary-foreground py-3 rounded-md font-semibold text-sm uppercase tracking-widest hover:opacity-90 disabled:opacity-50 flex items-center justify-center gap-2 transition-all"
        >
          {isGenerating ? 'Rendering...' : 'Shoot Campaign'}
          <Camera className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}