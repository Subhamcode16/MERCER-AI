'use client';

import { useEffect, useState, useRef } from 'react';
import Link from 'next/link';
import { ScrollSequence } from '@/components/ScrollSequence';
import { Preloader } from '@/components/Preloader';
import { ObservationArchive } from '@/components/ObservationArchive';
import { CinematicEnding } from '@/components/CinematicEnding';
import { Frame08 } from '@/components/Frame08';
import { PricingSection } from '@/components/PricingSection';
import { ContactSection } from '@/components/ContactSection';
import { Footer } from '@/components/Footer';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useGSAP } from '@gsap/react';

if (typeof window !== 'undefined') {
  gsap.registerPlugin(ScrollTrigger);
}

export default function Home() {
  const containerRef = useRef<HTMLDivElement>(null);
  const sequence01to03Ref = useRef<HTMLDivElement>(null);
  const frame06BgRef = useRef<HTMLDivElement>(null);
  const frame04UIRef = useRef<HTMLDivElement>(null);

  useGSAP(() => {
    gsap.set(frame04UIRef.current, { yPercent: 100, opacity: 1 });
    gsap.set(sequence01to03Ref.current, { yPercent: 0 });
  }, { scope: containerRef });

  const [globalScrollProgress, setGlobalScrollProgress] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const [showEnding, setShowEnding] = useState(false);
  const [showFrame08, setShowFrame08] = useState(false);
  const [isExitingEnding, setIsExitingEnding] = useState(false);
  const [frame02Revealed, setFrame02Revealed] = useState(false);
  const endingContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (globalScrollProgress > 0.995 && !showEnding && !showFrame08) {
      setShowEnding(true);
      setIsExitingEnding(false);
    } else if (globalScrollProgress <= 0.995 && (showEnding || showFrame08) && !isExitingEnding) {
      setIsExitingEnding(true);
    }
  }, [globalScrollProgress, showEnding, showFrame08, isExitingEnding]);

  useEffect(() => {
    if (globalScrollProgress >= 0.173 && globalScrollProgress < 0.340) {
      if (!frame02Revealed) {
        const timer = setTimeout(() => {
          setFrame02Revealed(true);
        }, 25);
        return () => clearTimeout(timer);
      }
    } else if (globalScrollProgress < 0.160) {
      setFrame02Revealed(false);
    }
  }, [globalScrollProgress, frame02Revealed]);

  useGSAP(() => {
    if (isExitingEnding && endingContainerRef.current) {
      gsap.to(endingContainerRef.current, {
        opacity: 0,
        duration: 0.8,
        ease: 'power2.out',
        onComplete: () => {
          setShowEnding(false);
          setShowFrame08(false);
          setIsExitingEnding(false);
        }
      });
    } else if (!isExitingEnding && endingContainerRef.current) {
      gsap.set(endingContainerRef.current, { opacity: 1 });
    }
  }, [isExitingEnding]);

  // Scale factor: The first 1400vh of the new 1700vh scrollable distance maps perfectly to the old 0-1.0 logic.
  const scrollProgress = globalScrollProgress * (1700 / 1400);

  useEffect(() => {
    let targetY = 100;
    let sequenceY = 0;
    let targetOpacity = 1;
    
    // Frame 04 & Frame 03 Slide Up Transition (0.486 to 0.513)
    if (scrollProgress >= 0.486 && scrollProgress <= 0.513) {
      targetY = 100 - ((scrollProgress - 0.486) / 0.027) * 100;
      sequenceY = - ((scrollProgress - 0.486) / 0.027) * 100;
    } else if (scrollProgress > 0.513) {
      targetY = 0;
      sequenceY = -100;
    }

    // Frame 04 Fades out into Frame 05 (0.646 to 0.666)
    if (scrollProgress > 0.646 && scrollProgress <= 0.666) {
      targetOpacity = Math.max(0, 1 - ((scrollProgress - 0.646) / 0.020));
    } else if (scrollProgress > 0.666) {
      targetOpacity = 0;
    } else {
      targetOpacity = 1;
    }
    
    // Frame 06 Dolly (Scale from 1.0 to 1.02 over its active scroll window)
    if (scrollProgress > 0.833) {
      const frame06Progress = Math.min(1, (scrollProgress - 0.833) / 0.167); // 0 to 1
      gsap.set(frame06BgRef.current, {
        scale: 1.0 + (frame06Progress * 0.02)
      });
    } else {
      gsap.set(frame06BgRef.current, { scale: 1.0 });
    }
    
    // Animate Frame 03 sliding up
    if (sequence01to03Ref.current) {
      gsap.to(sequence01to03Ref.current, {
        yPercent: sequenceY,
        duration: 0.8,
        ease: 'power2.out',
        overwrite: 'auto'
      });
    }
    
    // Animate Frame 04 sliding up and eventually fading out
    if (frame04UIRef.current) {
      gsap.to(frame04UIRef.current, {
        yPercent: targetY,
        opacity: targetOpacity,
        duration: 0.8,
        ease: 'power2.out',
        overwrite: 'auto'
      });
    }
  }, [scrollProgress]);

  // Track window scroll
  useEffect(() => {
    // Force scroll to top on mount to avoid being stuck at the bottom
    if (typeof window !== 'undefined' && 'scrollRestoration' in history) {
      history.scrollRestoration = 'manual';
    }
    window.scrollTo(0, 0);

    const handleScroll = () => {
      if (!containerRef.current) return;
      
      // The total scrollable distance of the World I sequence is the container height minus window height
      const scrollableDistance = containerRef.current.clientHeight - window.innerHeight;
      
      // Calculate progress from 0.0 to 1.0, capping at 1 so the final frame holds
      if (scrollableDistance > 0) {
        const progress = Math.min(1, Math.max(0, window.scrollY / scrollableDistance));
        setGlobalScrollProgress(progress);
      }
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    // Initial call
    handleScroll();

    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Stagger reveal orchestration after preloader finishes
  useEffect(() => {
    if (!isLoading) {
      // Small timeout allows DOM to settle after preloader unmounts
      const timer = setTimeout(() => {
        const block = document.querySelector(".t-stagger");
        if (block) {
          block.classList.remove("is-hiding", "is-shown");
          void (block as HTMLElement).offsetHeight; // reflow
          block.classList.add("is-shown");
        }
      }, 50);
      return () => clearTimeout(timer);
    }
  }, [isLoading]);

  // Calculate UI opacities based on scroll progress
  // Scale factor: 1250vh / 1500vh = 0.8333
  const frame01Opacity = scrollProgress < 0.026 ? 1 : Math.max(0, 1 - ((scrollProgress - 0.026) * (1 / 0.040)));
  
  // Transition Phase: Fade to Black between Frame sequences
  let blackFadeOpacity = 0;
  if (scrollProgress > 0.153 && scrollProgress <= 0.160) {
    blackFadeOpacity = (scrollProgress - 0.153) / 0.007;
  } else if (scrollProgress > 0.160 && scrollProgress <= 0.173) {
    blackFadeOpacity = 1; 
  } else if (scrollProgress > 0.173 && scrollProgress <= 0.180) {
    blackFadeOpacity = 1 - ((scrollProgress - 0.173) / 0.007); 
  } else if (scrollProgress > 0.320 && scrollProgress <= 0.326) {
    blackFadeOpacity = (scrollProgress - 0.320) / 0.006; 
  } else if (scrollProgress > 0.326 && scrollProgress <= 0.340) {
    blackFadeOpacity = 1; 
  } else if (scrollProgress > 0.340 && scrollProgress <= 0.346) {
    blackFadeOpacity = 1 - ((scrollProgress - 0.340) / 0.006); 
  } else if (scrollProgress > 0.653 && scrollProgress <= 0.660) {
    blackFadeOpacity = (scrollProgress - 0.653) / 0.007; 
  } else if (scrollProgress > 0.660 && scrollProgress <= 0.666) {
    blackFadeOpacity = 1; 
  } else if (scrollProgress > 0.666 && scrollProgress <= 0.673) {
    blackFadeOpacity = 1 - ((scrollProgress - 0.666) / 0.007); 
  } else if (scrollProgress > 0.816 && scrollProgress <= 0.823) {
    blackFadeOpacity = (scrollProgress - 0.816) / 0.007; 
  } else if (scrollProgress > 0.823 && scrollProgress <= 0.833) {
    blackFadeOpacity = 1; 
  } else if (scrollProgress > 0.833 && scrollProgress <= 0.840) {
    blackFadeOpacity = 1 - ((scrollProgress - 0.833) / 0.007); 
  }

  // Frame 02 UI & Video Scale
  let frame02Opacity = 0;
  let frame02VideoScaleProgress = 0;
  if (scrollProgress >= 0.173 && scrollProgress <= 0.230) {
    frame02Opacity = 1; 
  } else if (scrollProgress > 0.230 && scrollProgress <= 0.250) {
    frame02Opacity = Math.max(0, 1 - ((scrollProgress - 0.230) / 0.020));
    frame02VideoScaleProgress = (scrollProgress - 0.230) / 0.020;
  } else if (scrollProgress > 0.250) {
    frame02VideoScaleProgress = 1;
  }

  // Frame 03 UI
  let frame03Opacity = 0;
  if (scrollProgress >= 0.346 && scrollProgress <= 0.373) {
    frame03Opacity = (scrollProgress - 0.346) / 0.027;
  } else if (scrollProgress > 0.373 && scrollProgress <= 0.473) {
    frame03Opacity = 1;
  } else if (scrollProgress > 0.473 && scrollProgress <= 0.486) {
    frame03Opacity = Math.max(0, 1 - ((scrollProgress - 0.473) / 0.013));
  }

  // Frame 04 UI logic
  const frame04LocalProgress = Math.max(0, (scrollProgress - 0.513) / 0.133);

  // Frame 05 UI logic
  let frame05Opacity = 0;
  if (scrollProgress >= 0.666 && scrollProgress <= 0.683) {
    frame05Opacity = (scrollProgress - 0.666) / 0.017;
  } else if (scrollProgress > 0.683 && scrollProgress <= 0.800) {
    frame05Opacity = 1;
  } else if (scrollProgress > 0.800 && scrollProgress <= 0.816) {
    frame05Opacity = Math.max(0, 1 - ((scrollProgress - 0.800) / 0.016));
  }

  // Frame 06 UI logic
  let frame06Opacity = 0;
  if (scrollProgress >= 0.840 && scrollProgress <= 0.860) {
    frame06Opacity = (scrollProgress - 0.840) / 0.020;
  } else if (scrollProgress > 0.860 && scrollProgress <= 0.980) {
    frame06Opacity = 1;
  } else if (scrollProgress > 0.980) {
    frame06Opacity = Math.max(0, 1 - ((scrollProgress - 0.980) / 0.020));
  }

  // Frame 06 Background Fade out
  let frame06BgOpacity = 0;
  if (scrollProgress > 0.833 && scrollProgress <= 0.980) {
    frame06BgOpacity = 1;
  } else if (scrollProgress > 0.980) {
    frame06BgOpacity = Math.max(0, 1 - ((scrollProgress - 0.980) / 0.020));
  }

  // Frame 05 to 06 Black Transition
  let frame05to06Fade = 0;
  if (globalScrollProgress > 0.807 && globalScrollProgress <= 0.825) {
    frame05to06Fade = (globalScrollProgress - 0.807) / 0.018;
  } else if (globalScrollProgress > 0.825 && globalScrollProgress <= 0.845) {
    frame05to06Fade = 1;
  } else if (globalScrollProgress > 0.845 && globalScrollProgress <= 0.890) {
    frame05to06Fade = 1 - ((globalScrollProgress - 0.845) / 0.045);
  }

  // Frame 07 UI logic
  let frame07Opacity = 0;
  if (globalScrollProgress >= 0.900 && globalScrollProgress <= 0.950) {
    frame07Opacity = (globalScrollProgress - 0.900) / 0.050;
  } else if (globalScrollProgress > 0.950) {
    frame07Opacity = 1;
  }

  return (
    <>
      {/* Preloader */}
      {isLoading && <Preloader onComplete={() => setIsLoading(false)} />}
      
      {/* Cinematic Ending and Frame 08 Wrapper */}
      {(showEnding || showFrame08 || isExitingEnding) && (
        <div ref={endingContainerRef} className="fixed inset-0 z-[100]">
          {/* Frame 08 Sequence - mounts underneath CinematicEnding */}
          {(showEnding || showFrame08) && <Frame08 />}

          {/* Cinematic Ending Sequence */}
          {showEnding && <CinematicEnding onComplete={() => {
            setShowFrame08(true);
            setShowEnding(false);
          }} />}
        </div>
      )}

      {/* Virtual scroll container (1800vh gives us plenty of scroll distance to scrub sequences smoothly) */}
      <div ref={containerRef} className="w-full" style={{ height: '1800vh' }}>
        
        {/* Frame 05-07 Static Background Layer (Behind everything) */}
        <div className="fixed inset-0 z-[1] bg-black">
          {scrollProgress >= 0.666 && scrollProgress < 0.830 ? (
            <ScrollSequence 
              progress={Math.min(1, Math.max(0, (scrollProgress - 0.666) / 0.167))} 
              frameCount={192} 
              basePath="/frames_05" 
              imagePrefix="frame-"
            />
          ) : scrollProgress >= 0.830 ? (
            <ScrollSequence 
              progress={Math.min(1, Math.max(0, (globalScrollProgress * 1700 - 1400) / 300))} 
              frameCount={240} 
              basePath="/frames_07" 
              imagePrefix="frame-"
            />
          ) : null}
        </div>

        {/* Frame 01-03 Background Layer (Slides Up) */}
        <div 
          ref={sequence01to03Ref}
          className="fixed inset-0 z-[2] bg-black"
        >
          {scrollProgress < 0.173 ? (
            <ScrollSequence progress={Math.min(1, scrollProgress / 0.160)} frameCount={80} basePath="/frames" />
          ) : scrollProgress < 0.340 ? (
            <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
              <div 
                className="relative overflow-hidden bg-black"
                style={{
                  width: `${Math.min(100, 45 + frame02VideoScaleProgress * 55)}vw`,
                  height: `${Math.min(100, 35 + frame02VideoScaleProgress * 65)}vh`,
                  borderRadius: `${Math.max(0, 8 - frame02VideoScaleProgress * 8)}px`,
                  transition: 'width 0.1s linear, height 0.1s linear, border-radius 0.1s linear'
                }}
              >
                <video 
                  src="/videos/frame_02.mp4" 
                  autoPlay 
                  loop 
                  muted 
                  playsInline 
                  className="absolute inset-0 w-full h-full object-cover"
                />
              </div>
            </div>
          ) : scrollProgress < 0.666 ? (
            <ScrollSequence progress={Math.min(1, Math.max(0, (scrollProgress - 0.340) / 0.160))} frameCount={80} basePath="/frames_03" />
          ) : null}
        </div>

        {/* Transition Black Fade Layer (Applies to all sequences) */}
        <div 
          className="fixed inset-0 z-[5] bg-black pointer-events-none"
          style={{ opacity: blackFadeOpacity }}
        />

      {/* Atmospheric Gradients & Vignette (Fixed over the canvas) */}
      <div className="fixed inset-0 z-10 pointer-events-none">
        {/* Enhanced Vignettes based on user markings */}
        <div className="absolute inset-y-0 left-0 w-[45%] bg-gradient-to-r from-black/80 via-black/30 to-transparent" />
        <div className="absolute inset-y-0 right-0 w-[50%] bg-gradient-to-l from-black via-black/60 to-transparent" />
        <div className="absolute inset-x-0 top-0 h-[35%] bg-gradient-to-b from-black/70 via-black/20 to-transparent" />
        <div className="absolute inset-x-0 bottom-0 h-1/2 bg-gradient-to-t from-black/60 via-black/20 to-transparent" />
        <div className="absolute inset-0 shadow-[inset_0_0_250px_rgba(0,0,0,0.7)]" />
      </div>

      {/* Frame 01 UI Layer (Fixed, Fades Out) */}
      <div 
        className="fixed inset-0 z-20 flex flex-col pointer-events-none t-stagger"
        style={{ 
          opacity: frame01Opacity,
          pointerEvents: frame01Opacity > 0.5 ? 'auto' : 'none',
          transition: 'opacity 0.1s linear' // Very short transition to smooth out scroll steps slightly without lagging
        }}
      >
        {/* Logo */}
        <div className="t-stagger-line t-stagger-line--1 absolute top-[6vh] left-[8vw] max-w-[120px] font-sans font-bold tracking-widest text-sm opacity-90">
          ATELIER
        </div>
        
        {/* Navigation */}
        <nav className="t-stagger-line t-stagger-line--1 absolute top-[6vh] right-[8vw] flex gap-[40px] text-[15px] font-normal opacity-85">
          {['Institute', 'Research', 'Manifesto', 'Atlas'].map((item) => (
            <a key={item} href="#" className="hover:opacity-100 transition-opacity duration-300">
              {item}
            </a>
          ))}
        </nav>

        <main className="absolute top-[18vh] left-[8vw] max-w-[680px]">
          <h2 className="t-stagger-line t-stagger-line--2 text-[12px] tracking-[0.28em] font-medium opacity-70 mb-10 text-[#E1D4C0]">
            CREATIVE INTELLIGENCE INSTITUTE
          </h2>
          
          <h1 className="t-stagger-line t-stagger-line--3 font-serif font-bold text-[72px] lg:text-[88px] leading-[0.95] max-w-[620px] mb-12">
            Where <span className="italic">Creativity</span><br/>Becomes Intelligence
          </h1>
          
          <p className="t-stagger-line t-stagger-line--4 text-[15px] leading-[1.8] opacity-90 max-w-[520px] mb-14">
            The world's first creative institution where materials, research and intelligence converge to shape what has never existed before.
          </p>

          <Link href="/studio">
            <button className="t-stagger-line t-stagger-line--5 h-[52px] px-[32px] pointer-events-auto rounded-[14px] border border-[#E1D4C0]/20 bg-[#E1D4C0]/5 backdrop-blur-sm hover:bg-[#E1D4C0]/10 transition-colors duration-300 text-sm font-medium">
              Enter Studio
            </button>
          </Link>
        </main>

        <div className="t-stagger-line t-stagger-line--6 absolute bottom-[4vh] left-1/2 -translate-x-1/2 flex flex-col items-center opacity-60">
          <span className="text-[10px] tracking-widest uppercase mb-4">Scroll to Enter</span>
          <div className="w-[1px] h-[40px] bg-[#E1D4C0]/30 relative overflow-hidden">
            <div className="absolute top-0 left-0 w-full h-[50%] bg-[#E1D4C0] animate-[scrollLine_2s_ease-in-out_infinite]" />
          </div>
        </div>
      </div>

      {/* Frame 02 UI Layer */}
      <div 
        className="fixed inset-0 z-30 flex flex-col pointer-events-none items-center justify-center"
        style={{ 
          opacity: frame02Opacity,
          pointerEvents: frame02Opacity > 0.5 ? 'auto' : 'none',
          transition: 'opacity 0.1s linear'
        }}
      >
        <main className="absolute inset-0 flex flex-col items-center justify-between py-[12vh] px-8 text-center">
          {/* Top Section */}
          <div className="flex flex-col items-center">
            <h2 
              className="text-[12px] tracking-[0.28em] font-medium opacity-70 mb-6 text-[#E1D4C0] uppercase"
              style={{
                clipPath: frame02Revealed ? `inset(0% 0% 0% 0%)` : `inset(100% 0% 0% 0%)`,
                transition: 'clip-path 1.2s cubic-bezier(0.22, 1, 0.36, 1) 0s'
              }}
            >
              WORLD 01 · THE FIRST BREATH
            </h2>
            <h1 
              className="font-serif font-bold text-[64px] lg:text-[76px] leading-[0.95]"
              style={{
                clipPath: frame02Revealed ? `inset(0% 0% 0% 0%)` : `inset(100% 0% 0% 0%)`,
                transition: 'clip-path 1.2s cubic-bezier(0.22, 1, 0.36, 1) 0.15s'
              }}
            >
              Every Great Creation<br/>Begins With <span className="italic">Observation</span>
            </h1>
          </div>
          
          {/* Bottom Section */}
          <div className="flex flex-col items-center max-w-[520px]">
            <p 
              className="text-[15px] leading-[1.8] opacity-90"
              style={{
                clipPath: frame02Revealed ? `inset(0% 0% 0% 0%)` : `inset(100% 0% 0% 0%)`,
                transition: 'clip-path 1.2s cubic-bezier(0.22, 1, 0.36, 1) 0.3s'
              }}
            >
              Before imagination comes understanding. Every material, every shadow and every texture carries intelligence waiting to be discovered.
            </p>
          </div>
        </main>
      </div>

      {/* Frame 03 UI Layer */}
      <div 
        className="fixed inset-0 z-40 flex flex-col pointer-events-none"
        style={{ 
          opacity: frame03Opacity,
          pointerEvents: frame03Opacity > 0.5 ? 'auto' : 'none',
          transition: 'opacity 0.1s linear'
        }}
      >
        <main className="absolute top-[18vh] left-[8vw] max-w-[680px]">
          <h2 className="text-[12px] tracking-[0.28em] font-medium opacity-70 mb-10 text-[#E1D4C0] uppercase">
            WORLD 01 · MATTER AWAKENS
          </h2>
          
          <h1 className="font-serif font-bold text-[72px] lg:text-[88px] leading-[0.95] max-w-[620px] mb-12">
            Materials <span className="italic">Speak</span><br/>Before They Are Designed
          </h1>
          
          <p className="text-[15px] leading-[1.8] opacity-90 max-w-[520px]">
            Every fibre carries structure, every shadow reveals behaviour, and every texture communicates long before a designer makes a decision.
          </p>
        </main>
      </div>

      {/* Frame 04 UI Layer (Fixed, Slides In from bottom pushing Frame 03 up) */}
      <div 
        ref={frame04UIRef}
        className={`fixed inset-0 z-50 ${scrollProgress >= 0.486 && scrollProgress <= 0.666 ? 'pointer-events-auto' : 'pointer-events-none'}`}
      >
        <ObservationArchive 
          progress={frame04LocalProgress} 
          isVisible={scrollProgress >= 0.50 && scrollProgress <= 0.666}
        />
      </div>

      {/* Frame 05 UI Layer */}
      <div 
        className="fixed inset-0 z-[60] flex flex-col pointer-events-none t-stagger"
        style={{ 
          opacity: frame05Opacity,
          pointerEvents: frame05Opacity > 0.5 ? 'auto' : 'none',
          transition: 'opacity 0.1s linear'
        }}
      >
        <main className="absolute top-[18vh] left-[8vw] max-w-[680px]">
          <h2 className="text-[12px] tracking-[0.28em] font-medium opacity-70 mb-10 text-[#E1D4C0] uppercase">
            WORLD 01 · THE CREATIVE GALLERY
          </h2>
          
          <h1 className="font-serif font-bold text-[72px] lg:text-[88px] leading-[0.95] max-w-[620px] mb-12">
            Intelligence<br/>Becomes <span className="italic">Expression.</span>
          </h1>
          
          <p className="text-[15px] leading-[1.8] opacity-90 max-w-[520px]">
            Every campaign begins long before a camera is lifted. Observation becomes research, research becomes understanding, and understanding becomes imagery. The gallery is simply the visible result.
          </p>
        </main>
      </div>

      {/* Frame 05 to 06 Black Transition Layer */}
      <div 
        className="fixed inset-0 z-[62] bg-black pointer-events-none"
        style={{ 
          opacity: frame05to06Fade,
          transition: 'opacity 0.1s linear'
        }}
      />

      {/* Frame 06 Boxed Parallax Background */}
      <div 
        ref={frame06BgRef}
        className="fixed inset-0 z-[65] bg-black pointer-events-none flex items-center justify-center"
        style={{ opacity: frame06BgOpacity }}
      >
        <div 
          className="w-[55vw] h-[70vh] relative overflow-hidden rounded-sm"
          style={{
            transform: `scale(${Math.min(1, 0.6 + (Math.max(0, scrollProgress - 0.83) / 0.15) * 0.4)})`,
            transition: 'transform 0.1s linear'
          }}
        >
          <img 
            src="/frame_06_bg.jpg" 
            alt="Frame 06 Background" 
            className="w-full h-full object-cover origin-center"
          />
          {/* Subtle Inner Border */}
          <div className="absolute inset-0 border border-[#E1D4C0]/10 pointer-events-none" />
        </div>
      </div>

      {/* Frame 06 UI Layer */}
      <div 
        className="fixed inset-0 z-[70] pointer-events-none"
        style={{ 
          opacity: frame06Opacity,
          pointerEvents: frame06Opacity > 0.5 ? 'auto' : 'none',
          transition: 'opacity 0.4s ease-in-out'
        }}
      >
        {/* Technical Viewfinder Elements */}
        <div className="absolute top-[10vh] left-[5vw] w-12 h-12 border-t border-l border-[#E1D4C0]/20" />
        <div className="absolute bottom-[10vh] right-[5vw] w-12 h-12 border-b border-r border-[#E1D4C0]/20" />
        
        {/* Top Right: Technical Description */}
        <div className="absolute top-[15vh] right-[8vw] max-w-[320px] text-right flex flex-col items-end">
          <div className="flex items-center gap-4 mb-6 opacity-70">
            <span className="text-[10px] tracking-[0.2em] font-sans text-[#E1D4C0]/80">EV +2.4</span>
            <div className="h-[1px] w-12 bg-[#E1D4C0]/40"></div>
            <h2 className="text-[10px] tracking-[0.3em] font-medium text-[#E1D4C0] uppercase">
              THE LIGHT CHAMBER
            </h2>
          </div>
          <p className="text-[11px] font-sans leading-[2] opacity-80 text-[#E1D4C0]/70 uppercase tracking-widest text-justify text-last-right">
            Before colour, composition, or photography, light determines how every material will be understood. Everything else follows.
          </p>
        </div>

        {/* Bottom Left: Massive Motion-Revealed Title */}
        <div className="absolute bottom-[12vh] left-[5vw]">
          <h1 className="font-serif font-bold text-[90px] lg:text-[140px] leading-[0.85] tracking-tight">
            <span className="block overflow-hidden">
              <span className="block text-transparent bg-clip-text bg-gradient-to-r from-[#E1D4C0]/40 via-[#E1D4C0] to-[#E1D4C0]/40 bg-[length:200%_auto] animate-[pulse_4s_cubic-bezier(0.4,0,0.6,1)_infinite]">
                Light
              </span>
            </span>
            <span className="block overflow-hidden">
              <span className="block text-transparent bg-clip-text bg-gradient-to-r from-[#E1D4C0] via-[#E1D4C0]/40 to-[#E1D4C0] bg-[length:200%_auto] animate-[pulse_4s_cubic-bezier(0.4,0,0.6,1)_infinite_1s]">
                Designs
              </span>
            </span>
            <span className="block overflow-hidden mt-4">
              <span className="block italic font-medium text-[#E1D4C0] opacity-90">
                First.
              </span>
            </span>
          </h1>
        </div>
      </div>

      {/* Frame 07 UI Layer */}
      <div 
        className="fixed inset-0 z-[80] flex flex-col pointer-events-none t-stagger"
        style={{ 
          opacity: frame07Opacity,
          pointerEvents: frame07Opacity > 0.5 ? 'auto' : 'none',
          transition: 'opacity 0.1s linear'
        }}
      >
        <main className="absolute top-[18vh] left-[8vw] max-w-[680px]">
          <h2 className="text-[12px] tracking-[0.28em] font-medium opacity-70 mb-10 text-[#E1D4C0] uppercase">
            WORLD 01 · THE INSTITUTION
          </h2>
          
          <h1 className="font-serif font-bold text-[72px] lg:text-[88px] leading-[0.95] max-w-[620px] mb-12">
            Everything<br/><span className="italic">Connects.</span>
          </h1>
          
          <p className="text-[15px] leading-[1.8] opacity-90 max-w-[520px]">
            Observation, materials, research, light, and creation—each discipline strengthens the next. Together they form one cohesive creative intelligence system.
          </p>
        </main>
      </div>

      <style jsx>{`
        @keyframes scrollLine {
          0% { transform: translateY(-100%); }
          100% { transform: translateY(200%); }
        }
      `}</style>
    </div>

    {/* Buffer to hold Frame 08 on screen before pulling up the rest of the page */}
    <div className="w-full h-[150vh] bg-transparent pointer-events-none" />

    {/* Standard Scrolling Content */}
    <div className="relative w-full z-[200] bg-black">
      <PricingSection />
      <ContactSection />
      <Footer />
    </div>
    </>
  );
}
