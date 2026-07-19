'use client';

import { useRef, useState } from 'react';
import gsap from 'gsap';
import { useGSAP } from '@gsap/react';

export function CinematicEnding({ onComplete }: { onComplete?: () => void }) {
  const containerRef = useRef<HTMLDivElement>(null);
  const screen1Ref = useRef<HTMLDivElement>(null);
  const screen2Ref = useRef<HTMLDivElement>(null);
  const sentence1Ref = useRef<HTMLParagraphElement>(null);
  const sentence2Ref = useRef<HTMLParagraphElement>(null);
  const sentence3Ref = useRef<HTMLParagraphElement>(null);
  const promptRef = useRef<HTMLDivElement>(null);
  
  const [isDone, setIsDone] = useState(false);

  useGSAP(() => {
    // Initial states
    gsap.set([screen1Ref.current, screen2Ref.current, promptRef.current], { opacity: 0 });
    gsap.set([sentence1Ref.current, sentence2Ref.current, sentence3Ref.current], { opacity: 0, y: 10 });

    const tl = gsap.timeline({
      onComplete: () => {
        setIsDone(true);
        if (onComplete) onComplete();
      }
    });

    // Fade in skip prompt after a slight delay
    tl.to(promptRef.current, {
      opacity: 0.5,
      duration: 1,
      ease: 'power2.inOut',
    }, 0.5);

    // Blinking animation for prompt
    gsap.to(promptRef.current, {
      opacity: 0.2,
      duration: 1.5,
      yoyo: true,
      repeat: -1,
      ease: 'sine.inOut'
    });

    // Screen 1: THE THRESHOLD
    tl.to(screen1Ref.current, {
      opacity: 1,
      duration: 2,
      ease: 'power2.inOut'
    }, 1.0)
    .to(screen1Ref.current, {
      opacity: 0,
      duration: 1.5,
      ease: 'power2.inOut'
    }, '+=2.0') // Hold for 2 seconds

    // Screen 2: Philosophy sentences
    .to(screen2Ref.current, {
      opacity: 1,
      duration: 1,
    }, '+=0.5')
    .to(sentence1Ref.current, {
      opacity: 1,
      y: 0,
      duration: 1.5,
      ease: 'power3.out'
    }, '+=0.5')
    .to(sentence2Ref.current, {
      opacity: 1,
      y: 0,
      duration: 1.5,
      ease: 'power3.out'
    }, '+=1.0')
    .to(sentence3Ref.current, {
      opacity: 1,
      y: 0,
      duration: 1.5,
      ease: 'power3.out'
    }, '+=1.0')
    
    // Hold final screen for a bit, then fade out the prompt to leave just the text
    .to(promptRef.current, {
      opacity: 0,
      duration: 1
    }, '+=3.0')
    
    // Finally, dissolve the entire overlay to reveal Frame 08
    .to(containerRef.current, {
      opacity: 0,
      duration: 2.5,
      ease: 'power2.inOut'
    }, '+=2.0');

    // Handle skip functionality
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Enter' && !isDone) {
        // Fast forward the timeline to the very end to trigger the dissolve
        tl.progress(1);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);

  }, { scope: containerRef });

  return (
    <div 
      ref={containerRef} 
      className="fixed inset-0 z-[100] bg-black text-[#E1D4C0] flex items-center justify-center pointer-events-auto"
    >
      {/* Screen 1 */}
      <div ref={screen1Ref} className="absolute inset-0 flex items-center justify-center">
        <h1 className="font-serif text-[42px] tracking-[0.2em] font-light uppercase">
          The Threshold
        </h1>
      </div>

      {/* Screen 2 */}
      <div ref={screen2Ref} className="absolute inset-0 flex flex-col items-center justify-center px-8 text-center">
        <p ref={sentence1Ref} className="text-[18px] md:text-[22px] tracking-wide font-light mb-8 max-w-[800px]">
          You've walked through our philosophy.
        </p>
        <p ref={sentence2Ref} className="text-[18px] md:text-[22px] tracking-wide font-light mb-8 max-w-[800px]">
          You've witnessed how we observe, study and create.
        </p>
        <p ref={sentence3Ref} className="text-[18px] md:text-[22px] tracking-wide font-light max-w-[800px]">
          Now step inside and begin your own creative journey.
        </p>
      </div>

      {/* Skip Prompt */}
      {!isDone && (
        <div ref={promptRef} className="absolute bottom-12 left-1/2 -translate-x-1/2">
          <p className="text-[10px] tracking-[0.3em] uppercase opacity-50">
            Press [Enter] to skip
          </p>
        </div>
      )}
    </div>
  );
}
