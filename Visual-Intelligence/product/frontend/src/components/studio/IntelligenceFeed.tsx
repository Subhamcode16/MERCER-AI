"use client";
import React, { useState } from 'react';
import { Brain, Bot, Send, Sparkles } from 'lucide-react';

export function IntelligenceFeed({ campaign }: any) {
  const [chatInput, setChatInput] = useState("");
  const memoryStream = campaign?.memory_stream || [];

  return (
    <div className="flex flex-col h-full bg-card">
      <div className="p-4 border-b border-border flex items-center gap-2">
        <Brain className="w-5 h-5 text-primary" />
        <h2 className="text-sm font-medium tracking-wide uppercase">OS Intelligence</h2>
      </div>
      
      {/* Node Stream */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {memoryStream.map((node: any, i: number) => (
          <div key={i} className="bg-background border border-border rounded-md p-3 relative t-stagger-line">
            <div className="flex items-center gap-2 mb-2">
              <Sparkles className="w-3 h-3 text-muted-foreground" />
              <span className="text-[10px] uppercase tracking-widest text-muted-foreground font-mono">{node.type}</span>
            </div>
            <p className="text-sm text-foreground/90 font-serif leading-relaxed">
              {node.content}
            </p>
          </div>
        ))}
      </div>
      
      {/* Agent Chat */}
      <div className="p-4 border-t border-border bg-background/50">
        <div className="flex items-center gap-2 mb-3">
          <Bot className="w-4 h-4 text-muted-foreground" />
          <span className="text-xs text-muted-foreground">Art Director Agent</span>
        </div>
        <div className="relative">
          <input
            type="text"
            value={chatInput}
            onChange={(e) => setChatInput(e.target.value)}
            placeholder="Instruct the OS (e.g. 'Make it moodier')..."
            className="w-full bg-background border border-border rounded-md pl-3 pr-10 py-2.5 text-sm focus:outline-none focus:border-primary font-mono text-xs"
          />
          <button className="absolute right-2 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-primary transition-colors">
            <Send className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}