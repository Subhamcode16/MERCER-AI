import { useCallback, useId, useMemo, useRef, useState } from "react";
import type { KeyboardEvent, PointerEvent as ReactPointerEvent } from "react";
import type { Thread } from "./types";
import "./ChapterScrubber.css";

export interface ChapterItem {
  id: string;
  time: string;
  title: string;
  description: string;
  tick?: number;
}

export const defaultChapters: ChapterItem[] = [
  {
    id: "ch-1",
    time: "00:15",
    title: "project overview & goals",
    description: "Initial walkthrough of the architecture and core design principles.",
    tick: 3,
  },
  {
    id: "ch-2",
    time: "01:38",
    title: "add roving tabindex + arrow keys",
    description: "Up/Down walk the rail, Home/End jump to the ends, Enter selects. Only one tick is tabbable at a time.",
    tick: 11,
  },
  {
    id: "ch-3",
    time: "02:41",
    title: "re-read my own diff",
    description: "Skimmed the change end to end and trimmed a comment that no longer matched the code.",
    tick: 18,
  },
  {
    id: "ch-4",
    time: "03:52",
    title: "extract scrubber physics hook",
    description: "Extracted spring animation and gaussian magnification curve into reusable state.",
    tick: 24,
  },
  {
    id: "ch-5",
    time: "04:30",
    title: "keyboard & voice testing",
    description: "Verified screen reader announcements, high contrast mode, and sound feedback.",
    tick: 28,
  },
];

