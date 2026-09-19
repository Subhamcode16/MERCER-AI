"use client";

import React, { createContext, useContext, useEffect, useState } from "react";

export type Theme = "dark" | "light" | "system";
export type ResolvedTheme = "dark" | "light";

interface ThemeContextType {
  theme: Theme;
  resolvedTheme: ResolvedTheme;
  setTheme: (theme: Theme) => void;
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

const STORAGE_KEY = "vyren-theme";

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setThemeState] = useState<Theme>("dark");
  const [resolvedTheme, setResolvedTheme] = useState<ResolvedTheme>("dark");
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    // Read persisted preference
    const saved = localStorage.getItem(STORAGE_KEY) as Theme | null;
    if (saved && (saved === "dark" || saved === "light" || saved === "system")) {
      setThemeState(saved);
    } else {
      // Default to dark luxury theme
      setThemeState("dark");
    }
    setMounted(true);
  }, []);

  useEffect(() => {
    if (!mounted) return;

    const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");

    const calculateResolved = (currentTheme: Theme): ResolvedTheme => {
      if (currentTheme === "system") {
        return mediaQuery.matches ? "dark" : "light";
      }
      return currentTheme;
    };

    const nextResolved = calculateResolved(theme);
    setResolvedTheme(nextResolved);

    // Apply to DOM
    const root = document.documentElement;
    root.setAttribute("data-theme", nextResolved);
    if (nextResolved === "light") {
      root.classList.add("light");
      root.classList.remove("dark");
    } else {
      root.classList.add("dark");
      root.classList.remove("light");
    }

    localStorage.setItem(STORAGE_KEY, theme);

    const handleSystemChange = () => {
      if (theme === "system") {
        const sysResolved = mediaQuery.matches ? "dark" : "light";
        setResolvedTheme(sysResolved);
        root.setAttribute("data-theme", sysResolved);
        if (sysResolved === "light") {
          root.classList.add("light");
          root.classList.remove("dark");
        } else {
          root.classList.add("dark");
          root.classList.remove("light");
        }
      }
    };

    mediaQuery.addEventListener("change", handleSystemChange);
    return () => mediaQuery.removeEventListener("change", handleSystemChange);
  }, [theme, mounted]);

  const setTheme = (newTheme: Theme) => {
    setThemeState(newTheme);
  };

  const toggleTheme = () => {
    setThemeState((prev) => {
      const current = prev === "system" ? resolvedTheme : prev;
      return current === "dark" ? "light" : "dark";
    });
  };

  return (
    <ThemeContext.Provider value={{ theme, resolvedTheme, setTheme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error("useTheme must be used within a ThemeProvider");
  }
  return context;
}
