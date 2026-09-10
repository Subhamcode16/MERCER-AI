"use client";

import { useState, useEffect, useRef, useContext } from "react";
import Link from "next/link";
import { useSearchParams, useRouter } from "next/navigation";
import { ArrowLeft, Users, Sparkles } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import dynamic from "next/dynamic";
import { PromptInputBox } from "@/components/ui/ai-prompt-box";
import { useAuth } from "@/contexts/AuthContext";
import { SidebarContext } from "../layout";

import AnimatedGradientBackground from "@/components/ui/animated-gradient-background";

// Imported Modular Team Components & Types
import { PageState, ChatMessage, BrandDnaData, AgentId, AgentTaskInfo, CampaignFolder, ChatSession } from "@/components/team/types";
import { GreetingScreen } from "@/components/team/GreetingScreen";
import { BrandDnaModal } from "@/components/team/BrandDnaModal";
import { AgentMessage } from "@/components/team/AgentMessage";
import { UserMessage } from "@/components/team/UserMessage";
import { DnaSpecCard } from "@/components/team/DnaSpecCard";
import { PhotoDecompCard } from "@/components/team/PhotoDecompCard";
import { TypingIndicator } from "@/components/team/TypingIndicator";
import { ApprovalGate } from "@/components/team/ApprovalGate";
import { MentionAutocomplete } from "@/components/team/MentionAutocomplete";
import { AgentRosterPanel } from "@/components/team/AgentRosterPanel";
import { CanvasFolderPopover } from "@/components/team/CanvasFolderPopover";

// Mock Multi-Agent Simulator
import { MockOrchestrator } from "@/components/team/mockOrchestrator";

