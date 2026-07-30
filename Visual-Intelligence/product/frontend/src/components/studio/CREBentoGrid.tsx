'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { Camera, Tag, LayoutTemplate, Sparkles, TrendingUp } from 'lucide-react';
import { cn } from '@/lib/utils';

export interface CREScores {
  brand: number;
  product: number;
  photography: number;
  marketing: number;
  composition: number;
}

interface CREBentoGridProps {
  scores: CREScores;
  className?: string;
}

const getScoreColor = (score: number) => {
  if (score >= 90) return 'text-emerald-400';
  if (score >= 75) return 'text-amber-400';
  return 'text-red-400';
};

const getBgColor = (score: number) => {
  if (score >= 90) return 'bg-emerald-500/10 border-emerald-900/30';
  if (score >= 75) return 'bg-amber-500/10 border-amber-900/30';
  return 'bg-red-500/10 border-red-900/30';
};

export function CREBentoGrid({ scores, className }: CREBentoGridProps) {
  const metrics = [
    { key: 'brand', label: 'Brand Alignment', score: scores.brand },
    { key: 'product', label: 'Product Fidelity', score: scores.product },
    { key: 'photography', label: 'Photography', score: scores.photography },
    { key: 'marketing', label: 'Market Fit', score: scores.marketing },
    { key: 'composition', label: 'Composition', score: scores.composition },
  ];

  // Calculate overall average
  const overall = Math.round(
    Object.values(scores).reduce((a, b) => a + b, 0) / Object.values(scores).length
  );

  return (
    <div className={cn("flex flex-col border-t border-white/5 pt-4 mt-2", className)}>
      {/* Overall Header */}
      <div className="flex items-end justify-between mb-6">
        <div>
          <h3 className="text-[10px] uppercase tracking-widest text-white/30 font-mono mb-1">CRE Health Status</h3>
          <div className="flex items-baseline gap-1">
            <span className="text-5xl font-light font-mono tracking-tighter text-white">
              {overall}
            </span>
            <span className="text-xs text-white/20 font-mono">/100</span>
          </div>
        </div>
        <div className="text-right pb-1">
          <span className="text-[9px] uppercase tracking-widest text-[#9b87f5] font-mono font-semibold">Total Composite</span>
        </div>
      </div>

      {/* Metric Rows */}
      <div className="flex flex-col divide-y divide-white/5 border-y border-white/5">
        {metrics.map((metric, i) => (
          <motion.div
            key={metric.key}
            initial={{ opacity: 0, x: 10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.05 }}
            className="flex items-center justify-between py-2.5 group hover:bg-white/[0.02] transition-colors"
          >
            <span className="text-[11px] font-medium text-white/50 tracking-wide uppercase">
              {metric.label}
            </span>
            <div className="flex items-center gap-3">
              <span className={cn(
                "text-sm font-mono tracking-tight",
                metric.score >= 90 ? "text-[#E1D4C0]" : metric.score >= 75 ? "text-white/60" : "text-red-400/80"
              )}>
                {metric.score}
              </span>
              <div className="w-16 h-0.5 bg-white/5 rounded-full overflow-hidden">
                <div 
                  className={cn(
                    "h-full rounded-full",
                    metric.score >= 90 ? "bg-[#E1D4C0]" : metric.score >= 75 ? "bg-white/20" : "bg-red-500/50"
                  )}
                  style={{ width: `${metric.score}%` }}
                />
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
