"use client";

import { useState, useEffect } from "react";
import { Heart, Eye, CheckCircle2, ChevronLeft, ChevronRight } from "lucide-react";

const IMAGES = [
  {
    src: "/campaigns/editorial_03.png",
    title: "Architectural Volume — Heritage Spin",
    category: "Couture Physics",
    stats: { loves: "4,890", views: "34,200", usage: "Enterprise Tier" }
  },
  {
    src: "/campaigns/editorial_04.png",
    title: "Haute Couture Drape — Royal Crimson",
    category: "Generative Volume",
    stats: { loves: "5,210", views: "41,800", usage: "Studio Tier" }
  },
  {
    src: "/campaigns/editorial_06.png",
    title: "Sculptural Silhouette — Kinetic Motion",
    category: "Atmospheric Motion",
    stats: { loves: "3,980", views: "28,600", usage: "Pro Tier" }
  },
  {
    src: "/campaigns/editorial_01.jpg",
    title: "Heritage Korvai — Atelier Weave",
    category: "Textile Intelligence",
    stats: { loves: "4,150", views: "31,900", usage: "Enterprise Tier" }
  },
  {
    src: "/campaigns/editorial_05.jpg",
    title: "Editorial Silhouette — Golden Ray",
    category: "Lighting Geometry",
    stats: { loves: "6,040", views: "52,100", usage: "Studio Tier" }
  },
  {
    src: "/campaigns/editorial_07.jpg",
    title: "Embroidered Drape — Velvet Texture",
    category: "Material Physics",
    stats: { loves: "4,720", views: "39,400", usage: "Enterprise Tier" }
  }
];

export function AuthSlider() {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isHovered, setIsHovered] = useState(false);

  useEffect(() => {
    if (isHovered) return;
    const timer = setInterval(() => {
      setCurrentIndex((prev) => (prev + 1) % IMAGES.length);
    }, 5000);
    return () => clearInterval(timer);
  }, [isHovered]);

  const handleNext = () => {
    setCurrentIndex((prev) => (prev + 1) % IMAGES.length);
  };

  const handlePrev = () => {
    setCurrentIndex((prev) => (prev - 1 + IMAGES.length) % IMAGES.length);
  };

  return (
    <div 
      className="hidden lg:block w-1/2 relative bg-zinc-900 overflow-hidden group rounded-l-[28px]"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {IMAGES.map((img, idx) => (
        <div
          key={idx}
          className="absolute inset-0 transition-opacity duration-1000 ease-in-out"
          style={{ opacity: currentIndex === idx ? 1 : 0 }}
        >
          <img 
            src={img.src} 
            alt={img.title}
            className="absolute inset-0 w-full h-full object-cover scale-105 group-hover:scale-100 transition-transform duration-1000"
          />
          {/* Subtle luxury vignette gradient */}
          <div className="absolute inset-0 bg-gradient-to-t from-black/85 via-black/25 to-black/10" />
          
          {/* Top Brand Pill */}
          <div className="absolute top-8 left-8">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/20 backdrop-blur-xl border border-white/30 text-white shadow-sm">
              <div className="w-1.5 h-1.5 rounded-full bg-emerald-400 shadow-[0_0_8px_rgba(52,211,153,0.9)]" />
              <span className="text-[10px] font-sans font-bold tracking-[0.2em] uppercase">
                {img.category}
              </span>
            </div>
          </div>

          {/* Bottom Editorial Caption */}
          <div className="absolute bottom-8 left-8 right-8 flex flex-col gap-3">
            <div>
              <h3 className="text-white font-serif text-2xl sm:text-3xl font-bold tracking-tight mb-1 drop-shadow-md">
                {img.title}
              </h3>
              <p className="text-white/70 text-xs font-sans tracking-wide">
                Live generative artifact synthesized in VYREN Creative Studio
              </p>
            </div>

            {/* Frosted Glass Metadata Chips */}
            <div className="flex items-center gap-2 pt-1">
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/15 backdrop-blur-md border border-white/20 text-white text-xs font-medium shadow-sm">
                <Heart className="w-3 h-3 text-rose-300" />
                {img.stats.loves}
              </span>
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/15 backdrop-blur-md border border-white/20 text-white text-xs font-medium shadow-sm">
                <Eye className="w-3 h-3 text-emerald-300" />
                {img.stats.views}
              </span>
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/25 backdrop-blur-md border border-white/35 text-white text-xs font-semibold shadow-sm ml-auto">
                <CheckCircle2 className="w-3 h-3 text-amber-300" />
                {img.stats.usage}
              </span>
            </div>
          </div>
        </div>
      ))}

      {/* Navigation Arrows with Frosted Glass styling */}
      <button 
        onClick={handlePrev}
        aria-label="Previous image"
        className="absolute left-6 top-1/2 -translate-y-1/2 w-10 h-10 rounded-full bg-black/40 backdrop-blur-md border border-white/20 flex items-center justify-center text-white opacity-0 group-hover:opacity-100 transition-all hover:bg-black/60 hover:scale-105 z-10"
      >
        <ChevronLeft className="w-5 h-5" />
      </button>
      <button 
        onClick={handleNext}
        aria-label="Next image"
        className="absolute right-6 top-1/2 -translate-y-1/2 w-10 h-10 rounded-full bg-black/40 backdrop-blur-md border border-white/20 flex items-center justify-center text-white opacity-0 group-hover:opacity-100 transition-all hover:bg-black/60 hover:scale-105 z-10"
      >
        <ChevronRight className="w-5 h-5" />
      </button>
    </div>
  );
}
