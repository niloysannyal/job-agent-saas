---
paths:
  - "frontend/src/**/*.jsx"
  - "frontend/src/**/*.js"
  - "frontend/src/**/*.css"
---
# React Frontend Development Standards (adapted from ECC)

## 1. Anti-Template Quality & Design System
- Strictly adhere to the **Obsidian & Cyber Emerald** dual-theme design system.
- Support both `[data-theme="dark"]` (deep obsidian `#0a0f1a` with emerald neon accents) and Light mode (crisp `#ffffff` / `#f8fafc` with subtle emerald gradients).
- Ban generic template defaults (e.g. gray-on-white card grids, raw unstyled buttons, or inconsistent corner radii).
- All buttons must use standardized styling: `.btn-primary` or `.btn-secondary` with `border-radius: var(--radius-sm)` (6px) or `var(--radius-md)` (8px).

## 2. Modal Backdrops & Glassmorphism
- Modal overlays must use frosted glassmorphism:
  - `background: var(--modal-backdrop-bg)`
  - `backdrop-filter: blur(var(--modal-backdrop-blur, 16px)) saturate(160%)`
  - `-webkit-backdrop-filter: blur(var(--modal-backdrop-blur, 16px)) saturate(160%)`
- Never plunge the background into opaque black.
- The left sidebar (`.app-sidebar`) must stay intact and visible (`z-index: 1200; position: relative`). Scoped backdrop coordinates to `left: 270px; width: calc(100vw - 270px)` on desktop.

## 3. Component Architecture & State
- Keep components cohesive and clean. Extract repetitive sub-cards (e.g. Bento metrics, Provider cards, Status pills).
- Controlled modals must always support:
  - Click outside backdrop to close.
  - `Escape` key listener to dismiss.
  - Automatic close on tab change.

## 4. Accessibility & Responsiveness
- Provide `aria-label` for all icon-only buttons (`X`, `Search`, `Refresh`, `Trash2`).
- Responsive layout breakpoints: standard desktop (1280px+), compact desktop (900px-1200px), tablet/mobile (<900px).

