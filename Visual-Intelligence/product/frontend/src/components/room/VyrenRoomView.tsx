"use client";

import React, { useState } from "react";
import { 
  Sparkles, 
  Send, 
  CheckCircle2, 
  Lock, 
  Brain, 
  Compass, 
  ShieldCheck, 
  RefreshCw, 
  ArrowRight,
  User,
  Layers,
  FileCheck,
  Check
} from "lucide-react";

interface MessageArtifact {
  id: string;
  type: "RESEARCH" | "CREATIVE_DIRECTION" | "MOODBOARD";
  title: string;
  summary: string;
  data: any;
}

interface MessageDecision {
  id: string;
  title: string;
  context: string;
  options: { id: string; label: string; distinctiveness: string }[];
  chosenOptionId?: string;
  status: "PENDING" | "CONFIRMED";
}

interface WorkEvent {
  step: string;
  status: "DONE" | "PENDING" | "ACTIVE";
}

interface RoomMessage {
  id: string;
  senderId: string;
  senderName: string;
  senderRole: string;
  isHuman: boolean;
  content: string;
  timestamp: string;
  artifacts?: MessageArtifact[];
  decisions?: MessageDecision[];
  workEvents?: WorkEvent[];
}

export function VyrenRoomView() {
  const [messages, setMessages] = useState<RoomMessage[]>([
    {
      id: "msg-01",
      senderId: "user",
      senderName: "Elena Vance",
      senderRole: "Human Creative Director",
      isHuman: true,
      content: "Create a campaign for our new luxury bridal collection targeting younger high-intent buyers. Make the brand feel contemporary without losing heritage craftsmanship.",
      timestamp: "10:42 AM"
    },
    {
      id: "msg-02",
      senderId: "vyren_core",
      senderName: "VYREN",
      senderRole: "Creative Operating System",
      isHuman: false,
      content: "I've synthesized the intelligence for your bridal launch objective. Evidence shows younger luxury buyers respond strongly to architectural heritage silhouettes. I have prepared two distinct creative territories for your selection below.",
      timestamp: "10:43 AM",
      workEvents: [
        { step: "Understanding product & launch objective", status: "DONE" },
        { step: "Querying fashion intelligence & textile physics", status: "DONE" },
        { step: "Formulating comparative creative territories", status: "DONE" },
        { step: "Human direction sign-off", status: "PENDING" }
      ],
      artifacts: [
        {
          id: "art-01",
          type: "RESEARCH",
          title: "Luxury Bridal Audience & Textile Physics Evidence",
          summary: "Audience signals confirm +24.2% lift for modernized architectural heritage silhouettes. Textile physics indicates tungsten rim lighting (2800K) prevents optical glare on Banarasi gold zari.",
          data: { epistemicStatus: "OBSERVED", confidence: "96%" }
        },
        {
          id: "art-02",
          type: "CREATIVE_DIRECTION",
          title: "Comparative Creative Territories",
          summary: "Two distinct creative hypotheses formulated from brand DNA and audience signals.",
          data: {
            territoryA: { title: "Modern Sovereign", archetype: "Architectural Precision", distinctiveness: "96%" },
            territoryB: { title: "Regal Lineage", archetype: "Heritage Grandeur", distinctiveness: "88%" }
          }
        }
      ],
      decisions: [
        {
          id: "dec-01",
          title: "Select Primary Creative Direction",
          context: "Choose primary visual world to lock into campaign memory and develop into production assets.",
          status: "PENDING",
          options: [
            { id: "opt-01", label: "Direction A: Modern Sovereign (Architectural Precision)", distinctiveness: "96%" },
            { id: "opt-02", label: "Direction B: Regal Lineage (Heritage Grandeur)", distinctiveness: "88%" }
          ]
        }
      ]
    }
  ]);

  const [inputVal, setInputVal] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);

  const handleSendMessage = (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!inputVal.trim() || isProcessing) return;

    const userText = inputVal.trim();
    setInputVal("");
    setIsProcessing(true);

    const userMsg: RoomMessage = {
      id: `msg-${Date.now()}`,
      senderId: "user",
      senderName: "Elena Vance",
      senderRole: "Human Creative Director",
      isHuman: true,
      content: userText,
      timestamp: "Just now"
    };

    setMessages(prev => [...prev, userMsg]);

    setTimeout(() => {
      const vyrenReply: RoomMessage = {
        id: `msg-${Date.now() + 1}`,
        senderId: "vyren_core",
        senderName: "VYREN",
        senderRole: "Creative Operating System",
        isHuman: false,
        content: `I've updated our creative constraints according to your feedback: "${userText}". Marcus Vance (AI Creative Director) is generating the revised visual studies.`,
        timestamp: "Just now",
        workEvents: [
          { step: `Applying human feedback: "${userText.slice(0, 30)}..."`, status: "DONE" },
          { step: "Re-calibrating textile drape and lighting shaders", status: "DONE" },
          { step: "Synthesizing multi-surface visual assets", status: "DONE" }
        ]
      };
      setMessages(prev => [...prev, vyrenReply]);
      setIsProcessing(false);
    }, 1200);
  };

  const handleConfirmDecision = (decisionId: string, optionId: string) => {
    setMessages(prev => prev.map(msg => {
      if (msg.decisions) {
        return {
          ...msg,
          decisions: msg.decisions.map(dec => {
            if (dec.id === decisionId) {
              return { ...dec, chosenOptionId: optionId, status: "CONFIRMED" };
            }
            return dec;
          })
        };
      }
      return msg;
    }));
  };

  return (
    <div className="flex flex-col h-full bg-[#0A0A0A] text-white/90 font-sans">
      
      {/* Room Header */}
      <div className="px-6 py-4 border-b border-white/10 bg-[#0D0D0E]/90 backdrop-blur-md flex items-center justify-between shrink-0">
        <div className="space-y-0.5">
          <div className="flex items-center gap-2">
            <span className="text-[10px] font-mono tracking-widest uppercase text-[#E1D4C0] bg-[#E1D4C0]/10 border border-[#E1D4C0]/20 px-2 py-0.5 rounded">
              VYREN ROOM &bull; AUTUMN/WINTER 2026
            </span>
            <span className="text-white/20 text-xs">&bull;</span>
            <span className="text-xs text-white/50 font-light">The Modern Sovereign</span>
          </div>
          <h1 className="text-lg font-serif text-white font-normal">Collaborative Creative Studio</h1>
        </div>

        {/* Room Presence Strip */}
        <div className="flex items-center gap-3 text-xs">
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-white/[0.03] border border-white/5">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            <span className="text-white/80 font-medium">VYREN</span>
            <span className="text-white/30 font-mono text-[10px]">&bull; Active OS</span>
          </div>

          <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-white/[0.03] border border-white/5">
            <div className="w-5 h-5 rounded-full bg-purple-500/20 text-purple-300 flex items-center justify-center text-[10px] font-mono font-bold">
              MV
            </div>
            <span className="text-white/80 font-medium">Marcus Vance</span>
            <span className="text-white/30 font-mono text-[10px]">&bull; AI CD</span>
          </div>

          <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-white/[0.03] border border-white/5">
            <div className="w-5 h-5 rounded-full bg-amber-500/20 text-[#E1D4C0] flex items-center justify-center text-[10px] font-mono font-bold">
              EV
            </div>
            <span className="text-white/80 font-medium">Elena Vance</span>
            <span className="text-amber-400 font-mono text-[10px]">&bull; Human Authority</span>
          </div>
        </div>
      </div>

      {/* Messages Stream Viewport */}
      <div className="flex-1 overflow-y-auto p-6 lg:p-10 space-y-8 scrollbar-thin scrollbar-thumb-white/10 max-w-5xl mx-auto w-full">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex gap-4 animate-in fade-in duration-200 ${
              msg.isHuman ? "justify-end" : "justify-start"
            }`}
          >
            {/* AI Avatar */}
            {!msg.isHuman && (
              <div className="w-9 h-9 rounded-xl bg-[#E1D4C0]/15 text-[#E1D4C0] border border-[#E1D4C0]/30 flex items-center justify-center shrink-0 mt-1 shadow-lg">
                <Sparkles className="w-4 h-4" />
              </div>
            )}

            {/* Message Body */}
            <div className={`space-y-4 max-w-2xl ${msg.isHuman ? "items-end text-right" : "items-start"}`}>
              
              {/* Header Info */}
              <div className={`flex items-center gap-2 text-xs ${msg.isHuman ? "justify-end" : "justify-start"}`}>
                <span className="font-medium text-white">{msg.senderName}</span>
                <span className="text-[10px] font-mono text-white/40">{msg.senderRole}</span>
                <span className="text-[10px] text-white/20">&bull; {msg.timestamp}</span>
              </div>

              {/* Text Bubble */}
              <div
                className={`p-5 rounded-2xl text-xs leading-relaxed font-light ${
                  msg.isHuman
                    ? "bg-[#E1D4C0] text-[#0A0A0A] font-medium rounded-tr-sm shadow-md"
                    : "bg-[#121214] text-white/90 border border-white/10 rounded-tl-sm shadow-xl"
                }`}
              >
                {msg.content}
              </div>

              {/* In-Room Work Progress Events */}
              {msg.workEvents && msg.workEvents.length > 0 && (
                <div className="p-4 rounded-2xl bg-black/40 border border-white/5 space-y-2 text-left">
                  <span className="text-[9px] font-mono uppercase tracking-widest text-white/40">
                    Live Operational Trace
                  </span>
                  <div className="space-y-1.5 text-[11px]">
                    {msg.workEvents.map((we, idx) => (
                      <div key={idx} className="flex items-center justify-between text-white/70">
                        <span>{we.step}</span>
                        {we.status === "DONE" ? (
                          <span className="text-emerald-400 font-mono text-[10px] flex items-center gap-1">
                            <Check className="w-3 h-3" /> Done
                          </span>
                        ) : (
                          <span className="text-amber-300 font-mono text-[10px] flex items-center gap-1 animate-pulse">
                            &bull; Pending Gate
                          </span>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Inline Interactive Artifacts */}
              {msg.artifacts && msg.artifacts.length > 0 && (
                <div className="space-y-4 text-left">
                  {msg.artifacts.map((art) => (
                    <div
                      key={art.id}
                      className="p-5 rounded-2xl bg-[#141417] border border-white/10 space-y-3 shadow-xl hover:border-[#E1D4C0]/30 transition-all"
                    >
                      <div className="flex items-center justify-between border-b border-white/5 pb-2.5">
                        <div className="flex items-center gap-2">
                          {art.type === "RESEARCH" ? (
                            <Brain className="w-4 h-4 text-purple-400" />
                          ) : (
                            <Compass className="w-4 h-4 text-[#E1D4C0]" />
                          )}
                          <span className="text-xs font-serif text-white font-medium">{art.title}</span>
                        </div>
                        <span className="text-[9px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                          {art.data?.epistemicStatus || "READY"}
                        </span>
                      </div>

                      <p className="text-xs text-white/70 font-light leading-relaxed">{art.summary}</p>

                      {/* Creative Directions Comparison Preview */}
                      {art.type === "CREATIVE_DIRECTION" && art.data && (
                        <div className="grid grid-cols-2 gap-3 pt-1 text-xs">
                          <div className="p-3 rounded-xl bg-white/[0.02] border border-white/5 space-y-1">
                            <span className="text-[10px] font-mono text-[#E1D4C0]">Territory A: Modern Sovereign</span>
                            <div className="text-white font-medium">Architectural Precision</div>
                            <span className="text-[10px] text-emerald-400 font-mono">96% Distinctiveness</span>
                          </div>
                          <div className="p-3 rounded-xl bg-white/[0.02] border border-white/5 space-y-1">
                            <span className="text-[10px] font-mono text-purple-400">Territory B: Regal Lineage</span>
                            <div className="text-white font-medium">Heritage Grandeur</div>
                            <span className="text-[10px] text-emerald-400 font-mono">88% Distinctiveness</span>
                          </div>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}

              {/* Inline Human Decision Gates */}
              {msg.decisions && msg.decisions.length > 0 && (
                <div className="space-y-3 text-left">
                  {msg.decisions.map((dec) => (
                    <div
                      key={dec.id}
                      className="p-5 rounded-2xl bg-gradient-to-r from-amber-950/20 via-[#141418] to-black border border-amber-500/30 space-y-3 shadow-xl"
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <Lock className="w-4 h-4 text-amber-400" />
                          <span className="text-xs font-serif text-white font-medium">{dec.title}</span>
                        </div>
                        <span className={`text-[9px] font-mono px-2 py-0.5 rounded-full border ${
                          dec.status === "CONFIRMED" 
                            ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20" 
                            : "bg-amber-500/10 text-amber-300 border-amber-500/20"
                        }`}>
                          {dec.status === "CONFIRMED" ? "DECISION COMMITTED ★" : "HUMAN GATE"}
                        </span>
                      </div>

                      <p className="text-xs text-white/60 font-light">{dec.context}</p>

                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-1">
                        {dec.options.map((opt) => {
                          const isSelected = dec.chosenOptionId === opt.id;
                          return (
                            <button
                              key={opt.id}
                              onClick={() => handleConfirmDecision(dec.id, opt.id)}
                              disabled={dec.status === "CONFIRMED"}
                              className={`p-3 rounded-xl border text-left text-xs transition-all flex items-center justify-between ${
                                isSelected
                                  ? "bg-[#E1D4C0] text-[#0A0A0A] font-semibold border-[#E1D4C0] shadow-lg"
                                  : "bg-white/[0.02] text-white/80 border-white/5 hover:bg-white/5 hover:border-white/20"
                              }`}
                            >
                              <span>{opt.label}</span>
                              {isSelected && <CheckCircle2 className="w-4 h-4" />}
                            </button>
                          );
                        })}
                      </div>
                    </div>
                  ))}
                </div>
              )}

            </div>

            {/* Human Avatar */}
            {msg.isHuman && (
              <div className="w-9 h-9 rounded-xl bg-white/10 text-white border border-white/20 flex items-center justify-center shrink-0 mt-1">
                <User className="w-4 h-4" />
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Persistent Bottom Composer Bar */}
      <div className="p-4 border-t border-white/10 bg-[#0D0D0E]/90 backdrop-blur-md shrink-0">
        <form onSubmit={handleSendMessage} className="max-w-4xl mx-auto flex items-center gap-3 bg-black/50 p-2 rounded-2xl border border-white/10 focus-within:border-[#E1D4C0]/50 transition-all">
          <div className="w-8 h-8 rounded-xl bg-[#E1D4C0]/10 text-[#E1D4C0] flex items-center justify-center shrink-0">
            <Sparkles className="w-4 h-4" />
          </div>

          <input
            type="text"
            value={inputVal}
            onChange={(e) => setInputVal(e.target.value)}
            placeholder="Collaborate with VYREN in the Room... (e.g. 'Make the hero more commanding')"
            className="flex-1 bg-transparent text-xs text-white placeholder-white/40 focus:outline-none font-light"
          />

          <button
            type="submit"
            disabled={!inputVal.trim() || isProcessing}
            className="px-4 py-2 rounded-xl bg-[#E1D4C0] text-[#0A0A0A] font-semibold text-xs hover:opacity-90 disabled:opacity-40 transition-opacity flex items-center gap-1.5 shrink-0 shadow-lg"
          >
            {isProcessing ? (
              <>
                <RefreshCw className="w-3 h-3 animate-spin" />
                <span>Thinking...</span>
              </>
            ) : (
              <>
                <span>Send</span>
                <Send className="w-3 h-3" />
              </>
            )}
          </button>
        </form>
      </div>

    </div>
  );
}
