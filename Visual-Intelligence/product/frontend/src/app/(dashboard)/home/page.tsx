"use client";

import React from "react";
import { motion } from "framer-motion";
import { MeadowBackground } from "@/components/dashboard/MeadowBackground";
import { MeadowPromptBox } from "@/components/dashboard/MeadowPromptBox";
import { HomeVerticalDock } from "@/components/dashboard/HomeVerticalDock";

export default function HomePage() {
  const [timeStr, setTimeStr] = React.useState<string>("");

  React.useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      const hours = String(now.getHours()).padStart(2, "0");
      const minutes = String(now.getMinutes()).padStart(2, "0");
      const seconds = String(now.getSeconds()).padStart(2, "0");
      const tzAbbr = new Date()
        .toLocaleDateString("en-US", { timeZoneName: "short" })
        .split(", ")[1] || "LIVE";
      setTimeStr(`${hours}:${minutes}:${seconds} ${tzAbbr}`);
    };

    updateTime();
    const interval = setInterval(updateTime, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="relative w-full h-full min-h-screen flex flex-col overflow-hidden select-none pt-20">
      
      {/* 1. Exact 1:1 3D WebGL Meadow Background (Sky dome, Clouds, Flowers, Butterflies, Grass) */}
      <MeadowBackground />

      {/* Vertical Apple-style Application Dock placed at extreme left center */}
      <HomeVerticalDock />

      {/* Readability scrim — subtle radial gradient to protect text against the moving 3D meadow */}
      <div
        className="fixed inset-0 z-[5] pointer-events-none"
        style={{
          background:
            "radial-gradient(ellipse 70% 55% at 50% 35%, rgba(255,255,255,0.35) 0%, rgba(255,255,255,0.12) 50%, transparent 100%)",
        }}
      />

      {/* 2. Hero Content Section */}
      <main className="relative z-10 flex-1 flex flex-col items-center justify-start pt-28 sm:pt-36 md:pt-40 px-6 max-w-5xl mx-auto w-full text-center">
        
        {/* Top Frosted Capsule Badge */}
        <motion.div
          initial={{ opacity: 0, y: -16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1], delay: 0.1 }}
          className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-white/40 backdrop-blur-md border border-white/60 shadow-sm text-[10px] font-mono tracking-widest uppercase font-bold text-[#0f1419] mb-6 select-none"
        >
          <div className="relative w-2 h-2">
            <div className="absolute inset-0 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.8)]" />
            <div className="absolute inset-[-3px] rounded-full ring-1 ring-emerald-500/30 animate-[breathe_3s_ease-in-out_infinite]" />
          </div>
          <span className="tabular-nums tracking-wider">
            {timeStr || "SYNCING TIME..."}
          </span>
        </motion.div>

        {/* Editorial Masthead — Two-register composition:
             Line 1: Nohemi ExtraBold (commanding declaration)
             Line 2: Cormorant Garamond italic (flowing editorial counter-line) */}
        <h1
          className="font-sans text-5xl sm:text-6xl md:text-7xl text-[#0f1419] mb-5 font-extrabold drop-shadow-[0_2px_20px_rgba(255,255,255,0.55)]"
          style={{
            letterSpacing: "-0.04em",
            lineHeight: 1.05,
          }}
        >
          {/* Line 1: Nohemi ExtraBold with Blur-to-Focus Glide */}
          <motion.span
            initial={{ opacity: 0, y: 32, filter: "blur(14px)" }}
            animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
            transition={{ duration: 0.95, ease: [0.16, 1, 0.3, 1], delay: 0.25 }}
            className="block"
          >
            Create, decide, design,
          </motion.span>

          {/* Line 2: Cormorant Garamond Italic with Staggered Blur-to-Focus Glide */}
          <motion.span
            initial={{ opacity: 0, y: 28, filter: "blur(12px)" }}
            animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
            transition={{ duration: 0.95, ease: [0.16, 1, 0.3, 1], delay: 0.45 }}
            className="block font-serif italic font-semibold"
            style={{ letterSpacing: "-0.01em" }}
          >
            &amp; evolve your brand distinction.
          </motion.span>
        </h1>

        {/* Editorial Subtitle */}
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1], delay: 0.65 }}
          className="text-base sm:text-lg text-[#0f1419]/75 max-w-3xl font-medium leading-[1.6] mb-10 tracking-[-0.01em]"
        >
          An intelligent creative organization that remembers decisions, understands market context, designs visual systems, and continuously matures brand distinction.
        </motion.p>

        {/* Central Glassmorphic AI Prompt Box */}
        <MeadowPromptBox />

      </main>

    </div>
  );
}

