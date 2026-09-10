# SPEC-001
# Knowledge Specification (What is true?)

**Status:** Canonical  
**Version:** 1.0  
**Associated Law:** [LAW-001 (Laws of Knowledge)](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/System%20Laws/LAW-001.md)

---

## 1. Product Ingestion & Visual Analyzer
The platform must ingest raw physical product uploads and automatically extract verified product attributes.

### 1.1 Ingestion Specifications
- **Supported Formats:** JPG, PNG, WEBP, HEIC.
- **Maximum Resolution:** 4096px (longest edge).
- **Maximum File Size:** 15MB.
- **Base Extraction Pipeline:**
  1. Automated silhouette extraction (transparent background output).
  2. Color space extraction (dominant, secondary, and accent colors in HEX and Pantone values).
  3. Visual taxonomy mapping (attributing categories: e.g., "Human Expression > Apparel > Saree").

### 1.2 Surface Material Solver Inputs
The visual analyzer must compute material properties:
- **Surface Texture Density:** Coarseness, weave pattern (e.g., plain, twill, satin), or material composition (e.g., leather grain, metal finish).
- **Reflectance Matrix:** Specular highlights, metallic-ness, and glossiness values.
- **Draping Weight Index:** Estimate fabric weight (light, medium, heavy) based on draping folds and silhouette flow.

---

## 2. Brand Profile Specification
To maintain creative consistency, every Brand entity contains a structured representation of its visual identity.

### 2.1 Identity Vectors
- **Aesthetic DNA Tags:** Curated list of design tags (e.g., "Minimalist", "Heritage", "Quiet Luxury", "Avant-Garde").
- **Visual Style Guidelines:**
  - **Typography Rules:** Allowed font pairings, letter spacing guidelines, and casing rules.
  - **Color Palette Restrictions:** Primary, secondary, and negative-space colors.
  - **Composition Preferences:** Placement rules (e.g., "Symmetrical layouts only", "Negative space > 40%").
- **Brand Memory Core:** List of verified past successful campaign themes and approved visual directions.

---

## 3. Automated Domain Routing
When a product is uploaded, the system determines which domain plugin governs its creative reasoning.

### 3.1 Routing Rules
- The system checks the classification metadata against our canonical **Intelligence Domains** defined in [GLOSSARY-003](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Ontology%20foundations/GLOSSARY-003.md):
  - **Human Expression:** Activated for apparel, footwear, jewelry, and accessories.
  - **Living Environment:** Activated for furniture, rugs, lamps, and home decor.
  - **Personal Care:** Activated for skincare, cosmetics, and packaging.
- If classification confidence is below 85%, the system prompts the user with a low-friction classification step before loading domain ontologies.

---

## 4. Verification & Provenance UI
No extracted attribute becomes "Knowledge" until it passes through verification.

### 4.1 Provenance Logging
- Every attribute has a provenance card indicating:
  - **Source:** (e.g., "Gemini Vision Model v3.1")
  - **Confidence:** Percentage value (e.g., "94% Confidence")
  - **Verification Status:** `Unverified` (default) or `User-Verified`.
- Users must be able to edit any AI-generated attribute in the interface. Once edited or approved, the state shifts to `User-Verified` and is locked as verified Knowledge.
