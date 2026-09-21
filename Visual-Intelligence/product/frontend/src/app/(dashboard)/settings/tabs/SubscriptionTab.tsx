"use client";

import React, { useState } from "react";
import {
  Check,
  CreditCard,
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
    <div className="space-y-6 font-sans">
      
      {/* Current Plan Banner */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-6 border-b border-[var(--line)]">
        <div className="space-y-1">
          <span className="text-xs font-semibold uppercase tracking-wider text-[var(--muted)] font-mono">
            Current Subscription Plan
          </span>
          <h2 className="font-serif text-2xl text-[var(--ink)] font-medium">
            {currentTier === "PRO" ? "Atelier Pro Plan" : "Explorer Free Plan"}
          </h2>
          <p className="text-xs text-[var(--muted)]">
            {currentTier === "PRO"
              ? "1,000 monthly credits with high-priority generative pipelines."
              : "100 monthly credits. Upgrade to unlock prioritized inference."}
          </p>
        </div>

        <div className="flex items-center gap-2 text-xs font-mono text-[var(--muted)] bg-[var(--soft)] px-3 py-1.5 rounded-lg border border-[var(--line)]">
          <Calendar size={12} />
          <span>Renews: <strong className="text-[var(--ink)]">Aug 1, 2026</strong></span>
        </div>
      </div>

      {/* Cadence Toggle - Clean centered pill with proper spacing */}
      <div className="flex justify-center pt-2 pb-2">
        <div className="inline-flex items-center gap-1 p-1 bg-[var(--soft)] rounded-xl border border-[var(--line)]">
          <button
            type="button"
            onClick={() => {
              playFocusSound();
              setAnnualBilling(false);
            }}
            onMouseEnter={playHoverSound}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              !annualBilling
                ? "bg-[var(--surface)] text-[var(--ink)] shadow-2xs border border-[var(--line)]"
                : "text-[var(--muted)] hover:text-[var(--ink)]"
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
            onMouseEnter={playHoverSound}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5 ${
              annualBilling
                ? "bg-[var(--surface)] text-[var(--ink)] shadow-2xs border border-[var(--line)]"
                : "text-[var(--muted)] hover:text-[var(--ink)]"
            }`}
          >
            <span>Annual Billing</span>
            <span className="px-1.5 py-0.5 rounded font-mono text-[9px] font-bold bg-[var(--paper)] text-emerald-500 border border-[var(--line)]">
              Save 20%
            </span>
          </button>
        </div>
      </div>

      {/* Plans Comparison Matrix - Proportioned Equal Height Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-5 items-stretch">
        {/* Free Plan */}
        <div className="p-6 rounded-2xl bg-[var(--soft)] border border-[var(--line)] flex flex-col justify-between space-y-6">
          <div className="space-y-4">
            <div className="flex justify-between items-start">
              <div>
                <span className="text-[10px] font-mono uppercase tracking-widest text-[var(--muted)] font-bold">
                  Free
                </span>
                <h3 className="text-xl font-serif text-[var(--ink)] font-medium mt-0.5">
                  Explorer
                </h3>
              </div>
              {currentTier === "FREE" && (
                <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-[var(--surface)] text-[var(--ink)] border border-[var(--line)] font-bold">
                  Current
                </span>
              )}
            </div>

            <div className="font-serif text-3xl sm:text-4xl text-[var(--ink)] font-medium">
              $0 <span className="text-xs text-[var(--muted)] font-sans font-normal">/ month</span>
            </div>

            <ul className="space-y-2.5 text-xs text-[var(--ink)]">
              <li className="flex items-center gap-2">
                <Check size={13} className="text-emerald-500 shrink-0" />
                <span>100 compute credits monthly</span>
              </li>
              <li className="flex items-center gap-2">
                <Check size={13} className="text-emerald-500 shrink-0" />
                <span>Standard generation pipeline</span>
              </li>
              <li className="flex items-center gap-2 text-[var(--muted)]">
                <span className="text-[11px] font-mono">×</span>
                <span className="line-through">High-priority generation</span>
              </li>
            </ul>
          </div>

          <div className="pt-2">
            <div className="w-full py-2.5 rounded-xl bg-[var(--surface)]/80 border border-[var(--line)] text-center text-xs font-semibold text-[var(--muted)] uppercase tracking-wider">
              {currentTier === "FREE" ? "Active Free Plan" : "Included"}
            </div>
          </div>
        </div>

        {/* Pro Plan */}
        <div className="p-6 rounded-2xl bg-[var(--surface)] border-2 border-[var(--accent)] shadow-xs flex flex-col justify-between space-y-6 relative">
          <div className="space-y-4">
            <div className="flex justify-between items-start">
              <div>
                <span className="text-[10px] font-mono uppercase tracking-widest text-emerald-500 font-bold">
                  Pro
                </span>
                <h3 className="text-xl font-serif text-[var(--ink)] font-medium mt-0.5">
                  Atelier Pro
                </h3>
              </div>
              {currentTier === "PRO" ? (
                <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-[var(--accent)] text-[var(--accent-ink)] font-bold">
                  Active
                </span>
              ) : (
                <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-[var(--accent)] text-[var(--accent-ink)] font-bold">
                  Recommended
                </span>
              )}
            </div>

            <div className="font-serif text-3xl sm:text-4xl text-[var(--ink)] font-medium">
              {annualBilling ? "$149" : "$189"}{" "}
              <span className="text-xs text-[var(--muted)] font-sans font-normal">
                / month billed {annualBilling ? "annually" : "monthly"}
              </span>
            </div>

            <ul className="space-y-2.5 text-xs text-[var(--ink)]">
              <li className="flex items-center gap-2">
                <Check size={13} className="text-emerald-500 shrink-0" />
                <span className="font-semibold">1,000 compute credits monthly</span>
              </li>
              <li className="flex items-center gap-2">
                <Check size={13} className="text-emerald-500 shrink-0" />
                <span>Zero-wait prioritized inference</span>
              </li>
              <li className="flex items-center gap-2">
                <Check size={13} className="text-emerald-500 shrink-0" />
                <span>Full commercial license</span>
              </li>
            </ul>
          </div>

          <div className="pt-2">
            <button
              type="button"
              onClick={playSubmitSound}
              onMouseEnter={playHoverSound}
              className="w-full py-2.5 rounded-xl bg-[var(--accent)] hover:opacity-90 text-[var(--accent-ink)] text-xs font-semibold uppercase tracking-wider transition-all shadow-xs active:scale-[0.98]"
            >
              {currentTier === "PRO" ? "Current Active Plan" : "Upgrade to Pro"}
            </button>
          </div>
        </div>
      </div>

      {/* Payment Information */}
      <div className="p-4 rounded-xl bg-[var(--soft)] border border-[var(--line)] flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mt-6">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-[var(--surface)] border border-[var(--line)] flex items-center justify-center text-[var(--ink)]">
            <CreditCard size={15} />
          </div>
          <div>
            <div className="text-xs font-semibold text-[var(--ink)]">
              Mastercard ending in 4242
            </div>
            <div className="text-[11px] text-[var(--muted)]">
              Expires 09/2028 · 256-bit TLS Encrypted
            </div>
          </div>
        </div>

        <button
          type="button"
          onClick={playFocusSound}
          onMouseEnter={playHoverSound}
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-[var(--ink)] hover:text-[var(--accent)]"
        >
          <Download size={12} />
          <span>Download Invoices</span>
        </button>
      </div>

    </div>
  );
}
