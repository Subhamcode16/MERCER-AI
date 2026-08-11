"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import { ArrowLeft } from "lucide-react";
import { getCampaign, generateCampaign } from "@/lib/campaigns";
import { StudioEditorLayout } from "@/components/studio/StudioEditorLayout";
import Link from "next/link";
import { useAuth } from "@/contexts/AuthContext";

export default function StudioEditorPage() {
  const params = useParams();
  const router = useRouter();
  const campaignId = params.id as string;
  const { session, isLoading: isAuthLoading } = useAuth();
  
  const [campaign, setCampaign] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isGenerating, setIsGenerating] = useState(false);

  useEffect(() => {
    async function loadCampaign() {
      try {
        const data = await getCampaign(campaignId);
        setCampaign(data);
      } catch (error) {
        console.error("Error loading campaign", error);
      } finally {
        setIsLoading(false);
      }
    }
    
    if (isAuthLoading) return;
    
    if (!session) {
      router.push("/studio");
      return;
    }

    if (campaignId) loadCampaign();
  }, [campaignId, session, isAuthLoading, router]);

  const handleGenerate = async (modelId: string, options: any) => {
    setIsGenerating(true);
    try {
      // Assuming generateCampaign can now accept model_id in its body
      // We pass the model_id down to the API
      await generateCampaign(campaignId, { model_id: modelId, ...options });
      
      // Poll or wait for completion in a real scenario
      // For MVP, just reload campaign after a short delay
      setTimeout(async () => {
        const updated = await getCampaign(campaignId);
        setCampaign(updated);
        setIsGenerating(false);
      }, 3000);
      
    } catch (error) {
      console.error("Error generating campaign", error);
      setIsGenerating(false);
    }
  };

  if (isLoading) {
    return <div className="min-h-screen bg-background flex items-center justify-center text-muted-foreground">Loading Studio OS...</div>;
  }

  if (!campaign) {
    return <div className="min-h-screen bg-background flex items-center justify-center text-muted-foreground">Campaign not found.</div>;
  }

  return (
    <div className="flex flex-col min-h-screen bg-background">
      {/* Top Navbar */}
      <header className="h-16 border-b border-border px-6 flex items-center justify-between bg-card shrink-0">
        <div className="flex items-center gap-4">
          <Link href="/studio" className="text-muted-foreground hover:text-primary transition-colors">
            <ArrowLeft className="w-5 h-5" />
          </Link>
          <div>
            <h1 className="text-sm font-serif text-foreground">{campaign.name || "Untitled Campaign"}</h1>
            <p className="text-[10px] uppercase tracking-widest text-muted-foreground font-mono">Creative OS Editor</p>
          </div>
        </div>
        <div className="flex items-center gap-4">
           {/* Add export/share buttons here if needed */}
        </div>
      </header>

      {/* Main Layout */}
      <StudioEditorLayout 
        campaign={campaign} 
        onGenerate={handleGenerate} 
        isGenerating={isGenerating} 
      />
    </div>
  );
}
