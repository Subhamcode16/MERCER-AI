"use client";

import Link from "next/link";
import { ArrowRight, HelpCircle } from "lucide-react";
import AnimatedGradientBackground from "@/components/ui/animated-gradient-background";

export default function NotFound() {
  return (
    <div className="w-full min-h-screen relative overflow-hidden bg-[#050505] text-[#E1D4C0] flex flex-col items-center justify-center p-6 select-none font-sans">
      {/* Atmospheric Radial Gradient Background */}
      <AnimatedGradientBackground
        startingGap={110}
        Breathing={true}
        breathingRange={8}
        animationSpeed={0.015}
        topOffset={-10}
        gradientColors={[
          "#050505",
          "#1f1215",
          "#451a23",
          "#7c3d49",
          "#b36272",
          "#d48c9a",
          "#050505",
        ]}
        gradientStops={[30, 42, 52, 62, 73, 84, 100]}
      />

      {/* 404 Content Overlay */}
      <div className="relative z-10 flex flex-col items-center max-w-lg text-center gap-6">
        <div className="w-16 h-16 rounded-full bg-[#E1D4C0]/5 border border-[#E1D4C0]/20 flex items-center justify-center mb-2 shadow-2xl animate-pulse">
          <HelpCircle size={24} className="text-[#E1D4C0]" />
        </div>
        
        <span className="text-[10px] font-mono tracking-[0.3em] uppercase text-white/30">
          Error 404
        </span>

        <h1 className="text-4xl font-serif tracking-wide text-white leading-tight font-light">
          Lost in Visual Space
        </h1>

        <p className="text-[12px] text-white/40 leading-relaxed font-light font-sans max-w-sm">
          The coordinates you entered led to an uncharted quadrant. The specimen or sequence you are looking for does not exist.
        </p>

        <div className="mt-4">
          <Link href="/studio">
            <button className="flex items-center gap-2 px-8 py-3.5 bg-[#E1D4C0]/5 border border-[#E1D4C0]/20 hover:border-[#E1D4C0]/50 hover:bg-[#E1D4C0]/10 text-white rounded-full text-[11px] tracking-[0.2em] uppercase transition-all duration-300 cursor-pointer shadow-lg">
              Return to Studio <ArrowRight size={12} />
            </button>
          </Link>
        </div>
      </div>
    </div>
  );
}