export function getThreadChapters(thread?: Thread): ChapterItem[] {
  if (!thread || !thread.events || thread.events.length === 0) {
    return defaultChapters;
  }

  const events = thread.events;
  const count = events.length;

  return events.map((e, idx) => {
    const minutes = Math.floor((idx * 45) / 60);
    const seconds = (idx * 45) % 60;
    const time = `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;

    let title = "";
    let description = "";

    if (e.kind === "user") {
      title = "You: " + (e.text.slice(0, 30) + (e.text.length > 30 ? "…" : ""));
      description = e.text;
    } else if (e.kind === "tool") {
      title = "Source workspace access";
      description = "Open workspace to grant simulated document source access.";
    } else if (e.kind === "review") {
      title = "Landscape brief · draft v1";
      description = "Three recommendations grounded in example source collection.";
    } else if (e.kind === "event") {
      title = "System milestone";
      description = e.text;
    } else {
      const sender = e.actor?.name || "Orchestrator";
      title = `${sender}: ` + (e.text.slice(0, 30) + (e.text.length > 30 ? "…" : ""));
      description = e.text;
    }

    const tick = Math.round((idx / Math.max(1, count - 1)) * 26) + 3;

    return {
      id: e.id,
      time,
      title,
      description,
      tick,
    };
  });
}

export interface ChapterScrubberProps {
  chapters?: ChapterItem[];
  totalTicks?: number;
  initialChapterId?: string;
  onSelectChapter?: (chapter: ChapterItem, tickIndex: number) => void;
  className?: string;
  alwaysShowCard?: boolean;
}

export function ChapterScrubber({
  chapters = defaultChapters,
  totalTicks = 32,
  initialChapterId,
  onSelectChapter,
  className = "",
  alwaysShowCard = false,
}: ChapterScrubberProps) {
  const railRef = useRef<HTMLDivElement>(null);
  const liveRegionId = useId();

  // Map chapters to ticks
  const chapterMap = useMemo(() => {
    const map = new Map<number, ChapterItem>();
    chapters.forEach((ch, idx) => {
      const tick = ch.tick !== undefined ? ch.tick : Math.round((idx / (chapters.length - 1 || 1)) * (totalTicks - 1));
      map.set(Math.max(0, Math.min(totalTicks - 1, tick)), ch);
    });
    return map;
  }, [chapters, totalTicks]);

  // Initial tick index
  const initialTick = useMemo(() => {
    if (initialChapterId) {
      for (const [tick, ch] of chapterMap.entries()) {
        if (ch.id === initialChapterId) return tick;
      }
    }
    return chapters[1]?.tick ?? 11;
  }, [initialChapterId, chapterMap, chapters]);

  const [selectedTick, setSelectedTick] = useState(initialTick);
  const [hoveredTick, setHoveredTick] = useState<number | null>(null);
  const [focusedTick, setFocusedTick] = useState<number | null>(null);
  const [isHovering, setIsHovering] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const [announcement, setAnnouncement] = useState("");

  // Interaction active state
  const isInteracting = alwaysShowCard || isHovering || isDragging || focusedTick !== null;
  const activePos = hoveredTick !== null ? hoveredTick : focusedTick !== null ? focusedTick : selectedTick;

  // Find the closest chapter to active position
  const currentChapter = useMemo(() => {
    if (chapterMap.has(Math.round(activePos))) {
      return chapterMap.get(Math.round(activePos))!;
    }
    let closest = chapters[0];
    let minDiff = Infinity;
    for (const [tick, ch] of chapterMap.entries()) {
      const diff = Math.abs(tick - activePos);
      if (diff < minDiff) {
        minDiff = diff;
        closest = ch;
      }
    }
    return closest;
  }, [activePos, chapterMap, chapters]);

  // Select a tick/chapter
  const selectTick = useCallback(
    (tickIndex: number) => {
      const clamped = Math.max(0, Math.min(totalTicks - 1, tickIndex));
      setSelectedTick(clamped);
      const ch = chapterMap.get(clamped) || currentChapter;
      setAnnouncement(`Selected chapter: ${ch.title} at ${ch.time}`);
      onSelectChapter?.(ch, clamped);
    },
    [totalTicks, chapterMap, currentChapter, onSelectChapter]
  );

  // Calculate tick line properties with Gaussian Magnification curve
  const getTickStyle = useCallback(
    (index: number) => {
      if (!isInteracting) {
        // Resting calm state
        const hasChapter = chapterMap.has(index);
        return {
          width: hasChapter ? "14px" : "10px",
          height: "2px",
          opacity: hasChapter ? "0.45" : "0.22",
        };
      }

      // Active Magnification Wave
      const dist = Math.abs(index - activePos);
      const sigma = 2.4;
      const factor = Math.exp(-(dist * dist) / (2 * sigma * sigma));

      const minWidth = 10;
      const maxWidth = 48;
      const width = minWidth + (maxWidth - minWidth) * factor;

      const minOpacity = 0.22;
      const maxOpacity = 1.0;
      const opacity = minOpacity + (maxOpacity - minOpacity) * factor;

      const height = factor > 0.8 ? 2.5 : 2;

      return {
        width: `${width.toFixed(1)}px`,
        height: `${height}px`,
        opacity: opacity.toFixed(2),
      };
    },
    [isInteracting, activePos, chapterMap]
  );

  // Calculate pointer Y to tick index
  const getTickFromPointer = useCallback(
    (clientY: number) => {
      if (!railRef.current) return 0;
      const rect = railRef.current.getBoundingClientRect();
      const relativeY = clientY - rect.top;
      const tickHeight = rect.height / totalTicks;
      const tick = relativeY / tickHeight;
      return Math.max(0, Math.min(totalTicks - 1, tick));
    },
    [totalTicks]
  );

  // Pointer drag/scrub handlers
  const handlePointerDown = (e: ReactPointerEvent<HTMLDivElement>) => {
    setIsDragging(true);
    setIsHovering(true);
    e.currentTarget.setPointerCapture(e.pointerId);
    const tick = getTickFromPointer(e.clientY);
    setHoveredTick(tick);
    selectTick(Math.round(tick));
  };

  const handlePointerMove = (e: ReactPointerEvent<HTMLDivElement>) => {
    const tick = getTickFromPointer(e.clientY);
    setHoveredTick(tick);
    setIsHovering(true);
    if (isDragging) {
      selectTick(Math.round(tick));
    }
  };

  const handlePointerUp = (e: ReactPointerEvent<HTMLDivElement>) => {
    if (isDragging) {
      setIsDragging(false);
      try {
        e.currentTarget.releasePointerCapture(e.pointerId);
      } catch {
        // already released
      }
      const tick = getTickFromPointer(e.clientY);
      selectTick(Math.round(tick));
    }
  };

  const handlePointerEnter = () => {
    setIsHovering(true);
  };

  const handlePointerLeave = () => {
    if (!isDragging) {
      setIsHovering(false);
      setHoveredTick(null);
    }
  };

  // Keyboard navigation (Roving Tabindex)
  const handleKeyDown = (e: KeyboardEvent<HTMLDivElement>) => {
    let nextTick: number | null = null;

    switch (e.key) {
      case "ArrowUp":
      case "ArrowLeft":
        e.preventDefault();
        nextTick = Math.max(0, selectedTick - 1);
        break;
      case "ArrowDown":
      case "ArrowRight":
        e.preventDefault();
        nextTick = Math.min(totalTicks - 1, selectedTick + 1);
        break;
      case "PageUp":
        e.preventDefault();
        nextTick = Math.max(0, selectedTick - 4);
        break;
      case "PageDown":
        e.preventDefault();
        nextTick = Math.min(totalTicks - 1, selectedTick + 4);
        break;
      case "Home":
        e.preventDefault();
        nextTick = 0;
        break;
      case "End":
        e.preventDefault();
        nextTick = totalTicks - 1;
        break;
      case "Enter":
      case " ":
        e.preventDefault();
        selectTick(selectedTick);
        return;
      case "Escape":
        railRef.current?.blur();
        setFocusedTick(null);
        return;
      default:
        return;
    }

    if (nextTick !== null) {
      setSelectedTick(nextTick);
      setFocusedTick(nextTick);
      setHoveredTick(null);
      const ch = chapterMap.get(nextTick) || currentChapter;
      onSelectChapter?.(ch, nextTick);

      const tickButton = railRef.current?.querySelector<HTMLButtonElement>(
        `[data-tick-index="${nextTick}"]`
      );
      tickButton?.focus();
    }
  };

  // Card Y offset calculation
  const tickSpacing = 14;
  const cardOffsetY = Math.max(0, activePos * tickSpacing - 38);

  return (
    <div className={`chapter-scrubber-wrapper ${className} ${isInteracting ? "is-active" : ""}`}>
      <div className="chapter-scrubber-container">
        {/* Screen Reader Live Announcement */}
        <div id={liveRegionId} className="scrubber-sr-only" aria-live="polite" aria-atomic="true">
          {announcement}
        </div>

        {/* Vertical Rail of Tick Marks */}
        <div
          ref={railRef}
          className="scrubber-rail"
          role="slider"
          aria-label="Chapter timeline scrubber"
          aria-valuemin={0}
          aria-valuemax={totalTicks - 1}
          aria-valuenow={Math.round(activePos)}
          aria-valuetext={`${currentChapter.time} - ${currentChapter.title}`}
          onPointerEnter={handlePointerEnter}
          onPointerDown={handlePointerDown}
          onPointerMove={handlePointerMove}
          onPointerUp={handlePointerUp}
          onPointerCancel={handlePointerUp}
          onPointerLeave={handlePointerLeave}
          onKeyDown={handleKeyDown}
          tabIndex={0}
          onFocus={() => setFocusedTick(selectedTick)}
          onBlur={() => setFocusedTick(null)}
        >
          {Array.from({ length: totalTicks }, (_, index) => {
            const hasChapter = chapterMap.has(index);
            const isSelected = selectedTick === index;
            const style = getTickStyle(index);

            return (
              <button
                key={index}
                type="button"
                data-tick-index={index}
                className={`scrubber-tick ${hasChapter ? "has-chapter" : ""} ${
                  isSelected ? "is-selected" : ""
                }`}
                tabIndex={isSelected ? 0 : -1}
                aria-label={
                  hasChapter
                    ? `Chapter at ${chapterMap.get(index)!.time}: ${
                        chapterMap.get(index)!.title
                      }`
                    : `Tick ${index + 1}`
                }
                onClick={(e) => {
                  e.stopPropagation();
                  selectTick(index);
                }}
              >
                <span className="scrubber-tick-line" style={style} />
              </button>
            );
          })}
        </div>

        {/* Floating Chapter Card Tooltip (visible only when interacting) */}
        <div
          className={`scrubber-card-anchor ${isInteracting ? "visible" : "hidden"}`}
          aria-hidden={!isInteracting}
        >
          <div
            className="scrubber-card"
            style={{
              transform: `translateY(${cardOffsetY}px) scale(${isInteracting ? 1 : 0.95})`,
              opacity: isInteracting ? 1 : 0,
              pointerEvents: isInteracting ? "auto" : "none",
            }}
          >
            <div className="scrubber-card-time">{currentChapter.time}</div>
            <div className="scrubber-card-title">{currentChapter.title}</div>
            <p className="scrubber-card-desc">{currentChapter.description}</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export function ChapterScrubberDemo({ thread }: { thread?: Thread }) {
  const chapters = useMemo(() => getThreadChapters(thread), [thread]);
  const [selected, setSelected] = useState<ChapterItem>(chapters[1] || chapters[0]);

  const handleSelect = (ch: ChapterItem) => {
    setSelected(ch);
    const element = document.getElementById("event-" + ch.id);
    element?.scrollIntoView({ behavior: "smooth", block: "center" });
  };

  return (
    <div className="scrubber-demo-container">
      <div className="scrubber-demo-header">
        <h3>Conversation Milestones</h3>
        <p>Hover and glide over the rail or use arrow keys to jump between checkpoints</p>
      </div>

      <ChapterScrubber
        chapters={chapters}
        initialChapterId={selected.id}
        onSelectChapter={handleSelect}
        alwaysShowCard={true}
      />

      <div className="scrubber-demo-footer">
        <span>
          <kbd>↑</kbd> <kbd>↓</kbd> Walk rail
        </span>
        <span>
          <kbd>Home</kbd> <kbd>End</kbd> First / Last
        </span>
        <span>
          <kbd>Enter</kbd> Jump to event
        </span>
      </div>
    </div>
  );
}
