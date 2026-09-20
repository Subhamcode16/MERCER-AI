"use client";

import { useCallback, useState, useEffect } from "react";

// Global singleton state so all components stay 100% in sync across layout, promptbox, dock, etc.
let globalIsMuted = false;
let globalBgAudio: HTMLAudioElement | null = null;
let globalAudioCtx: AudioContext | null = null;
let lastHoverTimestamp = 0;
const listeners = new Set<(muted: boolean) => void>();

function notifyListeners() {
  listeners.forEach((fn) => fn(globalIsMuted));
}

function initBgAudio() {
  if (typeof window === "undefined") return;
  if (!globalBgAudio) {
    globalBgAudio = new Audio("/audio/meadow-ambience.mp3");
    globalBgAudio.loop = true;
    // Keep ambient noise at a pleasant background level so haptic clicks cut through with crystal clarity
    globalBgAudio.volume = 0.16;
    globalBgAudio.preload = "auto";
  }
}

function tryStartBgAudio() {
  if (typeof window === "undefined" || globalIsMuted) return;
  initBgAudio();
  if (globalBgAudio && globalBgAudio.paused) {
    globalBgAudio.play().catch(() => {
      // Browser blocked autoplay until first user gesture
    });
  }
}

export function useTactileAudio() {
  const [isMuted, setIsMuted] = useState(globalIsMuted);

  useEffect(() => {
    const handler = (muted: boolean) => setIsMuted(muted);
    listeners.add(handler);

    initBgAudio();

    // Auto-start ambient audio on first user gesture anywhere on the window
    const handleFirstGesture = () => {
      tryStartBgAudio();
    };

    window.addEventListener("pointerdown", handleFirstGesture);
    window.addEventListener("keydown", handleFirstGesture);
    window.addEventListener("touchstart", handleFirstGesture);

    // Also attempt immediate playback
    tryStartBgAudio();

    return () => {
      listeners.delete(handler);
      window.removeEventListener("pointerdown", handleFirstGesture);
      window.removeEventListener("keydown", handleFirstGesture);
      window.removeEventListener("touchstart", handleFirstGesture);
    };
  }, []);

  const getAudioContext = useCallback(() => {
    if (typeof window === "undefined") return null;
    if (!globalAudioCtx) {
      const AudioCtx = window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
      if (AudioCtx) {
        globalAudioCtx = new AudioCtx();
      }
    }
    if (globalAudioCtx && globalAudioCtx.state === "suspended") {
      globalAudioCtx.resume().catch(() => {});
    }
    return globalAudioCtx;
  }, []);

  // Crisp, high-definition haptic click with dual-harmonic presence
  const playHoverSound = useCallback(() => {
    if (globalIsMuted) return;
    const nowMs = typeof performance !== "undefined" ? performance.now() : Date.now();
    if (nowMs - lastHoverTimestamp < 32) return; // Prevent WebAudio node spikes during rapid cursor sweeps
    lastHoverTimestamp = nowMs;

    try {
      if (typeof navigator !== "undefined" && navigator.vibrate) {
        navigator.vibrate(5);
      }

      const ctx = getAudioContext();
      if (!ctx) return;
      const now = ctx.currentTime;

      // Primary crisp haptic click (high frequency glass/trackpad impulse)
      const osc1 = ctx.createOscillator();
      const gain1 = ctx.createGain();
      osc1.type = "sine";
      osc1.frequency.setValueAtTime(1600, now);
      osc1.frequency.exponentialRampToValueAtTime(2400, now + 0.025);

      gain1.gain.setValueAtTime(0.11, now);
      gain1.gain.exponentialRampToValueAtTime(0.0001, now + 0.028);

      osc1.connect(gain1);
      gain1.connect(ctx.destination);

      osc1.start(now);
      osc1.stop(now + 0.028);

      // Secondary tactile body impulse for physical weight
      const osc2 = ctx.createOscillator();
      const gain2 = ctx.createGain();
      osc2.type = "triangle";
      osc2.frequency.setValueAtTime(680, now);
      osc2.frequency.exponentialRampToValueAtTime(920, now + 0.035);

      gain2.gain.setValueAtTime(0.08, now);
      gain2.gain.exponentialRampToValueAtTime(0.0001, now + 0.035);

      osc2.connect(gain2);
      gain2.connect(ctx.destination);

      osc2.start(now);
      osc2.stop(now + 0.035);
    } catch {
      // AudioContext unavailable
    }
  }, [getAudioContext]);

  // Distinct, satisfying mechanical/glass tick for Apple-style dock magnification
  const playDockHoverSound = useCallback(() => {
    if (globalIsMuted) return;
    const nowMs = typeof performance !== "undefined" ? performance.now() : Date.now();
    if (nowMs - lastHoverTimestamp < 22) return;
    lastHoverTimestamp = nowMs;

    try {
      if (typeof navigator !== "undefined" && navigator.vibrate) {
        navigator.vibrate(8);
      }

      const ctx = getAudioContext();
      if (!ctx) return;
      const now = ctx.currentTime;

      // Ultra-crisp glass mechanical tick
      const osc1 = ctx.createOscillator();
      const gain1 = ctx.createGain();
      osc1.type = "sine";
      osc1.frequency.setValueAtTime(2100, now);
      osc1.frequency.exponentialRampToValueAtTime(3200, now + 0.022);

      gain1.gain.setValueAtTime(0.15, now);
      gain1.gain.exponentialRampToValueAtTime(0.0001, now + 0.024);

      osc1.connect(gain1);
      gain1.connect(ctx.destination);

      osc1.start(now);
      osc1.stop(now + 0.024);

      // Resonant body tick for physical weight
      const osc2 = ctx.createOscillator();
      const gain2 = ctx.createGain();
      osc2.type = "triangle";
      osc2.frequency.setValueAtTime(760, now);
      osc2.frequency.exponentialRampToValueAtTime(1120, now + 0.028);

      gain2.gain.setValueAtTime(0.10, now);
      gain2.gain.exponentialRampToValueAtTime(0.0001, now + 0.028);

      osc2.connect(gain2);
      gain2.connect(ctx.destination);

      osc2.start(now);
      osc2.stop(now + 0.028);
    } catch {
      // AudioContext unavailable
    }
  }, [getAudioContext]);

  // Satisfying confirmed action / focus chord
  const playFocusSound = useCallback(() => {
    if (globalIsMuted) return;
    try {
      const ctx = getAudioContext();
      if (!ctx) return;

      const now = ctx.currentTime;
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();

      osc.type = "sine";
      osc.frequency.setValueAtTime(440, now);
      osc.frequency.exponentialRampToValueAtTime(660, now + 0.09);

      gain.gain.setValueAtTime(0.12, now);
      gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.12);

      osc.connect(gain);
      gain.connect(ctx.destination);

      osc.start(now);
      osc.stop(now + 0.12);
    } catch {
      // AudioContext unavailable
    }
  }, [getAudioContext]);

  // Harmonic chord swell on prompt submission
  const playSubmitSound = useCallback(() => {
    if (globalIsMuted) return;
    try {
      const ctx = getAudioContext();
      if (!ctx) return;

      const now = ctx.currentTime;
      [440, 554.37, 659.25, 880].forEach((freq, idx) => {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();

        osc.type = "triangle";
        osc.frequency.setValueAtTime(freq, now + idx * 0.03);

        gain.gain.setValueAtTime(0.08, now + idx * 0.03);
        gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.45);

        osc.connect(gain);
        gain.connect(ctx.destination);

        osc.start(now + idx * 0.03);
        osc.stop(now + 0.45);
      });
    } catch {
      // AudioContext unavailable
    }
  }, [getAudioContext]);

  // Mechanical keyboard keypress haptic click with dual-harmonic presence and key-type tuning
  const playKeypressSound = useCallback((keyType?: "default" | "space" | "backspace" | "enter") => {
    if (globalIsMuted) return;
    try {
      if (typeof navigator !== "undefined" && navigator.vibrate) {
        navigator.vibrate(4);
      }

      const ctx = getAudioContext();
      if (!ctx) return;
      const now = ctx.currentTime;

      // Dynamic frequency tuning based on key type
      let baseHigh = 1950 + (Math.random() - 0.5) * 280;
      let baseLow = 440 + (Math.random() - 0.5) * 80;
      let highGain = 0.16;
      let lowGain = 0.12;

      if (keyType === "space" || keyType === "enter") {
        baseHigh = 1450 + (Math.random() - 0.5) * 150;
        baseLow = 320;
        highGain = 0.18;
        lowGain = 0.16;
      } else if (keyType === "backspace") {
        baseHigh = 2300 + (Math.random() - 0.5) * 200;
        baseLow = 520;
      }

      // 1. High-frequency crisp mechanical snap (transient attack)
      const osc1 = ctx.createOscillator();
      const gain1 = ctx.createGain();
      osc1.type = "sine";
      osc1.frequency.setValueAtTime(baseHigh, now);
      osc1.frequency.exponentialRampToValueAtTime(baseHigh * 0.45, now + 0.022);

      gain1.gain.setValueAtTime(highGain, now);
      gain1.gain.exponentialRampToValueAtTime(0.0001, now + 0.024);

      osc1.connect(gain1);
      gain1.connect(ctx.destination);

      osc1.start(now);
      osc1.stop(now + 0.024);

      // 2. Low-frequency tactile key bottom-out resonance
      const osc2 = ctx.createOscillator();
      const gain2 = ctx.createGain();
      osc2.type = "triangle";
      osc2.frequency.setValueAtTime(baseLow, now);
      osc2.frequency.exponentialRampToValueAtTime(baseLow * 0.6, now + 0.028);

      gain2.gain.setValueAtTime(lowGain, now);
      gain2.gain.exponentialRampToValueAtTime(0.0001, now + 0.03);

      osc2.connect(gain2);
      gain2.connect(ctx.destination);

      osc2.start(now);
      osc2.stop(now + 0.03);
    } catch {
      // AudioContext unavailable
    }
  }, [getAudioContext]);

  const toggleMute = useCallback(() => {
    globalIsMuted = !globalIsMuted;
    if (globalBgAudio) {
      if (globalIsMuted) {
        globalBgAudio.pause();
      } else {
        globalBgAudio.play().catch(() => {});
      }
    }
    notifyListeners();
  }, []);

  return {
    isMuted,
    toggleMute,
    playHoverSound,
    playDockHoverSound,
    playFocusSound,
    playSubmitSound,
    playKeypressSound,
  };
}
