"use client";

import React, { useState } from "react";
import {
  Check,
  Sparkles,
  CreditCard,
  ArrowRight,
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
    <div className="space-y-8 font-sans">
      {/* Current Plan Overview Row */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 pb-6 border-b border-[#e3dfd4]">
        <div className="space-y-1.5">
          <div className="inline-flex items-center gap-2 px-2.5 py-0.5 rounded-full bg-[#f0ebe1] text-[#0f1419] text-[10px] font-mono uppercase tracking-widest font-bold border border-[#e3dfd4]">
            <Sparkles size={11} className="text-[#059669]" />
            Active Membership
          </div>
          <h2 className="font-serif text-2xl sm:text-3xl text-[#0f1419] font-medium tracking-tight">
            {currentTier === "PRO" ? "Institutional Atelier Pro" : "Explorer Free Tier"}
          </h2>
          <p className="text-xs sm:text-sm text-[#5e6d68] font-normal max-w-lg leading-relaxed font-sans">
            {currentTier === "PRO"
              ? "Full access to high-priority generative pipelines, custom Banarasi fabric shaders, and 1,000 monthly credits."
              : "Standard tier with 100 monthly credits. Upgrade to unlock sub-second inference and full commercial licensing."}
          </p>
        </div>

        <div className="flex flex-col items-start md:items-end gap-3 self-start md:self-center">
          <div className="flex items-center gap-2 text-xs font-mono text-[#5e6d68] bg-[#f8f6f0] px-3 py-1.5 rounded-xl border border-[#e3dfd4]">
            <Calendar size={13} />
            Cycle Renews: <strong className="text-[#0f1419]">Aug 1st, 2026</strong>
          </div>

          {currentTier !== "PRO" ? (
            <button
              type="button"
              onClick={playSubmitSound}
              onMouseEnter={playHoverSound}
              className="bg-[#1e3a34] text-white hover:bg-[#284c44] text-xs sm:text-sm font-semibold px-5 py-2.5 rounded-xl shadow-xs transition-all active:scale-[0.98] flex items-center gap-2 font-sans"
            >
              Upgrade to Atelier Pro
              <ArrowRight size={14} />
            </button>
          ) : (
            <button
              type="button"
              onClick={playFocusSound}
              onMouseEnter={playHoverSound}
              className="bg-[#f0ebe1] hover:bg-[#f8f6f0] text-[#0f1419] text-xs font-semibold px-4 py-2 rounded-xl border border-[#e3dfd4] transition-all font-sans"
            >
              Manage Billing &amp; Invoices
            </button>
          )}
        </div>
      </div>

      {/* Interval Switcher (Monthly vs Annual) */}
      <div className="flex justify-center my-1">
        <div className="inline-flex items-center gap-1.5 p-1 rounded-2xl bg-[#f8f6f0] border border-[#e3dfd4] shadow-2xs">
          <button
            type="button"
            onClick={() => {
              playFocusSound();
              setAnnualBilling(false);
            }}
            className={`px-3.5 py-1.5 rounded-xl text-xs font-semibold transition-all font-sans ${
              !annualBilling
                ? "bg-white text-[#0f1419] shadow-xs border border-[#e3dfd4]"
                : "text-[#5e6d68] hover:text-[#0f1419]"
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
            className={`px-3.5 py-1.5 rounded-xl text-xs font-semibold transition-all flex items-center gap-1.5 font-sans ${
              annualBilling
                ? "bg-white text-[#0f1419] shadow-xs border border-[#e3dfd4]"
                : "text-[#5e6d68] hover:text-[#0f1419]"
            }`}
          >
            Annual Billing
            <span className="px-1.5 py-0.5 rounded-full bg-[#f0ebe1] text-[#059669] text-[10px] font-mono font-bold">
              Save 20%
            </span>
          </button>
        </div>
      </div>

      {/* Dual Plan Cards Matrix */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-stretch">
        {/* Tier 1: Explorer Free */}
        <div
          className={`p-6 sm:p-7 rounded-2xl flex flex-col justify-between transition-all ${
            currentTier === "FREE"
              ? "bg-[#f8f6f0] border-2 border-[#e3dfd4]"
              : "bg-[#f8f6f0]/60 border border-[#e3dfd4] opacity-80"
          }`}
        >
          <div className="space-y-4">
            <div className="flex justify-between items-start">
              <div>
                <span className="text-[10px] font-mono uppercase tracking-widest text-[#5e6d68] font-bold">
                  Free Tier
                </span>
                <h3 className="text-xl font-serif text-[#0f1419] font-medium mt-1">
                  Explorer
                </h3>
              </div>
              {currentTier === "FREE" && (
                <span className="text-[10px] font-mono uppercase tracking-wider px-2.5 py-0.5 rounded-full bg-white text-[#0f1419] border border-[#e3dfd4] font-bold">
                  Current
                </span>
              )}
            </div>

            <div className="flex items-baseline gap-1">
              <span className="font-serif text-4xl text-[#0f1419] font-semibold">$0</span>
              <span className="text-xs text-[#5e6d68] font-sans">/ month forever</span>
            </div>

            <ul className="space-y-2.5 pt-2 text-xs text-[#0f1419]">
              <li className="flex items-center gap-2.5">
                <Check size={14} className="text-[#059669] shrink-0" />
                <span>100 compute units / month</span>
              </li>
              <li className="flex items-center gap-2.5">
                <Check size={14} className="text-[#059669] shrink-0" />
                <span>Standard generation latency</span>
              </li>
              <li className="flex items-center gap-2.5">
                <Check size={14} className="text-[#059669] shrink-0" />
                <span>Public model weights access</span>
              </li>
              <li className="flex items-center gap-2.5 text-[#5e6d68]">
                <span className="w-3.5 h-3.5 rounded-full border border-[#e3dfd4] flex items-center justify-center text-[9px] shrink-0">
                  ×
                </span>
                <span className="line-through">Sub-second priority queues</span>
              </li>
            </ul>
          </div>
        </div>

        {/* Tier 2: Atelier Pro */}
        <div className="relative p-6 sm:p-7 rounded-2xl bg-white border-2 border-[#1e3a34] shadow-md flex flex-col justify-between">
          <div className="absolute -top-3 right-6 bg-[#1e3a34] text-white text-[10px] font-mono uppercase tracking-widest font-bold px-3 py-1 rounded-full shadow-xs">
            Institutional Standard
          </div>

          <div className="space-y-4">
            <div className="flex justify-between items-start">
              <div>
                <span className="text-[10px] font-mono uppercase tracking-widest text-[#059669] font-bold">
                  Professional Suite
                </span>
                <h3 className="text-xl font-serif text-[#0f1419] font-medium mt-1">
                  Atelier Pro
                </h3>
              </div>
              {currentTier === "PRO" && (
                <span className="text-[10px] font-mono uppercase tracking-wider px-2.5 py-0.5 rounded-full bg-[#1e3a34] text-white font-bold">
                  Active
                </span>
              )}
            </div>

            <div className="flex items-baseline gap-1">
              <span className="font-serif text-4xl text-[#0f1419] font-bold">
                {annualBilling ? "$149" : "$189"}
              </span>
              <span className="text-xs text-[#5e6d68] font-sans">
                / seat billed {annualBilling ? "annually" : "monthly"}
              </span>
            </div>

            <ul className="space-y-2.5 pt-2 text-xs text-[#0f1419]">
              <li className="flex items-center gap-2.5">
                <Check size={14} className="text-[#059669] shrink-0" />
                <span className="font-semibold">1,000 compute credits monthly</span>
              </li>
              <li className="flex items-center gap-2.5">
                <Check size={14} className="text-[#059669] shrink-0" />
                <span>Zero-queue prioritized GPU cluster routing</span>
              </li>
              <li className="flex items-center gap-2.5">
                <Check size={14} className="text-[#059669] shrink-0" />
                <span>Custom fabric physics &amp; volumetric shaders</span>
              </li>
              <li className="flex items-center gap-2.5">
                <Check size={14} className="text-[#059669] shrink-0" />
                <span>Full commercial license &amp; copyright ledger</span>
              </li>
            </ul>
          </div>

          <div className="pt-6">
            <button
              type="button"
              onClick={playSubmitSound}
              onMouseEnter={playHoverSound}
              className="w-full py-3 rounded-xl bg-[#1e3a34] hover:bg-[#284c44] text-white text-xs font-bold tracking-wider uppercase transition-all shadow-xs active:scale-[0.98] font-sans"
            >
              {currentTier === "PRO" ? "Current Active Plan" : "Upgrade Plan Now"}
            </button>
          </div>
        </div>
      </div>

      {/* Payment Method & Encrypted Ledger Chip */}
      <div className="rounded-xl bg-[#f8f6f0] border border-[#e3dfd4] p-4 sm:p-5 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="flex items-center gap-3.5">
          <div className="w-10 h-10 rounded-xl bg-white border border-[#e3dfd4] flex items-center justify-center text-[#0f1419] shadow-xs">
            <CreditCard size={18} />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs sm:text-sm font-semibold text-[#0f1419] font-sans">
                Mastercard ending in 4242
              </span>
              <span className="text-[10px] font-mono uppercase bg-[#f0ebe1] px-2 py-0.5 rounded text-[#059669] font-bold">
                Default
              </span>
            </div>
            <p className="text-xs text-[#5e6d68] font-normal font-sans">
              Expires 09/2028 · 256-bit TLS Encrypted
            </p>
          </div>
        </div>

        <button
          type="button"
          onClick={playFocusSound}
          onMouseEnter={playHoverSound}
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-[#0f1419] hover:underline font-sans"
        >
          <Download size={13} />
          Download Last Invoice
        </button>
      </div>
    </div>
  );
}
