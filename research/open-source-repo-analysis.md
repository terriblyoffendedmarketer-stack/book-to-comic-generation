# Open-Source Book-to-Comic Repo Analysis
# Date: 2026-09-21
# Purpose: Deep-dive into 4 GitHub repos for reusable techniques, patterns, and approaches

## Summary

Analyzed 4 repos by cloning and reading actual source code (not just READMEs).
One repo is a goldmine (codex-novel-to-comic-studio), one has useful tricks (make-comics),
one has a small insight (comics_generator), and one is a dead end (Book-To-Comics).

---

## 1. codex-novel-to-comic-studio (lhfer) — GOLDMINE

**Repo:** https://github.com/lhfer/codex-novel-to-comic-studio
**What it is:** A Codex (OpenAI) skill for EPUB/TXT → manga/comic production. 12-stage pipeline.
**Language:** Python 100%

### What They Solve Well

#### A. Visual Bible System (Anti-Drift)
Three tiers of consistency control:
- **Style Bible** (`visual-bible/style.md`): global art direction with hex colors, lighting rules,
  and a **reusable "image2 prompt phrase"** prepended to every generation prompt
- **Character Reference Cards** (`visual-bible/characters/{id}/reference-card.png`): face, full body,
  2-3 expressions, default outfit, color notes — all in one image
- **Reference Lock in Director Briefs**: every brief must cite exact paths to approved reference cards.
  The validator (`check_director_briefs.py`) FAILS if `visual-bible/characters/` doesn't appear

Key concept: **invariants vs variables** per character
- Invariants: face shape, hair, eye color, body type, scars, signature props, silhouette
- Variables: emotion, lighting, pose, temporary damage, wardrobe

**Bible Feedback Loop:** after completing a chapter, strong poses/settings from generated pages
get promoted back into `visual-bible/` so later chapters become more consistent.

#### B. page-script.json Format
Per-script tracking:
- `critical_information` — list of plot-critical items with source_span references
- `page_count_policy` — must be `story_first_variable` (no fixed page count)

Per-page tracking:
- `reader_state`: `known_before`, `new_information`, `open_question`
- `non_omittable_causality` — things that CANNOT be cut
- `source_lines` with `kept` and `adapted` sublists
- Per-panel: `story_function`, `visual_brief`, `dialogue`, `captions`, `sfx` (each with `purpose`)

The validator checks that every `critical_information` ID is covered by at least one page —
**nothing from the source gets silently dropped.**

#### C. Filesystem-Sentinel Pipeline Orchestration
State tracked entirely through file presence + mtime:
- Sentinel files: `PAGE_SCRIPT_APPROVED`, `STORYBOARD_APPROVED`, `APPROVED`
- Staleness: if page-script mtime > storyboard mtime, storyboard must regenerate
- Per-chapter gates checked in order: plan → approved → script → approved → storyboard → approved → briefs → pages → qc → approved
- Makes pipeline **resumable across sessions** and prevents stale downstream artifacts

#### D. QC Loop
Pre-generation structural validation:
- `check_page_story_plan.py` — required fields, sequential numbering
- `check_page_script.py` — critical information coverage, source traceability
- `check_director_briefs.py` — brief completeness, reference locks, anti-grid validation

Post-generation image QC (`qc.py`):
- Image existence (blocking), dimensions (high severity)
- Art coverage: `_non_white_bbox_coverage()` — non-white bounding box as fraction of page
  (medium severity if under 45%)
- Text presence check

Four-layer review: story faithfulness, continuity, image quality, comic readability.
Severity levels: `low`, `medium`, `high`, `blocking`. Can't approve while high/blocking open.

#### E. Anti-Vague Validation
`_looks_like_vague_summary()` rejects story_jobs like "introduce everything quickly",
"tell the story", "show what happens", or "lore montage". Forces specificity.

### What We Should Adopt

