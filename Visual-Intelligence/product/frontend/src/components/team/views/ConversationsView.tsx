"use client";

import React, { useState } from "react";
import { 
  MessageSquare, 
  Send, 
  AtSign, 
  Sparkles, 
  CheckCircle2, 
  Clock, 
  ArrowRight,
  ShieldCheck,
  Brain
} from "lucide-react";
import type { Coworker } from "@/lib/teamFixtures";

interface ConversationsViewProps {
  coworkers: Coworker[];
}

export function ConversationsView({ coworkers }: ConversationsViewProps) {
  const [selectedRecipient, setSelectedRecipient] = useState<string>("all");
  const [inputText, setInputText] = useState("");
  const [messages, setMessages] = useState<{
    id: string;
    sender: { name: string; role: string; avatarColor: string; isUser?: boolean };
    text: string;
    timestamp: string;
    evidenceNote?: string;
  }[]>([
    {
      id: "msg-01",
      sender: { name: "Marcus Vance", role: "Creative Director", avatarColor: "#E1D4C0" },
      text: "I've structured 3 distinct creative direction hypotheses for Autumn/Winter 2026. Direction 02 (The Sovereign Modernist) achieves the highest distinctiveness score (+65.6% lift). Awaiting your review in Campaign Studio.",
      timestamp: "10:30 AM",
      evidenceNote: "Evidence: Shopify/Meta conversion cohorts Q2-Q3 2026."
    },
    {
      id: "msg-02",
      sender: { name: "Aura Chen", role: "Visual DNA Stylist", avatarColor: "#A78BFA" },
      text: "Textile physics drape simulation on the Mulberry Silk Banarasi Brocade is complete. We've locked the 38.4 N/m shearing stiffness to prevent unrealistic dynamic wind flutter.",
      timestamp: "11:15 AM",
      evidenceNote: "Calibrated via VYREN Material Physics Engine v4."
    }
  ]);

  const handleSend = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputText.trim()) return;

    const userMsg = {
      id: `msg-${Date.now()}`,
      sender: { name: "Elena Vance (You)", role: "Human Creative Lead", avatarColor: "#F59E0B", isUser: true },
      text: inputText,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev => [...prev, userMsg]);
    const userPrompt = inputText;
    setInputText("");

    setTimeout(() => {
      const responder = coworkers.find(c => c.id === selectedRecipient) || coworkers[0];
      const aiReply = {
        id: `msg-reply-${Date.now()}`,
        sender: { name: responder.name, role: responder.role, avatarColor: responder.avatarColor },
        text: `Understood Elena. I've processed your instruction regarding "${userPrompt.slice(0, 40)}...". Applying locked brand DNA policies and coordinating with the team.`,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        evidenceNote: "Bounded execution under tenant isolation."
      };
      setMessages(prev => [...prev, aiReply]);
    }, 800);
  };

  const handleSuggestionClick = (prompt: string) => {
    setInputText(prompt);
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-200 max-w-5xl mx-auto">
      
      {/* Overview & Quick Mention Strip */}
      <div className="p-5 rounded-2xl bg-[#111113]/80 border border-white/10 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="space-y-0.5">
          <h2 className="text-base font-serif text-white font-medium flex items-center gap-2">
            <MessageSquare className="w-4 h-4 text-[#E1D4C0]" /> Team Conversations & Task Delegation
          </h2>
          <p className="text-xs text-white/50 font-light">
            Communicate with your creative organization or address specific coworkers with targeted tasks.
          </p>
        </div>

        {/* Recipient Selector */}
        <div className="flex items-center gap-2">
          <span className="text-[10px] font-mono text-white/40 uppercase">Direct to:</span>
          <select
            value={selectedRecipient}
            onChange={(e) => setSelectedRecipient(e.target.value)}
            className="p-1.5 px-3 rounded-xl bg-white/[0.03] border border-white/10 text-xs text-white focus:outline-none focus:border-[#E1D4C0]/50 font-mono"
          >
            <option value="all">@Entire Creative Team</option>
            {coworkers.map((c) => (
              <option key={c.id} value={c.id}>@{c.name} ({c.role.split(' ')[0]})</option>
            ))}
          </select>
        </div>
      </div>

      {/* Suggested Fast Prompts */}
      <div className="flex items-center gap-2 flex-wrap text-xs">
        <span className="text-[10px] font-mono text-white/40 uppercase">Suggested Inquiries:</span>
        {[
          "Ask @Marcus Vance why Direction 02 was chosen",
          "Ask @Aura Chen to verify Banarasi zari reflection angles",
          "Ask @Julian Mercer to summarize diaspora audience signals",
          "Ask @Cortex Producer for billboard pre-flight readiness"
        ].map((prompt, pIdx) => (
          <button
            key={pIdx}
            onClick={() => handleSuggestionClick(prompt)}
            className="px-3 py-1 rounded-xl bg-white/[0.02] hover:bg-white/[0.06] text-white/70 hover:text-white border border-white/5 transition-colors text-[11px]"
          >
            {prompt}
          </button>
        ))}
      </div>

      {/* Messages Feed Container */}
      <div className="p-6 rounded-2xl bg-[#111113]/90 border border-white/10 min-h-[420px] flex flex-col justify-between space-y-6">
        
        {/* Messages Stream */}
        <div className="space-y-4 overflow-y-auto max-h-[460px] pr-2 scrollbar-thin scrollbar-thumb-white/10">
          {messages.map((msg) => {
            const isUser = msg.sender.isUser;
            return (
              <div
                key={msg.id}
                className={`flex gap-3.5 ${isUser ? 'justify-end' : 'justify-start'}`}
              >
                {!isUser && (
                  <div 
                    className="w-9 h-9 rounded-xl flex items-center justify-center font-serif text-xs font-semibold border border-black/60 shrink-0 mt-0.5"
                    style={{ backgroundColor: `${msg.sender.avatarColor}20`, color: msg.sender.avatarColor }}
                  >
                    {msg.sender.name[0]}
                  </div>
                )}

                <div className={`space-y-1 max-w-xl ${isUser ? 'items-end text-right' : 'items-start text-left'}`}>
                  <div className="flex items-center gap-2 text-[10px] font-mono text-white/40">
                    <span className="font-semibold text-white/80">{msg.sender.name}</span>
                    <span>&bull;</span>
                    <span>{msg.sender.role}</span>
                    <span>&bull;</span>
                    <span>{msg.timestamp}</span>
                  </div>

                  <div className={`p-4 rounded-2xl text-xs leading-relaxed ${
                    isUser
                      ? 'bg-[#E1D4C0] text-[#0A0A0A] font-medium rounded-tr-none shadow-md'
                      : 'bg-white/[0.03] text-white/90 border border-white/5 rounded-tl-none font-light'
                  }`}>
                    {msg.text}
                  </div>

                  {msg.evidenceNote && (
                    <div className="text-[10px] font-mono text-emerald-400/80 flex items-center gap-1 pt-0.5">
                      <ShieldCheck className="w-3 h-3" /> {msg.evidenceNote}
                    </div>
                  )}
                </div>

                {isUser && (
                  <div className="w-9 h-9 rounded-xl bg-amber-500/20 text-[#E1D4C0] border border-amber-500/30 flex items-center justify-center font-serif text-xs font-semibold shrink-0 mt-0.5">
                    EV
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {/* Input Bar */}
        <form onSubmit={handleSend} className="pt-4 border-t border-white/5 flex items-center gap-3">
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Type a message or use @mention to direct specific tasks..."
            className="flex-1 p-3 rounded-xl bg-white/[0.02] border border-white/10 text-xs text-white placeholder-white/30 focus:outline-none focus:border-[#E1D4C0]/50"
          />
          <button
            type="submit"
            className="px-5 py-3 rounded-xl bg-[#E1D4C0] text-[#0A0A0A] font-semibold text-xs hover:opacity-90 transition-opacity flex items-center gap-2 shrink-0 shadow-lg"
          >
            <span>Send</span>
            <Send className="w-3.5 h-3.5" />
          </button>
        </form>

      </div>

    </div>
  );
}
