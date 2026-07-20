export function CreativeDirectionPreview({ onSelectDirection }: { onSelectDirection?: () => void }) {
  return (
    <div className="flex flex-col gap-8">
      <div className="flex items-end justify-between">
        <div>
          <h2 className="font-serif text-[24px] text-white/90 mb-2">AI Creative Direction</h2>
          <p className="text-[12px] text-white/40 tracking-wide">Based on your material and context, we propose 4 distinct visual directions.</p>
        </div>
        <div className="flex gap-2">
          <button className="w-9 h-9 rounded-full border border-white/10 flex items-center justify-center hover:bg-white/5 transition-colors text-white/50 hover:text-white">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M15 19l-7-7 7-7" /></svg>
          </button>
          <button className="w-9 h-9 rounded-full border border-white/10 flex items-center justify-center hover:bg-white/5 transition-colors text-white/50 hover:text-white">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 5l7 7-7 7" /></svg>
          </button>
        </div>
      </div>

      <div className="grid grid-cols-4 gap-5">
        <DirectionCard num="01" image="/public_backup/assets/fashion_hero_1_1783581266482.png" direction="Royal Warmth" lighting="Directional, Golden Hour" mood="Opulent, Nostalgic" color="Gold, Deep Red" active onSelect={onSelectDirection} />
        <DirectionCard num="02" image="/public_backup/assets/fashion_hero_2_1783581276651.png" direction="Minimal Heritage" lighting="Soft, Diffused" mood="Contemporary, Clean" color="Ivory, Muted Gold" onSelect={onSelectDirection} />
        <DirectionCard num="03" image="/public_backup/assets/fashion_hero_3_1783581286733.png" direction="Cinematic Drama" lighting="High Contrast, Chiaroscuro" mood="Mysterious, Bold" color="Black, Silver, Crimson" onSelect={onSelectDirection} />
        <DirectionCard num="04" image="/public_backup/assets/fashion_hero_1_1783581266482.png" direction="Ethereal Romance" lighting="Backlit, Airy" mood="Dreamy, Soft" color="Pastel Pink, White Gold" onSelect={onSelectDirection} />
      </div>
    </div>
  );
}

function DirectionCard({ num, image, direction, lighting, mood, color, active, onSelect }: any) {
  return (
    <div onClick={onSelect} className={`flex flex-col gap-4 p-3 rounded-xl border ${active ? 'border-[var(--color-warm-ivory)]/40 bg-[var(--color-warm-ivory)]/5 shadow-[0_0_30px_rgba(240,230,210,0.02)]' : 'border-white/5 bg-white/5'} transition-all duration-300 cursor-pointer group hover:border-white/20 hover:-translate-y-1`}>
      <div className="aspect-[3/4] rounded-lg overflow-hidden relative">
        <img src={image} className="w-full h-full object-cover opacity-80 group-hover:opacity-100 transition-opacity duration-500 group-hover:scale-105" />
        <div className="absolute top-3 left-3 px-2 py-1 rounded bg-black/60 backdrop-blur-md text-[9px] uppercase tracking-wider text-white/80">{num}</div>
      </div>
      <div className="flex flex-col gap-3 px-1 pb-2">
        <h4 className={`text-[13px] font-medium tracking-wide ${active ? 'text-[var(--color-warm-ivory)]' : 'text-white/80'}`}>{direction}</h4>
        <div className="flex flex-col gap-1.5">
          <span className="text-[9px] text-white/30 uppercase tracking-[0.15em]">Lighting: <span className="text-white/60 lowercase tracking-normal font-sans ml-1">{lighting}</span></span>
          <span className="text-[9px] text-white/30 uppercase tracking-[0.15em]">Mood: <span className="text-white/60 lowercase tracking-normal font-sans ml-1">{mood}</span></span>
          <span className="text-[9px] text-white/30 uppercase tracking-[0.15em]">Color: <span className="text-white/60 lowercase tracking-normal font-sans ml-1">{color}</span></span>
        </div>
      </div>
    </div>
  );
}
