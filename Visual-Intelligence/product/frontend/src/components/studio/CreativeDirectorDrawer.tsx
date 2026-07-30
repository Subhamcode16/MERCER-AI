'use client';

import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Sparkles, GraduationCap } from 'lucide-react';
import { CREBentoGrid, type CREScores } from './CREBentoGrid';
import { PromptInputBox } from '../ui/ai-prompt-box';

interface Message {
  id: string;
  sender: 'user' | 'director';
  text: string;
  timestamp: string;
  tweak?: {
    label: string;
    affectedParameters: {
      background?: string;
      pose?: string;
      lighting?: string;
    };
  };
}

interface CreativeDirectorDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  selectedBackground: string;
  selectedPose: string;
  selectedLighting: string;
  onApplyTweak: (params: { background?: string; pose?: string; lighting?: string }) => void;
  creScores: CREScores | null;
}

export function CreativeDirectorDrawer({
  isOpen,
  onClose,
  selectedBackground,
  selectedPose,
  selectedLighting,
  onApplyTweak,
  creScores
}: CreativeDirectorDrawerProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome',
      sender: 'director',
      text: "Welcome to the Creative Intelligence Studio. I've analyzed your specimen's textile DNA. How can we collaboratively refine the visual direction for this campaign?",
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  ]);
  const [isResponding, setIsResponding] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendBox = (text: string) => {
    if (!text.trim()) return;

    const userMsg: Message = {
      id: Date.now().toString(),
      sender: 'user',
      text,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev => [...prev, userMsg]);
    setIsResponding(true);

    setTimeout(() => {
      let directorText = "I see. Let's think about how that affects the visual narrative. For this fabric, it's best to maintain directional lighting to highlight the details.";
      let tweak: Message['tweak'] = undefined;

      const lowerInput = text.toLowerCase();
      
      if (lowerInput.includes('lighting') || lowerInput.includes('bright') || lowerInput.includes('dark')) {
        directorText = "Regarding lighting: High-key setups will flatten the metallic highlights of the Zari brocade. I recommend 'Ethereal Backlight / Edge Wrap' because it wraps the edges in light, preserving the micro-contrast of the weave while teaching the viewer about the silk's texture. Shall we update the lighting?";
        tweak = {
          label: "Set lighting to Ethereal Backlight",
          affectedParameters: { lighting: "Ethereal Backlight / Edge Wrap" }
        };
      } else if (lowerInput.includes('pose') || lowerInput.includes('motion') || lowerInput.includes('toss')) {
        directorText = "For poses, we must respect fabric physics. Stiff Banarasi silk has a heavy drape coefficient. A wind-blown toss will look forced and blocky. Instead, 'Dynamic Fabric Spin' leverages the fabric's heavy momentum to flare the pleats out architecturally, showing the structure. Would you like to switch to the spin pose?";
        tweak = {
          label: "Set pose to Dynamic Fabric Spin",
          affectedParameters: { pose: "Dynamic Fabric Spin" }
        };
      } else if (lowerInput.includes('background') || lowerInput.includes('palace') || lowerInput.includes('garden')) {
        directorText = "For the backdrop, palatial corridor elements create a strong heritage contrast that grounds the Banarasi origins, whereas a Persian carpet backdrop adds high textual complexity. I recommend the 'Nighttime Palace' to create high contrast. Let's apply it?";
        tweak = {
          label: "Set background to Nighttime Palace",
          affectedParameters: { background: "Nighttime Palace" }
        };
      } else {
        directorText = "To elevate this campaign, we should align the lighting and pose to respect the weave's surface properties. For example, backlighting always brings out the dimensional details of zari threads, while architectural poses show off the fabric's natural body. Let me know which direction you want to explore.";
      }

      const directorMsg: Message = {
        id: (Date.now() + 1).toString(),
        sender: 'director',
        text: directorText,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        tweak
      };

      setMessages(prev => [...prev, directorMsg]);
      setIsResponding(false);
    }, 1200);
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Transparent Backdrop - allows clicking outside to close */}
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40"
          />

          {/* Centered Modal Content Card - Transparent background with radial blur glow */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95, x: '-50%', y: '-50%' }}
            animate={{ opacity: 1, scale: 1, x: '-50%', y: '-50%' }}
            exit={{ opacity: 0, scale: 0.95, x: '-50%', y: '-50%' }}
            transition={{ duration: 0.3, ease: 'easeOut' }}
            className="fixed left-1/2 top-1/2 w-full max-w-2xl h-[80vh] z-50 flex flex-col pointer-events-auto bg-transparent"
          >
            {/* Glow Core */}
            <div className="absolute inset-0 bg-gradient-to-tr from-purple-600/10 via-pink-600/5 to-transparent rounded-3xl blur-3xl -z-10 pointer-events-none animate-pulse" />
            <div className="absolute -inset-4 bg-gradient-to-tr from-[#9b87f5]/20 to-[#F97316]/10 rounded-[40px] blur-2xl -z-10 pointer-events-none" />

            {/* Main transparent glassmorphic window */}
            <div className="flex-1 flex flex-col rounded-3xl border border-white/10 bg-zinc-950/20 backdrop-blur-2xl overflow-hidden shadow-[0_0_50px_0_rgba(155,135,245,0.15)]">
              
              {/* Header */}
              <div className="p-5 border-b border-white/5 flex items-center justify-between bg-black/10">
                <div className="flex items-center gap-2">
                  <GraduationCap className="w-5 h-5 text-[#E1D4C0]" />
                  <h3 className="font-serif text-lg text-white">Creative Director</h3>
                </div>
                <button 
                  onClick={onClose}
                  className="p-1.5 rounded-full hover:bg-white/10 text-white/50 hover:text-white transition-colors"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>

              {/* Body */}
              <div className="flex-1 overflow-y-auto p-5 space-y-6 flex flex-col min-h-0">
                
                {/* CRE Bento Grid Section */}
                {creScores && (
                  <div className="space-y-3 shrink-0">
                    <h4 className="text-[10px] tracking-[0.2em] uppercase text-white/40 font-medium text-left">Simulation Health Check</h4>
                    <CREBentoGrid scores={creScores} />
                  </div>
                )}

                {/* Chat Thread */}
                <div className="flex-1 flex flex-col gap-4 overflow-y-auto min-h-0 pr-1">
                  <div className="text-[10px] tracking-[0.2em] uppercase text-white/40 font-medium mb-1 text-left">Creative Dialogue</div>
                  
                  {messages.map(msg => (
                    <div 
                      key={msg.id}
                      className={`flex flex-col max-w-[85%] ${
                        msg.sender === 'user' ? 'self-end items-end' : 'self-start items-start'
                      }`}
                    >
                      <div 
                        className={`p-3.5 rounded-2xl text-[13px] leading-relaxed shadow-sm ${
                          msg.sender === 'user' 
                            ? 'bg-[#E1D4C0] text-black rounded-tr-none font-medium' 
                            : 'bg-zinc-900/60 border border-white/10 text-zinc-100 rounded-tl-none font-light backdrop-blur-md'
                        }`}
                      >
                        {msg.text}

                        {/* Interactive Tweak Block */}
                        {msg.tweak && (
                          <div className="mt-4 pt-3 border-t border-white/10 flex flex-col gap-2">
                            <span className="text-[11px] text-[#E1D4C0] font-mono flex items-center gap-1.5 font-medium">
                              <Sparkles className="w-3 h-3 animate-pulse" /> Proposed Tweak
                            </span>
                            <button
                              onClick={() => {
                                onApplyTweak(msg.tweak!.affectedParameters);
                                // Remove the tweak button after apply
                                setMessages(prev => 
                                  prev.map(m => m.id === msg.id ? { ...m, tweak: undefined } : m)
                                );
                              }}
                              className="w-full py-2 rounded-md bg-[#E1D4C0]/15 hover:bg-[#E1D4C0]/25 border border-[#E1D4C0]/35 text-[#E1D4C0] text-xs font-semibold tracking-wider uppercase transition-colors"
                            >
                              {msg.tweak.label}
                            </button>
                          </div>
                        )}
                      </div>
                      <span className="text-[9px] text-white/20 mt-1 font-mono">{msg.timestamp}</span>
                    </div>
                  ))}
                  <div ref={messagesEndRef} />
                </div>
              </div>

              {/* Embedded V2 Prompt Input Box at bottom */}
              <div className="p-4 bg-transparent border-t border-white/10">
                <PromptInputBox 
                  onSend={handleSendBox}
                  isLoading={isResponding}
                  placeholder="Ask the Director about physical adjustments..."
                  className="bg-black/30 border-white/10 shadow-[0_0_30px_0_rgba(155,135,245,0.05)]"
                />
              </div>

            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
