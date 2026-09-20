"use client";

import React from "react";
import { VyrenWorkspace } from "@/components/workspace/App";

export default function StudioPage() {
  return (
    <div className="w-full h-full min-h-screen flex flex-col bg-[var(--paper)] text-[var(--ink)] overflow-hidden pt-16">
      <VyrenWorkspace />
    </div>
  );
}
