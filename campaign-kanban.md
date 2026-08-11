# Mercer AI Campaign Generation — Kanban Roadmap

This roadmap organizes the remaining milestones for the Mercer AI (Fashion Knowledge DNA) system. As per the **Research Strategy** in [validation.md](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/validation.md) and the **Creative Studio OS** protocol, we follow a strict **Research → Specification → Validation → Lock** cycle. No code changes are implemented without prior approved research and detailed specs.

---

## 📋 Kanban Board

| Phase | Task Description | Target File / Component | Status | References |
|---|---|---|---|---|
| **Phase 1: Validation** | **Task 1.1**: Write End-to-End Campaign Workflow Simulation | `VAL-001-textile-workflow.md` | **Done** | [validation.md](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/validation.md) |
| **Phase 1: Validation** | **Task 1.2**: Trace ORRA input/output mapping against vault | `VAL-001-textile-workflow.md` | **Done** | [validation.md](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/validation.md) |
| **Phase 2: Orchestration** | **Task 2.1**: Wire ORRA loop `observe()` with VisionAdapter | [orra_loop.py](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Visual-Intelligence/product/backend/app/services/orra_loop.py) | **Done** | [Backend_missing_breakout.md](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Backend_missing_breakout.md) |
| **Phase 2: Orchestration** | **Task 2.2**: Wire ORRA loop `reason()` & `act()` with prompt/knowledge engines | [orra_loop.py](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Visual-Intelligence/product/backend/app/services/orra_loop.py) | **Done** | [Backend_missing_breakout.md](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Backend_missing_breakout.md) |
| **Phase 2: Orchestration** | **Task 2.3**: Replace local JSON with MongoDB collection storage | `local_store.py` / `database.py` | **Done** | [Backend_missing_breakout.md](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Backend_missing_breakout.md) |
| **Phase 2: Orchestration** | **Task 2.4**: Implement JWT Auth & RLS checks on campaign endpoints | Campaign router & middlewares | **Done** | [Backend_missing_breakout.md](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Backend_missing_breakout.md) |
| **Phase 3: Integration** | **Task 3.1**: Integrate external image generator API (Fal.ai/Flux) | `rendering_engine.py` | **Done** | [Backend_missing_breakout.md](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Backend_missing_breakout.md) |
| **Phase 3: Integration** | **Task 3.2**: Replace local AssetStore with S3/Supabase Storage | `AssetStore` / S3 Client | **Done** | [Backend_missing_breakout.md](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Backend_missing_breakout.md) |
| **Phase 3: Integration** | **Task 3.3**: Implement SSE/WebSockets for streaming AI thoughts | Campaign router & drawer | **Done** | [Backend_missing_breakout.md](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Backend_missing_breakout.md) |
| **Phase 4: Frontend v2** | **Task 4.1**: Build normalized GSAP & Framer Motion Experience Timeline | Frontend Page / Layout | **Done** | [v2-modify.md](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/v2-modify.md) |
| **Phase 4: Frontend v2** | **Task 4.2**: Redesign 4 stages to a single evolving spatial canvas | Frontend Components | **Done** | [v2-modify.md](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/v2-modify.md) |

---

## 🛠️ Step-by-Step Execution Plan

### Goal
Document the roadmap, gain alignment on Phase 1, and prepare the foundation for detailed workflow simulation before executing code.

### Phase 1: Research, Specification & Validation (Current Phase)
1. **Task 1**: Draft the `VAL-001-textile-workflow.md` validation blueprint to trace exactly how the ORRA loop responds to a single Saree input image.
   * *Verify*: The workflow document lists every owner, input schema, output schema, and decision node from upload to delivery.
2. **Task 2**: Walk through the mock scenario details: mapping user visual input -> `Product DNA` -> `Knowledge Node` -> `Prompt Compilation` -> `Render` -> `Remember`.
   * *Verify*: Ensure there is zero ambiguity on which class or database table owns each data attribute.

### Phase 2: Backend Orchestration & Database Integration
1. **Task 3**: Write technical specification for MongoDB Migration and ORRA Loop wiring.
   * *Verify*: Design approved by Creative Director & System Architect.
2. **Task 4**: Swap Local JSON storage with MongoDB campaigns collection.
   * *Verify*: Local unit tests verify campaign document insert, query, and edit.
3. **Task 5**: Connect `observe()`, `reason()`, and `act()` in `orra_loop.py` to live Gemini Vision/Text calls.
   * *Verify*: Triggering the endpoint with a saree image URL successfully extracts DNA and returns prompt recommendations.
4. **Task 6**: Add token authentication middleware and verify endpoint authorization.
   * *Verify*: Requests without a valid JWT are rejected with `401 Unauthorized`.

### Phase 3: External API & Cloud Integration
1. **Task 7**: Write technical specification for external image rendering API and S3/Supabase storage.
   * *Verify*: Specs locked.
2. **Task 8**: Wire Fal.ai/Flux image rendering client and save assets to storage.
   * *Verify*: Mock requests return real generated images stored securely on the cloud.
3. **Task 9**: Implement Server-Sent Events (SSE) or WebSockets to stream AI reasoning logs.
   * *Verify*: UI Drawer renders live execution logs without setInterval polling.

### Phase 4: Frontend v2 (Experience Redesign)
1. **Task 10**: Write design and motion bible for v2 experience.
   * *Verify*: Approved by Creative Director & Motion Director.
2. **Task 11**: Implement the normalized Experience Timeline and evolving spatial canvas.
   * *Verify*: Scroll pinning synchronizes Three.js canvas morphing, SVG patterns, and UI transitions flawlessly.

---

## 🔒 Done When
- [ ] The kanban file `campaign-kanban.md` is successfully registered in the project root.
- [ ] User alignment is obtained on Phase 1 goals and the "green signal" is granted.
