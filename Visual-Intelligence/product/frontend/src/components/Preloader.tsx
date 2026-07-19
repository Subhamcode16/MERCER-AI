'use client';

import { useEffect, useRef, useState } from 'react';
import gsap from 'gsap';

interface PreloaderProps {
  onComplete: () => void;
}

export function Preloader({ onComplete }: PreloaderProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const counterObj = useRef({ value: 0 });
  const [count, setCount] = useState(0);

  // refs for stages
  const stage1Ref = useRef<HTMLDivElement>(null);
  const ringRef = useRef<SVGCircleElement>(null);
  const stage2Ref = useRef<HTMLDivElement>(null);
  const titleRef = useRef<HTMLDivElement>(null);
  const subtitleRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Initial setup
    const circumference = 2 * Math.PI * 120; // r=120
    if (ringRef.current) {
      gsap.set(ringRef.current, { 
        strokeDasharray: circumference, 
        strokeDashoffset: circumference 
      });
    }
    
    // Create master timeline
    const tl = gsap.timeline({
      onComplete: () => {
        onComplete();
      }
    });

    // Stage 1: Counting and Ring
    tl.to(counterObj.current, {
      value: 100,
      duration: 2.8,
      ease: "power2.inOut",
      onUpdate: () => {
        setCount(Math.floor(counterObj.current.value));
      }
    }, "start")
    .to(ringRef.current, {
      strokeDashoffset: 0,
      duration: 2.8,
      ease: "power2.inOut"
    }, "start");

    // Exit Stage 1
    tl.to(stage1Ref.current, {
      opacity: 0,
      scale: 0.95,
      duration: 0.4,
      ease: "power2.out"
    }, "+=0.3");

    // Stage 2: The Flash Montage
    const images = stage2Ref.current?.querySelectorAll('img') || [];
    tl.set(stage2Ref.current, { opacity: 1 });
    
    // Rapidly flash each image
    images.forEach((img, i) => {
      // First image appears immediately, subsequent images delay by 0.1s
      tl.set(img, { opacity: 1 }, `+=${i === 0 ? 0 : 0.08}`);
      
      // Hide the image after 0.1s UNLESS it's the final image
      if (i < images.length - 1) {
        tl.set(img, { opacity: 0 }, `+=${0.08}`);
      }
    });

    // Stage 3: Title Reveal
    tl.fromTo(titleRef.current, {
      y: 40,
      opacity: 0
    }, {
      y: 0,
      opacity: 1,
      duration: 1.2,
      ease: "power3.out"
    }, "+=0.1")
    .fromTo(subtitleRef.current, {
      y: 20,
      opacity: 0
    }, {
      y: 0,
      opacity: 1,
      duration: 1,
      ease: "power3.out"
    }, "-=0.8");

    // Hold the hero title for reading
    tl.to({}, { duration: 1.5 });

    // Stage 4: Curtain Reveal
    tl.to(containerRef.current, {
      yPercent: -100,
      duration: 1.2,
      ease: "power4.inOut"
    });

    return () => {
      tl.kill();
    };
  }, [onComplete]);

  // Format count to always be at least 2 digits (e.g. 00, 05, 99, 100)
  const displayCount = count < 10 ? `0${count}` : count.toString();

  return (
    <div 
      ref={containerRef}
      className="fixed inset-0 z-[100] bg-[#0f0f0f] flex items-center justify-center overflow-hidden"
    >
      
      {/* Stage 1: Progress Circle */}
      <div ref={stage1Ref} className="absolute flex flex-col items-center justify-center">
        <div className="relative flex items-center justify-center w-[300px] h-[300px]">
          <svg className="absolute inset-0 w-full h-full -rotate-90" viewBox="0 0 300 300">
            {/* Background Track */}
            <circle cx="150" cy="150" r="120" stroke="#222" strokeWidth="1" fill="none" />
            {/* Animated Progress Ring */}
            <circle 
              ref={ringRef}
              cx="150" cy="150" r="120" 
              stroke="#E1D4C0" strokeWidth="1.5" fill="none" 
              strokeLinecap="round"
            />
          </svg>
          <span className="font-serif text-[#E1D4C0] text-7xl font-medium tracking-tighter tabular-nums">
            {displayCount}
          </span>
        </div>
        <span className="mt-8 text-[11px] uppercase tracking-[0.2em] text-[#E1D4C0]/50 font-medium">
          Loading...
        </span>
      </div>

      {/* Stage 2 & 3: Flash Montage & Hero Title */}
      <div ref={stage2Ref} className="absolute inset-0 flex items-center justify-center opacity-0 pointer-events-none">
        
        {/* Portrait Container for Images */}
        <div className="relative w-[320px] h-[480px] overflow-hidden">
          <img src="/preloader/audience.png" alt="" className="absolute inset-0 w-full h-full object-cover opacity-0 grayscale contrast-125" />
          <img src="/preloader/campaign-direction.png" alt="" className="absolute inset-0 w-full h-full object-cover opacity-0 grayscale contrast-125" />
          <img src="/preloader/culture.png" alt="" className="absolute inset-0 w-full h-full object-cover opacity-0 grayscale contrast-125" />
          <img src="/preloader/editorial-refs.png" alt="" className="absolute inset-0 w-full h-full object-cover opacity-0 grayscale contrast-125" />
          <img src="/preloader/material-dna.png" alt="" className="absolute inset-0 w-full h-full object-cover opacity-0 grayscale contrast-125 brightness-75" />
        </div>

        {/* Hero Title */}
        <div 
          ref={titleRef} 
          className="absolute text-[#E1D4C0] font-serif text-[120px] font-bold z-10 drop-shadow-2xl"
        >
          ATELIER
        </div>

        {/* Subtitle */}
        <div 
          ref={subtitleRef}
          className="absolute bottom-[25vh] text-[#E1D4C0] text-sm font-medium tracking-widest uppercase z-10"
        >
          the creative intelligence.
        </div>
        
      </div>
    </div>
  );
}
