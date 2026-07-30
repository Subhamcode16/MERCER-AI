'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Sparkles, HelpCircle, ChevronUp } from 'lucide-react';

interface SynthesisControlsBarProps {
  onGenerate: (prompt: string, options: { ratio: string; count: number }) => void;
  isGenerating: boolean;
  disabled?: boolean;
}

export function SynthesisControlsBar({ onGenerate, isGenerating, disabled }: SynthesisControlsBarProps) {
  const [prompt, setPrompt] = useState('');
  const [ratio, setRatio] = useState('3:4');
  const [assetCount, setAssetCount] = useState(4);
  const [showRatioDropdown, setShowRatioDropdown] = useState(false);

  const ratios = ['3:4', '1:1', '4:3', '16:9', '9:16'];

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt.trim() || isGenerating || disabled) return;
    onGenerate(prompt, { ratio, count: assetCount });
  };

  return (
    <div className="fixed bottom-8 left-1/2 -translate-x-1/2 z-30 w-full max-w-3xl px-4">
      {/* Promotion bar above controls */}
      <div className="bg-gradient-to-r from-pink-500/20 via-purple-500/20 to-indigo-500/20 border border-white/10 rounded-t-2xl py-2 px-4 flex justify-between items-center text-[10px] tracking-wide text-zinc-300">
        <span className="font-semibold text-white uppercase tracking-wider bg-white/10 px-2 py-0.5 rounded-sm">Premium Feature</span>
        <span>Unlimited runs available on Creative Master plan</span>
        <button className="text-white hover:underline uppercase tracking-wider font-semibold">Upgrade</button>
      </div>

      {/* Main Console Bar */}
      <form 
        onSubmit={handleSubmit}
        className="bg-[#121212]/95 backdrop-blur-xl border-x border-b border-white/10 rounded-b-2xl p-3 flex items-center gap-3 shadow-2xl relative"
      >
        {/* Describe Scene Input */}
        <div className="flex-1 flex items-center gap-2 bg-zinc-900 border border-white/5 rounded-xl px-3 py-1.5 focus-within:border-white/20 transition-all">
          <Sparkles className="w-4 h-4 text-white/30 shrink-0" />
          <input
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Describe the scene you imagine..."
            className="flex-1 bg-transparent text-[13px] outline-none text-white placeholder-white/25 w-full"
            disabled={isGenerating || disabled}
          />
        </div>

        {/* Action pills */}
        <div className="flex items-center gap-1.5 shrink-0">
          
          {/* Model Selector Pill */}
          <div className="px-3 py-2 bg-zinc-900 border border-white/5 rounded-xl text-xs font-medium text-white/70 hover:bg-zinc-800 transition-colors cursor-pointer select-none">
            G Nano Banana Pro
          </div>

          {/* Aspect Ratio Selector Pill */}
          <div className="relative">
            <div 
              onClick={() => !isGenerating && !disabled && setShowRatioDropdown(!showRatioDropdown)}
              className="px-3 py-2 bg-zinc-900 border border-white/5 rounded-xl text-xs font-mono text-[#E1D4C0] hover:bg-zinc-800 transition-colors cursor-pointer select-none flex items-center gap-1"
            >
              <span>{ratio}</span>
              <ChevronUp className={`w-3.5 h-3.5 transition-transform ${showRatioDropdown ? 'rotate-180' : ''}`} />
            </div>

            <AnimatePresence>
              {showRatioDropdown && (
                <>
                  <div className="fixed inset-0 z-40" onClick={() => setShowRatioDropdown(false)} />
                  <motion.div
                    initial={{ opacity: 0, y: 10, scale: 0.95 }}
                    animate={{ opacity: 1, y: 0, scale: 1 }}
                    exit={{ opacity: 0, y: 10, scale: 0.95 }}
                    className="absolute bottom-full right-0 mb-2 bg-[#1C1C1C] border border-white/10 rounded-lg p-1.5 shadow-xl z-50 flex flex-col gap-1 w-24"
                  >
                    {ratios.map(r => (
                      <button
                        type="button"
                        key={r}
                        onClick={() => {
                          setRatio(r);
                          setShowRatioDropdown(false);
                        }}
                        className={`px-2 py-1 rounded text-xs text-left font-mono ${
                          ratio === r ? 'bg-[#E1D4C0] text-black font-semibold' : 'text-white/60 hover:bg-white/5 hover:text-white'
                        }`}
                      >
                        {r}
                      </button>
                    ))}
                  </motion.div>
                </>
              )}
            </AnimatePresence>
          </div>

          {/* Asset Count Pill [ - 1/4 + ] */}
          <div className="flex items-center bg-zinc-900 border border-white/5 rounded-xl overflow-hidden select-none">
            <button
              type="button"
              onClick={() => setAssetCount(prev => Math.max(1, prev - 1))}
              disabled={isGenerating || disabled}
              className="px-2.5 py-2 hover:bg-zinc-800 text-white/40 hover:text-white transition-colors disabled:opacity-30"
            >
              -
            </button>
            <span className="px-1 py-2 text-xs font-mono text-white/80 min-w-[28px] text-center">
              {assetCount}/4
            </span>
            <button
              type="button"
              onClick={() => setAssetCount(prev => Math.min(4, prev + 1))}
              disabled={isGenerating || disabled}
              className="px-2.5 py-2 hover:bg-zinc-800 text-white/40 hover:text-white transition-colors disabled:opacity-30"
            >
              +
            </button>
          </div>

          {/* Generate Button (2 Credits) */}
          <button
            type="submit"
            disabled={isGenerating || !prompt.trim() || disabled}
            className="px-4 py-2 bg-[#C6F840] hover:bg-[#b0df32] text-black font-semibold text-xs rounded-xl shadow-lg transition-colors flex items-center gap-1.5 disabled:opacity-50 disabled:cursor-not-allowed select-none uppercase tracking-wider font-mono"
          >
            <span>{isGenerating ? "Gen..." : "Generate"}</span>
            <span className="w-4 h-4 rounded-full bg-black/15 text-[10px] flex items-center justify-center font-bold">2</span>
          </button>

        </div>
      </form>
    </div>
  );
}
