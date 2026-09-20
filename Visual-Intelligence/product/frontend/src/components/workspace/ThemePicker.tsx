import { useEffect, useState } from "react";
import type { CSSProperties, KeyboardEvent } from "react";
import { themes } from "./themes";
import { Modal } from "./Modal";
import { Icon } from "./Icon";
const keys = [
  "paper",
  "surface",
  "soft",
  "ink",
  "muted",
  "line",
  "accent",
  "accent-ink",
  "activity",
];
function saved(key: string, fallback: string) {
  try {
    return localStorage.getItem(key) || fallback;
  } catch {
    return fallback;
  }
}
export function useTheme() {
  const [palette, setPalette] = useState(() => {
    const value = saved("fieldwork-chat-palette", "fieldwork");
    return themes.some((t) => t.id === value) ? value : "fieldwork";
  });
  const [night, setNight] = useState(
    () => saved("fieldwork-theme", "paper") === "night",
  );
  useEffect(() => {
    const theme = themes.find((t) => t.id === palette)!;
    document.body.classList.toggle("night", night);
    document.body.dataset.chatTheme = palette;
    keys.forEach((key, i) =>
      document.body.style.setProperty(
        "--" + key,
        (night ? theme.dark : theme.light)[i],
      ),
    );
    try {
      localStorage.setItem("fieldwork-chat-palette", palette);
      localStorage.setItem("fieldwork-theme", night ? "night" : "paper");
    } catch {}
  }, [palette, night]);
  return { palette, setPalette, night, setNight };
}
export function ThemePicker({
  palette,
  night,
  onChange,
  onClose,
}: {
  palette: string;
  night: boolean;
  onChange: (id: string) => void;
  onClose: () => void;
}) {
  function navigate(e: KeyboardEvent<HTMLButtonElement>, index: number) {
    if (
      ![
        "ArrowRight",
        "ArrowLeft",
        "ArrowDown",
        "ArrowUp",
        "Home",
        "End",
      ].includes(e.key)
    )
      return;
    e.preventDefault();
    const next =
      e.key === "Home"
        ? 0
        : e.key === "End"
          ? themes.length - 1
          : (index +
              (["ArrowLeft", "ArrowUp"].includes(e.key)
                ? themes.length - 1
                : 1)) %
            themes.length;
    onChange(themes[next].id);
    e.currentTarget
      .closest("[role=radiogroup]")
      ?.querySelectorAll<HTMLButtonElement>("button")
      [next].focus();
  }
  return (
    <Modal title="Chat themes" className="theme-modal" onClose={onClose}>
      <div className="dialogbody">
        <p className="subtitle">Choose the atmosphere for your workspace</p>
        <div
          className="theme-grid"
          role="radiogroup"
          aria-label="Chat color palette"
        >
          {themes.map((t, i) => {
            const c = night ? t.dark : t.light;
            return (
              <button
                key={t.id}
                type="button"
                className="theme-choice"
                role="radio"
                aria-checked={palette === t.id}
                tabIndex={palette === t.id ? 0 : -1}
                onKeyDown={(e) => navigate(e, i)}
                onClick={() => onChange(t.id)}
                style={
                  {
                    "--preview-surface": c[1],
                    "--preview-soft": c[2],
                    "--preview-line": c[5],
                    "--preview-accent": c[6],
                  } as CSSProperties
                }
              >
                <span className="theme-preview" aria-hidden="true">
                  <span />
                  <span />
                  <span />
                </span>
                <strong>{t.name}</strong>
                <small>{t.description}</small>
                <Icon name="check" className="theme-check" />
              </button>
            );
          })}
        </div>
      </div>
      <div className="dialogfoot">
        <span className="subtitle">
          Saved automatically · pull the cord for {night ? "light" : "dark"}{" "}
          mode
        </span>
        <button className="primary with-icon" onClick={onClose}>
          <Icon name="check" />
          Done
        </button>
      </div>
    </Modal>
  );
}
