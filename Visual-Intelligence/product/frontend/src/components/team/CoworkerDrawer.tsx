"use client";

import React, { useState } from "react";
import { 
  X, 
  Sparkles, 
  ShieldCheck, 
  Send, 
  Clock, 
  CheckCircle2, 
  Lock, 
  Layers, 
  Database,
  ArrowRight,
  GitCommit,
  UserCheck,
  Brain
} from "lucide-react";
import type { Coworker } from "@/lib/teamFixtures";

interface CoworkerDrawerProps {
  coworker: Coworker | null;
  onClose: () => void;
  onNavigateToCampaign?: (campaignName: string) => void;
}

export function CoworkerDrawer({ coworker, onClose, onNavigateToCampaign }: CoworkerDrawerProps) {
  const [activeTab, setActiveTab] = useState<'overview' | 'chat' | 'handoffs' | 'governance'>('overview');
  const [messageInput, setMessageInput] = useState("");
  const [chatThread, setChatThread] = useState<{ sender: 'user' | 'coworker'; text: string; time: string }[]>([
    {
      sender: 'coworker',
      text: `Hello! I'm ${coworker?.name || 'your coworker'}. I'm currently focused on "${coworker?.currentWork.task || 'creative tasks'}". How can I assist you with this campaign?`,
      time: "Just now"
    }
  ]);

  if (!coworker) return null;

  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (!messageInput.trim()) return;

    const userText = messageInput;
    const now = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    
    setChatThread(prev => [...prev, { sender: 'user', text: userText, time: now }]);
    setMessageInput("");

    setTimeout(() => {
      let reply = `Understood. I've noted your instruction regarding "${userText.slice(0, 35)}...". I'm applying our locked brand policies and will prepare a structured recommendation memo.`;
      if (userText.toLowerCase().includes("status") || userText.toLowerCase().includes("progress")) {
        reply = `Current progress is at ${coworker.currentWork.progress}% on "${coworker.currentWork.task}". Expected delivery is ${coworker.currentWork.estimatedDelivery}.`;
      } else if (userText.toLowerCase().includes("approve") || userText.toLowerCase().includes("publish")) {
        reply = `I can prepare the package, but in accordance with VYREN governance invariants, final execution requires your explicit signature in the Review Gate.`;
      }

      setChatThread(prev => [...prev, { sender: 'coworker', text: reply, time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }]);
    }, 600);
  };

  return (
    <div className="fixed inset-0 z-50 flex justify-end bg-black/75 backdrop-blur-sm animate-in fade-in duration-200">
      <div 
        className="w-full max-w-xl bg-[#111113] border-l border-white/10 h-full shadow-2xl flex flex-col overflow-hidden animate-in slide-in-from-right duration-300"
        onClick={(e) => e.stopPropagation()}
      >
        
        {/* Drawer Header */}
        <div className="p-6 border-b border-white/5 bg-white/[0.02] flex items-start justify-between">
          <div className="flex items-center gap-3.5">
            <div 
              className="w-12 h-12 rounded-2xl flex items-center justify-center font-serif text-base font-semibold border border-black/60 shadow-lg"
              style={{ backgroundColor: `${coworker.avatarColor}20`, color: coworker.avatarColor }}
            >
              {coworker.avatarInitials}
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-base font-medium text-white">{coworker.name}</h2>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-white/5 text-white/60 border border-white/10">
                  {coworker.department}
                </span>
              </div>
              <p className="text-xs text-white/50 font-light">{coworker.role}</p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="w-8 h-8 rounded-xl border border-white/10 flex items-center justify-center text-white/40 hover:text-white hover:bg-white/5 transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Drawer Navigation Tabs */}
        <div className="flex items-center gap-2 px-6 border-b border-white/5 text-xs font-mono">
          {[
            { id: 'overview', label: 'Overview & Work' },
            { id: 'chat', label: 'Conversation' },
            { id: 'handoffs', label: 'Recent Outputs' },
            { id: 'governance', label: 'Capabilities & Scope' }
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`py-3 px-2 border-b-2 transition-all ${
                activeTab === tab.id
                  ? "border-[#E1D4C0] text-[#E1D4C0] font-semibold"
                  : "border-transparent text-white/40 hover:text-white"
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Drawer Body Scrollable Content */}
        <div className="flex-1 p-6 overflow-y-auto space-y-6 scrollbar-thin scrollbar-thumb-white/10">
          
          {/* TAB 1: Overview & Active Work */}
          {activeTab === 'overview' && (
            <div className="space-y-6 animate-in fade-in duration-150">
              
              {/* Bio & Focus */}
              <div className="p-4 rounded-xl bg-white/[0.02] border border-white/5 space-y-2">
                <span className="text-[10px] font-mono uppercase text-white/40 tracking-wider">Organizational Mandate</span>
                <p className="text-xs text-white/80 leading-relaxed font-light">{coworker.bio}</p>
              </div>

              {/* Current Active Task */}
              <div className="p-4 rounded-xl bg-black/60 border border-[#E1D4C0]/20 space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-mono uppercase text-[#E1D4C0]">Active Creative Workload</span>
                  <span className="text-[10px] font-mono text-emerald-400 font-semibold">{coworker.status}</span>
                </div>
                <div>
                  <h4 className="text-xs font-medium text-white">{coworker.currentWork.task}</h4>
                  <p className="text-[11px] font-mono text-white/40 mt-0.5">Campaign: {coworker.currentWork.campaign}</p>
                </div>
                <div className="space-y-1 pt-1">
                  <div className="flex justify-between text-[10px] font-mono text-white/40">
                    <span>Progress</span>
                    <span className="text-white">{coworker.currentWork.progress}% &bull; Est. {coworker.currentWork.estimatedDelivery}</span>
                  </div>
                  <div className="h-1.5 w-full bg-white/5 rounded-full overflow-hidden">
                    <div 
                      className="h-full rounded-full transition-all"
                      style={{ width: `${coworker.currentWork.progress}%`, backgroundColor: coworker.avatarColor }}
                    />
                  </div>
                </div>
              </div>

              {/* Recent Contributions */}
              <div className="space-y-3">
                <span className="text-[10px] font-mono uppercase text-white/40 tracking-wider">Recent Creative Contributions</span>
                <div className="space-y-2">
                  {coworker.recentContributions.map((contrib, idx) => (
                    <div key={idx} className="p-3.5 rounded-xl bg-white/[0.02] border border-white/5 space-y-1">
                      <div className="flex items-center justify-between text-[10px] font-mono text-white/40">
                        <span className="text-white/80 font-medium">{contrib.title}</span>
                        <span>{contrib.timestamp}</span>
                      </div>
                      <p className="text-xs text-emerald-400/90 font-light">&rarr; {contrib.impact}</p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Skills Tags */}
              <div className="space-y-2">
                <span className="text-[10px] font-mono uppercase text-white/40 tracking-wider">Governed Skills</span>
                <div className="flex flex-wrap gap-1.5">
                  {coworker.skills.map((skill, sIdx) => (
                    <span key={sIdx} className="px-2.5 py-1 rounded-lg bg-white/5 text-white/70 border border-white/10 text-[11px] font-mono">
                      {skill}
                    </span>
                  ))}
                </div>
              </div>

            </div>
          )}

          {/* TAB 2: Conversation & Tasking */}
          {activeTab === 'chat' && (
            <div className="flex flex-col h-full space-y-4 animate-in fade-in duration-150">
              
              {/* Message Feed */}
              <div className="flex-1 space-y-3 overflow-y-auto pr-1">
                {chatThread.map((msg, mIdx) => (
                  <div
                    key={mIdx}
                    className={`flex flex-col ${msg.sender === 'user' ? 'items-end' : 'items-start'}`}
                  >
                    <div className={`p-3.5 rounded-2xl max-w-[85%] text-xs leading-relaxed ${
                      msg.sender === 'user'
                        ? 'bg-[#E1D4C0] text-[#0A0A0A] font-medium rounded-tr-none'
                        : 'bg-white/[0.04] text-white/90 border border-white/5 rounded-tl-none font-light'
                    }`}>
                      {msg.text}
                    </div>
                    <span className="text-[9px] font-mono text-white/30 mt-1 px-1">{msg.time}</span>
                  </div>
                ))}
              </div>

              {/* Input Form */}
              <form onSubmit={handleSendMessage} className="pt-2 border-t border-white/5 flex items-center gap-2">
                <input
                  type="text"
                  value={messageInput}
                  onChange={(e) => setMessageInput(e.target.value)}
                  placeholder={`Ask ${coworker.name} or request a creative task...`}
                  className="flex-1 p-2.5 rounded-xl bg-white/[0.03] border border-white/10 text-xs text-white placeholder-white/30 focus:outline-none focus:border-[#E1D4C0]/50"
                />
                <button
                  type="submit"
                  className="p-2.5 rounded-xl bg-[#E1D4C0] text-[#0A0A0A] hover:opacity-90 transition-opacity"
                >
                  <Send className="w-4 h-4" />
                </button>
              </form>

            </div>
          )}

          {/* TAB 3: Recent Outputs & Handoffs */}
          {activeTab === 'handoffs' && (
            <div className="space-y-4 animate-in fade-in duration-150">
              <span className="text-[10px] font-mono uppercase text-white/40 tracking-wider">Handoff Chain of Custody</span>
              <div className="p-4 rounded-xl bg-white/[0.02] border border-white/5 space-y-3">
                <div className="flex items-center justify-between text-xs">
                  <span className="text-white font-medium">Direction 02 Concept Specification</span>
                  <span className="px-2 py-0.5 rounded text-[9px] font-mono bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                    DELIVERED
                  </span>
                </div>
                <p className="text-xs text-white/60 font-light">
                  Handed off to Aura Chen for Banarasi silk 38.4 N/m shearing stiffness verification.
                </p>
                <div className="text-[10px] font-mono text-white/30 flex items-center gap-1">
                  <GitCommit className="w-3 h-3 text-[#E1D4C0]" /> Proof Hash: 0x8f19c3b...39e1
                </div>
              </div>
            </div>
          )}

          {/* TAB 4: Governance & Capabilities */}
          {activeTab === 'governance' && (
            <div className="space-y-6 animate-in fade-in duration-150">
              
              {/* Bounded Capabilities */}
              <div className="space-y-2">
                <span className="text-[10px] font-mono uppercase text-white/40 tracking-wider flex items-center gap-1.5">
                  <ShieldCheck className="w-3.5 h-3.5 text-[#E1D4C0]" /> Bounded Operating Capabilities
                </span>
                <ul className="space-y-1.5 text-xs text-white/70">
                  {coworker.boundedCapabilities.map((cap, cIdx) => (
                    <li key={cIdx} className="flex items-start gap-2">
                      <span className="text-[#E1D4C0] font-mono">•</span>
                      <span className="font-light">{cap}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Memory Scopes */}
              <div className="space-y-2 pt-2 border-t border-white/5">
                <span className="text-[10px] font-mono uppercase text-white/40 tracking-wider flex items-center gap-1.5">
                  <Database className="w-3.5 h-3.5 text-purple-400" /> Accessible Memory Scopes
                </span>
                <div className="space-y-2">
                  {coworker.memoryScope.map((mem, mIdx) => (
                    <div key={mIdx} className="p-3 rounded-xl bg-white/[0.02] border border-white/5 flex items-center justify-between text-xs">
                      <div>
                        <div className="text-white font-medium">{mem.scope}</div>
                        <div className="text-[10px] text-white/40 font-light">{mem.description}</div>
                      </div>
                      <span className="px-2 py-0.5 rounded text-[9px] font-mono bg-purple-500/10 text-purple-300 border border-purple-500/20">
                        {mem.accessLevel}
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Human Approval Invariant */}
              <div className="p-4 rounded-xl bg-amber-500/[0.05] border border-amber-500/20 space-y-1 text-xs text-amber-200/90">
                <div className="flex items-center gap-1.5 font-semibold text-amber-300">
                  <Lock className="w-3.5 h-3.5" /> Approval Gate Invariant
                </div>
                <p className="font-light leading-relaxed">{coworker.approvalRequirements}</p>
              </div>

            </div>
          )}

        </div>

      </div>
    </div>
  );
}
