"use client";

import React, { useState, useEffect } from "react";
import {
  Camera,
  CheckCircle2,
  Lock,
  Sparkles,
  Key,
  Copy,
  Check,
  Laptop,
  Volume2,
  VolumeX,
  Sliders,
  Shield,
  ArrowUpRight,
} from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";
import { supabase } from "@/lib/supabase";
import { useTactileAudio } from "@/components/dashboard/useTactileAudio";

export default function ProfileTab() {
  const { session, profile } = useAuth();
  const { isMuted, toggleMute, playHoverSound, playFocusSound, playSubmitSound } =
    useTactileAudio();

  const user = session?.user;
  const [name, setName] = useState(
    user?.user_metadata?.full_name ||
      profile?.email?.split("@")[0] ||
      "Dr. Julian Mercer",
  );
  const [atelier, setAtelier] = useState("MERCER-VYREN Atelier");
  const [colorProfile, setColorProfile] = useState("banarasi");
  const [isUpdating, setIsUpdating] = useState(false);
  const [savedSuccess, setSavedSuccess] = useState(false);
  const [copiedKey, setCopiedKey] = useState(false);

  // Keyboard shortcut ⌘S / Ctrl+S to save
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "s") {
        e.preventDefault();
        handleUpdate();
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [name, atelier]);

  const handleUpdate = async () => {
    setIsUpdating(true);
    playSubmitSound();
    try {
      const { error } = await supabase.auth.updateUser({
        data: { full_name: name, atelier },
      });
      if (error) throw error;
      setSavedSuccess(true);
      setTimeout(() => setSavedSuccess(false), 3000);
    } catch (err) {
      console.error("Failed to update profile:", err);
    } finally {
      setIsUpdating(false);
    }
  };

  const copyApiKey = () => {
    playFocusSound();
    navigator.clipboard.writeText("vy_live_9f829a73812dc4e9a01e3a34");
    setCopiedKey(true);
    setTimeout(() => setCopiedKey(false), 2000);
  };

  const initials =
    name
      .split(" ")
      .map((part: string) => part[0])
      .filter(Boolean)
      .slice(0, 2)
      .join("")
      .toUpperCase() || "JM";

  return (
    <div className="space-y-10 font-sans pb-4">
      
      {/* 1. Atelier Director Monogram Seal & Executive Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6 pb-7 border-b border-[#e3dfd4]">
        <div className="flex items-center gap-5">
          {/* Engraved Seal Monogram */}
          <div
            className="relative group cursor-pointer"
            onMouseEnter={playHoverSound}
            onClick={playFocusSound}
            title="Upload Profile Crest"
          >
            <div className="w-16 h-16 sm:w-18 sm:h-18 rounded-full bg-[#fdfcf9] border-2 border-[#1e3a34]/30 flex items-center justify-center font-serif text-2xl font-bold tracking-wider text-[#0f1419] shadow-xs relative overflow-hidden transition-all group-hover:border-[#1e3a34] group-hover:shadow-sm">
              <span className="relative z-10">{initials}</span>
              <div className="absolute inset-1 rounded-full border border-dashed border-[#e3dfd4] pointer-events-none" />
              <div className="absolute inset-0 bg-[#1e3a34]/5 opacity-0 group-hover:opacity-100 transition-opacity" />
            </div>
            <div className="absolute inset-0 rounded-full bg-[#0f1419]/80 opacity-0 group-hover:opacity-100 transition-opacity flex flex-col items-center justify-center gap-0.5 text-white backdrop-blur-xs">
              <Camera size={14} />
              <span className="text-[8px] uppercase tracking-wider font-semibold font-mono">Edit</span>
            </div>
          </div>

          <div className="space-y-1">
            <div className="flex items-center gap-3 flex-wrap">
              <h2 className="font-serif text-2xl text-[#0f1419] font-medium tracking-tight">
                {name}
              </h2>
              <div className="flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-[#f0ebe1] text-[#1e3a34] text-[10px] font-mono font-bold tracking-wider uppercase border border-[#e3dfd4]">
                <span className="w-1.5 h-1.5 rounded-full bg-[#059669]" />
                Director Clearance · Tier 1
              </div>
            </div>
            <p className="text-xs text-[#5e6d68] font-normal flex items-center gap-2">
              <span>Node Consensus ID:</span>
              <code className="font-mono text-[#0f1419] font-semibold tracking-wider text-[11px]">
                VYR-ADM-089
              </code>
            </p>
          </div>
        </div>

        <button
          type="button"
          onClick={playFocusSound}
          onMouseEnter={playHoverSound}
          className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-semibold text-[#0f1419] hover:bg-[#f0ebe1] border border-[#e3dfd4] transition-all self-start sm:self-center font-sans shadow-2xs active:scale-[0.98]"
        >
          <span>Export ID Token</span>
          <ArrowUpRight size={13} className="text-[#5e6d68]" />
        </button>
      </div>

      {/* 2. Architectural Specification Sheet (Flush Hairline Rows) */}
      <div className="space-y-1">
        <div className="text-[10px] font-mono uppercase tracking-widest text-[#5e6d68] font-bold pb-2">
          01 // Executive &amp; Atelier Specifications
        </div>

        <div className="divide-y divide-[#e3dfd4] border-y border-[#e3dfd4]">
          {/* Executive Name Row */}
          <div className="grid grid-cols-1 sm:grid-cols-12 gap-2 sm:gap-4 py-3.5 items-center hover:bg-[#faf8f4]/60 transition-colors px-2 -mx-2 rounded-lg">
            <label className="sm:col-span-4 text-xs font-semibold text-[#0f1419] uppercase tracking-wider font-sans">
              Executive Full Name
            </label>
            <div className="sm:col-span-8">
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                onFocus={playFocusSound}
                className="w-full bg-transparent border-0 border-b border-transparent focus:border-[#1e3a34] px-1 py-1 text-sm font-medium text-[#0f1419] focus:outline-none transition-colors placeholder:text-[#5e6d68] font-sans"
                placeholder="Dr. Julian Mercer"
              />
            </div>
          </div>

          {/* Email Address Row */}
          <div className="grid grid-cols-1 sm:grid-cols-12 gap-2 sm:gap-4 py-3.5 items-center hover:bg-[#faf8f4]/60 transition-colors px-2 -mx-2 rounded-lg">
            <div className="sm:col-span-4 flex items-center gap-2">
              <span className="text-xs font-semibold text-[#0f1419] uppercase tracking-wider font-sans">
                Immutable Email
              </span>
              <Lock size={11} className="text-[#5e6d68]" />
            </div>
            <div className="sm:col-span-8 flex items-center justify-between">
              <span className="font-mono text-xs text-[#5e6d68] select-all">
                {user?.email || "user@example.com"}
              </span>
              <span className="text-[10px] font-mono text-[#5e6d68] bg-[#f0ebe1] px-2 py-0.5 rounded border border-[#e3dfd4]">
                Verified
              </span>
            </div>
          </div>

          {/* Studio Atelier Domain Row */}
          <div className="grid grid-cols-1 sm:grid-cols-12 gap-2 sm:gap-4 py-3.5 items-center hover:bg-[#faf8f4]/60 transition-colors px-2 -mx-2 rounded-lg">
            <label className="sm:col-span-4 text-xs font-semibold text-[#0f1419] uppercase tracking-wider font-sans">
              Brand Domain &amp; Atelier
            </label>
            <div className="sm:col-span-8">
              <input
                type="text"
                value={atelier}
                onChange={(e) => setAtelier(e.target.value)}
                onFocus={playFocusSound}
                className="w-full bg-transparent border-0 border-b border-transparent focus:border-[#1e3a34] px-1 py-1 text-sm font-medium text-[#0f1419] focus:outline-none transition-colors placeholder:text-[#5e6d68] font-sans"
                placeholder="MERCER-VYREN Atelier"
              />
            </div>
          </div>

          {/* Default Shader Pipeline */}
          <div className="grid grid-cols-1 sm:grid-cols-12 gap-2 sm:gap-4 py-3.5 items-center hover:bg-[#faf8f4]/60 transition-colors px-2 -mx-2 rounded-lg">
            <div className="sm:col-span-4">
              <div className="text-xs font-semibold text-[#0f1419] uppercase tracking-wider font-sans">
                Render Engine Shader
              </div>
              <p className="text-[11px] text-[#5e6d68] font-normal">
                Default fabric physics pipeline
              </p>
            </div>
            <div className="sm:col-span-8">
              <div className="inline-flex items-center gap-1.5 p-1 bg-[#f0ebe1] rounded-xl border border-[#e3dfd4]">
                {[
                  { id: "banarasi", label: "Banarasi Silk (Volumetric)" },
                  { id: "daylight", label: "Daylight Meadow" },
                  { id: "tungsten", label: "Tungsten Minimal" },
                ].map((shader) => (
                  <button
                    key={shader.id}
                    type="button"
                    onClick={() => {
                      playFocusSound();
                      setColorProfile(shader.id);
                    }}
                    onMouseEnter={playHoverSound}
                    className={`px-3 py-1 rounded-lg text-xs font-semibold transition-all ${
                      colorProfile === shader.id
                        ? "bg-white text-[#0f1419] shadow-2xs border border-[#e3dfd4]"
                        : "text-[#5e6d68] hover:text-[#0f1419]"
                    }`}
                  >
                    {shader.label}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Tactile Audio Row */}
          <div className="grid grid-cols-1 sm:grid-cols-12 gap-2 sm:gap-4 py-3.5 items-center hover:bg-[#faf8f4]/60 transition-colors px-2 -mx-2 rounded-lg">
            <div className="sm:col-span-4">
              <div className="text-xs font-semibold text-[#0f1419] uppercase tracking-wider font-sans">
                Tactile Audio Feedback
              </div>
              <p className="text-[11px] text-[#5e6d68] font-normal">
                Subtle glass ticks on click &amp; completion
              </p>
            </div>
            <div className="sm:col-span-8 flex items-center justify-between">
              <span className="text-xs text-[#5e6d68] font-mono">
                {isMuted ? "Sound disabled globally" : "Harmonic glass micro-acoustics active"}
              </span>
              <button
                type="button"
                onClick={toggleMute}
                onMouseEnter={playHoverSound}
                className={`flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-semibold border transition-all ${
                  isMuted
                    ? "bg-[#f0ebe1] text-[#5e6d68] border-[#e3dfd4] hover:bg-[#e3dfd4]"
                    : "bg-[#1e3a34] text-white border-[#1e3a34] hover:bg-[#142824]"
                }`}
              >
                {isMuted ? <VolumeX size={13} /> : <Volume2 size={13} />}
                <span>{isMuted ? "Muted" : "Active"}</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* 3. Cryptographic API Keys & Live Session Strip */}
      <div className="space-y-3">
        <div className="text-[10px] font-mono uppercase tracking-widest text-[#5e6d68] font-bold">
          02 // Cryptographic Node &amp; Developer Governance
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {/* API Key Row */}
          <div className="p-4 rounded-xl bg-[#faf8f4] border border-[#e3dfd4] flex flex-col justify-between gap-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-[#0f1419] flex items-center gap-1.5 font-sans">
                <Key size={13} className="text-[#059669]" />
                CLI &amp; Studio Secret Key
              </span>
              <span className="text-[10px] font-mono text-[#059669] bg-white px-2 py-0.5 rounded border border-[#e3dfd4] font-bold">
                LIVE NODE
              </span>
            </div>

            <div className="flex items-center gap-2">
              <code className="flex-1 bg-white border border-[#e3dfd4] rounded-lg px-3 py-1.5 text-xs font-mono text-[#5e6d68] tracking-wider select-all">
                vy_live_9f82••••••••3a34
              </code>
              <button
                type="button"
                onClick={copyApiKey}
                onMouseEnter={playHoverSound}
                className="px-2.5 py-1.5 rounded-lg bg-white hover:bg-[#f0ebe1] text-[#0f1419] border border-[#e3dfd4] text-xs font-semibold transition-all flex items-center gap-1.5 shrink-0"
              >
                {copiedKey ? (
                  <>
                    <Check size={12} className="text-[#059669]" />
                    <span className="text-[#059669]">Copied</span>
                  </>
                ) : (
                  <>
                    <Copy size={12} />
                    <span>Copy</span>
                  </>
                )}
              </button>
            </div>
          </div>

          {/* Active Session Node */}
          <div className="p-4 rounded-xl bg-[#faf8f4] border border-[#e3dfd4] flex flex-col justify-between gap-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-[#0f1419] flex items-center gap-1.5 font-sans">
                <Laptop size={13} className="text-[#059669]" />
                Active Hardware Node Session
              </span>
              <div className="flex items-center gap-1.5 text-[10px] font-mono text-[#059669] font-bold">
                <span className="w-1.5 h-1.5 rounded-full bg-[#059669] animate-pulse" />
                SYNCED
              </div>
            </div>

            <div className="text-xs text-[#5e6d68] font-mono bg-white border border-[#e3dfd4] rounded-lg px-3 py-1.5">
              macOS · Chrome 127 · US-East (0ms drift)
            </div>
          </div>
        </div>
      </div>

      {/* 4. Anchored Studio Action Dock */}
      <div className="pt-6 border-t border-[#e3dfd4] flex items-center justify-between flex-wrap gap-4">
        <div className="text-xs text-[#5e6d68] flex items-center gap-2 font-mono">
          {savedSuccess ? (
            <span className="text-[#059669] font-semibold flex items-center gap-1.5 animate-in fade-in">
              <CheckCircle2 size={14} /> All governance preferences synchronized to cluster.
            </span>
          ) : (
            <span className="flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-[#059669]" />
              Consensus synchronized across global nodes.
            </span>
          )}
        </div>

        <div className="flex items-center gap-3">
          <button
            type="button"
            onClick={handleUpdate}
            disabled={isUpdating}
            onMouseEnter={playHoverSound}
            className="bg-[#1e3a34] hover:bg-[#142824] text-white text-xs sm:text-sm font-semibold px-5 py-2.5 rounded-xl shadow-xs transition-all active:scale-[0.98] disabled:opacity-70 flex items-center gap-2 font-sans"
          >
            {isUpdating ? (
              <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
            ) : (
              <>
                <Sparkles size={14} />
                <span>Save Changes</span>
                <kbd className="hidden sm:inline-block px-1.5 py-0.5 text-[10px] font-mono bg-white/20 rounded ml-1 text-white/90">
                  ⌘S
                </kbd>
              </>
            )}
          </button>
        </div>
      </div>

    </div>
  );
}
