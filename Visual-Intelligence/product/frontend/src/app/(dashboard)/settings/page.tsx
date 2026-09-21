import React from "react";
import SettingsClient from "./SettingsClient";

export const metadata = {
  title: "Settings | VYREN Brand Intelligence OS",
  description: "Manage your institutional profile, computational quota allocations, and billing governance.",
};

export default function SettingsPage() {
  return (
    <div className="relative min-h-screen w-full overflow-y-auto px-4 py-24 sm:px-8 md:px-12 flex justify-center selection:bg-slate-900 selection:text-white">
      {/* ✦ 1. Luminous Daylight Meadow Sky Atmosphere (Option A) */}
      <div
        className="fixed inset-0 z-0 pointer-events-none overflow-hidden"
        style={{
          background: `
            radial-gradient(ellipse 90% 70% at 75% 15%, rgba(255, 246, 220, 0.65) 0%, rgba(255, 255, 255, 0.25) 45%, transparent 75%),
            radial-gradient(ellipse 80% 60% at 20% 20%, rgba(198, 226, 240, 0.6) 0%, rgba(255, 255, 255, 0) 65%),
            linear-gradient(180deg, #9bbecf 0%, #b8d4df 28%, #dce8ea 60%, #eef3ec 92%, #e5ecd8 100%)
          `,
        }}
      >
        {/* Soft Animated Daylight Caustic / Sun Glare */}
        <div className="absolute -top-32 right-1/4 w-[600px] h-[600px] rounded-full bg-gradient-to-br from-amber-100/50 via-white/40 to-transparent blur-3xl pointer-events-none" />
        <div className="absolute top-1/3 -left-20 w-[500px] h-[500px] rounded-full bg-gradient-to-tr from-teal-100/40 via-sky-100/30 to-transparent blur-3xl pointer-events-none" />
      </div>

      <div className="relative z-10 w-full max-w-4xl mx-auto space-y-7">
        {/* Editorial Header Section */}
        <div className="flex flex-col gap-2.5">
          <div className="inline-flex items-center gap-2 self-start px-3.5 py-1 rounded-full bg-white/75 backdrop-blur-md border border-white shadow-xs text-[10px] font-mono tracking-widest uppercase font-bold text-slate-800">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-600 animate-pulse" />
            VYREN // Account &amp; System Governance
          </div>

          <div className="flex flex-col sm:flex-row sm:items-baseline justify-between gap-2">
            <h1 className="font-serif text-3xl sm:text-4xl text-[#0f172a] font-normal tracking-tight drop-shadow-[0_1px_1px_rgba(255,255,255,0.8)]">
              Settings &amp; Configuration
            </h1>
            <span className="text-xs font-mono text-slate-700 font-semibold bg-white/50 px-2.5 py-0.5 rounded-md border border-white/80">
              NODE ID // VY-892014-SYS
            </span>
          </div>

          <p className="text-sm text-slate-800 max-w-2xl font-normal leading-relaxed drop-shadow-[0_1px_0_rgba(255,255,255,0.7)]">
            Configure your institutional workspace credentials, computational intelligence quotas, tier permissions, and brand governance.
          </p>
        </div>

        {/* Client Interactive Workbench */}
        <SettingsClient />
      </div>
    </div>
  );
}
