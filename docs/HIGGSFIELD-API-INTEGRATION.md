# ❖ Higgsfield Open API Integration — Architecture & Developer Guide

## 1. Executive Summary & Architectural Motivation

VYREN consolidates its visual and motion creative pipelines by integrating **Higgsfield's Open Source API** as the unified creative generation engine. 

Previously, disparate tools were required for static image synthesis, video generation, and 3D camera turntable motion. Higgsfield's open API standardizes:
1. **Cinematic Text-to-Image Generation**
2. **Text-to-Video & Image-to-Video Synthesis**
3. **14 Camera Trajectory & Physics Motion Vectors** (including 360° digital turntables, dolly, crane, orbit)
4. **Visual DNA Parameter Injection** (seed-locking, aesthetic token conditioning)
5. **Waterfall Failover** (Higgsfield &rarr; Gemini &rarr; Deterministic Sandbox)

Gemini Multimodal Vision remains paired alongside Higgsfield for high-speed semantic reasoning, Visual DNA extraction, and creative quality critique.

---

## 2. System Topology & Request Lifecycle

```
 ┌────────────────────────────────────────────────────────────────────────────────────────┐
 │                                       VYREN OS                                         │
 ├───────────────────────────────────────┬────────────────────────────────────────────────┤
 │   CREATIVE WORKFORCE & AGENTIC ROOMS  │   CAMPAIGN STUDIO & DIGITAL TURNTABLE (UI)     │
 │   • Creative Director Persona         │   • 360° Drape / Material Physics Inspector    │
 │   • Lighting & Camera Designer        │   • Omnichannel Aspect Ratio Switcher (9:16/16:9)
 └───────────────────┬───────────────────┴────────────────────────┬───────────────────────┘
                     │                                            │
                     ▼                                            ▼
 ┌────────────────────────────────────────────────────────────────────────────────────────┐
 │                              VISUAL MODEL GATEWAY                                      │
 │   ┌────────────────────────────────────────────────────────────────────────────────┐   │
 │   │ `HiggsfieldVisualProvider`                                                     │   │
 │   │   • Text-to-Image / Image-to-Video generation requests                         │   │
 │   │   • Camera motion vectors (Dolly, Pan, Orbit, Crane, Roll)                     │   │
 │   │   • Motion strength & seed consistency locks                                   │   │
 │   │   • Async job dispatch + Webhook/Polling task manager                          │   │
 │   └───────────────────────────────────────┬────────────────────────────────────────┘   │
 │                                           │                                            │
 │                     ┌─────────────────────┴───────────────────────┐                    │
 │                     ▼                                             ▼                    │
 │   ┌──────────────────────────────────┐          ┌──────────────────────────────────┐   │
 │   │    WATERFALL FAILOVER ENGINE     │          │    CRYPTOGRAPHIC VISUAL LEDGER   │   │
 │   │  1. Higgsfield Primary           │          │  • SHA-256 Prompt & Config Hash  │   │
 │   │  2. Gemini Image/Vision Fallback │          │  • Visual DNA Reference Pinning  │   │
 │   │  3. Deterministic Sandbox Mock   │          │  • Tamper-Evident Lineage Proof  │   │
 │   └──────────────────────────────────┘          └──────────────────────────────────┘   │
 └────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Data Schemas & Camera Motion Types

### Camera Motion Vectors (`CameraMotion`)
Defined in [`models.py`](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Visual-Intelligence/product/backend/src/visual_model_gateway/models.py):

```python
class CameraMotion(str, Enum):
    STATIC = "STATIC"
    PAN_LEFT = "PAN_LEFT"
    PAN_RIGHT = "PAN_RIGHT"
    TILT_UP = "TILT_UP"
    TILT_DOWN = "TILT_DOWN"
    ZOOM_IN = "ZOOM_IN"
    ZOOM_OUT = "ZOOM_OUT"
    DOLLY_IN = "DOLLY_IN"
    DOLLY_OUT = "DOLLY_OUT"
    ORBIT_360 = "ORBIT_360"
    TURNTABLE_CW = "TURNTABLE_CW"
    TURNTABLE_CCW = "TURNTABLE_CCW"
    CRANE_UP = "CRANE_UP"
    ROLL = "ROLL"
