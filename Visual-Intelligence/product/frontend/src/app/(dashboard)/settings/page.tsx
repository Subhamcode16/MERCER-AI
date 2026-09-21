import React from "react";
import SettingsClient from "./SettingsClient";

export const metadata = {
  title: "Settings & System Governance | VYREN",
  description: "Manage your institutional profile, computational quota allocations, and billing governance.",
};

export default function SettingsPage() {
  return (
    <div className="w-full h-full min-h-screen flex flex-col bg-[var(--paper)] text-[var(--ink)] overflow-y-auto pt-16">
      <SettingsClient />
    </div>
  );
}
