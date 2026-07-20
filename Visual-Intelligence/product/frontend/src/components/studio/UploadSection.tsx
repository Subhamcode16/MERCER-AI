export function UploadSection({ onUpload }: { onUpload: () => void }) {
  return (
    <div className="flex-1 flex flex-col items-center justify-center min-h-[60vh]">
      <div 
        onClick={onUpload}
        className="w-full max-w-3xl aspect-[2.5/1] rounded-2xl border-2 border-dashed border-white/10 hover:border-[var(--color-warm-ivory)]/40 bg-white/5 hover:bg-[var(--color-warm-ivory)]/5 transition-all duration-500 cursor-pointer flex flex-col items-center justify-center gap-6 group relative overflow-hidden"
      >
        <div className="w-16 h-16 rounded-full border border-white/20 flex items-center justify-center group-hover:scale-110 group-hover:border-[var(--color-warm-ivory)]/50 transition-all duration-500 bg-[#0a0a0a]">
          <svg className="w-6 h-6 text-white/50 group-hover:text-[var(--color-warm-ivory)] transition-colors duration-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" /></svg>
        </div>
        <div className="flex flex-col items-center gap-2">
          <h3 className="font-serif text-[22px] text-white/90">Upload Material Reference</h3>
          <p className="text-[11px] uppercase tracking-[0.2em] text-white/40">Drag & Drop or <span className="text-[var(--color-warm-ivory)]">Browse Files</span></p>
        </div>
      </div>
    </div>
  );
}
