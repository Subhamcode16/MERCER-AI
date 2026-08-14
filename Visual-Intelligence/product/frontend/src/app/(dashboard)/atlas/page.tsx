"use client";

import { Compass, Sparkles } from "lucide-react";
import Link from "next/link";

export default function AtlasPage() {
  return (
    <div className="flex-1 h-full flex flex-col px-12 py-12 relative">
      
      {/* Workspace Breadcrumb */}
      <div className="flex items-center gap-3 text-[10px] tracking-[0.2em] uppercase text-white/30 mb-12 select-none">
        <span>Institution</span>
        <span>/</span>
        <span className="text-white/60">Atlas</span>
      </div>

      {/* Premium Empty State */}
      <div className="flex-1 flex flex-col items-center justify-center max-w-md mx-auto w-full text-center select-none">
        <div className="w-16 h-16 rounded-3xl bg-[#E1D4C0]/5 border border-[#E1D4C0]/15 flex items-center justify-center mb-6 shadow-[0_20px_50px_rgba(0,0,0,0.5)]">
          <Compass size={20} className="text-[#E1D4C0]/70 animate-[spin_60s_linear_infinite]" />
        </div>
        <h3 className="font-serif text-lg text-white font-light tracking-wide mb-2">
          Atlas Map Uncharted
        </h3>
        <p className="text-[11.5px] font-sans text-white/40 leading-relaxed font-light mb-8">
          The visual rule engine is empty. Complete a visual synthesis and render your first campaign in the Studio to establish mapping constraints.
        </p>
        <Link href="/studio">
          <button className="flex items-center gap-2 px-8 py-4 bg-white/5 border border-white/10 hover:border-[#E1D4C0]/40 rounded-full text-[11px] tracking-[0.2em] uppercase text-white hover:bg-[#E1D4C0]/5 hover:text-[#E1D4C0] transition-all cursor-pointer">
            <Sparkles size={12} /> Go to Studio
          </button>
        </Link>
      </div>

    </div>
  );
}
