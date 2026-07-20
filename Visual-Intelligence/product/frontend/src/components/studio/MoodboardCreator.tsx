export function MoodboardCreator({ onSelectAsset }: { onSelectAsset: () => void }) {
  const images = [
    '/public_backup/assets/fashion_hero_1_1783581266482.png',
    '/public_backup/assets/fashion_hero_2_1783581276651.png',
    '/public_backup/assets/fashion_hero_3_1783581286733.png',
    '/public_backup/assets/fashion_hero_1_1783581266482.png',
    '/public_backup/assets/fashion_hero_2_1783581276651.png',
    '/public_backup/assets/fashion_hero_3_1783581286733.png',
  ];

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-end justify-between border-b border-white/5 pb-4">
        <div>
          <h2 className="font-serif text-[24px] text-white/90 mb-1">Generated Concepts</h2>
          <p className="text-[12px] text-white/40 tracking-wide">Direction 01: Royal Warmth - 6 iterations generated.</p>
        </div>
      </div>
      
      <div className="grid grid-cols-3 gap-6 pt-4">
        {images.map((img, idx) => (
          <div key={idx} className="group relative aspect-[3/4] rounded-xl overflow-hidden border border-white/5 bg-white/5 hover:border-[var(--color-warm-ivory)]/40 transition-all duration-500">
            <img src={img} className="w-full h-full object-cover opacity-80 group-hover:opacity-100 transition-opacity duration-500 group-hover:scale-105" />
            <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
              <button onClick={onSelectAsset} className="px-6 py-3 rounded bg-white/10 backdrop-blur-md border border-white/20 text-white text-[10px] uppercase tracking-wider hover:bg-[var(--color-warm-ivory)] hover:text-black transition-colors shadow-[0_0_30px_rgba(0,0,0,0.5)]">
                Select for Refinement
              </button>
            </div>
            <div className="absolute top-4 left-4 px-3 py-1.5 rounded bg-black/50 backdrop-blur-md border border-white/10 text-[9px] uppercase tracking-wider text-white/80">
              Iter {String(idx + 1).padStart(2, '0')}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
