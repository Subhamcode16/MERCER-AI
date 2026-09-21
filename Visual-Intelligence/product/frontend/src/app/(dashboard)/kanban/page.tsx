"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import { 
  Columns3, 
  Sparkles, 
  Bot, 
  Eye, 
  Activity, 
  CheckCircle2, 
  Clock, 
  ArrowLeft 
} from "lucide-react";
import { KanbanBoard, type KanbanColumn } from "@/components/ui/kanban-board";

const portraits = {
  sarah: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150&auto=format&fit=crop&q=80",
  michael: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80",
  emily: "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150&auto=format&fit=crop&q=80",
  daniel: "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&auto=format&fit=crop&q=80",
  olivia: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80",
} as const;

const people = {
  sarah: { name: "Sarah Anderson", avatar: portraits.sarah },
  michael: { name: "Michael Carter", avatar: portraits.michael },
  emily: { name: "Emily Thompson", avatar: portraits.emily },
  daniel: { name: "Daniel Wilson", avatar: portraits.daniel },
  olivia: { name: "Olivia Martinez", avatar: portraits.olivia },
};

const canonicalColumns: KanbanColumn[] = [
  {
    id: "backlog",
    name: "Backlog",
    accent: "slate",
    tasks: [
      {
        id: "t1",
        title: "Audit empty states",
        note: "Every list, table and search result",
        priority: "low",
        category: "Web app",
        icon: "web",
        assignees: [people.emily],
        due: "12 Oct",
        progress: 0,
      },
      {
        id: "t2",
        title: "Usage based billing",
        note: "Metered plans and overage alerts",
        priority: "normal",
        category: "Dashboard",
        icon: "dashboard",
        assignees: [people.michael, people.daniel],
        due: "18 Oct",
        progress: 0,
      },
      {
        id: "t3",
        title: "Offline mode spike",
        note: "How much can we cache safely?",
        priority: "low",
        category: "Mobile",
        icon: "mobile",
        assignees: [people.daniel],
        due: "24 Oct",
        progress: 0,
      },
    ],
  },
  {
    id: "plan",
    name: "Plan",
    accent: "blue",
    tasks: [
      {
        id: "t4",
        title: "Onboarding checklist",
        note: "Five steps to first value",
        priority: "high",
        category: "Web app",
        icon: "web",
        assignees: [people.sarah, people.emily],
        due: "3 Oct",
        progress: 10,
      },
      {
        id: "t5",
        title: "Design tokens v2",
        note: "Colour, spacing and radius from one source",
        priority: "normal",
        category: "Brand",
        icon: "brand",
        assignees: [people.emily, people.olivia],
        due: "7 Oct",
        progress: 0,
      },
    ],
  },
  {
    id: "inprogress",
    name: "In Progress",
    accent: "violet",
    tasks: [
      {
        id: "t6",
        title: "Team permissions",
        note: "Roles, seats and the invite flow",
        priority: "urgent",
        category: "Dashboard",
        icon: "dashboard",
        assignees: [people.michael, people.sarah, people.daniel],
        due: "Tomorrow",
        dueSoon: true,
        progress: 60,
      },
      {
        id: "t7",
        title: "Search across workspaces",
        note: "Debounced, with recent results",
        priority: "high",
        category: "Web app",
        icon: "web",
        assignees: [people.daniel],
        due: "2 Oct",
        progress: 35,
      },
      {
        id: "t8",
        title: "Mobile push setup",
        note: "APNs and FCM behind one service",
        priority: "normal",
        category: "Mobile",
        icon: "mobile",
        assignees: [people.olivia, people.michael],
        due: "5 Oct",
        progress: 20,
      },
    ],
  },
  {
    id: "review",
    name: "In Review",
    accent: "amber",
    tasks: [
      {
        id: "t9",
        title: "API rate limits",
        note: "Per key, per minute, with headers",
        priority: "high",
        category: "Infra",
        icon: "infra",
        assignees: [people.michael],
        due: "Today",
        dueSoon: true,
        progress: 90,
      },
      {
        id: "t10",
        title: "Changelog page",
        note: "Filterable by product area",
        priority: "low",
        category: "Docs",
        icon: "docs",
        assignees: [people.emily, people.sarah],
        due: "4 Oct",
        progress: 80,
      },
    ],
  },
  {
    id: "done",
    name: "Done",
    accent: "emerald",
    tasks: [
      {
        id: "t11",
        title: "SSO with Okta",
        note: "SAML sign in and SCIM provisioning",
        priority: "high",
        category: "Infra",
        icon: "infra",
        assignees: [people.daniel, people.michael],
        due: "26 Sep",
        progress: 100,
      },
      {
        id: "t12",
        title: "Billing history export",
        note: "CSV and PDF invoices",
        priority: "normal",
        category: "Dashboard",
        icon: "dashboard",
        assignees: [people.olivia],
        due: "22 Sep",
        progress: 100,
      },
    ],
  },
];

