"use client";

import React, { useState } from "react";
import { UserCheck, RotateCcw, Lock, Sun, Eye, Sparkles } from "lucide-react";

export const DigitalHumanTurntable: React.FC = () => {
  const [yawAngle, setYawAngle] = useState<number>(0);
  const [pitchAngle, setPitchAngle] = useState<number>(0);
  const [identityLocked, setIdentityLocked] = useState<boolean>(true);
  const [lightingAzimuth, setLightingAzimuth] = useState<number>(45);

  return (
    <div className="absolute inset-0 pointer-events-none flex flex-col justify-between p-4 z-20">
      {/* Top Bar */}
      <div className="pointer-events-auto flex items-center justify-between bg-black/85 backdrop-blur-md border border-purple-500/20 rounded-lg px-4 py-2.5 text-xs text-white">
        <div className="flex items-center gap-2">
          <UserCheck className="w-4 h-4 text-purple-400" />
          <span className="font-mono font-semibold tracking-wider text-purple-200">DIGITAL HUMAN 360° TURNTABLE & IDENTITY LOCK</span>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setIdentityLocked(!identityLocked)}
            className={`flex items-center gap-1.5 px-3 py-1 rounded font-mono text-[11px] transition-colors ${
              identityLocked
                ? "bg-purple-500/20 text-purple-300 border border-purple-500/40"
                : "bg-red-500/20 text-red-300 border border-red-500/40"
            }`}
          >
            <Lock className="w-3 h-3" />
            <span>{identityLocked ? "IDENTITY LOCKED (FIDELITY 99.2%)" : "UNLOCKED"}</span>
          </button>
        </div>
      </div>

      {/* Center 3D Turntable Reticle */}
      <div className="flex-1 flex items-center justify-center my-2 relative">
        <div className="w-[300px] h-[380px] rounded-full border border-purple-500/30 flex items-center justify-center relative">
          {/* Circular Angle Degree Ring */}
          <div
            className="absolute inset-0 rounded-full border-2 border-dashed border-purple-400/20 transition-transform duration-100"
            style={{ transform: `rotate(${yawAngle}deg)` }}
          />
          <div className="text-center font-mono text-xs z-10 bg-black/60 backdrop-blur-sm p-4 rounded-xl border border-white/10">
            <Sparkles className="w-5 h-5 text-purple-400 mx-auto mb-1 animate-spin" style={{ animationDuration: "12s" }} />
            <div className="text-white font-semibold">AVATAR MODEL: ELENA-V2</div>
            <div className="text-[11px] text-purple-300 mt-1">Yaw: {yawAngle}° • Pitch: {pitchAngle}°</div>
            <div className="text-[10px] text-neutral-400 mt-0.5">Lighting Key: {lightingAzimuth}° Azimuth</div>
          </div>
        </div>
      </div>

      {/* Bottom Interactive Rotational Slider HUD */}
      <div className="pointer-events-auto bg-black/85 backdrop-blur-md border border-white/10 rounded-lg p-3 text-xs text-white flex items-center justify-between gap-6">
        {/* Yaw Slider */}
        <div className="flex-1 flex items-center gap-2">
          <span className="text-neutral-400 font-mono text-[11px] w-14">Yaw (360°):</span>
          <input
            type="range"
            min="-180"
            max="180"
            value={yawAngle}
            onChange={(e) => setYawAngle(Number(e.target.value))}
            className="w-full accent-purple-500 cursor-pointer"
          />
          <span className="font-mono text-purple-300 w-10 text-right">{yawAngle}°</span>
        </div>

        {/* Pitch Slider */}
        <div className="flex-1 flex items-center gap-2">
          <span className="text-neutral-400 font-mono text-[11px] w-14">Pitch:</span>
          <input
            type="range"
            min="-30"
            max="30"
            value={pitchAngle}
            onChange={(e) => setPitchAngle(Number(e.target.value))}
            className="w-full accent-purple-500 cursor-pointer"
          />
          <span className="font-mono text-purple-300 w-10 text-right">{pitchAngle}°</span>
        </div>

        {/* Reset Button */}
        <button
          onClick={() => {
            setYawAngle(0);
            setPitchAngle(0);
          }}
          className="flex items-center gap-1 text-neutral-400 hover:text-white px-2 py-1 rounded bg-neutral-900 border border-white/5 font-mono text-[11px]"
        >
          <RotateCcw className="w-3 h-3" />
          <span>Reset Frontal</span>
        </button>
      </div>
    </div>
  );
};
