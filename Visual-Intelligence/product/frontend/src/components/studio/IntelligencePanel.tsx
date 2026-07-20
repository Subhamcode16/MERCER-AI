export function IntelligencePanel() {
  return (
    <aside className="w-[340px] h-screen overflow-y-auto border-l border-white/5 bg-[#0a0a0a] flex-shrink-0 z-40 custom-scrollbar">
      {/* Header */}
      <div className="p-6 pb-6 flex items-center justify-between sticky top-0 bg-[#0a0a0a]/90 backdrop-blur-md z-10 border-b border-white/5">
        <div className="flex items-center gap-3">
          <div className="w-3 h-3 grid grid-cols-2 gap-0.5 opacity-40">
            <div className="bg-white rounded-[1px]"></div><div className="bg-white rounded-[1px]"></div><div className="bg-white rounded-[1px]"></div><div className="bg-white rounded-[1px]"></div>
          </div>
          <span className="text-[10px] tracking-[0.2em] uppercase font-medium text-white/60">Intelligence Panel</span>
        </div>
      </div>

      <div className="p-6 flex flex-col gap-10">
        {/* Creative Intelligence */}
        <div>
          <h3 className="text-[9px] tracking-[0.25em] uppercase text-white/40 mb-4">Creative Intelligence</h3>
          <p className="font-serif text-[18px] leading-[1.5] text-white/80">
            The brain of Atelier. Every recommendation is backed by reasoning, evidence and institutional knowledge.
          </p>
        </div>

        {/* Confidence Score */}
        <div className="border-t border-white/5 pt-8">
          <h3 className="text-[9px] tracking-[0.25em] uppercase text-white/40 mb-6">Confidence Score</h3>
          <div className="flex items-center justify-between mb-4">
            <span className="font-serif text-[42px] leading-none text-white/90">92<span className="text-[20px] text-white/50">%</span></span>
            <div className="w-14 h-14 relative flex items-center justify-center">
              <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="45" fill="none" stroke="rgba(255,255,255,0.05)" strokeWidth="4" />
                <circle cx="50" cy="50" r="45" fill="none" stroke="var(--color-warm-ivory)" strokeWidth="4" strokeDasharray="283" strokeDashoffset="22" className="opacity-80" />
              </svg>
            </div>
          </div>
          <div className="w-full h-[1px] bg-white/5 relative">
            <div className="absolute top-0 left-0 h-[1px] bg-[var(--color-warm-ivory)]/70 w-[92%]"></div>
          </div>
          <p className="text-[10px] text-white/40 mt-3 tracking-wide">High Confidence</p>
        </div>

        {/* Reasoning */}
        <div className="border-t border-white/5 pt-8">
          <h3 className="text-[9px] tracking-[0.25em] uppercase text-white/40 mb-5 flex items-center gap-2">
            <div className="w-3 h-3 border border-white/30 border-t-2 opacity-60"></div>
            Reasoning
          </h3>
          <p className="text-[12px] leading-[1.7] text-white/70">
            The combination of Kadhua weave and metallic zari thrives in warm, directional light. Heritage storytelling will elevate brand perception.
          </p>
        </div>

        {/* Evidence */}
        <div className="border-t border-white/5 pt-8">
          <h3 className="text-[9px] tracking-[0.25em] uppercase text-white/40 mb-4 flex items-center gap-2">
            <div className="w-2.5 h-2.5 border border-white/30 transform rotate-45 opacity-60"></div>
            Evidence
          </h3>
          <p className="text-[11px] text-white/50 mb-5 tracking-wide">127 references support this direction</p>
          <div className="grid grid-cols-4 gap-2 mb-4">
            {[1,2,3,4].map(i => (
              <div key={i} className="aspect-[4/3] rounded bg-white/5 relative overflow-hidden">
                <img src={`/public_backup/assets/fashion_hero_${i === 4 ? 1 : i}_17835812${66482 + i}.png`} alt="" className="w-full h-full object-cover opacity-60 hover:opacity-100 transition-opacity" />
              </div>
            ))}
          </div>
          <button className="w-full py-2.5 rounded border border-white/10 bg-transparent text-[10px] tracking-[0.1em] text-white/50 hover:bg-white/5 hover:text-white/80 transition-colors uppercase">
            View All Evidence
          </button>
        </div>

        {/* Related Knowledge */}
        <div className="border-t border-white/5 pt-8">
          <h3 className="text-[9px] tracking-[0.25em] uppercase text-white/40 mb-5 flex items-center gap-2">
            <div className="w-3 h-3 rounded-full border border-white/30 opacity-60"></div>
            Related Knowledge
          </h3>
          <div className="flex flex-wrap gap-x-3 gap-y-2 text-[11px] text-white/60">
            <span>Banarasi Silk</span><span className="text-white/20">•</span>
            <span>Heritage Lighting</span><span className="text-white/20">•</span>
            <span>Indian Architecture</span><span className="text-white/20">•</span>
            <span>Royal Aesthetics</span><span className="text-white/20">•</span>
            <span>Gold & Warm Tones</span><span className="text-white/20">•</span>
            <span>Cultural Symbolism</span>
          </div>
          <button className="w-full mt-6 py-2.5 rounded border border-[var(--color-warm-ivory)]/20 bg-transparent text-[10px] tracking-[0.1em] text-[var(--color-warm-ivory)] hover:bg-[var(--color-warm-ivory)]/5 transition-colors uppercase">
            Explore Knowledge Atlas
          </button>
        </div>

        {/* Atelier Principles Footer */}
        <div className="border-t border-white/5 pt-10 pb-8 flex items-start justify-between">
          <div className="flex flex-col gap-2 text-[9px] text-white/30 uppercase tracking-[0.15em]">
            <span className="text-[var(--color-warm-ivory)]/50 mb-1">Atelier Principles</span>
            <span>Observe everything</span>
            <span>Understand deeply</span>
            <span>Reason with evidence</span>
            <span>Propose with clarity</span>
            <span>Create with intent</span>
            <span>Learn continuously</span>
          </div>
          <div className="w-12 h-12 rounded-full border border-white/10 flex items-center justify-center opacity-20">
            <span className="font-serif text-[18px]">A</span>
          </div>
        </div>
      </div>
    </aside>
  );
}
