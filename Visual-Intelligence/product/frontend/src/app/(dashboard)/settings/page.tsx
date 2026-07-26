import React from "react";
import SettingsClient from "./SettingsClient";

export const metadata = {
  title: "Settings | Antigravity",
  description: "Manage your account, subscription, and usage.",
};

export default function SettingsPage() {
  return (
    <div className="min-h-screen bg-[#0A0A0A] text-white p-6 md:p-12 w-full max-w-5xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight text-white/90">Settings</h1>
        <p className="text-sm text-white/50 mt-1">Manage your account preferences, billing, and usage statistics.</p>
      </div>
      
      <SettingsClient />
    </div>
  );
}
