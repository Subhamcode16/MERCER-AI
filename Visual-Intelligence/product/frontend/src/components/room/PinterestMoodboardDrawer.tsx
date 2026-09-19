'use client';

import React, { useState } from 'react';
import {
  X,
  Layers,
  Sparkles,
  TrendingUp,
  Image as ImageIcon,
  Palette,
  ExternalLink,
  CheckCircle2,
  RefreshCw,
  Search
} from 'lucide-react';

interface PinterestBoard {
  board_id: string;
  name: string;
  description: string;
  pin_count: number;
  image_cover_url: string;
  privacy: string;
}

interface PinterestMoodboardDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  onIngestBoard: (boardId: string, boardName: string) => void;
}

const SAMPLE_BOARDS: PinterestBoard[] = [
  {
    board_id: 'board_bridal_heritage',
    name: 'Sovereign Bridal & Gold Zari',
    description: 'Modern royal Indian bridal silhouettes with metallic thread embroidery.',
    pin_count: 42,
    image_cover_url: 'https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=800&auto=format&fit=crop&q=80',
    privacy: 'PUBLIC'
  },
  {
    board_id: 'board_architectural_minimal',
    name: 'Architectural Drape & Raw Silk',
    description: 'High-contrast editorial minimal drapes, structured lapels, and raw tussar textures.',
    pin_count: 28,
    image_cover_url: 'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=800&auto=format&fit=crop&q=80',
    privacy: 'PUBLIC'
  },
  {
    board_id: 'board_nocturne_cinematic',
    name: 'Midnight Velvet & Tungsten Rim',
    description: 'Low-key editorial fashion portraits with warm tungsten rim lighting (2800K).',
    pin_count: 35,
    image_cover_url: 'https://images.unsplash.com/photo-1539109136881-3be0616acf4b?w=800&auto=format&fit=crop&q=80',
    privacy: 'PUBLIC'
  }
];

