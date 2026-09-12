"use client";

import React, { useState } from "react";
import { 
  Compass, 
  CheckCircle2, 
  Lock, 
  Sparkles, 
  Layers, 
  ShieldCheck, 
  AlertTriangle, 
  ArrowRight,
  Sliders,
  Maximize2,
  X,
  Eye,
  RefreshCw,
  Scale
} from "lucide-react";
import type { CampaignStudioModel, CreativeDirection } from "@/lib/campaignStudioFixtures";

interface DirectionsTabProps {
  campaign: CampaignStudioModel;
  onSelectDirection: (directionId: string) => void;
  onNavigateTab: (tab: 'overview' | 'intelligence' | 'directions' | 'visuals' | 'assets' | 'review' | 'production' | 'outcomes') => void;
}

export function DirectionsTab({ campaign, onSelectDirection, onNavigateTab }: DirectionsTabProps) {
  const [directions, setDirections] = useState<CreativeDirection[]>(campaign.directions);
  const [selectedForCompare, setSelectedForCompare] = useState<string[]>(['dir-01', 'dir-02', 'dir-03']);
  const [isCompareModalOpen, setIsCompareModalOpen] = useState(false);
  const [selectedDirectionDetail, setSelectedDirectionDetail] = useState<CreativeDirection | null>(null);
  const [notification, setNotification] = useState<string | null>(null);

  const handleLockDirection = (dirId: string) => {
    setDirections(prev => prev.map(d => {
      if (d.id === dirId) {
        return { ...d, decisionStatus: 'selected' as const, badge: 'HUMAN LOCKED ★' };
      }
      return { ...d, decisionStatus: 'draft' as const, badge: d.badge.replace('HUMAN LOCKED ★', '').trim() || 'ALTERNATIVE' };
    }));
    onSelectDirection(dirId);
    const chosen = directions.find(d => d.id === dirId);
    setNotification(`Human Decision Recorded: Locked "${chosen?.title}" as primary campaign direction.`);
    setTimeout(() => setNotification(null), 4000);
  };

  const handleRejectDirection = (dirId: string) => {
    setDirections(prev => prev.map(d => d.id === dirId ? { ...d, decisionStatus: 'rejected' as const, badge: 'REJECTED' } : d));
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-200">
      
      {/* Toast Notification */}
      {notification && (
        <div className="fixed bottom-8 right-8 z-50 p-4 rounded-xl bg-[#141416] border border-emerald-500/40 text-emerald-300 shadow-2xl flex items-center gap-3 text-xs animate-in slide-in-from-bottom-3 duration-200">
          <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          <span>{notification}</span>
        </div>
      )}

      {/* Surface Header & Comparison Control */}
      <div className="p-6 rounded-2xl bg-[#111113]/80 border border-white/10 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <Compass className="w-5 h-5 text-[#E1D4C0]" />
            <h2 className="text-lg font-serif text-white font-medium">Creative Direction Architecture</h2>
          </div>
          <p className="text-xs text-white/50 font-light">
            Compare distinct strategic hypotheses. Human selection explicitly commits the direction into organizational memory.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={() => setIsCompareModalOpen(true)}
            className="px-3.5 py-2 rounded-xl bg-white/[0.04] hover:bg-white/10 text-white/80 hover:text-white border border-white/10 text-xs font-medium flex items-center gap-2 transition-colors"
          >
            <Scale className="w-3.5 h-3.5 text-[#E1D4C0]" />
            <span>Compare Directions Side-by-Side</span>
          </button>
        </div>
      </div>

      {/* Creative Directions Signature 3-Card Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {directions.map((dir) => {
          const isLocked = dir.decisionStatus === 'selected';
          const isRejected = dir.decisionStatus === 'rejected';

          return (
            <div
              key={dir.id}
              className={`rounded-2xl border p-6 flex flex-col justify-between space-y-6 transition-all duration-300 relative overflow-hidden ${
                isLocked
                  ? "bg-gradient-to-b from-[#161619] to-[#0E0E10] border-[#E1D4C0] shadow-[0_0_30px_rgba(225,212,192,0.12)]"
                  : isRejected
                  ? "bg-[#0E0E10]/40 border-white/5 opacity-50"
                  : "bg-[#111113]/70 border-white/10 hover:border-white/20"
              }`}
            >
              {/* Header Badges */}
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-mono tracking-widest text-[#E1D4C0] font-bold">
                    DIRECTION {dir.tag}
                  </span>
                  <span className={`text-[9px] font-mono px-2 py-0.5 rounded-full border ${
                    isLocked 
                      ? "bg-[#E1D4C0]/20 text-[#E1D4C0] border-[#E1D4C0]/40 font-bold"
                      : "bg-white/5 text-white/50 border-white/10"
                  }`}>
                    {dir.badge}
                  </span>
                </div>

                <div>
                  <h3 className="text-xl font-serif text-white font-medium">{dir.title}</h3>
                  <span className="text-[10px] font-mono text-[#E1D4C0]/70 uppercase">{dir.archetype}</span>
                  <p className="text-xs text-white/50 font-light mt-1">{dir.subtitle}</p>
                </div>
              </div>

              {/* Core Idea & Narrative */}
              <div className="space-y-3 text-xs flex-1">
                <div className="p-3.5 rounded-xl bg-white/[0.02] border border-white/5 space-y-1">
                  <span className="text-[9px] font-mono text-white/40 uppercase">Core Strategic Concept</span>
                  <p className="text-white/90 leading-relaxed font-light">{dir.coreIdea}</p>
                </div>

                {/* Visual Tokens Matrix */}
                <div className="space-y-1.5 pt-1 text-[11px]">
                  <div className="flex items-center justify-between text-white/70 py-1 border-b border-white/5">
                    <span className="text-white/40 font-mono">Lighting:</span>
                    <span className="truncate max-w-[180px]">{dir.lighting}</span>
                  </div>
                  <div className="flex items-center justify-between text-white/70 py-1 border-b border-white/5">
                    <span className="text-white/40 font-mono">Composition:</span>
                    <span className="truncate max-w-[180px]">{dir.composition}</span>
                  </div>
                  <div className="flex items-center justify-between text-white/70 py-1 border-b border-white/5">
                    <span className="text-white/40 font-mono">Material:</span>
                    <span className="truncate max-w-[180px]">{dir.materialTreatment}</span>
                  </div>
                </div>

                {/* Score Indicators */}
                <div className="grid grid-cols-2 gap-2 pt-2 text-[10px] font-mono">
                  <div className="p-2 rounded-lg bg-white/[0.02] border border-white/5">
                    <div className="text-white/40">DNA FIT</div>
                    <div className="text-[#E1D4C0] font-semibold text-sm">{dir.brandAlignmentScore}%</div>
                  </div>
                  <div className="p-2 rounded-lg bg-white/[0.02] border border-white/5">
                    <div className="text-white/40">DISTINCTIVENESS</div>
                    <div className="text-emerald-400 font-semibold text-sm">{dir.distinctivenessScore}%</div>
                  </div>
                </div>

                {/* Risks / Tensions */}
                {dir.risksAndTensions.length > 0 && (
                  <div className="p-2.5 rounded-lg bg-amber-500/[0.04] border border-amber-500/20 text-[10px] text-amber-300/80 space-y-0.5">
                    <span className="font-semibold uppercase tracking-wider">Tension:</span>
                    <p className="font-light">{dir.risksAndTensions[0]}</p>
                  </div>
                )}
              </div>

              {/* Action Buttons */}
              <div className="space-y-2 pt-2 border-t border-white/5">
                {isLocked ? (
                  <div className="w-full py-2.5 rounded-xl bg-[#E1D4C0] text-[#0A0A0A] font-bold text-xs flex items-center justify-center gap-2 shadow-lg">
                    <Lock className="w-3.5 h-3.5" />
                    <span>LOCKED AS CAMPAIGN DIRECTION</span>
                  </div>
                ) : (
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => handleLockDirection(dir.id)}
                      className="flex-1 py-2 rounded-xl bg-[#E1D4C0]/90 hover:bg-[#E1D4C0] text-[#0A0A0A] font-semibold text-xs transition-colors flex items-center justify-center gap-1.5"
                    >
                      <CheckCircle2 className="w-3.5 h-3.5" />
                      <span>Select & Lock</span>
                    </button>
                    <button
                      onClick={() => handleRejectDirection(dir.id)}
                      className="px-3 py-2 rounded-xl bg-white/[0.03] hover:bg-rose-500/20 text-white/40 hover:text-rose-300 border border-white/5 text-xs transition-colors"
                      title="Reject Direction"
                    >
                      Reject
                    </button>
                  </div>
                )}

                <button
                  onClick={() => {
                    setSelectedDirectionDetail(dir);
                    onNavigateTab('visuals');
                  }}
                  className="w-full py-1.5 rounded-lg bg-transparent hover:bg-white/5 text-[11px] font-mono text-white/50 hover:text-white transition-colors flex items-center justify-center gap-1"
                >
                  <span>Explore in Visual Development</span>
                  <ArrowRight className="w-3 h-3" />
                </button>
              </div>

            </div>
          );
        })}
      </div>

      {/* Side-by-Side Comparison Modal */}
      {isCompareModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-md animate-in fade-in duration-150">
          <div className="relative w-full max-w-5xl rounded-2xl bg-[#111113] border border-white/10 shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
            
            <div className="px-6 py-4 border-b border-white/5 flex items-center justify-between bg-white/[0.02]">
              <div className="flex items-center gap-2.5">
                <Scale className="w-5 h-5 text-[#E1D4C0]" />
                <h3 className="text-sm font-medium text-white">Side-by-Side Direction Comparative Evaluation</h3>
              </div>
              <button
                onClick={() => setIsCompareModalOpen(false)}
                className="w-7 h-7 rounded-lg border border-white/5 flex items-center justify-center text-white/40 hover:text-white"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="p-6 overflow-x-auto space-y-6 flex-1">
              <table className="w-full text-xs text-left border-collapse">
                <thead>
                  <tr className="border-b border-white/10 text-[10px] font-mono uppercase text-white/40">
                    <th className="p-3 w-1/4">Evaluation Vector</th>
                    {directions.map(d => (
                      <th key={d.id} className="p-3 w-1/4 text-white">
                        Direction {d.tag}: {d.title}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/5 text-white/80 font-light">
                  <tr>
                    <td className="p-3 font-mono text-[10px] text-white/40">Archetype</td>
                    {directions.map(d => (
                      <td key={d.id} className="p-3 font-medium text-[#E1D4C0]">{d.archetype}</td>
                    ))}
                  </tr>
                  <tr>
                    <td className="p-3 font-mono text-[10px] text-white/40">Core Narrative</td>
                    {directions.map(d => (
                      <td key={d.id} className="p-3 leading-relaxed">{d.narrative}</td>
                    ))}
                  </tr>
                  <tr>
                    <td className="p-3 font-mono text-[10px] text-white/40">Lighting Shader</td>
                    {directions.map(d => (
                      <td key={d.id} className="p-3 font-mono text-[11px]">{d.lighting}</td>
                    ))}
                  </tr>
                  <tr>
                    <td className="p-3 font-mono text-[10px] text-white/40">Material Treatment</td>
                    {directions.map(d => (
                      <td key={d.id} className="p-3">{d.materialTreatment}</td>
                    ))}
                  </tr>
                  <tr>
                    <td className="p-3 font-mono text-[10px] text-white/40">Brand DNA Fit</td>
                    {directions.map(d => (
                      <td key={d.id} className="p-3 font-mono text-emerald-400 font-bold">{d.brandAlignmentScore}%</td>
                    ))}
                  </tr>
                  <tr>
                    <td className="p-3 font-mono text-[10px] text-white/40">Distinctiveness Score</td>
                    {directions.map(d => (
                      <td key={d.id} className="p-3 font-mono text-[#E1D4C0] font-bold">{d.distinctivenessScore}%</td>
                    ))}
                  </tr>
                  <tr>
                    <td className="p-3 font-mono text-[10px] text-white/40">Selection Action</td>
                    {directions.map(d => (
                      <td key={d.id} className="p-3">
                        {d.decisionStatus === 'selected' ? (
                          <span className="text-emerald-400 font-mono text-[10px] flex items-center gap-1 font-bold">
                            <Lock className="w-3 h-3" /> LOCKED
                          </span>
                        ) : (
                          <button
                            onClick={() => {
                              handleLockDirection(d.id);
                              setIsCompareModalOpen(false);
                            }}
                            className="px-3 py-1.5 rounded-lg bg-[#E1D4C0] text-[#0A0A0A] font-semibold text-[10px]"
                          >
                            Lock Decision
                          </button>
                        )}
                      </td>
                    ))}
                  </tr>
                </tbody>
              </table>
            </div>

          </div>
        </div>
      )}

    </div>
  );
}
