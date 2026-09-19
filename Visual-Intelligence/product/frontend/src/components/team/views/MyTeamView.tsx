"use client";

import React, { useState } from "react";
import { 
  Users, 
  Filter, 
  Search, 
  Sparkles,
  Sliders,
  CheckCircle2
} from "lucide-react";
import type { Coworker, DepartmentName } from "@/lib/teamFixtures";
import { CoworkerCard } from "@/components/team/CoworkerCard";

interface MyTeamViewProps {
  coworkers: Coworker[];
  onSelectCoworker: (coworker: Coworker) => void;
  onOpenChat: (coworker: Coworker) => void;
}

export function MyTeamView({
  coworkers,
  onSelectCoworker,
  onOpenChat
}: MyTeamViewProps) {
  const [selectedDept, setSelectedDept] = useState<DepartmentName | 'All'>('All');
  const [searchQuery, setSearchQuery] = useState("");

  const departments: (DepartmentName | 'All')[] = [
    'All', 
    'Creative', 
    'Strategy', 
    'Intelligence', 
    'Production', 
    'Quality'
  ];

  const filteredCoworkers = coworkers.filter(c => {
    const matchesDept = selectedDept === 'All' || c.department === selectedDept;
    const matchesSearch = searchQuery === "" || 
      c.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      c.role.toLowerCase().includes(searchQuery.toLowerCase()) ||
      c.currentWork.task.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesDept && matchesSearch;
  });

  return (
    <div className="space-y-6 animate-in fade-in duration-200">
      
      {/* Search & Department Filters Toolbar */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 p-4 rounded-2xl bg-card border border-border shadow-sm">
        
        {/* Department Filter Pills */}
        <div className="flex items-center gap-1.5 flex-wrap">
          {departments.map((dept) => (
            <button
              key={dept}
              onClick={() => setSelectedDept(dept)}
              className={`px-3 py-1.5 rounded-xl text-xs font-mono transition-all border cursor-pointer ${
                selectedDept === dept
                  ? "bg-primary text-primary-foreground font-bold border-primary shadow-sm"
                  : "bg-muted/40 text-muted-foreground border-border hover:text-foreground hover:bg-accent"
              }`}
            >
              {dept === 'All' ? 'All Departments' : dept}
            </button>
          ))}
        </div>

        {/* Quick Search */}
        <div className="relative w-full sm:w-64">
          <Search className="w-3.5 h-3.5 text-muted-foreground/60 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search coworker or skill..."
            className="w-full pl-8 pr-3 py-1.5 rounded-xl bg-muted/40 border border-border text-xs text-foreground placeholder:text-muted-foreground/50 focus:outline-none focus:border-primary/50"
          />
        </div>

      </div>

      {/* Coworker Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredCoworkers.map((coworker) => (
          <CoworkerCard
            key={coworker.id}
            coworker={coworker}
            onSelect={onSelectCoworker}
            onOpenChat={onOpenChat}
          />
        ))}
      </div>

    </div>
  );
}
