import React from "react";
import SettingsClient from "./SettingsClient";

export const metadata = {
  title: "Settings & System Governance | VYREN",
  description: "Manage your institutional profile, computational quota allocations, and billing governance.",
};

export default function SettingsPage() {
  return (
    <div className="w-full h-full min-h-screen flex flex-col workspace-theme bg-[#f8f6f0] text-[#0f1419] font-sans overflow-y-auto pt-16">
      <SettingsClient />
    </div>
  );
}
