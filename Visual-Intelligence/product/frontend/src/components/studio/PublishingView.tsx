export function PublishingView() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] text-center gap-10">
      <div className="w-24 h-24 rounded-full border border-[var(--color-warm-ivory)]/30 flex items-center justify-center bg-[var(--color-warm-ivory)]/5 mb-2 shadow-[0_0_40px_rgba(240,230,210,0.05)] relative">
        <div className="absolute inset-0 rounded-full border border-[var(--color-warm-ivory)]/10 animate-ping opacity-20"></div>
        <svg className="w-10 h-10 text-[var(--color-warm-ivory)]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M5 13l4 4L19 7" /></svg>
      </div>
      
      <div className="flex flex-col gap-4 max-w-xl">
        <h2 className="font-serif text-[36px] text-white/90">Campaign Bundle Ready</h2>
        <p className="text-[13px] text-white/50 leading-[1.8] tracking-wide">
          The Banarasi Heritage Campaign has been successfully constructed. The package includes high-resolution production assets, material DNA metadata, and institutional reasoning logs.
        </p>
      </div>

      <div className="flex gap-6 w-full max-w-2xl mt-4">
        <div className="flex-[1.5] aspect-[4/3] rounded-xl overflow-hidden border border-[var(--color-warm-ivory)]/30 relative shadow-xl">
          <img src="/public_backup/assets/fashion_hero_1_1783581266482.png" className="w-full h-full object-cover" />
          <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent flex items-end p-5">
            <span className="text-[10px] uppercase tracking-[0.2em] text-[var(--color-warm-ivory)] font-medium">Final Asset</span>
          </div>
        </div>
        <div className="flex-1 aspect-[4/3] rounded-xl overflow-hidden border border-white/10 relative">
          <img src="/public_backup/assets/fashion_hero_1_1783581266482.png" className="w-full h-full object-cover opacity-50 grayscale" />
          <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent flex items-end p-5">
            <span className="text-[10px] uppercase tracking-[0.2em] text-white/60 font-medium">Source Material</span>
          </div>
        </div>
      </div>

      <button className="px-10 py-4 mt-8 rounded-lg border border-[var(--color-warm-ivory)]/40 bg-[var(--color-warm-ivory)]/5 text-[var(--color-warm-ivory)] font-medium text-[11px] uppercase tracking-[0.2em] hover:bg-[var(--color-warm-ivory)] hover:text-black transition-all duration-300">
        Export Campaign Bundle
      </button>
    </div>
  );
}
