"use client";

import React, { useEffect, useState } from "react";
import { IntelligenceAPI, StrategicScenario, StrategicRecommendation } from "@/lib/intelligence-api";
import { Sparkles, Compass, Eye, BookOpen, AlertCircle, Compass as ExploreIcon, CheckCircle, RefreshCcw, ArrowRight, ShieldCheck, Zap } from "lucide-react";

export type ForesightMode = "OBSERVE" | "UNDERSTAND" | "CHALLENGE" | "EXPLORE" | "DECIDE" | "LEARN";

export default function ForesightWorkspacePage() {
  const [activeMode, setActiveMode] = useState<ForesightMode>("EXPLORE");
  const [scenarios, setScenarios] = useState<Record<string, StrategicScenario>>({});
  const [challengeNotes, setChallengeNotes] = useState<string>("");
  const [isChallenged, setIsChallenged] = useState<boolean>(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadScenarios() {
      const matrix = await IntelligenceAPI.getForesightScenarios("TENANT-LUXE", "Minimalist Luxe Shift");
      setScenarios(matrix);
      setLoading(false);
    }
    loadScenarios();
  }, []);

  const handleChallenge = async () => {
    if (!challengeNotes) return;
    await IntelligenceAPI.challengeRecommendation("REC-ASYM-01", challengeNotes);
    setIsChallenged(true);
  };

  return (
    <div className="flex-1 space-y-8 p-8 max-w-7xl mx-auto text-foreground bg-background">
      {/* Header Banner */}
      <div className="flex items-center justify-between border-b border-border pb-6">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="px-2.5 py-0.5 rounded text-[10px] font-mono uppercase bg-purple-500/10 text-purple-600 dark:text-purple-300 border border-purple-500/20">
              Phase 29 Foresight Engine
            </span>
            <span className="text-xs text-muted-foreground font-mono">Scope: GLOBAL_FASHION</span>
          </div>
          <h1 className="text-3xl font-serif tracking-tight text-foreground flex items-center gap-3">
            <Sparkles className="w-7 h-7 text-purple-500" />
            Strategic Foresight Workspace
          </h1>
          <p className="text-sm text-muted-foreground mt-1">
            Explore 5-scenario futures, inspect counterfactual unknowns, challenge assumptions, and authorize governed experiments.
          </p>
        </div>
      </div>

      {/* 6-Mode Command Selector Bar */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2 bg-card p-1.5 rounded-xl border border-border font-mono text-xs shadow-xs">
        <button
          onClick={() => setActiveMode("OBSERVE")}
          className={`flex items-center justify-center gap-2 py-2.5 px-3 rounded-lg transition-all ${
            activeMode === "OBSERVE" ? "bg-purple-600 text-white font-semibold shadow-md" : "text-muted-foreground hover:text-foreground"
          }`}
        >
          <Eye className="w-3.5 h-3.5" />
          <span>1. OBSERVE</span>
        </button>

        <button
          onClick={() => setActiveMode("UNDERSTAND")}
          className={`flex items-center justify-center gap-2 py-2.5 px-3 rounded-lg transition-all ${
            activeMode === "UNDERSTAND" ? "bg-purple-600 text-white font-semibold shadow-md" : "text-muted-foreground hover:text-foreground"
          }`}
        >
          <BookOpen className="w-3.5 h-3.5" />
          <span>2. UNDERSTAND</span>
        </button>

        <button
          onClick={() => setActiveMode("CHALLENGE")}
          className={`flex items-center justify-center gap-2 py-2.5 px-3 rounded-lg transition-all ${
            activeMode === "CHALLENGE" ? "bg-purple-600 text-white font-semibold shadow-md" : "text-muted-foreground hover:text-foreground"
          }`}
        >
          <AlertCircle className="w-3.5 h-3.5" />
          <span>3. CHALLENGE</span>
        </button>

        <button
          onClick={() => setActiveMode("EXPLORE")}
          className={`flex items-center justify-center gap-2 py-2.5 px-3 rounded-lg transition-all ${
            activeMode === "EXPLORE" ? "bg-purple-600 text-white font-semibold shadow-md" : "text-muted-foreground hover:text-foreground"
          }`}
        >
          <ExploreIcon className="w-3.5 h-3.5" />
          <span>4. EXPLORE</span>
        </button>

        <button
          onClick={() => setActiveMode("DECIDE")}
          className={`flex items-center justify-center gap-2 py-2.5 px-3 rounded-lg transition-all ${
            activeMode === "DECIDE" ? "bg-purple-600 text-white font-semibold shadow-md" : "text-muted-foreground hover:text-foreground"
          }`}
        >
          <CheckCircle className="w-3.5 h-3.5" />
          <span>5. DECIDE</span>
        </button>

        <button
          onClick={() => setActiveMode("LEARN")}
          className={`flex items-center justify-center gap-2 py-2.5 px-3 rounded-lg transition-all ${
            activeMode === "LEARN" ? "bg-purple-600 text-white font-semibold shadow-md" : "text-muted-foreground hover:text-foreground"
          }`}
        >
          <RefreshCcw className="w-3.5 h-3.5" />
          <span>6. LEARN</span>
        </button>
      </div>

      {/* Mode Content: EXPLORE (5-Scenario Matrix) */}
      {activeMode === "EXPLORE" && (
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-foreground font-serif">
              Mandatory 5-Scenario Comparison Matrix: <span className="text-purple-600 dark:text-purple-300">Minimalist Luxe Shift</span>
            </h2>
            <span className="text-xs font-mono text-muted-foreground">Bounded Likelihood Preserved</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-5 gap-4 font-mono text-xs">
            {/* Baseline */}
            <div className="bg-card border border-border hover:border-primary/40 transition-all rounded-xl p-4 flex flex-col justify-between space-y-3 shadow-xs">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="px-2 py-0.5 rounded text-[10px] bg-muted text-foreground border border-border font-semibold">
                    BASELINE
                  </span>
                  <span className="text-muted-foreground">40% Likelihood</span>
                </div>
                <div className="font-semibold text-foreground text-sm mb-1">{scenarios.BASELINE?.title}</div>
                <p className="text-muted-foreground leading-relaxed text-[11px] font-sans">
                  {scenarios.BASELINE?.description}
                </p>
              </div>
              <div className="pt-3 border-t border-border space-y-1 text-[10px]">
                <div className="text-muted-foreground">Leading Indicator:</div>
                <div className="text-emerald-600 dark:text-emerald-400 font-semibold">{scenarios.BASELINE?.leading_indicators[0]}</div>
              </div>
            </div>

            {/* Upside */}
            <div className="bg-card border border-emerald-500/30 hover:border-emerald-500/50 transition-all rounded-xl p-4 flex flex-col justify-between space-y-3 shadow-xs">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="px-2 py-0.5 rounded text-[10px] bg-emerald-500/15 text-emerald-600 dark:text-emerald-400 border border-emerald-500/30 font-semibold">
                    UPSIDE
                  </span>
                  <span className="text-emerald-600 dark:text-emerald-300">25% Likelihood</span>
                </div>
                <div className="font-semibold text-foreground text-sm mb-1">{scenarios.UPSIDE?.title}</div>
                <p className="text-muted-foreground leading-relaxed text-[11px] font-sans">
                  {scenarios.UPSIDE?.description}
                </p>
              </div>
              <div className="pt-3 border-t border-border space-y-1 text-[10px]">
                <div className="text-muted-foreground">Leading Indicator:</div>
                <div className="text-emerald-600 dark:text-emerald-400 font-semibold">{scenarios.UPSIDE?.leading_indicators[0]}</div>
              </div>
            </div>

            {/* Downside */}
            <div className="bg-card border border-amber-500/30 hover:border-amber-500/50 transition-all rounded-xl p-4 flex flex-col justify-between space-y-3 shadow-xs">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="px-2 py-0.5 rounded text-[10px] bg-amber-500/15 text-amber-600 dark:text-amber-400 border border-amber-500/30 font-semibold">
                    DOWNSIDE
                  </span>
                  <span className="text-amber-600 dark:text-amber-300">20% Likelihood</span>
                </div>
                <div className="font-semibold text-foreground text-sm mb-1">{scenarios.DOWNSIDE?.title}</div>
                <p className="text-muted-foreground leading-relaxed text-[11px] font-sans">
                  {scenarios.DOWNSIDE?.description}
                </p>
              </div>
              <div className="pt-3 border-t border-border space-y-1 text-[10px]">
                <div className="text-muted-foreground">Leading Indicator:</div>
                <div className="text-amber-600 dark:text-amber-400 font-semibold">{scenarios.DOWNSIDE?.leading_indicators[0]}</div>
              </div>
            </div>

            {/* Disruption */}
            <div className="bg-card border border-red-500/30 hover:border-red-500/50 transition-all rounded-xl p-4 flex flex-col justify-between space-y-3 shadow-xs">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="px-2 py-0.5 rounded text-[10px] bg-red-500/15 text-red-600 dark:text-red-400 border border-red-500/30 font-semibold">
                    DISRUPTION
                  </span>
                  <span className="text-red-600 dark:text-red-300">10% Likelihood</span>
                </div>
                <div className="font-semibold text-foreground text-sm mb-1">{scenarios.DISRUPTION?.title}</div>
                <p className="text-muted-foreground leading-relaxed text-[11px] font-sans">
                  {scenarios.DISRUPTION?.description}
                </p>
              </div>
              <div className="pt-3 border-t border-border space-y-1 text-[10px]">
                <div className="text-muted-foreground">Leading Indicator:</div>
                <div className="text-red-600 dark:text-red-400 font-semibold">{scenarios.DISRUPTION?.leading_indicators[0]}</div>
              </div>
            </div>

            {/* Unknown */}
            <div className="bg-card border border-purple-500/40 bg-purple-500/5 hover:border-purple-500/60 transition-all rounded-xl p-4 flex flex-col justify-between space-y-3 shadow-xs">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="px-2 py-0.5 rounded text-[10px] bg-purple-500/20 text-purple-700 dark:text-purple-300 border border-purple-500/40 font-semibold">
                    UNKNOWN
                  </span>
                  <span className="text-purple-700 dark:text-purple-300">Uncertainty: 95%</span>
                </div>
                <div className="font-semibold text-foreground text-sm mb-1">{scenarios.UNKNOWN?.title}</div>
                <p className="text-muted-foreground leading-relaxed text-[11px] font-sans">
                  {scenarios.UNKNOWN?.description}
                </p>
              </div>
              <div className="pt-3 border-t border-border space-y-1 text-[10px]">
                <div className="text-muted-foreground">Resolution Action:</div>
                <div className="text-purple-700 dark:text-purple-300 font-semibold">Randomized A/B Trial</div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Mode Content: CHALLENGE */}
      {activeMode === "CHALLENGE" && (
        <div className="bg-card border border-border rounded-xl p-6 space-y-6 shadow-xs">
          <div>
            <h2 className="text-lg font-semibold text-foreground flex items-center gap-2">
              <AlertCircle className="w-5 h-5 text-amber-500" />
              Operator Challenge & Counter-Evidence Surface
            </h2>
            <p className="text-xs text-muted-foreground mt-1">
              Test assumptions, attach market dissent notes, and trigger mathematical confidence downgrading.
            </p>
          </div>

          <div className="space-y-4">
            <div>
              <label className="block text-xs font-mono text-foreground mb-2">
                Operator Dissent & Counter-Thesis Notes:
              </label>
              <textarea
                value={challengeNotes}
                onChange={(e) => setChallengeNotes(e.target.value)}
                placeholder="e.g. Traditional VIP clients express fatigue with fast-cut kinetic pacing. Recommend maintaining 30% heritage pacing baseline."
                className="w-full h-28 bg-card border border-border rounded-lg p-3 text-xs text-foreground placeholder-muted-foreground focus:outline-none focus:border-purple-500 font-mono shadow-xs"
              />
            </div>

            <div className="flex items-center justify-between">
              <button
                onClick={handleChallenge}
                className="px-4 py-2 bg-amber-500/20 text-amber-700 dark:text-amber-300 border border-amber-500/40 hover:bg-amber-500/30 rounded-lg font-mono text-xs font-semibold transition-colors flex items-center gap-2"
              >
                <AlertCircle className="w-4 h-4" />
                <span>Submit Challenge & Downgrade Confidence</span>
              </button>

              {isChallenged && (
                <div className="flex items-center gap-2 text-xs font-mono text-emerald-600 dark:text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-3 py-1.5 rounded-lg">
                  <ShieldCheck className="w-4 h-4" />
                  <span>Recommendation Status Updated to [DOWNGRADED] • Confidence Damped to 52%</span>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Mode Content: DECIDE */}
      {activeMode === "DECIDE" && (
        <div className="bg-card border border-border rounded-xl p-6 space-y-6 shadow-xs">
          <div>
            <h2 className="text-lg font-semibold text-foreground flex items-center gap-2">
              <CheckCircle className="w-5 h-5 text-emerald-500" />
              Strategic Decision Execution & Experiment Commissioning
            </h2>
            <p className="text-xs text-muted-foreground mt-1">
              Human-owned decision boundary. Authorize bounded exploratory trials without granting autonomous executive authority.
            </p>
          </div>

          <div className="p-4 bg-muted/30 border border-border rounded-xl space-y-3 text-xs font-mono">
            <div className="flex items-center justify-between">
              <span className="text-muted-foreground">Selected Recommendation:</span>
              <span className="text-foreground font-semibold">Deploy Asymmetric Jewelry Capsule Trial</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-muted-foreground">Reversibility:</span>
              <span className="text-emerald-600 dark:text-emerald-400 font-semibold">HIGHLY_REVERSIBLE (Low-Cost Holdout)</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-muted-foreground">Proposed Experiment:</span>
              <span className="text-purple-600 dark:text-purple-300">Run 50/50 split on 20k impressions across Instagram Reels</span>
            </div>
            <div className="pt-2 border-t border-border flex justify-end">
              <button className="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg font-semibold font-mono text-xs flex items-center gap-2 transition-colors shadow-sm">
                <span>Authorize Experiment (EXP-ASYM-01)</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
