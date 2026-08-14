"use client";

import React from "react";
import { motion } from "framer-motion";
import { CheckCheck } from "lucide-react";

interface UserMessageProps {
  time: string;
  text: string;
}

export const UserMessage: React.FC<UserMessageProps> = ({ time, text }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 12, filter: "blur(4px)" }}
      animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
      transition={{ duration: 0.45, ease: [0.215, 0.61, 0.355, 1] }}
      className="flex flex-col items-end w-full"
    >
      <div className="flex flex-col items-end max-w-lg">
        <div className="bg-[#0D0D0E]/90 border border-[#E1D4C0]/25 rounded-2xl px-5 py-3.5 text-left shadow-[0_4px_24px_rgba(0,0,0,0.4)] backdrop-blur-md">
          <p className="text-[12px] font-sans text-white/90 leading-relaxed font-light whitespace-pre-wrap">
            {text}
          </p>
        </div>
        <div className="flex items-center gap-1.5 mt-1 px-1">
          <span className="text-[8.5px] font-mono text-[#E1D4C0]/40">{time}</span>
          <motion.span
            initial={{ scale: 0, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ type: "spring", stiffness: 500, damping: 15, delay: 0.25 }}
            className="flex items-center"
          >
            <CheckCheck size={11} className="text-[#E1D4C0]/70" />
          </motion.span>
        </div>
      </div>
    </motion.div>
  );
};
