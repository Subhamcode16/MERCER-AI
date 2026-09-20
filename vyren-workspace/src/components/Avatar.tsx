import { useEffect, useRef, useState } from "react";
import type { CSSProperties } from "react";
import type { Agent, AgentState } from "../types";
export const shapes = [
  "M32 7C40 2 48 9 49 16C60 18 63 31 57 39C60 51 48 59 39 56C29 64 17 58 15 51C3 49 1 36 8 28C4 17 17 8 24 11C26 8 29 7 32 7Z",
  "M32 5C38 5 40 14 45 16C51 18 59 16 61 23C63 30 54 34 53 40C52 46 56 54 50 58C44 62 38 55 32 55C26 55 20 62 14 58C8 54 12 46 11 40C10 34 1 30 3 23C5 16 13 18 19 16C24 14 26 5 32 5Z",
  "M25 8Q32 3 39 8L57 19Q63 23 61 31L55 50Q53 58 45 59H19Q11 58 9 50L3 31Q1 23 7 19Z",
  "M24 9Q32 1 40 9L59 42Q66 56 51 58H13Q-2 56 5 42Z",
  "M20 6H44Q59 6 59 21V43Q59 58 44 58H20Q5 58 5 43V21Q5 6 20 6Z",
];
const visualState = (state: AgentState) =>
  ["action_needed", "human_control", "review_ready"].includes(state)
    ? "attention"
    : state;
function Eyes() {
  return (
    <g className="mascot-eyes">
      <rect x="22" y="23" width="7" height="17" rx="3.5" />
      <rect x="36" y="23" width="7" height="17" rx="3.5" />
    </g>
  );
}
export function Avatar({
  agent,
  state = "idle",
  members,
  className = "",
}: {
  agent?: Agent;
  state?: AgentState;
  members?: Agent[];
  className?: string;
}) {
  const people = members?.slice(0, 3),
    positions =
      people?.length === 2
        ? [
            [5, 20],
            [34, 20],
          ]
        : [
            [18, 1],
            [1, 32],
            [35, 32],
          ];
  const points = people?.map((_, i) => [
    positions[i][0] + 14,
    positions[i][1] + 14,
  ]);
  const connections =
    points
      ?.map((p, i) => (i ? `M${points[i - 1].join(" ")}L${p.join(" ")}` : ""))
      .join(" ") +
    (points?.length === 3
      ? `M${points[2].join(" ")}L${points[0].join(" ")}`
      : "");
  return (
    <span
      aria-hidden="true"
      data-state={visualState(state)}
      data-mascot
      data-trail-color={agent?.color || people?.[0]?.color || "#526b83"}
      className={`avatar ${people ? "group-constellation" : "agent-mascot"} ${className}`}
      style={{ "--avatar": agent?.color } as CSSProperties}
    >
      <svg viewBox="0 0 64 64">
        {people ? (
          <>
            <path className="constellation-links" d={connections} />
            <path className="constellation-pulse" d={connections} />
            {people.map((a, i) => (
              <g
                key={a.id}
                transform={`translate(${positions[i].join(" ")}) scale(.44)`}
              >
                <g
                  className="constellation-member"
                  style={
                    {
                      "--member-delay": i * -0.8 + "s",
                      "--gather-x": (32 - points![i][0]) * 0.2 + "px",
                      "--gather-y": (32 - points![i][1]) * 0.2 + "px",
                    } as CSSProperties
                  }
                >
                  <path d={shapes[a.shape % 5]} fill={a.color} />
                  <Eyes />
                </g>
              </g>
            ))}
          </>
        ) : (
          <>
            <g className="mascot-orbit">
              <ellipse
                cx="32"
                cy="32"
                rx="35"
                ry="15"
                transform="rotate(-30 32 32)"
              />
              <circle cx="62" cy="19" r="3" fill="currentColor" />
            </g>
            <path className="mascot-body" d={shapes[(agent?.shape || 0) % 5]} />
            <Eyes />
          </>
        )}
        <circle className="mascot-badge" cx="55" cy="8" r="6" />
      </svg>
    </span>
  );
}
interface Particle {
  id: number;
  x: number;
  y: number;
  color: string;
  dx: number;
  dy: number;
}
export function MouseTrails() {
  const [particles, setParticles] = useState<Particle[]>([]);
  const seq = useRef(0);
  useEffect(() => {
    const reduced = matchMedia("(prefers-reduced-motion: reduce)");
    let last = 0,
      previous: { x: number; y: number } | null = null;
    const timers = new Set<ReturnType<typeof setTimeout>>();
    const move = (e: PointerEvent) => {
      if (
        e.pointerType !== "mouse" ||
        reduced.matches ||
        document.hidden ||
        performance.now() - last < 25
      )
        return;
      const el = Array.from(
        document.querySelectorAll<HTMLElement>("[data-mascot]"),
      ).find((el) => {
        const r = el.getBoundingClientRect();
        return (
          r.width &&
          r.height &&
          e.clientX >= r.left - 18 &&
          e.clientX <= r.right + 18 &&
          e.clientY >= r.top - 18 &&
          e.clientY <= r.bottom + 18
        );
      });
      if (!el) {
        previous = null;
        return;
      }
      last = performance.now();
      const id = seq.current++;
      const p = {
        id,
        x: e.clientX,
        y: e.clientY,
        color: el.dataset.trailColor!,
        dx: previous ? Math.max(-12, Math.min(12, previous.x - e.clientX)) : 0,
        dy: previous ? Math.max(-12, Math.min(12, previous.y - e.clientY)) : 5,
      };
      previous = { x: e.clientX, y: e.clientY };
      setParticles((ps) => [...ps.slice(-23), p]);
      const timer = setTimeout(() => {
        timers.delete(timer);
        setParticles((ps) => ps.filter((p) => p.id !== id));
      }, 600);
      timers.add(timer);
    };
    const change = () => {
      if (reduced.matches) setParticles([]);
    };
    document.addEventListener("pointermove", move, { passive: true });
    reduced.addEventListener("change", change);
    return () => {
      document.removeEventListener("pointermove", move);
      reduced.removeEventListener("change", change);
      timers.forEach(clearTimeout);
    };
  }, []);
  return (
    <div aria-hidden="true" className="trail-layer">
      {particles.map((p) => (
        <i
          key={p.id}
          className="mascot-trail"
          style={
            {
              left: p.x,
              top: p.y,
              "--trail-color": p.color,
              "--drift-x": p.dx + "px",
              "--drift-y": p.dy + "px",
            } as CSSProperties
          }
        />
      ))}
    </div>
  );
}
