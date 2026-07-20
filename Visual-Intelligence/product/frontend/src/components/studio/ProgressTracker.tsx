export function ProgressTracker({ activeStep = 2 }: { activeStep?: number }) {
  return (
    <div className="px-12 py-6 border-y border-white/5 bg-[#0a0a0a]/50">
      <div className="flex items-center w-full max-w-4xl justify-between">
        <Step number="01" title="Understand" subtitle="Material & Context" active={activeStep >= 1} />
        <Arrow />
        <Step number="02" title="Reason" subtitle="AI Creative Direction" active={activeStep >= 2} />
        <Arrow />
        <Step number="03" title="Create" subtitle="Moodboard & Concepts" active={activeStep >= 3} />
        <Arrow />
        <Step number="04" title="Refine" subtitle="Art Direction" active={activeStep >= 4} />
        <Arrow />
        <Step number="05" title="Publish" subtitle="Campaign Assets" active={activeStep >= 5} />
      </div>
    </div>
  );
}

function Step({ number, title, subtitle, active }: { number: string; title: string; subtitle: string; active?: boolean }) {
  return (
    <div className={`flex items-center gap-4 ${active ? 'opacity-100' : 'opacity-40'}`}>
      <div className={`w-9 h-9 rounded-full border flex items-center justify-center text-[10px] tracking-wider ${active ? 'border-white/40 bg-white/5 text-white' : 'border-white/10 text-white/60'}`}>
        {number}
      </div>
      <div className="flex flex-col">
        <span className="text-[12px] tracking-wide text-white/90 mb-0.5">{title}</span>
        <span className="text-[10px] text-white/40">{subtitle}</span>
      </div>
    </div>
  );
}

function Arrow() {
  return (
    <div className="text-white/20 text-[12px]">→</div>
  );
}
