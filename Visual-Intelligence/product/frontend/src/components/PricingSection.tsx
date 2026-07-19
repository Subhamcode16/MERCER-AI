export function PricingSection() {
  return (
    <section className="relative w-full min-h-screen bg-black flex flex-col items-center justify-center py-32 px-6 z-[200]">
      {/* Background Glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[80vw] h-[80vh] bg-[#E1D4C0]/5 rounded-full blur-[120px] pointer-events-none" />

      <div className="relative z-10 w-full max-w-7xl mx-auto flex flex-col items-center">
        {/* Header */}
        <h2 className="text-[12px] tracking-[0.28em] font-medium opacity-70 mb-8 text-[#E1D4C0] uppercase text-center">
          Access the Intelligence
        </h2>
        <h1 className="font-serif font-bold text-[56px] lg:text-[72px] leading-[0.95] text-center mb-24 max-w-3xl">
          The Cost of Creation.
        </h1>

        {/* Pricing Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 w-full max-w-5xl">
          
          {/* Base Tier */}
          <div className="relative group rounded-2xl border border-white/10 bg-white/5 p-12 overflow-hidden transition-all duration-500 hover:border-white/20 hover:bg-white/10">
            <div className="absolute inset-0 pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity duration-700 bg-gradient-to-b from-white/5 to-transparent" />
            <div className="relative z-10">
              <h3 className="font-serif text-[32px] mb-2">Base</h3>
              <p className="text-[15px] opacity-70 mb-8">For independent creators.</p>
              <div className="flex items-baseline gap-2 mb-12">
                <span className="text-[48px] font-light tracking-tight">$49</span>
                <span className="text-[13px] tracking-widest uppercase opacity-50">/ mo</span>
              </div>
              
              <ul className="space-y-6 mb-12">
                {['100 Visual Renderings', 'Basic Scene Context', 'Standard Export Resolution', 'Community Support'].map((feature, i) => (
                  <li key={i} className="flex items-center gap-4 text-[14px] opacity-90">
                    <div className="w-1.5 h-1.5 rounded-full bg-[#E1D4C0]/50" />
                    {feature}
                  </li>
                ))}
              </ul>
              
              <button className="w-full py-4 rounded-full border border-white/20 bg-transparent text-[13px] tracking-[0.15em] uppercase font-medium hover:bg-white/10 transition-colors">
                Begin Trial
              </button>
            </div>
          </div>

          {/* Atelier Tier */}
          <div className="relative group rounded-2xl border border-[#E1D4C0]/30 bg-white/5 p-12 overflow-hidden transition-all duration-500 hover:border-[#E1D4C0]/60 hover:bg-white/10 shadow-[0_0_40px_rgba(225,212,192,0.05)]">
            <div className="absolute inset-0 pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity duration-700 bg-gradient-to-b from-[#E1D4C0]/10 to-transparent" />
            
            {/* Fluid Glare */}
            <div className="absolute top-0 -bottom-[100%] left-0 w-32 bg-gradient-to-r from-transparent via-[#E1D4C0]/20 to-transparent skew-x-[-20deg] pointer-events-none -translate-x-[200%] group-hover:translate-x-[500%] transition-transform duration-1000 ease-in-out" />

            <div className="relative z-10">
              <div className="flex items-center justify-between mb-2">
                <h3 className="font-serif text-[32px] text-[#E1D4C0]">Atelier</h3>
                <span className="text-[10px] tracking-[0.2em] border border-[#E1D4C0]/30 px-3 py-1 rounded-full text-[#E1D4C0] uppercase">
                  Premium
                </span>
              </div>
              <p className="text-[15px] opacity-70 mb-8">For professional studios.</p>
              <div className="flex items-baseline gap-2 mb-12">
                <span className="text-[48px] font-light tracking-tight text-[#E1D4C0]">$199</span>
                <span className="text-[13px] tracking-widest uppercase opacity-50">/ mo</span>
              </div>
              
              <ul className="space-y-6 mb-12">
                {['Unlimited Renderings', 'Deep Cinematic Intelligence', '8K Export Resolution', 'Dedicated Technical Director'].map((feature, i) => (
                  <li key={i} className="flex items-center gap-4 text-[14px] opacity-90">
                    <div className="w-1.5 h-1.5 rounded-full bg-[#E1D4C0]" />
                    {feature}
                  </li>
                ))}
              </ul>
              
              <button className="w-full py-4 rounded-full border border-[#E1D4C0]/40 bg-[#E1D4C0]/10 text-[13px] tracking-[0.15em] uppercase font-medium text-[#E1D4C0] hover:bg-[#E1D4C0]/20 transition-colors">
                Select Atelier
              </button>
            </div>
          </div>

        </div>
      </div>
    </section>
  );
}
