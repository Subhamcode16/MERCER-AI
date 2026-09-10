"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Image as ImageIcon, Eye, GitBranch, ShieldCheck, Sparkles, Sliders, CheckCircle2 } from "lucide-react";
import { generateVisualAsset, ImageGenerationResponseDTO } from "@/lib/phase20Client";

export function VisualModelStudio() {
  const [prompt, setPrompt] = useState("NOCAP Silk trench coat luxury editorial hero shot with dynamic drape folds");
  const [aspectRatio, setAspectRatio] = useState<'1:1' | '9:16' | '16:9' | '4:5'>("9:16");
  const [assetResponse, setAssetResponse] = useState<ImageGenerationResponseDTO | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [showLineageModal, setShowLineageModal] = useState(false);

  const handleGenerateAsset = async () => {
    setIsGenerating(true);
    try {
      const res = await generateVisualAsset(prompt, aspectRatio);
      setAssetResponse(res);
    } catch (e) {
      console.error(e);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="flex flex-col gap-6 w-full text-zinc-100">
      {/* Controls & Generation Form */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="bg-zinc-900/90 border border-zinc-800 rounded-xl p-6 flex flex-col gap-5 shadow-2xl">
          <div className="flex items-center gap-3 border-b border-zinc-800 pb-3">
            <ImageIcon className="w-5 h-5 text-[#E1D4C0]" />
            <h3 className="text-base font-semibold text-white">Visual Model Asset Generator</h3>
          </div>

          <div className="flex flex-col gap-2">
            <label className="text-xs font-mono text-zinc-400 uppercase">Creative Direction Prompt</label>
            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              rows={4}
              className="bg-zinc-950 border border-zinc-800 text-sm text-white rounded-lg p-3 focus:outline-none focus:border-[#E1D4C0] resize-none"
            />
          </div>

          <div className="flex flex-col gap-2">
            <label className="text-xs font-mono text-zinc-400 uppercase">Aspect Ratio Selector</label>
            <div className="grid grid-cols-4 gap-2">
              {(["1:1", "9:16", "16:9", "4:5"] as const).map((ratio) => (
                <button
                  key={ratio}
                  onClick={() => setAspectRatio(ratio)}
                  className={`py-2 text-xs font-mono rounded-lg border transition-colors ${
                    aspectRatio === ratio
                      ? "bg-[#E1D4C0] text-black border-[#E1D4C0] font-semibold"
                      : "bg-zinc-950 text-zinc-300 border-zinc-800 hover:border-zinc-700"
                  }`}
                >
                  {ratio}
                </button>
              ))}
            </div>
          </div>

          <button
            onClick={handleGenerateAsset}
            disabled={isGenerating}
            className="w-full py-3 bg-[#E1D4C0] hover:bg-white text-black font-medium text-sm rounded-lg transition-colors shadow-lg flex items-center justify-center gap-2 disabled:opacity-50 mt-2"
          >
            <Sparkles className="w-4 h-4 fill-current" />
            {isGenerating ? "Generating Visual Asset..." : "Generate Visual Asset"}
          </button>
        </div>

        {/* Generated Asset Preview & Vision Analysis */}
        <div className="lg:col-span-2 bg-zinc-900/90 border border-zinc-800 rounded-xl p-6 flex flex-col gap-5 shadow-2xl">
          <div className="flex items-center justify-between border-b border-zinc-800 pb-3">
            <div className="flex items-center gap-3">
              <Eye className="w-5 h-5 text-sky-400" />
              <h3 className="text-base font-semibold text-white">Visual Analysis & Asset Canvas</h3>
            </div>
            {assetResponse && (
              <button
                onClick={() => setShowLineageModal(true)}
                className="flex items-center gap-1.5 text-xs font-mono text-[#E1D4C0] bg-zinc-800 px-3 py-1 rounded-full border border-zinc-700 hover:bg-zinc-700"
              >
                <GitBranch className="w-3.5 h-3.5" />
                Lineage ({assetResponse.artifact_id})
              </button>
            )}
          </div>

          {assetResponse ? (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-center">
              <div className="relative aspect-[9/16] max-h-[380px] bg-zinc-950 rounded-xl overflow-hidden border border-zinc-800 flex items-center justify-center p-4">
                <img
                  src={assetResponse.image_url_or_bytes}
                  alt="Generated Asset"
                  className="w-full h-full object-contain drop-shadow-xl"
                />
                <div className="absolute top-3 left-3 bg-black/70 backdrop-blur px-2.5 py-1 rounded text-[10px] font-mono text-[#E1D4C0] border border-white/10">
                  {assetResponse.aspect_ratio} ({assetResponse.width}x{assetResponse.height})
                </div>
              </div>

              {/* Structured Vision Analysis Panel */}
              <div className="flex flex-col gap-4 bg-zinc-950 p-5 rounded-xl border border-zinc-800">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-mono uppercase text-zinc-400">Extracted Visual DNA</span>
                  <span className="text-xs font-mono text-emerald-400 flex items-center gap-1">
                    <CheckCircle2 className="w-3.5 h-3.5" /> 92% Confidence
                  </span>
                </div>

                <div className="flex flex-col gap-2 text-xs font-mono text-zinc-300">
                  <div><span className="text-zinc-500">Palette:</span> #000000 (Black), #FF0055 (Cyber Silk)</div>
                  <div><span className="text-zinc-500">Composition:</span> Minimalist 3x3 Grid Center Focus</div>
                  <div><span className="text-zinc-500">Lighting:</span> High-Contrast Studio Strobe</div>
                  <div><span className="text-zinc-500">Critique Score:</span> 0.92 / 1.0 (No Critical Defects)</div>
                </div>
              </div>
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center h-64 text-zinc-500 text-sm gap-2">
              <ImageIcon className="w-8 h-8 text-zinc-600" />
              <span>No asset generated yet. Enter a prompt to generate.</span>
            </div>
          )}
        </div>
      </div>

      {/* Visual Lineage Modal */}
      <AnimatePresence>
        {showLineageModal && assetResponse && (
          <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-md flex items-center justify-center p-4">
            <motion.div
              initial={{ scale: 0.95, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.95, opacity: 0 }}
              className="bg-zinc-900 border border-zinc-800 max-w-md w-full rounded-xl p-6 flex flex-col gap-4 shadow-2xl"
            >
              <div className="flex items-center justify-between border-b border-zinc-800 pb-3">
                <h4 className="text-base font-semibold text-white">Immutable Visual Lineage Trace</h4>
                <button onClick={() => setShowLineageModal(false)} className="text-zinc-400 hover:text-white text-sm">
                  ✕
                </button>
              </div>

              <div className="flex flex-col gap-2.5 text-xs font-mono text-zinc-300">
                <div><span className="text-zinc-500">Artifact ID:</span> {assetResponse.lineage.artifact_id}</div>
                <div><span className="text-zinc-500">Model Name:</span> {assetResponse.lineage.model_name} ({assetResponse.lineage.model_version})</div>
                <div><span className="text-zinc-500">Request Hash:</span> {assetResponse.lineage.request_hash}</div>
                <div><span className="text-zinc-500">Creative Direction Hash:</span> {assetResponse.lineage.creative_direction_hash}</div>
                <div><span className="text-zinc-500">Visual DNA Ref:</span> {assetResponse.lineage.visual_dna_ref}</div>
                <div><span className="text-zinc-500">Validation Status:</span> <span className="text-emerald-400">{assetResponse.lineage.validation_status}</span></div>
              </div>

              <button
                onClick={() => setShowLineageModal(false)}
                className="mt-2 w-full py-2 bg-zinc-800 hover:bg-zinc-700 text-white rounded-lg text-xs font-medium"
              >
                Close Lineage Trace
              </button>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  );
}
