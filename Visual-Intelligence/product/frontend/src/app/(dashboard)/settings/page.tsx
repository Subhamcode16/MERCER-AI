import React from "react";
import SettingsClient from "./SettingsClient";

export const metadata = {
  title: "Settings | VYREN Brand Intelligence OS",
  description: "Manage your institutional profile, computational quota allocations, and billing governance.",
};

export default function SettingsPage() {
  return (
    <div className="relative min-h-screen w-full overflow-y-auto px-4 py-24 sm:px-8 md:px-12 flex justify-center selection:bg-slate-900 selection:text-white">
      {/* Daylight Atmospheric Diffusion Scrim from DESIGN.md */}
      <div
        className="fixed inset-0 z-0 pointer-events-none"
        style={{
          background:
            "radial-gradient(ellipse 80% 60% at 50% 20%, rgba(255,255,255,0.5) 0%, rgba(255,255,255,0.15) 60%, transparent 100%)",
        }}
      />

      <div className="relative z-10 w-full max-w-5xl mx-auto space-y-8">
        {/* Editorial Header Section */}
        <div className="flex flex-col gap-2.5">
          <div className="inline-flex items-center gap-2 self-start px-3 py-1 rounded-full bg-white/60 backdrop-blur-md border border-white/80 shadow-xs text-[10px] font-mono tracking-widest uppercase font-bold text-slate-800">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-600 animate-pulse" />
            VYREN // Account &amp; System Governance
          </div>

          <div className="flex flex-col sm:flex-row sm:items-baseline justify-between gap-2">
            <h1 className="font-serif text-3xl sm:text-4xl text-[#0f172a] font-normal tracking-tight">
              Settings &amp; Configuration
            </h1>
            <span className="text-xs font-mono text-slate-600 font-medium">
              NODE ID // VY-892014-SYS
            </span>
          </div>

          <p className="text-sm text-slate-700 max-w-2xl font-light leading-relaxed">
            Configure your institutional workspace seat, computational intelligence quotas, tier permissions, and brand governance.
          </p>
        </div>

        {/* Client Interactive Tabs */}
        <SettingsClient />
      </div>
    </div>
  );
}
