---
VIS-ID: RES-002
Title: Image Analysis Pipeline (Station 2)
Version: 1.0.0
Status: Draft
Owner: Visual Intelligence Research (Track B)
Last Updated: 2026-07-01
Depends On:
  - RES-001
---

# RES-002: Image Analysis Pipeline (Station 2)

## Purpose

The **Image Analysis Pipeline (Station 2)** is the first active processing node in the Visual Intelligence Factory (VIF). 

Once an image passes the Quality Assessment (Station 1), it arrives at Station 2. The purpose of this station is strictly **structural isolation**. It does *not* attempt to understand the semantic meaning of the image (e.g., it does not care if the garment is a Saree or a Lehenga). Its sole responsibility is to find the primary subjects, generate pixel-perfect masks, and establish coordinate metadata so that downstream stations can perform focused semantic extraction.

---

## 1. Station Contract

### A. Inputs
- **Asset ID:** Unique identifier for the image.
- **Verified Image Asset:** High-resolution image (passed Station 1 quality checks).

### B. Outputs
- **Subject Bounding Boxes:** `[x_min, y_min, x_max, y_max]` coordinates for all primary subjects (Human, Garment).
- **Subject Masks:** High-fidelity Alpha masks for foreground isolation.
- **Coordinate Metadata (JSON):** Normalized spatial data allowing downstream stations (like Station 3 and 4) to crop the image in memory dynamically. *Note: Station 2 does not generate or save physical cropped files, preventing storage bloat.*

---

## 2. Core Tasks

### Task 1: Foreground Detection (Subject Isolation)
The station utilizes a foundational object detection model (e.g., YOLO, Grounding DINO) to identify the boundaries of the primary subjects within the image.
- **Target Objects:** Human Body, Primary Garment, Props.

### Task 2: High-Fidelity Segmentation
Once the bounding box is established, a segmentation model (e.g., SAM - Segment Anything Model) generates a pixel-perfect mask separating the foreground from the background.
- This mask is critical for downstream extraction. The semantic engine at Station 3 needs to know exactly which pixels belong to the "fabric" and which belong to the "background wall".

### Task 3: Normalization & Coordinate Generation
The spatial relationships are normalized into a lightweight JSON payload.
- This includes the centroid of the subject, the percentage of the frame occupied, and the aspect ratio.

---

## 3. Quality & Confidence Metrics

Every image exiting Station 2 is stamped with mathematical metrics.

### Quality Metrics
- **Edge Precision:** The sharpness of the segmentation mask.
- **Occlusion Rate:** The percentage of the subject hidden by foreground obstacles (e.g., a hand covering the drape).

### Confidence Score
- **Detection Probability (0.0 to 1.0):** The model's statistical confidence that the bounding box contains the intended subject.

---

## 4. Failure Handling & Human Review

The VIF is an industrial pipeline. It cannot afford to choke on edge cases. Station 2 enforces a strict fallback hierarchy:

1. **Primary Execution:** Run the primary segmentation model.
2. **Failure Condition:** If `Detection Probability < 0.85` or if multiple overlapping subjects cause catastrophic occlusion.
3. **Automated Fallback:** The station re-attempts segmentation using an alternative, slower, high-precision model.
4. **Human Review Threshold:** If the fallback model also yields a `Confidence < 0.85`, the image is safely paused and routed to the **Human Verification Queue (Station 6)**, where an annotator manually draws or corrects the bounding box.

---

## 5. Architectural Boundaries

- **No Semantic Parsing:** Station 2 cannot output "Silk." It can only output "Foreground Subject."
- **No Ontology Mapping:** Station 2 does not interact with `VIO-005` or `VIO-006`. It prepares the asset so that Station 3 and Station 4 can map the ontology.
