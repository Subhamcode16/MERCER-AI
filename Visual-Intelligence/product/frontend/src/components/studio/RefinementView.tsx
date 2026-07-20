export function RefinementView({ onApprove }: { onApprove: () => void }) {
  return (
    <div className="flex gap-12">
      <div className="flex-[1.5] rounded-xl overflow-hidden border border-[var(--color-warm-ivory)]/20 aspect-[3/4] relative shadow-[0_0_40px_rgba(240,230,210,0.03)] group">
        <img src="/public_backup/assets/fashion_hero_1_1783581266482.png" className="w-full h-full object-cover" />
        <div className="absolute top-4 left-4 flex gap-2">
          <div className="px-3 py-1.5 rounded bg-black/60 backdrop-blur-md border border-white/10 text-[9px] uppercase tracking-[0.15em] text-[var(--color-warm-ivory)]">Active Iteration 03</div>
        </div>
        <div className="absolute inset-0 border border-white/0 group-hover:border-white/10 transition-colors pointer-events-none rounded-xl"></div>
      </div>
      
      <div className="flex-1 flex flex-col gap-10">
        <div className="border-b border-white/5 pb-4">
          <h2 className="font-serif text-[24px] text-white/90 mb-2">Art Direction Refinement</h2>
          <p className="text-[12px] text-white/40 tracking-wide leading-relaxed">
            Fine-tune specific characteristics of the selected concept. Atelier will recalibrate the reasoning upon approval.
          </p>
        </div>

        <div className="flex flex-col gap-8">
          <Slider label="Lighting Intensity" value="70%" />
          <Slider label="Composition Width" value="40%" />
          <Slider label="Color Balance (Warmth)" value="85%" />
          <Slider label="Motif Clarity" value="90%" />
        </div>
        
        <div className="mt-auto pt-8 border-t border-white/5">
          <button onClick={onApprove} className="w-full py-4 rounded-lg bg-[var(--color-warm-ivory)]/90 text-black font-semibold text-[11px] uppercase tracking-[0.2em] hover:bg-white transition-colors shadow-[0_0_20px_rgba(240,230,210,0.2)]">
            Approve Asset
          </button>
        </div>
      </div>
    </div>
  );
}

function Slider({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex flex-col gap-3 group">
      <div className="flex items-center justify-between text-[9px] uppercase tracking-[0.15em]">
        <span className="text-white/50 group-hover:text-white/80 transition-colors">{label}</span>
        <span className="text-[var(--color-warm-ivory)]">{value}</span>
      </div>
      <div className="w-full h-1 rounded-full bg-white/10 relative cursor-pointer">
        <div className="absolute top-0 left-0 h-full rounded-full bg-[var(--color-warm-ivory)] shadow-[0_0_10px_rgba(240,230,210,0.3)]" style={{ width: value }}>
          <div className="absolute right-0 top-1/2 -translate-y-1/2 w-3 h-3 bg-white rounded-full shadow-lg transform scale-0 group-hover:scale-100 transition-transform"></div>
        </div>
      </div>
    </div>
  );
}
