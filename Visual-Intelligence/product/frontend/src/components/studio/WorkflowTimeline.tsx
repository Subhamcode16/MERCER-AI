'use client';

import React, { useRef } from 'react';
import { useGSAP } from '@gsap/react';
import gsap from 'gsap';
import { motion } from 'framer-motion';
import { Cpu, ShieldCheck, Database, Sliders, Image } from 'lucide-react';

interface WorkflowTimelineProps {
  status?: 'pending' | 'approved' | 'rendering' | 'completed' | 'failed' | string;
  hasMaterial?: boolean;
  weaveType?: string;
  fiberBase?: string;
}

export function WorkflowTimeline({ 
  status = 'pending', 
  hasMaterial = false,
  weaveType = 'Zari Brocade',
  fiberBase = 'Silk'
}: WorkflowTimelineProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const lineRef = useRef<SVGPathElement>(null);

  // Map status to a pipeline progress level (0 to 4)
  let level = 0; // Waiting
  if (hasMaterial) level = 1; // Ingested
  if (status === 'pending') level = 2; // Art Direction
  if (status === 'approved' || status === 'rendering') level = 3; // Rendering
  if (status === 'completed') level = 4; // Complete / Vaulted

  const totalLength = 100; // SVG path coordinate width scale
  const segmentLength = 25; // 4 segments: 0 -> 25 -> 50 -> 75 -> 100
  const targetOffset = totalLength - (level * segmentLength);

  useGSAP(() => {
    if (!lineRef.current) return;
    
    // Animate active path dash offset with custom spring-like ease
    gsap.to(lineRef.current, {
      strokeDashoffset: targetOffset,
      duration: 1.5,
      ease: 'power3.out',
      overwrite: 'auto'
    });

    // Staggered load-in animation for panel text and elements
    const items = containerRef.current?.querySelectorAll('.telemetry-item');
    if (items && items.length > 0) {
      gsap.fromTo(
        items,
        { opacity: 0, y: 10 },
        { opacity: 1, y: 0, duration: 0.8, stagger: 0.08, ease: 'power2.out' }
      );
    }
  }, { scope: containerRef, dependencies: [level] });

  const steps = [
    { name: 'Upload', icon: Database, desc: 'Specimen Load' },
    { name: 'Ingest', icon: Cpu, desc: 'DNA Analysis' },
    { name: 'Direct', icon: Sliders, desc: 'Art Selection' },
    { name: 'Render', icon: Image, desc: 'Flux Rendering' },
    { name: 'Vault', icon: ShieldCheck, desc: 'Secure Commit' }
  ];

  return (
    <div 
      ref={containerRef}
      className="w-full bg-[#050505]/40 border border-white/5 p-1 rounded-[2rem] shadow-[0_20px_50px_-15px_rgba(0,0,0,0.8)] backdrop-blur-3xl overflow-hidden telemetry-item"
    >
      {/* Inner Core Enclosure with highlight bevel */}
      <div className="bg-[#0C0C0E]/90 border border-white/10 rounded-[calc(2rem-0.25rem)] p-6 md:p-8 flex flex-col gap-6 relative shadow-[inset_0_1px_1px_rgba(255,255,255,0.05)]">
        
        {/* Dynamic ambient background glow */}
        <div className="absolute top-0 right-1/4 w-60 h-20 bg-[#E1D4C0]/5 blur-3xl rounded-full pointer-events-none -z-10 animate-pulse" />

        {/* Telemetry Header Statistics */}
        <div className="flex flex-wrap items-center justify-between gap-4 border-b border-white/5 pb-4 telemetry-item">
          <div className="flex items-center gap-3">
            <span className="w-2 h-2 rounded-full bg-[#E1D4C0] animate-ping" />
            <h4 className="font-serif text-sm tracking-wide text-white">Telemetry Dock</h4>
            <span className="text-[9px] font-mono tracking-widest text-white/30 uppercase px-2 py-0.5 bg-white/5 rounded">
              Active Stream
            </span>
          </div>
          
          <div className="flex gap-8 font-mono text-[10px]">
            <div className="flex flex-col">
              <span className="text-white/30 uppercase tracking-widest">Base Material</span>
              <span className="text-white font-medium mt-0.5">{fiberBase}</span>
            </div>
            <div className="flex flex-col">
              <span className="text-white/30 uppercase tracking-widest">Weave structure</span>
              <span className="text-white font-medium mt-0.5">{weaveType}</span>
            </div>
            <div className="flex flex-col">
              <span className="text-white/30 uppercase tracking-widest">Render Pipeline</span>
              <span className="text-[#E1D4C0] font-medium mt-0.5 uppercase tracking-wide">
                {status === 'pending' && 'Art Direction Phase'}
                {status === 'approved' && 'Rendering queued'}
                {status === 'rendering' && 'Flux active'}
                {status === 'completed' && 'Vaulted / Success'}
                {status === 'failed' && 'Pipeline Failure'}
              </span>
            </div>
          </div>
        </div>

        {/* Telemetry SVG Pipeline & Indicators */}
        <div className="relative w-full py-2 telemetry-item">
          {/* Horizontal Trace Line behind everything */}
          <div className="absolute top-1/2 left-0 right-0 h-[2px] bg-white/5 -translate-y-1/2 -z-10" />

          {/* SVG Active Segment Line */}
          <svg 
            className="absolute top-1/2 left-0 right-0 w-full h-[2px] -translate-y-1/2 -z-10 pointer-events-none" 
            viewBox="0 0 100 2" 
            preserveAspectRatio="none"
          >
            <path 
              ref={lineRef}
              d="M 0 1 L 100 1" 
              stroke="#E1D4C0" 
              strokeWidth="2" 
              strokeDasharray="100" 
              strokeDashoffset="100" 
            />
          </svg>

          {/* Nodes Container */}
          <div className="flex items-center justify-between px-1 relative">
            {steps.map((step, idx) => {
              const StepIcon = step.icon;
              const isPassed = idx < level;
              const isActive = idx === level;
              const isFuture = idx > level;

              return (
                <div key={step.name} className="flex flex-col items-center relative group">
                  {/* Circle Node Plate */}
                  <motion.div 
                    whileHover={{ scale: 1.05 }}
                    className={`w-9 h-9 rounded-full border flex items-center justify-center transition-all duration-300 ${
                      isActive 
                        ? 'bg-[#E1D4C0] border-[#E1D4C0] text-black shadow-[0_0_15px_rgba(225,212,192,0.4)]'
                        : isPassed 
                        ? 'bg-[#0C0C0E] border-[#E1D4C0]/40 text-[#E1D4C0]'
                        : 'bg-[#050505] border-white/5 text-white/20'
                    }`}
                  >
                    <StepIcon className="w-4 h-4" />
                  </motion.div>

                  {/* Label Text below node */}
                  <div className="absolute top-11 flex flex-col items-center w-24 text-center">
                    <span className={`text-[10px] font-medium tracking-wide uppercase transition-colors ${
                      isActive ? 'text-[#E1D4C0]' : isPassed ? 'text-white/60' : 'text-white/20'
                    }`}>
                      {step.name}
                    </span>
                    <span className="text-[8px] font-mono uppercase tracking-widest text-white/25 mt-0.5 scale-90">
                      {step.desc}
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Outer Padding/Spacing for nodes text labels */}
        <div className="h-4" />

      </div>
    </div>
  );
}
