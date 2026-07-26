"use client";

export default function MaterialLibraryPage() {
  return (
    <div className="flex-1 h-full flex flex-col px-12 py-12 relative">
      
      {/* Workspace Breadcrumb */}
      <div className="flex items-center gap-3 text-[10px] tracking-[0.2em] uppercase text-white/30 mb-12">
        <span>Institution</span>
        <span>/</span>
        <span className="text-white/60">Material Library</span>
      </div>

      {/* Empty State */}
      <div className="flex-1 flex flex-col items-center justify-center max-w-2xl mx-auto w-full text-center">
        <div className="text-[13px] text-white/40 font-light mb-8">
          The library is empty.
        </div>
        <button className="px-8 py-4 bg-white/5 border border-white/10 rounded-full text-[11px] tracking-[0.2em] uppercase text-white hover:bg-white/10 transition-colors">
          Upload Material
        </button>
      </div>

    </div>
  );
}
