"use client";

import React from "react";
import { Activity, Clock, Zap } from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";

// Mock data for the ledger
const usageLog = [
  { id: "gen_1", type: "Generation", model: "World I", cost: -1, date: "2026-07-25T14:22:00Z", status: "Success" },
  { id: "gen_2", type: "Generation", model: "World II", cost: -2, date: "2026-07-24T09:15:00Z", status: "Success" },
  { id: "refill", type: "Subscription", model: "Pro Plan", cost: "+1000", date: "2026-07-01T00:00:00Z", status: "Completed" },
  { id: "gen_3", type: "Generation", model: "World I", cost: -1, date: "2026-06-29T18:45:00Z", status: "Success" },
  { id: "gen_4", type: "Generation", model: "Character Concept", cost: -3, date: "2026-06-28T11:20:00Z", status: "Failed (Refunded)" },
];

export default function UsageTab() {
  const { profile } = useAuth();
  
  // Real values from DB profile
  const maxCredits = profile?.max_credits || 1000;
  const currentCredits = profile?.credit_balance !== undefined ? profile.credit_balance : 854;
  
  const percentage = Math.round((currentCredits / maxCredits) * 100);

  return (
    <div className="space-y-10 animate-in fade-in duration-500">
      
      {/* Credit Summary Block */}
      <div className="bg-card border border-border rounded-2xl p-6 md:p-8 flex flex-col md:flex-row items-start md:items-center justify-between gap-8 shadow-xs">
        <div>
          <h2 className="text-4xl font-bold tracking-tight text-foreground flex items-baseline gap-2">
            {currentCredits} <span className="text-base font-normal text-muted-foreground tracking-wide uppercase">Credits Remaining</span>
          </h2>
          <p className="text-sm text-muted-foreground mt-2">Your next billing cycle resets on August 1st, 2026.</p>
        </div>
        
        <div className="w-full md:w-64 space-y-3">
          <div className="flex justify-between text-xs font-medium text-muted-foreground">
            <span>Usage</span>
            <span>{maxCredits - currentCredits} / {maxCredits}</span>
          </div>
          <div className="h-2 w-full bg-muted rounded-full overflow-hidden">
            <div 
              className="h-full bg-primary rounded-full transition-all duration-1000 ease-out"
              style={{ width: `${100 - percentage}%` }}
            />
          </div>
        </div>
      </div>

      {/* Consumption Ledger */}
      <div className="space-y-4">
        <div className="flex items-center gap-2 mb-2">
          <Activity size={16} className="text-primary" />
          <h3 className="text-lg font-semibold text-foreground">Activity Ledger</h3>
        </div>
        
        <div className="border border-border rounded-xl overflow-hidden bg-card shadow-xs">
          <div className="grid grid-cols-12 gap-4 p-4 border-b border-border text-xs font-semibold tracking-wider text-muted-foreground uppercase bg-muted/50">
            <div className="col-span-5 md:col-span-4">Event</div>
            <div className="col-span-4 hidden md:block">Date</div>
            <div className="col-span-4 md:col-span-2">Status</div>
            <div className="col-span-3 md:col-span-2 text-right">Credits</div>
          </div>
          
          <div className="divide-y divide-border">
            {usageLog.map((log) => (
              <div key={log.id} className="grid grid-cols-12 gap-4 p-4 items-center hover:bg-muted/30 transition-colors">
                <div className="col-span-5 md:col-span-4 flex items-center gap-3">
                  <div className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 ${log.type === 'Subscription' ? 'bg-primary/10 text-primary' : 'bg-muted text-foreground'}`}>
                    {log.type === 'Subscription' ? <Zap size={14} /> : <Activity size={14} />}
                  </div>
                  <div className="min-w-0">
                    <p className="text-sm font-medium text-foreground truncate">{log.type}</p>
                    <p className="text-xs text-muted-foreground truncate">{log.model}</p>
                  </div>
                </div>
                
                <div className="col-span-4 hidden md:flex items-center gap-2 text-sm text-muted-foreground">
                  <Clock size={12} />
                  {new Date(log.date).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' })}
                </div>
                
                <div className="col-span-4 md:col-span-2">
                  <span className={`text-[10px] px-2 py-0.5 rounded-full font-medium tracking-wide ${
                    log.status === 'Success' || log.status === 'Completed' 
                      ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20' 
                      : 'bg-muted text-muted-foreground border border-border'
                  }`}>
                    {log.status}
                  </span>
                </div>
                
                <div className="col-span-3 md:col-span-2 text-right">
                  <span className={`text-sm font-bold ${log.cost.toString().startsWith('+') ? 'text-primary' : 'text-foreground'}`}>
                    {log.cost}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
      
    </div>
  );
}
