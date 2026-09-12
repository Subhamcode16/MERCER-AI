"use client";

import { useState, useEffect } from "react";
import { useSearchParams } from "next/navigation";
import Link from "next/link";
import { 
  Fingerprint, 
  Sparkles, 
  Layers, 
  Dna, 
  Target, 
  Users, 
  TrendingUp, 
  ShieldCheck, 
  AlertTriangle, 
  ArrowRight, 
  UploadCloud, 
  PlusCircle, 
  CheckCircle2, 
  HelpCircle, 
  FileText,
  Palette
} from "lucide-react";

export default function BrandWorkspacePage() {
  const searchParams = useSearchParams();
  const [activeTab, setActiveTab] = useState<"overview" | "dna" | "strategy" | "products" | "decisions">("overview");
  const [showIngestModal, setShowIngestModal] = useState(false);
  const [showNewBrandModal, setShowNewBrandModal] = useState(false);

  useEffect(() => {
    const modalParam = searchParams.get("modal");
    if (modalParam === "ingest") setShowIngestModal(true);
    if (modalParam === "new") setShowNewBrandModal(true);
  }, [searchParams]);

  return (
    <div className="h-full overflow-y-auto bg-[#0A0A0A] text-white/90 p-8 lg:p-12 scrollbar-thin scrollbar-thumb-white/10">
      <div className="max-w-6xl mx-auto space-y-10">
        
        {/* Brand Header & Health Scorecard */}
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6 pb-8 border-b border-white/5">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-[#E1D4C0]/20 via-[#C9B99A]/10 to-transparent border border-[#E1D4C0]/30 flex items-center justify-center text-[#E1D4C0] shadow-inner">
              <Fingerprint className="w-8 h-8" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-2xl sm:text-3xl font-serif text-white font-light">AURA Couture</h1>
                <span className="px-2.5 py-0.5 rounded-full text-[10px] font-mono tracking-wider bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                  HEALTHY
                </span>
              </div>
              <p className="text-xs text-white/50 font-light mt-1 max-w-xl">
                Contemporary Indian luxury apparel fusing heritage Banarasi brocades with modern minimalist architectural silhouettes.
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <button 
              onClick={() => setShowIngestModal(true)}
              className="px-4 py-2 rounded-xl border border-white/10 bg-white/[0.03] hover:bg-white/[0.08] text-xs font-medium text-white/80 hover:text-white transition-all flex items-center gap-2"
            >
              <UploadCloud className="w-4 h-4 text-purple-400" /> Ingest Assets
            </button>
            <button 
              onClick={() => setShowNewBrandModal(true)}
              className="px-4 py-2 rounded-xl bg-[#E1D4C0] text-[#0A0A0A] text-xs font-semibold hover:opacity-90 transition-opacity flex items-center gap-2"
            >
              <PlusCircle className="w-4 h-4" /> New Brand
            </button>
          </div>
        </div>

        {/* Brand Perception Banner — "VYREN understands my brand" */}
        <div className="rounded-2xl border border-white/10 bg-gradient-to-r from-[#141414] via-[#111111] to-[#161412] p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-6 shadow-xl">
          <div className="space-y-1.5">
            <div className="flex items-center gap-2 text-[10px] tracking-[0.2em] uppercase text-[#E1D4C0] font-mono">
              <Sparkles className="w-3.5 h-3.5" /> Organizational Memory Active
            </div>
            <div className="text-sm font-medium text-white">
              VYREN Brand DNA & Consistency Model
            </div>
            <p className="text-xs text-white/60 font-light max-w-2xl">
              14 memory classes and 32 historical asset sets synchronized. Visual DNA, voice guidelines, and drape physics calibrated across all channels.
            </p>
          </div>

          <div className="flex items-center gap-6 divide-x divide-white/10">
            <div className="text-center px-3">
              <div className="text-xl font-serif text-emerald-400">96.4%</div>
              <div className="text-[10px] text-white/40 tracking-wider uppercase font-mono">Fidelity</div>
            </div>
            <div className="text-center pl-6 pr-3">
              <div className="text-xl font-serif text-[#E1D4C0]">0.02%</div>
              <div className="text-[10px] text-white/40 tracking-wider uppercase font-mono">Drift</div>
            </div>
            <div className="text-center pl-6">
              <div className="text-xl font-serif text-blue-400">14</div>
              <div className="text-[10px] text-white/40 tracking-wider uppercase font-mono">Decisions</div>
            </div>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="flex items-center gap-2 border-b border-white/10 pb-px text-xs font-medium">
          <button
            onClick={() => setActiveTab("overview")}
            className={`pb-3 px-3 transition-colors relative ${
              activeTab === "overview" ? "text-[#E1D4C0]" : "text-white/40 hover:text-white"
            }`}
          >
            Overview
            {activeTab === "overview" && <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-[#E1D4C0]" />}
          </button>

          <button
            onClick={() => setActiveTab("dna")}
            className={`pb-3 px-3 transition-colors relative ${
              activeTab === "dna" ? "text-[#E1D4C0]" : "text-white/40 hover:text-white"
            }`}
          >
            Visual DNA & Tokens
            {activeTab === "dna" && <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-[#E1D4C0]" />}
          </button>

          <button
            onClick={() => setActiveTab("strategy")}
            className={`pb-3 px-3 transition-colors relative ${
              activeTab === "strategy" ? "text-[#E1D4C0]" : "text-white/40 hover:text-white"
            }`}
          >
            Strategy & Positioning
            {activeTab === "strategy" && <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-[#E1D4C0]" />}
          </button>

          <button
            onClick={() => setActiveTab("products")}
            className={`pb-3 px-3 transition-colors relative ${
              activeTab === "products" ? "text-[#E1D4C0]" : "text-white/40 hover:text-white"
            }`}
          >
            Collections & Products
            {activeTab === "products" && <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-[#E1D4C0]" />}
          </button>

          <button
            onClick={() => setActiveTab("decisions")}
            className={`pb-3 px-3 transition-colors relative ${
              activeTab === "decisions" ? "text-[#E1D4C0]" : "text-white/40 hover:text-white"
            }`}
          >
            Decision Ledger
            {activeTab === "decisions" && <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-[#E1D4C0]" />}
          </button>
        </div>

        {/* Tab Content: Overview */}
        {activeTab === "overview" && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            
            {/* Left 2 Columns: Core Identity & Strategy */}
            <div className="md:col-span-2 space-y-8">
              
              {/* Positioning & Identity Card */}
              <div className="rounded-2xl border border-white/10 bg-[#111111]/80 p-6 space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-sm font-medium text-white flex items-center gap-2">
                    <Target className="w-4 h-4 text-[#E1D4C0]" /> Core Positioning & Target Audience
                  </h3>
                  <Link href="/research" className="text-[11px] text-[#E1D4C0]/70 hover:text-[#E1D4C0]">
                    Research Whitespace &rarr;
                  </Link>
                </div>
                
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
                  <div className="p-3.5 rounded-xl bg-white/[0.02] border border-white/5 space-y-1">
                    <div className="text-white/40 text-[10px] uppercase tracking-wider font-mono">Value Proposition</div>
                    <div className="text-white font-medium">Reimagining Indian heritage craft for high-end cosmopolitan living.</div>
                  </div>
                  <div className="p-3.5 rounded-xl bg-white/[0.02] border border-white/5 space-y-1">
                    <div className="text-white/40 text-[10px] uppercase tracking-wider font-mono">Primary Audience</div>
                    <div className="text-white font-medium">Affluent Gen Z & Millennial consumers in Mumbai, Delhi, London, NYC.</div>
                  </div>
                </div>

                <div className="p-3.5 rounded-xl bg-white/[0.02] border border-white/5 space-y-1 text-xs">
                  <div className="text-white/40 text-[10px] uppercase tracking-wider font-mono">Brand Archetype & Voice</div>
                  <div className="text-white/80 font-light leading-relaxed">
                    <strong>The Modern Sovereign:</strong> Sophisticated, architectural, respectful of artisan provenance, unapologetically elevated.
                  </div>
                </div>
              </div>

              {/* Visual DNA Highlight */}
              <div className="rounded-2xl border border-white/10 bg-[#111111]/80 p-6 space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-sm font-medium text-white flex items-center gap-2">
                    <Dna className="w-4 h-4 text-purple-400" /> Visual DNA Snapshot
                  </h3>
                  <Link href="/visual-dna" className="text-[11px] text-[#E1D4C0]/70 hover:text-[#E1D4C0]">
                    Full Visual DNA &rarr;
                  </Link>
                </div>

                <div className="grid grid-cols-3 sm:grid-cols-6 gap-3">
                  <div className="space-y-1.5">
                    <div className="h-10 rounded-lg bg-[#0F0D0A] border border-white/10" />
                    <div className="text-[10px] text-white/50 text-center font-mono">#0F0D0A</div>
                  </div>
                  <div className="space-y-1.5">
                    <div className="h-10 rounded-lg bg-[#E1D4C0] border border-white/10" />
                    <div className="text-[10px] text-white/50 text-center font-mono">#E1D4C0</div>
                  </div>
                  <div className="space-y-1.5">
                    <div className="h-10 rounded-lg bg-[#8A3324] border border-white/10" />
                    <div className="text-[10px] text-white/50 text-center font-mono">#8A3324</div>
                  </div>
                  <div className="space-y-1.5">
                    <div className="h-10 rounded-lg bg-[#D4AF37] border border-white/10" />
                    <div className="text-[10px] text-white/50 text-center font-mono">#D4AF37</div>
                  </div>
                  <div className="space-y-1.5">
                    <div className="h-10 rounded-lg bg-[#2E3B32] border border-white/10" />
                    <div className="text-[10px] text-white/50 text-center font-mono">#2E3B32</div>
                  </div>
                  <div className="space-y-1.5">
                    <div className="h-10 rounded-lg bg-[#F5F2EB] border border-white/10" />
                    <div className="text-[10px] text-white/50 text-center font-mono">#F5F2EB</div>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-3 text-xs pt-2">
                  <div className="p-3 rounded-xl bg-white/[0.02] border border-white/5">
                    <span className="text-white/40 text-[10px] font-mono">TYPOGRAPHY:</span>
                    <div className="text-white font-medium mt-0.5">Editorial Serif + Neue Haas Grotesk</div>
                  </div>
                  <div className="p-3 rounded-xl bg-white/[0.02] border border-white/5">
                    <span className="text-white/40 text-[10px] font-mono">OPTICAL LIGHTING:</span>
                    <div className="text-white font-medium mt-0.5">Tungsten 3200K + Chiaroscuro Rim</div>
                  </div>
                </div>
              </div>

            </div>

            {/* Right Column: AI Team & Recommended Action */}
            <div className="space-y-8">
              
              {/* Next Recommended Action */}
              <div className="rounded-2xl border border-[#E1D4C0]/30 bg-gradient-to-b from-[#161411] to-[#101010] p-6 space-y-4 shadow-lg">
                <div className="text-[10px] tracking-[0.2em] uppercase text-[#E1D4C0] font-mono flex items-center gap-1.5">
                  <Sparkles className="w-3.5 h-3.5" /> Next Recommended Action
                </div>
                <h4 className="text-sm font-medium text-white leading-snug">
                  Launch Visual Exploration for Festive 2026 Campaign
                </h4>
                <p className="text-xs text-white/60 font-light leading-relaxed">
                  Your AI Team has completed market analysis and detected a luxury whitespace in sheer organza overlay styling.
                </p>
                <Link
                  href="/studio"
                  className="w-full py-2.5 rounded-xl bg-[#E1D4C0] text-[#0A0A0A] text-xs font-semibold tracking-wide flex items-center justify-center gap-2 hover:opacity-90 transition-opacity"
                >
                  Enter Creative Studio <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              </div>

              {/* AI Workforce Working On This Brand */}
              <div className="rounded-2xl border border-white/10 bg-[#111111]/80 p-5 space-y-3">
                <div className="flex items-center justify-between text-xs">
                  <span className="font-medium text-white flex items-center gap-2">
                    <Users className="w-4 h-4 text-blue-400" /> Assigned AI Coworkers
                  </span>
                  <Link href="/team" className="text-[10px] text-white/40 hover:text-white">Manage &rarr;</Link>
                </div>

                <div className="space-y-2 text-xs">
                  <div className="flex items-center justify-between p-2 rounded-lg bg-white/[0.02]">
                    <span className="text-white font-light">Elena Vance</span>
                    <span className="text-[10px] text-emerald-400 font-mono">Creative Director</span>
                  </div>
                  <div className="flex items-center justify-between p-2 rounded-lg bg-white/[0.02]">
                    <span className="text-white font-light">Marcus Reed</span>
                    <span className="text-[10px] text-blue-400 font-mono">Brand Strategist</span>
                  </div>
                  <div className="flex items-center justify-between p-2 rounded-lg bg-white/[0.02]">
                    <span className="text-white font-light">Aria Chen</span>
                    <span className="text-[10px] text-purple-400 font-mono">Visual Intelligence</span>
                  </div>
                </div>
              </div>

            </div>

          </div>
        )}

        {/* Tab Content: Decisions */}
        {activeTab === "decisions" && (
          <div className="rounded-2xl border border-white/10 bg-[#111111]/80 p-6 space-y-4">
            <h3 className="text-sm font-medium text-white flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-emerald-400" /> Cryptographic Decision Ledger (Human Governance)
            </h3>
            <p className="text-xs text-white/50 font-light">
              Every strategic commitment, budget approval, and brand DNA change requires human authorization and is stored with tamper-evident audit proofs.
            </p>

            <div className="space-y-3 pt-2">
              <div className="p-4 rounded-xl bg-white/[0.02] border border-white/5 flex items-center justify-between text-xs">
                <div>
                  <div className="font-medium text-white">DEC-2026-089: Ratify Banarasi Weave Drape Simulation Tokens</div>
                  <div className="text-[11px] text-white/40 mt-0.5 font-mono">Authorized by Creative Director • Block #892014</div>
                </div>
                <span className="px-2 py-0.5 rounded text-[10px] bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-mono">
                  APPROVED
                </span>
              </div>

              <div className="p-4 rounded-xl bg-white/[0.02] border border-white/5 flex items-center justify-between text-xs">
                <div>
                  <div className="font-medium text-white">DEC-2026-088: Autumn/Winter Omnichannel Palette Expansion</div>
                  <div className="text-[11px] text-white/40 mt-0.5 font-mono">Authorized by Brand Lead • Block #891980</div>
                </div>
                <span className="px-2 py-0.5 rounded text-[10px] bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-mono">
                  APPROVED
                </span>
              </div>
            </div>
          </div>
        )}

      </div>

      {/* Modal: Bring an Existing Brand */}
      {showIngestModal && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="w-full max-w-lg rounded-2xl border border-white/10 bg-[#121212] p-6 space-y-6 shadow-2xl">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <div className="w-8 h-8 rounded-lg bg-purple-500/10 text-purple-400 flex items-center justify-center">
                  <UploadCloud className="w-4 h-4" />
                </div>
                <h3 className="text-base font-medium text-white">Bring an Existing Brand</h3>
              </div>
              <button onClick={() => setShowIngestModal(false)} className="text-white/40 hover:text-white text-sm">✕</button>
            </div>

            <p className="text-xs text-white/60 font-light leading-relaxed">
              Upload past campaign images, brand guidelines, packaging PDFs, or website URLs. VYREN will ingest your assets, extract your Brand DNA, and detect any visual or narrative drift.
            </p>

            <div className="border-2 border-dashed border-white/10 rounded-xl p-8 text-center space-y-3 hover:border-[#E1D4C0]/40 transition-colors cursor-pointer bg-white/[0.01]">
              <UploadCloud className="w-8 h-8 text-white/30 mx-auto" />
              <div className="text-xs text-white font-medium">Drop brand guidelines, PDFs, or packaging photos here</div>
              <div className="text-[10px] text-white/40">Supports PDF, PNG, JPG, ZIP (up to 500MB)</div>
            </div>

            <div className="flex items-center justify-end gap-3 pt-2">
              <button 
                onClick={() => setShowIngestModal(false)}
                className="px-4 py-2 rounded-xl text-xs text-white/60 hover:text-white"
              >
                Cancel
              </button>
              <button 
                onClick={() => {
                  setShowIngestModal(false);
                  alert("Assets queued for VYREN Brand DNA ingestion and drift analysis.");
                }}
                className="px-4 py-2 rounded-xl bg-[#E1D4C0] text-[#0A0A0A] text-xs font-semibold hover:opacity-90"
              >
                Start Ingestion & Audit
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Modal: Start a New Brand */}
      {showNewBrandModal && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="w-full max-w-lg rounded-2xl border border-white/10 bg-[#121212] p-6 space-y-6 shadow-2xl">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <div className="w-8 h-8 rounded-lg bg-[#E1D4C0]/10 text-[#E1D4C0] flex items-center justify-center">
                  <PlusCircle className="w-4 h-4" />
                </div>
                <h3 className="text-base font-medium text-white">Start a New Brand (0 &rarr; 1)</h3>
              </div>
              <button onClick={() => setShowNewBrandModal(false)} className="text-white/40 hover:text-white text-sm">✕</button>
            </div>

            <p className="text-xs text-white/60 font-light leading-relaxed">
              Define your vision from scratch. VYREN’s Strategy and Creative workers will research your market whitespace and synthesize a distinct visual identity.
            </p>

            <div className="space-y-4 text-xs">
              <div className="space-y-1.5">
                <label className="text-white/60 font-mono text-[10px] uppercase">Brand Name / Working Title</label>
                <input 
                  type="text" 
                  placeholder="e.g. SOLIS Botanical Skincare"
                  className="w-full px-3.5 py-2.5 rounded-xl bg-white/[0.03] border border-white/10 text-white outline-none focus:border-[#E1D4C0]"
                />
              </div>

              <div className="space-y-1.5">
                <label className="text-white/60 font-mono text-[10px] uppercase">Core Vision & Product Category</label>
                <textarea 
                  rows={3}
                  placeholder="Describe what you plan to offer, target demographic, and primary brand ethos..."
                  className="w-full px-3.5 py-2.5 rounded-xl bg-white/[0.03] border border-white/10 text-white outline-none focus:border-[#E1D4C0] resize-none"
                />
              </div>
            </div>

            <div className="flex items-center justify-end gap-3 pt-2">
              <button 
                onClick={() => setShowNewBrandModal(false)}
                className="px-4 py-2 rounded-xl text-xs text-white/60 hover:text-white"
              >
                Cancel
              </button>
              <button 
                onClick={() => {
                  setShowNewBrandModal(false);
                  alert("New brand workspace initialized. Strategy workers assigned.");
                }}
                className="px-4 py-2 rounded-xl bg-[#E1D4C0] text-[#0A0A0A] text-xs font-semibold hover:opacity-90"
              >
                Create Brand Workspace
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}
