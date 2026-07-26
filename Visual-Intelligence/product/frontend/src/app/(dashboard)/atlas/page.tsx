"use client";

export default function AtlasPage() {
  return (
    <div className="flex-1 h-full flex flex-col px-12 py-12 relative">
      
      {/* Workspace Breadcrumb */}
      <div className="flex items-center gap-3 text-[10px] tracking-[0.2em] uppercase text-white/30 mb-12">
        <span>Institution</span>
        <span>/</span>
        <span className="text-white/60">Atlas</span>
      </div>

      {/* Empty State */}
      <div className="flex-1 flex flex-col items-center justify-center max-w-2xl mx-auto w-full text-center">
        <div className="text-[13px] text-white/40 font-light">
          The Atlas is empty. Generate a campaign to populate visual rules.
        </div>
      </div>

    </div>
  );
}
