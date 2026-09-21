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
      <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-8 pb-6 border-b border-[var(--line)]">
        <div className="space-y-2">
          <div className="inline-flex items-center gap-2 px-2.5 py-0.5 rounded-full bg-[var(--soft)] border border-[var(--line)] text-[10px] font-mono uppercase tracking-widest text-[var(--ink)] font-bold">
            <Coins size={11} className="text-[var(--activity)]" />
            Live Compute Allocation
          </div>
          <div className="flex items-baseline gap-3">
            <span className="font-serif text-5xl sm:text-6xl text-[var(--ink)] font-normal tracking-tight">
              {currentCredits}
            </span>
            <span className="text-xs font-semibold uppercase tracking-wider text-[var(--muted)]">
              Credits Remaining
            </span>
          </div>
          <p className="text-xs text-[var(--muted)] font-light">
            Automatic computational cycle refresh on{" "}
            <strong className="text-[var(--ink)] font-semibold">August 1st, 2026</strong>.
          </p>
        </div>

        {/* Capacity Meter */}
        <div className="w-full lg:w-80 space-y-3 p-4 rounded-2xl bg-[var(--paper)] border border-[var(--line)] shadow-2xs">
          <div className="flex justify-between text-xs font-semibold text-[var(--ink)]">
            <span className="flex items-center gap-1.5">
              <TrendingUp size={13} className="text-[var(--activity)]" />
              Available Quota
            </span>
            <span className="font-mono text-[var(--ink)]">{percentage}%</span>
          </div>

          <div className="h-2 w-full bg-[var(--soft)] rounded-full overflow-hidden p-[1px]">
            <div
              className="h-full bg-[var(--activity)] rounded-full transition-all duration-1000 ease-out"
              style={{ width: `${percentage}%` }}
            />
          </div>

          <div className="flex justify-between text-[11px] font-mono text-[var(--muted)] pt-0.5">
            <span>Burned: {consumedCredits}</span>
            <span>Limit: {maxCredits}</span>
          </div>
        </div>
      </div>

      {/* 3 Pillar Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="p-4 rounded-xl bg-[var(--paper)] border border-[var(--line)]">
          <span className="text-[10px] font-mono uppercase tracking-widest text-[var(--muted)] font-bold">
            Monthly Pool
          </span>
          <p className="font-serif text-2xl text-[var(--ink)] font-medium mt-1">
            {maxCredits.toLocaleString()}{" "}
            <span className="text-xs font-sans text-[var(--muted)] font-normal">credits</span>
          </p>
        </div>

        <div className="p-4 rounded-xl bg-[var(--paper)] border border-[var(--line)]">
          <span className="text-[10px] font-mono uppercase tracking-widest text-[var(--muted)] font-bold">
            Average Cost / Gen
          </span>
          <p className="font-serif text-2xl text-[var(--ink)] font-medium mt-1">
            1.4{" "}
            <span className="text-xs font-sans text-[var(--muted)] font-normal">units</span>
          </p>
        </div>

        <div className="p-4 rounded-xl bg-[var(--paper)] border border-[var(--line)]">
          <span className="text-[10px] font-mono uppercase tracking-widest text-[var(--muted)] font-bold">
            Cluster Reliability
          </span>
          <div className="flex items-center gap-2 mt-2">
            <span className="w-2 h-2 rounded-full bg-[var(--activity)]" />
            <span className="text-xs font-semibold text-[var(--activity)]">
              100% Operational
            </span>
          </div>
        </div>
      </div>

      {/* Cryptographic Activity Ledger */}
      <div className="space-y-4 pt-2">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-lg bg-[var(--soft)] text-[var(--ink)]">
              <Activity size={15} />
            </div>
            <div>
              <h3 className="font-serif text-lg sm:text-xl text-[var(--ink)] font-medium">
                Activity Ledger &amp; Audit Log
              </h3>
              <p className="text-xs text-[var(--muted)] font-light">
                Verifiable cryptographic record of neural inference and allocations.
              </p>
            </div>
          </div>

          {/* Filter Chips */}
          <div className="inline-flex items-center gap-1 p-1 rounded-xl bg-[var(--soft)] border border-[var(--line)] text-xs">
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
                    ? "bg-[var(--surface)] text-[var(--ink)] shadow-2xs"
                    : "text-[var(--muted)] hover:text-[var(--ink)]"
                }`}
              >
                {mode === "all" ? "All Logs" : mode + "s"}
              </button>
            ))}
          </div>
        </div>

        {/* Ledger Table */}
        <div className="rounded-xl border border-[var(--line)] overflow-hidden bg-[var(--surface)]">
          <div className="grid grid-cols-12 gap-4 px-5 py-3 border-b border-[var(--line)] bg-[var(--soft)]/50 text-[10px] font-mono font-bold tracking-widest text-[var(--muted)] uppercase">
            <div className="col-span-5 md:col-span-5">Event &amp; Workflow</div>
            <div className="col-span-3 md:col-span-3 hidden sm:block">Timestamp</div>
            <div className="col-span-4 md:col-span-2">Verification</div>
            <div className="col-span-3 md:col-span-2 text-right">Debit / Credit</div>
          </div>

          <div className="divide-y divide-[var(--line)]">
            {filteredLogs.map((log) => {
              const isRefill = String(log.cost).startsWith("+");
              return (
                <div
                  key={log.id}
                  className="grid grid-cols-12 gap-4 px-5 py-3.5 items-center hover:bg-[var(--soft)]/30 transition-colors"
                >
                  <div className="col-span-5 md:col-span-5 flex items-center gap-3">
                    <div
                      className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 ${
                        isRefill
                          ? "bg-[var(--soft)] text-[var(--activity)]"
                          : "bg-[var(--soft)] text-[var(--ink)]"
                      }`}
                    >
                      {isRefill ? <Zap size={14} /> : <Activity size={14} />}
                    </div>
                    <div className="min-w-0">
                      <p className="text-xs sm:text-sm font-semibold text-[var(--ink)] truncate">
                        {log.type}
                      </p>
                      <p className="text-xs text-[var(--muted)] truncate font-light">
                        {log.model}
                      </p>
                    </div>
                  </div>

                  <div className="col-span-3 md:col-span-3 hidden sm:flex items-center gap-1.5 text-xs text-[var(--muted)] font-mono">
                    <Clock size={12} />
                    {new Date(log.date).toLocaleDateString(undefined, {
                      month: "short",
                      day: "numeric",
                      hour: "2-digit",
                      minute: "2-digit",
                    })}
                  </div>

                  <div className="col-span-4 md:col-span-2">
                    <span
                      className={`inline-flex items-center gap-1 text-[10px] px-2 py-0.5 rounded-full font-mono font-bold uppercase tracking-wider ${
                        log.status === "Success" || log.status === "Completed"
                          ? "bg-[var(--soft)] text-[var(--activity)] border border-[var(--line)]"
                          : "bg-[var(--soft)] text-[var(--muted)] border border-[var(--line)]"
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
                        isRefill ? "text-[var(--activity)]" : "text-[var(--ink)]"
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
