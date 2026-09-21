"use client";

import React, { useState } from "react";
import {
  Activity,
  Clock,
  Zap,
  TrendingUp,
  Coins,
  CheckCircle2,
  AlertCircle,
} from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";
import { useTactileAudio } from "@/components/dashboard/useTactileAudio";

interface LedgerEvent {
  id: string;
  type: string;
  model: string;
  cost: number | string;
  date: string;
  status: "Success" | "Completed" | "Failed (Refunded)" | "Processing";
}

const usageLog: LedgerEvent[] = [
  {
    id: "gen_1",
    type: "Generation",
    model: "Banarasi Drape Physics // World I",
    cost: -1,
    date: "2026-07-25T14:22:00Z",
    status: "Success",
  },
  {
    id: "gen_2",
    type: "Generation",
    model: "Tungsten Lighting Array // World II",
    cost: -2,
    date: "2026-07-24T09:15:00Z",
    status: "Success",
  },
  {
    id: "refill_1",
    type: "Subscription",
    model: "Institutional Pro Plan Allocation",
    cost: "+1000",
    date: "2026-07-01T00:00:00Z",
    status: "Completed",
  },
  {
    id: "gen_3",
    type: "Generation",
    model: "Volumetric Lookbook Render",
    cost: -1,
    date: "2026-06-29T18:45:00Z",
    status: "Success",
  },
  {
    id: "gen_4",
    type: "Generation",
    model: "Character Concept Latent Walk",
    cost: -3,
    date: "2026-06-28T11:20:00Z",
    status: "Failed (Refunded)",
  },
];

