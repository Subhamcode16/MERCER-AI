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
      <div className="bg-gradient-to-br from-card to-muted/40 border border-border rounded-2xl p-6 md:p-8 relative overflow-hidden shadow-xs">
        {/* Decorative background element */}
        <div className="absolute top-0 right-0 -mr-16 -mt-16 w-64 h-64 bg-primary opacity-[0.05] rounded-full blur-3xl pointer-events-none" />
        
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 relative z-10">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <Sparkles size={16} className={currentTier === "PRO" ? "text-primary" : "text-muted-foreground"} />
              <span className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Current Plan</span>
            </div>
            <h2 className="text-3xl font-bold text-foreground tracking-tight">
              {currentTier === "PRO" ? "Pro Plan" : "Free Tier"}
            </h2>
            <p className="text-sm text-muted-foreground mt-2 max-w-sm">
              {currentTier === "PRO" 
                ? "You have full access to premium models and high-speed generation." 
                : "You are currently on the free tier. Upgrade to access premium models."}
            </p>
          </div>
          
          <div className="flex flex-col items-start md:items-end gap-3">
            <div className="text-left md:text-right">
              <p className="text-sm font-medium text-foreground">30-Day Cycle</p>
              <p className="text-xs text-muted-foreground">Renews on Aug 1st, 2026</p>
            </div>
            {currentTier !== "PRO" ? (
              <button className="bg-primary hover:bg-primary/90 text-primary-foreground text-sm font-bold px-6 py-2.5 rounded-lg transition-colors flex items-center gap-2 shadow-sm">
                Upgrade to Pro <ArrowRight size={14} />
              </button>
            ) : (
              <button className="bg-muted hover:bg-muted/80 text-foreground text-sm font-medium px-6 py-2.5 rounded-lg border border-border transition-colors">
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
            ? "border-primary/30 bg-card shadow-sm" 
            : "border-border bg-card/50 opacity-70"
        }`}>
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-foreground">Free</h3>
            <p className="text-[28px] font-bold text-foreground mt-2">$0<span className="text-sm font-normal text-muted-foreground">/mo</span></p>
          </div>
          
          <ul className="space-y-4">
            {[
              "100 Credits per month",
              "Standard generation speed",
              "Access to base models",
              "Community support"
            ].map((feature, i) => (
              <li key={i} className="flex items-start gap-3 text-sm text-muted-foreground">
                <Check size={16} className="text-muted-foreground/60 shrink-0 mt-0.5" />
                <span>{feature}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Pro Plan Card */}
        <div className={`border rounded-xl p-6 transition-all relative overflow-hidden ${
          currentTier === "PRO" 
            ? "border-primary/50 bg-card shadow-md" 
            : "border-border bg-card shadow-xs"
        }`}>
          {currentTier === "PRO" && (
             <div className="absolute top-0 inset-x-0 h-[2px] bg-gradient-to-r from-transparent via-primary to-transparent" />
          )}
          
          <div className="mb-6">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold text-foreground">Pro</h3>
              {currentTier !== "PRO" && (
                <span className="text-[10px] bg-primary text-primary-foreground px-2 py-0.5 rounded-full font-bold uppercase tracking-wider">Recommended</span>
              )}
            </div>
            <p className="text-[28px] font-bold text-primary mt-2">$29<span className="text-sm font-normal text-muted-foreground">/mo</span></p>
          </div>
          
          <ul className="space-y-4">
            {[
              "1000 Credits per month",
              "Priority generation speed",
              "Access to all premium models",
              "Private generations",
              "Commercial license"
            ].map((feature, i) => (
              <li key={i} className="flex items-start gap-3 text-sm text-foreground">
                <Check size={16} className="text-primary shrink-0 mt-0.5" />
                <span>{feature}</span>
              </li>
            ))}
          </ul>
        </div>
        
      </div>
      
      {/* Payment Method Stub */}
      {currentTier === "PRO" && (
        <div className="border border-border bg-card rounded-xl p-6 flex items-center justify-between shadow-xs">
          <div className="flex items-center gap-4">
            <div className="w-12 h-8 bg-muted rounded flex items-center justify-center">
              <CreditCard size={18} className="text-muted-foreground" />
            </div>
            <div>
              <p className="text-sm font-medium text-foreground">•••• •••• •••• 4242</p>
              <p className="text-xs text-muted-foreground">Expires 12/28</p>
            </div>
          </div>
          <button className="text-xs font-medium text-muted-foreground hover:text-foreground transition-colors">
            Update
          </button>
        </div>
      )}
      
    </div>
  );
}
