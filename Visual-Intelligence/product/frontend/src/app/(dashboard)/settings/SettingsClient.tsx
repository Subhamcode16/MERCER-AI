"use client";

import React, { useState } from "react";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import { User, Activity, CreditCard, ArrowLeft, ShieldCheck, Sparkles, Volume2 } from "lucide-react";
import ProfileTab from "./tabs/ProfileTab";
import UsageTab from "./tabs/UsageTab";
import SubscriptionTab from "./tabs/SubscriptionTab";
import { useTactileAudio } from "@/components/dashboard/useTactileAudio";

const navItems = [
  { id: "profile", label: "Personal Profile", description: "Identity, credentials & studio", icon: User },
  { id: "usage", label: "Computational Usage", description: "Ledger, quotas & consensus", icon: Activity },
  { id: "subscription", label: "Membership & Tiers", description: "Plans, billing & invoices", icon: CreditCard },
];

export default function SettingsClient() {
  const [activeTab, setActiveTab] = useState("profile");
  const { playHoverSound, playFocusSound } = useTactileAudio();

  return (
    <div className="w-full max-w-6xl mx-auto px-4 sm:px-8 py-8 flex flex-col md:flex-row gap-8 items-start">
      
      {/* Left Sidebar Sub-Nav */}
      <aside className="w-full md:w-64 shrink-0 space-y-6">
        
        {/* Back to Studio Anchor */}
        <div>
          <Link
            href="/studio"
            onMouseEnter={playHoverSound}
            className="inline-flex items-center gap-2 text-xs font-semibold text-[var(--muted)] hover:text-[var(--ink)] transition-colors py-1"
          >
            <ArrowLeft size={13} />
            Back to Studio
          </Link>
        </div>

        {/* Header Block */}
        <div className="space-y-1">
          <h1 className="font-serif text-2xl sm:text-3xl text-[var(--ink)] font-medium tracking-tight">
            Settings
          </h1>
          <p className="text-xs text-[var(--muted)] font-light leading-relaxed">
            Institutional seat preferences, inference quota allocation, and billing.
          </p>
        </div>

        {/* Navigation List */}
        <nav className="space-y-1.5 pt-2" aria-label="Settings Categories">
          {navItems.map((item) => {
            const IconComp = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                type="button"
                onClick={() => {
                  playFocusSound();
                  setActiveTab(item.id);
                }}
                onMouseEnter={playHoverSound}
                className={`w-full text-left px-3.5 py-3 rounded-xl transition-all duration-150 flex items-start gap-3 select-none ${
                  isActive
                    ? "bg-[var(--surface)] text-[var(--ink)] border border-[var(--line)] shadow-xs"
                    : "text-[var(--muted)] hover:text-[var(--ink)] hover:bg-[var(--soft)] border border-transparent"
                }`}
              >
                <div className={`mt-0.5 p-1.5 rounded-lg shrink-0 ${isActive ? "bg-[var(--soft)] text-[var(--ink)]" : "text-[var(--muted)]"}`}>
                  <IconComp size={15} />
                </div>
                <div className="min-w-0">
                  <div className={`text-xs font-semibold ${isActive ? "text-[var(--ink)]" : "text-[var(--ink)]/80"}`}>
                    {item.label}
                  </div>
                  <div className="text-[11px] text-[var(--muted)] truncate font-light mt-0.5">
                    {item.description}
                  </div>
                </div>
              </button>
            );
          })}
        </nav>

        {/* Node Status Box */}
        <div className="pt-4 border-t border-[var(--line)] space-y-2">
          <div className="flex items-center gap-2 text-[10px] font-mono text-[var(--muted)]">
            <span className="w-1.5 h-1.5 rounded-full bg-[var(--activity)]" />
            NODE: VY-892014-SYS
          </div>
          <div className="text-[11px] text-[var(--muted)] font-light">
            Zero telemetry drift detected. Local consensus synchronized.
          </div>
        </div>
      </aside>

      {/* Right Main Workbench Stage */}
      <main className="flex-1 w-full min-w-0 bg-[var(--surface)] border border-[var(--line)] rounded-2xl shadow-xs p-6 sm:p-9 transition-all duration-200">
        <AnimatePresence mode="wait">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            transition={{ duration: 0.18, ease: "easeOut" }}
            className="w-full"
          >
            {activeTab === "profile" && <ProfileTab />}
            {activeTab === "usage" && <UsageTab />}
            {activeTab === "subscription" && <SubscriptionTab />}
          </motion.div>
        </AnimatePresence>
      </main>

    </div>
  );
}
