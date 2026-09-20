import { useState } from "react";
import "./ToolCalls.css";

export type ToolType = "gmail" | "calendar" | "executor" | "handoff" | "search" | "custom";

export interface ToolCallItem {
  id: string;
  tool: ToolType;
  title: string;
  provider: string;
  status?: "success" | "running" | "error";
  details?: {
    input?: Record<string, unknown> | string;
    output?: Record<string, unknown> | string;
  };
}

export const defaultToolCalls: ToolCallItem[] = [
  {
    id: "tool-1",
    tool: "gmail",
    title: "Sent email to the team",
    provider: "Gmail",
    status: "success",
    details: {
      input: { to: "team@company.com", subject: "Landscape brief summary & review" },
      output: { status: "sent", messageId: "msg_9841249" },
    },
  },
  {
    id: "tool-2",
    tool: "calendar",
    title: "Created meeting for tomorrow at 2 PM",
    provider: "Google Calendar",
    status: "success",
    details: {
      input: { title: "Workforce Sync", time: "Tomorrow 14:00 - 14:30", attendees: 4 },
      output: { eventId: "cal_391051", link: "https://meet.google.com/xyz-demo" },
    },
  },
  {
    id: "tool-3",
    tool: "executor",
    title: "Executed code analysis task",
    provider: "Executor",
    status: "success",
    details: {
      input: { language: "typescript", command: "analyzeSources()" },
      output: { filesScanned: 24, coverage: "98%", status: "0 errors" },
    },
  },
  {
    id: "tool-4",
    tool: "handoff",
    title: "Delegated to scheduling assistant",
    provider: "Handoff",
    status: "success",
    details: {
      input: { targetAgent: "Operations Assistant", priority: "high" },
      output: { handoffState: "accepted", sessionId: "hand_4812" },
    },
  },
];

/* Real-World Official Vector App Icons */
export function ToolIcon({ tool, size = 28 }: { tool: ToolType; size?: number }) {
  switch (tool) {
    case "gmail":
      return (
        <svg
          width={size}
          height={size}
          viewBox="0 0 48 48"
          fill="none"
          aria-label="Gmail"
          style={{ width: "100%", height: "100%", padding: "2px", boxSizing: "border-box" }}
        >
          <path
            fill="#4285F4"
            d="M4.5 16.2l3.6 2.1L13 23.7V40H7.5c-1.66 0-3-1.34-3-3V16.2z"
          />
          <path
            fill="#34A853"
            d="M43.5 16.2l-5 2.8-4.5 4.7V40h5.5c1.66 0 3-1.34 3-3V16.2z"
          />
          <polygon
            fill="#EA4335"
            points="35,11.2 24,19.5 13,11.2 12,17 13,23.7 24,32 35,23.7 36,17"
          />
          <path
            fill="#C5221F"
            d="M4.5 12.3v3.9l8.5 7.5V11.2l-3.1-2.3c-1.74-1.31-4.22-.82-5.4 1.1z"
          />
          <path
            fill="#FBBC04"
            d="M43.5 12.3v3.9l-9.5 7.5V11.2l3.1-2.3c1.74-1.31 4.22-.82 5.4 1.1z"
          />
        </svg>
      );
    case "calendar":
      return (
        <svg
          width={size}
          height={size}
          viewBox="0 0 48 48"
          fill="none"
          aria-label="Google Calendar"
          style={{ width: "100%", height: "100%" }}
        >
          <rect x="3" y="3" width="42" height="42" rx="9" fill="#1A73E8" />
          <rect x="8.5" y="8.5" width="31" height="31" rx="4" fill="#FFFFFF" />
          <path
            d="M8.5 12.5C8.5 10.3 10.3 8.5 12.5 8.5H35.5C37.7 8.5 39.5 10.3 39.5 12.5V16.5H8.5V12.5Z"
            fill="#EA4335"
          />
          <path
            d="M8.5 31.5H39.5V35.5C39.5 37.7 37.7 39.5 35.5 39.5H12.5C10.3 39.5 8.5 37.7 8.5 35.5V31.5Z"
            fill="#34A853"
          />
          <path d="M36 16.5H39.5V31.5H36V16.5Z" fill="#FBBC04" />
          <text
            x="24"
            y="29.5"
            fill="#1565C0"
            fontSize="14.5"
            fontFamily="system-ui, -apple-system, sans-serif"
            fontWeight="800"
            textAnchor="middle"
          >
            31
          </text>
        </svg>
      );
    case "executor":
      return (
        <svg
          width={size}
          height={size}
          viewBox="0 0 32 32"
          fill="none"
          aria-label="Executor"
          style={{ width: "100%", height: "100%" }}
        >
          <rect width="32" height="32" rx="7" fill="#E6F4EA" />
          <rect
            x="5.5"
            y="6.5"
            width="21"
            height="14"
            rx="3.5"
            stroke="#0F9D58"
            strokeWidth="1.8"
            fill="#E6F4EA"
          />
          <path
            d="M16 20.5V24.5M11.5 24.5H20.5"
            stroke="#0F9D58"
            strokeWidth="1.8"
            strokeLinecap="round"
          />
          <path
            d="M11 10.5L8.5 13L11 15.5M21 10.5L23.5 13L21 15.5M16.5 9.5L15 16.5"
            stroke="#0F9D58"
            strokeWidth="1.6"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      );
    case "handoff":
      return (
        <svg
          width={size}
          height={size}
          viewBox="0 0 32 32"
          fill="none"
          aria-label="Handoff"
          style={{ width: "100%", height: "100%" }}
        >
          <rect width="32" height="32" rx="7" fill="#E0F2FE" />
          <rect
            x="6.5"
            y="6.5"
            width="19"
            height="19"
            rx="4.5"
            stroke="#0284C7"
            strokeWidth="1.8"
            fill="#E0F2FE"
          />
          <path
            d="M11 21L21 11M21 11H14.5M21 11V17.5"
            stroke="#0284C7"
            strokeWidth="2.2"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      );
    default:
      return (
        <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
          <circle cx="12" cy="12" r="9" />
          <path d="M12 8v8M8 12h8" />
        </svg>
      );
  }
}

