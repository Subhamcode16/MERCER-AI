"use client";

import { Layers, Upload } from "lucide-react";

export default function MaterialLibraryPage() {
  return (
    <div className="flex-1 h-full flex flex-col px-12 py-12 relative bg-background text-foreground">
      
      {/* Workspace Breadcrumb */}
      <div className="flex items-center gap-3 text-[10px] tracking-[0.2em] uppercase text-muted-foreground/60 mb-12 select-none">
        <span>Institution</span>
        <span>/</span>
        <span className="text-foreground">Material Library</span>
      </div>

      {/* Premium Empty State */}
      <div className="flex-1 flex flex-col items-center justify-center max-w-md mx-auto w-full text-center select-none">
        <div className="w-16 h-16 rounded-3xl bg-primary/10 border border-primary/20 flex items-center justify-center mb-6 shadow-sm">
          <Layers size={20} className="text-primary" />
        </div>
        <h3 className="font-serif text-lg text-foreground font-light tracking-wide mb-2">
          Material Vault Empty
        </h3>
        <p className="text-[12px] font-sans text-muted-foreground leading-relaxed font-normal mb-8">
          Upload textile scans or raw fabric imagery. Our analysis engine will extract physical weave and thread density specs to sync with your agent team.
        </p>
        <button className="flex items-center gap-2 px-8 py-4 bg-card border border-border hover:border-primary/40 rounded-full text-[11px] tracking-[0.2em] uppercase text-foreground hover:bg-primary/5 hover:text-primary transition-all cursor-pointer shadow-xs">
          <Upload size={12} /> Upload Material
        </button>
      </div>

    </div>
  );
}
