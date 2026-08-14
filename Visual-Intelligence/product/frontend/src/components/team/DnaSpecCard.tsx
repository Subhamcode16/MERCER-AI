"use client";

import React from "react";
import { motion } from "framer-motion";

interface DnaSpecCardProps {
  title: string;
  details: Record<string, string>;
  bullet?: string;
}

export const DnaSpecCard: React.FC<DnaSpecCardProps> = ({
  title,
  details,
  bullet,
}) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 15, filter: "blur(3px)" }}
      animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
      whileHover={{ 
        y: -3, 
        borderColor: "rgba(225, 212, 192, 0.35)", 
        boxShadow: "0 12px 40px rgba(225, 212, 192, 0.08)" 
      }}
      whileTap={{ scale: 0.995 }}
      transition={{ 
        type: "spring", 
        stiffness: 400, 
        damping: 30,
        layout: { duration: 0.2 }
      }}
      className="border border-[#E1D4C0]/20 bg-[#0C0C0D]/95 rounded-2xl p-5 relative overflow-hidden flex flex-col gap-3.5 max-w-lg mt-1 shadow-2xl backdrop-blur-xl cursor-pointer"
    >
      <div className="absolute top-0 left-0 right-0 h-[1px] bg-gradient-to-r from-transparent via-[#E1D4C0]/30 to-transparent" />
      <div>
        <span className="text-[9px] font-mono tracking-widest text-[#E1D4C0]/80 uppercase mb-2 block font-semibold">
          {title}
        </span>
        <div className="grid grid-cols-2 gap-x-6 gap-y-2 border-b border-white/5 pb-3">
          {Object.entries(details).map(([key, val]) => (
            <div key={key} className="flex justify-between items-baseline py-1">
              <span className="text-[8.5px] font-mono uppercase tracking-wider text-white/40">
                {key}
              </span>
              <span className="text-[10px] text-[#E1D4C0] font-light">{val}</span>
            </div>
          ))}
        </div>
        {bullet && (
          <p className="text-[10px] text-white/50 font-sans leading-relaxed mt-2.5 italic">
            * {bullet}
          </p>
        )}
      </div>
    </motion.div>
  );
};
