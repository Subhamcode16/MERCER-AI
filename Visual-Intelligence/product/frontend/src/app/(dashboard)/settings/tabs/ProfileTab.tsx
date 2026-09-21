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
      .map((part) => part[0])
      .filter(Boolean)
      .slice(0, 2)
      .join("")
      .toUpperCase() || "JM";

  return (
    <div className="space-y-8">
      {/* Top Identity Header & Avatar Row */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6 pb-6 border-b border-[var(--line)]">
        <div className="flex items-center gap-5">
          {/* Architectural Crest / Avatar */}
          <div
            className="relative group cursor-pointer"
            onMouseEnter={playHoverSound}
            onClick={playFocusSound}
            title="Upload Profile Crest"
          >
            <div className="w-18 h-18 sm:w-20 sm:h-20 rounded-2xl bg-[var(--soft)] text-[var(--ink)] border border-[var(--line)] flex items-center justify-center font-serif text-2xl sm:text-3xl font-bold tracking-wider shadow-xs">
              {initials}
            </div>
            <div className="absolute inset-0 rounded-2xl bg-[var(--ink)]/60 opacity-0 group-hover:opacity-100 transition-opacity flex flex-col items-center justify-center gap-1 text-[var(--surface)] backdrop-blur-xs">
              <Camera size={16} />
              <span className="text-[9px] uppercase tracking-wider font-semibold">Change</span>
            </div>
          </div>

          <div className="space-y-1">
            <div className="flex items-center gap-2.5 flex-wrap">
              <h2 className="font-serif text-xl sm:text-2xl text-[var(--ink)] font-medium tracking-tight">
                {name}
              </h2>
              <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-[var(--soft)] text-[var(--activity)] border border-[var(--line)] text-[10px] font-mono uppercase font-bold tracking-wider">
                <CheckCircle2 size={11} />
                Verified Director Seat
              </span>
            </div>
            <p className="text-xs text-[var(--muted)] font-light">
              Autonomous Consensus Seat ID:{" "}
              <code className="font-mono text-[var(--ink)] bg-[var(--soft)] px-1.5 py-0.5 rounded text-[11px]">
                VYR-ADM-089
              </code>
            </p>
          </div>
        </div>

        <button
          type="button"
          onClick={playFocusSound}
          onMouseEnter={playHoverSound}
          className="px-3.5 py-2 rounded-xl text-xs font-semibold bg-[var(--soft)] hover:bg-[var(--paper)] text-[var(--ink)] border border-[var(--line)] shadow-2xs transition-all active:scale-[0.98] self-start sm:self-center"
        >
          Export Credentials
        </button>
      </div>

      {/* Form Fields: 2-Column Balanced Architecture */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
        {/* Full Name */}
        <div className="space-y-2">
          <label className="text-xs font-semibold text-[var(--ink)] tracking-wider uppercase flex items-center gap-2">
            <User size={13} className="text-[var(--muted)]" />
            Executive Name
          </label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            onFocus={playFocusSound}
            className="w-full bg-[var(--paper)] hover:bg-[var(--surface)] focus:bg-[var(--surface)] border border-[var(--line)] rounded-xl px-4 py-2.5 text-sm font-medium text-[var(--ink)] focus:outline-none focus:border-[var(--accent)] transition-all placeholder:text-[var(--muted)]"
            placeholder="e.g. Dr. Julian Mercer"
          />
        </div>

        {/* Email Address (Immutable Security) */}
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <label className="text-xs font-semibold text-[var(--ink)] tracking-wider uppercase flex items-center gap-2">
              <Mail size={13} className="text-[var(--muted)]" />
              Email Address
            </label>
            <span className="text-[10px] font-mono text-[var(--muted)] flex items-center gap-1">
              <Lock size={10} /> Immutable
            </span>
          </div>
          <input
            type="email"
            value={user?.email || "user@example.com"}
            disabled
            className="w-full bg-[var(--soft)]/70 border border-[var(--line)] rounded-xl px-4 py-2.5 text-sm font-mono text-[var(--muted)] cursor-not-allowed"
          />
        </div>

        {/* Studio Atelier Domain */}
        <div className="space-y-2">
          <label className="text-xs font-semibold text-[var(--ink)] tracking-wider uppercase flex items-center gap-2">
            <Building size={13} className="text-[var(--muted)]" />
            Studio Atelier / Brand Domain
          </label>
          <input
            type="text"
            value={atelier}
            onChange={(e) => setAtelier(e.target.value)}
            onFocus={playFocusSound}
            className="w-full bg-[var(--paper)] hover:bg-[var(--surface)] focus:bg-[var(--surface)] border border-[var(--line)] rounded-xl px-4 py-2.5 text-sm font-medium text-[var(--ink)] focus:outline-none focus:border-[var(--accent)] transition-all placeholder:text-[var(--muted)]"
            placeholder="Atelier domain"
          />
        </div>

        {/* Institutional Privilege */}
        <div className="space-y-2">
          <label className="text-xs font-semibold text-[var(--ink)] tracking-wider uppercase flex items-center gap-2">
            <Shield size={13} className="text-[var(--muted)]" />
            Institutional Privilege
          </label>
          <div className="w-full bg-[var(--soft)]/70 border border-[var(--line)] rounded-xl px-4 py-2.5 flex items-center justify-between">
            <span className="text-sm font-medium text-[var(--ink)]">
              {profile?.role ? profile.role.toUpperCase() : "CREATIVE DIRECTOR"}
            </span>
            <span className="text-[10px] bg-[var(--ink)] text-[var(--surface)] px-2.5 py-0.5 rounded-full font-mono font-bold tracking-wider">
              TIER-1 ACCESS
            </span>
          </div>
        </div>
      </div>

      {/* Tactile Audio Preferences Row */}
      <div className="pt-6 border-t border-[var(--line)] flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center gap-2 text-sm font-semibold text-[var(--ink)]">
            {isMuted ? (
              <VolumeX size={16} className="text-[var(--muted)]" />
            ) : (
              <Volume2 size={16} className="text-[var(--activity)]" />
            )}
            Tactile Audio &amp; Glass Micro-Acoustics
          </div>
          <p className="text-xs text-[var(--muted)] font-light">
            High-frequency glass ticks, haptic feedback, and harmonic completion tones.
          </p>
        </div>

        <button
          type="button"
          onClick={toggleMute}
          onMouseEnter={playHoverSound}
          className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold transition-all shadow-xs ${
            isMuted
              ? "bg-[var(--soft)] text-[var(--muted)] hover:bg-[var(--line)]"
              : "bg-[var(--accent)] text-[var(--accent-ink)] hover:opacity-90"
          }`}
        >
          {isMuted ? "Sound Disabled" : "Acoustics Active"}
        </button>
      </div>

      {/* Action Footer */}
      <div className="pt-6 border-t border-[var(--line)] flex items-center justify-between flex-wrap gap-4">
        <div className="text-xs text-[var(--muted)]">
          {savedSuccess ? (
            <span className="text-[var(--activity)] font-medium flex items-center gap-1.5 animate-in fade-in">
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
          className="bg-[var(--accent)] text-[var(--accent-ink)] hover:opacity-90 text-xs sm:text-sm font-semibold px-6 py-2.5 rounded-xl shadow-xs transition-all active:scale-[0.98] disabled:opacity-70 flex items-center gap-2"
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
