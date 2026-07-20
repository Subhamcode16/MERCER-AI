export function CampaignHeader({ onBack, showBack }: { onBack?: () => void; showBack?: boolean }) {
  return (
    <div className="px-12 pt-10 pb-6 flex items-center justify-between">
      <div className="flex flex-col gap-4">
        {/* Breadcrumb / Back Button */}
        <div className="flex items-center gap-3 text-[11px] text-white/40 uppercase tracking-[0.1em]">
          {showBack ? (
            <button onClick={onBack} className="flex items-center gap-2 cursor-pointer hover:text-[var(--color-warm-ivory)] transition-colors">
              <span className="text-[12px]">{'<'}</span>
              <span>Back to Previous Step</span>
            </button>
          ) : (
            <>
              <span className="cursor-pointer hover:text-white/80 transition-colors">{'<'}</span>
              <span className="cursor-pointer hover:text-white/80 transition-colors">Campaign Studio</span>
            </>
          )}
        </div>
        
        {/* Title Area */}
        <div className="flex items-center gap-5">
          <h1 className="font-serif text-[28px] text-white/90 tracking-wide">Banarasi Heritage Campaign</h1>
          <div className="flex items-center gap-2 px-3 py-1 rounded-full border border-[var(--color-warm-ivory)]/20 bg-[var(--color-warm-ivory)]/10 text-[var(--color-warm-ivory)] text-[9px] uppercase tracking-[0.2em] opacity-80">
            <div className="w-1 h-1 rounded-full bg-[var(--color-warm-ivory)] shadow-[0_0_8px_var(--color-warm-ivory)]"></div>
            Active
          </div>
        </div>
        
        <div className="text-[11px] text-white/30 flex items-center gap-3 tracking-wide">
          <span>Luxury Saree Campaign</span>
          <span className="opacity-50">•</span>
          <span>Created 2 days ago</span>
          <span className="opacity-50">•</span>
          <span>Updated 3 min ago</span>
        </div>
      </div>
      
      {/* Actions */}
      <div className="flex items-center gap-3 self-end">
        <button className="flex items-center gap-2 px-5 py-2.5 rounded border border-white/10 bg-transparent hover:bg-white/5 transition-colors text-[11px] text-white/60 tracking-wider">
          <svg className="w-3.5 h-3.5 opacity-70" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" /></svg>
          Share
        </button>
        <button className="flex items-center gap-2 px-5 py-2.5 rounded border border-white/10 bg-transparent hover:bg-white/5 transition-colors text-[11px] text-white/60 tracking-wider">
          <svg className="w-3.5 h-3.5 opacity-70" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" /></svg>
          Export
        </button>
      </div>
    </div>
  );
}
