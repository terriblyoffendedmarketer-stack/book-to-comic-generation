# How Comic Tools Actually Solve Poses + Expressiveness
# Date: 2026-09-29
# Based on: 8 web searches, Dashtoon technical blog, dev.to pipeline article, DrawThings wiki

## The Problem We're Solving
Parametric SVG assembly produces accurate but stiff characters — paper dolls.
Comics need characters in ACTION: running, cowering, gesturing, sitting.
Just building more pose variants still looks "assembled."
How do real tools make panels look drawn, not assembled?

## What The Industry Actually Does (2026)

### The Universal Pattern: Reference + Pose + Identity = Panel

Every serious comic tool uses the same three-signal architecture:

1. **Identity signal** — WHO is this character (face, hair, outfit)
   - Our component assembly handles this perfectly (100% accurate)
   
2. **Pose signal** — WHAT is the character doing (body position, gesture)
   - ControlNet OpenPose: stick figure skeleton → AI draws a body in that pose
   - 133 keypoints (face + body + hands) in modern systems (Dashtoon uses RTMPose-l)
   
3. **Style signal** — HOW should it look (art style, line weight, color palette)
   - LoRA, style prompts, or IP-Adapter for consistent aesthetic

The AI model (SDXL, Flux, etc.) receives all three signals and generates a
panel that is faithful to identity, pose, AND style simultaneously.

### Dashtoon's Pipeline (most relevant to us)
Source: https://insiders.dashtoon.com/a-road-towards-tuning-free-id-consistent-character-inpainting/

1. User creates a reference image per character (their character creator or upload)
2. For each panel, system determines the required pose
3. RTMPose extracts 133 keypoints from a target pose image
4. ArcFace extracts facial identity embeddings from reference
5. InternViT extracts body/clothing features from reference
6. "Pose-IdentityNet" (modified ControlNet) combines pose + identity
7. SDXL inpaints the character region maintaining identity in new pose
8. Per-panel editing suite for touch-ups

Key insight: they SEPARATE identity from pose. Identity comes from the reference
image (our assembled SVG). Pose comes from a skeleton. The AI model combines them.

### Training-Free Pipeline (dev.to article)
Source: https://dev.to/qcrao/character-consistency-in-ai-comics-3-tricks-that-beat-lora-training-for-me-3ad7

Uses Flux Kontext with three techniques:
1. IP-Adapter at scale=0.65 — reference image → identity preservation
2. Prompt template locking — fixed attribute slots, variable action/scene
3. ControlNet pose + layer-specific token injection

Results: 85% panel-to-panel consistency, zero training time per character.
Single RTX 4090. This is achievable on our Mac with DrawThings.

### DrawThings Capabilities (confirmed available locally)
Source: https://wiki.drawthings.ai/wiki/Flux_Kontext

DrawThings supports ALL the pieces we need:
- **Flux Kontext** — 12B parameter model, identity-preserving edits
- **ControlNet** with Pose input type — skeleton → character in pose
- **IP-Adapter** (FaceID Plus) — reference image identity injection
- **Moodboard** — load reference images for style/character consistency
- **Image-to-image** — transform existing images while preserving structure

## The Hybrid Pipeline For Us

### Our SVG assembly becomes the REFERENCE IMAGE — not the final art.

This changes everything. Instead of trying to make SVGs look like comic panels:

```
STEP 1: ASSEMBLE (what we built)
  Book description → component selection → SVG character reference
  100% accurate traits. Stiff pose. That's fine — it's a REFERENCE.

STEP 2: POSE (new — simple stick figures)
  For each panel's action, provide a pose skeleton.
  Can be: hand-drawn stick figure, OpenPose from a photo, or
  a simple SVG skeleton Claude draws for the specific action.
  "Character cowering" = bent stick figure with raised arms.

STEP 3: RENDER (DrawThings Flux Kontext + ControlNet)
  Input: character reference SVG (identity) + pose skeleton (action)
         + style prompt ("bold outlined comic, Persepolis style, flat colors")
  Model: Flux Kontext with ControlNet Pose
  Output: Character in the correct pose, with correct identity, in comic style
  
  The AI's job is now MUCH simpler than before:
  - Identity: given by reference (not hallucinated from text)
  - Pose: given by skeleton (not hallucinated from text)
  - Style: given by style prompt + IP-Adapter
  - Only creative work: connecting these signals into a natural drawing

STEP 4: VERIFY + FALLBACK
  Claude vision checks: does the panel match identity?
  If yes → use it
  If no → try again with higher IP-Adapter weight, or
          fall back to the assembled SVG (accurate but stiff)
```