export default function TeamMode() {
  const { session } = useAuth();
  const searchParams = useSearchParams();
  const router = useRouter();
  
  const { setIsInWorkspace } = useContext(SidebarContext);

  // Collapse sidebar on mount, restore on unmount
  useEffect(() => {
    setIsInWorkspace(true);
    return () => setIsInWorkspace(false);
  }, [setIsInWorkspace]);

  // Ref for the scrollable chat feed container (prevents window scrolling shift)
  const chatFeedRef = useRef<HTMLDivElement>(null);
  
  const userId = session?.user?.id || "default_user";
  const userName = session?.user?.user_metadata?.full_name || session?.user?.email?.split("@")[0] || "Creator";

  // Resolution and manual popup trigger states
  const [isResolved, setIsResolved] = useState(false);
  const [isDnaConfigOpen, setIsDnaConfigOpen] = useState(false);

  // State Machine: greeting -> onboarding -> workspace
  const [pageState, setPageState] = useState<PageState>("greeting");
  const [brandDna, setBrandDna] = useState<BrandDnaData | null>(null);

  // Multi-Campaign Nested Databases
  const [campaigns, setCampaigns] = useState<CampaignFolder[]>([
    {
      id: "campaign-silk",
      name: "Fall 2026 Silk Launch",
      assets: [
        { url: "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?q=80&w=600", label: "Banarasi Silk Texture Structure" },
        { url: "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=600", label: "Twilight Mood Silhouette" }
      ],
      sessions: [
        {
          id: "session-silk-textile",
          name: "🧵 Textile Analysis & Weave Specs",
          messages: [
            {
              id: "welcome-silk-textile",
              sender: "brand-dna",
              senderName: "@Brand-DNA",
              time: "10:30 AM",
              text: "Welcome Creator. Campaign session 'Textile Analysis' active. Tag @Material-DNA to inspect weave specs."
            }
          ]
        },
        {
          id: "session-silk-shot",
          name: "🎬 Twilight Shot Composition Setup",
          messages: [
            {
              id: "welcome-silk-shot",
              sender: "art-director",
              senderName: "@Art-Director",
              time: "11:15 AM",
              text: "Active session 'Twilight Shot Setup'. Ready to configure lighting parameters and shot composition details."
            }
          ]
        }
      ]
    },
    {
      id: "campaign-tweed",
      name: "Winter Tweed Collection",
      assets: [
        { url: "https://images.unsplash.com/photo-1598033129183-c4f50c736f10?q=80&w=600", label: "Heavy Tweed Weave Structure" }
      ],
      sessions: [
        {
          id: "session-tweed-diagnostics",
          name: "🧥 Heavy Weave Diagnostics",
          messages: [
            {
              id: "welcome-tweed",
              sender: "material-dna",
              senderName: "@Material-DNA",
              time: "02:10 PM",
              text: "Active session 'Heavy Weave Diagnostics'. Tweed thread density profiles loaded. Ask me to perform distortion checks or inspect fiber specs."
            }
          ]
        }
      ]
    },
    {
      id: "campaign-linen",
      name: "Summer Resort Swatch",
      assets: [],
      sessions: [
        {
          id: "session-linen-palette",
          name: "🎨 Linen Palette Setup",
          messages: [
            {
              id: "welcome-linen",
              sender: "brand-dna",
              senderName: "@Brand-DNA",
              time: "04:45 PM",
              text: "Active session 'Linen Palette Setup'. Ready to synthesize warm ivory and pastel linen presets."
            }
          ]
        }
      ]
    }
  ]);

  // Active Context IDs
  const [activeCampaignId, setActiveCampaignId] = useState("campaign-silk");
  const [activeSessionId, setActiveSessionId] = useState("session-silk-textile");
  const [isCanvasPopoverOpen, setIsCanvasPopoverOpen] = useState(false);

  // Dynamic Lookup Helpers
  const activeCampaign = campaigns.find(c => c.id === activeCampaignId) || campaigns[0];
  const activeSession = activeCampaign.sessions.find(s => s.id === activeSessionId) || activeCampaign.sessions[0];
  const messages = activeSession.messages;

  // Task & Generating States
  const [typingAgent, setTypingAgent] = useState<AgentId | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [isAwaitingApproval, setIsAwaitingApproval] = useState(false);
  const [agentTasks, setAgentTasks] = useState<Partial<Record<AgentId, AgentTaskInfo>>>({
    'brand-dna': { status: 'idle' },
    'material-dna': { status: 'idle' },
    'image-decomposer': { status: 'idle' },
    'art-director': { status: 'idle' },
    'strategist': { status: 'idle' },
    'renderer': { status: 'idle' },
    'validator': { status: 'idle' },
    'copywriter': { status: 'idle' },
  });

  // @ Mention Popup State
  const [promptText, setPromptText] = useState("");
  const [showMentionPopup, setShowMentionPopup] = useState(false);
  const [mentionFilter, setMentionFilter] = useState("");

  // Scroll to bottom using container scrollTop (completely immune to browser viewport shifting)
  useEffect(() => {
    if (pageState === "workspace" && chatFeedRef.current) {
      chatFeedRef.current.scrollTop = chatFeedRef.current.scrollHeight;
    }
  }, [messages, typingAgent, pageState]);

  // Onboard resolver + Load stored Brand DNA on mount
  useEffect(() => {
    const visited = localStorage.getItem(`mercer_team_visited_${userId}`);
    const savedDna = localStorage.getItem(`mercer_brand_dna_${userId}`);
    const skippedDna = localStorage.getItem(`mercer_brand_dna_skipped_${userId}`);
    
    if (savedDna) {
      try {
        setBrandDna(JSON.parse(savedDna));
      } catch (e) {
        console.error("Failed to parse stored brand DNA", e);
      }
    }

    if (visited === "true") {
      // Recurring visitor -> Skip greeting
      if (savedDna || skippedDna === "true") {
        setPageState("workspace");
      } else {
        setPageState("onboarding");
      }
    } else {
      // First time visitor -> Show greeting
      setPageState("greeting");
    }
    setIsResolved(true);
  }, [userId]);

  const handleWorkspaceStart = () => {
    setPageState("workspace");
  };

  // Switch Active Session Context
  const handleSelectSession = (campaignId: string, sessionId: string) => {
    setActiveCampaignId(campaignId);
    setActiveSessionId(sessionId);
    setIsCanvasPopoverOpen(false);
  };

  // Rename Session
  const handleRenameSession = (campaignId: string, sessionId: string, newName: string) => {
    setCampaigns((prev) =>
      prev.map((campaign) => {
        if (campaign.id === campaignId) {
          return {
            ...campaign,
            sessions: campaign.sessions.map((sess) =>
              sess.id === sessionId ? { ...sess, name: newName } : sess
            ),
          };
        }
        return campaign;
      })
    );
  };

  // Delete Session
  const handleDeleteSession = (campaignId: string, sessionId: string) => {
    setCampaigns((prev) => {
      return prev.map((campaign) => {
        if (campaign.id === campaignId) {
          const filteredSessions = campaign.sessions.filter((s) => s.id !== sessionId);
          
          // Prevent empty sessions array to avoid crash on activeSession fallback
          if (filteredSessions.length === 0) {
            const newSessionId = `session-${Date.now()}`;
            const newSessionName = `💬 Session Draft #1`;
            return {
              ...campaign,
              sessions: [
                {
                  id: newSessionId,
                  name: newSessionName,
                  messages: [
                    {
                      id: `welcome-${newSessionId}`,
                      sender: "brand-dna",
                      senderName: "@Brand-DNA",
                      time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
                      text: `Initialized blank chat session '${newSessionName}'. Tag @agents to begin.`
                    }
                  ]
                }
              ]
            };
          }
          return { ...campaign, sessions: filteredSessions };
        }
        return campaign;
      });
    });
  };

  // Create New Nested Chat Session inside Campaign
  const handleCreateSession = (campaignId: string) => {
    const newSessionId = `session-${Date.now()}`;
    const newSessionName = `💬 Session Draft #${activeCampaign.sessions.length + 1}`;
    
    const newSession: ChatSession = {
      id: newSessionId,
      name: newSessionName,
      messages: [
        {
          id: `welcome-${newSessionId}`,
          sender: "brand-dna",
          senderName: "@Brand-DNA",
          time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
          text: `Initialized blank chat session '${newSessionName}' in campaign '${activeCampaign.name}'. Tag @agents to begin.`
        }
      ]
    };

    setCampaigns(prev => prev.map(campaign => {
      if (campaign.id === campaignId) {
        return {
          ...campaign,
          sessions: [...campaign.sessions, newSession]
        };
      }
      return campaign;
    }));

    setActiveCampaignId(campaignId);
    setActiveSessionId(newSessionId);
    setIsCanvasPopoverOpen(false);
  };

  // Helper to update agent task tracking in right panel
  const handleTaskUpdate = (
    agentId: AgentId,
    status: "idle" | "processing" | "completed",
    taskName?: string
  ) => {
    setAgentTasks((prev) => ({
      ...prev,
      [agentId]: {
        status,
        currentTask: taskName,
      },
    }));
  };

  // Helper to append message to active session in campaigns state
  const appendSessionMessage = (msg: ChatMessage) => {
    setCampaigns(prev => prev.map(campaign => {
      if (campaign.id === activeCampaignId) {
        return {
          ...campaign,
          sessions: campaign.sessions.map(sess => {
            if (sess.id === activeSessionId) {
              return {
                ...sess,
                messages: [...sess.messages, msg]
              };
            }
            return sess;
          })
        };
      }
      return campaign;
    }));
  };

  // Handle Send Prompt (with transcription intercept)
  const handleSendPrompt = async (text: string) => {
    if (!text.trim()) return;

    setIsGenerating(true);
    setPromptText("");
    setShowMentionPopup(false);

    // Check if voice message format: [Voice message - X seconds]
    const isVoice = text.startsWith("[Voice message -");

    if (isVoice) {
      // 1. Post original Voice Message bubble
      const voiceMsg: ChatMessage = {
        id: Date.now().toString(),
        sender: "user",
        senderName: userName,
        time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
        text,
        isRead: true,
      };
      appendSessionMessage(voiceMsg);

      // 2. Delay and post Transcription directive text
      setTypingAgent("brand-dna");
      await new Promise((resolve) => setTimeout(resolve, 1200));
      setTypingAgent(null);

      const transcriptText = "Create a twilight shot composition setup for our silk campaign.";
      const transcriptMsg: ChatMessage = {
        id: `transcript-${Date.now()}`,
        sender: "brand-dna",
        senderName: "@Brand-DNA",
        time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
        text: `🎙️ Transcribed Voice Directive: "${transcriptText}"`
      };
      appendSessionMessage(transcriptMsg);

      // 3. Delegate the transcribed instruction to MockOrchestrator
      try {
        await MockOrchestrator.processUserPrompt({
          prompt: `@Art-Director ${transcriptText}`,
          onTyping: (agentId) => setTypingAgent(agentId),
          onMessage: (msg) => appendSessionMessage(msg),
          onTaskUpdate: handleTaskUpdate,
          onTriggerApproval: () => setIsAwaitingApproval(true),
        });
      } catch (err) {
        console.error("Transcription pipeline error:", err);
      } finally {
        setIsGenerating(false);
      }
    } else {
      // Regular text/mention flow
      const userMsg: ChatMessage = {
        id: Date.now().toString(),
        sender: "user",
        senderName: userName,
        time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
        text,
        isRead: true,
      };
      appendSessionMessage(userMsg);

      try {
        await MockOrchestrator.processUserPrompt({
          prompt: text,
          onTyping: (agentId) => setTypingAgent(agentId),
          onMessage: (msg) => appendSessionMessage(msg),
          onTaskUpdate: handleTaskUpdate,
          onTriggerApproval: () => setIsAwaitingApproval(true),
        });
      } catch (err) {
        console.error("Text pipeline error:", err);
      } finally {
        setIsGenerating(false);
      }
    }
  };

  // Handle Approval Gate Execution
  const handleApproveSetup = async () => {
    setIsAwaitingApproval(false);
    setIsGenerating(true);

    try {
      await MockOrchestrator.runRenderingPipeline(
        (agentId) => setTypingAgent(agentId),
        (msg) => appendSessionMessage(msg),
        handleTaskUpdate
      );
    } catch (err) {
      console.error("Rendering pipeline error:", err);
    } finally {
      setIsGenerating(false);
    }
  };

  // Handle Prompt Box Input Change (detects @ symbol for mention popup)
  const handlePromptChange = (val: string) => {
    setPromptText(val);
    const lastWord = val.split(/\s+/).pop() || "";
    if (lastWord.startsWith("@")) {
      setShowMentionPopup(true);
      setMentionFilter(lastWord);
    } else {
      setShowMentionPopup(false);
    }
  };

  // Insert Mention Handle
  const handleSelectMention = (handle: string) => {
    const words = promptText.split(/\s+/);
    words.pop();
    const newText = [...words, handle, ""].join(" ");
    setPromptText(newText);
    setShowMentionPopup(false);
  };

  const generatedAssets = activeCampaign.assets;

  if (!isResolved) {
    return (
      <div className="w-full h-full bg-[#050505] text-[#E1D4C0] flex items-center justify-center font-mono text-[10px] tracking-widest uppercase">
        Loading Mercer AI...
      </div>
    );
  }

  return (
    <div className="w-full h-full relative overflow-hidden bg-[#050505] text-[#E1D4C0] flex flex-col">
      {/* Atmospheric Radial Gradient Background */}
      <AnimatedGradientBackground
        startingGap={110}
        Breathing={true}
        breathingRange={8}
        animationSpeed={0.015}
        topOffset={-10}
        gradientColors={[
          "#050505",  // near-black base
          "#1f1215",  // deep rose shadow
          "#451a23",  // dark burgundy
          "#7c3d49",  // dusty rose
          "#b36272",  // velvet rose
          "#d48c9a",  // rose gold highlight
          "#050505",  // fade to black at edges
        ]}
        gradientStops={[30, 42, 52, 62, 73, 84, 100]}
      />

      {/* STATE 1: GREETING SCREEN */}
      <AnimatePresence>
        {pageState === "greeting" && (
          <GreetingScreen
            userName={userName}
            onComplete={() => {
              localStorage.setItem(`mercer_team_visited_${userId}`, "true");
              const savedDna = localStorage.getItem(`mercer_brand_dna_${userId}`);
              const skippedDna = localStorage.getItem(`mercer_brand_dna_skipped_${userId}`);
              if (savedDna || skippedDna === "true") {
                setPageState("workspace");
              } else {
                setPageState("onboarding");
              }
            }}
          />
        )}
      </AnimatePresence>

      {/* STATE 2: BRAND DNA ONBOARDING MODAL */}
      <AnimatePresence>
        {pageState === "onboarding" && (
          <BrandDnaModal
            userId={userId}
            onComplete={(data) => {
              setBrandDna(data);
              if (!data) {
                localStorage.setItem(`mercer_brand_dna_skipped_${userId}`, "true");
              } else {
                localStorage.removeItem(`mercer_brand_dna_skipped_${userId}`);
              }
              localStorage.setItem(`mercer_team_visited_${userId}`, "true");
              handleWorkspaceStart();
            }}
          />
        )}
      </AnimatePresence>

      {/* MANUAL BRAND DNA TRIGGER */}
      <AnimatePresence>
        {isDnaConfigOpen && (
          <BrandDnaModal
            userId={userId}
            onComplete={(data) => {
              if (data) {
                setBrandDna(data);
                localStorage.removeItem(`mercer_brand_dna_skipped_${userId}`);
              }
              setIsDnaConfigOpen(false);
            }}
          />
        )}
      </AnimatePresence>

      {/* STATE 3: MAIN WORKSPACE */}
      {pageState === "workspace" && (
        <div className="w-full flex-1 flex flex-col relative z-10 min-h-0">
          {/* Top Header */}
          <header className="h-[60px] border-b border-white/10 bg-[#0C0C0E] flex items-center justify-between px-8 shrink-0 relative z-20 shadow-md">
            <div className="flex items-center gap-4">
              <Link
                href="/studio"
                className="w-8 h-8 rounded-full border border-white/10 flex items-center justify-center text-white/40 hover:text-white hover:bg-white/5 transition-colors shrink-0"
                title="Return to Studio"
              >
                <ArrowLeft size={14} />
              </Link>
              <div>
                <h1 className="text-[13px] font-serif tracking-[0.15em] uppercase text-white font-medium flex items-center gap-2">
                  <Users size={14} className="text-[#E1D4C0]" />
                  Team Mode
                </h1>
                <p className="text-[9px] font-mono tracking-widest text-[#E1D4C0] uppercase mt-0.5">
                  📂 {activeCampaign.name}
                </p>
              </div>
            </div>
            <div className="flex items-center gap-6">
              {/* Brand DNA Config Option */}
              <button
                onClick={() => {
                  setIsDnaConfigOpen(true);
                }}
                className="flex items-center gap-2 px-3.5 py-1.5 rounded-full border border-white/10 hover:border-[#E1D4C0]/40 bg-white/[0.02] hover:bg-white/[0.06] text-white/60 hover:text-white transition-all text-[10px] font-mono tracking-wider cursor-pointer"
              >
                <Sparkles size={11} className="text-[#E1D4C0]" />
                {brandDna ? "BRAND DNA: ACTIVE" : "SET BRAND DNA"}
              </button>

              <div className="flex items-center gap-3">
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                <span className="text-[9.5px] font-mono tracking-widest text-white/40 uppercase">
                  {activeSession.name}
                </span>
              </div>
            </div>
          </header>

          {/* Workspace Body */}
          <div className="flex-1 flex min-h-0 relative">
            {/* Telegram-style Chat Feed Window */}
            <div className="flex-1 flex flex-col min-h-0 bg-transparent border-r border-white/5 relative">
              
              {/* Messages Scroll Viewport */}
              <div 
                ref={chatFeedRef}
                className="flex-1 overflow-y-auto px-10 py-8 space-y-6 scrollbar-none flex flex-col min-h-0"
              >
                
                {/* Empty State Guidance Banner (if no messages) */}
                {messages.length === 0 && (
                  <div className="flex-1 flex flex-col items-center justify-center text-center p-8 max-w-xl mx-auto my-auto select-none">
                    <div className="w-16 h-16 rounded-full bg-[#E1D4C0]/5 border border-[#E1D4C0]/20 flex items-center justify-center mb-4 shadow-xl">
                      <Users size={24} className="text-[#E1D4C0]" />
                    </div>
                    <h3 className="font-serif text-lg text-[#E1D4C0] font-light tracking-wide mb-2">
                      A2A Collaborative Environment
                    </h3>
                    <p className="text-[11px] font-sans text-white/40 leading-relaxed font-light mb-6">
                      8 Specialist agents connected. Send a message or tag an agent using <code className="text-[#E1D4C0] bg-white/5 px-1.5 py-0.5 rounded font-mono">@</code> to delegate visual tasks.
                    </p>

                    <div className="flex flex-wrap gap-2.5 justify-center">
                      {[
                        "@Material-DNA Analyze Banarasi silk specimen",
                        "@Visual-DNA Deconstruct photo lighting",
                        "@Art-Director Resolve shot parameters",
                      ].map((sample, i) => (
                        <button
                          key={i}
                          onClick={() => {
                            setPromptText(sample);
                            setShowMentionPopup(false);
                          }}
                          className="text-[10px] font-mono text-white/60 hover:text-white border border-white/10 hover:border-[#E1D4C0]/40 px-3.5 py-2 rounded-xl bg-white/[0.02] hover:bg-white/[0.05] transition-all cursor-pointer"
                        >
                          {sample}
                        </button>
                      ))}
                    </div>
                  </div>
                )}

                <AnimatePresence initial={false}>
                  {messages.map((msg) => {
                    if (msg.sender === "user") {
                      return (
                        <UserMessage key={msg.id} time={msg.time} text={msg.text || ""} />
                      );
                    }

                    return (
                      <AgentMessage
                        key={msg.id}
                        sender={msg.sender}
                        time={msg.time}
                        text={msg.text}
                      >
                        {msg.dnaCard && (
                          <DnaSpecCard
                            title={msg.dnaCard.title}
                            details={msg.dnaCard.details}
                            bullet={msg.dnaCard.bullet}
                          />
                        )}
                        {msg.photoCard && (
                          <PhotoDecompCard
                            title={msg.photoCard.title}
                            description={msg.photoCard.description}
                            images={msg.photoCard.images}
                          />
                        )}
                        {msg.imageCard && (
                          <div className="border border-[#E1D4C0]/20 bg-[#0C0C0D]/95 rounded-2xl p-3 relative overflow-hidden flex flex-col gap-2.5 max-w-lg mt-1 shadow-2xl backdrop-blur-xl">
                            <img
                              src={msg.imageCard.url}
                              alt="Rendered Asset"
                              className="rounded-xl w-full object-cover max-h-[300px]"
                            />
                            <div className="flex flex-col px-1">
                              <span className="text-[8.5px] font-mono uppercase tracking-wider text-white/30">
                                Render Payload
                              </span>
                              <p className="text-[10.5px] text-[#E1D4C0]/90 font-light leading-relaxed mt-0.5">
                                {msg.imageCard.prompt}
                              </p>
                            </div>
                          </div>
                        )}
                      </AgentMessage>
                    );
                  })}

                  {typingAgent && <TypingIndicator agentId={typingAgent} />}
                </AnimatePresence>
              </div>

              {/* Bottom Transparent Input Area (Floats on Black Canvas) */}
              <div className="px-10 pb-6 pt-2 shrink-0 bg-transparent relative z-20">
                <div className="relative w-full max-w-3xl mx-auto flex flex-col gap-3">
                  
                  {/* Canvas Folder Popover Context Selector */}
                  <AnimatePresence>
                    {isCanvasPopoverOpen && (
                      <CanvasFolderPopover
                        campaigns={campaigns}
                        activeCampaignId={activeCampaignId}
                        activeSessionId={activeSessionId}
                        onSelectSession={handleSelectSession}
                        onCreateSession={handleCreateSession}
                        onRenameSession={handleRenameSession}
                        onDeleteSession={handleDeleteSession}
                        onClose={() => setIsCanvasPopoverOpen(false)}
                      />
                    )}
                  </AnimatePresence>

                  {/* Floating Mention Autocomplete */}
                  {showMentionPopup && (
                    <MentionAutocomplete
                      filterText={mentionFilter}
                      onSelect={handleSelectMention}
                      onClose={() => setShowMentionPopup(false)}
                    />
                  )}

                  {/* Approval Gate */}
                  <AnimatePresence>
                    {isAwaitingApproval && (
                      <ApprovalGate 
                        onApprove={handleApproveSetup} 
                        onCancel={() => setIsAwaitingApproval(false)}
                      />
                    )}
                  </AnimatePresence>

                  {/* Prompt Input Box */}
                  {!isAwaitingApproval && (
                    <div className="relative w-full">
                      <div className="absolute -inset-2 bg-gradient-to-r from-[#E1D4C0]/10 via-[#C9B99A]/5 to-[#E1D4C0]/10 rounded-[36px] blur-xl -z-10 pointer-events-none" />
                      <PromptInputBox
                        value={promptText}
                        onValueChange={handlePromptChange}
                        onSend={handleSendPrompt}
                        isLoading={isGenerating}
                        placeholder="Chat with your team or mention @agents..."
                        className="bg-[#09090A]/95 border-[#E1D4C0]/25 shadow-[0_0_40px_rgba(225,212,192,0.1)] backdrop-blur-xl placeholder-white/20"
                        onCanvasClick={() => setIsCanvasPopoverOpen(!isCanvasPopoverOpen)}
                        isCanvasActive={isCanvasPopoverOpen}
                        activeCampaignName={activeCampaign.name}
                      />
                    </div>
                  )}
                </div>
              </div>

            </div>

            {/* Collapsible Right Panel */}
            <AgentRosterPanel
              brandDna={brandDna}
              generatedAssets={generatedAssets}
              agentTasks={agentTasks}
            />
          </div>
        </div>
      )}
    </div>
  );
}
