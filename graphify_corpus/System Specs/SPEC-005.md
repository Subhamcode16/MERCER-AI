# SPEC-005
# Autonomy Specification (When may the platform act independently?)

**Status:** Canonical  
**Version:** 1.0  
**Associated Law:** [LAW-005 (Laws of Autonomy)](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/System%20Laws/LAW-005.md)

---

## 1. Credit Ledger & Billing Policies
Every autonomous execution (rendering, parsing, optimization) is bound to credit constraints to protect user resources.

### 1.1 Credit Cost Schedule
- **Product Extraction & Parsing:** 0 credits (universal platform capability).
- **Standard Real-time Generation:**
  - **Nano Banana 2 / GPT Image 2:** 2 credits per image.
  - **Nano Banana Pro (1K Preview):** 3 credits per image.
- **Studio Batch Generation:**
  - **Nano Banana Pro (2K Full):** 4 credits per image (processed through the batch queue).

### 1.2 Two-Phase Commit Safeguard
To guarantee zero double-charging:
- **Phase 1 (Reserve):** Credits are reserved on request. If user balance is insufficient, request is rejected before contacting model APIs.
- **Phase 2 (Commit or Refund):** Upon successful image delivery, credits are committed. If rendering fails due to model timeouts or safety filters, credits are refunded immediately.

---

## 2. Delegation Controls UI
Users control the platform's autonomy settings in a centralized configuration panel.

### 2.1 Autonomy Toggles
- **Asset Rendering Mode:**
  - *Standard Mode:* User approves each scene manually before generation.
  - *Batch Mode (Level 3 - Delegate):* AI schedules rendering campaigns automatically based on approved strategy bento cards.
- **Catalog Management:**
  - *Assisted (Default):* AI categorizes and tags product attributes, awaiting user approval.
  - *Autonomous (Level 4 - Steward):* AI automatically updates catalog attributes and domains, reporting updates to the logs.

---

## 3. Automated Batch Queue Processing
For cost-optimized and non-urgent rendering tasks, the platform runs an autonomous batch coordinator.

### 3.1 Batch Window Policies
- **Rolling Execution Window:** Queue runs every 15 to 30 minutes (not once per day) to maintain a responsive user loop.
- **Background Execution:** User can navigate away or close the campaign.
- **Notification Protocol:** Upon completion, the system fires an in-app toast notification and pushes the assets to the campaign folder.

---

## 4. Safety Gates & Content Policies
The system gates all autonomous prompt compilation against moderation filters prior to model execution.

### 4.1 Content Moderation Loop
1. The AI compiles the **Creative State** into a model prompt.
2. The prompt is sent to the moderation API.
3. If flagged:
   - Request is aborted.
   - Zero credits are reserved.
   - The user receives a clear, non-technical explanation of the safety policy flag.
