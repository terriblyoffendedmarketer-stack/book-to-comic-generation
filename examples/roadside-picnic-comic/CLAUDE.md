# Roadside Picnic — Comic Adaptation

## Status
**Phase:** Chapter 1 complete — 12 pages total
**Current:** 3 prologue pages + 9 chapter 1 pages, hybrid art mode (DrawThings AI backgrounds + SVG/CSS overlays)
**Next:** Chapter 2 pages (cemetery escape with Burbridge, domestic scenes, Noonan's cafe)

## What This Is
A comic adaptation of "Roadside Picnic" by Arkady & Boris Strugatsky. Hybrid art: AI-generated PNG backgrounds (DrawThings SDXL) with HTML/CSS speech bubbles, narrator boxes, and SVG character art overlaid. Built as standalone HTML pages.

## Characters Designed
- **Red Schuhart** — red hair, green jacket, stocky, squinting eyes, cigarette
- **Kirill Panov** — glasses, lab coat/blue jacket, thin, earnest
- **Tender** — heavyset, round, balding, nervous/sweaty
- **Captain Herzog** — military uniform, pipe, stern
- **Ernest** — bartender, mustache, shrewd eyes, white apron
- **Dick Noonan** — small, round, pink, balding, red tie
- **Gutalin** — huge, dark skin, intense, long arms, preacher
- **Dr. Pilman** — older, grey hair, composed (prologue only)
- **Guta** — beautiful, long dark hair, long neck, proud

## Pages Complete (12)

### Prologue (3 pages)
1. `page-00a-prologue.html` — Title, radio studio (AI bg), Pilman Radiant diagram (AI bg)
2. `page-00b-prologue.html` — Interview continues, stalker-at-fence (AI bg)
3. `page-00c-prologue.html` — Closing exchange, Harmont panorama (AI bg)

### Chapter 1 (9 pages)
1. `page-01.html` — Repository: Red tells Kirill about the full empty
2. `page-02.html` — Herzog's warning, Red tries to back out, changes his mind
3. `page-03.html` — Suiting up, marching to Zone, entering the Zone (AI bg)
4. `page-04.html` — Tender's babbling, Red punches him, THE SHIMMER (AI bg)
5. `page-05.html` — Mosquito mange, bolt trajectory sequence, Red's instinct
6. `page-06.html` — The garage (AI bg), finding the full empty, THE SILVER WEB
7. `page-07.html` — Return on autopilot, shower stall breakdown, bonus pay
8. `page-08.html` — The Borscht bar (AI bg), Gutalin preaching, Dick's announcement
9. `page-09.html` — Red's rage at Ernest, walking alone, meeting Guta, "What will happen to us now?"

## AI-Generated Assets (DrawThings SDXL)
- `test-radio-studio.png` — seed 42, 1024x512
- `pilman-radiant.png` — seed 101, 1024x768
- `stalker-fence.png` — seed 202, 1024x512
- `harmont-aerial.png` — seed 303, 1024x768
- `zone-shimmer.png` — seed 404, 1024x512
- `pilman-radiant-v2.png` — seed 505, 1024x768
- `zone-entrance.png` — seed 606, 1024x512
- `borscht-bar.png` — seed 707, 1024x512
- `garage-silverweb.png` — seed 808, 1024x768

## How to Read
Open `reader.html` in any browser (served from a local HTTP server for asset loading).
Each page is also standalone in `pages/`.

```bash
python3 -m http.server 8765
# Then open http://localhost:8765/reader.html
```

## Source
EPUB: `~/Downloads/Roadside Picnic - Arkady and Boris.epub`
