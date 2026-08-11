"use client";
import React from 'react';
import { Loader2 } from 'lucide-react';

export function AssetCanvas({ campaign, isGenerating }: any) {
  const assets = campaign?.execution?.assets || {};
  const assetKeys = Object.keys(assets);
  
  return (
    <div className="flex-1 flex items-center justify-center p-8 bg-[#020202]">
      {isGenerating ? (
        <div className="flex flex-col items-center justify-center space-y-4">
          <Loader2 className="w-8 h-8 animate-spin text-muted-foreground" />
          <p className="text-sm text-muted-foreground tracking-widest uppercase font-mono">Synthesizing Assets...</p>
        </div>
      ) : assetKeys.length > 0 ? (
        <div className="grid grid-cols-2 gap-8 w-full max-w-5xl">
          {assetKeys.map((key) => {
            const asset = assets[key];
            return (
              <div key={key} className="relative aspect-[3/4] bg-card border border-border overflow-hidden group rounded-sm shadow-2xl">
                {asset.url ? (
                  <img src={asset.url} alt={key} className="w-full h-full object-cover" />
                ) : (
                  <div className="w-full h-full flex flex-col items-center justify-center">
                    <p className="text-xs text-muted-foreground tracking-widest uppercase">Pending Render</p>
                    <p className="text-xs text-muted-foreground mt-2 font-mono opacity-50">{key}</p>
                  </div>
                )}
                <div className="absolute bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-black/80 to-transparent opacity-0 group-hover:opacity-100 transition-opacity">
                  <p className="text-xs font-mono text-white/80 line-clamp-2">{asset.prompt}</p>
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <div className="text-center space-y-2">
          <div className="w-16 h-16 mx-auto border-2 border-dashed border-border rounded-full flex items-center justify-center">
            <span className="text-2xl opacity-20">+</span>
          </div>
          <p className="text-sm text-muted-foreground">Canvas empty. Awaiting ORRA Loop directives.</p>
        </div>
      )}
    </div>
  );
}