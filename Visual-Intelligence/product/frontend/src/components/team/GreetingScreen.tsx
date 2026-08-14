"use client";

import React, { useEffect } from "react";
import { motion } from "framer-motion";

interface GreetingScreenProps {
  userName?: string;
  onComplete: () => void;
}

export const GreetingScreen: React.FC<GreetingScreenProps> = ({
  userName = "Creator",
  onComplete,
}) => {
  useEffect(() => {
    const timer = setTimeout(() => {
      onComplete();
    }, 2800);
    return () => clearTimeout(timer);
  }, [onComplete]);

  const greetingText = `WELCOME BACK, ${userName.toUpperCase()}`;
  const words = greetingText.split(" ");

  const container = {
    hidden: { opacity: 0 },
    visible: (i = 1) => ({
      opacity: 1,
      transition: { staggerChildren: 0.03, delayChildren: 0.2 * i },
    }),
    exit: {
      opacity: 0,
      scale: 0.96,
      transition: { duration: 0.5, ease: [0.22, 1, 0.36, 1] as const },
    },
  };

  const child = {
    visible: {
      opacity: 1,
      y: 0,
      filter: "blur(0px)",
      transition: {
        type: "spring" as const,
        damping: 12,
        stiffness: 100,
      },
    },
    hidden: {
      opacity: 0,
      y: 20,
      filter: "blur(10px)",
      transition: {
        type: "spring" as const,
        damping: 12,
        stiffness: 100,
      },
    },
  };

  return (
    <motion.div
      variants={container}
      initial="hidden"
      animate="visible"
      exit="exit"
      className="fixed inset-0 z-50 bg-[#050505] flex flex-col items-center justify-center p-6 select-none overflow-hidden"
    >
      {/* Soft Glow */}
      <div className="absolute w-[600px] h-[600px] bg-[#E1D4C0]/5 rounded-full blur-[160px] pointer-events-none" />

      {/* Guaranteed Single-Line Fluid Responsive Container */}
      <div className="flex items-center justify-center text-center z-10 w-full max-w-[95vw] overflow-hidden">
        <div className="flex items-center justify-center gap-[0.4em] whitespace-nowrap text-[clamp(1.1rem,3.8vw,3.2rem)] font-serif tracking-[0.14em]">
          {words.map((word, wordIdx) => (
            <span key={wordIdx} className="inline-flex whitespace-nowrap">
              {Array.from(word).map((letter, letterIdx) => (
                <motion.span
                  variants={child}
                  key={letterIdx}
                  className="text-[#E1D4C0] font-light"
                >
                  {letter}
                </motion.span>
              ))}
            </span>
          ))}
        </div>
      </div>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 0.4 }}
        transition={{ delay: 1.2, duration: 0.8 }}
        className="mt-6 font-mono text-[9px] uppercase tracking-[0.3em] text-white/50 z-10"
      >
        Initializing A2A Cooperative Environment...
      </motion.p>
    </motion.div>
  );
};
