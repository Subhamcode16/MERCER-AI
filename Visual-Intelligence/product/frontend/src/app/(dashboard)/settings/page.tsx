import React from "react";
import SettingsClient from "./SettingsClient";

export const metadata = {
  title: "Settings | VYREN",
  description: "Manage your personal profile, computational credit allocation, and subscription plan.",
};

export default function SettingsPage() {
  return (
    <div className="w-full min-h-screen flex flex-col workspace-theme bg-[#f8f6f0] text-[#0f1419] font-sans pt-16 pb-16 overflow-y-auto">
      <SettingsClient />
    </div>
  );
}
