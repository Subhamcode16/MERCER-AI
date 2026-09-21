"use client";

import React, { useState } from "react";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import { User, Activity, CreditCard, ArrowLeft, CheckCircle2 } from "lucide-react";
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
    <div className="w-full max-w-6xl mx-auto px-4 sm:px-8 py-8 flex flex-col md:flex-row gap-8 items-start font-sans">
      
      {/* Left Sidebar Sub-Nav */}
      <aside className="w-full md:w-64 shrink-0 space-y-6">
        
        {/* Back to Studio Anchor */}
        <div>
          <Link
            href="/studio"
            onMouseEnter={playHoverSound}
            className="inline-flex items-center gap-2 text-xs font-semibold text-[#5e6d68] hover:text-[#0f1419] transition-colors py-1"
          >
            <ArrowLeft size={13} />
            Back to Studio
          </Link>
        </div>

        {/* Header Block */}
        <div className="space-y-1">
          <h1 className="font-serif text-2xl sm:text-3xl text-[#0f1419] font-medium tracking-tight">
            Settings
          </h1>
          <p className="text-xs text-[#5e6d68] font-normal leading-relaxed">
            Institutional seat preferences, inference quota allocation, and billing governance.
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
                    ? "bg-white text-[#0f1419] border border-[#e3dfd4] shadow-xs"
                    : "text-[#5e6d68] hover:text-[#0f1419] hover:bg-[#f0ebe1] border border-transparent"
                }`}
              >
                <div className={`mt-0.5 p-1.5 rounded-lg shrink-0 ${isActive ? "bg-[#f0ebe1] text-[#0f1419]" : "text-[#5e6d68]"}`}>
                  <IconComp size={15} />
                </div>
                <div className="min-w-0">
                  <div className={`text-xs font-semibold ${isActive ? "text-[#0f1419]" : "text-[#0f1419]/80"}`}>
                    {item.label}
                  </div>
                  <div className="text-[11px] text-[#5e6d68] truncate font-normal mt-0.5">
                    {item.description}
                  </div>
                </div>
              </button>
            );
          })}
        </nav>

        {/* Node Status Box */}
        <div className="pt-4 border-t border-[#e3dfd4] space-y-2">
          <div className="flex items-center gap-2 text-[10px] font-mono text-[#5e6d68] font-bold tracking-wider uppercase">
            <span className="w-2 h-2 rounded-full bg-[#059669]" />
            NODE: VY-892014-SYS
          </div>
          <div className="text-[11px] text-[#5e6d68] font-normal leading-relaxed">
            Zero telemetry drift detected. Local consensus synchronized.
          </div>
        </div>
      </aside>

      {/* Right Main Workbench Stage */}
      <main className="flex-1 w-full min-w-0 bg-white border border-[#e3dfd4] rounded-2xl shadow-xs p-6 sm:p-9 transition-all duration-200">
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
