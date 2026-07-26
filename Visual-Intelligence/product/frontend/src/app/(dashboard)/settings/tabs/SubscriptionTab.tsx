"use client";

import React from "react";
import { Check, Sparkles, CreditCard, ArrowRight } from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";

export default function SubscriptionTab() {
  const { profile } = useAuth();
  const currentTier = profile?.tier || "FREE";
  
  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      
      {/* Current Plan Banner */}
      <div className="bg-gradient-to-br from-[#1A1A1A] to-[#0A0A0A] border border-white/10 rounded-2xl p-6 md:p-8 relative overflow-hidden">
        {/* Decorative background element */}
        <div className="absolute top-0 right-0 -mr-16 -mt-16 w-64 h-64 bg-[#E1D4C0] opacity-[0.03] rounded-full blur-3xl pointer-events-none" />
        
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 relative z-10">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <Sparkles size={16} className={currentTier === "PRO" ? "text-[#E1D4C0]" : "text-white/40"} />
              <span className="text-xs font-semibold uppercase tracking-wider text-white/50">Current Plan</span>
            </div>
            <h2 className="text-3xl font-bold text-white tracking-tight">
              {currentTier === "PRO" ? "Pro Plan" : "Free Tier"}
            </h2>
            <p className="text-sm text-white/50 mt-2 max-w-sm">
              {currentTier === "PRO" 
                ? "You have full access to premium models and high-speed generation." 
                : "You are currently on the free tier. Upgrade to access premium models."}
            </p>
          </div>
          
          <div className="flex flex-col items-start md:items-end gap-3">
            <div className="text-left md:text-right">
              <p className="text-sm font-medium text-white/90">30-Day Cycle</p>
              <p className="text-xs text-white/40">Renews on Aug 1st, 2026</p>
            </div>
            {currentTier !== "PRO" ? (
              <button className="bg-[#E1D4C0] hover:bg-white text-black text-sm font-bold px-6 py-2.5 rounded-lg transition-colors flex items-center gap-2">
                Upgrade to Pro <ArrowRight size={14} />
              </button>
            ) : (
              <button className="bg-white/10 hover:bg-white/15 text-white text-sm font-medium px-6 py-2.5 rounded-lg border border-white/5 transition-colors">
                Manage Billing
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Feature Comparison */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        {/* Free Plan Card */}
        <div className={`border rounded-xl p-6 transition-all ${
          currentTier === "FREE" 
            ? "border-white/20 bg-[#111111] shadow-[0_0_20px_rgba(0,0,0,0.5)]" 
            : "border-white/5 bg-transparent opacity-70"
        }`}>
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-white">Free</h3>
            <p className="text-[28px] font-bold text-white/90 mt-2">$0<span className="text-sm font-normal text-white/40">/mo</span></p>
          </div>
          
          <ul className="space-y-4">
            {[
              "100 Credits per month",
              "Standard generation speed",
              "Access to base models",
              "Community support"
            ].map((feature, i) => (
              <li key={i} className="flex items-start gap-3 text-sm text-white/70">
                <Check size={16} className="text-white/30 shrink-0 mt-0.5" />
                <span>{feature}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Pro Plan Card */}
        <div className={`border rounded-xl p-6 transition-all relative overflow-hidden ${
          currentTier === "PRO" 
            ? "border-[#E1D4C0]/30 bg-[#111111] shadow-[0_0_30px_rgba(225,212,192,0.05)]" 
            : "border-white/5 bg-[#0A0A0A]"
        }`}>
          {currentTier === "PRO" && (
             <div className="absolute top-0 inset-x-0 h-[2px] bg-gradient-to-r from-transparent via-[#E1D4C0] to-transparent" />
          )}
          
          <div className="mb-6">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold text-white">Pro</h3>
              {currentTier !== "PRO" && (
                <span className="text-[10px] bg-[#E1D4C0] text-black px-2 py-0.5 rounded-full font-bold uppercase tracking-wider">Recommended</span>
              )}
            </div>
            <p className="text-[28px] font-bold text-[#E1D4C0] mt-2">$29<span className="text-sm font-normal text-white/40">/mo</span></p>
          </div>
          
          <ul className="space-y-4">
            {[
              "1000 Credits per month",
              "Priority generation speed",
              "Access to all premium models",
              "Private generations",
              "Commercial license"
            ].map((feature, i) => (
              <li key={i} className="flex items-start gap-3 text-sm text-white/90">
                <Check size={16} className="text-[#E1D4C0] shrink-0 mt-0.5" />
                <span>{feature}</span>
              </li>
            ))}
          </ul>
        </div>
        
      </div>
      
      {/* Payment Method Stub */}
      {currentTier === "PRO" && (
        <div className="border border-white/5 bg-[#111111]/50 rounded-xl p-6 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="w-12 h-8 bg-white/10 rounded flex items-center justify-center">
              <CreditCard size={18} className="text-white/60" />
            </div>
            <div>
              <p className="text-sm font-medium text-white">•••• •••• •••• 4242</p>
              <p className="text-xs text-white/40">Expires 12/28</p>
            </div>
          </div>
          <button className="text-xs font-medium text-white/50 hover:text-white transition-colors">
            Update
          </button>
        </div>
      )}
      
    </div>
  );
}