```

### Video Generation Request & Response
```python
class VideoGenerationRequest(BaseModel):
    request_id: str
    prompt: str
    source_image_url: Optional[str] = None
    aspect_ratio: str = "16:9"  # "16:9", "9:16", "1:1", "4:5"
    camera_motion: CameraMotion = CameraMotion.STATIC
    duration_sec: float = 4.0
    fps: int = 24
    motion_strength: float = 1.0
    seed: Optional[int] = None
    creative_direction: Dict[str, Any] = Field(default_factory=dict)
    visual_dna: Dict[str, Any] = Field(default_factory=dict)
    parent_artifact_id: Optional[str] = None
    client_id: Optional[str] = None
    created_at: float = Field(default_factory=time.time)

class VideoGenerationResponse(BaseModel):
    artifact_id: str
    request_id: str
    video_url: str
    thumbnail_url: Optional[str] = None
    mime_type: str = "video/mp4"
    aspect_ratio: str
    duration_sec: float
    fps: int
    camera_motion: CameraMotion
    lineage: VisualLineage
    latency_ms: float = 0.0
    status: str = "SUCCESS"
```

---

## 4. Usage Examples

### 1. Generating an Image with Visual DNA Injection
```python
from src.visual_model_gateway import VisualModelGateway, ImageGenerationRequest

gateway = VisualModelGateway.create_default()

req = ImageGenerationRequest(
    prompt="Haute couture silk evening gown in studio strobe lighting",
    aspect_ratio="9:16",
    quality_mode="HIGH",
    visual_dna={"dna_id": "vdna_couture_01", "palette": ["#000000", "#D4AF37"]}
)

response = gateway.generate_image(req)
print(f"Artifact ID: {response.artifact_id}")
print(f"Image URL: {response.image_url_or_bytes}")
print(f"SHA-256 Lineage Hash: {response.lineage.request_hash}")
```

### 2. Generating a 360° Digital Turntable Motion Video
```python
from src.visual_model_gateway import (
    VisualModelGateway,
    VideoGenerationRequest,
    CameraMotion
)

gateway = VisualModelGateway.create_default()

vid_req = VideoGenerationRequest(
    prompt="360 rotation showcase of embroidered bomber jacket with satin sheen",
    aspect_ratio="16:9",
    camera_motion=CameraMotion.ORBIT_360,
    duration_sec=5.0,
    fps=30,
    motion_strength=1.1,
    source_image_url="https://sandbox.vyren.internal/assets/hero_jacket.png"
)

vid_response = gateway.generate_video(vid_req)
print(f"Video URL: {vid_response.video_url}")
print(f"Motion Type: {vid_response.camera_motion.value}")
```

---

## 5. Waterfall Failover Protocol

When the primary Higgsfield endpoint is unreachable (e.g. rate limits `429`, server timeouts `504`, or offline local instances):
1. `HiggsfieldVisualProvider` catches the exception.
2. An error log is recorded to server telemetry.
3. The request is immediately and seamlessly delegated to `self.fallback_provider` (e.g. `SandboxVisualProvider` or `GeminiVisualProvider`).
4. The generated artifact is tagged with the actual executing model name in `VisualLineage` and recorded in the append-only [`VisualLedger`](file:///c:/Users/User/OneDrive/Desktop/Fashion%20Knowldge%20Wiki/Visual-Intelligence/product/backend/src/visual_model_gateway/visual_ledger.py).

---

## 6. Environment Configuration

Add the following keys to your `.env` configuration:

```bash
# ── Higgsfield Open API (Unified Creative & Video Motion Engine) ───────────────
HIGGSFIELD_API_BASE_URL=http://localhost:8080/v1
HIGGSFIELD_API_KEY=hf_open_local_key
HIGGSFIELD_DEFAULT_MOTION_BUCKET_ID=127
HIGGSFIELD_TIMEOUT_SECONDS=60
```

---

## 7. Verification & Automated Testing

Run the dedicated test suite:
```powershell
python -m pytest Visual-Intelligence/product/backend/tests/phase20/test_higgsfield_integration.py -v
```

Run full regression verification:
```powershell
python Visual-Intelligence/product/backend/run_phase31_room_tests.py
```
*All 110 tests must pass (100% pass rate).*
