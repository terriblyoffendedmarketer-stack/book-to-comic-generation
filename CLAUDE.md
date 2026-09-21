# Book to Comic Generation

## Status
**Phase:** Book inventory complete — ready for character redesign
**Current:** Full book inventory done (20 characters, 97 expressions, all settings/pairings/scene types catalogued).
12 prototype pages exist (3 prologue + 9 ch1) but approach has known flaws.
**Blocking:** Nothing — Step 2 complete.
**Next:** Step 3 (data-driven character redesign) → Step 4 (background planning) → one chapter proof-of-concept
**GitHub:** https://github.com/terriblyoffendedmarketer-stack/book-to-comic-generation

## CRITICAL: Read Before Working
1. **Read `MISTAKES.md` first** — 10 documented mistakes with fixes. Do not repeat them.
2. **Read `APPROACH.md`** — the refined 10-step pipeline and all design decisions.
3. **Read `research/comic-generation-landscape.md`** — industry research informing the approach.
4. Do NOT start producing pages until the approach is validated on one chapter.

## Roadmap (revised)
- [x] Phase 1: EPUB extraction script (Python 3, no deps)
- [x] Phase 2: Prototype SVG characters + HTML pages (12 pages — flawed, lessons learned)
- [x] Phase 3: Industry research (Dashtoon, TaleAtelier, ComicsMaker.ai, open source tools)
- [x] Phase 4: Mistakes documented + refined approach designed
- [x] Phase 5: Full book inventory (Step 2 of pipeline — characters, expressions, settings)
- [ ] Phase 6: Data-driven character redesign (only expressions found in text)
- [ ] Phase 7: New template system (zone-based layout, composition types, reuse patterns)
- [ ] Phase 8: One chapter proof-of-concept with new approach
- [ ] Phase 9: Full Roadside Picnic adaptation
- [ ] Phase 10: Test with a second book to validate generality

## File Map
- `APPROACH.md` — **THE approach document. The 10-step pipeline, DrawThings rules, style guide.**
- `MISTAKES.md` — **10 documented mistakes. Read before any work.**
- `SKILL.md` — The skill file (needs update to match new approach)
- `README.md` — Project overview
- `scripts/extract-epub.py` — Extracts EPUB to one .txt per chapter
- `research/comic-generation-landscape.md` — Industry research on AI comic tools
- `templates/page-template.html` — Old HTML template (to be replaced)
- `templates/character-templates.svg` — Old SVG templates (to be replaced)
- `examples/roadside-picnic-comic/` — Prototype pages (flawed but instructive)
  - `planning/00-book-inventory.md` — **Full book inventory: 20 characters, 97 expressions, all settings/pairings/scene types**
  - `planning/` — Structure map, beat maps (ch1-4), character bible, scripts
  - `pages/` — 12 prototype pages (prologue + chapter 1)
  - `assets/` — 9 DrawThings AI-generated backgrounds (some usable, some not)
  - `characters/` — Old character SVGs (to be redesigned)
  - `reader.html` — Combined reader
  - `REVISION-NOTES.md` — Early feedback

## Key Decisions (settled)
- **SVG for all characters** — deterministic, zero drift, infinitely reusable
- **DrawThings for SIMPLE ambient backgrounds ONLY** — never for spatial/directional scenes
- **Zone-based panel layout** — speech zone (top) + art zone (bottom), no overlap possible
- **Data-driven expressions** — analyze book first, create only what's needed per character
- **Dialogue scene reuse** — same composition across panels, only bubbles change
- **Simplicity is fine** — Persepolis/XKCD style, strong identifiers, not manga-quality
- **Max 6 panels/page, max 3 bubbles/panel**
- **No background > bad background** — solid color for dialogue, gradient for mood

## Setup
```bash
python3 scripts/extract-epub.py <epub-path> [output-dir]
# DrawThings: HTTP protocol, port 7860, SDXL Base v1.0 (8-bit)
```

## Tech
- Python 3 stdlib for EPUB extraction
- Pure HTML/CSS for comic pages (Google Fonts: Bangers + Patrick Hand)
- SVG for characters (deterministic, templatizable)
- DrawThings MCP for simple backgrounds only (SDXL Base v1.0, 8-bit, seed-pinned)
- Future: Claude API (Messages API) for batch pipeline execution
