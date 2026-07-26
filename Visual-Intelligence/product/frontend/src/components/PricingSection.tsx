"use client";

import { useRef, useState } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/dist/ScrollTrigger';
import { useGSAP } from '@gsap/react';
import { PricingComponent, BillingCycle, PriceTier } from '@/components/ui/pricing-card';

gsap.registerPlugin(ScrollTrigger);

const pricingPlans: [PriceTier, PriceTier, PriceTier] = [
  {
    id: "essential",
    name: "Starter",
    description: "For independent creators & discovery.",
    priceMonthly: 12,
    priceAnnually: 9,
    isPopular: false,
    buttonLabel: "Begin Trial",
    features: [
      { name: "Monthly Credits", isIncluded: true, stringValue: "200" },
      { name: "AI Models Available", isIncluded: true, stringValue: "Nano Banana 2 & GPT-4o" },
      { name: "Export Resolution", isIncluded: true, stringValue: "Standard" },
      { name: "Real-time Generation", isIncluded: true },
      { name: "Batch Priority Routing", isIncluded: false },
      { name: "Dedicated Tech Director", isIncluded: false },
    ],
  },
  {
    id: "professional",
    name: "Pro",
    description: "The standard for professional output.",
    priceMonthly: 35,
    priceAnnually: 27,
    isPopular: true,
    buttonLabel: "Select Pro",
    features: [
      { name: "Monthly Credits", isIncluded: true, stringValue: "800" },
      { name: "AI Models Available", isIncluded: true, stringValue: "All Models" },
      { name: "Export Resolution", isIncluded: true, stringValue: "4K Cinematic" },
      { name: "Real-time Generation", isIncluded: true },
      { name: "Batch Priority Routing", isIncluded: false },
      { name: "Dedicated Tech Director", isIncluded: false },
    ],
  },
  {
    id: "atelier",
    name: "Studio",
    description: "For agencies and high-volume teams.",
    priceMonthly: 85,
    priceAnnually: 64,
    isPopular: false,
    buttonLabel: "Select Studio",
    features: [
      { name: "Monthly Credits", isIncluded: true, stringValue: "2,500" },
      { name: "AI Models Available", isIncluded: true, stringValue: "All Models" },
      { name: "Export Resolution", isIncluded: true, stringValue: "8K Cinematic" },
      { name: "Real-time Generation", isIncluded: true },
      { name: "Batch Priority Routing", isIncluded: true },
      { name: "Dedicated Tech Director", isIncluded: true },
    ],
  }
];

export function PricingSection() {
  const sectionRef = useRef<HTMLElement>(null);
  const textRef = useRef<HTMLDivElement>(null);
  const [billingCycle, setBillingCycle] = useState<BillingCycle>('monthly');

  useGSAP(() => {
    if (!sectionRef.current) return;

    // Headline Reveal
    if (textRef.current) {
      gsap.fromTo(textRef.current.children, 
        { y: 40, opacity: 0 },
        {
          y: 0,
          opacity: 1,
          duration: 1.2,
          stagger: 0.15,
          ease: "power3.out",
          scrollTrigger: {
            trigger: textRef.current,
            start: "top 80%",
          }
        }
      );
    }
  }, { scope: sectionRef });

  const handlePlanSelect = (planId: string, cycle: BillingCycle) => {
    console.log(`Selected plan: ${planId} (${cycle})`);
  };

  return (
    <section ref={sectionRef} className="relative w-full min-h-screen bg-black flex flex-col items-center justify-center py-32 px-6 z-[200]">
      {/* Background Glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[80vw] h-[80vh] bg-[#E1D4C0]/5 rounded-full blur-[120px] pointer-events-none" />

      <div className="relative z-10 w-full max-w-7xl mx-auto flex flex-col items-center">
        {/* Header */}
        <div ref={textRef} className="flex flex-col items-center w-full mb-8">
          <h2 className="text-[12px] tracking-[0.28em] font-medium opacity-70 mb-8 text-[#E1D4C0] uppercase text-center">
            Access the Intelligence
          </h2>
          <h1 className="font-serif font-bold text-[56px] lg:text-[72px] leading-[0.95] text-center max-w-3xl">
            The Cost of <span className="italic">Creation.</span>
          </h1>
        </div>

        <PricingComponent
          plans={pricingPlans}
          billingCycle={billingCycle}
          onCycleChange={setBillingCycle}
          onPlanSelect={handlePlanSelect}
        />
        
        <p className="mt-16 text-[13px] text-zinc-500 max-w-xl text-center">
          Free accounts receive a one-time grant of 20 credits valid for 14 days. Prices reflect monthly billing. Annual plans are available at a ~25% discount.
        </p>
      </div>
    </section>
  );
}
