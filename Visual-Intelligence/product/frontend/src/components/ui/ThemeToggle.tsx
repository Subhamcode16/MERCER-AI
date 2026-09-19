"use client";

import React, { useEffect, useState } from "react";
import { useTheme } from "@/contexts/ThemeContext";
import { Sun, Moon } from "lucide-react";

interface ThemeToggleProps {
  className?: string;
  showLabel?: boolean;
}

export function ThemeToggle({ className = "", showLabel = false }: ThemeToggleProps) {
  const { resolvedTheme, toggleTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return (
      <button
        aria-label="Toggle theme"
        className={`w-9 h-9 rounded-full flex items-center justify-center border border-border/40 bg-card/60 backdrop-blur-md opacity-70 ${className}`}
        disabled
      >
        <div className="w-4 h-4 rounded-full bg-foreground/20 animate-pulse" />
      </button>
    );
  }

  const isLight = resolvedTheme === "light";

  return (
    <button
      onClick={toggleTheme}
      aria-label={isLight ? "Switch to dark mode" : "Switch to light mode"}
      title={isLight ? "Switch to dark mode" : "Switch to light mode"}
      className={`group relative flex items-center gap-2 px-2.5 py-1.5 rounded-full border border-border/60 bg-card/70 hover:bg-card/90 hover:border-border transition-all duration-300 backdrop-blur-md cursor-pointer focus:outline-none focus:ring-1 focus:ring-ring ${className}`}
    >
      <div className="relative w-5 h-5 flex items-center justify-center">
        {/* Sun Icon */}
        <Sun
          className={`w-4 h-4 text-amber-600 dark:text-amber-300 transition-all duration-300 ${
            isLight
              ? "opacity-100 rotate-0 scale-100"
              : "opacity-0 -rotate-90 scale-0 absolute"
          }`}
        />
        {/* Moon Icon */}
        <Moon
          className={`w-4 h-4 text-foreground/80 group-hover:text-foreground transition-all duration-300 ${
            !isLight
              ? "opacity-100 rotate-0 scale-100"
              : "opacity-0 rotate-90 scale-0 absolute"
          }`}
        />
      </div>

      {showLabel && (
        <span className="text-xs font-sans uppercase tracking-wider text-muted-foreground group-hover:text-foreground transition-colors pr-1">
          {isLight ? "Light" : "Dark"}
        </span>
      )}
    </button>
  );
}
