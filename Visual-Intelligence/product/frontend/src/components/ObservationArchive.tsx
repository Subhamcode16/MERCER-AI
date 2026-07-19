'use client';

import { useMemo } from 'react';

interface ObservationArchiveProps {
  progress: number; // 0.0 to 1.0 specifically for this section
}

export function ObservationArchive({ progress }: ObservationArchiveProps) {
  const observations = useMemo(() => [
    { 
      id: '01', 
      title: 'MATERIAL STUDY', 
      desc: 'Understanding how woven fibres respond to light and gravity.',
      image: '/observations/obs_01.png'
    },
    { 
      id: '02', 
      title: 'BOTANICAL REFERENCE', 
      desc: 'Nature teaches proportion before design.',
      image: '/observations/obs_02.png'
    },
    { 
      id: '03', 
      title: 'LIGHT ANALYSIS', 
      desc: 'Light reveals structure before colour.',
      image: '/observations/obs_03.png'
    },
    { 
      id: '04', 
      title: 'HISTORICAL ARCHIVE', 
      desc: 'Every material carries cultural memory.',
      image: '/observations/obs_04.png'
    },
    { 
      id: '05', 
      title: 'HUMAN PERCEPTION', 
      desc: 'Texture influences emotion before language.',
      image: '/observations/obs_05.png'
    },
    { 
      id: '06', 
      title: 'VISUAL INTELLIGENCE', 
      desc: 'Observation becomes reusable knowledge.',
      image: '/observations/obs_06.png'
    }
  ], []);

  // Determine active observation based on progress
  // progress will typically be exactly 1.0 at the very end
  // We want to map 0-1 to 0-5 indices evenly.
  // Using Math.max to avoid -1 or out of bounds.
  const activeIndex = progress >= 1.0 
    ? observations.length - 1 
    : Math.max(0, Math.floor(progress * observations.length));

  return (
    <div className="w-full h-full flex font-sans text-[#E1D4C0]">
      {/* Left Column (45%) */}
      <div className="w-[45%] h-full flex flex-col pt-[18vh] pl-[8vw] pr-[4vw]">
        <h2 className="text-[12px] tracking-[0.28em] font-medium opacity-70 mb-10 uppercase">
          WORLD 01
          <br /><br />
          THE OBSERVATION
        </h2>
        
        <h1 className="font-serif font-bold text-[72px] lg:text-[88px] leading-[0.95] mb-12 text-[#E1D4C0]">
          Every Detail<br/>Becomes Knowledge.
        </h1>
        
        <div className="w-[40px] h-[1px] bg-[#E1D4C0]/20 mb-8" />

        <p className="text-[15px] leading-[1.7] opacity-90 max-w-[420px]">
          Observation is the beginning of intelligence.<br/>
          Every material, shadow, texture and form<br/>
          becomes structured knowledge before it<br/>
          becomes creativity.
        </p>

        <div className="mt-auto pb-[8vh] flex items-center gap-4">
          <span className="text-[10px] tracking-widest uppercase opacity-60">Scroll to continue reading</span>
          <div className="w-[100px] h-[1px] bg-[#E1D4C0]/20 relative overflow-hidden">
          </div>
        </div>
      </div>

      {/* Right Column (55%) */}
      <div className="w-[55%] h-full flex flex-col justify-center pr-[12vw] pl-[4vw] border-l border-[#E1D4C0]/20 bg-black/40 backdrop-blur-[4px]">
        <div className="flex flex-col">
          <div className="w-full h-[1px] bg-[#E1D4C0]/20" />
          {observations.map((obs, idx) => {
            const isActive = activeIndex === idx;
            return (
              <div key={obs.id} className="flex flex-col">
                <div 
                  className={`flex items-start py-8 transition-all duration-500 ease-out`}
                >
                  {/* Number */}
                  <div className="w-[60px] text-[15px] opacity-70 flex items-center pt-2 font-light">
                    {obs.id} <span className={`ml-4 w-[4px] h-[4px] rounded-full bg-[#E1D4C0] transition-opacity duration-500 ${isActive ? 'opacity-100' : 'opacity-0'}`} />
                  </div>
                  
                  {/* Content Container */}
                  <div className="flex-1 flex gap-8 relative">
                    {/* Thumbnail placeholder */}
                    <div 
                      className={`overflow-hidden transition-all duration-500 ease-out`}
                      style={{ 
                        width: isActive ? '140px' : '0px',
                        opacity: isActive ? 1 : 0
                      }}
                    >
                      <div className="w-[140px] h-[90px] bg-[#E1D4C0]/5 border border-[#E1D4C0]/10 shrink-0 relative overflow-hidden">
                        <img src={obs.image} alt={obs.title} className="w-full h-full object-cover opacity-90" />
                      </div>
                    </div>

                    {/* Text block */}
                    <div className="flex-1 flex flex-col justify-center">
                      <h3 className={`text-[15px] tracking-wider mb-2 uppercase transition-opacity duration-500 ${isActive ? 'opacity-100 font-medium' : 'opacity-50'}`}>
                        {obs.title}
                      </h3>
                      <div 
                        className={`overflow-hidden transition-all duration-500 ease-out`}
                        style={{
                          maxHeight: isActive ? '100px' : '0px',
                          opacity: isActive ? 0.8 : 0
                        }}
                      >
                        <p className="text-[14px] leading-[1.7] max-w-[280px]">
                          {obs.desc}
                        </p>
                      </div>
                    </div>
                    
                    {/* Arrow icon */}
                    <div className="w-[24px] flex justify-end pt-1">
                      <svg width="12" height="12" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg" className="opacity-40">
                        <path d="M1 11L11 1M11 1H3.5M11 1V8.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                      </svg>
                    </div>
                  </div>
                </div>
                {/* Divider */}
                <div className="w-full h-[1px] bg-[#E1D4C0]/20" />
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
