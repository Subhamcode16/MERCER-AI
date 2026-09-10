---
tags:
  - technical
  - frontend
  - backend
  - ui
---

# 💻 Technical & UI Specifications

This note maps the implementation details of the frontend user interface and backend storage adapters.

---

## 🎨 Frontend UI Layer

The product frontend is built using Next.js, incorporating rich motion gradients and dynamic campaign routing.

### 🌊 Shader Background
- **Component File:** [ShaderBg.tsx](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Visual-Intelligence/product/frontend/src/components/ShaderBg.tsx)
- **Tech Stack:** `@shadergradient/react` and `three` (WebGL).
- **Configuration:**
  - Type: `waterPlane`
  - Speed: `0.2`, Strength: `1.5`, Density: `1.2`
  - Colors: `#040407` (Deep Obsidian), `#4f4f80` (Muted Purple), and `#6199f6` (Vibrant Blue).
  - Overlay: Linear gradient fade blending into a dark charcoal theme (`#0a0a13`).

### 🗺️ Dynamic Campaign Page
- **Page File:** [campaign/[id]/page.tsx](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Visual-Intelligence/product/frontend/src/app/campaign/%5Bid%5D/page.tsx)
- **Layout File:** [layout.tsx](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Visual-Intelligence/product/frontend/src/app/layout.tsx)
- **Details:** Dynamically pulls generated marketing campaigns based on campaign IDs, rendering localized imagery matching target visual attributes.

---

## 💾 Backend Storage Layer

- **Local Store:** [local_store.py](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Visual-Intelligence/product/backend/storage/local_store.py)
- **Purpose:** Handles local storage protocols for caching ingested image files and storing mapped knowledge claims before they are committed to database clusters.

---

## 🔗 Related Notes
- [[Visual_Intelligence_MOC]] — Return to the Visual Intelligence MOC.
- [[Specialty_Fabrics]] — Referenced during dynamic rendering in Campaign pages.
