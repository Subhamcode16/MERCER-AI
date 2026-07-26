"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import ProfileTab from "./tabs/ProfileTab";
import UsageTab from "./tabs/UsageTab";
import SubscriptionTab from "./tabs/SubscriptionTab";

const tabs = [
  { id: "profile", label: "Personal Profile" },
  { id: "usage", label: "Usage" },
  { id: "subscription", label: "Subscription" },
];

export default function SettingsClient() {
  const [activeTab, setActiveTab] = useState("profile");

  return (
    <div className="w-full">
      {/* Tabs Navigation */}
      <div className="flex border-b border-white/10 mb-8 overflow-x-auto hide-scrollbar">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`relative px-4 py-3 text-sm font-medium tracking-wide transition-colors whitespace-nowrap ${
              activeTab === tab.id ? "text-[#E1D4C0]" : "text-white/40 hover:text-white/80"
            }`}
          >
            {tab.label}
            {activeTab === tab.id && (
              <motion.div
                layoutId="activeTabIndicator"
                className="absolute bottom-0 left-0 right-0 h-0.5 bg-[#E1D4C0]"
                initial={false}
                transition={{ type: "spring", stiffness: 400, damping: 30 }}
              />
            )}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="relative min-h-[400px]">
        <AnimatePresence mode="wait">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.2 }}
            className="w-full"
          >
            {activeTab === "profile" && <ProfileTab />}
            {activeTab === "usage" && <UsageTab />}
            {activeTab === "subscription" && <SubscriptionTab />}
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
}
