"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Upload, Sparkles, ArrowRight, Check } from "lucide-react";
import { BrandDnaData } from "./types";

interface BrandDnaModalProps {
  userId?: string;
  onComplete: (data: BrandDnaData | null) => void;
}

export const BrandDnaModal: React.FC<BrandDnaModalProps> = ({
  userId = "default_user",
  onComplete,
}) => {
  const [activeTab, setActiveTab] = useState<"menu" | "upload" | "wizard">(
    "menu"
  );

  // Wizard state
  const [wizardStep, setWizardStep] = useState(1);
  const [formArchetype, setFormArchetype] = useState("Luxury / Minimalist");
  const [formVoice, setFormVoice] = useState("Calm, Architectural");
  const [formPalette, setFormPalette] = useState([
    "#E1D4C0",
    "#0D0D0E",
    "#1F1F21",
  ]);

  // Upload state
  const [uploadText, setUploadText] = useState("");

  const saveAndExit = (data: BrandDnaData | null) => {
    if (data) {
      localStorage.setItem(`vyren_brand_dna_${userId}`, JSON.stringify(data));
    }
    onComplete(data);
  };

  const handleFinishWizard = () => {
    const data: BrandDnaData = {
      account: "VYREN Atelier",
      archetype: formArchetype,
      voice: formVoice,
      palette: formPalette,
    };
    saveAndExit(data);
  };

  const handleFinishUpload = () => {
    const data: BrandDnaData = {
      account: "Custom Brand Profile",
      archetype: "Custom Uploaded",
      voice: "User Defined",
      palette: ["#E1D4C0", "#000000"],
      customRules: uploadText,
    };
    saveAndExit(data);
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-50 bg-black/80 backdrop-blur-xl flex items-center justify-center p-6"
    >
      <motion.div
        initial={{ opacity: 0, scale: 0.95, y: 20 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        exit={{ opacity: 0, scale: 0.95, y: 20 }}
        transition={{ duration: 0.3, ease: [0.22, 1, 0.36, 1] }}
        className="w-full max-w-2xl bg-[#0C0C0E]/95 border border-[#E1D4C0]/25 rounded-3xl p-8 shadow-2xl relative overflow-hidden flex flex-col gap-6 text-left"
      >
        <div className="absolute top-0 left-0 right-0 h-[1px] bg-gradient-to-r from-transparent via-[#E1D4C0]/40 to-transparent" />

        {/* Modal Header */}
        <div className="flex flex-col gap-1">
          <span className="text-[9px] font-mono tracking-[0.3em] uppercase text-white/30">
            Account Setup
          </span>
          <h2 className="text-xl font-serif tracking-wide text-[#E1D4C0] font-light">
            Establish Your Brand DNA
          </h2>
          <p className="text-[11px] font-sans text-white/50 font-light leading-relaxed">
            Specialist agents align their visual outputs against your brand identity constraints.
          </p>
        </div>

        <AnimatePresence mode="wait">
          {/* MENU VIEW */}
          {activeTab === "menu" && (
            <motion.div
              key="menu"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="flex flex-col gap-4"
            >
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Option 1: Upload */}
                <button
                  onClick={() => setActiveTab("upload")}
                  className="group border border-white/10 hover:border-[#E1D4C0]/40 bg-white/[0.01] hover:bg-white/[0.03] p-6 rounded-2xl flex flex-col gap-3 text-left transition-all cursor-pointer"
                >
                  <div className="w-10 h-10 rounded-xl bg-white/5 border border-white/10 flex items-center justify-center text-[#E1D4C0] group-hover:scale-105 transition-transform">
                    <Upload size={18} />
                  </div>
                  <div>
                    <h3 className="font-serif text-[13px] text-white group-hover:text-[#E1D4C0] transition-colors">
                      Upload Brand DNA File
                    </h3>
                    <p className="text-[10px] font-sans text-white/40 leading-normal mt-1">
                      Paste guidelines or attach your brand configuration document.
                    </p>
                  </div>
                </button>

                {/* Option 2: Develop Wizard */}
                <button
                  onClick={() => setActiveTab("wizard")}
                  className="group border border-[#E1D4C0]/30 hover:border-[#E1D4C0] bg-[#E1D4C0]/[0.02] hover:bg-[#E1D4C0]/[0.05] p-6 rounded-2xl flex flex-col gap-3 text-left transition-all cursor-pointer relative overflow-hidden shadow-lg"
                >
                  <div className="w-10 h-10 rounded-xl bg-[#E1D4C0]/10 border border-[#E1D4C0]/30 flex items-center justify-center text-[#E1D4C0] group-hover:scale-105 transition-transform">
                    <Sparkles size={18} />
                  </div>
                  <div>
                    <h3 className="font-serif text-[13px] text-[#E1D4C0] transition-colors">
                      Develop Brand DNA With Us
                    </h3>
                    <p className="text-[10px] font-sans text-white/50 leading-normal mt-1">
                      Interactive 3-step builder to define archetype, tone, and palette tokens.
                    </p>
                  </div>
                </button>
              </div>

              {/* Option 3: Skip */}
              <div className="flex justify-center pt-2">
                <button
                  onClick={() => saveAndExit(null)}
                  className="text-[10px] font-mono tracking-widest uppercase text-white/30 hover:text-white/70 transition-colors cursor-pointer"
                >
                  Skip for Now
                </button>
              </div>
            </motion.div>
          )}

          {/* UPLOAD VIEW */}
          {activeTab === "upload" && (
            <motion.div
              key="upload"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="flex flex-col gap-4"
            >
              <textarea
                value={uploadText}
                onChange={(e) => setUploadText(e.target.value)}
                placeholder="Paste your brand guidelines, prompt rules, or raw DNA specs..."
                className="w-full h-40 bg-black/50 border border-white/10 rounded-xl p-4 text-[11px] font-mono text-white/90 focus:outline-none focus:border-[#E1D4C0]/50 resize-none"
              />

              <div className="flex justify-between items-center">
                <button
                  onClick={() => setActiveTab("menu")}
                  className="text-[10px] font-mono text-white/40 hover:text-white transition-colors"
                >
                  ← Back to Options
                </button>
                <button
                  onClick={handleFinishUpload}
                  disabled={!uploadText.trim()}
                  className="px-6 py-2.5 bg-[#E1D4C0] hover:bg-[#C9B99A] text-black font-bold text-[10px] tracking-widest uppercase rounded-xl transition-all disabled:opacity-20 cursor-pointer"
                >
                  Save & Continue
                </button>
              </div>
            </motion.div>
          )}

          {/* WIZARD VIEW */}
          {activeTab === "wizard" && (
            <motion.div
              key="wizard"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="flex flex-col gap-5"
            >
              <div>
                <div className="flex justify-between items-baseline mb-1">
                  <span className="text-[11px] font-serif text-[#E1D4C0]">
                    Step {wizardStep} of 3
                  </span>
                  <span className="text-[8.5px] font-mono text-white/30">
                    Interactive Builder
                  </span>
                </div>
                <div className="w-full bg-white/5 h-[1px] rounded-full overflow-hidden">
                  <div
                    className="bg-[#E1D4C0] h-full transition-all duration-300"
                    style={{ width: `${(wizardStep / 3) * 100}%` }}
                  />
                </div>
              </div>

              {wizardStep === 1 && (
                <div className="flex flex-col gap-3">
                  <span className="text-[9.5px] uppercase tracking-wider text-white/40 font-mono">
                    Select Brand Archetype
                  </span>
                  <div className="grid grid-cols-2 gap-3">
                    {[
                      "Luxury / Minimalist",
                      "Avant-Garde / Brutalist",
                      "Heritage / Editorial",
                      "Kinetic / Streetwear",
                    ].map((arch) => (
                      <button
                        key={arch}
                        onClick={() => setFormArchetype(arch)}
                        className={`p-3.5 text-[10px] text-left border rounded-xl font-mono uppercase tracking-wider transition-all cursor-pointer ${
                          formArchetype === arch
                            ? "bg-[#E1D4C0] text-black border-[#E1D4C0] font-bold"
                            : "bg-white/5 border-white/10 hover:border-white/30 text-white/60 hover:text-white"
                        }`}
                      >
                        {arch}
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {wizardStep === 2 && (
                <div className="flex flex-col gap-3">
                  <span className="text-[9.5px] uppercase tracking-wider text-white/40 font-mono">
                    Select Voice & Tone
                  </span>
                  <div className="grid grid-cols-2 gap-3">
                    {[
                      "Calm, Architectural",
                      "Bold, Assertive",
                      "Mysterious, Noir",
                      "Warm, Editorial",
                    ].map((voice) => (
                      <button
                        key={voice}
                        onClick={() => setFormVoice(voice)}
                        className={`p-3.5 text-[10px] text-left border rounded-xl font-mono uppercase tracking-wider transition-all cursor-pointer ${
                          formVoice === voice
                            ? "bg-[#E1D4C0] text-black border-[#E1D4C0] font-bold"
                            : "bg-white/5 border-white/10 hover:border-white/30 text-white/60 hover:text-white"
                        }`}
                      >
                        {voice}
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {wizardStep === 3 && (
                <div className="flex flex-col gap-3">
                  <span className="text-[9.5px] uppercase tracking-wider text-white/40 font-mono">
                    Color Palette Configuration
                  </span>
                  <div className="grid grid-cols-3 gap-3">
                    {[
                      {
                        label: "Warm Ivory Suite",
                        colors: ["#E1D4C0", "#0D0D0E", "#1F1F21"],
                      },
                      {
                        label: "Monochrome Obsidian",
                        colors: ["#000000", "#111111", "#FFFFFF"],
                      },
                      {
                        label: "Heritage Brocade",
                        colors: ["#C5A880", "#2D261E", "#0B0A08"],
                      },
                    ].map((pal) => (
                      <button
                        key={pal.label}
                        onClick={() => setFormPalette(pal.colors)}
                        className={`p-3 flex flex-col gap-2 border rounded-xl transition-all cursor-pointer ${
                          formPalette[0] === pal.colors[0]
                            ? "border-[#E1D4C0] bg-white/[0.02]"
                            : "bg-white/5 border-white/10 hover:border-white/20"
                        }`}
                      >
                        <span className="text-[8px] uppercase tracking-wider font-mono text-white/60">
                          {pal.label}
                        </span>
                        <div className="flex gap-1">
                          {pal.colors.map((c, i) => (
                            <div
                              key={i}
                              className="w-3.5 h-3.5 rounded-full border border-white/10"
                              style={{ backgroundColor: c }}
                            />
                          ))}
                        </div>
                      </button>
                    ))}
                  </div>
                </div>
              )}

              <div className="flex justify-between items-center pt-3 border-t border-white/5">
                <button
                  onClick={() => {
                    if (wizardStep === 1) setActiveTab("menu");
                    else setWizardStep((prev) => prev - 1);
                  }}
                  className="text-[10px] font-mono text-white/40 hover:text-white transition-colors"
                >
                  ← Back
                </button>
                {wizardStep < 3 ? (
                  <button
                    onClick={() => setWizardStep((prev) => prev + 1)}
                    className="px-5 py-2 bg-[#E1D4C0] hover:bg-[#C9B99A] text-black font-bold text-[10px] tracking-widest uppercase rounded-xl transition-all flex items-center gap-1.5 cursor-pointer"
                  >
                    Next <ArrowRight size={12} />
                  </button>
                ) : (
                  <button
                    onClick={handleFinishWizard}
                    className="px-5 py-2 bg-[#E1D4C0] hover:bg-[#C9B99A] text-black font-bold text-[10px] tracking-widest uppercase rounded-xl transition-all flex items-center gap-1.5 cursor-pointer"
                  >
                    Save & Finish <Check size={12} />
                  </button>
                )}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>
    </motion.div>
  );
};
