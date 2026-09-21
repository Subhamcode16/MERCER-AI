"use client";

import React, { useState } from "react";
import {
  Activity,
  Clock,
  Zap,
  Coins,
  CheckCircle2,
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
    <div className="space-y-8 font-sans">
      
      {/* Hero Quota Overview */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6 pb-6 border-b border-[var(--line)]">
        <div className="space-y-1">
          <span className="text-xs font-semibold uppercase tracking-wider text-[var(--muted)] font-mono">
            Active Compute Allocation
          </span>
          <div className="flex items-baseline gap-2">
            <span className="font-serif text-4xl sm:text-5xl text-[var(--ink)] font-normal tracking-tight">
              {currentCredits}
            </span>
            <span className="text-xs font-semibold text-[var(--muted)] font-mono">
              / {maxCredits} Credits
            </span>
          </div>
          <p className="text-xs text-[var(--muted)]">
            Refills on the 1st of each calendar month.
          </p>
        </div>

        {/* Progress Bar Block */}
        <div className="w-full sm:w-72 space-y-2 p-4 rounded-xl bg-[var(--soft)] border border-[var(--line)]">
          <div className="flex justify-between items-center text-xs font-medium">
            <span className="text-[var(--ink)]">Monthly Capacity</span>
            <span className="font-mono text-emerald-500 font-bold">{percentage}%</span>
          </div>

          <div className="w-full h-2 rounded-full bg-[var(--paper)] overflow-hidden p-0.5 border border-[var(--line)]">
            <div
              className="h-full rounded-full bg-emerald-500 transition-all duration-700 ease-out"
              style={{ width: `${percentage}%` }}
            />
          </div>

          <div className="flex justify-between items-center text-[10px] font-mono text-[var(--muted)]">
            <span>{consumedCredits} consumed</span>
            <span>{currentCredits} available</span>
          </div>
        </div>
      </div>

      {/* Activity Table */}
      <div className="space-y-3">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <h3 className="font-serif text-lg text-[var(--ink)] font-medium">
            Recent Usage Activity
          </h3>

          {/* Filter Chips */}
          <div className="inline-flex items-center gap-1 p-1 bg-[var(--soft)] rounded-xl border border-[var(--line)] text-xs">
            {(["all", "generation", "subscription"] as const).map((mode) => (
              <button
                key={mode}
                type="button"
                onClick={() => {
                  playFocusSound();
                  setFilter(mode);
                }}
                onMouseEnter={playHoverSound}
                className={`px-3 py-1 rounded-lg font-semibold capitalize transition-all ${
                  filter === mode
                    ? "bg-[var(--surface)] text-[var(--ink)] shadow-2xs border border-[var(--line)]"
                    : "text-[var(--muted)] hover:text-[var(--ink)]"
                }`}
              >
                {mode === "all" ? "All" : mode + "s"}
              </button>
            ))}
          </div>
        </div>

        {/* Table */}
        <div className="rounded-xl border border-[var(--line)] overflow-hidden bg-[var(--surface)]">
          <div className="grid grid-cols-12 gap-3 px-4 py-2.5 border-b border-[var(--line)] bg-[var(--soft)] text-[10px] font-mono font-bold tracking-widest text-[var(--muted)] uppercase">
            <div className="col-span-6">Event</div>
            <div className="col-span-3 hidden sm:block">Date</div>
            <div className="col-span-3 text-right">Credits</div>
          </div>

          <div className="divide-y divide-[var(--line)]">
            {filteredLogs.map((log) => {
              const isRefill = String(log.cost).startsWith("+");
              return (
                <div
                  key={log.id}
                  className="grid grid-cols-12 gap-3 px-4 py-3 items-center hover:bg-[var(--soft)]/50 transition-colors"
                >
                  <div className="col-span-6 flex items-center gap-2.5">
                    <div
                      className={`w-6 h-6 rounded-md flex items-center justify-center shrink-0 text-xs font-mono font-bold ${
                        isRefill
                          ? "bg-[var(--soft)] text-emerald-500 border border-[var(--line)]"
                          : "bg-[var(--soft)] text-[var(--ink)] border border-[var(--line)]"
                      }`}
                    >
                      {isRefill ? "+" : "↓"}
                    </div>
                    <div className="min-w-0">
                      <p className="text-xs font-semibold text-[var(--ink)] truncate">
                        {log.type}
                      </p>
                      <p className="text-[11px] text-[var(--muted)] truncate font-mono">
                        {log.model}
                      </p>
                    </div>
                  </div>

                  <div className="col-span-3 hidden sm:flex items-center gap-1 text-xs text-[var(--muted)] font-mono">
                    <Clock size={11} />
                    {new Date(log.date).toLocaleDateString(undefined, {
                      month: "short",
                      day: "numeric",
                    })}
                  </div>

                  <div className="col-span-6 sm:col-span-3 text-right">
                    <span
                      className={`font-mono text-xs font-bold ${
                        isRefill ? "text-emerald-500" : "text-[var(--ink)]"
                      }`}
                    >
                      {log.cost} Credits
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
