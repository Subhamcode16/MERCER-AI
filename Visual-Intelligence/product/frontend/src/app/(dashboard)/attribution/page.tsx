"use client";

import React, { useEffect, useState } from "react";
import { LearningAPI, AttributionReport, CalibrationTelemetry } from "@/lib/learning-api";
import { Target, Activity, ShieldCheck, AlertOctagon, BarChart2, CheckCircle2, TrendingUp, Sliders } from "lucide-react";

export default function EpistemicAttributionPage() {
  const [attributions, setAttributions] = useState<AttributionReport[]>([]);
  const [calibrations, setCalibrations] = useState<CalibrationTelemetry[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      const [attr, cal] = await Promise.all([
        LearningAPI.getAttributions("TENANT-LUXE"),
        LearningAPI.getCalibrationRadar(),
      ]);
      setAttributions(attr);
      setCalibrations(cal);
      setLoading(false);
    }
    loadData();
  }, []);

  return (
    <div className="flex-1 space-y-8 p-8 max-w-7xl mx-auto text-foreground">
      {/* Header Banner */}
      <div className="flex items-center justify-between border-b border-border pb-6">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="px-2.5 py-0.5 rounded text-[10px] font-mono uppercase bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
              Phase 28 Operating Loop
            </span>
            <span className="text-xs text-muted-foreground font-mono">Tenant: LUXE-MAISON</span>
          </div>
          <h1 className="text-3xl font-serif tracking-tight text-white flex items-center gap-3">
            <Target className="w-7 h-7 text-cyan-400" />
            Epistemic Attribution & Model Calibration Radar
          </h1>
          <p className="text-sm text-muted-foreground mt-1">
            Confounder isolation, empirical lift recalibration, and continuous Brier score overconfidence tracking.
          </p>
        </div>
      </div>

      {/* Top Confounder Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {attributions.map((item) => (
          <div
            key={item.campaign_id}
            className="bg-card border border-border rounded-xl p-6 space-y-4 shadow-sm hover:border-cyan-500/30 transition-all"
          >
            <div className="flex items-center justify-between">
              <span className="font-mono text-xs font-semibold text-white">{item.campaign_id}</span>
              <span className={`px-2.5 py-0.5 rounded text-[10px] font-mono font-semibold ${
                item.epistemic_grade === "CONTROLLED_EXPERIMENT"
                  ? "bg-emerald-500/15 text-emerald-400 border border-emerald-500/30"
                  : "bg-amber-500/15 text-amber-400 border border-amber-500/30"
              }`}>
                {item.epistemic_grade}
              </span>
            </div>

            <div className="grid grid-cols-3 gap-3 p-3 bg-neutral-950/60 rounded-lg border border-white/5 font-mono text-center">
              <div>
                <div className="text-neutral-400 text-[10px] uppercase">Raw CTR Lift</div>
                <div className="text-lg font-bold text-neutral-300 mt-0.5">+{(item.raw_lift * 100).toFixed(1)}%</div>
              </div>
              <div>
                <div className="text-neutral-400 text-[10px] uppercase">Confounder Score</div>
                <div className="text-lg font-bold text-amber-400 mt-0.5">{(item.confounder_score * 100).toFixed(0)}%</div>
              </div>
              <div>
                <div className="text-neutral-400 text-[10px] uppercase">Isolated Lift</div>
                <div className="text-lg font-bold text-emerald-400 mt-0.5">+{(item.calibrated_lift * 100).toFixed(1)}%</div>
              </div>
            </div>

            <div className="space-y-1.5 text-xs font-mono">
              <div className="text-neutral-400 text-[11px]">Confounders Isolated:</div>
              {item.confounders_detected.map((c, idx) => (
                <div key={idx} className="flex items-center gap-1.5 text-neutral-300">
                  <AlertOctagon className="w-3.5 h-3.5 text-amber-400 shrink-0" />
                  <span>{c}</span>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* Model Calibration Radar Section */}
      <div className="bg-card border border-border rounded-xl p-6 space-y-6">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold text-white flex items-center gap-2 font-serif">
            <Activity className="w-5 h-5 text-cyan-400" />
            Model Calibration Radar (Brier Score Tracking)
          </h2>
          <span className="text-xs font-mono text-muted-foreground">Threshold: Brier Score &lt; 0.15</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {calibrations.map((cal) => (
            <div
              key={cal.model_id}
              className="p-5 bg-neutral-950/60 rounded-xl border border-white/5 space-y-4 font-mono text-xs"
            >
              <div className="flex items-center justify-between">
                <div>
                  <div className="font-semibold text-white text-sm">{cal.model_id}</div>
                  <div className="text-muted-foreground text-[11px]">Skill: {cal.skill_name}</div>
                </div>
                <span className={`px-2.5 py-0.5 rounded text-[10px] font-semibold ${
                  cal.is_well_calibrated
                    ? "bg-emerald-500/15 text-emerald-400 border border-emerald-500/30"
                    : "bg-amber-500/15 text-amber-400 border border-amber-500/30"
                }`}>
                  {cal.is_well_calibrated ? "WELL-CALIBRATED" : "OVERCONFIDENT"}
                </span>
              </div>

              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-neutral-400">Brier Score (Lower is better):</span>
                  <span className="text-white font-bold">{cal.brier_score}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-neutral-400">Overconfidence Penalty:</span>
                  <span className="text-amber-400">-{cal.overconfidence_penalty}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-neutral-400">Empirical Accuracy vs Confidence:</span>
                  <span className="text-emerald-400">{(cal.empirical_accuracy * 100).toFixed(0)}% vs {(cal.predicted_confidence_mean * 100).toFixed(0)}%</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
