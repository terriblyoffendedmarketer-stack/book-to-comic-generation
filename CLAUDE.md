# Book to Comic Generation

## Status
**Phase:** Character redesign COMPLETE — ready for template system + proof-of-concept
**Current:** All 20 characters designed as modular SVG sheets (97 total expressions). Open-source repo analysis done (4 repos, adoption plan written).
**Blocking:** Nothing — Steps 2-3 complete.
**Next:** Step 4 (background planning) → Step 5 (beat extraction) → one chapter proof-of-concept
**GitHub:** https://github.com/terriblyoffendedmarketer-stack/book-to-comic-generation

## CRITICAL: Read Before Working
1. **Read `MISTAKES.md` first** — 10 documented mistakes with fixes. Do not repeat them.
2. **Read `APPROACH.md`** — the refined 10-step pipeline and all design decisions.
3. **Read `research/comic-generation-landscape.md`** — industry research informing the approach.
4. **Read `research/open-source-repo-analysis.md`** — deep-dive into 4 GitHub repos with reusable techniques.
5. Do NOT start producing pages until the approach is validated on one chapter.

## Roadmap (revised)
- [x] Phase 1: EPUB extraction script (Python 3, no deps)
- [x] Phase 2: Prototype SVG characters + HTML pages (12 pages — flawed, lessons learned)
- [x] Phase 3: Industry research (Dashtoon, TaleAtelier, ComicsMaker.ai, open source repos)
- [x] Phase 4: Mistakes documented + refined approach designed
- [x] Phase 5: Full book inventory (Step 2 of pipeline — characters, expressions, settings)
- [x] Phase 6: Data-driven character redesign (97 expressions across 20 characters, 12 SVG files)
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
- `research/open-source-repo-analysis.md` — **Deep-dive into 4 open-source repos: reusable techniques, adoption plan**
- `templates/page-template.html` — Old HTML template (to be replaced)
- `templates/character-templates.svg` — Old SVG templates (to be replaced)
- `examples/roadside-picnic-comic/` — Prototype pages (flawed but instructive)
  - `planning/00-book-inventory.md` — **Full book inventory: 20 characters, 97 expressions, all settings/pairings/scene types**
  - `planning/` — Structure map, beat maps (ch1-4), character bible, scripts
  - `pages/` — 12 prototype pages (prologue + chapter 1)
  - `assets/` — 9 DrawThings AI-generated backgrounds (some usable, some not)
  - `characters/` — **12 modular SVG character sheets (97 expressions total)**
    - `red-schuhart.svg` (20 expr), `noonan.svg` (10), `arthur-burbridge.svg` (9)
    - `guta-schuhart.svg` (8), `kirill-panov.svg` (5), `burbridge.svg` (5), `pilman.svg` (5)
    - `monkey.svg` (4), `dina-burbridge.svg` (4), `tender.svg` (4), `throaty.svg` (4)
    - `minor-characters.svg` (19 — Herzog, Ernest, Gutalin, Quarterblad, Bones, Hamster, Lemchen, Mosul, Schuhart Sr)
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
