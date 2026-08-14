"use client";

import React from "react";
import { motion } from "framer-motion";
import { Sparkles } from "lucide-react";

interface ApprovalGateProps {
  onApprove: () => void;
  onCancel?: () => void;
}

export const ApprovalGate: React.FC<ApprovalGateProps> = ({ onApprove, onCancel }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 15, scale: 0.98 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: 15, scale: 0.98 }}
      transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
      className="border border-[#E1D4C0]/40 bg-[#0C0C0D]/95 rounded-2xl p-5 shadow-[0_0_50px_rgba(225,212,192,0.15)] flex justify-between items-center text-left backdrop-blur-xl"
    >
      <div className="flex flex-col gap-0.5">
        <span className="text-[11px] font-serif tracking-[0.15em] uppercase text-[#E1D4C0] font-medium flex items-center gap-2">
          <Sparkles size={12} className="text-[#E1D4C0]" />
          Awaiting Pipeline Approval
        </span>
        <span className="text-[9px] font-sans text-white/50 tracking-wide font-light">
          Art Director parameters resolved. Tap below to synthesize high-fidelity visual assets.
        </span>
      </div>
      <div className="flex items-center gap-3 shrink-0">
        {onCancel && (
          <motion.button
            onClick={onCancel}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="py-3 px-6 text-[10px] font-bold tracking-[0.2em] uppercase text-white/60 hover:text-white transition-colors cursor-pointer"
          >
            Cancel
          </motion.button>
        )}
        <motion.button
          onClick={onApprove}
          whileHover={{ scale: 1.03, backgroundColor: "#D8C5A7" }}
          whileTap={{ scale: 0.97 }}
          transition={{ type: "spring", stiffness: 400, damping: 15 }}
          className="py-3 px-6 text-[10px] font-bold tracking-[0.2em] uppercase bg-[#E1D4C0] text-black rounded-xl shadow-md cursor-pointer"
        >
          Approve & Render
        </motion.button>
      </div>
    </motion.div>
  );
};
