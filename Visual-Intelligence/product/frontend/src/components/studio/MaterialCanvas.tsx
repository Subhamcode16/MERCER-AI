export function MaterialCanvas() {
  return (
    <div className="flex gap-10">
      {/* Material Image */}
      <div className="flex-[2] rounded-xl overflow-hidden bg-white/5 border border-white/10 aspect-video relative group">
        <img src="/public_backup/assets/fashion_hero_1_1783581266482.png" className="w-full h-full object-cover opacity-90 group-hover:opacity-100 transition-opacity duration-700" />
        <div className="absolute top-5 left-5 flex gap-2">
          <div className="px-3 py-1.5 rounded bg-black/60 backdrop-blur-md text-[9px] uppercase tracking-[0.2em] border border-white/10 text-white/80">Base Material</div>
        </div>
        <div className="absolute bottom-5 right-5 w-8 h-8 rounded-full bg-black/40 backdrop-blur-md border border-white/10 flex items-center justify-center cursor-pointer hover:bg-black/60 transition-colors">
          <svg className="w-3.5 h-3.5 text-white/70" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" /></svg>
        </div>
      </div>

      {/* Analysis & Context */}
      <div className="flex-1 flex flex-col gap-10">
        <div>
          <h3 className="text-[9px] tracking-[0.25em] uppercase text-white/40 mb-5 border-b border-white/5 pb-3">Material Analysis</h3>
          <div className="grid grid-cols-2 gap-y-6 gap-x-6">
            <DataPoint label="Fabric" value="Silk" />
            <DataPoint label="Weave" value="Kadhua" />
            <DataPoint label="Primary Motifs" value="Floral" />
            <DataPoint label="Technique" value="Handwoven" />
            <DataPoint label="Lustre" value="High" />
            <DataPoint label="Weight" value="Heavy" />
          </div>
        </div>

        <div>
          <h3 className="text-[9px] tracking-[0.25em] uppercase text-white/40 mb-5 border-b border-white/5 pb-3">Campaign Context</h3>
          <div className="grid grid-cols-2 gap-y-6 gap-x-6">
            <DataPoint label="Brand Personality" value="Heritage Luxury" />
            <DataPoint label="Target Audience" value="HNI" />
            <DataPoint label="Occasion" value="Bridal / Festive" />
            <DataPoint label="Location Mood" value="Palatial" />
            <DataPoint label="Season" value="Autumn/Winter" />
            <DataPoint label="Objective" value="Brand Elevation" />
          </div>
        </div>
      </div>
    </div>
  );
}

function DataPoint({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex flex-col gap-1.5">
      <span className="text-[9px] uppercase tracking-[0.15em] text-white/30">{label}</span>
      <span className="text-[13px] text-white/80">{value}</span>
    </div>
  );
}
