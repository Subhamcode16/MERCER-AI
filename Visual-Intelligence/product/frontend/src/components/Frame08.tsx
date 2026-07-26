'use client';

import { useRef, useState } from 'react';
import gsap from 'gsap';
import { useGSAP } from '@gsap/react';
import { useRouter } from 'next/navigation';

export function Frame08() {
  const containerRef = useRef<HTMLDivElement>(null);
  const buttonRef = useRef<HTMLButtonElement>(null);
  const videoRef = useRef<HTMLVideoElement>(null);
  const arrowRef = useRef<HTMLSpanElement>(null);
  const glareRef = useRef<HTMLDivElement>(null);
  const ctaWrapperRef = useRef<HTMLDivElement>(null);

  const [isHovered, setIsHovered] = useState(false);
  const [isActive, setIsActive] = useState(false);
  const router = useRouter();

  // Initial appearance animation
  useGSAP(() => {
    gsap.fromTo(ctaWrapperRef.current,
      { opacity: 0, y: 30 },
      { opacity: 1, y: 0, duration: 1.8, delay: 1.5, ease: 'power3.out' }
    );
  }, { scope: containerRef });

  // Hover state animation
  useGSAP(() => {
    if (isHovered) {
      // Button stretches slightly
      gsap.to(buttonRef.current, {
        scale: 1.02,
        paddingRight: '3.5rem', // Stretch the right side to feel fluid
        duration: 0.4,
        ease: 'power2.out',
        boxShadow: '0 0 40px rgba(255,255,255,0.1), inset 0 0 20px rgba(255,255,255,0.2)',
        borderColor: 'rgba(255,255,255,0.4)',
        backdropFilter: 'blur(32px)'
      });

      // Glare sweeps across the button
      gsap.fromTo(glareRef.current, 
        { x: '-150%', opacity: 0.6 },
        { x: '250%', opacity: 0, duration: 0.7, ease: 'power2.inOut' }
      );

      // Arrow shoots out right, wraps around, and snaps back into place
      const tl = gsap.timeline();
      tl.to(arrowRef.current, { x: 30, opacity: 0, duration: 0.2, ease: 'power2.in' })
        .set(arrowRef.current, { x: -30 })
        .to(arrowRef.current, { x: 0, opacity: 1, duration: 0.3, ease: 'back.out(1.5)' });

    } else {
      gsap.to(buttonRef.current, {
        scale: 1,
        paddingRight: '2.5rem', // Revert to normal padding
        duration: 0.4,
        ease: 'power2.out',
        boxShadow: '0 0 20px rgba(255,255,255,0.0), inset 0 0 10px rgba(255,255,255,0.1)',
        borderColor: 'rgba(255,255,255,0.2)',
        backdropFilter: 'blur(24px)'
      });
      // Ensure arrow comes back to center if hovered out mid-animation
      gsap.to(arrowRef.current, { x: 0, opacity: 1, duration: 0.3, ease: 'power2.out' });
      gsap.set(glareRef.current, { opacity: 0 });
    }
  }, [isHovered]);

  // Click state animation and final transition
  const handleClick = () => {
    setIsActive(true);
    
    const tl = gsap.timeline();
    
    // Quick compress
    tl.to(buttonRef.current, {
      scale: 0.98,
      duration: 0.12,
      ease: 'power1.out'
    })
    // Release and dissolve button
    .to(buttonRef.current, {
      scale: 1.05,
      opacity: 0,
      duration: 0.5,
      ease: 'power2.inOut'
    })
    // Zoom into video to simulate walking through
    .to(videoRef.current, {
      scale: 1.5,
      duration: 2.5,
      ease: 'power2.inOut'
    }, '-=0.3')
    .to(containerRef.current, {
      opacity: 0,
      duration: 1,
      ease: 'power2.inOut',
      onComplete: () => {
        router.push('/studio');
      }
    }, '-=1.0');
  };

  return (
    <div 
      ref={containerRef} 
      className="fixed inset-0 z-[90] bg-black flex items-center justify-center overflow-hidden"
    >
      {/* Cinematic Widescreen Video Container */}
      <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
        <div 
          className="relative w-full overflow-hidden shadow-[0_0_100px_rgba(255,255,255,0.05)] border-y border-white/5"
          style={{ aspectRatio: '2.76 / 1' }}
        >
          <video 
            ref={videoRef}
            src="/videos/frame_08.mp4" 
            autoPlay 
            loop 
            muted 
            playsInline 
            className="absolute inset-0 w-full h-full object-cover origin-center"
            style={{ transform: 'scale(1.15)' }}
          />
          {/* Cinematic Vignette Overlay with center darkening for CTA contrast */}
          <div 
            className="absolute inset-0 pointer-events-none z-10" 
            style={{
              background: 'radial-gradient(ellipse at center, rgba(0,0,0,0.4) 0%, rgba(0,0,0,0.8) 100%)'
            }} 
          />
          
          {/* Film Grain */}
          <div 
            className="absolute inset-0 pointer-events-none z-20 opacity-[0.06] mix-blend-overlay"
            style={{ backgroundImage: `url('data:image/svg+xml,%3Csvg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg"%3E%3Cfilter id="noiseFilter"%3E%3CfeTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="3" stitchTiles="stitch"/%3E%3C/filter%3E%3Crect width="100%25" height="100%25" filter="url(%23noiseFilter)"/%3E%3C/svg%3E')` }}
          />
        </div>
      </div>
      
      {/* Liquid Glass CTA */}
      <div ref={ctaWrapperRef} className="relative z-50 opacity-0">
        {/* Ambient Pulse Glow */}
        <div className="absolute inset-0 rounded-full shadow-[0_0_40px_rgba(255,255,255,0.15)] animate-[pulse_4s_ease-in-out_infinite]" />
        
        <button
          ref={buttonRef}
          onMouseEnter={() => !isActive && setIsHovered(true)}
          onMouseLeave={() => !isActive && setIsHovered(false)}
          onClick={handleClick}
          disabled={isActive}
          style={{
            boxShadow: '0 0 20px rgba(255,255,255,0.0), inset 0 0 10px rgba(255,255,255,0.1)',
            borderColor: 'rgba(255,255,255,0.2)',
            backdropFilter: 'blur(24px)',
            paddingRight: '2.5rem'
          }}
          className="relative flex items-center p-2 rounded-full border border-white/20 bg-white/5 overflow-hidden group cursor-pointer select-none"
        >
        {/* Sweeping Glare */}
        <div 
          ref={glareRef}
          className="absolute top-0 bottom-0 left-0 w-24 bg-gradient-to-r from-transparent via-white/50 to-transparent skew-x-[-20deg] pointer-events-none opacity-0 z-20"
        />

        {/* Inner Arrow Container */}
        <div className="flex items-center justify-center w-14 h-14 rounded-full border border-white/10 bg-white/5 mr-6 shrink-0">
          <span ref={arrowRef} className="text-white transform transition-transform will-change-transform flex items-center justify-center">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M4 12H20M20 12L14 6M20 12L14 18" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </span>
        </div>
        
        {/* Text */}
        <span className="text-white uppercase text-[15px] tracking-[0.2em] font-medium opacity-95">
          Enter Mercer AI
        </span>
      </button>
    </div>
    </div>
  );
}