### Why This Is Different From Our Failed SDXL Attempts

Before: "Draw a character with golden hair, no-white eyes, fur on cheeks"
→ Model ignores unusual features (training distribution gravity)

Now: "Here is a PICTURE of the character. Put them in THIS pose."
→ Model copies what it sees. No interpretation of text needed for identity.
→ Unusual features are IN the reference image. Model reproduces them.

The key shift: we moved identity from TEXT (unreliable) to IMAGE (reliable).
The assembled SVG IS the identity image. DrawThings just animates it.

## Pose Skeleton Sources

For each panel, we need a stick figure showing the pose. Options:

1. **Claude draws simple SVG skeletons** — 18 joints as circles+lines.
   Fast, programmatic, works for common poses. Claude can write:
   "standing with left arm pointing forward, right arm at side, slight lean"
   as positioned circles and lines.

2. **Pre-made pose library** — collect ~20 common comic poses as skeletons.
   Standing, sitting, walking, running, cowering, pointing, fighting, etc.
   One-time effort, reusable across all books.

3. **OpenPose from stock photos** — find a photo of someone in the pose,
   run OpenPose preprocessor (DrawThings has this), get skeleton automatically.
   Most flexible but requires finding reference photos.

4. **AI-generated poses** — describe the action in text, generate a generic
   figure, extract pose. Circular but works for unusual poses.

Recommendation: Start with option 2 (pre-made library of ~15 common poses)
+ option 1 (Claude draws custom skeletons for unusual actions).

## DrawThings API Integration Plan

The DrawThings MCP tools we already have:
- generate_image: text-to-image (used for backgrounds)
- transform_image: image-to-image with denoising (used for enhancement)

What we need to figure out:
- How to pass ControlNet pose input via the API
- How to use Moodboard/IP-Adapter via the API  
- Whether Flux Kontext is accessible via the HTTP API

This needs testing. The MCP tools may expose these features, or we may
need to use the DrawThings GUI for the initial character renders and only
use the API for batch production.

## Scaling Analysis

Per character: 1 SVG assembly (seconds) + 1 DrawThings render (30-60 sec)
Per panel: 1 pose skeleton + 1 DrawThings render (30-60 sec)
Per page (5 panels avg): ~3-5 min of DrawThings time
Per chapter (12 pages avg): ~36-60 min of DrawThings time
Full book (20 chapters): ~12-20 hours of DrawThings time

This fits within 2 five-hour Claude Pro sessions if we batch efficiently
and reuse compositions for dialogue scenes (same setup, different bubbles).

## Sources
- Dashtoon ID-consistent inpainting: https://insiders.dashtoon.com/a-road-towards-tuning-free-id-consistent-character-inpainting/
- Training-free consistency tricks: https://dev.to/qcrao/character-consistency-in-ai-comics-3-tricks-that-beat-lora-training-for-me-3ad7
- Flux Kontext in DrawThings: https://wiki.drawthings.ai/wiki/Flux_Kontext
- DrawThings ControlNet basics: https://wiki.drawthings.ai/wiki/ControlNet_Basics
- Flux Kontext consistency tips: https://selfielab.me/blog/flux1-kontext-character-consistency-tips-20260216
- AI comic panel generation guide: https://www.jenova.ai/en/resources/ai-comic-panel-creator
- ControlNet pose guide: https://www.apatero.com/blog/comfyui-controlnet-pose-guide-2026
- Flux Kontext review: https://www.flixly.ai/blog/flux-kontext-review-character-consistency-2026
