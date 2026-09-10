"use client";

import React, { useEffect, useState } from "react";
import { IntelligenceAPI, StrategicObservatorySnapshot, StrategicSignal } from "@/lib/intelligence-api";
import { Activity, Radio, AlertTriangle, TrendingUp, Compass, ShieldAlert, Cpu, CheckCircle2, ArrowUpRight } from "lucide-react";

export default function StrategicObservatoryPage() {
  const [snapshot, setSnapshot] = useState<StrategicObservatorySnapshot | null>(null);
  const [signals, setSignals] = useState<StrategicSignal[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      const [snap, sigs] = await Promise.all([
        IntelligenceAPI.getObservatory("TENANT-LUXE"),
        IntelligenceAPI.getSignals("TENANT-LUXE"),
      ]);
      setSnapshot(snap);
      setSignals(sigs);
      setLoading(false);
    }
    fetchData();
  }, []);

  return (
    <div className="flex-1 space-y-8 p-8 max-w-7xl mx-auto text-foreground">
      {/* Header Banner */}
      <div className="flex items-center justify-between border-b border-border pb-6">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="px-2.5 py-0.5 rounded text-[10px] font-mono uppercase bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              Phase 29 Operating Layer
            </span>
            <span className="text-xs text-muted-foreground font-mono">Tenant: LUXE-MAISON</span>
          </div>
          <h1 className="text-3xl font-serif tracking-tight text-white flex items-center gap-3">
            <Compass className="w-7 h-7 text-emerald-400" />
            Strategic Intelligence Observatory
          </h1>
          <p className="text-sm text-muted-foreground mt-1">
            Organizational decision fabric, cross-campaign signal radar, and continuous epistemic monitoring.
          </p>
        </div>

        <div className="flex items-center gap-3 font-mono text-xs">
          <div className="flex items-center gap-2 bg-neutral-900 border border-border px-3 py-1.5 rounded-lg">
            <Radio className="w-3.5 h-3.5 text-emerald-400 animate-pulse" />
            <span>Telemetry Live</span>
          </div>
        </div>
      </div>

      {/* Top Telemetry KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 font-mono">
        <div className="bg-card border border-border rounded-xl p-5 shadow-sm">
          <div className="text-xs text-muted-foreground uppercase flex items-center justify-between">
            <span>Graph Nodes</span>
            <Activity className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-bold text-white mt-2">
            {snapshot?.metrics.total_entities_in_graph || 342}
          </div>
          <div className="text-[11px] text-emerald-400 mt-1 flex items-center gap-1">
            <CheckCircle2 className="w-3 h-3" /> 100% Provenance Hashed
          </div>
        </div>

        <div className="bg-card border border-border rounded-xl p-5 shadow-sm">
          <div className="text-xs text-muted-foreground uppercase flex items-center justify-between">
            <span>Active Signals</span>
            <TrendingUp className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-2xl font-bold text-white mt-2">
            {snapshot?.metrics.active_signals_count || 14}
          </div>
          <div className="text-[11px] text-cyan-400 mt-1">
            5 Emerging • 3 Fatigue
          </div>
        </div>

        <div className="bg-card border border-border rounded-xl p-5 shadow-sm">
          <div className="text-xs text-muted-foreground uppercase flex items-center justify-between">
            <span>Active Hypotheses</span>
            <Cpu className="w-4 h-4 text-purple-400" />
          </div>
          <div className="text-2xl font-bold text-white mt-2">
            {snapshot?.metrics.active_hypotheses_count || 6}
          </div>
          <div className="text-[11px] text-purple-300 mt-1">
            3 Supported in A/B Trials
          </div>
        </div>

        <div className="bg-card border border-border rounded-xl p-5 shadow-sm">
          <div className="text-xs text-muted-foreground uppercase flex items-center justify-between">
            <span>Governance Queue</span>
            <AlertTriangle className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-2xl font-bold text-white mt-2">
            {snapshot?.metrics.active_recommendations_count || 4}
          </div>
          <div className="text-[11px] text-amber-400 mt-1">
            2 Awaiting Operator Review
          </div>
        </div>
      </div>

      {/* Main Signal Radar Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left 2 Cols: Live Signal Feed */}
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-white flex items-center gap-2">
              <Radio className="w-4 h-4 text-emerald-400" />
              Strategic Signal Timeline
            </h2>
            <span className="text-xs font-mono text-muted-foreground">Epistemic Status Calibrated</span>
          </div>

          <div className="space-y-3">
            {signals.map((sig) => (
              <div
                key={sig.signal_id}
                className="bg-card border border-border hover:border-emerald-500/30 transition-all rounded-xl p-5 space-y-3"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-semibold ${
                      sig.signal_class === "EMERGING_PATTERN"
                        ? "bg-emerald-500/15 text-emerald-400 border border-emerald-500/30"
                        : "bg-amber-500/15 text-amber-400 border border-amber-500/30"
                    }`}>
                      {sig.signal_class}
                    </span>
                    <span className="text-xs font-mono text-neutral-400">{sig.scope}</span>
                  </div>
                  <span className="font-mono text-xs text-neutral-400">
                    Confidence: <strong className="text-white">{(sig.confidence * 100).toFixed(0)}%</strong>
                  </span>
                </div>

                <div className="text-sm text-neutral-200 leading-relaxed font-medium">
                  {sig.observed_pattern}
                </div>

                <div className="bg-neutral-950/60 rounded-lg p-3 border border-white/5 space-y-1.5 text-xs font-mono">
                  <div className="flex items-center justify-between text-muted-foreground">
                    <span>Epistemic Status: <strong className="text-neutral-300">{sig.epistemic_status}</strong></span>
                    <span>Freshness: <strong className="text-emerald-400">{sig.freshness * 100}%</strong></span>
                  </div>
                  {sig.unknowns.length > 0 && (
                    <div className="text-[11px] text-amber-400/90 pt-1 border-t border-white/5">
                      <strong>Unobserved Unknowns:</strong> {sig.unknowns[0]}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Right Col: Contradiction & Knowledge Decay Map */}
        <div className="space-y-6">
          <div className="bg-card border border-border rounded-xl p-5 space-y-4">
            <h3 className="text-sm font-semibold text-white uppercase font-mono tracking-wider flex items-center gap-2">
              <ShieldAlert className="w-4 h-4 text-cyan-400" />
              Contradiction Radar
            </h3>
            <p className="text-xs text-muted-foreground">
              Preserves scope-specific divergence without forced synthesis.
            </p>

            <div className="space-y-2.5">
              <div className="p-3 rounded-lg bg-neutral-950/60 border border-white/5 text-xs font-mono space-y-1">
                <div className="text-cyan-300 font-semibold">Brutalist vs Heritage Typography</div>
                <div className="text-muted-foreground text-[11px]">
                  • Brutalist Sans: +22% lift on Gen-Z Streetwear<br />
                  • Serif Minimal: +14% lift on High-Net-Worth Heritage
                </div>
                <div className="text-[10px] text-emerald-400 pt-1">
                  Status: Scope Split Resolved (Zero Overwrite)
                </div>
              </div>
            </div>
          </div>

          <div className="bg-card border border-border rounded-xl p-5 space-y-4">
            <h3 className="text-sm font-semibold text-white uppercase font-mono tracking-wider flex items-center gap-2">
              <Activity className="w-4 h-4 text-purple-400" />
              Exponential Freshness Decay
            </h3>
            <div className="space-y-2 text-xs font-mono">
              <div className="flex justify-between items-center">
                <span className="text-neutral-400">Meta Video Formats (Half-life 35d)</span>
                <span className="text-emerald-400">92% Fresh</span>
              </div>
              <div className="w-full bg-neutral-900 rounded-full h-1.5">
                <div className="bg-emerald-500 h-1.5 rounded-full" style={{ width: "92%" }} />
              </div>

              <div className="flex justify-between items-center pt-2">
                <span className="text-neutral-400">TikTok Pacing Models (Half-life 14d)</span>
                <span className="text-amber-400">54% (Recalibrating)</span>
              </div>
              <div className="w-full bg-neutral-900 rounded-full h-1.5">
                <div className="bg-amber-500 h-1.5 rounded-full" style={{ width: "54%" }} />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
