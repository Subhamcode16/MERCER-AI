"use client";

import { useState } from "react";
import Image from "next/image";
import { 
  PricingComponent, 
  BillingCycle, 
  PriceTier 
} from "@/components/ui/pricing-card";

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
      { name: "200 Credits / mo", isIncluded: true },
      { name: "Nano Banana 2 & GPT-4o", isIncluded: true },
      { name: "Standard Resolution", isIncluded: true },
      { name: "Real-time Generation", isIncluded: true },
      { name: "8K Cinematic Exports", isIncluded: false },
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
      { name: "800 Credits / mo", isIncluded: true },
      { name: "All Models Unlocked", isIncluded: true },
      { name: "4K Export Resolution", isIncluded: true },
      { name: "Real-time Generation", isIncluded: true },
      { name: "8K Cinematic Exports", isIncluded: false },
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
      { name: "2,500 Credits / mo", isIncluded: true },
      { name: "Batch Priority Routing", isIncluded: true },
      { name: "8K Cinematic Exports", isIncluded: true },
      { name: "Dedicated Tech Director", isIncluded: true },
      { name: "All Models Unlocked", isIncluded: true },
    ],
  }
];

export default function PricingPage() {
  const [billingCycle, setBillingCycle] = useState<BillingCycle>('monthly');

  const handlePlanSelect = (planId: string, cycle: BillingCycle) => {
    console.log(`Selected plan: ${planId} (${cycle})`);
    // Redirect to checkout or contact form
  };

  return (
    <div className="relative min-h-screen flex flex-col bg-background selection:bg-primary/20 selection:text-primary">
      {/* Background Image Layer */}
      <div className="fixed inset-0 z-0 pointer-events-none opacity-20">
        <Image
          src="https://images.unsplash.com/photo-1490481651871-ab68de25d43d?q=80&w=2070&auto=format&fit=crop"
          alt="High-end fashion background"
          fill
          className="object-cover object-top"
          priority
        />
        <div className="absolute inset-0 bg-gradient-to-b from-background via-background/90 to-background pointer-events-none" />
      </div>

      <main className="flex-grow flex flex-col items-center justify-center relative z-10 pt-24 pb-12">
        <div className="text-center mb-6 mt-4 relative z-10 flex flex-col items-center">
          <span className="text-[#E1D4C0] text-xs sm:text-sm font-semibold tracking-[0.2em] uppercase mb-4 opacity-80">
            Access the Intelligence
          </span>
          <h1 className="text-5xl sm:text-7xl font-serif text-[#E1D4C0] mb-6">
            The Cost of Creation.
          </h1>
        </div>

        <div className="w-full">
          <PricingComponent
            plans={pricingPlans}
            billingCycle={billingCycle}
            onCycleChange={setBillingCycle}
            onPlanSelect={handlePlanSelect}
          />
        </div>
      </main>
    </div>
  );
}
