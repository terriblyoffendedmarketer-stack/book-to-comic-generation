# Book to Comic Generation

## Status
**Phase:** Parametric character system — designing component library
**Current:** DrawThings AI generation tested and FAILED (3 attempts, prompt adherence too low). Pivoted to parametric SVG assembly approach after deep research. Architecture designed, component library spec written.
**Blocking:** Component library needs to be built (~60-80 core SVG components)
**Next:** Build core component library → test-assemble 2 characters → validate quality
**GitHub:** https://github.com/terriblyoffendedmarketer-stack/book-to-comic-generation

## CRITICAL: Read Before Working
1. **Read `MISTAKES.md` first** — 11 documented mistakes with fixes. Do not repeat them.
2. **Read `APPROACH.md`** — the 10-step pipeline with parametric character system.
3. **Read `research/character-generation-solution.md`** — why AI generation fails + the solution.
4. **Read `research/open-source-repo-analysis.md`** — 4 repos with reusable techniques.
5. **Read `research/comic-generation-landscape.md`** — industry research.
6. Do NOT start producing pages until approach is validated on one chapter.

## Roadmap (revised 2026-09-29)
- [x] Phase 1: EPUB extraction script (Python 3, no deps)
- [x] Phase 2: Prototype SVG characters + HTML pages (12 pages — flawed, lessons learned)
- [x] Phase 3: Industry research (Dashtoon, TaleAtelier, ComicsMaker.ai, open source repos)
- [x] Phase 4: Mistakes documented + refined approach designed
- [x] Phase 5: Full book inventory (Step 2 — characters, expressions, settings)
- [x] Phase 6: Data-driven character redesign (97 expressions, 20 characters, 12 SVGs)
- [x] Phase 7: DrawThings AI generation test — FAILED, pivoted to parametric
  - [x] 7a: Tested SDXL pipeline (3 attempts, proved unreliable for unusual features)
  - [x] 7b: VTracer vectorization pipeline working (Python 3.12 bindings)
  - [x] 7c: Deep research → designed parametric SVG assembly approach
- [~] Phase 8: Parametric character system
  - [ ] 8a: Build core component library (~60-80 SVGs: bodies, heads, hair, eyes, clothing)
  - [ ] 8b: Build differentiation algorithm (similar-character detection + color coding)
  - [ ] 8c: Test-assemble Red Schuhart + Monkey from components (the easy + hard case)
  - [ ] 8d: Silhouette test — are all 20 characters distinguishable as black shapes?
  - [ ] 8e: Optional: test AI enhancement layer (DrawThings img2img, low denoising)
- [ ] Phase 9: Template system (zone-based layout, composition types, reuse patterns)
- [ ] Phase 10: One chapter proof-of-concept with new approach
- [ ] Phase 11: Full Roadside Picnic adaptation
- [ ] Phase 12: Test with a second book to validate generality

## File Map
- `APPROACH.md` — **THE approach document. 10-step pipeline, parametric character system.**
- `MISTAKES.md` — **11 documented mistakes. Read before any work.**
- `SKILL.md` — The skill file (needs update to match new approach)
- `README.md` — Project overview
- `scripts/extract-epub.py` — Extracts EPUB to one .txt per chapter
- `scripts/verify-character.py` — Claude vision verification of generated images
- `research/comic-generation-landscape.md` — Industry research on AI comic tools
- `research/open-source-repo-analysis.md` — Deep-dive: 4 repos, reusable techniques
- `research/character-generation-solution.md` — **Why AI gen fails + parametric solution**
- `research/svg-generation-tools.md` — SVG tool research
- `templates/page-template.html` — Old HTML template (to be replaced)
- `templates/character-templates.svg` — Old SVG templates (to be replaced)
- `components/` — **Component library (TO BE BUILT)**
  - `bodies/` — Body type base templates
  - `heads/` — Face shape outlines
  - `hair/` — Hairstyle paths (color via fill attribute)
  - `eyes/` — Eye types with expression variants
  - `mouths/` — Mouth shapes
  - `clothing/` — Outfit templates
  - `accessories/` — Glasses, hats, etc.
  - `special/` — Unusual features (fur, scales, etc.)
- `examples/roadside-picnic-comic/` — Prototype pages + test characters
  - `planning/00-book-inventory.md` — Full book inventory: 20 chars, 97 expr
  - `characters/` — 12 old SVG sheets + DrawThings test outputs
  - `pages/` — 12 prototype pages
  - `assets/` — 9 DrawThings AI-generated backgrounds

## Key Decisions (settled)
- **Parametric SVG for all characters** — component assembly, not AI generation
  - REASON: AI generation (SDXL) proved unreliable for unusual features (Mistake #10)
  - Component selection is deterministic: "golden hair" = pick golden hair SVG
  - Same component library = all characters in same art style = same universe
- **Bold outlined art style** — Persepolis/Tintin-inspired, thick black outlines, flat fills
- **DrawThings for SIMPLE ambient backgrounds ONLY** — never for characters
- **Zone-based panel layout** — speech zone (top) + art zone (bottom)
- **Data-driven expressions** — analyze book first, create only what's needed
- **Color coding for character identity** — each character gets unique primary color
- **Silhouette test** — every character must be recognizable as a solid black shape
- **Component library is extensible** — new books can add components on demand
- **Max 6 panels/page, max 3 bubbles/panel**
- **No background > bad background** — solid color for dialogue, gradient for mood

## Setup
```bash
python3 scripts/extract-epub.py <epub-path> [output-dir]
# DrawThings: HTTP protocol, port 7860, Flux model (for backgrounds/enhancement)
# VTracer: /opt/homebrew/bin/python3.12 -c "import vtracer; ..."
```

## Tech
- Python 3 stdlib for EPUB extraction
- Pure HTML/CSS for comic pages (Google Fonts: Bangers + Patrick Hand)
- SVG component library for characters (deterministic, templatizable)
- DrawThings MCP for backgrounds + optional character enhancement (Flux, seed-pinned)
- VTracer (Python 3.12) for PNG→SVG vectorization when needed
- Future: Claude API (Messages API) for batch pipeline execution
