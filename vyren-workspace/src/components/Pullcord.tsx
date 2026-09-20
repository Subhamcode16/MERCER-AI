import { useEffect, useRef } from "react";
export function Pullcord({
  night,
  onToggle,
}: {
  night: boolean;
  onToggle: () => void;
}) {
  const path = useRef<SVGPathElement>(null),
    button = useRef<HTMLButtonElement>(null),
    toggle = useRef(onToggle);
  toggle.current = onToggle;
  const drag = useRef<{
    id: number;
    startX: number;
    startY: number;
    x: number;
    y: number;
    moved: boolean;
    fired: boolean;
  } | null>(null);
  const suppress = useRef(false),
    wake = useRef(() => {});
  const nodes = useRef(
    Array.from({ length: 13 }, (_, i) => ({
      x: 50,
      y: (i * 112) / 12,
      px: 50,
      py: (i * 112) / 12,
    })),
  );
  const reduced = useRef(false);
  useEffect(() => {
    const media = matchMedia("(prefers-reduced-motion: reduce)");
    reduced.current = media.matches;
    let frame = 0,
      last = 0,
      quiet = 0;
    const n = nodes.current;
    const draw = () => {
      path.current?.setAttribute(
        "d",
        n
          .map(
            (p, i) => (i ? "L" : "M") + p.x.toFixed(2) + " " + p.y.toFixed(2),
          )
          .join(" "),
      );
      if (button.current) {
        button.current.style.left = n[12].x + "px";
        button.current.style.top = n[12].y + "px";
      }
    };
    const tick = (now: number) => {
      frame = 0;
      const dt = Math.min((now - last) / 1000, 0.025);
      last = now;
      const before = n.map((p) => ({ x: p.x, y: p.y }));
      for (let i = 1; i < 13; i++) {
        const p = n[i],
          vx = (p.x - p.px) * 0.94,
          vy = (p.y - p.py) * 0.94;
        p.px = p.x;
        p.py = p.y;
        p.x += vx;
        p.y += vy + 1250 * dt * dt;
      }
      const step = (112 + (drag.current ? drag.current.y - 112 : 0)) / 12;
      for (let loop = 0; loop < 22; loop++) {
        n[0].x = 50;
        n[0].y = 0;
        if (drag.current) {
          n[12].x = drag.current.x;
          n[12].y = drag.current.y;
        }
        for (let i = 0; i < 12; i++) {
          const a = n[i],
            b = n[i + 1],
            dx = b.x - a.x,
            dy = b.y - a.y,
            len = Math.hypot(dx, dy) || 1,
            diff = (len - step) / len,
            af = i === 0,
            bf = !!drag.current && i === 11,
            w = af || bf ? 1 : 0.5;
          if (!af) {
            a.x += dx * diff * w;
            a.y += dy * diff * w;
          }
          if (!bf) {
            b.x -= dx * diff * w;
            b.y -= dy * diff * w;
          }
        }
      }
      draw();
      quiet =
        n.some(
          (p, i) => Math.hypot(p.x - before[i].x, p.y - before[i].y) > 0.04,
        ) || drag.current
          ? 0
          : quiet + 1;
      if (quiet < 25) frame = requestAnimationFrame(tick);
    };
    wake.current = () => {
      quiet = 0;
      if (reduced.current) {
        if (drag.current) {
          n[12].x = drag.current.x;
          n[12].y = drag.current.y;
        } else
          n.forEach((p, i) => {
            p.x = p.px = 50;
            p.y = p.py = (i * 112) / 12;
          });
        draw();
        return;
      }
      if (!frame) {
        last = performance.now();
        frame = requestAnimationFrame(tick);
      }
    };
    const change = () => {
      reduced.current = media.matches;
      if (media.matches) {
        cancelAnimationFrame(frame);
        frame = 0;
      }
      wake.current();
    };
    const visible = () => {
      if (document.hidden) {
        cancelAnimationFrame(frame);
        frame = 0;
      } else wake.current();
    };
    media.addEventListener("change", change);
    document.addEventListener("visibilitychange", visible);
    draw();
    wake.current();
    return () => {
      cancelAnimationFrame(frame);
      media.removeEventListener("change", change);
      document.removeEventListener("visibilitychange", visible);
    };
  }, []);
  function release(id: number) {
    if (drag.current?.id !== id) return;
    suppress.current = drag.current.moved || drag.current.fired;
    drag.current = null;
    wake.current();
  }
  return (
    <div className={"theme-pullcord " + (night ? "is-night" : "")}>
      <svg className="cord-line" viewBox="0 0 100 200" aria-hidden="true">
        <path ref={path} className="cord-rope" />
      </svg>
      <span className="cord-anchor" />
      <button
        ref={button}
        type="button"
        className="cord-knob"
        role="switch"
        aria-checked={night}
        aria-label={"Switch to " + (night ? "light" : "dark") + " theme"}
        title="Pull down to switch theme"
        onPointerDown={(e) => {
          if (e.button !== 0) return;
          suppress.current = false;
          drag.current = {
            id: e.pointerId,
            startX: e.clientX,
            startY: e.clientY,
            x: nodes.current[12].x,
            y: nodes.current[12].y,
            moved: false,
            fired: false,
          };
          e.currentTarget.setPointerCapture(e.pointerId);
          wake.current();
        }}
        onPointerMove={(e) => {
          const d = drag.current;
          if (!d || d.id !== e.pointerId) return;
          const dy = Math.max(0, e.clientY - d.startY),
            dx = e.clientX - d.startX;
          d.moved ||= Math.hypot(dx, dy) > 5;
          d.x = 50 + Math.max(-33, Math.min(33, dx));
          d.y = 112 + Math.min(34, dy);
          if (dy >= 22 && !d.fired) {
            d.fired = true;
            toggle.current();
          }
          wake.current();
        }}
        onPointerUp={(e) => release(e.pointerId)}
        onPointerCancel={(e) => release(e.pointerId)}
        onLostPointerCapture={(e) => release(e.pointerId)}
        onClick={(e) => {
          if (suppress.current && e.detail !== 0) {
            suppress.current = false;
            return;
          }
          toggle.current();
          if (!reduced.current) {
            nodes.current[12].py -= 16;
            wake.current();
          }
        }}
      >
        <span className="cord-bead" />
      </button>
      <span className="cord-hint" aria-hidden="true">
        Pull to switch
      </span>
    </div>
  );
}
