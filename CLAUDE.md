# Book to Comic Generation

## Status
**Phase:** Active development — Chapter 1 complete, hybrid art mode working
**Current:** 12 comic pages produced (3 prologue + 9 chapter 1). DrawThings SDXL generating AI backgrounds, integrated as CSS background-image with SVG/CSS speech bubbles overlaid. All beat maps complete (prologue + ch1-4).
**Next:** Chapter 2 pages → Chapter 3 → Chapter 4 → Assembly → Test with a second book
**GitHub:** https://github.com/terriblyoffendedmarketer-stack/book-to-comic-generation

## Roadmap
- [x] Phase 1: EPUB extraction script (Python 3, no deps)
- [x] Phase 2: SVG character template system (body types, expressions, poses)
- [x] Phase 3: HTML page template (panels, speech bubbles, narrator boxes)
- [x] Phase 4: Prototype — Roadside Picnic prologue + Chapter 1 pages
- [x] Phase 5: Skill file — comprehensive multi-pass pipeline
- [x] Phase 6: Dual art mode support (SVG / DrawThings / Hybrid)
- [~] Phase 7: Full Roadside Picnic adaptation as test case
- [ ] Phase 8: Test with a second book to validate generality

## File Map
- `SKILL.md` — The skill file. Install to `~/.claude/skills/book-to-comic/`
- `README.md` — Project overview and getting started
- `scripts/extract-epub.py` — Extracts EPUB to one .txt per chapter
- `templates/page-template.html` — Starter HTML for comic pages (CSS, panel grid, bubbles)
- `templates/character-templates.svg` — SVG body types, 7 expressions, 6 accessories
- `examples/roadside-picnic-comic/` — Full Chapter 1 adaptation (12 pages)
  - `planning/01-structure-map.md` — Full book structure analysis
  - `planning/02-beats-prologue.md` through `02-beats-ch4.md` — All beat maps complete
  - `planning/03-character-bible.md` — 8 characters with visual design notes
  - `planning/05-script-prologue.md` — Panel script for 3-page prologue
  - `pages/page-00a..c-prologue.html` — 3 prologue pages (Pilman interview)
  - `pages/page-01..09.html` — 9 Chapter 1 pages (full chapter)
  - `assets/` — 9 DrawThings AI-generated PNG backgrounds
  - `characters/` — Character reference SVGs
  - `reader.html` — Combined reader with navigation (12 pages)
  - `REVISION-NOTES.md` — Feedback and lessons from prototype review

## Setup
```bash
# No dependencies needed for core pipeline
python3 scripts/extract-epub.py <epub-path> [output-dir]

# For DrawThings art mode: need DrawThings app + MCP server running
# DrawThings API server: HTTP protocol, port 7860, IP 0.0.0.0
```

## Tech
- Python 3 stdlib for EPUB extraction
- Pure HTML/CSS for comic pages (Google Fonts: Bangers + Patrick Hand)
- SVG for deterministic character art
- DrawThings MCP for AI-generated backgrounds (SDXL Base v1.0, 8-bit)
- Hybrid art: AI PNG backgrounds via CSS `background-image` + SVG characters/bubbles overlaid
- No build tools, no npm, no frameworks

## DrawThings Seeds (for reproducibility)
- 42: radio studio | 101: pilman radiant | 202: stalker fence
- 303: harmont aerial | 404: zone shimmer | 505: pilman radiant v2
- 606: zone entrance | 707: borscht bar | 808: garage silver web
