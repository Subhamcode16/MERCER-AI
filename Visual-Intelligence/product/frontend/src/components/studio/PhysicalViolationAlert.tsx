'use client';

import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ShieldAlert, X } from 'lucide-react';
import { cn } from '@/lib/utils';

export interface PhysicalViolation {
  id: string;
  rule: string;
  message: string;
  conflictingElements: string[];
}

interface PhysicalViolationAlertProps {
  violation: PhysicalViolation | null;
  onDismiss: () => void;
  className?: string;
}

export function PhysicalViolationAlert({ violation, onDismiss, className }: PhysicalViolationAlertProps) {
  return (
    <AnimatePresence>
      {violation && (
        <motion.div
          initial={{ opacity: 0, y: -20, scale: 0.95 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: -20, scale: 0.95 }}
          transition={{ type: 'spring', damping: 20, stiffness: 300 }}
          className={cn(
            "relative w-full bg-red-950/40 border border-red-900/50 rounded-lg p-4 overflow-hidden",
            className
          )}
        >
          {/* Background subtle pulse */}
          <div className="absolute inset-0 bg-red-500/5 animate-pulse pointer-events-none" />
          
          <div className="relative flex items-start gap-4">
            <div className="bg-red-900/30 p-2 rounded-md">
              <ShieldAlert className="w-5 h-5 text-red-500" />
            </div>
            
            <div className="flex-1 space-y-2">
              <h4 className="text-red-400 font-semibold tracking-tight text-sm uppercase">
                Physical Law Violation
              </h4>
              <p className="text-zinc-300 text-sm leading-relaxed">
                {violation.message}
              </p>
              
              <div className="flex flex-wrap gap-2 pt-2">
                {violation.conflictingElements.map((el, i) => (
                  <span 
                    key={i}
                    className="inline-flex items-center px-2 py-1 rounded-md bg-red-950/50 border border-red-900/50 text-xs font-mono text-red-300"
                  >
                    {el}
                  </span>
                ))}
              </div>
            </div>

            <button 
              onClick={onDismiss}
              className="p-1 rounded-md hover:bg-red-900/30 transition-colors text-red-400/70 hover:text-red-400"
            >
              <X className="w-4 h-4" />
              <span className="sr-only">Dismiss</span>
            </button>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
