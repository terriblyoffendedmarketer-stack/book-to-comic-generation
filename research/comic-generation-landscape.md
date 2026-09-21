# AI Comic Generation — Industry Research
# Compiled 2026-09-18

## The Problem We're Solving
Convert any book into a comic using AI. Needs to be a repeatable, templatizable pipeline —
plug in a book, get a comic. Key challenges: character consistency, panel layout, speech
bubble placement, and art quality.

---

## Top Tools in the Space (2026)

### 1. Dashtoon (#1 ranked, 8.6/10)
- **Character consistency**: LoRA-based character locking. Train on 10-20 reference images.
- **Advanced approach**: Tuning-free ID-consistent character inpainting:
  - ArcFace for facial embeddings → Perceiver-Resampler → SDXL cross-attention
  - InternViT-300M for body/global features (hairstyle, body shape)
  - 133-point OpenPose keypoints for diverse poses
  - Zero-shot: processes unseen characters without per-subject training
  - Trained on 50K movie-extracted + 30K anime character IDs
- **Result**: "Very Low" drift across 20+ pages
- **Bubble handling**: Customizable text bubbles built into the page designer
- **Source**: https://insiders.dashtoon.com/a-road-towards-tuning-free-id-consistent-character-inpainting/

### 2. TaleAtelier (#2, 8.5/10)
- **Character consistency**: Job-scoped tracking across 4-400 pages within a single job
- **Story pipeline**: Beat generation + script input parsing → multi-page output
- **Key insight**: Consistency maintained within a generation "job" — no LoRA needed
- **Source**: https://taleatelier.com/best-ai-comic-generators

### 3. ComicsMaker.ai (#3, 8.1/10)
- **Pipeline**: Characters → Scenes → Pages → Publish
- **Character consistency**: Custom LoRA training (upload reference images)
- **Page Designer**: Precise control over panel size, spacing, orientation
- **Scene editing**: Refine with text prompts
- **Not open source** — proprietary SaaS
- **Source**: https://comicsmaker.ai

### 4. AI Comic Factory (open source, archived)
- **Stack**: Next.js + Tailwind, LLM (multiple backends) + SDXL
- **License**: Apache 2.0 (commercial-friendly)
- **Archived**: Oct 31, 2025 — no more updates
- **Source**: https://github.com/jbilcke-hf/ai-comic-factory

### 5. comic_book_project (open source, active)
- **Pipeline**: Prompt → Story Scenes → Image Prompts → Reference Characters → Comic Panels → Captions → Evaluation
- **Character consistency**: StoryDiffusion-style custom spatial attention + reference images as visual anchors
- **Models**: Qwen2.5-7B-Instruct (story) + SDXL/RealVisXL (images)
- **Evaluation**: CLIP similarity + GPT-2 perplexity
- **Caption rendering**: Automatic caption box overlay
- **Source**: https://github.com/AbdelrahmanMostafa12/comic_book_project

---

## Key Technical Findings

### Character Consistency — Three Approaches
1. **LoRA training** (Dashtoon, ComicsMaker.ai): Train a small model on 10-20 reference images. Most reliable but requires compute per character.
2. **Job-scoped tracking** (TaleAtelier): Keep character context locked within a generation session. No extra training.
3. **Reference anchoring** (StoryDiffusion, Midjourney --cref): Lock character descriptions + face embeddings. Face holds well, outfits drift.

**For our tool (SVG + DrawThings)**: We use deterministic SVG for characters — this is actually
the MOST consistent approach possible because SVG is code, not generated images. The key is
making the SVG characters detailed and recognizable enough. DrawThings handles backgrounds only.

### Panel Layout — Systematic Rules
- **Max 9 panels/page** (visual fatigue threshold)
- **Optimal dialogue pages**: 5-7 panels
- **Optimal action pages**: 3-4 panels
- **Splash page**: 1 per major narrative beat
- **Base grid**: Flexible 3-row system with variable panel widths per tier
- **Panel types map to narrative function**:
  - Close-up → emotional beats, reveals
  - Establishing/distant → scene openers
  - Silhouette → drama, mystery
  - Overlapping → simultaneous action
  - Diagonal → chaos, energy
  - Splash → major reveals
  - Inset → detail/reaction
- **Gutter width controls pacing**: standard=smooth, wide=pause, none=immediate

**Codifiable layout structure**:
```
Page = [Tier, Tier, Tier]
Tier = [Panel, Panel] where widths sum to 100%
Panel = { type, width%, speechBubbles[], artContent }
```

### Speech Bubble Placement — The Rules That Matter
1. **Reserve 15-20% of panel area for text** — don't overwhelm art
2. **Place along panel PERIPHERY** — never center-weighted over character faces
3. **Max 3 speech balloons per panel** — comprehension limit
4. **Z-pattern reading flow**: First speaker upper-left/upper-right, responses descend
5. **Tail points to speaker's mouth** — never crossing other tails
6. **First speaker on panel LEFT** (Western comics)
7. **10mm margin from page edges** for print safety
8. **Plan text footprint during layout phase** — not afterthought

**For our tool**: The zone-based approach (speech zone top, art zone bottom) already
solves the overlap problem. Enhancement: make the speech zone a flex container where
bubbles flow naturally in reading order. The art zone is then 100% art, no overlap possible.

### The Ideal Pipeline (synthesized from all sources)
```
1. BOOK EXTRACTION    → Text per chapter
2. STRUCTURE MAP      → Key scenes, characters, settings
3. CHARACTER DESIGN   → Reference sheets (SVG templates with key identifiers)
4. BEAT MAPPING       → Each scene → visual beats (what to show)
5. PANEL SCRIPTING    → Beat → panel type + dialogue + art description
6. LAYOUT GENERATION  → Flexible grid (3-row base, variable widths)
7. ART GENERATION     → Backgrounds (DrawThings) + Characters (SVG)
8. BUBBLE PLACEMENT   → Zone-based, Z-pattern flow, max 3 per panel
9. PAGE ASSEMBLY      → HTML/CSS page with all elements
10. REVIEW/ITERATE    → Quality check, consistency check
```

---

## What This Means for Our Approach

### What we're doing RIGHT:
- SVG characters = deterministic consistency (better than AI for this)
- DrawThings for backgrounds only = reproducible (seed-pinned)
- HTML/CSS for layout = infinitely templatizable
- Zone-based speech/art separation = solves the overlap problem structurally

### What we need to CHANGE:
1. **SVG characters need WAY more detail** — current ones are too simple. Need proper
   character reference sheets with 5+ expressions, multiple poses, key identifiers
   that read at comic scale.
2. **Panel layout needs to be systematic** — define panel types, use flexible 3-row grid,
   map narrative function to panel type automatically.
3. **Speech bubbles need the Z-pattern rule** — not just zone separation, but proper
   left→right, top→down reading flow within the zone.
4. **The pipeline needs to be codified** — each step should be a function in the skill
   file that takes structured input and produces structured output.
5. **Background generation needs to be strategic** — only generate for establishing shots
   and atmosphere panels. Dialogue-heavy panels use simple gradient/color backgrounds.

### Priority order:
1. Character SVG quality (the biggest gap)
2. Panel type system (template library)
3. Speech bubble flow rules
4. Pipeline codification
