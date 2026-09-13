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
      <div className="rounded-2xl bg-[#121214]/92 backdrop-blur-xl border border-white/10 shadow-[0_20px_50px_rgba(0,0,0,0.7)] p-2.5 transition-all hover:border-[#E1D4C0]/30 group">
        
        {/* Input Bar */}
        <div className="flex items-center gap-3 px-3 py-1.5 bg-black/40 rounded-xl border border-white/5">
          <div className="w-7 h-7 rounded-lg bg-[#E1D4C0]/15 text-[#E1D4C0] flex items-center justify-center shrink-0 border border-[#E1D4C0]/20">
            <Sparkles className="w-3.5 h-3.5 animate-pulse" />
          </div>

          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={`Ask VYREN anything about ${campaign.name}... (e.g. "Make it more editorial")`}
            className="flex-1 bg-transparent text-xs text-white placeholder-white/40 focus:outline-none font-light"
          />

          <div className="flex items-center gap-2 shrink-0">
            {inputValue.trim() ? (
              <button
                onClick={() => {
                  onOpenAskVyrenModal(inputValue.trim());
                  setInputValue("");
                }}
                className="px-2.5 py-1 rounded-lg bg-[#E1D4C0] text-[#0A0A0A] text-[11px] font-semibold hover:opacity-90 transition-opacity flex items-center gap-1"
              >
                <span>Ask</span>
                <CornerDownLeft className="w-3 h-3" />
              </button>
            ) : (
              <button
                onClick={() => onOpenAskVyrenModal()}
                className="px-2.5 py-1 rounded-lg bg-white/[0.06] hover:bg-white/10 text-white/70 hover:text-white text-[11px] font-medium transition-colors flex items-center gap-1.5"
              >
                <MessageSquare className="w-3 h-3 text-[#E1D4C0]" />
                <span>Ask VYREN</span>
              </button>
            )}
          </div>
        </div>

        {/* Suggestion Chips */}
        <div className="flex items-center gap-2 overflow-x-auto scrollbar-none pt-2 px-1">
          <span className="text-[9px] font-mono uppercase tracking-widest text-white/30 shrink-0">
            Suggestions:
          </span>
          {suggestions.map((suggestion, idx) => (
            <button
              key={idx}
              onClick={() => handleChipClick(suggestion)}
              className="text-[10.5px] font-light text-white/60 hover:text-[#E1D4C0] bg-white/[0.03] hover:bg-white/[0.07] border border-white/5 hover:border-[#E1D4C0]/30 px-2.5 py-0.5 rounded-full whitespace-nowrap transition-all flex items-center gap-1 shrink-0"
            >
              <span>{suggestion}</span>
              <ArrowRight className="w-2.5 h-2.5 opacity-40 group-hover:opacity-100" />
            </button>
          ))}
        </div>

      </div>
    </div>
  );
}
