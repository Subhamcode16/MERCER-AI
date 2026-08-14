"use client";

import { motion, AnimatePresence } from "framer-motion";
import { useState, useRef, useEffect } from "react";
import { Folder, Plus, Check, ChevronRight, ChevronDown, FolderOpen, MoreHorizontal, Edit2, Share2, Trash2 } from "lucide-react";
import { CampaignFolder, ChatSession } from "./types";
import { cn } from "@/lib/utils";

interface CanvasFolderPopoverProps {
  campaigns: CampaignFolder[];
  activeCampaignId: string;
  activeSessionId: string;
  onSelectSession: (campaignId: string, sessionId: string) => void;
  onCreateSession: (campaignId: string) => void;
  onRenameSession: (campaignId: string, sessionId: string, newName: string) => void;
  onDeleteSession: (campaignId: string, sessionId: string) => void;
  onClose: () => void;
}

export function CanvasFolderPopover({
  campaigns,
  activeCampaignId,
  activeSessionId,
  onSelectSession,
  onCreateSession,
  onRenameSession,
  onDeleteSession,
  onClose,
}: CanvasFolderPopoverProps) {
  const [expandedId, setExpandedId] = useState<string>(activeCampaignId);
  
  // Inline edit state
  const [editingSessionId, setEditingSessionId] = useState<string | null>(null);
  const [editValue, setEditValue] = useState<string>("");
  const inputRef = useRef<HTMLInputElement>(null);

  // Custom Popover menu state
  const [openMenuId, setOpenMenuId] = useState<string | null>(null);
  const [copiedId, setCopiedId] = useState<string | null>(null);

  // Focus input when editing
  useEffect(() => {
    if (editingSessionId && inputRef.current) {
      inputRef.current.focus();
      inputRef.current.select();
    }
  }, [editingSessionId]);

  // Click outside to close menu
  useEffect(() => {
    if (!openMenuId) return;
    const handleClick = () => setOpenMenuId(null);
    
    setTimeout(() => {
      document.addEventListener("click", handleClick);
    }, 10);
    
    return () => document.removeEventListener("click", handleClick);
  }, [openMenuId]);

  return (
    <motion.div
      initial={{ opacity: 0, y: 15, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: 15, scale: 0.95 }}
      transition={{ duration: 0.18, ease: [0.22, 1, 0.36, 1] }}
      className="absolute bottom-[calc(100%+12px)] left-0 z-50 bg-[#0B0B0D]/98 border border-white/10 rounded-2xl shadow-[0_20px_50px_rgba(0,0,0,0.6)] backdrop-blur-2xl p-4 w-[350px] text-[#E1D4C0] select-none"
    >
      <div className="flex items-center justify-between border-b border-white/10 pb-2.5 mb-3">
        <div className="flex items-center gap-2">
          <FolderOpen size={15} className="text-[#E1D4C0]" />
          <span className="text-[10px] font-mono tracking-wider uppercase font-semibold">
            Campaign Directories
          </span>
        </div>
        <span className="text-[9px] font-mono text-white/30 uppercase tracking-widest">
          {campaigns.length} folders
        </span>
      </div>

      <div className="space-y-3.5 max-h-[280px] overflow-y-auto pr-1 scrollbar-none pb-8">
        {campaigns.map((campaign) => {
          const isActive = campaign.id === activeCampaignId;
          const isExpanded = campaign.id === expandedId;

          return (
            <div key={campaign.id} className="flex flex-col gap-1.5">
              {/* Campaign Header Folder Row */}
              <div
                onClick={() => setExpandedId(isExpanded ? "" : campaign.id)}
                className={cn(
                  "flex items-center justify-between p-2 rounded-xl transition-all cursor-pointer border border-transparent",
                  isActive
                    ? "bg-white/[0.04] text-white border-white/5"
                    : "hover:bg-white/[0.02] text-white/60 hover:text-white",
                  isExpanded && !isActive && "bg-white/[0.02]"
                )}
              >
                <div className="flex items-center gap-2.5 min-w-0">
                  <Folder
                    size={14}
                    className={cn(
                      isActive ? "text-[#E1D4C0] fill-[#E1D4C0]/10" : "text-white/40",
                      isExpanded && !isActive && "text-white/80"
                    )}
                  />
                  <span className="text-[11.5px] font-serif tracking-wide truncate">
                    {campaign.name}
                  </span>
                </div>
                {isExpanded ? (
                  <ChevronDown size={14} className={isActive ? "text-white/30" : "text-white/40"} />
                ) : (
                  <ChevronRight size={14} className="text-white/20" />
                )}
              </div>

              {/* Nested Chat Sessions List (visible for expanded campaign) */}
              {isExpanded && (
                <div className="pl-6 ml-3.5 border-l border-white/10 flex flex-col gap-1">
                  {campaign.sessions.map((session) => {
                    const isSessionActive = session.id === activeSessionId && isActive;

                    return (
                      <div key={session.id} className="relative group/session w-full">
                        {editingSessionId === session.id ? (
                          <div className="w-full flex items-center py-1 px-2 rounded-lg bg-black/60 border border-white/20 my-0.5">
                            <input
                              ref={inputRef}
                              value={editValue}
                              onChange={(e) => setEditValue(e.target.value)}
                              onBlur={() => {
                                if (editValue.trim() && editValue !== session.name) onRenameSession(campaign.id, session.id, editValue.trim());
                                setEditingSessionId(null);
                              }}
                              onKeyDown={(e) => {
                                if (e.key === "Enter") {
                                  if (editValue.trim() && editValue !== session.name) onRenameSession(campaign.id, session.id, editValue.trim());
                                  setEditingSessionId(null);
                                } else if (e.key === "Escape") {
                                  setEditingSessionId(null);
                                }
                              }}
                              className="bg-transparent outline-none text-white w-full font-medium text-[11px]"
                            />
                          </div>
                        ) : (
                          <button
                            onClick={() => onSelectSession(campaign.id, session.id)}
                            className={cn(
                              "w-full flex items-center justify-between py-1.5 px-2.5 rounded-lg text-left text-[11px] font-sans font-light transition-colors group cursor-pointer",
                              isSessionActive
                                ? "bg-[#E1D4C0]/10 text-white font-medium"
                                : "text-white/40 hover:text-white/80 hover:bg-white/[0.02]"
                            )}
                          >
                            <span className="truncate pr-6">{session.name}</span>
                            {isSessionActive && (
                              <Check size={11} className="text-[#E1D4C0] shrink-0 mr-4" />
                            )}
                          </button>
                        )}

                        {/* Three dot menu button */}
                        {!editingSessionId && (
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              setOpenMenuId(openMenuId === session.id ? null : session.id);
                            }}
                            className={cn(
                              "absolute right-1.5 top-1/2 -translate-y-1/2 p-1 rounded transition-all z-10",
                              openMenuId === session.id 
                                ? "bg-white/15 text-white" 
                                : "bg-black/60 border border-white/10 text-white/40 hover:text-white hover:bg-white/20"
                            )}
                          >
                            <MoreHorizontal size={11} />
                          </button>
                        )}

                        {/* Custom Dropdown Menu */}
                        <AnimatePresence>
                          {openMenuId === session.id && (
                            <motion.div
                              initial={{ opacity: 0, scale: 0.95, y: -5 }}
                              animate={{ opacity: 1, scale: 1, y: 0 }}
                              exit={{ opacity: 0, scale: 0.95, y: -5 }}
                              transition={{ duration: 0.15 }}
                              className="absolute right-0 top-[110%] mt-1 w-32 bg-[#0C0C0E]/98 backdrop-blur-xl border border-white/15 rounded-lg p-1.5 shadow-[0_10px_30px_rgba(0,0,0,0.8)] z-50"
                            >
                              <button
                                onClick={(e) => {
                                  e.stopPropagation();
                                  setOpenMenuId(null);
                                  setEditingSessionId(session.id);
                                  setEditValue(session.name);
                                }}
                                className="w-full flex items-center gap-2 px-2 py-1.5 text-[10px] font-mono text-white/70 hover:text-white hover:bg-white/10 rounded transition-colors text-left"
                              >
                                <Edit2 size={10} /> Rename
                              </button>
                              <button
                                onClick={(e) => {
                                  e.stopPropagation();
                                  navigator.clipboard.writeText(`https://mercer.com/team/share/${session.id}`);
                                  setCopiedId(session.id);
                                  setTimeout(() => { setCopiedId(null); setOpenMenuId(null); }, 1500);
                                }}
                                className="w-full flex items-center gap-2 px-2 py-1.5 text-[10px] font-mono text-white/70 hover:text-white hover:bg-white/10 rounded transition-colors text-left"
                              >
                                {copiedId === session.id ? <Check size={10} className="text-emerald-400" /> : <Share2 size={10} />}
                                {copiedId === session.id ? "Copied!" : "Share"}
                              </button>
                              <div className="w-full h-px bg-white/10 my-1" />
                              <button
                                onClick={(e) => {
                                  e.stopPropagation();
                                  setOpenMenuId(null);
                                  onDeleteSession(campaign.id, session.id);
                                }}
                                className="w-full flex items-center gap-2 px-2 py-1.5 text-[10px] font-mono text-red-400 hover:bg-red-500/10 hover:text-red-300 rounded transition-colors text-left"
                              >
                                <Trash2 size={10} /> Delete
                              </button>
                            </motion.div>
                          )}
                        </AnimatePresence>
                      </div>
                    );
                  })}

                  {/* Add New Chat Session Action */}
                  <button
                    onClick={() => onCreateSession(campaign.id)}
                    className="w-full flex items-center gap-2 py-1.5 px-2.5 rounded-lg text-left text-[10px] font-mono text-white/30 hover:text-[#E1D4C0] hover:bg-white/[0.02] transition-colors mt-0.5 cursor-pointer"
                  >
                    <Plus size={11} />
                    <span>NEW CHAT SESSION</span>
                  </button>
                </div>
              )}
            </div>
          );
        })}
      </div>

      <div className="border-t border-white/5 pt-2.5 mt-3 flex items-center justify-between text-[9px] font-mono text-white/20 absolute bottom-4 left-4 right-4 bg-[#0B0B0D]">
        <span>Click folders to switch context</span>
        <button
          onClick={onClose}
          className="text-white/40 hover:text-white transition-colors uppercase font-medium cursor-pointer"
        >
          Close
        </button>
      </div>
    </motion.div>
  );
}
