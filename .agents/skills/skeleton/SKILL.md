---
name: skeleton
description: >-
  Use this skill when implementing skeleton UI loading placeholders, shimmer transitions,
  and loading states for dashboard components in Tailwind CSS (especially Tailwind v4).
---

# Skeleton Loading UI

This skill outlines the patterns and CSS utilities for building premium, high-fidelity skeleton loading placeholder screens.

## Core CSS Utilities (Tailwind v4 `@utility`)

Rather than relying on large Javascript loader packages, we register lightweight, native CSS utility classes inside `globals.css` that define custom background fills matching our Mercer AI theme:

```css
@utility placeholder {
  background-color: rgba(225, 212, 192, 0.06); /* subtle warm ivory */
  border-radius: var(--radius-md, 0.75rem);
}

@utility placeholder-circle {
  aspect-ratio: 1 / 1;
  background-color: rgba(225, 212, 192, 0.06);
  border-radius: 9999px;
}
```

Combine these utilities with Tailwind's standard `animate-pulse` to create a smooth, rhythmic breathing effect:

```tsx
// Simple Avatar + Title + Line Skeleton Loader
export function UserProfileSkeleton() {
  return (
    <div className="flex items-center gap-4 animate-pulse">
      <div className="placeholder-circle w-12" />
      <div className="flex-1 space-y-2">
        <div className="placeholder h-4 w-1/3" />
        <div className="placeholder h-3 w-1/2" />
      </div>
    </div>
  );
}
```

## Premium Shimmer Effects (Glossy/Metallic Sweep)

For visual card listings or headers, use a custom gradient shimmer sweep to give a hardware-accelerated gloss effect:

```css
@keyframes shimmer-sweep {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

.shimmer-gradient {
  position: relative;
  overflow: hidden;
}

.shimmer-gradient::after {
  position: absolute;
  inset: 0;
  transform: translateX(-100%);
  background-image: linear-gradient(
    90deg,
    rgba(255, 255, 255, 0) 0%,
    rgba(225, 212, 192, 0.04) 20%,
    rgba(225, 212, 192, 0.08) 60%,
    rgba(255, 255, 255, 0) 100%
  );
  animation: shimmer-sweep 2s infinite;
  content: '';
}
```
