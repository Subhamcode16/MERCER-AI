import { useEffect, useRef } from "react";
import {
  loadLiquidGlass,
  type LiquidGlassInstance,
} from "./liquidGlassRuntime";

export function LiquidGlassSurface({
  className = "",
  type = "rounded",
  tintOpacity = 0.16,
  borderRadius = 12,
}: {
  className?: string;
  type?: "circle" | "rounded" | "pill";
  tintOpacity?: number;
  borderRadius?: number;
}) {
  const host = useRef<HTMLSpanElement>(null);
  useEffect(() => {
    let disposed = false,
      instance: LiquidGlassInstance | null = null,
      resize: ResizeObserver | null = null;
    void loadLiquidGlass().then((Container) => {
      if (disposed || !Container || !host.current) return;
      instance = new Container({ type, tintOpacity, borderRadius });
      instance.element.classList.add("liquid-surface-renderer");
      instance.element.style.width = "100%";
      instance.element.style.height = "100%";
      instance.element.style.padding = "0";
      instance.element.style.pointerEvents = "none";
      host.current.appendChild(instance.element);
      resize = new ResizeObserver(() => instance?.updateSizeFromDOM());
      resize.observe(host.current);
      requestAnimationFrame(() => instance?.updateSizeFromDOM());
    });
    return () => {
      disposed = true;
      resize?.disconnect();
      instance?.destroy();
    };
  }, [borderRadius, tintOpacity, type]);
  return (
    <span
      ref={host}
      className={`liquid-surface-host ${className}`}
      aria-hidden="true"
    />
  );
}
