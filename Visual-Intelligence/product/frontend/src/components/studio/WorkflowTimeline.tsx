export function WorkflowTimeline({ hasUploaded }: { hasUploaded?: boolean }) {
  return (
    <div className="px-12 py-5 border-t border-white/5 bg-[#0a0a0a] flex items-center justify-between text-[9px] text-white/30 uppercase tracking-[0.2em]">
      <div className="flex gap-10">
        <span className="font-medium text-white/50">Timeline</span>
        {hasUploaded ? (
          <>
            <div className="flex items-center gap-2">
              <div className="w-1.5 h-1.5 rounded-full bg-[var(--color-warm-ivory)]/50"></div>
              <span className="text-[var(--color-warm-ivory)]/80">Material Uploaded (2d ago)</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-1.5 h-1.5 rounded-full bg-white/20"></div>
              <span className="text-white/50">Analysis Complete (1d ago)</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-1 h-1 rounded-full bg-white/20"></div>
              <span className="text-white/40">Creative Direction (Just now)</span>
            </div>
          </>
        ) : (
          <div className="flex items-center gap-2">
            <div className="w-1.5 h-1.5 rounded-full bg-[var(--color-warm-ivory)]/50"></div>
            <span className="text-[var(--color-warm-ivory)]/80">Waiting for material upload</span>
          </div>
        )}
      </div>
      <div className="tracking-[0.25em] opacity-50">
        Atelier OS v1.0.0
      </div>
    </div>
  );
}
