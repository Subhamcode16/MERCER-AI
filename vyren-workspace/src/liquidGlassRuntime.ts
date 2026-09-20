export interface LiquidGlassInstance {
  element: HTMLDivElement;
  tintOpacity: number;
  gl_refs: {
    gl?: WebGLRenderingContext;
    tintOpacityLoc?: WebGLUniformLocation | null;
  };
  updateSizeFromDOM: () => void;
  render?: () => void;
  destroy: () => void;
}

type LiquidGlassConstructor = new (options: {
  type: "circle" | "rounded" | "pill";
  tintOpacity: number;
  borderRadius?: number;
}) => LiquidGlassInstance;

declare global {
  interface Window {
    html2canvas: typeof import("html2canvas").default;
    LiquidGlassContainer?: LiquidGlassConstructor;
  }
}

let loader: Promise<LiquidGlassConstructor | null> | null = null;

export function loadLiquidGlass() {
  if (loader) return loader;
  loader = new Promise(async (resolve) => {
    if (matchMedia("(prefers-reduced-motion: reduce)").matches) {
      resolve(null);
      return;
    }
    const probe = document.createElement("canvas");
    if (!probe.getContext("webgl2")) {
      resolve(null);
      return;
    }
    const { default: html2canvas } = await import("html2canvas");
    window.html2canvas = html2canvas;
    if (window.LiquidGlassContainer) {
      resolve(window.LiquidGlassContainer);
      return;
    }
    const script = document.createElement("script");
    script.src = "/vendor/liquid-glass/container.js";
    script.dataset.liquidGlassRuntime = "true";
    script.onload = () => resolve(window.LiquidGlassContainer || null);
    script.onerror = () => resolve(null);
    document.head.appendChild(script);
  });
  return loader;
}
