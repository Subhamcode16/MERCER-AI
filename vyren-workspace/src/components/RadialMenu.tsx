import { useEffect, useRef, useState } from "react";
import type { CSSProperties, PointerEvent as ReactPointerEvent } from "react";
import { Icon, type IconName } from "./Icon";
import { Modal } from "./Modal";
import {
  loadLiquidGlass,
  type LiquidGlassInstance,
} from "./liquidGlassRuntime";

export interface MenuItemDefinition {
  id: string;
  label: string;
  icon: IconName;
  category: "routes" | "workspace";
}

export const ALL_MENU_ITEMS: MenuItemDefinition[] = [
  // Routes / Navigation
  { id: "home", label: "Home", icon: "home", category: "routes" },
  { id: "studio", label: "Workspace", icon: "grid", category: "routes" },
  { id: "metrics", label: "Metrics Dashboard", icon: "metrics", category: "routes" },
  { id: "kanban", label: "Kanban Board", icon: "kanban", category: "routes" },
  { id: "assets", label: "Assets", icon: "assets", category: "routes" },
  { id: "settings", label: "Settings", icon: "settings", category: "routes" },

  // Workspace Actions
  { id: "appearance", label: "Appearance", icon: "palette", category: "workspace" },
  { id: "workforce", label: "New agent", icon: "plus", category: "workspace" },
  { id: "groups", label: "Groups", icon: "group", category: "workspace" },
  { id: "projects", label: "New project", icon: "file", category: "workspace" },
  { id: "workspace", label: "Overview", icon: "shield", category: "workspace" },
  { id: "shortcuts", label: "Shortcuts", icon: "model", category: "workspace" },
];

export type Point = { x: number; y: number };
export type MenuId = string;

export type MenuPreferences = {
  size: number;
  opacity: number;
  enabled: MenuId[];
};

export const defaultPreferences: MenuPreferences = {
  size: 52,
  opacity: 86,
  enabled: [
    "home",
    "metrics",
    "kanban",
    "assets",
    "appearance",
    "workforce",
    "groups",
    "settings",
  ],
};

function clamp(point: Point, rad = 104): Point {
  const margin = rad + 32;
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
        if (saved && Array.isArray(saved.enabled) && saved.enabled.length > 0) {
          const validIds = new Set(ALL_MENU_ITEMS.map((i) => i.id));
          const enabled = saved.enabled.filter((id) => validIds.has(id));
          return {
            size: Math.min(72, Math.max(42, Number(saved.size) || 52)),
            opacity: Math.min(100, Math.max(35, Number(saved.opacity) || 86)),
            enabled: enabled.length > 0 ? enabled : defaultPreferences.enabled,
          };
        }
        return defaultPreferences;
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

  const visibleItems = ALL_MENU_ITEMS.filter((item) =>
    preferences.enabled.includes(item.id),
  );
  const menuItems: { id: string; label: string; icon: IconName }[] = [
    ...visibleItems,
    { id: "menu-settings", label: "Menu settings", icon: "settings" },
  ];

  const dynamicRadius = Math.max(
    104,
    Math.min(150, 96 + (menuItems.length - 6) * 8),
  );

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
      dynamicRadius,
    );
    setPosition(next);
    setReady(true);
    const resize = () => setPosition((point) => clamp(point, dynamicRadius));
    addEventListener("resize", resize);
    return () => removeEventListener("resize", resize);
  }, [dynamicRadius]);

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
    const next = clamp(
      {
        x: e.clientX - drag.current.dx,
        y: e.clientY - drag.current.dy,
      },
      dynamicRadius,
    );
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
        {menuItems.map((item, index) => {
          const angle =
            ((-90 + index * (360 / menuItems.length)) * Math.PI) / 180;
          return (
            <button
              key={item.id}
              type="button"
              className="radial-action"
              style={
                {
                  "--radial-x": `${Math.cos(angle) * dynamicRadius}px`,
                  "--radial-y": `${Math.sin(angle) * dynamicRadius}px`,
                  "--radial-delay": `${index * 24}ms`,
                } as CSSProperties
              }
              aria-label={item.label}
              tabIndex={open ? 0 : -1}
              onClick={() => {
                if (item.id === "menu-settings") setSettingsOpen(true);
                else onAction(item.id);
                setOpen(false);
              }}
            >
              <Icon name={item.icon} />
              <span>{item.label}</span>
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
              <legend>Routes &amp; Navigation</legend>
              {ALL_MENU_ITEMS.filter((i) => i.category === "routes").map(
                (item) => (
                  <label key={item.id}>
                    <span>
                      <Icon name={item.icon} />
                      {item.label}
                    </span>
                    <input
                      type="checkbox"
                      checked={preferences.enabled.includes(item.id)}
                      onChange={(event) =>
                        setPreferences((value) => ({
                          ...value,
                          enabled: event.target.checked
                            ? [...value.enabled, item.id]
                            : value.enabled.filter((id) => id !== item.id),
                        }))
                      }
                    />
                  </label>
                ),
              )}
            </fieldset>
            <fieldset className="radial-action-options">
              <legend>Workspace Actions</legend>
              {ALL_MENU_ITEMS.filter((i) => i.category === "workspace").map(
                (item) => (
                  <label key={item.id}>
                    <span>
                      <Icon name={item.icon} />
                      {item.label}
                    </span>
                    <input
                      type="checkbox"
                      checked={preferences.enabled.includes(item.id)}
                      onChange={(event) =>
                        setPreferences((value) => ({
                          ...value,
                          enabled: event.target.checked
                            ? [...value.enabled, item.id]
                            : value.enabled.filter((id) => id !== item.id),
                        }))
                      }
                    />
                  </label>
                ),
              )}
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
              Save &amp; Apply
            </button>
          </div>
        </Modal>
      )}
    </>
  );
}
