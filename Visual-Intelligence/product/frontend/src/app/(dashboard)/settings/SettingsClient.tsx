"use client";

import React, { useState } from "react";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import { ArrowLeft, User, Activity, CreditCard } from "lucide-react";
import ProfileTab from "./tabs/ProfileTab";
import UsageTab from "./tabs/UsageTab";
import SubscriptionTab from "./tabs/SubscriptionTab";
import { useTactileAudio } from "@/components/dashboard/useTactileAudio";

const tabs = [
  { id: "profile", label: "Profile", icon: User },
  { id: "usage", label: "Usage & Compute", icon: Activity },
  { id: "subscription", label: "Subscription", icon: CreditCard },
];

export default function SettingsClient() {
  const [activeTab, setActiveTab] = useState("profile");
  const { playHoverSound, playFocusSound } = useTactileAudio();

  return (
    <div className="w-full max-w-3xl mx-auto px-4 sm:px-6 pt-6 pb-12 space-y-6 font-sans">
      
      {/* Top Breadcrumb & Headline */}
      <div className="space-y-3">
        <Link
          href="/studio"
          onMouseEnter={playHoverSound}
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-[#5e6d68] hover:text-[#0f1419] transition-colors py-1 group"
        >
          <ArrowLeft size={13} className="transition-transform group-hover:-translate-x-0.5" />
          <span>Back to Studio</span>
        </Link>

        <div>
          <h1 className="font-serif text-3xl sm:text-4xl text-[#0f1419] font-medium tracking-tight">
            Settings
          </h1>
          <p className="text-sm text-[#5e6d68] font-normal mt-1 leading-relaxed">
            Manage your personal profile, computational quotas, and subscription plan.
          </p>
        </div>
      </div>

      {/* Segmented Horizontal Tabs */}
      <div className="flex border-b border-[#e3dfd4] gap-6">
        {tabs.map((tab) => {
          const IconComp = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              type="button"
              onClick={() => {
                playFocusSound();
                setActiveTab(tab.id);
              }}
              onMouseEnter={playHoverSound}
              className={`relative pb-3 flex items-center gap-2 text-sm font-semibold transition-colors ${
                isActive ? "text-[#0f1419]" : "text-[#5e6d68] hover:text-[#0f1419]"
              }`}
            >
              <IconComp size={15} />
              <span>{tab.label}</span>
              {isActive && (
                <motion.div
                  layoutId="activeTabUnderline"
                  className="absolute bottom-0 left-0 right-0 h-0.5 bg-[#1e3a34]"
                  initial={false}
                  transition={{ type: "spring", stiffness: 450, damping: 35 }}
                />
              )}
            </button>
          );
        })}
      </div>

      {/* Main Tab Stage Card */}
      <main className="bg-white border border-[#e3dfd4] rounded-2xl p-6 sm:p-8 shadow-xs">
        <AnimatePresence mode="wait">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, y: 6 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -6 }}
            transition={{ duration: 0.16, ease: "easeOut" }}
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