const MOTION_SPRING = { type: "spring", stiffness: 420, damping: 28, mass: 0.8 } as const;

/**
 * Genjutsu Animated Rolling Ticker
 * Seamless vertical number rolling with subtle spring easing and blur-fade physics.
 */
function RollingTicker({ 
  value, 
  suffix = "", 
  className = "" 
}: { 
  value: string | number; 
  suffix?: React.ReactNode; 
  className?: string;
}) {
  return (
    <div className={`inline-flex items-baseline overflow-hidden h-[1.25em] ${className}`}>
      <AnimatePresence mode="popLayout" initial={false}>
        <motion.span
          key={String(value)}
          initial={{ y: "80%", opacity: 0, filter: "blur(4px)" }}
          animate={{ y: "0%", opacity: 1, filter: "blur(0px)" }}
          exit={{ y: "-80%", opacity: 0, filter: "blur(4px)" }}
          transition={MOTION_SPRING}
          className="inline-block tabular-nums"
        >
          {value}
        </motion.span>
      </AnimatePresence>
      {suffix && <span className="ml-1.5">{suffix}</span>}
    </div>
  );
}

export default function KanbanPage() {
  const [columns] = useState<KanbanColumn[]>(canonicalColumns);
  const [activeFilter, setActiveFilter] = useState<"all" | "high" | "active">("all");

  // Live telemetry dynamic states (simulating agent real-time streaming)
  const [taskCount, setTaskCount] = useState(12);
  const [activeAgents, setActiveAgents] = useState(5);
  const [velocity, setVelocity] = useState("1.2");
  const [compliance, setCompliance] = useState("99.8");
  const [pulsePing, setPulsePing] = useState(false);

  useEffect(() => {
    const interval = setInterval(() => {
      setPulsePing(true);
      setTimeout(() => setPulsePing(false), 900);

      // Micro-jitter to simulate agent actions in real time
      setTaskCount((prev) => {
        const delta = Math.random() > 0.6 ? 1 : Math.random() < 0.3 ? -1 : 0;
        return Math.max(10, Math.min(16, prev + delta));
      });

      if (Math.random() > 0.7) {
        setActiveAgents((prev) => (prev === 5 ? 6 : prev === 6 ? 4 : 5));
      }

      if (Math.random() > 0.6) {
        const vels = ["1.1", "1.2", "1.3", "0.9", "1.4"];
        setVelocity(vels[Math.floor(Math.random() * vels.length)]);
      }

      if (Math.random() > 0.8) {
        const comps = ["99.8", "99.9", "99.7", "100"];
        setCompliance(comps[Math.floor(Math.random() * comps.length)]);
      }
    }, 4500);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="w-full h-full min-h-screen overflow-y-auto font-sans bg-transparent text-[var(--ink)] pt-24 sm:pt-28 pb-20 px-6 sm:px-10 lg:px-14 scrollbar-thin">
      <div className="w-full max-w-[1700px] mx-auto space-y-8">
        
        {/* Breadcrumb & Navigation */}
        <div className="flex items-center justify-between">
          <Link
            href="/studio"
            className="inline-flex items-center gap-1.5 text-xs font-medium text-[var(--muted)] hover:text-[var(--ink)] transition-colors group"
          >
            <ArrowLeft size={13} className="transition-transform group-hover:-translate-x-0.5" />
            <span>Back to Studio</span>
          </Link>

          <div className="flex items-center gap-2.5">
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[11px] font-mono font-medium bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20 shadow-xs">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
                <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500" />
              </span>
              LIVE AGENT STREAM
            </span>
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-[var(--soft)] text-[var(--ink)] text-[11px] font-mono font-medium border border-[var(--line)] shadow-xs">
              <Eye className="w-3.5 h-3.5 text-blue-500 dark:text-blue-400" />
              <span>Permission: <strong>View-Only</strong></span>
            </div>
          </div>
        </div>

        {/* Header Hero Section */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 pb-4 border-b border-[var(--line)]">
          <div>
            <div className="flex items-center gap-3">
              <div className="p-2.5 rounded-2xl bg-[var(--accent)] text-[var(--accent-ink)] shadow-sm">
                <Columns3 className="w-6 h-6" />
              </div>
              <div>
                <h1 className="text-2xl sm:text-3xl font-semibold tracking-tight text-[var(--ink)]">
                  Kanban Board
                </h1>
                <p className="text-xs sm:text-sm text-[var(--muted)] font-normal mt-1">
                  Real-time pipeline board &middot; Task moves and executions are updated dynamically by agents.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Live Telemetry Metric Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          
          {/* Active Tasks */}
          <motion.div 
            whileHover={{ y: -2, scale: 1.012 }}
            transition={MOTION_SPRING}
            className="group relative p-4 rounded-2xl bg-[var(--surface)] border border-[var(--line)] shadow-xs flex items-center justify-between overflow-hidden"
          >
            <div className="space-y-1">
              <span className="text-[10.5px] font-mono font-medium uppercase tracking-widest text-[var(--muted)]">
                Active Tasks
              </span>
              <div className="text-2xl sm:text-[26px] font-normal tracking-tight text-[var(--ink)] leading-none">
                <RollingTicker value={taskCount} />
              </div>
            </div>
            <div className="relative p-2.5 rounded-xl bg-blue-500/10 text-blue-500 dark:text-blue-400 transition-transform duration-200 group-hover:scale-110">
              {pulsePing && (
                <span className="absolute inset-0 rounded-xl bg-blue-500/20 animate-ping" />
              )}
              <Activity className="w-5 h-5 relative z-10" />
            </div>
          </motion.div>

          {/* Active Agents */}
          <motion.div 
            whileHover={{ y: -2, scale: 1.012 }}
            transition={MOTION_SPRING}
            className="group relative p-4 rounded-2xl bg-[var(--surface)] border border-[var(--line)] shadow-xs flex items-center justify-between overflow-hidden"
          >
            <div className="space-y-1">
              <span className="text-[10.5px] font-mono font-medium uppercase tracking-widest text-[var(--muted)]">
                Active Agents
              </span>
              <div className="text-2xl sm:text-[26px] font-normal tracking-tight text-[var(--ink)] leading-none">
                <RollingTicker 
                  value={activeAgents} 
                  suffix={<span className="text-sm font-normal text-[var(--muted)]">Collaborating</span>} 
                />
              </div>
            </div>
            <div className="relative p-2.5 rounded-xl bg-violet-500/10 text-violet-500 dark:text-violet-400 transition-transform duration-200 group-hover:scale-110">
              {pulsePing && (
                <span className="absolute inset-0 rounded-xl bg-violet-500/20 animate-ping" />
              )}
              <Bot className="w-5 h-5 relative z-10" />
            </div>
          </motion.div>

          {/* Average Velocity */}
          <motion.div 
            whileHover={{ y: -2, scale: 1.012 }}
            transition={MOTION_SPRING}
            className="group relative p-4 rounded-2xl bg-[var(--surface)] border border-[var(--line)] shadow-xs flex items-center justify-between overflow-hidden"
          >
            <div className="space-y-1">
              <span className="text-[10.5px] font-mono font-medium uppercase tracking-widest text-[var(--muted)]">
                Average Velocity
              </span>
              <div className="text-2xl sm:text-[26px] font-normal tracking-tight text-[var(--ink)] leading-none">
                <RollingTicker 
                  value={`${velocity}m`} 
                  suffix={<span className="text-sm font-normal text-[var(--muted)]">/ Task</span>} 
                />
              </div>
            </div>
            <div className="relative p-2.5 rounded-xl bg-amber-500/10 text-amber-500 dark:text-amber-400 transition-transform duration-200 group-hover:scale-110">
              {pulsePing && (
                <span className="absolute inset-0 rounded-xl bg-amber-500/20 animate-ping" />
              )}
              <Clock className="w-5 h-5 relative z-10" />
            </div>
          </motion.div>

          {/* Compliance Rate */}
          <motion.div 
            whileHover={{ y: -2, scale: 1.012 }}
            transition={MOTION_SPRING}
            className="group relative p-4 rounded-2xl bg-[var(--surface)] border border-[var(--line)] shadow-xs flex items-center justify-between overflow-hidden"
          >
            <div className="space-y-1">
              <span className="text-[10.5px] font-mono font-medium uppercase tracking-widest text-[var(--muted)]">
                Compliance Rate
              </span>
              <div className="text-2xl sm:text-[26px] font-normal tracking-tight text-[var(--ink)] leading-none">
                <RollingTicker 
                  value={`${compliance}%`} 
                />
              </div>
            </div>
            <div className="relative p-2.5 rounded-xl bg-emerald-500/10 text-emerald-500 dark:text-emerald-400 transition-transform duration-200 group-hover:scale-110">
              {pulsePing && (
                <span className="absolute inset-0 rounded-xl bg-emerald-500/20 animate-ping" />
              )}
              <CheckCircle2 className="w-5 h-5 relative z-10" />
            </div>
          </motion.div>

        </div>

        {/* Pipeline Controls & Uncontained Full-Width Board Section */}
        <div className="space-y-4 pt-2">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-2">
            <div className="flex items-center gap-3">
              <span className="text-xs font-mono font-medium uppercase tracking-wider text-[var(--ink)]">
                Workflow Pipeline
              </span>
              <span className="px-2.5 py-0.5 rounded-full text-[10px] font-mono font-medium bg-[var(--soft)] text-[var(--muted)] border border-[var(--line)]">
                5 Stages
              </span>
            </div>
            
            <div className="flex items-center gap-1.5 bg-[var(--soft)] p-1 rounded-xl border border-[var(--line)]">
              <button 
                onClick={() => setActiveFilter("all")}
                className={`px-3 py-1 rounded-lg text-xs font-medium transition-all ${
                  activeFilter === "all" 
                    ? "bg-[var(--surface)] text-[var(--ink)] shadow-2xs border border-[var(--line)]" 
                    : "text-[var(--muted)] hover:text-[var(--ink)]"
                }`}
              >
                All Stages
              </button>
              <button 
                onClick={() => setActiveFilter("high")}
                className={`px-3 py-1 rounded-lg text-xs font-medium transition-all ${
                  activeFilter === "high" 
                    ? "bg-[var(--surface)] text-[var(--ink)] shadow-2xs border border-[var(--line)]" 
                    : "text-[var(--muted)] hover:text-[var(--ink)]"
                }`}
              >
                High Priority
              </button>
              <button 
                onClick={() => setActiveFilter("active")}
                className={`px-3 py-1 rounded-lg text-xs font-medium transition-all ${
                  activeFilter === "active" 
                    ? "bg-[var(--surface)] text-[var(--ink)] shadow-2xs border border-[var(--line)]" 
                    : "text-[var(--muted)] hover:text-[var(--ink)]"
                }`}
              >
                In Progress
              </button>
            </div>
          </div>

          {/* KanbanBoard Uncontained with Full Horizontal Breathability */}
          <div className="w-full">
            <KanbanBoard 
              columns={columns} 
              readOnly={true}
              label="Project Workflow Board" 
            />
          </div>
        </div>

      </div>
    </div>
  );
}
