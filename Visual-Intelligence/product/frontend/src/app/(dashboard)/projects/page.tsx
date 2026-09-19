"use client";

import { useState } from "react";
import Link from "next/link";
import { 
  FolderKanban, 
  Plus, 
  ArrowRight, 
  CheckCircle2, 
  Clock, 
  Layers, 
  Palette, 
  Sparkles, 
  Filter, 
  Search
} from "lucide-react";

export default function ProjectsPage() {
  const [filter, setFilter] = useState<"all" | "active" | "review" | "completed">("all");

  const projects = [
    {
      id: "PRJ-2026-01",
      title: "Autumn Lookbook 2026",
      category: "Campaign Production",
      brand: "AURA Couture",
      status: "In Review",
      progress: 85,
      assets: 12,
      coworkers: ["Elena Vance", "Aria Chen"],
      updated: "2 hours ago"
    },
    {
      id: "PRJ-2026-02",
      title: "Sustainable Packaging Redesign",
      category: "Visual Identity",
      brand: "AURA Couture",
      status: "Active",
      progress: 45,
      assets: 8,
      coworkers: ["Marcus Reed", "Elena Vance"],
      updated: "Yesterday"
    },
    {
      id: "PRJ-2026-03",
      title: "Heritage Brocade Drape Simulation",
      category: "Visual DNA Research",
      brand: "AURA Couture",
      status: "Active",
      progress: 60,
      assets: 16,
      coworkers: ["Aria Chen"],
      updated: "3 days ago"
    },
    {
      id: "PRJ-2026-04",
      title: "Summer Resort Wear Global Launch",
      category: "Omnichannel Campaign",
      brand: "AURA Couture",
      status: "Completed",
      progress: 100,
      assets: 24,
      coworkers: ["Elena Vance", "Marcus Reed", "David Ross"],
      updated: "1 week ago"
    }
  ];

  return (
    <div className="h-full overflow-y-auto bg-background text-foreground p-8 lg:p-12 scrollbar-thin">
      <div className="max-w-6xl mx-auto space-y-8">
        
        {/* Header */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-6 border-b border-border">
          <div>
            <div className="flex items-center gap-2">
              <FolderKanban className="w-5 h-5 text-primary" />
              <h1 className="text-2xl font-serif text-foreground font-light">Creative Projects</h1>
            </div>
            <p className="text-xs text-muted-foreground font-light mt-1">
              Track creative briefs, asset development pipelines, and multi-agent production workflows.
            </p>
          </div>

          <Link
            href="/studio"
            className="px-4 py-2 rounded-xl bg-primary text-primary-foreground text-xs font-semibold hover:opacity-90 transition-opacity flex items-center gap-2 shadow-sm"
          >
            <Plus className="w-4 h-4" /> New Creative Project
          </Link>
        </div>

        {/* Filter & Search Bar */}
        <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <button
              onClick={() => setFilter("all")}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors cursor-pointer ${
                filter === "all" ? "bg-primary text-primary-foreground font-semibold" : "bg-muted text-muted-foreground hover:text-foreground"
              }`}
            >
              All Projects
            </button>
            <button
              onClick={() => setFilter("active")}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors cursor-pointer ${
                filter === "active" ? "bg-primary text-primary-foreground font-semibold" : "bg-muted text-muted-foreground hover:text-foreground"
              }`}
            >
              Active
            </button>
            <button
              onClick={() => setFilter("review")}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors cursor-pointer ${
                filter === "review" ? "bg-primary text-primary-foreground font-semibold" : "bg-muted text-muted-foreground hover:text-foreground"
              }`}
            >
              In Review
            </button>
            <button
              onClick={() => setFilter("completed")}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors cursor-pointer ${
                filter === "completed" ? "bg-primary text-primary-foreground font-semibold" : "bg-muted text-muted-foreground hover:text-foreground"
              }`}
            >
              Completed
            </button>
          </div>

          <div className="relative">
            <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
            <input
              type="text"
              placeholder="Search projects..."
              className="pl-9 pr-4 py-1.5 rounded-xl bg-card border border-border text-xs text-foreground placeholder:text-muted-foreground outline-none focus:border-primary shadow-xs"
            />
          </div>
        </div>

        {/* Project Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {projects.map((p) => (
            <div 
              key={p.id}
              className="rounded-2xl border border-border bg-card hover:border-primary/40 p-6 space-y-4 transition-all duration-300 flex flex-col justify-between shadow-sm"
            >
              <div className="space-y-3">
                <div className="flex items-center justify-between text-xs">
                  <span className="text-[10px] font-mono text-primary uppercase tracking-wider font-semibold">{p.category}</span>
                  <span className={`px-2 py-0.5 rounded text-[9px] font-mono tracking-wider font-medium ${
                    p.status === "In Review" ? "bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 border border-emerald-500/20" :
                    p.status === "Completed" ? "bg-blue-500/10 text-blue-700 dark:text-blue-400 border border-blue-500/20" :
                    "bg-amber-500/10 text-amber-700 dark:text-amber-400 border border-amber-500/20"
                  }`}>
                    {p.status}
                  </span>
                </div>

                <h3 className="text-base font-medium text-foreground">{p.title}</h3>
                
                {/* Progress bar */}
                <div className="space-y-1">
                  <div className="flex items-center justify-between text-[10px] text-muted-foreground font-mono">
                    <span>Progress</span>
                    <span className="text-foreground font-medium">{p.progress}%</span>
                  </div>
                  <div className="w-full bg-muted rounded-full h-1.5 overflow-hidden">
                    <div className="bg-primary h-full rounded-full" style={{ width: `${p.progress}%` }} />
                  </div>
                </div>
              </div>

              <div className="pt-4 border-t border-border flex items-center justify-between text-xs text-muted-foreground">
                <div className="flex items-center gap-1.5">
                  <span className="text-[10px] font-mono">{p.assets} Assets</span>
                  <span>•</span>
                  <span className="text-[10px] font-mono">{p.coworkers.join(", ")}</span>
                </div>

                <Link 
                  href="/studio"
                  className="text-[11px] text-primary hover:underline flex items-center gap-1 font-medium"
                >
                  Open Studio <ArrowRight className="w-3 h-3" />
                </Link>
              </div>
            </div>
          ))}
        </div>

      </div>
    </div>
  );
}
