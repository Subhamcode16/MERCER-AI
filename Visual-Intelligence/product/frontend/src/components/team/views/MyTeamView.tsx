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
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 p-4 rounded-2xl bg-[#111113]/80 border border-white/10">
        
        {/* Department Filter Pills */}
        <div className="flex items-center gap-1.5 flex-wrap">
          {departments.map((dept) => (
            <button
              key={dept}
              onClick={() => setSelectedDept(dept)}
              className={`px-3 py-1.5 rounded-xl text-xs font-mono transition-all border ${
                selectedDept === dept
                  ? "bg-[#E1D4C0] text-[#0A0A0A] font-bold border-[#E1D4C0]"
                  : "bg-white/[0.02] text-white/50 border-white/5 hover:text-white"
              }`}
            >
              {dept === 'All' ? 'All Departments' : dept}
            </button>
          ))}
        </div>

        {/* Quick Search */}
        <div className="relative w-full sm:w-64">
          <Search className="w-3.5 h-3.5 text-white/40 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search coworker or skill..."
            className="w-full pl-8 pr-3 py-1.5 rounded-xl bg-white/[0.03] border border-white/10 text-xs text-white placeholder-white/30 focus:outline-none focus:border-[#E1D4C0]/50"
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