| Technique | How to Apply |
|-----------|-------------|
| Reusable style phrase for all prompts | Create a DrawThings "style preamble" that prefixes every background prompt |
| Invariant/variable separation per character | Already doing this implicitly with SVG defs; formalize it in inventory |
| Bible feedback loop | After generating backgrounds, promote good ones as reference for later chapters |
| page-script.json format | Adopt for our Script step (Step 6) — especially `critical_information` tracking and `reader_state` |
| Filesystem-sentinel state tracking | Add to our pipeline — marker files + mtime checks for resumability |
| Art coverage check | Run on DrawThings outputs — reject backgrounds that are mostly white/empty |
| Anti-vague validation | Add to beat-extraction step — reject vague scene descriptions |
| "Do not cover" zones in briefs | Maps directly to our zone-based layout (speech zone / art zone) |

---

## 2. make-comics (nutlope) — USEFUL TRICKS

**Repo:** https://github.com/nutlope/make-comics
**What it is:** Next.js SaaS for creating comics from prompts. Uses Google Flash Image 2.5 + Qwen3.
**Language:** TypeScript 97%

### What They Solve Well

#### A. Panel Generation Prompts
`lib/prompt.ts` (`buildComicPrompt()`) specifies a fixed 5-panel layout as text:
```
[Panel 1] [Panel 2] -- top row, 2 equal panels
[    Panel 3      ] -- middle row, 1 large cinematic hero panel
[Panel 4] [Panel 5] -- bottom row, 2 equal panels
```
Includes: "Vary camera angles: close-up, medium shot, wide establishing shot"
and "Natural visual flow: left-to-right, top-to-bottom reading order."

The entire page (panels + borders + speech bubbles + text) is generated as ONE image.

#### B. Character Consistency via Reference Images
`app/api/generate-comic/route.ts`:
- User-uploaded character photos (max 2) stored as S3 URLs
- **Previous page's generated image** added to `referenceImages` array
- Emphatic prompt language: "FACE MATCHING: The character's face must be IDENTICAL
  to the reference image - same eyes, nose, mouth, hair, facial structure"
- Temperature set to 0.1 for tight adherence

This uses Gemini Flash's `reference_images` API parameter — not available in SD/DrawThings directly.
But the **pattern** (feed previous output as reference for next generation) translates to img2img.

#### C. Style Prompt Strings
`constants.ts` has reusable style descriptions per genre:
- Noir: "film noir style, high contrast black and white, deep dramatic shadows, 1940s detective aesthetic, heavy bold inking, moody atmospheric lighting"
- And similar for other styles

These are directly usable as DrawThings prompt fragments.

#### D. CSS Post-Processing for Visual Unity
On the displayed comic image:
- `opacity-90 grayscale-10 contrast-110`
- Plus a scan-line overlay effect

Cheap trick that unifies inconsistent generations into a cohesive visual style.

### What We Should Adopt

| Technique | How to Apply |
|-----------|-------------|
| Style prompt strings | Adapt for DrawThings — create a library of genre-specific prompt fragments |
| CSS post-processing filters | Add to our HTML comic viewer — slight contrast + desaturation unifies mixed media |
| Previous-page-as-reference pattern | For DrawThings: use img2img with previous panel as init image for setting continuity |
| 2-1-2 panel layout concept | Add as a composition type in our layout system |
| Emphatic face-matching language | Adapt for DrawThings prompts when generating scenes with silhouettes/figures |

---

## 3. comics_generator (Aschen) — SMALL INSIGHT

**Repo:** https://github.com/Aschen/comics_generator
**What it is:** Python script — LLM splits scenario into 6 panels, Stability API generates images, merges into strip.
**Language:** Python 100%

### How It Works (Simply)

