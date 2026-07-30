'use client';

import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Lightbulb, Check, X } from 'lucide-react';
import { cn } from '@/lib/utils';

export interface HeuristicRecommendationData {
  id: string;
  suggestion: string;
  rationale: string;
  affectedParameters: Record<string, any>;
}

interface HeuristicRecommendationProps {
  recommendation: HeuristicRecommendationData | null;
  onAccept: (rec: HeuristicRecommendationData) => void;
  onIgnore: (rec: HeuristicRecommendationData) => void;
  className?: string;
}

export function HeuristicRecommendation({ recommendation, onAccept, onIgnore, className }: HeuristicRecommendationProps) {
  return (
    <AnimatePresence>
      {recommendation && (
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: 20 }}
          className={cn(
            "bg-indigo-950/30 border border-indigo-900/50 rounded-lg overflow-hidden flex flex-col",
            className
          )}
        >
          <div className="p-3 flex items-start gap-3">
            <div className="bg-indigo-900/40 p-1.5 rounded-md shrink-0">
              <Lightbulb className="w-4 h-4 text-indigo-400" />
            </div>
            
            <div className="flex-1 space-y-1 mt-0.5">
              <h4 className="text-sm font-medium text-indigo-300">Creative Suggestion</h4>
              <p className="text-sm text-zinc-300">
                {recommendation.suggestion}
              </p>
              <p className="text-xs text-zinc-500 italic">
                {recommendation.rationale}
              </p>
            </div>
          </div>
          
          <div className="flex border-t border-indigo-900/50 divide-x divide-indigo-900/50">
            <button
              onClick={() => onIgnore(recommendation)}
              className="flex-1 py-2 flex items-center justify-center gap-2 text-xs font-medium text-zinc-400 hover:text-zinc-200 hover:bg-white/5 transition-colors"
            >
              <X className="w-3.5 h-3.5" />
              Ignore
            </button>
            <button
              onClick={() => onAccept(recommendation)}
              className="flex-1 py-2 flex items-center justify-center gap-2 text-xs font-medium text-indigo-400 hover:text-indigo-300 hover:bg-indigo-500/10 transition-colors"
            >
              <Check className="w-3.5 h-3.5" />
              Apply Tweak
            </button>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
