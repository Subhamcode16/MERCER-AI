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
    <div className="h-full overflow-y-auto bg-background text-foreground p-8 lg:p-12 scrollbar-thin">
      <div className="max-w-6xl mx-auto space-y-10">
        
        {/* Brand Header & Health Scorecard */}
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6 pb-8 border-b border-border">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 rounded-2xl bg-primary/10 border border-primary/30 flex items-center justify-center text-primary shadow-xs">
              <Fingerprint className="w-8 h-8" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-2xl sm:text-3xl font-serif text-foreground font-light">AURA Couture</h1>
                <span className="px-2.5 py-0.5 rounded-full text-[10px] font-mono tracking-wider bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 border border-emerald-500/20 font-medium">
                  HEALTHY
                </span>
              </div>
              <p className="text-xs text-muted-foreground font-light mt-1 max-w-xl">
                Contemporary Indian luxury apparel fusing heritage Banarasi brocades with modern minimalist architectural silhouettes.
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <button 
              onClick={() => setShowIngestModal(true)}
              className="px-4 py-2 rounded-xl border border-border bg-card hover:bg-muted text-xs font-medium text-foreground transition-all flex items-center gap-2 shadow-xs cursor-pointer"
            >
              <UploadCloud className="w-4 h-4 text-purple-600 dark:text-purple-400" /> Ingest Assets
            </button>
            <button 
              onClick={() => setShowNewBrandModal(true)}
              className="px-4 py-2 rounded-xl bg-primary text-primary-foreground text-xs font-semibold hover:opacity-90 transition-opacity flex items-center gap-2 shadow-sm cursor-pointer"
            >
              <PlusCircle className="w-4 h-4" /> New Brand
            </button>
          </div>
        </div>

        {/* Brand Perception Banner — "VYREN understands my brand" */}
        <div className="rounded-2xl border border-border bg-card p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-6 shadow-sm">
          <div className="space-y-1.5">
            <div className="flex items-center gap-2 text-[10px] tracking-[0.2em] uppercase text-primary font-mono font-semibold">
              <Sparkles className="w-3.5 h-3.5" /> Organizational Memory Active
            </div>
            <div className="text-sm font-medium text-foreground">
              VYREN Brand DNA & Consistency Model
            </div>
            <p className="text-xs text-muted-foreground font-light max-w-2xl">
              14 memory classes and 32 historical asset sets synchronized. Visual DNA, voice guidelines, and drape physics calibrated across all channels.
            </p>
          </div>

          <div className="flex items-center gap-6 divide-x divide-border">
            <div className="text-center px-3">
              <div className="text-xl font-serif text-emerald-600 dark:text-emerald-400 font-medium">96.4%</div>
              <div className="text-[10px] text-muted-foreground tracking-wider uppercase font-mono">Fidelity</div>
            </div>
            <div className="text-center pl-6 pr-3">
              <div className="text-xl font-serif text-primary font-medium">0.02%</div>
              <div className="text-[10px] text-muted-foreground tracking-wider uppercase font-mono">Drift</div>
            </div>
            <div className="text-center pl-6">
              <div className="text-xl font-serif text-blue-600 dark:text-blue-400 font-medium">14</div>
              <div className="text-[10px] text-muted-foreground tracking-wider uppercase font-mono">Decisions</div>
            </div>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="flex items-center gap-2 border-b border-border pb-px text-xs font-medium">
          <button
            onClick={() => setActiveTab("overview")}
            className={`pb-3 px-3 transition-colors relative cursor-pointer ${
              activeTab === "overview" ? "text-primary font-semibold" : "text-muted-foreground hover:text-foreground"
            }`}
          >
            Overview
            {activeTab === "overview" && <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-primary" />}
          </button>

          <button
            onClick={() => setActiveTab("dna")}
            className={`pb-3 px-3 transition-colors relative cursor-pointer ${
              activeTab === "dna" ? "text-primary font-semibold" : "text-muted-foreground hover:text-foreground"
            }`}
          >
            Visual DNA & Tokens
            {activeTab === "dna" && <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-primary" />}
          </button>

          <button
            onClick={() => setActiveTab("strategy")}
            className={`pb-3 px-3 transition-colors relative cursor-pointer ${
              activeTab === "strategy" ? "text-primary font-semibold" : "text-muted-foreground hover:text-foreground"
            }`}
          >
            Strategy & Positioning
            {activeTab === "strategy" && <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-primary" />}
          </button>

          <button
            onClick={() => setActiveTab("products")}
            className={`pb-3 px-3 transition-colors relative cursor-pointer ${
              activeTab === "products" ? "text-primary font-semibold" : "text-muted-foreground hover:text-foreground"
            }`}
          >
            Collections & Products
            {activeTab === "products" && <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-primary" />}
          </button>

          <button
            onClick={() => setActiveTab("decisions")}
            className={`pb-3 px-3 transition-colors relative cursor-pointer ${
              activeTab === "decisions" ? "text-primary font-semibold" : "text-muted-foreground hover:text-foreground"
            }`}
          >
            Decision Ledger
            {activeTab === "decisions" && <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-primary" />}
          </button>
        </div>

        {/* Tab Content: Overview */}
        {activeTab === "overview" && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            
            {/* Left 2 Columns: Core Identity & Strategy */}
            <div className="md:col-span-2 space-y-8">
              
              {/* Positioning & Identity Card */}
              <div className="rounded-2xl border border-border bg-card p-6 space-y-4 shadow-sm">
                <div className="flex items-center justify-between">
                  <h3 className="text-sm font-medium text-foreground flex items-center gap-2">
                    <Target className="w-4 h-4 text-primary" /> Core Positioning & Target Audience
                  </h3>
                  <Link href="/research" className="text-[11px] text-primary/80 hover:text-primary font-medium">
                    Research Whitespace &rarr;
                  </Link>
                </div>
                
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
                  <div className="p-3.5 rounded-xl bg-muted/30 border border-border space-y-1">
                    <div className="text-muted-foreground text-[10px] uppercase tracking-wider font-mono">Value Proposition</div>
                    <div className="text-foreground font-medium">Reimagining Indian heritage craft for high-end cosmopolitan living.</div>
                  </div>
                  <div className="p-3.5 rounded-xl bg-muted/30 border border-border space-y-1">
                    <div className="text-muted-foreground text-[10px] uppercase tracking-wider font-mono">Primary Audience</div>
                    <div className="text-foreground font-medium">Affluent Gen Z & Millennial consumers in Mumbai, Delhi, London, NYC.</div>
                  </div>
                </div>

                <div className="p-3.5 rounded-xl bg-muted/30 border border-border space-y-1 text-xs">
                  <div className="text-muted-foreground text-[10px] uppercase tracking-wider font-mono">Brand Archetype & Voice</div>
                  <div className="text-foreground/80 font-light leading-relaxed">
                    <strong>The Modern Sovereign:</strong> Sophisticated, architectural, respectful of artisan provenance, unapologetically elevated.
                  </div>
                </div>
              </div>

              {/* Visual DNA Highlight */}
              <div className="rounded-2xl border border-border bg-card p-6 space-y-4 shadow-sm">
                <div className="flex items-center justify-between">
                  <h3 className="text-sm font-medium text-foreground flex items-center gap-2">
                    <Dna className="w-4 h-4 text-purple-600 dark:text-purple-400" /> Visual DNA Snapshot
                  </h3>
                  <Link href="/visual-dna" className="text-[11px] text-primary/80 hover:text-primary font-medium">
                    Full Visual DNA &rarr;
                  </Link>
                </div>

                <div className="grid grid-cols-3 sm:grid-cols-6 gap-3">
                  <div className="space-y-1.5">
                    <div className="h-10 rounded-lg bg-[#0F0D0A] border border-border" />
                    <div className="text-[10px] text-muted-foreground text-center font-mono">#0F0D0A</div>
                  </div>
                  <div className="space-y-1.5">
                    <div className="h-10 rounded-lg bg-[#E1D4C0] border border-border" />
                    <div className="text-[10px] text-muted-foreground text-center font-mono">#E1D4C0</div>
                  </div>
                  <div className="space-y-1.5">
                    <div className="h-10 rounded-lg bg-[#8A3324] border border-border" />
                    <div className="text-[10px] text-muted-foreground text-center font-mono">#8A3324</div>
                  </div>
                  <div className="space-y-1.5">
                    <div className="h-10 rounded-lg bg-[#D4AF37] border border-border" />
                    <div className="text-[10px] text-muted-foreground text-center font-mono">#D4AF37</div>
                  </div>
                  <div className="space-y-1.5">
                    <div className="h-10 rounded-lg bg-[#2E3B32] border border-border" />
                    <div className="text-[10px] text-muted-foreground text-center font-mono">#2E3B32</div>
                  </div>
                  <div className="space-y-1.5">
                    <div className="h-10 rounded-lg bg-[#F5F2EB] border border-border" />
                    <div className="text-[10px] text-muted-foreground text-center font-mono">#F5F2EB</div>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-3 text-xs pt-2">
                  <div className="p-3 rounded-xl bg-muted/30 border border-border">
                    <span className="text-muted-foreground text-[10px] font-mono">TYPOGRAPHY:</span>
                    <div className="text-foreground font-medium mt-0.5">Editorial Serif + Neue Haas Grotesk</div>
                  </div>
                  <div className="p-3 rounded-xl bg-muted/30 border border-border">
                    <span className="text-muted-foreground text-[10px] font-mono">OPTICAL LIGHTING:</span>
                    <div className="text-foreground font-medium mt-0.5">Tungsten 3200K + Chiaroscuro Rim</div>
                  </div>
                </div>
              </div>

            </div>

            {/* Right Column: AI Team & Recommended Action */}
            <div className="space-y-8">
              
              {/* Next Recommended Action */}
              <div className="rounded-2xl border border-primary/30 bg-card p-6 space-y-4 shadow-sm">
                <div className="text-[10px] tracking-[0.2em] uppercase text-primary font-mono font-semibold flex items-center gap-1.5">
                  <Sparkles className="w-3.5 h-3.5" /> Next Recommended Action
                </div>
                <h4 className="text-sm font-medium text-foreground leading-snug">
                  Launch Visual Exploration for Festive 2026 Campaign
                </h4>
                <p className="text-xs text-muted-foreground font-light leading-relaxed">
                  Your AI Team has completed market analysis and detected a luxury whitespace in sheer organza overlay styling.
                </p>
                <Link
                  href="/studio"
                  className="w-full py-2.5 rounded-xl bg-primary text-primary-foreground text-xs font-semibold tracking-wide flex items-center justify-center gap-2 hover:opacity-90 transition-opacity shadow-sm"
                >
                  Enter Creative Studio <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              </div>

              {/* AI Workforce Working On This Brand */}
              <div className="rounded-2xl border border-border bg-card p-5 space-y-3 shadow-sm">
                <div className="flex items-center justify-between text-xs">
                  <span className="font-medium text-foreground flex items-center gap-2">
                    <Users className="w-4 h-4 text-blue-600 dark:text-blue-400" /> Assigned AI Coworkers
                  </span>
                  <Link href="/team" className="text-[10px] text-muted-foreground hover:text-foreground">Manage &rarr;</Link>
                </div>

                <div className="space-y-2 text-xs">
                  <div className="flex items-center justify-between p-2 rounded-lg bg-muted/30">
                    <span className="text-foreground font-light">Elena Vance</span>
                    <span className="text-[10px] text-emerald-600 dark:text-emerald-400 font-mono">Creative Director</span>
                  </div>
                  <div className="flex items-center justify-between p-2 rounded-lg bg-muted/30">
                    <span className="text-foreground font-light">Marcus Reed</span>
                    <span className="text-[10px] text-blue-600 dark:text-blue-400 font-mono">Brand Strategist</span>
                  </div>
                  <div className="flex items-center justify-between p-2 rounded-lg bg-muted/30">
                    <span className="text-foreground font-light">Aria Chen</span>
                    <span className="text-[10px] text-purple-600 dark:text-purple-400 font-mono">Visual Intelligence</span>
                  </div>
                </div>
              </div>

            </div>

          </div>
        )}

        {/* Tab Content: Decisions */}
        {activeTab === "decisions" && (
          <div className="rounded-2xl border border-border bg-card p-6 space-y-4 shadow-sm">
            <h3 className="text-sm font-medium text-foreground flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-emerald-600 dark:text-emerald-400" /> Cryptographic Decision Ledger (Human Governance)
            </h3>
            <p className="text-xs text-muted-foreground font-light">
              Every strategic commitment, budget approval, and brand DNA change requires human authorization and is stored with tamper-evident audit proofs.
            </p>

            <div className="space-y-3 pt-2">
              <div className="p-4 rounded-xl bg-muted/30 border border-border flex items-center justify-between text-xs">
                <div>
                  <div className="font-medium text-foreground">DEC-2026-089: Ratify Banarasi Weave Drape Simulation Tokens</div>
                  <div className="text-[11px] text-muted-foreground mt-0.5 font-mono">Authorized by Creative Director • Block #892014</div>
                </div>
                <span className="px-2 py-0.5 rounded text-[10px] bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 border border-emerald-500/20 font-mono font-medium">
                  APPROVED
                </span>
              </div>

              <div className="p-4 rounded-xl bg-muted/30 border border-border flex items-center justify-between text-xs">
                <div>
                  <div className="font-medium text-foreground">DEC-2026-088: Autumn/Winter Omnichannel Palette Expansion</div>
                  <div className="text-[11px] text-muted-foreground mt-0.5 font-mono">Authorized by Brand Lead • Block #891980</div>
                </div>
                <span className="px-2 py-0.5 rounded text-[10px] bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 border border-emerald-500/20 font-mono font-medium">
                  APPROVED
                </span>
              </div>
            </div>
          </div>
        )}

      </div>

      {/* Modal: Bring an Existing Brand */}
      {showIngestModal && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="w-full max-w-lg rounded-2xl border border-border bg-card p-6 space-y-6 shadow-2xl">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <div className="w-8 h-8 rounded-lg bg-purple-500/10 text-purple-600 dark:text-purple-400 flex items-center justify-center">
                  <UploadCloud className="w-4 h-4" />
                </div>
                <h3 className="text-base font-medium text-foreground">Bring an Existing Brand</h3>
              </div>
              <button onClick={() => setShowIngestModal(false)} className="text-muted-foreground hover:text-foreground text-sm cursor-pointer">✕</button>
            </div>

            <p className="text-xs text-muted-foreground font-light leading-relaxed">
              Upload past campaign images, brand guidelines, packaging PDFs, or website URLs. VYREN will ingest your assets, extract your Brand DNA, and detect any visual or narrative drift.
            </p>

            <div className="border-2 border-dashed border-border rounded-xl p-8 text-center space-y-3 hover:border-primary/50 transition-colors cursor-pointer bg-muted/20">
              <UploadCloud className="w-8 h-8 text-muted-foreground/60 mx-auto" />
              <div className="text-xs text-foreground font-medium">Drop brand guidelines, PDFs, or packaging photos here</div>
              <div className="text-[10px] text-muted-foreground">Supports PDF, PNG, JPG, ZIP (up to 500MB)</div>
            </div>

            <div className="flex items-center justify-end gap-3 pt-2">
              <button 
                onClick={() => setShowIngestModal(false)}
                className="px-4 py-2 rounded-xl text-xs text-muted-foreground hover:text-foreground cursor-pointer"
              >
                Cancel
              </button>
              <button 
                onClick={() => {
                  setShowIngestModal(false);
                  alert("Assets queued for VYREN Brand DNA ingestion and drift analysis.");
                }}
                className="px-4 py-2 rounded-xl bg-primary text-primary-foreground text-xs font-semibold hover:opacity-90 shadow-sm cursor-pointer"
              >
                Start Ingestion & Audit
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Modal: Start a New Brand */}
      {showNewBrandModal && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="w-full max-w-lg rounded-2xl border border-border bg-card p-6 space-y-6 shadow-2xl">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <div className="w-8 h-8 rounded-lg bg-primary/10 text-primary flex items-center justify-center">
                  <PlusCircle className="w-4 h-4" />
                </div>
                <h3 className="text-base font-medium text-foreground">Start a New Brand (0 &rarr; 1)</h3>
              </div>
              <button onClick={() => setShowNewBrandModal(false)} className="text-muted-foreground hover:text-foreground text-sm cursor-pointer">✕</button>
            </div>

            <p className="text-xs text-muted-foreground font-light leading-relaxed">
              Define your vision from scratch. VYREN’s Strategy and Creative workers will research your market whitespace and synthesize a distinct visual identity.
            </p>

            <div className="space-y-4 text-xs">
              <div className="space-y-1.5">
                <label className="text-muted-foreground font-mono text-[10px] uppercase">Brand Name / Working Title</label>
                <input 
                  type="text" 
                  placeholder="e.g. SOLIS Botanical Skincare"
                  className="w-full px-3.5 py-2.5 rounded-xl bg-background border border-border text-foreground placeholder:text-muted-foreground outline-none focus:border-primary shadow-xs"
                />
              </div>

              <div className="space-y-1.5">
                <label className="text-muted-foreground font-mono text-[10px] uppercase">Core Vision & Product Category</label>
                <textarea 
                  rows={3}
                  placeholder="Describe what you plan to offer, target demographic, and primary brand ethos..."
                  className="w-full px-3.5 py-2.5 rounded-xl bg-background border border-border text-foreground placeholder:text-muted-foreground outline-none focus:border-primary resize-none shadow-xs"
                />
              </div>
            </div>

            <div className="flex items-center justify-end gap-3 pt-2">
              <button 
                onClick={() => setShowNewBrandModal(false)}
                className="px-4 py-2 rounded-xl text-xs text-muted-foreground hover:text-foreground cursor-pointer"
              >
                Cancel
              </button>
              <button 
                onClick={() => {
                  setShowNewBrandModal(false);
                  alert("New brand workspace initialized. Strategy workers assigned.");
                }}
                className="px-4 py-2 rounded-xl bg-primary text-primary-foreground text-xs font-semibold hover:opacity-90 shadow-sm cursor-pointer"
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
