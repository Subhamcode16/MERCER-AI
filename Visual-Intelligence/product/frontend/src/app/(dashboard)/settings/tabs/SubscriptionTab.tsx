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
    <div className="space-y-8">
      {/* Current Plan Overview Row */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 pb-6 border-b border-[var(--line)]">
        <div className="space-y-1.5">
          <div className="inline-flex items-center gap-2 px-2.5 py-0.5 rounded-full bg-[var(--soft)] text-[var(--ink)] text-[10px] font-mono uppercase tracking-widest font-bold border border-[var(--line)]">
            <Sparkles size={11} className="text-[var(--activity)]" />
            Active Membership
          </div>
          <h2 className="font-serif text-2xl sm:text-3xl text-[var(--ink)] font-medium tracking-tight">
            {currentTier === "PRO" ? "Institutional Atelier Pro" : "Explorer Free Tier"}
          </h2>
          <p className="text-xs sm:text-sm text-[var(--muted)] font-light max-w-lg leading-relaxed">
            {currentTier === "PRO"
              ? "Full access to high-priority generative pipelines, custom Banarasi fabric shaders, and 1,000 monthly credits."
              : "Standard tier with 100 monthly credits. Upgrade to unlock sub-second inference and full commercial licensing."}
          </p>
        </div>

        <div className="flex flex-col items-start md:items-end gap-3 self-start md:self-center">
          <div className="flex items-center gap-2 text-xs font-mono text-[var(--muted)] bg-[var(--paper)] px-3 py-1.5 rounded-xl border border-[var(--line)]">
            <Calendar size={13} />
            Cycle Renews: <strong className="text-[var(--ink)]">Aug 1st, 2026</strong>
          </div>

          {currentTier !== "PRO" ? (
            <button
              type="button"
              onClick={playSubmitSound}
              onMouseEnter={playHoverSound}
              className="bg-[var(--accent)] text-[var(--accent-ink)] hover:opacity-90 text-xs sm:text-sm font-semibold px-5 py-2.5 rounded-xl shadow-xs transition-all active:scale-[0.98] flex items-center gap-2"
            >
              Upgrade to Atelier Pro
              <ArrowRight size={14} />
            </button>
          ) : (
            <button
              type="button"
              onClick={playFocusSound}
              onMouseEnter={playHoverSound}
              className="bg-[var(--soft)] hover:bg-[var(--paper)] text-[var(--ink)] text-xs font-semibold px-4 py-2 rounded-xl border border-[var(--line)] transition-all"
            >
              Manage Billing &amp; Invoices
            </button>
          )}
        </div>
      </div>

      {/* Interval Switcher (Monthly vs Annual) */}
      <div className="flex justify-center my-1">
        <div className="inline-flex items-center gap-1.5 p-1 rounded-2xl bg-[var(--paper)] border border-[var(--line)] shadow-2xs">
          <button
            type="button"
            onClick={() => {
              playFocusSound();
              setAnnualBilling(false);
            }}
            className={`px-3.5 py-1.5 rounded-xl text-xs font-semibold transition-all ${
              !annualBilling
                ? "bg-[var(--surface)] text-[var(--ink)] shadow-xs border border-[var(--line)]"
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
            className={`px-3.5 py-1.5 rounded-xl text-xs font-semibold transition-all flex items-center gap-1.5 ${
              annualBilling
                ? "bg-[var(--surface)] text-[var(--ink)] shadow-xs border border-[var(--line)]"
                : "text-[var(--muted)] hover:text-[var(--ink)]"
            }`}
          >
            Annual Billing
            <span className="px-1.5 py-0.2 rounded-full bg-[var(--soft)] text-[var(--activity)] text-[10px] font-mono font-bold">
              Save 20%
            </span>
          </button>
        </div>
      </div>

      {/* Tier Comparison Matrix */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-stretch">
        {/* Explorer Free Plan */}
        <div
          className={`rounded-2xl p-6 sm:p-7 flex flex-col justify-between transition-all duration-200 ${
            currentTier === "FREE"
              ? "bg-[var(--paper)] border-2 border-[var(--line)]"
              : "bg-[var(--paper)]/60 border border-[var(--line)] opacity-80"
          }`}
        >
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-xs font-mono uppercase tracking-widest text-[var(--muted)] font-bold">
                Explorer
              </span>
              {currentTier === "FREE" && (
                <span className="text-[10px] font-mono font-bold uppercase tracking-wider bg-[var(--soft)] text-[var(--ink)] px-2.5 py-0.5 rounded-full border border-[var(--line)]">
                  Current Tier
                </span>
              )}
            </div>

            <div>
              <h3 className="font-serif text-xl text-[var(--ink)] font-medium">Free Access</h3>
              <div className="flex items-baseline gap-1 mt-1.5">
                <span className="font-serif text-3xl sm:text-4xl text-[var(--ink)] font-normal">$0</span>
                <span className="text-xs font-mono text-[var(--muted)]">/ month</span>
              </div>
            </div>

            <div className="h-[1px] w-full bg-[var(--line)]" />

            <ul className="space-y-3 text-xs text-[var(--ink)]">
              {[
                "100 Compute credits per cycle",
                "Standard speed generation queue",
                "Access to base foundation models",
                "Community governance & support",
                "Standard 1080p asset export",
              ].map((feature, i) => (
                <li key={i} className="flex items-center gap-2.5">
                  <div className="w-4 h-4 rounded-full bg-[var(--soft)] text-[var(--ink)] flex items-center justify-center shrink-0">
                    <Check size={11} />
                  </div>
                  <span>{feature}</span>
                </li>
              ))}
            </ul>
          </div>

          <div className="pt-6">
            <button
              type="button"
              disabled={currentTier === "FREE"}
              className="w-full py-2.5 rounded-xl border border-[var(--line)] text-[var(--muted)] text-xs font-semibold bg-[var(--surface)] hover:bg-[var(--soft)] cursor-default disabled:opacity-60 transition-all"
            >
              {currentTier === "FREE" ? "Active Tier" : "Downgrade to Free"}
            </button>
          </div>
        </div>

        {/* Institutional Atelier Pro Plan */}
        <div className="rounded-2xl p-6 sm:p-7 flex flex-col justify-between relative overflow-hidden bg-[var(--accent)] text-[var(--accent-ink)] shadow-md border-2 border-[var(--accent)]">
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-xs font-mono uppercase tracking-widest text-[var(--accent-ink)]/70 font-bold">
                Atelier Pro
              </span>
              <span className="inline-flex items-center gap-1 text-[10px] font-mono font-bold uppercase tracking-wider bg-white/10 text-[var(--accent-ink)] border border-white/20 px-2.5 py-0.5 rounded-full shadow-2xs">
                <Sparkles size={10} />
                Institutional Standard
              </span>
            </div>

            <div>
              <h3 className="font-serif text-xl text-[var(--accent-ink)] font-medium">Professional Creative Suite</h3>
              <div className="flex items-baseline gap-1 mt-1.5">
                <span className="font-serif text-3xl sm:text-4xl text-[var(--accent-ink)] font-normal">
                  {annualBilling ? "$24" : "$29"}
                </span>
                <span className="text-xs font-mono text-[var(--accent-ink)]/70">/ month billed annually</span>
              </div>
            </div>

            <div className="h-[1px] w-full bg-white/15" />

            <ul className="space-y-3 text-xs text-[var(--accent-ink)] font-medium">
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
                  <div className="w-4 h-4 rounded-full bg-white/15 text-[var(--accent-ink)] flex items-center justify-center shrink-0">
                    <Check size={11} />
                  </div>
                  <span>{feature}</span>
                </li>
              ))}
            </ul>
          </div>

          <div className="pt-6">
            <button
              type="button"
              onClick={playSubmitSound}
              onMouseEnter={playHoverSound}
              className="w-full py-3 rounded-xl bg-[var(--surface)] hover:bg-[var(--soft)] text-[var(--ink)] text-xs sm:text-sm font-bold shadow-xs transition-all active:scale-[0.98] flex items-center justify-center gap-2"
            >
              {currentTier === "PRO" ? "Current Pro Subscription" : "Upgrade to Atelier Pro"}
              <ArrowRight size={14} />
            </button>
          </div>
        </div>
      </div>

      {/* Payment Method & Security Row */}
      <div className="rounded-xl bg-[var(--paper)] border border-[var(--line)] p-4 sm:p-5 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="flex items-center gap-3.5">
          <div className="w-11 h-8 rounded-lg bg-[var(--soft)] text-[var(--ink)] flex items-center justify-center border border-[var(--line)]">
            <CreditCard size={17} />
          </div>
          <div>
            <p className="text-xs sm:text-sm font-semibold text-[var(--ink)]">
              Mastercard ending in <span className="font-mono">4242</span>
            </p>
            <p className="text-[11px] text-[var(--muted)] font-mono">
              Expires 12/28 • Encrypted Vault
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2.5 self-end sm:self-center">
          <button
            type="button"
            onClick={playFocusSound}
            onMouseEnter={playHoverSound}
            className="px-3.5 py-1.5 rounded-lg text-xs font-semibold bg-[var(--surface)] border border-[var(--line)] text-[var(--ink)] hover:bg-[var(--soft)] transition-all"
          >
            Update Card
          </button>
          <button
            type="button"
            onClick={playFocusSound}
            onMouseEnter={playHoverSound}
            className="px-3.5 py-1.5 rounded-lg text-xs font-semibold bg-[var(--surface)] border border-[var(--line)] text-[var(--ink)] hover:bg-[var(--soft)] transition-all flex items-center gap-1.5"
          >
            <Download size={12} />
            Invoices
          </button>
        </div>
      </div>
    </div>
  );
}
