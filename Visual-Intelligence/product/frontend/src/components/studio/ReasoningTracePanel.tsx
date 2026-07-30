'use client';

import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Brain, CheckCircle2, AlertTriangle, Info } from 'lucide-react';
import { cn } from '@/lib/utils';

interface ConstraintDecision {
  id: string;
  type: 'satisfied' | 'relaxed' | 'applied';
  description: string;
  rationale?: string;
  level: 1 | 2 | 3;
}

interface ReasoningTracePanelProps {
  decisions: ConstraintDecision[];
  className?: string;
}

  export function ReasoningTracePanel({ decisions, className }: ReasoningTracePanelProps) {
    return (
      <div className={cn('flex flex-col', className)}>
        <div className="flex items-center justify-between pb-3 mb-2 border-b border-white/5">
          <div className="flex items-center gap-2">
            <Brain className="w-4 h-4 text-[#9b87f5]" />
            <h3 className="text-[10px] font-semibold text-[#E1D4C0] font-mono tracking-widest uppercase">Intelligence_Trace</h3>
          </div>
        </div>
        
        <div className="flex-1 overflow-y-auto space-y-0 relative">
          <AnimatePresence initial={false}>
            {decisions.length === 0 ? (
              <motion.div 
                initial={{ opacity: 0 }} 
                animate={{ opacity: 1 }}
                className="text-xs text-white/30 font-mono italic py-4"
              >
                Awaiting solver input...
              </motion.div>
            ) : (
              decisions.map((decision, idx) => (
                <motion.div
                  key={decision.id}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  layout
                  className={cn(
                    "py-3 flex items-start gap-3 relative",
                    idx !== decisions.length - 1 && "border-b border-white/5"
                  )}
                >
                  <div className="mt-1 flex-shrink-0">
                    {decision.type === 'satisfied' || decision.type === 'applied' ? (
                      <div className="w-1.5 h-1.5 rounded-full bg-[#E1D4C0]/80 shadow-[0_0_8px_rgba(225,212,192,0.5)]" />
                    ) : (
                      <div className="w-1.5 h-1.5 rounded-full bg-amber-500/80 shadow-[0_0_8px_rgba(245,158,11,0.5)]" />
                    )}
                  </div>
                  <div className="space-y-1.5 flex-1 min-w-0">
                    <p className="text-[12px] text-white/90 font-medium leading-snug">
                      {decision.description}
                    </p>
                    {decision.rationale && (
                      <p className="text-white/40 text-[11px] leading-relaxed tracking-wide">
                        {decision.rationale}
                      </p>
                    )}
                    <div className="flex items-center gap-2 mt-1">
                      <span className="text-[9px] uppercase tracking-widest font-mono text-white/40">
                        LVL {decision.level}
                      </span>
                      <span className={cn(
                        "text-[9px] uppercase tracking-widest font-mono",
                        decision.type === 'relaxed' ? "text-amber-500/70" : "text-[#E1D4C0]/60"
                      )}>
                        • {decision.type}
                      </span>
                    </div>
                  </div>
                </motion.div>
              ))
            )}
        </AnimatePresence>
      </div>
    </div>
  );
}
