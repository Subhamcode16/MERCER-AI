"use client";

import React from "react";
import { VisualKnowledgeDashboard } from "@/components/phase20/VisualKnowledgeDashboard";

export default function KnowledgePage() {
  return (
    <div className="flex-1 h-full flex flex-col p-8 overflow-y-auto scrollbar-none">
      {/* Workspace Breadcrumb */}
      <div className="flex items-center gap-3 text-[10px] tracking-[0.2em] uppercase text-white/30 mb-6 select-none">
        <span>Institution</span>
        <span>/</span>
        <span className="text-white/60">Knowledge & Failure Taxonomy</span>
      </div>

      {/* Visual Knowledge Benchmark Component */}
      <VisualKnowledgeDashboard />
    </div>
  );
}