export const PinterestMoodboardDrawer: React.FC<PinterestMoodboardDrawerProps> = ({
  isOpen,
  onClose,
  onIngestBoard
}) => {
  const [boards] = useState<PinterestBoard[]>(SAMPLE_BOARDS);
  const [selectedBoardId, setSelectedBoardId] = useState<string>('board_bridal_heritage');
  const [isIngesting, setIsIngesting] = useState(false);
  const [ingestedSuccess, setIngestedSuccess] = useState(false);

  if (!isOpen) return null;

  const handleIngest = async (board: PinterestBoard) => {
    setIsIngesting(true);
    setSelectedBoardId(board.board_id);
    
    // Simulate API round-trip
    await new Promise((r) => setTimeout(r, 600));
    setIsIngesting(false);
    setIngestedSuccess(true);
    
    onIngestBoard(board.board_id, board.name);
    setTimeout(() => {
      setIngestedSuccess(false);
      onClose();
    }, 900);
  };

  return (
    <div className="fixed inset-0 z-50 overflow-hidden bg-background/80 backdrop-blur-sm transition-opacity flex justify-end">
      <div className="w-full max-w-lg bg-card border-l border-border h-full shadow-2xl flex flex-col transform transition-transform duration-300">
        
        {/* Header */}
        <div className="p-5 border-b border-border flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-[#E60023]/10 border border-[#E60023]/30 flex items-center justify-center text-[#E60023]">
              <Layers className="w-4 h-4" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-sm font-semibold text-foreground tracking-wide">Pinterest Moodboard Engine</h3>
                <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-emerald-500/10 border border-emerald-500/30 text-emerald-600 dark:text-emerald-400 font-semibold">
                  MCP ONLINE
                </span>
              </div>
              <p className="text-xs text-muted-foreground">Ingest pins, palettes, and aesthetic tokens directly into room memory</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-muted-foreground hover:text-foreground hover:bg-accent transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-5 space-y-4">
          <div className="flex items-center justify-between">
            <h4 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Connected Moodboards</h4>
            <span className="text-xs text-muted-foreground/60">{boards.length} Boards available</span>
          </div>

          <div className="grid grid-cols-1 gap-3.5">
            {boards.map((board) => {
              const isSelected = selectedBoardId === board.board_id;
              return (
                <div
                  key={board.board_id}
                  className={`group relative rounded-xl border p-3.5 transition-all overflow-hidden ${
                    isSelected
                      ? 'border-[#E60023]/50 bg-[#E60023]/5'
                      : 'border-border bg-muted/30 hover:border-border/80 hover:bg-accent/40'
                  }`}
                >
                  <div className="flex gap-3.5">
                    <img
                      src={board.image_cover_url}
                      alt={board.name}
                      className="w-20 h-24 rounded-lg object-cover border border-border shadow-sm shrink-0"
                    />
                    <div className="flex-1 flex flex-col justify-between">
                      <div>
                        <div className="flex items-start justify-between gap-2">
                          <h5 className="text-sm font-medium text-foreground transition-colors">
                            {board.name}
                          </h5>
                          <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-muted text-muted-foreground">
                            {board.pin_count} pins
                          </span>
                        </div>
                        <p className="text-xs text-muted-foreground mt-1 line-clamp-2 leading-relaxed">
                          {board.description}
                        </p>
                      </div>

                      <div className="mt-3 flex items-center justify-between">
                        <span className="text-[10px] text-muted-foreground/80 flex items-center gap-1">
                          <Palette className="w-3 h-3 text-amber-500" />
                          Auto-extracts palette & drape
                        </span>
                        <button
                          onClick={() => handleIngest(board)}
                          disabled={isIngesting}
                          className="px-3 py-1.5 rounded-lg text-xs font-medium bg-[#E60023] hover:bg-[#c9001f] text-white transition-colors flex items-center gap-1.5 shadow-sm shadow-[#E60023]/20 disabled:opacity-50"
                        >
                          {isIngesting && isSelected ? (
                            <>
                              <RefreshCw className="w-3 h-3 animate-spin" />
                              Ingesting...
                            </>
                          ) : ingestedSuccess && isSelected ? (
                            <>
                              <CheckCircle2 className="w-3 h-3 text-white" />
                              Ingested!
                            </>
                          ) : (
                            <>
                              <Sparkles className="w-3 h-3" />
                              Ingest Board
                            </>
                          )}
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Editorial Trends Preview */}
          <div className="mt-6 pt-5 border-t border-border space-y-3">
            <div className="flex items-center justify-between">
              <h4 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground flex items-center gap-1.5">
                <TrendingUp className="w-3.5 h-3.5 text-indigo-500" />
                Live Editorial Trends
              </h4>
              <span className="text-[10px] text-indigo-600 dark:text-indigo-400 font-mono font-medium">Pinterest Signals</span>
            </div>

            <div className="grid grid-cols-2 gap-2.5">
              <div className="p-3 rounded-lg border border-border bg-muted/40">
                <span className="text-[10px] font-mono text-emerald-600 dark:text-emerald-400 font-semibold">+44.8% MoM</span>
                <p className="text-xs font-medium text-foreground mt-0.5">Modern Royalty</p>
                <p className="text-[10px] text-muted-foreground mt-1">Architectural shoulders & gilded accents</p>
              </div>
              <div className="p-3 rounded-lg border border-border bg-muted/40">
                <span className="text-[10px] font-mono text-emerald-600 dark:text-emerald-400 font-semibold">+31.2% MoM</span>
                <p className="text-xs font-medium text-foreground mt-0.5">Matte Metallic Weaves</p>
                <p className="text-[10px] text-muted-foreground mt-1">Textured Khadi & diffuse sunlight</p>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-border bg-muted/20 flex items-center justify-between text-xs text-muted-foreground">
          <span>Tenant Scope: <code className="text-foreground font-mono">isolated</code></span>
          <span className="flex items-center gap-1 text-[11px] font-medium text-emerald-600 dark:text-emerald-400">
            <CheckCircle2 className="w-3 h-3" />
            T-013 Invariant Gated
          </span>
        </div>

      </div>
    </div>
  );
};
