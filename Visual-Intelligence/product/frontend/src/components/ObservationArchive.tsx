'use client';

import { useMemo } from 'react';

interface ObservationArchiveProps {
  progress: number; // 0.0 to 1.0 specifically for this section
  isVisible?: boolean;
}

export function ObservationArchive({ progress, isVisible = false }: ObservationArchiveProps) {
  const observations = useMemo(() => [
    { 
      id: '01', 
      title: 'Material Study', 
      image: '/observations/obs_01.png'
    },
    { 
      id: '02', 
      title: 'Botanical Reference', 
      image: '/observations/obs_02.png'
    },
    { 
      id: '03', 
      title: 'Light Analysis', 
      image: '/observations/obs_03.png'
    },
    { 
      id: '04', 
      title: 'Historical Archive', 
      image: '/observations/obs_04.png'
    },
    { 
      id: '05', 
      title: 'Human Perception', 
      image: '/observations/obs_05.png'
    },
    { 
      id: '06', 
      title: 'Visual Intelligence', 
      image: '/observations/obs_06.png'
    }
  ], []);

  // Determine active observation based on progress
  const activeIndex = progress >= 1.0 
    ? observations.length - 1 
    : Math.max(0, Math.floor(progress * observations.length));

  return (
    <div className={`w-full h-screen flex flex-col font-sans text-[#E1D4C0] bg-black relative overflow-hidden t-stagger ${isVisible ? 'is-shown' : 'is-hiding'}`}>
      
      {/* Header (Top Center) */}
      <div className="t-stagger-line t-stagger-line--1 absolute top-[10vh] left-0 w-full flex flex-col items-center text-center z-20 px-4">
        <h1 className="font-serif font-bold text-[64px] lg:text-[88px] leading-[1] mb-6 text-[#E1D4C0]">
          Every details becomes <span className="italic">knowledge</span>
        </h1>
        <p className="text-[15px] leading-[1.7] opacity-60 max-w-[600px] text-[#E1D4C0] font-light">
          Observation is the beginning of intelligence. Every material, shadow, texture and form becomes structured knowledge before it becomes creativity.
        </p>
      </div>

      {/* Main Two-Column Layout */}
      <div className="flex-1 flex w-full pt-[20vh]">
        
        {/* Left Column: Typographic Slider (3D Ring) */}
        <div 
          className="t-stagger-line t-stagger-line--2 w-[50%] h-full flex flex-col justify-center pl-[12vw] relative" 
          style={{ perspective: '1200px' }}
        >
          {/* Relative wrapper for absolute items */}
          <div className="relative w-full h-[100px] flex items-center" style={{ transformStyle: 'preserve-3d' }}>
            {observations.map((obs, idx) => {
              const offset = idx - activeIndex;
              const isActive = offset === 0;
              
              // 3D Ring Math
              const rotateX = offset * -15; // Milder tilt angle
              const translateZ = Math.abs(offset) * -50; // Push inactive items back
              const translateY = offset * 90; // Larger vertical spacing for bigger text
              
              // Visual fading and blurring based on distance from center
              const opacity = isActive ? 1 : Math.max(0, 0.4 - Math.abs(offset) * 0.15);
              const blur = isActive ? 0 : Math.min(12, Math.abs(offset) * 3);
              const scale = isActive ? 1 : Math.max(0.8, 1 - Math.abs(offset) * 0.05);

              return (
                <div 
                  key={obs.id} 
                  className="absolute left-0 w-full flex items-center transition-all duration-700 ease-[cubic-bezier(0.16,1,0.3,1)]"
                  style={{
                    transform: `translateY(${translateY}px) translateZ(${translateZ}px) rotateX(${rotateX}deg) scale(${scale})`,
                    opacity: opacity,
                    filter: `blur(${blur}px)`,
                    transformOrigin: 'center center',
                  }}
                >
                  <h2 className={`text-[56px] lg:text-[72px] transition-all duration-500 ease-out flex items-center ${
                    isActive ? 'font-bold text-white tracking-tight' : 'font-bold text-[#E1D4C0]'
                  }`}>
                    {/* Arrow Indicator for Active Item */}
                    <div className={`overflow-hidden transition-all duration-500 flex items-center ${
                      isActive ? 'w-[60px] opacity-100 mr-2' : 'w-0 opacity-0 mr-0'
                    }`}>
                      <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className="text-white shrink-0">
                        <path d="M4 12H20M20 12L14 6M20 12L14 18" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/>
                      </svg>
                    </div>
                    {obs.title}
                  </h2>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right Column: Image Showcase */}
        <div className="t-stagger-line t-stagger-line--3 w-[50%] h-full flex items-center justify-center pr-[12vw] relative">
          {observations.map((obs, idx) => {
            const isActive = activeIndex === idx;
            return (
              <div 
                key={obs.id}
                className={`absolute transition-opacity duration-700 ease-in-out ${
                  isActive ? 'opacity-100 z-10' : 'opacity-0 z-0'
                }`}
              >
                <div className="w-[400px] h-[500px] bg-[#111] overflow-hidden relative">
                  <img 
                    src={obs.image} 
                    alt={obs.title} 
                    className="w-full h-full object-cover opacity-90 transition-transform duration-[20s] ease-out hover:scale-105"
                  />
                  {/* Subtle inner border overlay */}
                  <div className="absolute inset-0 border border-[#E1D4C0]/10 pointer-events-none" />
                </div>
              </div>
            );
          })}
        </div>

      </div>
    </div>
  );
}
