"use client";

import { Compass, Sparkles } from "lucide-react";
import Link from "next/link";

export default function AtlasPage() {
  return (
    <div className="flex-1 h-full flex flex-col px-12 py-12 relative bg-background text-foreground">
      
      {/* Workspace Breadcrumb */}
      <div className="flex items-center gap-3 text-[10px] tracking-[0.2em] uppercase text-muted-foreground/60 mb-12 select-none">
        <span>Institution</span>
        <span>/</span>
        <span className="text-foreground">Atlas</span>
      </div>

      {/* Premium Empty State */}
      <div className="flex-1 flex flex-col items-center justify-center max-w-md mx-auto w-full text-center select-none">
        <div className="w-16 h-16 rounded-3xl bg-primary/10 border border-primary/20 flex items-center justify-center mb-6 shadow-sm">
          <Compass size={20} className="text-primary animate-[spin_60s_linear_infinite]" />
        </div>
        <h3 className="font-serif text-lg text-foreground font-light tracking-wide mb-2">
          Atlas Map Uncharted
        </h3>
        <p className="text-[12px] font-sans text-muted-foreground leading-relaxed font-normal mb-8">
          The visual rule engine is empty. Complete a visual synthesis and render your first campaign in the Studio to establish mapping constraints.
        </p>
        <Link href="/studio">
          <button className="flex items-center gap-2 px-8 py-4 bg-card border border-border hover:border-primary/40 rounded-full text-[11px] tracking-[0.2em] uppercase text-foreground hover:bg-primary/5 hover:text-primary transition-all cursor-pointer shadow-xs">
            <Sparkles size={12} /> Go to Studio
          </button>
        </Link>
      </div>

    </div>
  );
}
