"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { 
  Sparkles, 
  ArrowRight, 
  PlusCircle, 
  UploadCloud, 
  Fingerprint, 
  FolderKanban, 
  Target, 
  Users, 
  Search, 
  Brain, 
  TrendingUp, 
  ShieldCheck,
  ChevronRight,
  Palette
} from "lucide-react";

export default function HomePage() {
  const router = useRouter();
  const [prompt, setPrompt] = useState("");
  const [selectedBrand, setSelectedBrand] = useState("AURA Couture");
  const [activeModal, setActiveModal] = useState<"new" | "existing" | null>(null);

  const handleStart = (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt.trim()) return;
    router.push(`/studio?prompt=${encodeURIComponent(prompt)}`);
  };

  return (
    <div className="h-full overflow-y-auto bg-[#0A0A0A] text-white/90 p-8 lg:p-12 scrollbar-thin scrollbar-thumb-white/10">
      <div className="max-w-6xl mx-auto space-y-12">
        
        {/* Top Header / Brand Context Bar */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-6 border-b border-white/5">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-[#E1D4C0]/20 to-[#E1D4C0]/5 border border-[#E1D4C0]/30 flex items-center justify-center text-[#E1D4C0]">
              <Fingerprint className="w-4 h-4" />
            </div>
            <div>
              <div className="text-[10px] tracking-[0.2em] uppercase text-white/40 font-mono">Active Brand</div>
              <div className="text-sm font-medium text-white flex items-center gap-2">
                {selectedBrand}
                <span className="inline-flex items-center px-2 py-0.5 rounded-full text-[9px] font-mono tracking-wider bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                  <ShieldCheck className="w-2.5 h-2.5 mr-1" /> DNA Synced
                </span>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-3 text-xs">
            <Link 
              href="/brand" 
              className="px-3.5 py-1.5 rounded-lg border border-white/10 bg-white/[0.02] hover:bg-white/[0.06] text-white/70 hover:text-white transition-colors flex items-center gap-1.5"
            >
              Brand Dashboard <ChevronRight className="w-3.5 h-3.5 opacity-50" />
            </Link>
            <Link 
              href="/team" 
              className="px-3.5 py-1.5 rounded-lg border border-white/10 bg-white/[0.02] hover:bg-white/[0.06] text-white/70 hover:text-white transition-colors flex items-center gap-1.5"
            >
              <Users className="w-3.5 h-3.5 text-[#E1D4C0]" /> AI Team (6 Active)
            </Link>
          </div>
        </div>

        {/* Hero Prompt Section — "What are we building?" */}
        <div className="text-center max-w-3xl mx-auto space-y-6 pt-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#E1D4C0]/5 border border-[#E1D4C0]/20 text-[10px] tracking-[0.2em] uppercase text-[#E1D4C0]">
            <Sparkles className="w-3 h-3" /> Creative Operating System
          </div>
          
          <h1 className="text-3xl sm:text-4xl lg:text-5xl font-serif tracking-tight text-white font-light">
            What are we building?
          </h1>
          
          <p className="text-sm sm:text-base text-white/50 font-light max-w-xl mx-auto">
            Describe an idea, campaign objective, or brand challenge. Your persistent AI creative organization will research, design, and direct the workflow.
          </p>

          {/* Conversational Prompt Box */}
          <form onSubmit={handleStart} className="relative max-w-2xl mx-auto group">
            <div className="relative rounded-2xl border border-white/10 bg-[#121212]/90 shadow-2xl p-2 focus-within:border-[#E1D4C0]/50 transition-all duration-300">
              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Tell VYREN what you're working on (e.g. 'Launch a sustainable luxury bridal collection for contemporary India')..."
                rows={3}
                className="w-full bg-transparent resize-none border-none outline-none p-3 text-sm text-white placeholder-white/30 font-light focus:ring-0"
              />
              <div className="flex items-center justify-between pt-2 px-2 border-t border-white/5">
                <div className="flex items-center gap-2 text-[11px] text-white/40">
                  <span className="hover:text-white/70 cursor-pointer" onClick={() => setPrompt("Develop 3 visual directions for our autumn packaging redesign.")}>
                    💡 Packaging Redesign
                  </span>
                  <span>•</span>
                  <span className="hover:text-white/70 cursor-pointer" onClick={() => setPrompt("Audit our last 3 campaigns and propose visual consistency evolutions.")}>
                    🔍 Brand Audit
                  </span>
                </div>

                <button
                  type="submit"
                  disabled={!prompt.trim()}
                  className="px-4 py-2 rounded-xl bg-gradient-to-r from-[#E1D4C0] to-[#C9B99A] text-[#0A0A0A] font-semibold text-xs tracking-wider flex items-center gap-2 hover:opacity-90 transition-opacity disabled:opacity-30 disabled:cursor-not-allowed shadow-md"
                >
                  Start with VYREN <ArrowRight className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          </form>
        </div>

        {/* Two Clear Brand Pathways */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl mx-auto pt-4">
          
          {/* Pathway A: Start a new brand */}
          <div 
            onClick={() => router.push("/brand?modal=new")}
            className="group relative rounded-2xl border border-white/10 bg-[#111111]/80 hover:bg-[#151515] p-6 transition-all duration-300 hover:border-[#E1D4C0]/40 cursor-pointer flex flex-col justify-between"
          >
            <div className="space-y-3">
              <div className="w-10 h-10 rounded-xl bg-[#E1D4C0]/10 border border-[#E1D4C0]/20 flex items-center justify-center text-[#E1D4C0]">
                <PlusCircle className="w-5 h-5" />
              </div>
              <div className="text-base font-medium text-white group-hover:text-[#E1D4C0] transition-colors flex items-center justify-between">
                Start a New Brand
                <ArrowRight className="w-4 h-4 opacity-0 group-hover:opacity-100 group-hover:translate-x-1 transition-all" />
              </div>
              <p className="text-xs text-white/50 font-light leading-relaxed">
                Build an identity from zero. VYREN guides you through market research, positioning, aesthetic token synthesis, and Visual DNA establishment.
              </p>
            </div>
            <div className="pt-4 mt-4 border-t border-white/5 flex items-center gap-2 text-[10px] text-white/40 font-mono">
              <span>0 &rarr; 1 EXPLORATION</span>
              <span>•</span>
              <span>SYNTHESIS</span>
            </div>
          </div>

          {/* Pathway B: Bring an existing brand */}
          <div 
            onClick={() => router.push("/brand?modal=ingest")}
            className="group relative rounded-2xl border border-white/10 bg-[#111111]/80 hover:bg-[#151515] p-6 transition-all duration-300 hover:border-[#E1D4C0]/40 cursor-pointer flex flex-col justify-between"
          >
            <div className="space-y-3">
              <div className="w-10 h-10 rounded-xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-300">
                <UploadCloud className="w-5 h-5" />
              </div>
              <div className="text-base font-medium text-white group-hover:text-[#E1D4C0] transition-colors flex items-center justify-between">
                Bring an Existing Brand
                <ArrowRight className="w-4 h-4 opacity-0 group-hover:opacity-100 group-hover:translate-x-1 transition-all" />
              </div>
              <p className="text-xs text-white/50 font-light leading-relaxed">
                Ingest historical assets, guidelines, and past campaigns. VYREN maps your Brand DNA, detects drift, and recommends evolutionary improvements.
              </p>
            </div>
            <div className="pt-4 mt-4 border-t border-white/5 flex items-center gap-2 text-[10px] text-white/40 font-mono">
              <span>INGESTION</span>
              <span>•</span>
              <span>DRIFT AUDIT</span>
              <span>•</span>
              <span>EVOLUTION</span>
            </div>
          </div>

        </div>

        {/* Quick Context Bento: Brands, Campaigns, AI Team, Intelligence */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-6">
          
          {/* Recent Projects & Campaigns */}
          <div className="rounded-2xl border border-white/10 bg-[#111111]/60 p-5 space-y-4">
            <div className="flex items-center justify-between text-xs">
              <span className="font-medium text-white flex items-center gap-2">
                <FolderKanban className="w-3.5 h-3.5 text-[#E1D4C0]" /> Active Projects
              </span>
              <Link href="/projects" className="text-[10px] text-white/40 hover:text-white transition-colors">View All &rarr;</Link>
            </div>
            
            <div className="space-y-2.5">
              <Link href="/studio" className="block p-3 rounded-xl bg-white/[0.02] hover:bg-white/[0.05] border border-white/5 transition-all">
                <div className="flex items-center justify-between text-xs text-white font-medium">
                  Autumn Lookbook 2026
                  <span className="text-[9px] text-emerald-400 font-mono">In Review</span>
                </div>
                <div className="text-[11px] text-white/40 mt-1">12 multi-surface assets • Banarasi Silk drape study</div>
              </Link>

              <Link href="/campaigns" className="block p-3 rounded-xl bg-white/[0.02] hover:bg-white/[0.05] border border-white/5 transition-all">
                <div className="flex items-center justify-between text-xs text-white font-medium">
                  Heritage Rebrand Campaign
                  <span className="text-[9px] text-amber-400 font-mono">Exploring</span>
                </div>
                <div className="text-[11px] text-white/40 mt-1">3 creative directions synthesized • Outcome model pending</div>
              </Link>
            </div>
          </div>

          {/* AI Creative Workforce Pulse */}
          <div className="rounded-2xl border border-white/10 bg-[#111111]/60 p-5 space-y-4">
            <div className="flex items-center justify-between text-xs">
              <span className="font-medium text-white flex items-center gap-2">
                <Users className="w-3.5 h-3.5 text-blue-400" /> AI Team Activity
              </span>
              <Link href="/team" className="text-[10px] text-white/40 hover:text-white transition-colors">Team Room &rarr;</Link>
            </div>

            <div className="space-y-2.5">
              <div className="p-3 rounded-xl bg-white/[0.02] border border-white/5 space-y-1.5">
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                  <span className="text-xs font-medium text-white">Elena Vance (Creative Director)</span>
                </div>
                <p className="text-[11px] text-white/50 font-light">
                  "Proposed warm tungsten rim lighting adjustments for Autumn Lookbook variations."
                </p>
              </div>

              <div className="p-3 rounded-xl bg-white/[0.02] border border-white/5 space-y-1.5">
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-blue-400" />
                  <span className="text-xs font-medium text-white">Marcus Reed (Brand Strategist)</span>
                </div>
                <p className="text-[11px] text-white/50 font-light">
                  "Completed competitor whitespace audit against 4 European luxury heritage brands."
                </p>
              </div>
            </div>
          </div>

          {/* Intelligence & Visual DNA Summary */}
          <div className="rounded-2xl border border-white/10 bg-[#111111]/60 p-5 space-y-4">
            <div className="flex items-center justify-between text-xs">
              <span className="font-medium text-white flex items-center gap-2">
                <Brain className="w-3.5 h-3.5 text-purple-400" /> Brand Intelligence
              </span>
              <Link href="/visual-dna" className="text-[10px] text-white/40 hover:text-white transition-colors">Visual DNA &rarr;</Link>
            </div>

            <div className="space-y-2.5">
              <div className="p-3 rounded-xl bg-white/[0.02] border border-white/5 space-y-1">
                <div className="text-xs font-medium text-white">Consistency Score: 94%</div>
                <div className="w-full bg-white/10 rounded-full h-1.5 overflow-hidden">
                  <div className="bg-gradient-to-r from-emerald-500 to-[#E1D4C0] h-full rounded-full" style={{ width: "94%" }} />
                </div>
                <div className="text-[10px] text-white/40 pt-1">Strong palette fidelity across social & print channels</div>
              </div>

              <div className="p-3 rounded-xl bg-white/[0.02] border border-white/5 space-y-1">
                <div className="text-xs font-medium text-white">Next Recommended Action</div>
                <p className="text-[11px] text-[#E1D4C0]/80 font-light">
                  Validate 3D drape physics on heavy brocade textiles before final campaign export.
                </p>
              </div>
            </div>
          </div>

        </div>

      </div>
    </div>
  );
}
