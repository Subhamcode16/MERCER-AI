"use client";

import { useState } from "react";
import Link from "next/link";
import { 
  Activity, 
  Bell, 
  ShieldCheck, 
  Users, 
  CheckCircle2, 
  Clock, 
  Sparkles,
  Filter,
  ArrowRight
} from "lucide-react";

export default function ActivityPage() {
  const [filter, setFilter] = useState<"all" | "team" | "decisions" | "system">("all");

  const events = [
    {
      id: "EVT-001",
      type: "decision",
      title: "Decision Approved: DEC-2026-089 (Banarasi Drape Tokens)",
      author: "Subham Rath (Creative Director)",
      time: "10 minutes ago",
      details: "Cryptographic consensus verified on block #892014. Zero drift detected.",
      tag: "Governance"
    },
    {
      id: "EVT-002",
      type: "team",
      title: "Elena Vance (Creative Director) submitted 4 Lookbook Variations",
      author: "AI Creative Workforce",
      time: "45 minutes ago",
      details: "Applied tungsten lighting presets and Banarasi brocade drape physics shaders.",
      tag: "Production"
    },
    {
      id: "EVT-003",
      type: "team",
      title: "Marcus Reed (Brand Strategist) updated Competitor Whitespace Map",
      author: "AI Creative Workforce",
      time: "2 hours ago",
      details: "Identified high-intent consumer demand for artisanal sheer organza overlays.",
      tag: "Intelligence"
    },
    {
      id: "EVT-004",
      type: "system",
      title: "Automatic Freshness & Drift Scan Completed",
      author: "VYREN Institutional Engine",
      time: "5 hours ago",
      details: "Brand consistency rated at 96.4%. No unauthorized semantic mutations found.",
      tag: "Audit"
    }
  ];

  return (
    <div className="h-full overflow-y-auto bg-background text-foreground p-8 lg:p-12 scrollbar-thin">
      <div className="max-w-4xl mx-auto space-y-8">
        
        {/* Header */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-6 border-b border-border">
          <div>
            <div className="flex items-center gap-2">
              <Activity className="w-5 h-5 text-primary" />
              <h1 className="text-2xl font-serif text-foreground font-light">Workspace Activity</h1>
            </div>
            <p className="text-xs text-muted-foreground font-light mt-1">
              Live event stream of AI coworker contributions, human governance decisions, and organizational audit logs.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setFilter("all")}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                filter === "all" ? "bg-primary/10 text-primary border border-primary/20" : "text-muted-foreground hover:text-foreground"
              }`}
            >
              All Events
            </button>
            <button
              onClick={() => setFilter("team")}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                filter === "team" ? "bg-primary/10 text-primary border border-primary/20" : "text-muted-foreground hover:text-foreground"
              }`}
            >
              AI Team
            </button>
            <button
              onClick={() => setFilter("decisions")}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                filter === "decisions" ? "bg-primary/10 text-primary border border-primary/20" : "text-muted-foreground hover:text-foreground"
              }`}
            >
              Decisions
            </button>
          </div>
        </div>

        {/* Activity Timeline */}
        <div className="space-y-4">
          {events.map((evt) => (
            <div 
              key={evt.id}
              className="p-5 rounded-2xl border border-border bg-card hover:border-primary/30 transition-all space-y-2 shadow-xs"
            >
              <div className="flex items-center justify-between text-xs">
                <div className="flex items-center gap-2">
                  <span className={`w-2 h-2 rounded-full ${
                    evt.type === "decision" ? "bg-emerald-500" :
                    evt.type === "team" ? "bg-primary" : "bg-purple-500"
                  }`} />
                  <span className="font-medium text-foreground">{evt.author}</span>
                </div>
                <span className="text-[10px] text-muted-foreground font-mono">{evt.time}</span>
              </div>

              <h3 className="text-sm font-medium text-foreground">{evt.title}</h3>
              <p className="text-xs text-muted-foreground font-light">{evt.details}</p>

              <div className="pt-2 flex items-center justify-between text-[10px] text-muted-foreground font-mono">
                <span>{evt.id} • {evt.tag}</span>
                {evt.type === "team" && (
                  <Link href="/team" className="text-primary hover:underline flex items-center gap-1 font-medium">
                    View in Team Room <ArrowRight className="w-2.5 h-2.5" />
                  </Link>
                )}
              </div>
            </div>
          ))}
        </div>

      </div>
    </div>
  );
}
