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
      "Antigravity Director",
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
      .map((part) => part[0])
      .filter(Boolean)
      .slice(0, 2)
      .join("")
      .toUpperCase() || "VY";

  return (
    <div className="space-y-8">
      {/* Top Identity Header & Avatar Row */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6 pb-7 border-b border-slate-200/90">
        <div className="flex items-center gap-5">
          {/* Executive Crest / Avatar with Camera Trigger */}
          <div
            className="relative group cursor-pointer"
            onMouseEnter={playHoverSound}
            onClick={playFocusSound}
            title="Upload New Profile Image"
          >
            <div className="w-20 h-20 sm:w-22 sm:h-22 rounded-2xl bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white flex items-center justify-center font-serif text-2xl sm:text-3xl font-bold tracking-wider shadow-md border-2 border-white ring-1 ring-slate-200">
              {initials}
            </div>
            <div className="absolute inset-0 rounded-2xl bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity flex flex-col items-center justify-center gap-1 backdrop-blur-xs text-white">
              <Camera size={18} />
              <span className="text-[9px] uppercase tracking-wider font-semibold">
                Change
              </span>
            </div>
          </div>

          <div className="space-y-1.5">
            <div className="flex items-center gap-2.5 flex-wrap">
              <h2 className="font-serif text-2xl text-[#0f172a] font-medium tracking-tight">
                {name}
              </h2>
              <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-emerald-50 text-emerald-800 border border-emerald-200 text-[10px] font-mono uppercase font-bold tracking-wider">
                <CheckCircle2 size={11} className="text-emerald-600" />
                Verified Executive Seat
              </span>
            </div>
            <p className="text-xs text-slate-600 font-light">
              Autonomous Consensus Seat ID:{" "}
              <code className="font-mono text-slate-900 bg-slate-100 px-1.5 py-0.5 rounded font-medium">
                VYR-ADM-089
              </code>
            </p>
          </div>
        </div>

        <button
          type="button"
          onClick={playFocusSound}
          onMouseEnter={playHoverSound}
          className="px-4 py-2 rounded-xl text-xs font-semibold bg-slate-100 hover:bg-slate-200 text-slate-800 border border-slate-200 shadow-2xs transition-all active:scale-[0.98] self-start sm:self-center"
        >
          Export Credentials
        </button>
      </div>

      {/* Form Fields: 2-Column Balanced Architecture */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Full Name */}
        <div className="space-y-2">
          <label className="text-xs font-semibold text-slate-800 tracking-wider uppercase flex items-center gap-2">
            <User size={13} className="text-slate-500" />
            Executive Name
          </label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            onFocus={playFocusSound}
            className="w-full bg-slate-50/80 hover:bg-slate-50 focus:bg-white border border-slate-200 rounded-xl px-4 py-3 text-sm font-medium text-[#0f172a] focus:outline-none focus:ring-2 focus:ring-slate-900/15 focus:border-slate-800 transition-all placeholder:text-slate-400 shadow-[inset_0_1px_2px_rgba(0,0,0,0.03)]"
            placeholder="e.g. Subham Rath"
          />
        </div>

        {/* Email Address (Immutable Security) */}
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <label className="text-xs font-semibold text-slate-800 tracking-wider uppercase flex items-center gap-2">
              <Mail size={13} className="text-slate-500" />
              Email Address
            </label>
            <span className="text-[10px] font-mono text-slate-500 flex items-center gap-1">
              <Lock size={10} /> Locked for Security
            </span>
          </div>
          <input
            type="email"
            value={user?.email || "user@example.com"}
            disabled
            className="w-full bg-slate-100/80 border border-slate-200 rounded-xl px-4 py-3 text-sm font-mono text-slate-600 cursor-not-allowed shadow-2xs"
          />
        </div>

        {/* Studio Atelier Domain */}
        <div className="space-y-2">
          <label className="text-xs font-semibold text-slate-800 tracking-wider uppercase flex items-center gap-2">
            <Building size={13} className="text-slate-500" />
            Studio Atelier / Brand Domain
          </label>
          <input
            type="text"
            value={atelier}
            onChange={(e) => setAtelier(e.target.value)}
            onFocus={playFocusSound}
            className="w-full bg-slate-50/80 hover:bg-slate-50 focus:bg-white border border-slate-200 rounded-xl px-4 py-3 text-sm font-medium text-[#0f172a] focus:outline-none focus:ring-2 focus:ring-slate-900/15 focus:border-slate-800 transition-all shadow-[inset_0_1px_2px_rgba(0,0,0,0.03)]"
            placeholder="Atelier domain"
          />
        </div>

        {/* Institutional Privilege */}
        <div className="space-y-2">
          <label className="text-xs font-semibold text-slate-800 tracking-wider uppercase flex items-center gap-2">
            <Shield size={13} className="text-slate-500" />
            Institutional Privilege
          </label>
          <div className="w-full bg-slate-50/80 border border-slate-200 rounded-xl px-4 py-3 flex items-center justify-between shadow-[inset_0_1px_2px_rgba(0,0,0,0.03)]">
            <span className="text-sm font-semibold text-[#0f172a]">
              {profile?.role ? profile.role.toUpperCase() : "CREATIVE DIRECTOR"}
            </span>
            <span className="text-[10px] bg-slate-900 text-white px-2.5 py-0.5 rounded-full font-mono font-bold tracking-wider">
              TIER-1 ACCESS
            </span>
          </div>
        </div>
      </div>

      {/* Tactile Audio Preferences Row */}
      <div className="pt-6 border-t border-slate-200/90 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center gap-2 text-sm font-semibold text-[#0f172a]">
            {isMuted ? (
              <VolumeX size={16} className="text-slate-500" />
            ) : (
              <Volume2 size={16} className="text-emerald-700" />
            )}
            Tactile Audio &amp; Glass Micro-Acoustics
          </div>
          <p className="text-xs text-slate-600 font-light">
            Enable high-frequency glass ticks, haptic feedback, and harmonic completion tones.
          </p>
        </div>

        <button
          type="button"
          onClick={toggleMute}
          onMouseEnter={playHoverSound}
          className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold transition-all shadow-xs ${
            isMuted
              ? "bg-slate-200 text-slate-700 hover:bg-slate-300"
              : "bg-emerald-600 text-white hover:bg-emerald-700"
          }`}
        >
          {isMuted ? "Sound Disabled" : "Acoustics Active"}
        </button>
      </div>

      {/* Action Footer */}
      <div className="pt-6 border-t border-slate-200/90 flex items-center justify-between flex-wrap gap-4">
        <div className="text-xs text-slate-500">
          {savedSuccess ? (
            <span className="text-emerald-700 font-medium flex items-center gap-1.5 animate-in fade-in">
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
          className="bg-[#0f172a] hover:bg-[#1e293b] text-white text-xs sm:text-sm font-semibold px-7 py-3 rounded-xl shadow-[0_4px_16px_rgba(15,23,42,0.18)] transition-all active:scale-[0.98] disabled:opacity-70 flex items-center gap-2"
        >
          {isUpdating ? (
            <div className="w-4 h-4 border-2 border-white/20 border-t-white rounded-full animate-spin" />
          ) : (
            <>
              <Sparkles size={14} className="text-amber-300" />
              Save Changes
            </>
          )}
        </button>
      </div>
    </div>
  );
}
