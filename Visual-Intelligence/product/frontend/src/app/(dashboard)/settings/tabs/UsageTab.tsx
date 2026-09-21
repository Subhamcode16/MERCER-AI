"use client";

import React, { useState } from "react";
import {
  Activity,
  Clock,
  Zap,
  Coins,
  CheckCircle2,
  ArrowUpRight,
  Filter,
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
    <div className="space-y-10 font-sans pb-4">
      
      {/* 1. Typographic Quota Balance & Allocation Bar */}
      <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-8 pb-7 border-b border-[#e3dfd4]">
        <div className="space-y-1">
          <div className="text-[10px] font-mono uppercase tracking-widest text-[#5e6d68] font-bold">
            01 // Active Compute Pool Allocation
          </div>
          <div className="flex items-baseline gap-3">
            <span className="font-serif text-5xl sm:text-6xl text-[#0f1419] font-normal tracking-tight">
              {currentCredits}
            </span>
            <div className="space-y-0.5">
              <div className="text-xs font-semibold uppercase tracking-wider text-[#0f1419] font-mono">
                / {maxCredits} Units
              </div>
              <div className="text-[11px] text-[#5e6d68]">
                Auto-refills on 1st of every month
              </div>
            </div>
          </div>
        </div>

        {/* Precision Progress Track */}
        <div className="w-full lg:w-96 space-y-2.5">
          <div className="flex justify-between items-center text-xs">
            <span className="text-[#0f1419] font-medium font-sans">Pool Utilization</span>
            <span className="font-mono text-[#059669] font-bold">{percentage}% Available</span>
          </div>

          <div className="w-full h-2 rounded-full bg-[#f0ebe1] overflow-hidden p-0.5 border border-[#e3dfd4]">
            <div
              className="h-full rounded-full bg-[#059669] transition-all duration-700 ease-out"
              style={{ width: `${percentage}%` }}
            />
          </div>

          <div className="flex justify-between items-center text-[10px] font-mono text-[#5e6d68]">
            <span>{consumedCredits} consumed this cycle</span>
            <span>0 throttled inferences</span>
          </div>
        </div>
      </div>

      {/* 2. Architectural 3-Column Metric Strip (Flush Dividers) */}
      <div className="grid grid-cols-1 sm:grid-cols-3 divide-y sm:divide-y-0 sm:divide-x divide-[#e3dfd4] border-y border-[#e3dfd4] py-4 -my-2">
        <div className="px-4 py-2 sm:py-0 first:pl-0">
          <span className="text-[10px] font-mono uppercase tracking-widest text-[#5e6d68] font-bold">
            Monthly Quota Floor
          </span>
          <p className="text-2xl font-serif text-[#0f1419] font-medium mt-1">
            {maxCredits} Credits
          </p>
          <span className="text-[11px] text-[#5e6d68] font-mono">Tier-1 Institutional allocation</span>
        </div>

        <div className="px-4 py-2 sm:py-0">
          <span className="text-[10px] font-mono uppercase tracking-widest text-[#5e6d68] font-bold">
            Average Burn Rate
          </span>
          <p className="text-2xl font-serif text-[#0f1419] font-medium mt-1">
            1.4 Credits
          </p>
          <span className="text-[11px] text-[#5e6d68] font-mono">Per volumetric render pass</span>
        </div>

        <div className="px-4 py-2 sm:py-0 last:pr-0">
          <span className="text-[10px] font-mono uppercase tracking-widest text-[#5e6d68] font-bold">
            Cluster Reliability
          </span>
          <p className="text-2xl font-serif text-[#059669] font-medium mt-1 flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-[#059669] animate-pulse" />
            100.0%
          </p>
          <span className="text-[11px] text-[#5e6d68] font-mono">US-East routing active</span>
        </div>
      </div>

      {/* 3. Cryptographic Activity Ledger Table */}
      <div className="space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="text-[10px] font-mono uppercase tracking-widest text-[#5e6d68] font-bold">
              02 // Cryptographic Activity Ledger
            </div>
            <h3 className="font-serif text-xl text-[#0f1419] font-medium mt-0.5">
              Inference &amp; Refill Audit Log
            </h3>
          </div>

          {/* Filter Chips */}
          <div className="inline-flex items-center gap-1 p-1 bg-[#f0ebe1] rounded-xl border border-[#e3dfd4] text-xs">
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
                    ? "bg-white text-[#0f1419] shadow-2xs border border-[#e3dfd4]"
                    : "text-[#5e6d68] hover:text-[#0f1419]"
                }`}
              >
                {mode === "all" ? "All Logs" : mode + "s"}
              </button>
            ))}
          </div>
        </div>

        {/* Ledger Table */}
        <div className="rounded-xl border border-[#e3dfd4] overflow-hidden bg-white">
          <div className="grid grid-cols-12 gap-4 px-5 py-3 border-b border-[#e3dfd4] bg-[#faf8f4] text-[10px] font-mono font-bold tracking-widest text-[#5e6d68] uppercase">
            <div className="col-span-6 md:col-span-5">Event &amp; Model Target</div>
            <div className="col-span-3 md:col-span-3 hidden sm:block">Timestamp</div>
            <div className="col-span-3 md:col-span-2">Verification</div>
            <div className="col-span-3 md:col-span-2 text-right">Debit / Credit</div>
          </div>

          <div className="divide-y divide-[#e3dfd4]">
            {filteredLogs.map((log) => {
              const isRefill = String(log.cost).startsWith("+");
              return (
                <div
                  key={log.id}
                  className="grid grid-cols-12 gap-4 px-5 py-3.5 items-center hover:bg-[#faf8f4]/60 transition-colors"
                >
                  <div className="col-span-6 md:col-span-5 flex items-center gap-3">
                    <div
                      className={`w-7 h-7 rounded-lg flex items-center justify-center shrink-0 text-xs font-mono font-bold ${
                        isRefill
                          ? "bg-[#f0ebe1] text-[#059669] border border-[#e3dfd4]"
                          : "bg-[#f0ebe1] text-[#0f1419] border border-[#e3dfd4]"
                      }`}
                    >
                      {isRefill ? "+" : "↓"}
                    </div>
                    <div className="min-w-0">
                      <p className="text-xs font-semibold text-[#0f1419] truncate font-sans">
                        {log.type}
                      </p>
                      <p className="text-[11px] text-[#5e6d68] truncate font-mono">
                        {log.model}
                      </p>
                    </div>
                  </div>

                  <div className="col-span-3 md:col-span-3 hidden sm:flex items-center gap-1.5 text-xs text-[#5e6d68] font-mono">
                    <Clock size={11} className="text-[#5e6d68]" />
                    {new Date(log.date).toLocaleDateString(undefined, {
                      month: "short",
                      day: "numeric",
                      hour: "2-digit",
                      minute: "2-digit",
                    })}
                  </div>

                  <div className="col-span-3 md:col-span-2">
                    <span
                      className={`inline-flex items-center gap-1 text-[10px] px-2 py-0.5 rounded-md font-mono font-bold uppercase tracking-wider ${
                        log.status === "Success" || log.status === "Completed"
                          ? "bg-[#f0ebe1] text-[#059669] border border-[#e3dfd4]"
                          : "bg-[#f0ebe1] text-[#5e6d68] border border-[#e3dfd4]"
                      }`}
                    >
                      {log.status === "Success" && <CheckCircle2 size={9} />}
                      {log.status}
                    </span>
                  </div>

                  <div className="col-span-3 md:col-span-2 text-right">
                    <span
                      className={`font-mono text-xs font-bold ${
                        isRefill ? "text-[#059669]" : "text-[#0f1419]"
                      }`}
                    >
                      {log.cost} Units
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
