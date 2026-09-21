"use client";

import React, { useState } from "react";
import {
  Check,
  Sparkles,
  CreditCard,
  ArrowRight,
  ShieldCheck,
  Zap,
  Award,
  Download,
  Calendar,
} from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";
import { useTactileAudio } from "@/components/dashboard/useTactileAudio";

export default function SubscriptionTab() {
  const { profile } = useAuth();
  const { playHoverSound, playFocusSound, playSubmitSound } = useTactileAudio();
  const [annualBilling, setAnnualBilling] = useState(true);

  const currentTier = profile?.tier || "FREE";

  return (
    <div className="space-y-8">
      {/* Current Plan Overview Banner */}
      <div className="rounded-3xl bg-white/70 backdrop-blur-2xl border border-white/80 p-6 sm:p-8 shadow-[0_20px_50px_rgba(0,0,0,0.06),inset_0_1.5px_2px_rgba(255,255,255,0.95)] relative overflow-hidden">
        {/* Subtle ambient light gradient */}
        <div className="absolute top-0 right-0 w-80 h-80 bg-gradient-to-bl from-amber-200/30 via-emerald-200/20 to-transparent rounded-full blur-3xl pointer-events-none" />

        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 relative z-10">
          <div className="space-y-2">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900 text-white text-[10px] font-mono uppercase tracking-widest font-bold shadow-xs">
              <Sparkles size={11} className="text-amber-300" />
              Active Membership
            </div>
            <h2 className="font-serif text-3xl sm:text-4xl text-[#0f172a] font-medium tracking-tight">
              {currentTier === "PRO" ? "Institutional Atelier Pro" : "Explorer Free Tier"}
            </h2>
            <p className="text-xs sm:text-sm text-slate-600 font-light max-w-lg leading-relaxed">
              {currentTier === "PRO"
                ? "Full access to high-priority generative pipelines, custom Banarasi fabric shaders, and 1,000 monthly credits."
                : "Standard tier with 100 monthly credits. Upgrade to unlock sub-second inference and full commercial licensing."}
            </p>
          </div>

          <div className="flex flex-col items-start md:items-end gap-3 self-start md:self-center">
            <div className="flex items-center gap-2 text-xs font-mono text-slate-600 bg-white/70 px-3 py-1.5 rounded-xl border border-slate-200">
              <Calendar size={13} className="text-slate-500" />
              Cycle Renews: <strong>Aug 1st, 2026</strong>
            </div>

            {currentTier !== "PRO" ? (
              <button
                type="button"
                onClick={playSubmitSound}
                onMouseEnter={playHoverSound}
                className="bg-[#0f172a] hover:bg-[#1e293b] text-white text-xs sm:text-sm font-semibold px-6 py-3 rounded-xl shadow-[0_4px_16px_rgba(15,23,42,0.2)] transition-all active:scale-[0.98] flex items-center gap-2"
              >
                Upgrade to Atelier Pro
                <ArrowRight size={14} className="text-amber-300" />
              </button>
            ) : (
              <button
                type="button"
                onClick={playFocusSound}
                onMouseEnter={playHoverSound}
                className="bg-white hover:bg-slate-50 text-[#0f172a] text-xs font-semibold px-5 py-2.5 rounded-xl border border-slate-200 shadow-xs transition-all"
              >
                Manage Billing Portal
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Interval Switcher (Monthly vs Annual) */}
      <div className="flex justify-center my-2">
        <div className="inline-flex items-center gap-2 p-1.5 rounded-2xl bg-white/60 backdrop-blur-md border border-white/90 shadow-xs">
          <button
            type="button"
            onClick={() => {
              playFocusSound();
              setAnnualBilling(false);
            }}
            className={`px-4 py-1.5 rounded-xl text-xs font-semibold transition-all ${
              !annualBilling
                ? "bg-[#0f172a] text-white shadow-xs"
                : "text-slate-600 hover:text-slate-900"
            }`}
          >
            Monthly Billing
          </button>
          <button
            type="button"
            onClick={() => {
              playFocusSound();
              setAnnualBilling(true);
            }}
            className={`px-4 py-1.5 rounded-xl text-xs font-semibold transition-all flex items-center gap-1.5 ${
              annualBilling
                ? "bg-[#0f172a] text-white shadow-xs"
                : "text-slate-600 hover:text-slate-900"
            }`}
          >
            Annual Billing
            <span className="px-1.5 py-0.2 rounded-full bg-emerald-100 text-emerald-800 text-[10px] font-mono font-bold">
              Save 20%
            </span>
          </button>
        </div>
      </div>

      {/* Tier Comparison Matrix */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-stretch">
        {/* Explorer Free Plan */}
        <div
          className={`rounded-3xl p-6 sm:p-8 flex flex-col justify-between transition-all duration-300 ${
            currentTier === "FREE"
              ? "bg-white/75 backdrop-blur-2xl border-2 border-slate-300 shadow-[0_20px_50px_rgba(0,0,0,0.05)]"
              : "bg-white/50 backdrop-blur-xl border border-white/80 opacity-75"
          }`}
        >
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <span className="text-xs font-mono uppercase tracking-widest text-slate-500 font-bold">
                Explorer
              </span>
              {currentTier === "FREE" && (
                <span className="text-[10px] font-mono font-bold uppercase tracking-wider bg-slate-100 text-slate-700 px-2.5 py-0.5 rounded-full border border-slate-200">
                  Current Plan
                </span>
              )}
            </div>

            <div>
              <h3 className="font-serif text-2xl text-[#0f172a] font-medium">Free Access</h3>
              <div className="flex items-baseline gap-1 mt-2">
                <span className="font-serif text-4xl text-[#0f172a] font-normal">$0</span>
                <span className="text-xs font-mono text-slate-500">/ month forever</span>
              </div>
            </div>

            <div className="h-[1px] w-full bg-slate-200/80" />

            <ul className="space-y-3.5 text-xs text-slate-600">
              {[
                "100 Compute credits per cycle",
                "Standard speed generation queue",
                "Access to base foundation models",
                "Community governance & Discord support",
                "Standard 1080p asset export",
              ].map((feature, i) => (
                <li key={i} className="flex items-center gap-2.5">
                  <div className="w-4 h-4 rounded-full bg-slate-100 text-slate-700 flex items-center justify-center shrink-0">
                    <Check size={11} />
                  </div>
                  <span>{feature}</span>
                </li>
              ))}
            </ul>
          </div>

          <div className="pt-8">
            <button
              type="button"
              disabled={currentTier === "FREE"}
              className="w-full py-3 rounded-xl border border-slate-300 text-slate-600 text-xs font-semibold bg-white/60 hover:bg-white cursor-default disabled:opacity-60 transition-all"
            >
              {currentTier === "FREE" ? "Active Tier" : "Downgrade to Free"}
            </button>
          </div>
        </div>

        {/* Institutional Atelier Pro Plan */}
        <div className="rounded-3xl p-6 sm:p-8 flex flex-col justify-between relative overflow-hidden bg-white/90 backdrop-blur-2xl border-2 border-slate-900 shadow-[0_25px_60px_rgba(15,23,42,0.12)]">
          {/* Accent top gradient bar */}
          <div className="absolute top-0 inset-x-0 h-1 bg-gradient-to-r from-amber-400 via-emerald-500 to-teal-500" />

          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <span className="text-xs font-mono uppercase tracking-widest text-slate-800 font-bold">
                Atelier Pro
              </span>
              <span className="inline-flex items-center gap-1 text-[10px] font-mono font-bold uppercase tracking-wider bg-slate-900 text-amber-300 px-2.5 py-0.5 rounded-full shadow-xs">
                <Sparkles size={10} />
                Institutional Standard
              </span>
            </div>

            <div>
              <h3 className="font-serif text-2xl text-[#0f172a] font-medium">Professional Creative Suite</h3>
              <div className="flex items-baseline gap-1 mt-2">
                <span className="font-serif text-4xl text-[#0f172a] font-normal">
                  {annualBilling ? "$24" : "$29"}
                </span>
                <span className="text-xs font-mono text-slate-500">/ month billed annually</span>
              </div>
            </div>

            <div className="h-[1px] w-full bg-slate-200/80" />

            <ul className="space-y-3.5 text-xs text-[#0f172a] font-medium">
              {[
                "1,000 High-performance compute credits / mo",
                "Dedicated sub-second GPU inference pipeline",
                "Full Banarasi Drape Shaders & Lighting Engines",
                "Zero data retention & cryptographic privacy vault",
                "Ultra-HD 4K Lookbook exports & vector packages",
                "Unrestricted commercial usage & brand license",
                "Direct Slack bridge with engineering team",
              ].map((feature, i) => (
                <li key={i} className="flex items-center gap-2.5">
                  <div className="w-4 h-4 rounded-full bg-emerald-100 text-emerald-800 flex items-center justify-center shrink-0">
                    <Check size={11} />
                  </div>
                  <span>{feature}</span>
                </li>
              ))}
            </ul>
          </div>

          <div className="pt-8">
            <button
              type="button"
              onClick={playSubmitSound}
              onMouseEnter={playHoverSound}
              className="w-full py-3.5 rounded-xl bg-[#0f172a] hover:bg-[#1e293b] text-white text-xs sm:text-sm font-semibold shadow-[0_4px_18px_rgba(15,23,42,0.25)] transition-all active:scale-[0.98] flex items-center justify-center gap-2"
            >
              {currentTier === "PRO" ? "Current Pro Subscription" : "Upgrade to Atelier Pro"}
              <ArrowRight size={14} className="text-amber-300" />
            </button>
          </div>
        </div>
      </div>

      {/* Payment Method & Security Card */}
      <div className="rounded-3xl bg-white/70 backdrop-blur-2xl border border-white/80 p-6 shadow-xs flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="flex items-center gap-4">
          <div className="w-12 h-9 rounded-xl bg-slate-900 text-white flex items-center justify-center shadow-xs">
            <CreditCard size={18} />
          </div>
          <div>
            <p className="text-xs sm:text-sm font-semibold text-[#0f172a]">
              Mastercard ending in <span className="font-mono">4242</span>
            </p>
            <p className="text-[11px] text-slate-500 font-mono">
              Expires 12/28 • Secure 256-Bit Vault
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3 self-end sm:self-center">
          <button
            type="button"
            onClick={playFocusSound}
            onMouseEnter={playHoverSound}
            className="px-4 py-2 rounded-xl text-xs font-semibold bg-white border border-slate-200 text-slate-700 hover:text-slate-900 hover:border-slate-300 shadow-2xs transition-all"
          >
            Update Card
          </button>
          <button
            type="button"
            onClick={playFocusSound}
            onMouseEnter={playHoverSound}
            className="px-4 py-2 rounded-xl text-xs font-semibold bg-white border border-slate-200 text-slate-700 hover:text-slate-900 hover:border-slate-300 shadow-2xs transition-all flex items-center gap-1.5"
          >
            <Download size={13} />
            Invoices
          </button>
        </div>
      </div>
    </div>
  );
}
