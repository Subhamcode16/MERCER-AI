"use client";

import React, { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  User,
  Mail,
  Shield,
  Camera,
  Volume2,
  VolumeX,
  CheckCircle2,
  Check,
  Lock,
  AlertCircle,
  X,
  Trash2,
} from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";
import { supabase } from "@/lib/supabase";
import { useTactileAudio } from "@/components/dashboard/useTactileAudio";

const ALLOWED_MIME_TYPES = [
  "image/png",
  "image/jpeg",
  "image/jpg",
  "image/webp",
  "image/gif",
];

const ALLOWED_EXTENSIONS = [".png", ".jpg", ".jpeg", ".webp", ".gif"];
const MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024; // 5 MB

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
  const [avatarUrl, setAvatarUrl] = useState<string | null>(
    user?.user_metadata?.avatar_url || null,
  );
  const [isUpdating, setIsUpdating] = useState(false);
  const [savedSuccess, setSavedSuccess] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const fileInputRef = useRef<HTMLInputElement>(null);

  // Auto-dismiss error after 5 seconds
  useEffect(() => {
    if (errorMessage) {
      const timer = setTimeout(() => setErrorMessage(null), 5000);
      return () => clearTimeout(timer);
    }
  }, [errorMessage]);

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
  }, [name, avatarUrl]);

  const handleAvatarClick = () => {
    playFocusSound();
    setErrorMessage(null);
    fileInputRef.current?.click();
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Reset input value so re-selecting same file triggers change
    e.target.value = "";

    // 1. Validate File Extension
    const fileName = file.name.toLowerCase();
    const hasValidExtension = ALLOWED_EXTENSIONS.some((ext) =>
      fileName.endsWith(ext),
    );

    // 2. Validate MIME Type
    const hasValidMime = ALLOWED_MIME_TYPES.includes(file.type.toLowerCase());

    if (!hasValidExtension || !hasValidMime) {
      setErrorMessage(
        "Unsupported file format. Please upload a PNG, JPG, WEBP, or GIF image.",
      );
      return;
    }

    // 3. Validate File Size
    if (file.size > MAX_FILE_SIZE_BYTES) {
      setErrorMessage(
        "File size exceeds the 5MB limit. Please upload a smaller image.",
      );
      return;
    }

    // Clear any previous error and generate preview
    setErrorMessage(null);
    playSubmitSound();

    const reader = new FileReader();
    reader.onload = (event) => {
      if (event.target?.result) {
        setAvatarUrl(event.target.result as string);
      }
    };
    reader.readAsDataURL(file);
  };

  const handleRemoveAvatar = () => {
    playFocusSound();
    setAvatarUrl(null);
    setErrorMessage(null);
  };

  const handleUpdate = async () => {
    setIsUpdating(true);
    playSubmitSound();
    try {
      const { error } = await supabase.auth.updateUser({
        data: { full_name: name, avatar_url: avatarUrl },
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
      
      {/* Hidden File Input with accept filter */}
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileChange}
        accept="image/png,image/jpeg,image/jpg,image/webp,image/gif"
        className="hidden"
        aria-label="Upload profile photo"
      />

      {/* Avatar & User Details */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-5 pb-6 border-b border-[var(--line)]">
        <div className="flex items-center gap-4">
          <div
            className="relative group cursor-pointer"
            onMouseEnter={playHoverSound}
            onClick={handleAvatarClick}
            title="Click to upload profile photo"
          >
            <div className="w-16 h-16 rounded-full bg-[var(--soft)] text-[var(--ink)] border border-[var(--line)] flex items-center justify-center overflow-hidden shadow-2xs">
              {avatarUrl ? (
                <img
                  src={avatarUrl}
                  alt={name}
                  className="w-full h-full object-cover"
                />
              ) : (
                <span className="font-serif text-2xl font-bold tracking-wider">
                  {initials}
                </span>
              )}
            </div>
            <div className="absolute inset-0 rounded-full bg-black/75 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center text-white backdrop-blur-xs">
              <Camera size={16} />
            </div>
          </div>

          <div className="space-y-1">
            <h2 className="font-serif text-xl sm:text-2xl text-[var(--ink)] font-medium tracking-tight">
              {name}
            </h2>
            <div className="flex items-center gap-2 flex-wrap">
              <span className="text-xs text-[var(--muted)] font-normal">
                {user?.email || "user@example.com"}
              </span>
              <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-[var(--soft)] text-emerald-500 text-[10px] font-mono font-bold">
                <CheckCircle2 size={10} /> Verified
              </span>
              {avatarUrl && (
                <button
                  type="button"
                  onClick={handleRemoveAvatar}
                  onMouseEnter={playHoverSound}
                  className="inline-flex items-center gap-1 text-[11px] text-red-500 hover:underline font-sans ml-1"
                >
                  <Trash2 size={11} /> Remove photo
                </button>
              )}
            </div>
          </div>
        </div>

        <div className="px-3 py-1 rounded-full bg-[var(--soft)] border border-[var(--line)] text-[11px] font-mono text-[var(--muted)]">
          Role: <strong className="text-[var(--ink)] uppercase">{profile?.role || "Creative Director"}</strong>
        </div>
      </div>

      {/* Security Validation Error Alert */}
      {errorMessage && (
        <div className="p-3.5 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 text-xs font-medium flex items-center justify-between gap-3 animate-in fade-in">
          <div className="flex items-center gap-2">
            <AlertCircle size={15} className="shrink-0 text-red-500" />
            <span>{errorMessage}</span>
          </div>
          <button
            type="button"
            onClick={() => setErrorMessage(null)}
            className="p-1 hover:bg-red-500/20 rounded text-red-400 transition-colors"
          >
            <X size={13} />
          </button>
        </div>
      )}

      {/* Form Fields */}
      <div className="space-y-5">
        {/* Full Name */}
        <div className="space-y-1.5">
          <label className="text-xs font-semibold text-[var(--ink)] uppercase tracking-wider flex items-center gap-2 font-sans">
            <User size={13} className="text-[var(--muted)]" />
            Full Name
          </label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            onFocus={playFocusSound}
            className="w-full bg-[var(--paper)] hover:bg-[var(--soft)] focus:bg-[var(--soft)] border border-[var(--line)] rounded-xl px-4 py-2.5 text-sm font-medium text-[var(--ink)] focus:outline-none focus:border-[var(--accent)] focus:ring-1 focus:ring-[var(--accent)] transition-all placeholder:text-[var(--muted)] font-sans"
            placeholder="e.g. Dr. Julian Mercer"
          />
        </div>

        {/* Email Address */}
        <div className="space-y-1.5">
          <div className="flex items-center justify-between">
            <label className="text-xs font-semibold text-[var(--ink)] uppercase tracking-wider flex items-center gap-2 font-sans">
              <Mail size={13} className="text-[var(--muted)]" />
              Email Address
            </label>
            <span className="text-[10px] font-mono text-[var(--muted)] flex items-center gap-1 font-bold">
              <Lock size={10} /> Immutable
            </span>
          </div>
          <input
            type="email"
            value={user?.email || "user@example.com"}
            disabled
            className="w-full bg-[var(--soft)]/80 border border-[var(--line)] rounded-xl px-4 py-2.5 text-sm font-mono text-[var(--muted)] cursor-not-allowed"
          />
          <p className="text-[11px] text-[var(--muted)] font-normal">
            Your email is managed via your authentication provider and cannot be modified here.
          </p>
        </div>

        {/* Account Role & Privilege */}
        <div className="space-y-1.5">
          <label className="text-xs font-semibold text-[var(--ink)] uppercase tracking-wider flex items-center gap-2 font-sans">
            <Shield size={13} className="text-[var(--muted)]" />
            Account Privilege Tier
          </label>
          <div className="w-full bg-[var(--soft)]/80 border border-[var(--line)] rounded-xl px-4 py-2.5 flex items-center justify-between">
            <span className="text-sm font-semibold text-[var(--ink)] font-sans">
              {profile?.role ? profile.role.toUpperCase() : "CREATIVE DIRECTOR"}
            </span>
            <span className="inline-flex items-center gap-1.5 bg-emerald-500/15 text-emerald-500 border border-emerald-500/30 text-[11px] font-medium px-2.5 py-0.5 rounded-full font-sans shadow-xs">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
              Tier 1 Active
            </span>
          </div>
        </div>

        {/* Tactile Audio Row */}
        <div className="pt-4 border-t border-[var(--line)] flex items-center justify-between gap-4">
          <div className="space-y-0.5">
            <div className="flex items-center gap-2 text-xs font-semibold text-[var(--ink)] font-sans">
              {isMuted ? <VolumeX size={15} className="text-[var(--muted)]" /> : <Volume2 size={15} className="text-emerald-500" />}
              Tactile Audio Feedback
            </div>
            <p className="text-[11px] text-[var(--muted)] font-normal">
              Play subtle acoustic glass clicks and completion chimes across the app.
            </p>
          </div>

          <button
            type="button"
            role="switch"
            aria-checked={!isMuted}
            onClick={toggleMute}
            onMouseEnter={playHoverSound}
            aria-label={isMuted ? "Enable tactile audio feedback" : "Disable tactile audio feedback"}
            className={`relative inline-flex h-6 w-11 shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none ${
              !isMuted ? "bg-[var(--accent)]" : "bg-[var(--soft)] border-[var(--line)]"
            }`}
          >
            <motion.span
              layout
              transition={{ type: "spring", stiffness: 500, damping: 30 }}
              className={`pointer-events-none inline-block h-5 w-5 rounded-full bg-white shadow-xs ring-0 transition-transform ${
                !isMuted ? "translate-x-5" : "translate-x-0"
              }`}
            />
          </button>
        </div>
      </div>

      {/* Action Footer */}
      <div className="pt-6 border-t border-[var(--line)] flex items-center justify-between flex-wrap gap-4">
        <div className="text-xs text-[var(--muted)] min-h-[20px] flex items-center">
          <AnimatePresence mode="wait">
            {savedSuccess ? (
              <motion.div
                key="saved"
                initial={{ opacity: 0, y: 3 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -3 }}
                transition={{ duration: 0.2 }}
                className="text-emerald-500 font-semibold flex items-center gap-1.5 font-sans"
              >
                <CheckCircle2 size={14} /> Profile settings saved successfully.
              </motion.div>
            ) : (
              <motion.div
                key="idle"
                initial={{ opacity: 0, y: 3 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -3 }}
                transition={{ duration: 0.2 }}
              >
                All profile changes are synchronized to your account.
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        <motion.button
          type="button"
          layout
          onClick={handleUpdate}
          disabled={isUpdating}
          onMouseEnter={playHoverSound}
          whileTap={{ scale: 0.97 }}
          className={`text-[var(--accent-ink)] text-xs sm:text-sm font-semibold px-6 py-2.5 rounded-xl shadow-xs transition-all duration-300 disabled:opacity-70 flex items-center gap-2 overflow-hidden bg-[var(--accent)] hover:opacity-90 active:scale-[0.98]`}
        >
          <AnimatePresence mode="wait" initial={false}>
            {isUpdating ? (
              <motion.div
                key="updating"
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.8 }}
                className="flex items-center gap-2"
              >
                <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
                <span>Saving...</span>
              </motion.div>
            ) : savedSuccess ? (
              <motion.div
                key="saved"
                initial={{ opacity: 0, y: 4, scale: 0.95 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: -4, scale: 0.95 }}
                transition={{ type: "spring", stiffness: 450, damping: 25 }}
                className="flex items-center gap-1.5"
              >
                <Check size={14} className="stroke-[2.5]" />
                <span>Changes Saved</span>
              </motion.div>
            ) : (
              <motion.div
                key="idle"
                initial={{ opacity: 0, y: 4 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -4 }}
                transition={{ duration: 0.15 }}
                className="flex items-center gap-2"
              >
                <span>Save Changes</span>
                <kbd className="hidden sm:inline-block px-1.5 py-0.5 text-[10px] font-mono bg-white/20 rounded ml-1 text-inherit">
                  ⌘S
                </kbd>
              </motion.div>
            )}
          </AnimatePresence>
        </motion.button>
      </div>

    </div>
  );
}
