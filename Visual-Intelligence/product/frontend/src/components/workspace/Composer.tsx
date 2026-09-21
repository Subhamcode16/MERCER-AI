import { useEffect, useLayoutEffect, useRef, useState } from "react";
import type { CSSProperties, KeyboardEvent } from "react";
import type { Agent } from "./types";
import { Icon, IconButton } from "./Icon";
const permissions = [
  {
    id: "ask",
    name: "Ask every time",
    description: "Request confirmation before each action.",
  },
  {
    id: "limited",
    name: "Approve routine actions",
    description:
      "Allow routine reversible work; ask before external or consequential actions.",
  },
  {
    id: "review",
    name: "Prepare for review",
    description: "Research and draft only; take no external action.",
  },
];
const models = [
  {
    id: "balanced",
    name: "Balanced",
    description: "General work · balanced speed and detail",
  },
  {
    id: "fast",
    name: "Fast",
    description: "Short tasks · prioritize quick responses",
  },
  {
    id: "reasoning",
    name: "Reasoning",
    description: "Complex planning · prioritize depth",
  },
];
const commands = [
  {
    id: "summarize",
    name: "summarize",
    description: "Condense the conversation",
    icon: "file" as const,
  },
  {
    id: "rewrite",
    name: "rewrite",
    description: "Improve tone and clarity",
    icon: "model" as const,
  },
  {
    id: "translate",
    name: "translate",
    description: "Translate to another language",
    icon: "arrow" as const,
  },
  {
    id: "todo",
    name: "todo",
    description: "Create a task",
    icon: "check" as const,
  },
  {
    id: "remind",
    name: "remind",
    description: "Set a reminder",
    icon: "watch" as const,
  },
];
interface SpeechResult {
  isFinal: boolean;
  0: { transcript: string };
}
interface Recognition {
  continuous: boolean;
  interimResults: boolean;
  lang: string;
  onstart: (() => void) | null;
  onend: (() => void) | null;
  onerror: ((e: { error: string }) => void) | null;
  onresult: ((e: { results: ArrayLike<SpeechResult> }) => void) | null;
  start: () => void;
  stop: () => void;
  abort: () => void;
}
type SpeechWindow = Window & {
  SpeechRecognition?: new () => Recognition;
  webkitSpeechRecognition?: new () => Recognition;
};
export interface PromptSettings {
  permission: string;
  model: string;
}
export function Composer({
  name,
  draft,
  onDraft,
  onSend,
  members,
  settings,
  onSettings,
  files,
  onFiles,
}: {
  name: string;
  draft: string;
  onDraft: (text: string) => void;
  onSend: (text: string) => void;
  members: Agent[];
  settings: PromptSettings;
  onSettings: (settings: PromptSettings) => void;
  files: File[];
  onFiles: (files: File[]) => void;
}) {
  const [open, setOpen] = useState<
      "attachments" | "permissions" | "models" | null
    >(null),
    [notice, setNotice] = useState(""),
    [listening, setListening] = useState(false),
    [transcript, setTranscript] = useState(""),
    [bars, setBars] = useState<number[]>(Array(35).fill(4)),
    [suggestionIndex, setSuggestionIndex] = useState(0),
    [suggestionDismissed, setSuggestionDismissed] = useState(false),
    [viewportVersion, setViewportVersion] = useState(0),
    [suggestionPosition, setSuggestionPosition] = useState({
      left: 12,
      top: 42,
    });
  const root = useRef<HTMLDivElement>(null),
    input = useRef<HTMLTextAreaElement>(null),
    mirror = useRef<HTMLDivElement>(null),
    caretAnchor = useRef<HTMLSpanElement>(null),
    picker = useRef<HTMLInputElement>(null),
    popup = useRef<HTMLDivElement>(null),
    suggestionListRef = useRef<HTMLDivElement>(null),
    triggers = useRef<Record<string, HTMLButtonElement | null>>({}),
    recognition = useRef<Recognition | null>(null),
    audio = useRef<{ stream: MediaStream; context: AudioContext } | null>(null),
    frame = useRef(0),
    mounted = useRef(true),
    voice = useRef({ base: "", text: "", cancel: false }),
    draftCallback = useRef(onDraft);
  draftCallback.current = onDraft;
  const [selection, setSelection] = useState(0);
  const before = draft.slice(0, selection),
    mentionMatch = !suggestionDismissed
      ? before.match(/(?:^|\s)@([^@\n\s]{0,40})$/)
      : null,
    commandMatch = !suggestionDismissed
      ? before.match(/(?:^|\s)\/([a-z-]{0,30})$/i)
      : null,
    suggestionType = mentionMatch ? "mention" : commandMatch ? "command" : null,
    mentionCandidates = mentionMatch
      ? members.filter((a) =>
          a.name
            .toLowerCase()
            .replace(/\s/g, "")
            .startsWith(mentionMatch[1].toLowerCase().replace(/\s/g, "")),
        )
      : [],
    commandCandidates = commandMatch
      ? commands.filter((command) =>
          command.name.startsWith(commandMatch[1].toLowerCase()),
        )
      : [],
    candidates =
      suggestionType === "mention" ? mentionCandidates : commandCandidates;
  useLayoutEffect(() => {
    const el = input.current;
    if (!el) return;
    el.style.height = "auto";
    const max = Math.min(300, innerHeight * 0.32);
    el.style.height = Math.min(el.scrollHeight, max) + "px";
    el.style.overflowY = el.scrollHeight > max ? "auto" : "hidden";
  }, [draft, listening]);
  useLayoutEffect(() => {
    if (!candidates.length || !caretAnchor.current) return;
    const caret = caretAnchor.current.getBoundingClientRect(),
      composer = caretAnchor.current
        .closest(".composer")!
        .getBoundingClientRect(),
      popupWidth = Math.min(310, composer.width - 24),
      popupHeight = Math.min(310, candidates.length * 58 + 16),
      left = Math.max(
        12,
        Math.min(caret.left - composer.left, composer.width - popupWidth - 12),
      ),
      roomBelow = innerHeight - caret.bottom - 12,
      roomAbove = caret.top - 12,
      opensBelow = roomBelow >= popupHeight || roomBelow >= roomAbove,
      top = opensBelow
        ? caret.bottom - composer.top + 8
        : caret.top - composer.top - popupHeight + 12;
    setSuggestionPosition({ left, top });
  }, [draft, selection, candidates.length, suggestionType, viewportVersion]);
  useEffect(() => {
    const reposition = () => setViewportVersion((version) => version + 1);
    window.addEventListener("resize", reposition);
    return () => window.removeEventListener("resize", reposition);
  }, []);
  useEffect(() => {
    mounted.current = true;
    return () => {
      mounted.current = false;
      if (recognition.current) {
        draftCallback.current(
          voice.current.cancel
            ? voice.current.base
            : [voice.current.base, voice.current.text]
                .filter(Boolean)
                .join(" ")
                .trim(),
        );
        recognition.current.onend = null;
        recognition.current.onresult = null;
        recognition.current.abort();
      }
      cancelAnimationFrame(frame.current);
      audio.current?.stream.getTracks().forEach((t) => t.stop());
      void audio.current?.context.close();
    };
  }, []);
  useEffect(() => {
    if (!open) return;
    const away = (e: PointerEvent) => {
      if (!root.current?.contains(e.target as Node)) setOpen(null);
    };
    const key = (e: globalThis.KeyboardEvent) => {
      if (e.key === "Escape") {
        setOpen(null);
        triggers.current[open]?.focus();
      }
    };
    document.addEventListener("pointerdown", away);
    document.addEventListener("keydown", key);
    popup.current
      ?.querySelector<HTMLButtonElement>("button[aria-checked=true],button")
      ?.focus();
    return () => {
      document.removeEventListener("pointerdown", away);
      document.removeEventListener("keydown", key);
    };
  }, [open]);

  function toggle(type: typeof open) {
    setOpen((old) => (old === type ? null : type));
  }

  const safeIndex = candidates.length
    ? ((suggestionIndex % candidates.length) + candidates.length) % candidates.length
    : 0;

  useEffect(() => {
    if (!candidates.length) return;
    const activeBtn = suggestionListRef.current?.querySelector<HTMLButtonElement>(
      'button[aria-selected="true"]',
    );
    activeBtn?.scrollIntoView({ block: "nearest" });
  }, [safeIndex, candidates.length]);

  function chooseSuggestion(index: number) {
    if (!candidates.length || !suggestionType) return;
    const safeIdx =
      ((index % candidates.length) + candidates.length) % candidates.length;
    const item = candidates[safeIdx];
    if (!item) return;
    const trigger = suggestionType === "mention" ? "@" : "/",
      beforeText = draft.slice(0, selection),
      start = beforeText.lastIndexOf(trigger);
    if (start === -1) return;
    const token = trigger + item.name,
      text = draft.slice(0, start) + token + " " + draft.slice(selection),
      cursor = start + token.length + 1;
    onDraft(text);
    setSuggestionDismissed(true);
    setSuggestionIndex(0);
    requestAnimationFrame(() => {
      input.current?.focus();
      input.current?.setSelectionRange(cursor, cursor);
      setSelection(cursor);
    });
  }
  function onKey(e: KeyboardEvent<HTMLTextAreaElement>) {
    if (
      candidates.length > 0 &&
      ["ArrowDown", "ArrowUp", "Enter", "Tab", "Escape"].includes(e.key)
    ) {
      e.preventDefault();
      e.stopPropagation();
      if (e.key === "Escape") {
        setSuggestionDismissed(true);
      } else if (e.key === "Enter" || e.key === "Tab") {
        chooseSuggestion(safeIndex);
      } else if (e.key === "ArrowDown") {
        setSuggestionIndex(
          (prev) => (prev + 1) % candidates.length,
        );
      } else if (e.key === "ArrowUp") {
        setSuggestionIndex(
          (prev) => (prev - 1 + candidates.length) % candidates.length,
        );
      }
      return;
    }
    if (e.key === "Enter" && !e.shiftKey && !e.nativeEvent.isComposing) {
      e.preventDefault();
      send();
    }
  }
  function send() {
    if (listening) return;
    if (draft.trim()) {
      onSend(draft.trim());
      setSuggestionDismissed(true);
      setSelection(0);
    } else startVoice();
  }
  function insertTrigger(trigger: "@" | "/") {
    const el = input.current,
      cursor = el?.selectionStart ?? draft.length,
      prefix = cursor > 0 && !/\s/.test(draft[cursor - 1]) ? " " : "",
      text = draft.slice(0, cursor) + prefix + trigger + draft.slice(cursor),
      next = cursor + prefix.length + 1;
    onDraft(text);
    setSuggestionDismissed(false);
    setSuggestionIndex(0);
    requestAnimationFrame(() => {
      input.current?.focus();
      input.current?.setSelectionRange(next, next);
      setSelection(next);
    });
  }
  const MENTION_PALETTES = [
    { bg: "rgba(217, 119, 6, 0.15)", color: "#b45309", shadow: "rgba(217, 119, 6, 0.35)" }, // Amber
    { bg: "rgba(16, 185, 129, 0.15)", color: "#047857", shadow: "rgba(16, 185, 129, 0.35)" }, // Emerald
    { bg: "rgba(59, 130, 246, 0.15)", color: "#1d4ed8", shadow: "rgba(59, 130, 246, 0.35)" }, // Blue
    { bg: "rgba(147, 51, 234, 0.15)", color: "#7e22ce", shadow: "rgba(147, 51, 234, 0.35)" }, // Violet
    { bg: "rgba(244, 63, 94, 0.15)", color: "#be123c", shadow: "rgba(244, 63, 94, 0.35)" }, // Rose
    { bg: "rgba(20, 184, 166, 0.15)", color: "#0f766e", shadow: "rgba(20, 184, 166, 0.35)" }, // Teal
    { bg: "rgba(234, 88, 12, 0.15)", color: "#c2410c", shadow: "rgba(234, 88, 12, 0.35)" }, // Orange
    { bg: "rgba(99, 102, 241, 0.15)", color: "#4338ca", shadow: "rgba(99, 102, 241, 0.35)" }, // Indigo
    { bg: "rgba(236, 72, 153, 0.15)", color: "#be185d", shadow: "rgba(236, 72, 153, 0.35)" }, // Pink
  ];

  function getMentionStyle(nameOrToken: string) {
    let hash = 0;
    const clean = nameOrToken.replace(/^@/, "").toLowerCase();
    for (let i = 0; i < clean.length; i++) {
      hash = (hash * 31 + clean.charCodeAt(i)) >>> 0;
    }
    const p = MENTION_PALETTES[hash % MENTION_PALETTES.length];
    return {
      backgroundColor: p.bg,
      color: p.color,
      boxShadow: `inset 0 -1px ${p.shadow}`,
    };
  }

  function highlightedText(text: string) {
    if (!text) return text;
    // Sort names longest first so "Dr. Julian Mercer" is matched before shorter substrings
    const sortedMembers = [...members].sort((a, b) => b.name.length - a.name.length);
    const memberPatterns = sortedMembers.map((a) =>
      a.name.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"),
    );
    const commandPatterns = commands.map((c) =>
      c.name.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"),
    );

    const specificPatterns = [
      ...memberPatterns.map((n) => `@${n}`),
      ...commandPatterns.map((c) => `/${c}`),
    ];

    const patternStr = specificPatterns.length
      ? `(${specificPatterns.join("|")}|@[a-zA-Z0-9_.-]+)(?=\\s|$|[.,!?])`
      : `(@[a-zA-Z0-9_.-]+|/[a-zA-Z0-9_-]+)(?=\\s|$|[.,!?])`;

    const regex = new RegExp(patternStr, "gi");
    const parts = text.split(regex);

    return parts.map((part, index) => {
      if (!part) return null;
      if (part.startsWith("@")) {
        const style = getMentionStyle(part);
        return (
          <mark
            key={index}
            className="mention-token"
            style={style}
          >
            {part}
          </mark>
        );
      }
      if (part.startsWith("/")) {
        return (
          <mark
            key={index}
            className="command-token"
          >
            {part}
          </mark>
        );
      }
      return part;
    });
  }
  function cleanAudio() {
    cancelAnimationFrame(frame.current);
    audio.current?.stream.getTracks().forEach((t) => t.stop());
    void audio.current?.context.close();
    audio.current = null;
  }
  function finishVoice(cancel = false) {
    voice.current.cancel = cancel;
    recognition.current?.stop();
  }
  async function meter(session: Recognition) {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      if (!mounted.current || recognition.current !== session) {
        stream.getTracks().forEach((t) => t.stop());
        return;
      }
      const context = new AudioContext(),
        analyser = context.createAnalyser();
      analyser.fftSize = 128;
      context.createMediaStreamSource(stream).connect(analyser);
      audio.current = { stream, context };
      const values = new Uint8Array(analyser.frequencyBinCount);
      const tick = () => {
        if (!mounted.current || !audio.current) return;
        analyser.getByteFrequencyData(values);
        setBars(
          Array.from({ length: 35 }, (_, i) => Math.max(4, values[i] * 0.22)),
        );
        frame.current = requestAnimationFrame(tick);
      };
      tick();
    } catch {
      if (mounted.current)
        setNotice(
          "Microphone levels are unavailable; dictation may still work.",
        );
    }
  }
  function startVoice() {
    if (recognition.current) return;
    const Constructor =
      (window as SpeechWindow).SpeechRecognition ||
      (window as SpeechWindow).webkitSpeechRecognition;
    if (!Constructor) {
      setNotice(
        "Live dictation is unavailable in this browser. Use a browser with speech recognition support.",
      );
      return;
    }
    setOpen(null);
    voice.current = { base: draft, text: "", cancel: false };
    const rec = new Constructor();
    recognition.current = rec;
    rec.continuous = true;
    rec.interimResults = true;
    rec.lang = navigator.language || "en-US";
    rec.onstart = () => {
      if (!mounted.current) return;
      setListening(true);
      setTranscript("");
      setNotice("");
      void meter(rec);
    };
    rec.onresult = (e) => {
      const words = Array.from(e.results)
        .map((r) => r[0].transcript)
        .join(" ");
      voice.current.text = words;
      if (mounted.current) setTranscript(words);
    };
    rec.onerror = (e) => {
      if (mounted.current)
        setNotice(
          e.error === "not-allowed"
            ? "Microphone permission was denied."
            : "Dictation stopped. You can edit any captured text.",
        );
    };
    rec.onend = () => {
      recognition.current = null;
      cleanAudio();
      if (!mounted.current) return;
      const text = voice.current.cancel
        ? voice.current.base
        : [voice.current.base, voice.current.text]
            .filter(Boolean)
            .join(" ")
            .trim();
      draftCallback.current(text);
      setListening(false);
      setNotice(
        voice.current.cancel
          ? "Dictation canceled. Original draft restored."
          : "Dictation ready to edit. Nothing was sent.",
      );
      requestAnimationFrame(() => input.current?.focus());
    };
    try {
      rec.start();
    } catch {
      recognition.current = null;
      setNotice("Could not start dictation. Please try again.");
    }
  }
  const options = open === "permissions" ? permissions : models,
    selected = open === "permissions" ? settings.permission : settings.model;
  return (
    <div className="composerwrap" ref={root}>
      {notice && (
        <div className="prompt-notice" role="status">
          {notice}
          <IconButton
            icon="close"
            label="Dismiss message"
            onClick={() => setNotice("")}
          />
        </div>
      )}
      <form
        className={
          "composer " +
          (draft.trim() ? "has-text" : "") +
          (listening ? " listening" : "")
        }
        onSubmit={(e) => {
          e.preventDefault();
          send();
        }}
      >
        {open && (
          <div
            ref={popup}
            className={"prompt-popover " + open}
            role="dialog"
            aria-label={
              open === "attachments"
                ? "Add to your prompt"
                : open === "permissions"
                  ? "Permission level"
                  : "Choose a model"
            }
          >
            <div className="dialoghead">
              <strong>
                {open === "attachments"
                  ? "Add to your prompt"
                  : open === "permissions"
                    ? "Permission level"
                    : "Choose a model"}
              </strong>
              <IconButton
                icon="close"
                label="Close options"
                onClick={() => {
                  setOpen(null);
                  triggers.current[open]?.focus();
                }}
              />
            </div>
            <div className="controls-body">
              {open === "attachments" ? (
                <>
                  <p>Add reference files to your prompt.</p>
                  <button
                    className="option-card"
                    type="button"
                    onClick={() => picker.current?.click()}
                  >
                    <Icon name="file" />
                    <span>
                      <strong>Choose files</strong>
                      <small>Documents, images, or other reference files</small>
                    </span>
                  </button>
                  {files.map((file, i) => (
                    <div className="drawer-file" key={file.name + i}>
                      <span>
                        {file.name}
                        <small>{Math.ceil(file.size / 1024)} KB</small>
                      </span>
                      <IconButton
                        icon="close"
                        label={"Remove " + file.name}
                        onClick={() => onFiles(files.filter((_, j) => i !== j))}
                      />
                    </div>
                  ))}
                </>
              ) : (
                <>
                  <p>
                    {open === "permissions"
                      ? "Choose how your workforce should handle actions."
                      : "Choose a model profile for this conversation."}
                  </p>
                  <div
                    role="radiogroup"
                    aria-label={
                      open === "permissions"
                        ? "Permission level"
                        : "Model profiles"
                    }
                  >
                    {options.map((o) => (
                      <button
                        type="button"
                        key={o.id}
                        className="option-card"
                        role="radio"
                        aria-checked={selected === o.id}
                        onKeyDown={(e) => {
                          if (["ArrowUp", "ArrowDown"].includes(e.key)) {
                            e.preventDefault();
                            const buttons =
                              e.currentTarget.parentElement!.querySelectorAll<HTMLButtonElement>(
                                "button",
                              );
                            buttons[
                              (options.indexOf(o) +
                                (e.key === "ArrowDown"
                                  ? 1
                                  : options.length - 1)) %
                                options.length
                            ].focus();
                          }
                        }}
                        onClick={() => {
                          onSettings({
                            ...settings,
                            [open === "permissions" ? "permission" : "model"]:
                              o.id,
                          });
                          setOpen(null);
                          triggers.current[open]?.focus();
                        }}
                      >
                        <Icon
                          name={open === "permissions" ? "shield" : "model"}
                        />
                        <span>
                          <strong>{o.name}</strong>
                          <small>{o.description}</small>
                        </span>
                        {selected === o.id && <Icon name="check" />}
                      </button>
                    ))}
                  </div>
                </>
              )}
            </div>
          </div>
        )}
        {candidates.length > 0 && !listening && (
          <div
            ref={suggestionListRef}
            className="suggestion-list"
            style={suggestionPosition}
            role="listbox"
            aria-label={
              suggestionType === "mention"
                ? "Mention a teammate"
                : "Choose a command"
            }
          >
            {candidates.map((item, i) => (
              <button
                key={item.id}
                type="button"
                role="option"
                aria-selected={i === safeIndex}
                onMouseDown={(event) => event.preventDefault()}
                onClick={() => chooseSuggestion(i)}
              >
                {suggestionType === "mention" ? (
                  <>
                    <span
                      className="suggestion-avatar"
                      style={{ background: (item as Agent).color }}
                    >
                      {(item as Agent).initials}
                    </span>
                    <span>
                      <strong>{item.name}</strong>
                      <small>{(item as Agent).role}</small>
                    </span>
                  </>
                ) : (
                  <>
                    <span className="suggestion-icon">
                      <Icon name={(item as (typeof commands)[number]).icon} />
                    </span>
                    <span>
                      <strong>/{item.name}</strong>
                      <small>
                        {(item as (typeof commands)[number]).description}
                      </small>
                    </span>
                  </>
                )}
                <kbd>↵</kbd>
              </button>
            ))}
          </div>
        )}
        {files.length > 0 && (
          <div className="attachment-chips">
            {files.map((f, i) => (
              <span key={f.name + i} className="attachment-chip">
                <Icon name="file" />
                <span>{f.name}</span>
                <IconButton
                  icon="close"
                  label={"Remove " + f.name}
                  onClick={() => onFiles(files.filter((_, j) => i !== j))}
                />
              </span>
            ))}
          </div>
        )}
        {listening ? (
          <div className="voice-panel">
            <div className="voice-transcript" aria-live="polite">
              {transcript || "Listening…"}
            </div>
            <div className="waveform" aria-hidden="true">
              {bars.map((height, i) => (
                <i
                  key={i}
                  style={{ height, animation: "none" } as CSSProperties}
                />
              ))}
            </div>
            <div className="voice-footer">
              <span>Listening · finish to edit before sending</span>
              <div>
                <IconButton
                  icon="close"
                  label="Cancel dictation"
                  onClick={() => finishVoice(true)}
                />
                <IconButton
                  icon="check"
                  label="Finish dictation and edit"
                  onClick={() => finishVoice()}
                />
              </div>
            </div>
          </div>
        ) : (
          <div className="prompt-editor">
            <div ref={mirror} className="prompt-highlight" aria-hidden="true">
              {highlightedText(draft.slice(0, selection))}
              <span ref={caretAnchor} className="caret-anchor">
                &#8203;
              </span>
              {highlightedText(draft.slice(selection))}
              {draft.endsWith("\n") ? "\n " : ""}
            </div>
            <textarea
              ref={input}
              rows={1}
              aria-label="Message assistant"
              placeholder={"Work with " + name + "…"}
              value={draft}
              onScroll={(e) => {
                if (mirror.current)
                  mirror.current.scrollTop = e.currentTarget.scrollTop;
              }}
              onChange={(e) => {
                onDraft(e.target.value);
                setSelection(e.target.selectionStart);
                setSuggestionDismissed(false);
                setSuggestionIndex(0);
              }}
              onSelect={(e) => setSelection(e.currentTarget.selectionStart)}
              onClick={(e) => setSelection(e.currentTarget.selectionStart)}
              onKeyUp={(e) => {
                if (!["ArrowDown", "ArrowUp", "Enter", "Tab", "Escape"].includes(e.key)) {
                  setSelection(e.currentTarget.selectionStart);
                }
              }}
              onKeyDown={onKey}
            />
          </div>
        )}
        {!listening && (
          <div className="prompt-toolbar">
            <div className="prompt-left">
              <button
                ref={(el) => {
                  triggers.current.attachments = el;
                }}
                type="button"
                className="prompt-icon"
                aria-label="Attach files"
                aria-haspopup="dialog"
                aria-expanded={open === "attachments"}
                onClick={() => toggle("attachments")}
              >
                <Icon name="plus" />
              </button>
              <button
                type="button"
                className="syntax-control"
                aria-label="Mention a teammate"
                onClick={() => insertTrigger("@")}
              >
                @ <span>mention</span>
              </button>
              <button
                type="button"
                className="syntax-control"
                aria-label="Insert a command"
                onClick={() => insertTrigger("/")}
              >
                / <span>commands</span>
              </button>
              <button
                ref={(el) => {
                  triggers.current.permissions = el;
                }}
                type="button"
                className="approval-control"
                aria-haspopup="dialog"
                aria-expanded={open === "permissions"}
                onClick={() => toggle("permissions")}
              >
                <Icon name="shield" />
                <span>
                  {settings.permission === "ask"
                    ? "Ask every time"
                    : permissions.find((p) => p.id === settings.permission)
                        ?.name}
                </span>
              </button>
            </div>
            <div className="prompt-right">
              <button
                ref={(el) => {
                  triggers.current.models = el;
                }}
                className="model-control"
                type="button"
                aria-label="Choose model"
                aria-haspopup="dialog"
                aria-expanded={open === "models"}
                onClick={() => toggle("models")}
              >
                <span>{models.find((m) => m.id === settings.model)?.name}</span>
                <Icon name="chevron" />
              </button>
              <button
                type="button"
                className="prompt-icon"
                aria-label="Dictate prompt"
                onClick={startVoice}
              >
                <Icon name="mic" />
              </button>
              <button
                type="submit"
                className="voice-send"
                aria-label={draft.trim() ? "Send message" : "Start voice mode"}
              >
                <Icon name={draft.trim() ? "send" : "wave"} />
              </button>
            </div>
          </div>
        )}
      </form>
      <input
        ref={picker}
        type="file"
        multiple
        hidden
        onChange={(e) => {
          onFiles([...files, ...Array.from(e.target.files || [])]);
          e.target.value = "";
        }}
      />
    </div>
  );
}
