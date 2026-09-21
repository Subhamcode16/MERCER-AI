"use client";

import React, { useState } from "react";
import {
  User,
  Mail,
  Shield,
  Camera,
  Building,
  Volume2,
  VolumeX,
  CheckCircle2,
  Lock,
  Sparkles,
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
  const [isUpdating, setIsUpdating] = useState(false);
  const [savedSuccess, setSavedSuccess] = useState(false);

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

  const initials =
    name
      .split(" ")
      .map((part: string) => part[0])
      .filter(Boolean)
      .slice(0, 2)
      .join("")
      .toUpperCase() || "JM";

  return (
    <div className="space-y-8 font-sans">
      {/* Top Identity Header & Avatar Row */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6 pb-6 border-b border-[#e3dfd4]">
        <div className="flex items-center gap-5">
          {/* Architectural Crest / Avatar */}
          <div
            className="relative group cursor-pointer"
            onMouseEnter={playHoverSound}
            onClick={playFocusSound}
            title="Upload Profile Crest"
          >
            <div className="w-18 h-18 sm:w-20 sm:h-20 rounded-2xl bg-[#f0ebe1] text-[#0f1419] border border-[#e3dfd4] flex items-center justify-center font-serif text-2xl sm:text-3xl font-bold tracking-wider shadow-xs">
              {initials}
            </div>
            <div className="absolute inset-0 rounded-2xl bg-[#0f1419]/70 opacity-0 group-hover:opacity-100 transition-opacity flex flex-col items-center justify-center gap-1 text-white backdrop-blur-xs">
              <Camera size={16} />
              <span className="text-[9px] uppercase tracking-wider font-semibold font-sans">Change</span>
            </div>
          </div>

          <div className="space-y-1">
            <div className="flex items-center gap-2.5 flex-wrap">
              <h2 className="font-serif text-xl sm:text-2xl text-[#0f1419] font-medium tracking-tight">
                {name}
              </h2>
              <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-[#f0ebe1] text-[#059669] border border-[#e3dfd4] text-[10px] font-mono uppercase font-bold tracking-wider">
                <CheckCircle2 size={11} />
                Verified Director Seat
              </span>
            </div>
            <p className="text-xs text-[#5e6d68] font-normal">
              Autonomous Consensus Seat ID:{" "}
              <code className="font-mono text-[#0f1419] bg-[#f0ebe1] px-1.5 py-0.5 rounded text-[11px] font-semibold">
                VYR-ADM-089
              </code>
            </p>
          </div>
        </div>

        <button
          type="button"
          onClick={playFocusSound}
          onMouseEnter={playHoverSound}
          className="px-3.5 py-2 rounded-xl text-xs font-semibold bg-[#f0ebe1] hover:bg-[#f8f6f0] text-[#0f1419] border border-[#e3dfd4] shadow-2xs transition-all active:scale-[0.98] self-start sm:self-center font-sans"
        >
          Export Credentials
        </button>
      </div>

      {/* Form Fields: 2-Column Balanced Architecture */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
        {/* Full Name */}
        <div className="space-y-2">
          <label className="text-xs font-semibold text-[#0f1419] tracking-wider uppercase flex items-center gap-2 font-sans">
            <User size={13} className="text-[#5e6d68]" />
            Executive Name
          </label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            onFocus={playFocusSound}
            className="w-full bg-[#f8f6f0] hover:bg-white focus:bg-white border border-[#e3dfd4] rounded-xl px-4 py-2.5 text-sm font-medium text-[#0f1419] focus:outline-none focus:border-[#1e3a34] focus:ring-1 focus:ring-[#1e3a34] transition-all placeholder:text-[#5e6d68] font-sans"
            placeholder="e.g. Dr. Julian Mercer"
          />
        </div>

        {/* Email Address (Immutable Security) */}
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <label className="text-xs font-semibold text-[#0f1419] tracking-wider uppercase flex items-center gap-2 font-sans">
              <Mail size={13} className="text-[#5e6d68]" />
              Email Address
            </label>
            <span className="text-[10px] font-mono text-[#5e6d68] flex items-center gap-1 font-bold">
              <Lock size={10} /> Immutable
            </span>
          </div>
          <input
            type="email"
            value={user?.email || "user@example.com"}
            disabled
            className="w-full bg-[#f0ebe1]/70 border border-[#e3dfd4] rounded-xl px-4 py-2.5 text-sm font-mono text-[#5e6d68] cursor-not-allowed"
          />
        </div>

        {/* Studio Atelier Domain */}
        <div className="space-y-2">
          <label className="text-xs font-semibold text-[#0f1419] tracking-wider uppercase flex items-center gap-2 font-sans">
            <Building size={13} className="text-[#5e6d68]" />
            Studio Atelier / Brand Domain
          </label>
          <input
            type="text"
            value={atelier}
            onChange={(e) => setAtelier(e.target.value)}
            onFocus={playFocusSound}
            className="w-full bg-[#f8f6f0] hover:bg-white focus:bg-white border border-[#e3dfd4] rounded-xl px-4 py-2.5 text-sm font-medium text-[#0f1419] focus:outline-none focus:border-[#1e3a34] focus:ring-1 focus:ring-[#1e3a34] transition-all placeholder:text-[#5e6d68] font-sans"
            placeholder="Atelier domain"
          />
        </div>

        {/* Institutional Privilege */}
        <div className="space-y-2">
          <label className="text-xs font-semibold text-[#0f1419] tracking-wider uppercase flex items-center gap-2 font-sans">
            <Shield size={13} className="text-[#5e6d68]" />
            Institutional Privilege
          </label>
          <div className="w-full bg-[#f0ebe1]/70 border border-[#e3dfd4] rounded-xl px-4 py-2.5 flex items-center justify-between">
            <span className="text-sm font-semibold text-[#0f1419] font-sans">
              {profile?.role ? profile.role.toUpperCase() : "CREATIVE DIRECTOR"}
            </span>
            <span className="text-[10px] bg-[#0f1419] text-white px-2.5 py-0.5 rounded-full font-mono font-bold tracking-wider">
              TIER-1 ACCESS
            </span>
          </div>
        </div>
      </div>

      {/* Tactile Audio Preferences Row */}
      <div className="pt-6 border-t border-[#e3dfd4] flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center gap-2 text-sm font-semibold text-[#0f1419] font-sans">
            {isMuted ? (
              <VolumeX size={16} className="text-[#5e6d68]" />
            ) : (
              <Volume2 size={16} className="text-[#059669]" />
            )}
            Tactile Audio &amp; Glass Micro-Acoustics
          </div>
          <p className="text-xs text-[#5e6d68] font-normal font-sans">
            High-frequency glass ticks, haptic feedback, and harmonic completion tones.
          </p>
        </div>

        <button
          type="button"
          onClick={toggleMute}
          onMouseEnter={playHoverSound}
          className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold transition-all shadow-xs font-sans ${
            isMuted
              ? "bg-[#f0ebe1] text-[#5e6d68] hover:bg-[#e3dfd4]"
              : "bg-[#1e3a34] text-white hover:bg-[#284c44]"
          }`}
        >
          {isMuted ? "Sound Disabled" : "Acoustics Active"}
        </button>
      </div>

      {/* Action Footer */}
      <div className="pt-6 border-t border-[#e3dfd4] flex items-center justify-between flex-wrap gap-4">
        <div className="text-xs text-[#5e6d68] font-normal font-sans">
          {savedSuccess ? (
            <span className="text-[#059669] font-semibold flex items-center gap-1.5 animate-in fade-in">
              <CheckCircle2 size={14} /> Profile settings persisted securely.
            </span>
          ) : (
            "Cryptographic seat credentials are synchronized across nodes."
          )}
        </div>

        <button
          type="button"
          onClick={handleUpdate}
          disabled={isUpdating}
          onMouseEnter={playHoverSound}
          className="bg-[#1e3a34] text-white hover:bg-[#284c44] text-xs sm:text-sm font-semibold px-6 py-2.5 rounded-xl shadow-xs transition-all active:scale-[0.98] disabled:opacity-70 flex items-center gap-2 font-sans"
        >
          {isUpdating ? (
            <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
          ) : (
            <>
              <Sparkles size={14} />
              Save Changes
            </>
          )}
        </button>
      </div>
    </div>
  );
}