export interface ToolCallsProps {
  tools?: ToolCallItem[];
  defaultExpanded?: boolean;
  className?: string;
  onToggle?: (expanded: boolean) => void;
}

export function ToolCalls({
  tools = defaultToolCalls,
  defaultExpanded = false,
  className = "",
  onToggle,
}: ToolCallsProps) {
  const [expanded, setExpanded] = useState(defaultExpanded);
  const [expandedItems, setExpandedItems] = useState<Record<string, boolean>>({});

  const toggleExpanded = () => {
    const next = !expanded;
    setExpanded(next);
    onToggle?.(next);
  };

  const toggleItem = (id: string) => {
    setExpandedItems((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  if (!tools || tools.length === 0) return null;

  return (
    <div className={`tool-calls-container ${className}`}>
      {/* Header Trigger Button */}
      <button
        type="button"
        className="tool-calls-trigger"
        aria-expanded={expanded}
        aria-controls="tool-calls-timeline"
        onClick={toggleExpanded}
      >
        {/* Overlapping Badge Cluster */}
        <span className="tool-icons-stack" aria-hidden="true">
          {tools.slice(0, 5).map((t) => (
            <span key={t.id} className="tool-badge-item">
              <ToolIcon tool={t.tool} size={26} />
            </span>
          ))}
        </span>

        {/* Text Label */}
        <span className="tool-calls-label">Used {tools.length} tools</span>

        {/* Chevron */}
        <span className={`tool-calls-chevron ${expanded ? "is-open" : ""}`} aria-hidden="true">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
            <path d="m6 9 6 6 6-6" />
          </svg>
        </span>
      </button>

      {/* Expanded Timeline Tree */}
      {expanded && (
        <div id="tool-calls-timeline" className="tool-calls-body">
          <div className="tool-timeline-list" role="list">
            {tools.map((t) => {
              const isItemExpanded = Boolean(expandedItems[t.id]);

              return (
                <div key={t.id} className="tool-step-item" role="listitem">
                  <button
                    type="button"
                    className="tool-step-header"
                    onClick={() => toggleItem(t.id)}
                    aria-expanded={isItemExpanded}
                  >
                    {/* Tool App Icon */}
                    <div className="tool-step-icon-wrap" aria-hidden="true">
                      <ToolIcon tool={t.tool} size={34} />
                    </div>

                    {/* Step Description & Provider */}
                    <div className="tool-step-content">
                      <div className="tool-step-title-row">
                        <span className="tool-step-title">{t.title}</span>
                        <span className={`tool-step-chevron ${isItemExpanded ? "is-open" : ""}`} aria-hidden="true">
                          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <path d="m6 9 6 6 6-6" />
                          </svg>
                        </span>
                      </div>
                      <span className="tool-step-provider">{t.provider}</span>
                    </div>
                  </button>

                  {/* Optional Item Payload / Output Inspection */}
                  {isItemExpanded && t.details && (
                    <div className="tool-step-details">
                      {t.details.input && (
                        <div className="tool-step-details-row">
                          <span className="tool-step-details-label">Input</span>
                          <pre className="tool-step-details-code">
                            {typeof t.details.input === "string"
                              ? t.details.input
                              : JSON.stringify(t.details.input, null, 2)}
                          </pre>
                        </div>
                      )}
                      {t.details.output && (
                        <div className="tool-step-details-row" style={{ marginTop: "6px" }}>
                          <span className="tool-step-details-label">Output</span>
                          <pre className="tool-step-details-code">
                            {typeof t.details.output === "string"
                              ? t.details.output
                              : JSON.stringify(t.details.output, null, 2)}
                          </pre>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
