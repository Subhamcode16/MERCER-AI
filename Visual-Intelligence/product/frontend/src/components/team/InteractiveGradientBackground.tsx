"use client";

import React, { useEffect, useRef } from "react";
import { useTheme } from "@/contexts/ThemeContext";

export function InteractiveGradientBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const mouseRef = useRef({ x: 0, y: 0, targetX: 0, targetY: 0 });
  const { resolvedTheme } = useTheme();

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let animationFrameId: number;
    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    // Initial mouse center position
    mouseRef.current.x = width / 2;
    mouseRef.current.y = height / 2;
    mouseRef.current.targetX = width / 2;
    mouseRef.current.targetY = height / 2;

    const isLight = resolvedTheme === "light";

    // Soft colored blobs adjusted for theme
    const blobs = isLight
      ? [
          {
            x: width * 0.3,
            y: height * 0.4,
            r: 480,
            color: "rgba(225, 175, 120, 0.22)", // Warm Champagne / Amber
          },
          {
            x: width * 0.7,
            y: height * 0.3,
            r: 520,
            color: "rgba(180, 140, 210, 0.18)", // Muted Lilac
          },
          {
            x: width * 0.5,
            y: height * 0.7,
            r: 420,
            color: "rgba(235, 190, 160, 0.2)", // Soft Peach
          },
        ]
      : [
          {
            x: width * 0.3,
            y: height * 0.4,
            r: 450,
            color: "rgba(124, 45, 18, 0.35)", // Crimson
          },
          {
            x: width * 0.7,
            y: height * 0.3,
            r: 500,
            color: "rgba(76, 29, 149, 0.3)", // Violet
          },
          {
            x: width * 0.5,
            y: height * 0.7,
            r: 400,
            color: "rgba(120, 53, 15, 0.25)", // Amber Gold
          },
        ];

    const handleMouseMove = (e: MouseEvent) => {
      mouseRef.current.targetX = e.clientX;
      mouseRef.current.targetY = e.clientY;
    };

    window.addEventListener("mousemove", handleMouseMove);

    const handleResize = () => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    };
    window.addEventListener("resize", handleResize);

    let time = 0;
    const render = () => {
      time += 0.003;
      
      // Paint background
      ctx.fillStyle = isLight ? "#FBF9F5" : "#050505";
      ctx.fillRect(0, 0, width, height);

      // Smooth cursor spring physics
      const mouse = mouseRef.current;
      mouse.x += (mouse.targetX - mouse.x) * 0.04;
      mouse.y += (mouse.targetY - mouse.y) * 0.04;

      blobs.forEach((blob, index) => {
        // Slow orbital oscillations
        const offsetX = Math.sin(time + index * 12) * 180;
        const offsetY = Math.cos(time + index * 18) * 180;

        // Attract toward mouse coordinates with index-staggered spring delays
        const attractionSpeed = 0.015 + index * 0.008;
        blob.x += (mouse.x - blob.x) * attractionSpeed;
        blob.y += (mouse.y - blob.y) * attractionSpeed;

        const currentX = blob.x + offsetX;
        const currentY = blob.y + offsetY;

        // Draw soft radial gradient circles
        const grad = ctx.createRadialGradient(
          currentX,
          currentY,
          0,
          currentX,
          currentY,
          blob.r
        );
        grad.addColorStop(0, blob.color);
        grad.addColorStop(1, isLight ? "rgba(251, 249, 245, 0)" : "rgba(5, 5, 5, 0)");

        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.arc(currentX, currentY, blob.r, 0, Math.PI * 2);
        ctx.fill();
      });

      animationFrameId = requestAnimationFrame(render);
    };

    render();

    return () => {
      cancelAnimationFrame(animationFrameId);
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("resize", handleResize);
    };
  }, [resolvedTheme]);


  return (
    <canvas
      ref={canvasRef}
      className="absolute inset-0 w-full h-full object-cover filter blur-[100px] transition-opacity duration-1000"
      style={{ pointerEvents: "none", zIndex: 0 }}
    />
  );
}
