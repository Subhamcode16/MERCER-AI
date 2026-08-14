"use client";

import React from "react";
import { ShaderGradientCanvas, ShaderGradient } from "@shadergradient/react";

export function WebGLFluidBackground() {
  return (
    <div className="absolute inset-0 z-0 opacity-70 pointer-events-none overflow-hidden select-none">
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
          color1="#4C1D95" // Deep Violet
          color2="#7C2D12" // Rich Crimson
          color3="#050505" // Pitch Black
          cDistance={2.8}
          cPolarAngle={80}
          cameraZoom={9.12}
          rotationZ={235}
          brightness={1.2}
          grain="off"
        />
      </ShaderGradientCanvas>
    </div>
  );
}
