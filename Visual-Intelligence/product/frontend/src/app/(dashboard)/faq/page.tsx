"use client";

import { FAQSection } from "@/components/FAQSection";

export default function FAQPage() {
  return (
    <div className="flex-1 h-full flex flex-col px-12 py-12 relative overflow-y-auto scrollbar-none bg-background text-foreground">
      {/* Workspace Breadcrumb */}
      <div className="flex items-center gap-3 text-[10px] tracking-[0.2em] uppercase text-muted-foreground/60 mb-6 shrink-0">
        <span>System</span>
        <span>/</span>
        <span className="text-foreground">FAQ Desk</span>
      </div>

      <div className="flex-1 flex flex-col justify-start">
        <FAQSection />
      </div>
    </div>
  );
}
