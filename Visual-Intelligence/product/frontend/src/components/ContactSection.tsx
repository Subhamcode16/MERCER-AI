import Image from 'next/image';
import { useRef } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/dist/ScrollTrigger';
import { useGSAP } from '@gsap/react';

gsap.registerPlugin(ScrollTrigger);

export function ContactSection() {
  const sectionRef = useRef<HTMLElement>(null);
  const headlineRef = useRef<HTMLDivElement>(null);
  const galleryRef = useRef<HTMLDivElement>(null);
  const textRef = useRef<HTMLParagraphElement>(null);
  const formRef = useRef<HTMLFormElement>(null);

  useGSAP(() => {
    if (!sectionRef.current) return;

    // 1. Image Scale & Fade Parallax
    const images = gsap.utils.toArray('.gallery-item');
    gsap.set(images, { scale: 0.8, opacity: 0 });
    
    images.forEach((img, i) => {
      // Staggered reveal
      gsap.to(img as Element, {
        scale: 1,
        opacity: 1,
        duration: 1.2,
        delay: i * 0.1,
        ease: "power3.out",
        scrollTrigger: {
          trigger: galleryRef.current,
          start: "top 80%"
        }
      });

      // Y-axis Parallax scrub
      const speed = i === 2 ? 20 : (i === 0 || i === 4 ? 80 : 50); 
      gsap.to(img as Element, {
        y: speed,
        ease: "none",
        scrollTrigger: {
          trigger: galleryRef.current,
          start: "top bottom",
          end: "bottom top",
          scrub: true
        }
      });
    });

    // 2. Scrubbing Text Reveal
    const words = gsap.utils.toArray('.reveal-word');
    gsap.to(words, {
      opacity: 1,
      color: "#ffffff",
      stagger: 0.05,
      scrollTrigger: {
        trigger: textRef.current,
        start: "top 85%",
        end: "bottom 60%",
        scrub: true
      }
    });

    // 3. Form Stagger Reveal
    if (formRef.current) {
      gsap.fromTo(formRef.current.children, 
        { y: 40, opacity: 0 },
        {
          y: 0,
          opacity: 1,
          duration: 1,
          stagger: 0.15,
          ease: "power3.out",
          scrollTrigger: {
            trigger: formRef.current,
            start: "top 85%",
          }
        }
      );
    }

    // 4. Headline Reveal
    if (headlineRef.current) {
      gsap.fromTo(headlineRef.current.children, 
        { y: 40, opacity: 0 },
        {
          y: 0,
          opacity: 1,
          duration: 1.2,
          stagger: 0.15,
          ease: "power3.out",
          scrollTrigger: {
            trigger: headlineRef.current,
            start: "top 80%",
          }
        }
      );
    }
  }, { scope: sectionRef });

  const textContent = "We invite you to reach out for bespoke inquiries, collaborative projects, or general studio information. Our team reviews all correspondences with the utmost attention to detail.";
  const words = textContent.split(" ");

  return (
    <section ref={sectionRef} className="relative w-full min-h-screen bg-black flex flex-col items-center pt-32 pb-32 px-6 z-[200] overflow-hidden">
      
      {/* Headline */}
      <div ref={headlineRef} className="w-full max-w-7xl mx-auto flex flex-col items-center relative z-20 mb-20">
        <h2 className="text-[10px] tracking-[0.3em] font-medium text-[var(--color-warm-ivory)] uppercase text-center mb-6">
          Inquiries
        </h2>
        <h1 className="font-serif font-bold text-[40px] md:text-[64px] lg:text-[80px] leading-[1] text-center text-[var(--color-warm-ivory)]">
          CONNECT WITH<br/>OUR <span className="italic">STUDIO</span>
        </h1>
      </div>

      {/* Gallery & Background Text */}
      <div className="relative w-full max-w-[1400px] mx-auto flex items-center justify-center mb-32 h-[300px] sm:h-[400px] md:h-[600px]">
        {/* Background Text */}
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none z-0">
          <span className="font-serif font-bold text-[18vw] leading-none text-white opacity-5 whitespace-nowrap select-none">
            THE STUDIO
          </span>
        </div>

        {/* 5-Image Gallery */}
        <div ref={galleryRef} className="relative z-10 flex items-center justify-center gap-2 sm:gap-4 md:gap-8 w-full h-full px-2 sm:px-4">
          {[
            { src: '/moodboard/audience.png', height: 'h-[40%]', align: 'justify-end pb-8', num: '01' },
            { src: '/moodboard/editorial-refs.png', height: 'h-[60%]', align: 'justify-start pt-16', num: '02' },
            { src: '/assets/fashion_hero_1_1783581266482.png', height: 'h-[80%]', align: 'justify-center', num: '03' },
            { src: '/assets/fashion_hero_2_1783581276651.png', height: 'h-[60%]', align: 'justify-start pt-16', num: '04' },
            { src: '/assets/fashion_hero_3_1783581286733.png', height: 'h-[40%]', align: 'justify-end pb-8', num: '05' },
          ].map((img, i) => (
            <div key={i} className={`gallery-item relative flex flex-col items-center w-1/5 h-full ${img.align}`}>
              <span className="text-[10px] font-medium tracking-widest text-white/50 mb-4">
                {img.num}
              </span>
              <div className={`relative w-full ${img.height} transition-transform duration-700 hover:scale-105`}>
                <Image 
                  src={img.src}
                  alt={`Observation ${img.num}`}
                  fill
                  className="object-cover rounded-sm opacity-80 hover:opacity-100 transition-opacity duration-500"
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Contact Form Area - 2 Columns */}
      <div className="w-full max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-16 md:gap-24 relative z-20">
        
        {/* Left: Editorial Paragraph */}
        <div className="flex flex-col justify-start pt-4">
          <h3 className="font-serif text-[24px] text-[var(--color-warm-ivory)] mb-6">Studio Relations</h3>
          <p ref={textRef} className="text-[14px] leading-[1.8] font-light max-w-sm flex flex-wrap gap-x-[4px]">
            {words.map((word, idx) => (
              <span key={idx} className="reveal-word text-white/20">{word}</span>
            ))}
          </p>
          <div className="mt-12 text-[11px] text-white/40 tracking-[0.2em] uppercase flex flex-col gap-3">
            <span>New York — 09:00 EST</span>
            <span>Paris — 15:00 CET</span>
            <span>Tokyo — 23:00 JST</span>
          </div>
        </div>

        {/* Right: Apple Liquid Glass Form */}
        <form ref={formRef} className="flex flex-col gap-6" onSubmit={(e) => e.preventDefault()}>
          <div className="flex flex-col gap-2">
            <label htmlFor="name" className="text-[10px] tracking-[0.2em] text-[var(--color-warm-ivory)] uppercase ml-1 opacity-70">Name</label>
            <input 
              type="text" 
              id="name"
              required
              className="w-full bg-white/5 border border-white/10 rounded-xl px-5 py-4 text-[15px] text-white focus:outline-none focus:border-[var(--color-warm-ivory)] focus:bg-white/10 transition-all backdrop-blur-md"
            />
          </div>

          <div className="flex flex-col gap-2">
            <label htmlFor="email" className="text-[10px] tracking-[0.2em] text-[var(--color-warm-ivory)] uppercase ml-1 opacity-70">Email</label>
            <input 
              type="email" 
              id="email"
              required
              className="w-full bg-white/5 border border-white/10 rounded-xl px-5 py-4 text-[15px] text-white focus:outline-none focus:border-[var(--color-warm-ivory)] focus:bg-white/10 transition-all backdrop-blur-md"
            />
          </div>

          <div className="flex flex-col gap-2">
            <label htmlFor="message" className="text-[10px] tracking-[0.2em] text-[var(--color-warm-ivory)] uppercase ml-1 opacity-70">Inquiry</label>
            <textarea 
              id="message"
              required
              rows={4}
              className="w-full bg-white/5 border border-white/10 rounded-xl px-5 py-4 text-[15px] text-white focus:outline-none focus:border-[var(--color-warm-ivory)] focus:bg-white/10 transition-all backdrop-blur-md resize-none"
            />
          </div>

          {/* Submit Button */}
          <div className="mt-4">
            <button 
              type="submit"
              className="relative overflow-hidden group w-full sm:w-auto rounded-xl border border-[var(--color-warm-ivory)]/30 bg-[var(--color-warm-ivory)]/5 px-12 py-4 hover:bg-[var(--color-warm-ivory)]/10 hover:border-[var(--color-warm-ivory)]/50 transition-all backdrop-blur-md flex items-center justify-center"
            >
              <div className="absolute top-0 bottom-0 left-0 w-24 bg-gradient-to-r from-transparent via-[var(--color-warm-ivory)]/20 to-transparent skew-x-[-20deg] pointer-events-none -translate-x-[150%] group-hover:translate-x-[300%] transition-transform duration-700 ease-in-out" />
              <span className="relative z-10 text-[11px] tracking-[0.2em] uppercase font-medium text-[var(--color-warm-ivory)] group-hover:text-white transition-colors">
                Submit Inquiry
              </span>
            </button>
          </div>
        </form>

      </div>
    </section>
  );
}
