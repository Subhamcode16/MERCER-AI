"use client";

import React, { useState } from "react";
import {
  Check,
  Sparkles,
  CreditCard,
  ArrowRight,
  Download,
  Calendar,
  ShieldCheck,
} from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";
import { useTactileAudio } from "@/components/dashboard/useTactileAudio";

export default function SubscriptionTab() {
  const { profile } = useAuth();
  const { playHoverSound, playFocusSound, playSubmitSound } = useTactileAudio();
  const [annualBilling, setAnnualBilling] = useState(true);

  const currentTier = profile?.tier || "FREE";

  return (
    <div className="space-y-10 font-sans pb-4">
      
      {/* 1. Current Plan Header & Cycle Renew Indicator */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 pb-7 border-b border-[#e3dfd4]">
        <div className="space-y-1">
          <div className="text-[10px] font-mono uppercase tracking-widest text-[#5e6d68] font-bold">
            01 // Active Institutional Tier
          </div>
          <h2 className="font-serif text-2xl sm:text-3xl text-[#0f1419] font-medium tracking-tight">
            {currentTier === "PRO" ? "Institutional Atelier Pro" : "Explorer Free Tier"}
          </h2>
          <p className="text-xs text-[#5e6d68] font-normal max-w-xl leading-relaxed">
            {currentTier === "PRO"
              ? "Full priority routing on Banarasi volumetric shaders, dedicated 1,000 monthly credits, and commercial copyright ledger."
              : "Standard tier with 100 monthly credits. Upgrade to unlock sub-second inference and full commercial license."}
          </p>
        </div>

        <div className="flex flex-col sm:flex-row items-start sm:items-center gap-3">
          <div className="flex items-center gap-2 text-xs font-mono text-[#5e6d68] bg-[#faf8f4] px-3 py-1.5 rounded-lg border border-[#e3dfd4]">
            <Calendar size={12} />
            <span>Renews: <strong className="text-[#0f1419]">Aug 1, 2026</strong></span>
          </div>

          {currentTier === "PRO" ? (
            <button
              type="button"
              onClick={playFocusSound}
              onMouseEnter={playHoverSound}
              className="px-3.5 py-1.5 rounded-lg text-xs font-semibold text-[#0f1419] hover:bg-[#f0ebe1] border border-[#e3dfd4] transition-all font-sans"
            >
              Manage Invoices
            </button>
          ) : (
            <button
              type="button"
              onClick={playSubmitSound}
              onMouseEnter={playHoverSound}
              className="bg-[#1e3a34] hover:bg-[#142824] text-white text-xs font-semibold px-4 py-1.5 rounded-lg shadow-xs transition-all active:scale-[0.98] flex items-center gap-1.5 font-sans"
            >
              <span>Upgrade Tier</span>
              <ArrowRight size={13} />
            </button>
          )}
        </div>
      </div>

      {/* 2. Billing Interval Selector */}
      <div className="flex justify-center -my-2">
        <div className="inline-flex items-center gap-1 p-1 bg-[#f0ebe1] rounded-xl border border-[#e3dfd4]">
          <button
            type="button"
            onClick={() => {
              playFocusSound();
              setAnnualBilling(false);
            }}
            onMouseEnter={playHoverSound}
            className={`px-3.5 py-1 rounded-lg text-xs font-semibold transition-all font-sans ${
              !annualBilling
                ? "bg-white text-[#0f1419] shadow-2xs border border-[#e3dfd4]"
                : "text-[#5e6d68] hover:text-[#0f1419]"
            }`}
          >
            Monthly Cadence
          </button>
          <button
            type="button"
            onClick={() => {
              playFocusSound();
              setAnnualBilling(true);
            }}
            onMouseEnter={playHoverSound}
            className={`px-3.5 py-1 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5 font-sans ${
              annualBilling
                ? "bg-white text-[#0f1419] shadow-2xs border border-[#e3dfd4]"
                : "text-[#5e6d68] hover:text-[#0f1419]"
            }`}
          >
            <span>Annual Cadence</span>
            <span className="px-1.5 py-0.2 rounded font-mono text-[9px] font-bold bg-[#faf8f4] text-[#059669] border border-[#e3dfd4]">
              Save 20%
            </span>
          </button>
        </div>
      </div>

      {/* 3. Dual Tier Matrix (Architectural Cards) */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-stretch">
        {/* Explorer Free Tier */}
        <div
          className={`p-6 rounded-2xl flex flex-col justify-between transition-all border ${
            currentTier === "FREE"
              ? "bg-[#faf8f4] border-[#e3dfd4]"
              : "bg-white border-[#e3dfd4] opacity-80"
          }`}
        >
          <div className="space-y-4">
            <div className="flex justify-between items-start">
              <div>
                <span className="text-[10px] font-mono uppercase tracking-widest text-[#5e6d68] font-bold">
                  Community Tier
                </span>
                <h3 className="text-xl font-serif text-[#0f1419] font-medium mt-0.5">
                  Explorer Seat
                </h3>
              </div>
              {currentTier === "FREE" && (
                <span className="text-[10px] font-mono uppercase tracking-wider px-2 py-0.5 rounded bg-white text-[#0f1419] border border-[#e3dfd4] font-bold">
                  Current
                </span>
              )}
            </div>

            <div className="flex items-baseline gap-1">
              <span className="font-serif text-3xl sm:text-4xl text-[#0f1419] font-medium">$0</span>
              <span className="text-xs text-[#5e6d68] font-mono">/ forever</span>
            </div>

            <ul className="space-y-2.5 pt-2 text-xs text-[#0f1419]">
              <li className="flex items-center gap-2.5">
                <Check size={13} className="text-[#059669] shrink-0" />
                <span>100 compute units per month</span>
              </li>
              <li className="flex items-center gap-2.5">
                <Check size={13} className="text-[#059669] shrink-0" />
                <span>Standard generation latency</span>
              </li>
              <li className="flex items-center gap-2.5">
                <Check size={13} className="text-[#059669] shrink-0" />
                <span>Public model checkpoint routing</span>
              </li>
              <li className="flex items-center gap-2.5 text-[#5e6d68]">
                <span className="text-[11px] font-mono">×</span>
                <span className="line-through">Sub-second prioritized GPU clusters</span>
              </li>
            </ul>
          </div>
        </div>

        {/* Atelier Pro Tier */}
        <div className="relative p-6 rounded-2xl bg-white border-2 border-[#1e3a34] shadow-xs flex flex-col justify-between">
          <div className="absolute -top-2.5 right-5 bg-[#1e3a34] text-white text-[9px] font-mono uppercase tracking-widest font-bold px-2.5 py-0.5 rounded-full">
            Institutional Standard
          </div>

          <div className="space-y-4">
            <div className="flex justify-between items-start">
              <div>
                <span className="text-[10px] font-mono uppercase tracking-widest text-[#059669] font-bold">
                  Director Suite
                </span>
                <h3 className="text-xl font-serif text-[#0f1419] font-medium mt-0.5">
                  Atelier Pro
                </h3>
              </div>
              {currentTier === "PRO" && (
                <span className="text-[10px] font-mono uppercase tracking-wider px-2 py-0.5 rounded bg-[#1e3a34] text-white font-bold">
                  Active
                </span>
              )}
            </div>

            <div className="flex items-baseline gap-1">
              <span className="font-serif text-3xl sm:text-4xl text-[#0f1419] font-medium">
                {annualBilling ? "$149" : "$189"}
              </span>
              <span className="text-xs text-[#5e6d68] font-mono">
                / seat billed {annualBilling ? "annually" : "monthly"}
              </span>
            </div>

            <ul className="space-y-2.5 pt-2 text-xs text-[#0f1419]">
              <li className="flex items-center gap-2.5">
                <Check size={13} className="text-[#059669] shrink-0" />
                <span className="font-semibold">1,000 monthly inference credits</span>
              </li>
              <li className="flex items-center gap-2.5">
                <Check size={13} className="text-[#059669] shrink-0" />
                <span>Zero-wait GPU cluster routing (US-East)</span>
              </li>
              <li className="flex items-center gap-2.5">
                <Check size={13} className="text-[#059669] shrink-0" />
                <span>Banarasi silk volumetric physics shaders</span>
              </li>
              <li className="flex items-center gap-2.5">
                <Check size={13} className="text-[#059669] shrink-0" />
                <span>Full commercial license &amp; cryptographic audit trail</span>
              </li>
            </ul>
          </div>

          <div className="pt-5">
            <button
              type="button"
              onClick={playSubmitSound}
              onMouseEnter={playHoverSound}
              className="w-full py-2.5 rounded-xl bg-[#1e3a34] hover:bg-[#142824] text-white text-xs font-semibold tracking-wide uppercase transition-all shadow-xs active:scale-[0.98] font-sans"
            >
              {currentTier === "PRO" ? "Current Active Seat" : "Upgrade to Pro"}
            </button>
          </div>
        </div>
      </div>

      {/* 4. Payment Credentials Strip */}
      <div className="p-4 rounded-xl bg-[#faf8f4] border border-[#e3dfd4] flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-lg bg-white border border-[#e3dfd4] flex items-center justify-center text-[#0f1419] shrink-0">
            <CreditCard size={16} />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-semibold text-[#0f1419] font-sans">
                Mastercard ending in 4242
              </span>
              <span className="text-[9px] font-mono uppercase bg-white border border-[#e3dfd4] px-1.5 py-0.2 rounded text-[#059669] font-bold">
                Default
              </span>
            </div>
            <p className="text-[11px] text-[#5e6d68] font-mono">
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
          <Download size={12} />
          <span>Download Invoice PDF</span>
        </button>
      </div>

    </div>
  );
}
