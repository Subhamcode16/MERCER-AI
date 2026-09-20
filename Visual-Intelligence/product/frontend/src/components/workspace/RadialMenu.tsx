import { useEffect, useRef, useState } from "react";
import type { CSSProperties, PointerEvent as ReactPointerEvent } from "react";
import { Icon } from "./Icon";
import { Modal } from "./Modal";
import {
  loadLiquidGlass,
  type LiquidGlassInstance,
} from "./liquidGlassRuntime";

const items = [
  ["appearance", "Appearance", "palette"],
  ["workforce", "New agent", "plus"],
  ["groups", "Groups", "group"],
  ["projects", "New project", "file"],
  ["workspace", "Workspace", "shield"],
  ["shortcuts", "Shortcuts", "model"],
] as const;
type Point = { x: number; y: number };
type MenuId = (typeof items)[number][0];
type MenuPreferences = {
  size: number;
  opacity: number;
  enabled: MenuId[];
};
const defaultPreferences: MenuPreferences = {
  size: 52,
  opacity: 86,
  enabled: items.map(([id]) => id),
};
const radius = 104;
function clamp(point: Point): Point {
  const margin = radius + 28;
  return {
    x: Math.max(margin, Math.min(innerWidth - margin, point.x)),
    y: Math.max(margin, Math.min(innerHeight - margin, point.y)),
  };
}
export function RadialMenu({ onAction }: { onAction: (id: string) => void }) {
  const [open, setOpen] = useState(false),
    [settingsOpen, setSettingsOpen] = useState(false),
    [position, setPosition] = useState<Point>({ x: 0, y: 0 }),
    [ready, setReady] = useState(false),
    [preferences, setPreferences] = useState<MenuPreferences>(() => {
      try {
        const saved = JSON.parse(
          localStorage.getItem("fieldwork-quick-menu-settings") || "null",
        ) as Partial<MenuPreferences> | null;
        return saved
          ? {
              size: Math.min(72, Math.max(42, Number(saved.size) || 52)),
              opacity: Math.min(100, Math.max(35, Number(saved.opacity) || 86)),
              enabled: items
                .map(([id]) => id)
                .filter((id) => saved.enabled?.includes(id)),
            }
          : defaultPreferences;
      } catch {
        return defaultPreferences;
      }
    });
  const drag = useRef<{
      id: number;
      dx: number;
      dy: number;
      moved: boolean;
    } | null>(null),
    glassHost = useRef<HTMLDivElement>(null),
    glassInstance = useRef<LiquidGlassInstance | null>(null);
  useEffect(() => {
    let next: Point | null = null;
    const saved = localStorage.getItem("fieldwork-quick-menu-position");
    if (saved)
      try {
        next = JSON.parse(saved) as Point;
      } catch {
        /* use a fresh position */
      }
    next = clamp(
      next || {
        x: innerWidth * (0.62 + Math.random() * 0.18),
        y: innerHeight * (0.24 + Math.random() * 0.24),
      },
    );
    setPosition(next);
    setReady(true);
    const resize = () => setPosition((point) => clamp(point));
    addEventListener("resize", resize);
    return () => removeEventListener("resize", resize);
  }, []);
  useEffect(() => {
    localStorage.setItem(
      "fieldwork-quick-menu-settings",
      JSON.stringify(preferences),
    );
  }, [preferences]);
  useEffect(() => {
    let disposed = false;
    void loadLiquidGlass().then((Container) => {
      if (disposed || !Container || !glassHost.current) return;
      const instance = new Container({
        type: "circle",
        tintOpacity: 0.08 + (preferences.opacity / 100) * 0.3,
      });
      instance.element.classList.add("radial-liquid-surface");
      instance.element.style.width = "100%";
      instance.element.style.height = "100%";
      instance.element.style.padding = "0";
      instance.element.style.pointerEvents = "none";
      glassHost.current.appendChild(instance.element);
      glassInstance.current = instance;
      requestAnimationFrame(() => instance.updateSizeFromDOM());
    });
    return () => {
      disposed = true;
      glassInstance.current?.destroy();
      glassInstance.current = null;
    };
  }, []);
  useEffect(() => {
    const instance = glassInstance.current,
      gl = instance?.gl_refs.gl,
      tint = instance?.gl_refs.tintOpacityLoc;
    if (instance) {
      instance.tintOpacity = 0.08 + (preferences.opacity / 100) * 0.3;
      instance.updateSizeFromDOM();
      if (gl && tint) gl.uniform1f(tint, instance.tintOpacity);
      instance.render?.();
    }
  }, [preferences.size, preferences.opacity, position]);
  function down(e: ReactPointerEvent<HTMLButtonElement>) {
    e.currentTarget.setPointerCapture(e.pointerId);
    drag.current = {
      id: e.pointerId,
      dx: e.clientX - position.x,
      dy: e.clientY - position.y,
      moved: false,
    };
  }
  function move(e: ReactPointerEvent<HTMLButtonElement>) {
    if (!drag.current || drag.current.id !== e.pointerId) return;
    const next = clamp({
      x: e.clientX - drag.current.dx,
      y: e.clientY - drag.current.dy,
    });
    if (Math.hypot(next.x - position.x, next.y - position.y) > 3)
      drag.current.moved = true;
    setPosition(next);
  }
  function up(e: ReactPointerEvent<HTMLButtonElement>) {
    if (!drag.current) return;
    const moved = drag.current.moved;
    drag.current = null;
    localStorage.setItem(
      "fieldwork-quick-menu-position",
      JSON.stringify(position),
    );
    if (!moved) setOpen((value) => !value);
    e.currentTarget.releasePointerCapture(e.pointerId);
  }
  if (!ready) return null;
  const visibleItems = items.filter(([id]) => preferences.enabled.includes(id)),
    menuItems = [
      ...visibleItems,
      ["menu-settings", "Menu settings", "settings"] as const,
    ];
  return (
    <>
      <nav
        className={"radial-menu " + (open ? "open" : "")}
        style={
          {
            left: position.x,
            top: position.y,
            "--radial-size": `${preferences.size}px`,
            "--radial-opacity": preferences.opacity / 100,
          } as CSSProperties
        }
        aria-label="Quick access"
      >
        <div ref={glassHost} className="liquid-glass-host" aria-hidden="true" />
        {menuItems.map(([id, label, icon], index) => {
          const angle =
            ((-90 + index * (360 / menuItems.length)) * Math.PI) / 180;
          return (
            <button
              key={id}
              type="button"
              className="radial-action"
              style={
                {
                  "--radial-x": `${Math.cos(angle) * radius}px`,
                  "--radial-y": `${Math.sin(angle) * radius}px`,
                  "--radial-delay": `${index * 28}ms`,
                } as CSSProperties
              }
              aria-label={label}
              tabIndex={open ? 0 : -1}
              onClick={() => {
                if (id === "menu-settings") setSettingsOpen(true);
                else onAction(id);
                setOpen(false);
              }}
            >
              <Icon name={icon} />
              <span>{label}</span>
            </button>
          );
        })}
        <button
          type="button"
          className="radial-trigger"
          aria-label={
            open ? "Close quick menu" : "Open quick menu. Drag to move"
          }
          aria-expanded={open}
          onPointerDown={down}
          onPointerMove={move}
          onPointerUp={up}
          onPointerCancel={() => {
            drag.current = null;
          }}
        >
          <Icon name={open ? "close" : "menu"} />
        </button>
      </nav>
      {settingsOpen && (
        <Modal
          title="Quick menu"
          className="radial-settings-modal"
          onClose={() => setSettingsOpen(false)}
        >
          <div className="dialogbody radial-settings-body">
            <p className="radial-settings-intro">
              Tune how the floating menu looks and what it contains.
            </p>
            <label className="radial-range">
              <span>
                <strong>Button size</strong>
                <output>{preferences.size}px</output>
              </span>
              <input
                type="range"
                min="42"
                max="72"
                step="2"
                value={preferences.size}
                onChange={(event) =>
                  setPreferences((value) => ({
                    ...value,
                    size: Number(event.target.value),
                  }))
                }
              />
            </label>
            <label className="radial-range">
              <span>
                <strong>Glass opacity</strong>
                <output>{preferences.opacity}%</output>
              </span>
              <input
                type="range"
                min="35"
                max="100"
                step="5"
                value={preferences.opacity}
                onChange={(event) =>
                  setPreferences((value) => ({
                    ...value,
                    opacity: Number(event.target.value),
                  }))
                }
              />
            </label>
            <fieldset className="radial-action-options">
              <legend>Menu actions</legend>
              {items.map(([id, label, icon]) => (
                <label key={id}>
                  <span>
                    <Icon name={icon} />
                    {label}
                  </span>
                  <input
                    type="checkbox"
                    checked={preferences.enabled.includes(id)}
                    onChange={(event) =>
                      setPreferences((value) => ({
                        ...value,
                        enabled: event.target.checked
                          ? [...value.enabled, id]
                          : value.enabled.filter((item) => item !== id),
                      }))
                    }
                  />
                </label>
              ))}
            </fieldset>
          </div>
          <div className="dialogfoot">
            <button
              type="button"
              onClick={() => setPreferences(defaultPreferences)}
            >
              Reset
            </button>
            <button
              type="button"
              className="primary"
              onClick={() => setSettingsOpen(false)}
            >
              Done
            </button>
          </div>
        </Modal>
      )}
    </>
  );
}
