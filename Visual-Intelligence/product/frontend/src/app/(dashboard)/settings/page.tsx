import React from "react";
import SettingsClient from "./SettingsClient";

export const metadata = {
  title: "Settings & System Governance | VYREN",
  description: "Manage your institutional profile, computational quota allocations, and billing governance.",
};

export default function SettingsPage() {
  return (
    <div className="w-full h-[calc(100vh-60px)] min-h-[640px] flex flex-col workspace-theme bg-[#f8f6f0] text-[#0f1419] font-sans pt-18 sm:pt-20 px-4 sm:px-8 pb-6 overflow-hidden">
      <SettingsClient />
    </div>
  );
}
