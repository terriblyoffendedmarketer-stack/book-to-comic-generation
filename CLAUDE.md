# Book to Comic Generation

## Status
**Phase:** Active development — skill file complete, prototype tested with Roadside Picnic
**Current:** Multi-pass pipeline with dual art mode support (SVG + DrawThings + Hybrid)
**Next:** Continue testing with Roadside Picnic adaptation, refine DrawThings integration

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
- `examples/roadside-picnic-comic/` — Prototype adaptation (4 pages produced)
  - `pages/` — HTML comic pages
  - `characters/` — Character reference SVGs
  - `reader.html` — Combined reader with navigation
  - `REVISION-NOTES.md` — Feedback and lessons from prototype review

## Setup
```bash
# No dependencies needed for core pipeline
python3 scripts/extract-epub.py <epub-path> [output-dir]

# For DrawThings art mode: need DrawThings app + MCP server running
```

## Tech
- Python 3 stdlib for EPUB extraction
- Pure HTML/CSS for comic pages (Google Fonts: Bangers + Patrick Hand)
- SVG for deterministic character art
- DrawThings MCP for AI-generated panels (optional)
- No build tools, no npm, no frameworks
