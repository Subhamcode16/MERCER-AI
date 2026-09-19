"use client";

import React from "react";
import { ShaderGradientCanvas, ShaderGradient } from "@shadergradient/react";
import { useTheme } from "@/contexts/ThemeContext";

export function WebGLFluidBackground() {
  const { resolvedTheme } = useTheme();
  const isLight = resolvedTheme === "light";

  return (
    <div className={`absolute inset-0 z-0 pointer-events-none overflow-hidden select-none transition-opacity duration-500 ${isLight ? "opacity-35" : "opacity-70"}`}>
      <ShaderGradientCanvas
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          width: "100%",
          height: "100%",
        }}
        pixelDensity={1.2}
        fov={45}
      >
        <ShaderGradient
          control="props"
          type="plane"
          animate="on"
          uSpeed={0.15}
          uStrength={1.5}
          uDensity={1.5}
          uFrequency={5.5}
          color1={isLight ? "#D8C7B0" : "#4C1D95"} // Warm Sand in Light / Deep Violet in Dark
          color2={isLight ? "#EAE0D0" : "#7C2D12"} // Pale Gold in Light / Rich Crimson in Dark
          color3={isLight ? "#FBF9F5" : "#050505"} // Alabaster Base
          cDistance={2.8}
          cPolarAngle={80}
          cameraZoom={9.12}
          rotationZ={235}
          brightness={isLight ? 1.05 : 1.2}
          grain="off"
        />
      </ShaderGradientCanvas>
    </div>
  );
}
