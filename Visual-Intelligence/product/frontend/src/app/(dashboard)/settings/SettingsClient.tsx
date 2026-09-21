"use client";

import React, { useState } from "react";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import { User, Activity, CreditCard, ArrowLeft, ShieldCheck, CheckCircle2 } from "lucide-react";
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
    <div className="w-full max-w-[1280px] mx-auto h-full flex flex-col md:flex-row bg-white border border-[#e3dfd4] rounded-[20px] shadow-[0_18px_55px_rgba(24,55,42,0.06)] overflow-hidden font-sans">
      
      {/* Integrated Left Sidebar */}
      <aside className="w-full md:w-72 shrink-0 bg-[#faf8f4] border-b md:border-b-0 md:border-r border-[#e3dfd4] flex flex-col justify-between p-6 sm:p-7 overflow-y-auto">
        <div className="space-y-6">
          
          {/* Back to Studio Link */}
          <div>
            <Link
              href="/studio"
              onMouseEnter={playHoverSound}
              className="inline-flex items-center gap-2 text-xs font-semibold text-[#5e6d68] hover:text-[#0f1419] transition-colors py-1 group font-sans"
            >
              <ArrowLeft size={13} className="transition-transform group-hover:-translate-x-0.5" />
              Back to Studio
            </Link>
          </div>

          {/* Header Block */}
          <div className="space-y-1.5">
            <h1 className="font-serif text-2xl sm:text-3xl text-[#0f1419] font-medium tracking-tight">
              Settings &amp; Governance
            </h1>
            <p className="text-xs text-[#5e6d68] font-normal leading-relaxed font-sans">
              Manage your institutional seat preferences, inference quota allocation, and billing.
            </p>
          </div>

          {/* Navigation Category List */}
          <nav className="space-y-2 pt-1" aria-label="Settings Categories">
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
                  className={`w-full text-left px-4 py-3 rounded-xl transition-all duration-150 flex items-start gap-3 select-none font-sans ${
                    isActive
                      ? "bg-white text-[#0f1419] border border-[#e3dfd4] shadow-xs"
                      : "text-[#5e6d68] hover:text-[#0f1419] hover:bg-[#f0ebe1]/70 border border-transparent"
                  }`}
                >
                  <div className={`mt-0.5 p-1.5 rounded-lg shrink-0 ${isActive ? "bg-[#f0ebe1] text-[#0f1419]" : "text-[#5e6d68]"}`}>
                    <IconComp size={16} />
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
        </div>

        {/* Node Telemetry Footer */}
        <div className="pt-6 mt-6 border-t border-[#e3dfd4] space-y-2">
          <div className="flex items-center gap-2 text-[10px] font-mono text-[#5e6d68] font-bold tracking-wider uppercase">
            <span className="w-2 h-2 rounded-full bg-[#059669]" />
            NODE: VY-892014-SYS
          </div>
          <div className="text-[11px] text-[#5e6d68] font-normal leading-relaxed font-sans">
            Zero telemetry drift. Local consensus synchronized across nodes.
          </div>
        </div>
      </aside>

      {/* Integrated Right Main Stage */}
      <main className="flex-1 h-full overflow-y-auto p-6 sm:p-10 bg-white">
        <div className="max-w-4xl mx-auto">
          <AnimatePresence mode="wait">
            <motion.div
              key={activeTab}
              initial={{ opacity: 0, y: 6 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -6 }}
              transition={{ duration: 0.16, ease: "easeOut" }}
              className="w-full"
            >
              {activeTab === "profile" && <ProfileTab />}
              {activeTab === "usage" && <UsageTab />}
              {activeTab === "subscription" && <SubscriptionTab />}
            </motion.div>
          </AnimatePresence>
        </div>
      </main>

    </div>
  );
}
