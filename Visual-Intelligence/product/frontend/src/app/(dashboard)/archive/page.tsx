"use client";

import { Archive, ArrowRight } from "lucide-react";
import Link from "next/link";

export default function ArchivePage() {
  return (
    <div className="flex-1 h-full flex flex-col px-12 py-12 relative">
      
      {/* Workspace Breadcrumb */}
      <div className="flex items-center gap-3 text-[10px] tracking-[0.2em] uppercase text-white/30 mb-12 select-none">
        <span>Institution</span>
        <span>/</span>
        <span className="text-white/60">Archive</span>
      </div>

      {/* Premium Empty State */}
      <div className="flex-1 flex flex-col items-center justify-center max-w-md mx-auto w-full text-center select-none">
        <div className="w-16 h-16 rounded-3xl bg-[#E1D4C0]/5 border border-[#E1D4C0]/15 flex items-center justify-center mb-6 shadow-[0_20px_50px_rgba(0,0,0,0.5)]">
          <Archive size={20} className="text-[#E1D4C0]/70" />
        </div>
        <h3 className="font-serif text-lg text-white font-light tracking-wide mb-2">
          Archive Cabinet Empty
        </h3>
        <p className="text-[11.5px] font-sans text-white/40 leading-relaxed font-light mb-8">
          No campaigns have been archived yet. Once you complete a creative cycle in the Studio, you can safely stash the workspace memory here.
        </p>
        <Link href="/studio">
          <button className="flex items-center gap-2 px-8 py-4 bg-white/5 border border-white/10 hover:border-[#E1D4C0]/40 rounded-full text-[11px] tracking-[0.2em] uppercase text-white hover:bg-[#E1D4C0]/5 hover:text-[#E1D4C0] transition-all cursor-pointer">
            Go to Studio <ArrowRight size={12} />
          </button>
        </Link>
      </div>

    </div>
  );
}
