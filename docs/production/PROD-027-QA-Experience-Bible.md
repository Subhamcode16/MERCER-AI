# PROD-027 — QA Experience Bible
**Layer:** Production Intelligence (Translate)
**Agent:** `technical-author`
**Movement:** I — The Threshold

---

## 1. The "Feel" Test
Standard QA tests for crashes and functional bugs. Creative Studio QA tests for emotion.
- **Inertia Verification:** When scrolling violently and releasing the mouse/trackpad, does the camera stop instantly? If yes, **FAIL**. It must glide to a halt.
- **Pop-in Verification:** Does any geometry, texture, or font abruptly snap into existence? If yes, **FAIL**. Everything must fade or emerge from the fog.

## 2. The Lighting Audit
- Are there any blown-out pure white (`#FFFFFF`) pixels on the screen? If yes, **FAIL**. Light must always have a realistic falloff.
- Can you clearly see the boundaries of the 3D scene? If yes, **FAIL**. The fog must successfully mask the edges of the geometry into pure darkness.

## 3. The Audio Audit
- Does the audio play immediately on load? If yes, **FAIL**. Audio must fade in gently in response to user interaction to satisfy browser auto-play policies and maintain the "Silence before spectacle" principle.

## 4. The Typography Audit
- Is the text perfectly legible on all screen sizes despite the background? If no, **FAIL**. Adjust the text shadow or the background lighting attenuation.
