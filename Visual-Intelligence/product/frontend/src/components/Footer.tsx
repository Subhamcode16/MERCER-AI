import { useRef } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/dist/ScrollTrigger';
import { useGSAP } from '@gsap/react';

gsap.registerPlugin(ScrollTrigger);

export function Footer() {
  const footerRef = useRef<HTMLElement>(null);
  const titleRef = useRef<HTMLHeadingElement>(null);

  useGSAP(() => {
    if (!footerRef.current || !titleRef.current) return;

    gsap.fromTo(titleRef.current, 
      { scale: 0.9, letterSpacing: "-0.05em" },
      { 
        scale: 1.0, 
        letterSpacing: "-0.02em",
        ease: "none",
        scrollTrigger: {
          trigger: footerRef.current,
          start: "top bottom",
          end: "bottom bottom",
          scrub: true
        }
      }
    );
  }, { scope: footerRef });

  return (
    <footer ref={footerRef} className="relative w-full bg-black text-white pt-24 pb-8 px-6 md:px-12 z-[200]">
      <div className="w-full max-w-[1600px] mx-auto flex flex-col">
        
        {/* Top Row: Newsletter (Left) & Links (Right) */}
        <div className="flex flex-col lg:flex-row justify-between items-start gap-16 mb-24 w-full">
          
          {/* Newsletter */}
          <div className="flex flex-col w-full max-w-md">
            <h4 className="text-[11px] tracking-[0.2em] uppercase text-white/60 mb-6 font-medium">Join Our Newsletter</h4>
            <div className="relative group">
              <input 
                type="email" 
                placeholder="Email Address"
                className="w-full bg-white/5 border border-white/10 rounded-xl pl-5 pr-32 py-4 text-[15px] text-white placeholder-white/30 focus:outline-none focus:border-white/30 focus:bg-white/10 transition-all backdrop-blur-md"
              />
              <button className="absolute right-2 top-1/2 -translate-y-1/2 px-4 py-2 text-[10px] tracking-[0.2em] uppercase text-[var(--color-warm-ivory)] hover:text-white transition-colors font-medium">
                Subscribe
              </button>
            </div>
            <p className="text-[10px] text-white/30 mt-4 tracking-wide">
              By subscribing, you agree to our Privacy Policy and consent to receive updates from our studio.
            </p>
          </div>

          {/* Links 3 Columns */}
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-12 sm:gap-24 w-full lg:w-auto">
            <div className="flex flex-col gap-4">
              <h4 className="text-[10px] tracking-[0.2em] uppercase text-white/40 mb-2 font-medium">Explore</h4>
              <a href="#" className="text-[13px] text-white/50 hover:text-[var(--color-warm-ivory)] transition-colors">Intelligence</a>
              <a href="#" className="text-[13px] text-white/50 hover:text-[var(--color-warm-ivory)] transition-colors">Architecture</a>
              <a href="#" className="text-[13px] text-white/50 hover:text-[var(--color-warm-ivory)] transition-colors">Pricing</a>
            </div>
            <div className="flex flex-col gap-4">
              <h4 className="text-[10px] tracking-[0.2em] uppercase text-white/40 mb-2 font-medium">Company</h4>
              <a href="#" className="text-[13px] text-white/50 hover:text-[var(--color-warm-ivory)] transition-colors">About Us</a>
              <a href="#" className="text-[13px] text-white/50 hover:text-[var(--color-warm-ivory)] transition-colors">Careers</a>
              <a href="#" className="text-[13px] text-white/50 hover:text-[var(--color-warm-ivory)] transition-colors">Contact</a>
            </div>
            <div className="flex flex-col gap-4">
              <h4 className="text-[10px] tracking-[0.2em] uppercase text-white/40 mb-2 font-medium">Legal</h4>
              <a href="#" className="text-[13px] text-white/50 hover:text-[var(--color-warm-ivory)] transition-colors">Terms</a>
              <a href="#" className="text-[13px] text-white/50 hover:text-[var(--color-warm-ivory)] transition-colors">Privacy</a>
              <a href="#" className="text-[13px] text-white/50 hover:text-[var(--color-warm-ivory)] transition-colors">Cookies</a>
            </div>
          </div>
        </div>

        {/* Bottom Row: Monumental Text & Logo */}
        <div className="w-full flex flex-col sm:flex-row items-end justify-between border-t border-white/10 pt-12 overflow-hidden">
          {/* Monumental Typography */}
          <h2 ref={titleRef} className="font-serif text-[18vw] sm:text-[140px] md:text-[180px] lg:text-[220px] leading-[0.8] tracking-[-0.02em] text-white opacity-90 select-none origin-left">
            ATELIER
          </h2>
          
          {/* Right side Logomark & Copyright */}
          <div className="flex flex-col items-end gap-6 mb-2 sm:mb-8 mt-8 sm:mt-0 shrink-0">
            {/* Square Logomark */}
            <div className="w-8 h-8 border border-white/20 flex items-center justify-center">
              <div className="w-2.5 h-2.5 bg-[var(--color-warm-ivory)]/80" />
            </div>
            <p className="text-[10px] tracking-[0.1em] uppercase text-white/30 text-right">
              © {new Date().getFullYear()} Atelier OS.<br/>All rights reserved.
            </p>
          </div>
        </div>

      </div>
    </footer>
  );
}