export default function UsageTab() {
  const { profile } = useAuth();
  const { playHoverSound, playFocusSound } = useTactileAudio();
  const [filter, setFilter] = useState<"all" | "generation" | "subscription">("all");

  const maxCredits = profile?.max_credits || 1000;
  const currentCredits =
    profile?.credit_balance !== undefined ? profile.credit_balance : 854;
  const consumedCredits = maxCredits - currentCredits;
  const percentage = Math.round((currentCredits / maxCredits) * 100);

  const filteredLogs = usageLog.filter((log) => {
    if (filter === "generation") return log.type === "Generation";
    if (filter === "subscription") return log.type === "Subscription";
    return true;
  });

  return (
    <div className="space-y-8">
      {/* Hero Metrics Row */}
      <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-8 pb-8 border-b border-slate-200/90">
        <div className="space-y-2">
          <div className="inline-flex items-center gap-2 px-2.5 py-0.5 rounded-full bg-slate-100 border border-slate-200 text-[10px] font-mono uppercase tracking-widest text-slate-700 font-bold">
            <Coins size={11} className="text-amber-600" />
            Live Compute Allocation
          </div>
          <div className="flex items-baseline gap-3">
            <span className="font-serif text-5xl sm:text-6xl text-[#0f172a] font-normal tracking-tight">
              {currentCredits}
            </span>
            <span className="text-sm font-semibold uppercase tracking-wider text-slate-600">
              Credits Remaining
            </span>
          </div>
          <p className="text-xs text-slate-600 font-light">
            Automatic computational refresh on{" "}
            <strong className="text-slate-900 font-semibold">August 1st, 2026</strong>.
          </p>
        </div>

        {/* Capacity Meter */}
        <div className="w-full lg:w-80 space-y-3 p-4 rounded-2xl bg-slate-50 border border-slate-200/90 shadow-2xs">
          <div className="flex justify-between text-xs font-semibold text-slate-800">
            <span className="flex items-center gap-1.5">
              <TrendingUp size={13} className="text-emerald-700" />
              Available Quota
            </span>
            <span className="font-mono text-slate-900">{percentage}%</span>
          </div>

          <div className="h-2.5 w-full bg-slate-200 rounded-full overflow-hidden p-[1px]">
            <div
              className="h-full bg-gradient-to-r from-emerald-600 to-teal-600 rounded-full transition-all duration-1000 ease-out shadow-[0_0_10px_rgba(16,185,129,0.4)]"
              style={{ width: `${percentage}%` }}
            />
          </div>

          <div className="flex justify-between text-[11px] font-mono text-slate-600 pt-0.5">
            <span>Burned: {consumedCredits}</span>
            <span>Limit: {maxCredits}</span>
          </div>
        </div>
      </div>

      {/* 3 Pillar Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="p-4 rounded-2xl bg-slate-50/90 border border-slate-200/80">
          <span className="text-[10px] font-mono uppercase tracking-widest text-slate-500 font-bold">
            Monthly Pool
          </span>
          <p className="font-serif text-2xl text-[#0f172a] font-medium mt-1">
            {maxCredits.toLocaleString()}{" "}
            <span className="text-xs font-sans text-slate-600 font-normal">credits</span>
          </p>
        </div>

        <div className="p-4 rounded-2xl bg-slate-50/90 border border-slate-200/80">
          <span className="text-[10px] font-mono uppercase tracking-widest text-slate-500 font-bold">
            Average Cost / Gen
          </span>
          <p className="font-serif text-2xl text-[#0f172a] font-medium mt-1">
            1.4{" "}
            <span className="text-xs font-sans text-slate-600 font-normal">units</span>
          </p>
        </div>

        <div className="p-4 rounded-2xl bg-slate-50/90 border border-slate-200/80">
          <span className="text-[10px] font-mono uppercase tracking-widest text-slate-500 font-bold">
            Cluster Reliability
          </span>
          <div className="flex items-center gap-2 mt-2">
            <span className="w-2 h-2 rounded-full bg-emerald-600" />
            <span className="text-xs font-semibold text-emerald-800">
              100% Operational
            </span>
          </div>
        </div>
      </div>

      {/* Cryptographic Activity Ledger */}
      <div className="space-y-4 pt-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-xl bg-slate-900 text-white shadow-xs">
              <Activity size={16} />
            </div>
            <div>
              <h3 className="font-serif text-xl text-[#0f172a] font-medium">
                Activity Ledger &amp; Audit Log
              </h3>
              <p className="text-xs text-slate-600 font-light">
                Verifiable cryptographic record of neural inference and monthly allocations.
              </p>
            </div>
          </div>

          {/* Filter Chips */}
          <div className="inline-flex items-center gap-1 p-1 rounded-xl bg-slate-100 border border-slate-200 text-xs">
            {(["all", "generation", "subscription"] as const).map((mode) => (
              <button
                key={mode}
                onClick={() => {
                  playFocusSound();
                  setFilter(mode);
                }}
                onMouseEnter={playHoverSound}
                className={`px-3 py-1.5 rounded-lg font-semibold capitalize transition-all ${
                  filter === mode
                    ? "bg-[#0f172a] text-white shadow-xs"
                    : "text-slate-600 hover:text-[#0f172a]"
                }`}
              >
                {mode === "all" ? "All Logs" : mode + "s"}
              </button>
            ))}
          </div>
        </div>

        {/* Ledger Table */}
        <div className="rounded-2xl border border-slate-200 overflow-hidden bg-white shadow-xs">
          <div className="grid grid-cols-12 gap-4 px-5 py-3.5 border-b border-slate-200 bg-slate-50 text-[10px] font-mono font-bold tracking-widest text-slate-600 uppercase">
            <div className="col-span-5 md:col-span-5">Event &amp; Workflow</div>
            <div className="col-span-3 md:col-span-3 hidden sm:block">Timestamp</div>
            <div className="col-span-4 md:col-span-2">Verification</div>
            <div className="col-span-3 md:col-span-2 text-right">Debit / Credit</div>
          </div>

          <div className="divide-y divide-slate-100">
            {filteredLogs.map((log) => {
              const isRefill = String(log.cost).startsWith("+");
              return (
                <div
                  key={log.id}
                  className="grid grid-cols-12 gap-4 px-5 py-4 items-center hover:bg-slate-50 transition-colors"
                >
                  <div className="col-span-5 md:col-span-5 flex items-center gap-3">
                    <div
                      className={`w-9 h-9 rounded-xl flex items-center justify-center shrink-0 shadow-xs ${
                        isRefill
                          ? "bg-emerald-100 text-emerald-800 border border-emerald-200"
                          : "bg-slate-100 text-slate-800 border border-slate-200"
                      }`}
                    >
                      {isRefill ? <Zap size={15} /> : <Activity size={15} />}
                    </div>
                    <div className="min-w-0">
                      <p className="text-xs sm:text-sm font-semibold text-[#0f172a] truncate">
                        {log.type}
                      </p>
                      <p className="text-xs text-slate-600 truncate font-light">
                        {log.model}
                      </p>
                    </div>
                  </div>

                  <div className="col-span-3 md:col-span-3 hidden sm:flex items-center gap-1.5 text-xs text-slate-600 font-mono">
                    <Clock size={12} className="text-slate-400" />
                    {new Date(log.date).toLocaleDateString(undefined, {
                      month: "short",
                      day: "numeric",
                      hour: "2-digit",
                      minute: "2-digit",
                    })}
                  </div>

                  <div className="col-span-4 md:col-span-2">
                    <span
                      className={`inline-flex items-center gap-1 text-[10px] px-2.5 py-0.5 rounded-full font-mono font-bold uppercase tracking-wider ${
                        log.status === "Success" || log.status === "Completed"
                          ? "bg-emerald-50 text-emerald-800 border border-emerald-200"
                          : "bg-slate-100 text-slate-700 border border-slate-200"
                      }`}
                    >
                      {log.status === "Success" && <CheckCircle2 size={10} />}
                      {log.status === "Completed" && <CheckCircle2 size={10} />}
                      {log.status.includes("Refunded") && <AlertCircle size={10} />}
                      {log.status}
                    </span>
                  </div>

                  <div className="col-span-3 md:col-span-2 text-right">
                    <span
                      className={`font-mono text-xs sm:text-sm font-bold ${
                        isRefill ? "text-emerald-700 font-extrabold" : "text-slate-800"
                      }`}
                    >
                      {log.cost}
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
