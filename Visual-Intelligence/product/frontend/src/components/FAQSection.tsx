"use client";

import { useState } from "react";
import { ChevronDown, HelpCircle } from "lucide-react";
import { cn } from "@/lib/utils";

interface FAQItem {
  question: string;
  answer: string;
}

const FAQ_ITEMS: FAQItem[] = [
  {
    question: "What is Mercer AI and how does it operate?",
    answer: "Mercer AI is an advanced collaborative visual intelligence platform. It brings together textile physics, material analysis, and multi-agent AI pipelines to synthesize high-end fashion and lifestyle campaign imagery from design specifications."
  },
  {
    question: "How does the Material DNA engine analyze fabrics?",
    answer: "By uploading high-resolution photos or scans of textiles (such as Silk, Linen, or Tweed), our Material-DNA agent processes weave techniques, thread densities, and physical textures to extract a digital profile that ensures rendering accuracy."
  },
  {
    question: "What are the roles of the different agents in Team Mode?",
    answer: "Team Mode enables a pipeline of 8 specialist agents (including Brand-DNA, Material-DNA, Visual-DNA, Art Director, and Campaign Strategist). Each agent handles a specific step of the creative direction, composition, copywriting, and quality validation."
  },
  {
    question: "How do generation credits work?",
    answer: "Each visual synthesis consumes credits based on rendering complexity, active agents in the pipeline, aspect ratios, and output quantity. You can monitor your consumption in the main billing dashboard."
  }
];

export function FAQSection() {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  const toggleIndex = (index: number) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  return (
    <section className="w-full py-24 px-6 md:px-12 bg-black border-t border-white/5 relative z-10">
      <div className="max-w-4xl mx-auto w-full flex flex-col gap-12">
        {/* Section Header */}
        <div className="flex flex-col gap-2 text-center items-center">
          <div className="w-10 h-10 rounded-full bg-[#E1D4C0]/5 border border-[#E1D4C0]/15 flex items-center justify-center mb-2">
            <HelpCircle size={16} className="text-[#E1D4C0]" />
          </div>
          <span className="text-[10px] font-mono tracking-[0.3em] uppercase text-white/30">
            Information Desk
          </span>
          <h2 className="text-3xl font-serif tracking-wide text-[#E1D4C0] font-light">
            Frequently Asked Questions
          </h2>
        </div>

        {/* Accordion List */}
        <div className="flex flex-col gap-3">
          {FAQ_ITEMS.map((item, idx) => {
            const isOpen = openIndex === idx;

            return (
              <div
                key={idx}
                className={cn(
                  "border border-white/10 hover:border-[#E1D4C0]/25 rounded-2xl bg-white/[0.01] hover:bg-white/[0.02] transition-all duration-300 overflow-hidden",
                  isOpen && "border-[#E1D4C0]/40 bg-white/[0.02]"
                )}
              >
                {/* Accordion Trigger */}
                <button
                  onClick={() => toggleIndex(idx)}
                  className="w-full flex items-center justify-between p-6 text-left cursor-pointer transition-colors"
                >
                  <span className="text-[13px] font-sans font-light tracking-wide text-white/90 group-hover:text-white transition-colors">
                    {item.question}
                  </span>
                  <ChevronDown
                    size={16}
                    className={cn(
                      "text-white/30 transition-transform duration-300",
                      isOpen && "transform rotate-180 text-[#E1D4C0]"
                    )}
                  />
                </button>

                {/* Accordion Content */}
                <div
                  className={cn(
                    "grid transition-all duration-300 ease-in-out",
                    isOpen ? "grid-rows-[1fr] opacity-100" : "grid-rows-[0fr] opacity-0"
                  )}
                >
                  <div className="overflow-hidden">
                    <p className="px-6 pb-6 pt-1 text-[11.5px] font-sans text-white/40 leading-relaxed font-light">
                      {item.answer}
                    </p>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
