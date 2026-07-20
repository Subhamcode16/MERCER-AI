export function CopilotInterface({ onSubmit }: { onSubmit?: () => void }) {
  return (
    <div className="mt-4 rounded-xl border border-white/5 bg-gradient-to-b from-white/5 to-transparent p-[1px]">
      <div className="rounded-[11px] bg-[#0d0d0d] p-8 flex flex-col gap-8">
        {/* Assistant Message */}
        <div className="flex gap-5">
          <div className="w-10 h-10 rounded-full border border-white/10 flex items-center justify-center shrink-0 bg-[#111]">
            <span className="font-serif text-[16px] text-white/70">A</span>
          </div>
          <div className="flex flex-col gap-2.5">
            <span className="text-[10px] text-white/40 uppercase tracking-[0.2em] font-medium">Atelier Copilot</span>
            <p className="text-[13px] text-white/70 leading-[1.8] max-w-4xl tracking-wide">
              I've analyzed the Kadhua weave and your brand's heritage positioning. <span className="text-[var(--color-warm-ivory)]">Direction 01 (Royal Warmth)</span> aligns perfectly with the objective of brand elevation by emphasizing the intricate zari work through directional golden hour lighting. Would you like me to proceed with generating the moodboard for this direction?
            </p>
          </div>
        </div>

        {/* Input */}
        <div className="relative mt-2">
          <input 
            type="text" 
            placeholder="Ask Atelier anything... (e.g. Generate a moodboard based on Direction 01)" 
            className="w-full bg-black/50 border border-white/10 rounded-lg px-5 py-4 pl-14 text-[13px] text-white placeholder-white/30 focus:outline-none focus:border-[var(--color-warm-ivory)]/40 transition-colors"
          />
          <div className="absolute left-5 top-1/2 -translate-y-1/2 w-[18px] h-[18px] rounded-sm border border-white/20 flex flex-col items-center justify-center gap-[2px] opacity-60">
             <div className="w-2.5 h-[1px] bg-white"></div>
             <div className="w-2.5 h-[1px] bg-white"></div>
             <div className="w-2.5 h-[1px] bg-white"></div>
          </div>
          <button onClick={onSubmit} className="absolute right-3 top-1/2 -translate-y-1/2 px-5 py-2.5 rounded border border-transparent bg-white hover:bg-[var(--color-warm-ivory)] text-black text-[10px] font-medium uppercase tracking-[0.15em] transition-colors">
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
