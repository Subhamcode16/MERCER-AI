"use client";

import React, { useState } from "react";
import { Sparkles, ArrowRight, CornerDownLeft, MessageSquare, Compass, X } from "lucide-react";
import type { CampaignStudioModel } from "@/lib/campaignStudioFixtures";

interface PersistentAskVyrenBarProps {
  campaign: CampaignStudioModel;
  activeStage: string;
  onOpenAskVyrenModal: (customQuery?: string) => void;
}

export function PersistentAskVyrenBar({
  campaign,
  activeStage,
  onOpenAskVyrenModal,
}: PersistentAskVyrenBarProps) {
  const [inputValue, setInputValue] = useState("");

  // Contextual suggestion chips depending on stage
  const getSuggestions = () => {
    switch (activeStage) {
      case "overview":
        return [
          "What does VYREN understand about this audience?",
          "What decisions need human sign-off?",
          "Explain the strategic opportunity",
        ];
      case "create":
        return [
          "Make it more editorial",
          "Show me something riskier",
          "Why did you recommend Modern Sovereign?",
          "Keep the lighting but change composition",
        ];
      case "review":
        return [
          "Why did you flag the shadow compression?",
          "Is this safe for 300 DPI CMYK print?",
          "Show policy compliance trace",
        ];
      case "ship":
        return [
          "Are all surfaces ready for export?",
          "What approval is blocking OOH Billboard?",
          "Download production manifest",
        ];
      case "learn":
        return [
          "Compare with our previous campaign",
          "What remains unknown after 30 days?",
          "Apply this learning to next campaign",
        ];
      default:
        return [
          "Make the hero more commanding",
          "Why did you recommend this?",
          "Show comparative territories",
        ];
    }
  };

  const suggestions = getSuggestions();

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && inputValue.trim()) {
      onOpenAskVyrenModal(inputValue.trim());
      setInputValue("");
    }
  };

  const handleChipClick = (suggestion: string) => {
    onOpenAskVyrenModal(suggestion);
  };

  return (
    <div className="fixed bottom-6 left-1/2 -translate-x-1/2 z-40 w-full max-w-3xl px-4 pointer-events-auto">
      <div className="rounded-2xl bg-card/90 backdrop-blur-xl border border-border shadow-[0_20px_50px_rgba(0,0,0,0.15)] dark:shadow-[0_20px_50px_rgba(0,0,0,0.7)] p-2.5 transition-all hover:border-primary/40 group">
        
        {/* Input Bar */}
        <div className="flex items-center gap-3 px-3 py-1.5 bg-muted/50 rounded-xl border border-border/40">
          <div className="w-7 h-7 rounded-lg bg-primary/15 text-primary flex items-center justify-center shrink-0 border border-primary/25">
            <Sparkles className="w-3.5 h-3.5 animate-pulse" />
          </div>

          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={`Ask VYREN anything about ${campaign.name}... (e.g. "Make it more editorial")`}
            className="flex-1 bg-transparent text-xs text-foreground placeholder:text-muted-foreground/60 focus:outline-none font-light"
          />

          <div className="flex items-center gap-2 shrink-0">
            {inputValue.trim() ? (
              <button
                onClick={() => {
                  onOpenAskVyrenModal(inputValue.trim());
                  setInputValue("");
                }}
                className="px-2.5 py-1 rounded-lg bg-primary text-primary-foreground text-[11px] font-semibold hover:opacity-90 transition-opacity flex items-center gap-1 shadow-sm"
              >
                <span>Ask</span>
                <CornerDownLeft className="w-3 h-3" />
              </button>
            ) : (
              <button
                onClick={() => onOpenAskVyrenModal()}
                className="px-2.5 py-1 rounded-lg bg-accent/60 hover:bg-accent text-accent-foreground text-[11px] font-medium transition-colors flex items-center gap-1.5 border border-border/50"
              >
                <MessageSquare className="w-3 h-3 text-primary" />
                <span>Ask VYREN</span>
              </button>
            )}
          </div>
        </div>

        {/* Suggestion Chips */}
        <div className="flex items-center gap-2 overflow-x-auto scrollbar-none pt-2 px-1">
          <span className="text-[9px] font-mono uppercase tracking-widest text-muted-foreground/60 shrink-0">
            Suggestions:
          </span>
          {suggestions.map((suggestion, idx) => (
            <button
              key={idx}
              onClick={() => handleChipClick(suggestion)}
              className="text-[10.5px] font-light text-muted-foreground hover:text-foreground bg-accent/40 hover:bg-accent border border-border/60 hover:border-primary/40 px-2.5 py-0.5 rounded-full whitespace-nowrap transition-all flex items-center gap-1 shrink-0"
            >
              <span>{suggestion}</span>
              <ArrowRight className="w-2.5 h-2.5 opacity-50 group-hover:opacity-100 text-primary" />
            </button>
          ))}
        </div>

      </div>
    </div>
  );
}
