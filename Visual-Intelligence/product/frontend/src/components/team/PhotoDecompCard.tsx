"use client";

import React from "react";
import { motion } from "framer-motion";
import { Image as ImageIcon } from "lucide-react";

interface PhotoDecompCardProps {
  title: string;
  description: string;
  images: { label: string; url: string }[];
}

export const PhotoDecompCard: React.FC<PhotoDecompCardProps> = ({
  title,
  description,
  images,
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
      className="border border-[#E1D4C0]/20 bg-[#0C0C0D]/95 rounded-2xl p-5 relative overflow-hidden flex flex-col gap-4 max-w-lg mt-1 shadow-2xl backdrop-blur-xl cursor-pointer"
    >
      <div className="absolute top-0 left-0 right-0 h-[1px] bg-gradient-to-r from-transparent via-[#E1D4C0]/30 to-transparent" />
      <div>
        <span className="text-[9px] font-mono tracking-widest text-[#E1D4C0]/80 uppercase mb-1 block font-semibold">
          {title}
        </span>
        <p className="text-[11px] text-white/50 font-light mb-3">{description}</p>

        <div className="flex flex-col gap-2.5">
          {images.map((item, idx) => (
            <div
              key={idx}
              className="flex items-center gap-3 bg-black/50 hover:bg-black/70 border border-white/5 hover:border-white/10 p-2.5 rounded-xl transition-colors duration-200"
            >
              <div className="w-8 h-8 rounded-lg bg-white/5 flex items-center justify-center text-[#E1D4C0]/70 shrink-0 border border-white/10">
                <ImageIcon size={14} />
              </div>
              <div className="flex flex-col text-left">
                <span className="text-[8px] font-mono uppercase tracking-wider text-white/30">
                  {item.label}
                </span>
                <span className="text-[10px] text-[#E1D4C0]/90 font-light">
                  {item.url}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </motion.div>
  );
};
