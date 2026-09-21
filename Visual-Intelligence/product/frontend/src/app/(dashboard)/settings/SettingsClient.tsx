"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { User, Activity, CreditCard } from "lucide-react";
import ProfileTab from "./tabs/ProfileTab";
import UsageTab from "./tabs/UsageTab";
import SubscriptionTab from "./tabs/SubscriptionTab";
import { useTactileAudio } from "@/components/dashboard/useTactileAudio";
import { RadialMenu } from "@/components/workspace/RadialMenu";

const tabs = [
  { id: "profile", label: "Personal Profile", icon: User },
  { id: "usage", label: "Computational Usage", icon: Activity },
  { id: "subscription", label: "Membership & Tiers", icon: CreditCard },
];

export default function SettingsClient() {
  const [activeTab, setActiveTab] = useState("profile");
  const { playHoverSound, playFocusSound } = useTactileAudio();
  const router = useRouter();

  const handleRadialAction = (id: string) => {
    if (id === "home") router.push("/home");
    else if (id === "studio") router.push("/studio");
    else if (id === "metrics") router.push("/activity");
    else if (id === "kanban") router.push("/campaigns");
    else if (id === "assets") router.push("/assets");
    else if (id === "settings") router.push("/settings");
  };

  return (
    <div className="w-full space-y-6">
      {/* Universal Floating Radial Quick Menu for Non-Home Pages */}
      <RadialMenu onAction={handleRadialAction} />

      {/* Floating Segmented Glass Tab Switcher */}
      <div className="inline-flex items-center gap-1.5 p-1.5 rounded-2xl bg-white/75 backdrop-blur-xl border border-white shadow-sm overflow-x-auto max-w-full">
        {tabs.map((tab) => {
          const IconComp = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => {
                playFocusSound();
                setActiveTab(tab.id);
              }}
              onMouseEnter={playHoverSound}
              className={`relative flex items-center gap-2 px-4 sm:px-5 py-2.5 rounded-xl text-xs sm:text-sm font-semibold transition-all duration-200 select-none whitespace-nowrap ${
                isActive
                  ? "text-[#0f172a]"
                  : "text-slate-600 hover:text-[#0f172a] hover:bg-white/40"
              }`}
            >
              {isActive && (
                <motion.div
                  layoutId="activeSettingsTabPill"
                  className="absolute inset-0 rounded-xl bg-white shadow-[0_2px_12px_rgba(0,0,0,0.08)] border border-white"
                  transition={{ type: "spring", stiffness: 420, damping: 32 }}
                />
              )}
              <span className="relative z-10 flex items-center gap-2">
                <IconComp
                  size={15}
                  className={isActive ? "text-[#0f172a]" : "text-slate-500"}
                />
                {tab.label}
              </span>
            </button>
          );
        })}
      </div>

      {/* Unified High-Density Alabaster Liquid Glass Workbench */}
      <main className="w-full rounded-3xl bg-white/94 backdrop-blur-3xl border border-white shadow-[0_30px_80px_rgba(15,23,42,0.12),inset_0_1.5px_2px_rgba(255,255,255,1)] p-6 sm:p-10 transition-all duration-300">
        <AnimatePresence mode="wait">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, y: 10, filter: "blur(3px)" }}
            animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
            exit={{ opacity: 0, y: -8, filter: "blur(3px)" }}
            transition={{ duration: 0.22, ease: [0.16, 1, 0.3, 1] }}
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
