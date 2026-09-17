# Roadside Picnic — Comic Adaptation

## Status
**Phase:** Proof of concept — Chapter 1 in progress
**Current:** 4 pages complete (Prologue + 3 pages of Chapter 1)
**Next:** Pages 4-8 covering the Zone expedition (mosquito mange, the garage, silver web), then the Borscht bar and Kirill's death

## What This Is
A comic adaptation of "Roadside Picnic" by Arkady & Boris Strugatsky, using simple SVG character art (Calvin & Hobbes level) with hand-drawn style. Characters are deterministic SVG — same shapes every time, no AI drift. Built as HTML pages with inline SVG.

## Characters Designed
- **Red Schuhart** — red hair, green jacket, stocky, squinting eyes, cigarette
- **Kirill Panov** — glasses, lab coat, thin, earnest
- **Tender** — heavyset, round, balding, nervous/sweaty
- **Captain Herzog** — military uniform, pipe, stern
- **Ernest** — bartender, mustache, shrewd eyes, wiping glass
- **Dick Noonan** — small, round, pink, friendly, red tie
- **Gutalin** — huge, dark skin, intense, long arms
- **Dr. Pilman** — older, grey hair, composed (prologue only)

## Pages Complete
1. `page-00-prologue.html` — Radio interview with Pilman, Visitation explanation, Zone setup
2. `page-01.html` — Repository scene: Red offers Kirill the full empty, Kirill comes alive
3. `page-02.html` — Herzog's warning, Red can't go, changes mind seeing Kirill's face
4. `page-03.html` — Suiting up, walking to Zone entrance, entering the Zone (big atmospheric panel)

## Pages Remaining (Chapter 1)
5. Page 4 — Tender's babbling, the shimmering thing on the dump, mosquito mange
6. Page 5 — Nuts and bolts pathfinding, the garage approach
7. Page 6 — Inside the garage, the silver web on Kirill's back, getting the full empty
8. Page 7 — Return, showers, bonus pay, checking Kirill's back (clean)
9. Page 8 — The Borscht bar: Ernest, Dick, Gutalin preaching
10. Page 9 — Dick brings news of Kirill's death, Red's rage, the itcher
11. Page 10 — Meeting Guta, pregnancy reveal, "What will happen to us now?"

## File Map
- `reader.html` — Combined reader, all pages scrollable with navigation
- `pages/` — Individual comic pages as standalone HTML
- `characters/characters.svg` — Character reference sheet (all 6 main characters)
- `assets/` — (empty, for future background images if we add AI-generated ones)

## How to Read
Open `reader.html` in any browser. Each page is also standalone in `pages/`.

## Tech Approach
- Pure HTML + inline SVG — no dependencies, no build step
- Characters are hand-coded SVG shapes — deterministic, consistent
- Google Fonts: Bangers (titles/captions), Patrick Hand (dialogue)
- Earthy color palette matching the book's Soviet industrial atmosphere
- Panel layouts vary: wide/narrow/full combinations per row

## Source
EPUB: `~/Downloads/Roadside Picnic - Arkady and Boris.epub`