1. You write a scenario: "Francis is a knight. He fights a dragon. Princess is angry."
2. GPT-4 (via LangChain) splits it into exactly 6 panels
3. Each panel gets: a **description** (comma-separated visual keywords) + **text** (dialogue)
4. For each panel: Stability SDXL generates an image from the description
5. PIL adds text as a caption strip below each panel image
6. All 6 panels merge into a 2-column × 3-row grid

### The One Useful Technique

The LLM prompt forces **comma-separated visual descriptors per panel** (not prose sentences)
and requires **full physical descriptions repeated in every panel** (since image gen has no
cross-panel memory):

```
description: 2 guys, a blond hair guy wearing glasses, a dark hair guy wearing hat,
sitting at the office, with computers
```

NOT: "Francis and Madeline discuss their plan" (which SD can't render consistently).

Style control is purely a prompt suffix: `"american comic, colored"` or `"manga"`.
A single random seed is shared across all 6 panels (naive, doesn't actually work well).

### What We Should Adopt

| Technique | How to Apply |
|-----------|-------------|
| Force comma-separated visual descriptors (not prose) | Use this format for DrawThings prompts — keyword lists, not sentences |
| Repeat full physical descriptions per panel | When our DrawThings prompts include silhouettes, always re-describe them |

---

## 4. Book-To-Comics (KeithLin724) — DEAD END

**Repo:** https://github.com/KeithLin724/Book-To-Comics
**What it is:** FastAPI + Docker chatbot with bolted-on SD image generation.
**Language:** Python 80%

### Honest Assessment

Despite the name, this has **no book-to-comic pipeline at all.** It's a generic chatbot where
if you type "generate image [description]", it sends that raw text to Stable Diffusion.

- No text analysis, scene decomposition, or panel scripting
- GPT used only as generic chatbot (no system prompt, no comic-specific instructions)
- SD uses all defaults (no negative prompts, no guidance scale, no seed control)
- No panel layout, no speech bubbles, no composition
- No character consistency of any kind

The only marginally interesting pattern is the Redis task queue for async image generation
with polling — standard infrastructure, not comic-generation technique.

**Nothing reusable for our pipeline.**

---

## Combined Adoption Plan

### HIGH PRIORITY (adopt now)

1. **page-script.json format** from codex-novel-to-comic-studio
   - `critical_information` tracking prevents dropping plot points
   - `reader_state` (known/new/open_question) improves narrative flow
   - Validation that every critical item is covered by at least one page

2. **Filesystem-sentinel pipeline state** from codex-novel-to-comic-studio
   - Marker files (`APPROVED`, `PAGE_SCRIPT_APPROVED`) as gates
   - Mtime-based staleness detection
   - Makes our pipeline resumable across sessions

3. **CSS post-processing filters** from make-comics
   - `contrast(1.1) grayscale(0.1) opacity(0.9)` + scan-line overlay
   - Unifies mixed media (SVG characters + DrawThings backgrounds) into cohesive look

### MEDIUM PRIORITY (adopt during refinement)

4. **DrawThings style preamble** — combine techniques from codex-novel-to-comic-studio
   (reusable style phrase) and make-comics (genre prompt strings) and comics_generator
   (comma-separated descriptors, not prose)

5. **Anti-vague validation** from codex-novel-to-comic-studio
   - Reject vague beat descriptions before they reach page scripting

6. **Art coverage QC check** from codex-novel-to-comic-studio
   - `non_white_bbox_coverage()` on DrawThings outputs
   - Auto-reject backgrounds that are mostly empty/white

7. **Bible feedback loop** from codex-novel-to-comic-studio
   - Promote good DrawThings outputs as reference for later chapters

### LOW PRIORITY (nice to have)

8. **Previous-page-as-reference** from make-comics
   - img2img with previous background for setting continuity across pages

9. **2-1-2 panel composition** from make-comics
   - Add as a layout type alongside our existing composition types

10. **Invariant/variable formalization** from codex-novel-to-comic-studio
    - Already implicit in our SVG defs; could make explicit in inventory format
