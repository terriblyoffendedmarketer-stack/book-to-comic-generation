---
name: book-to-comic
description: "Convert any book (EPUB, PDF, or text) into a comic book. Multi-pass pipeline: extract text → map structure → map beats → build character bible → design characters → script panels → produce pages → assemble reader. Two art modes: deterministic SVG characters (consistency guaranteed, simple style) or AI-generated panels via DrawThings (richer art, requires consistency management). Triggers: comic, comic book, graphic novel, book to comic, adapt book, visual novel, comic adaptation, make a comic, turn into comic, illustrate book, book illustration, draw a comic"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Agent
  - mcp__drawthings__generate_image
  - mcp__drawthings__check_status
  - mcp__drawthings__get_config
  - mcp__Claude_Browser__preview_start
  - mcp__Claude_Browser__navigate
  - mcp__Claude_Browser__computer
  - mcp__Claude_Browser__read_page
---

# Book-to-Comic Adaptation Skill

Convert any book into a readable comic. Feed it a book, get a comic out.

## Core Principle

This is a **multi-pass pipeline**, not a one-shot process. Each pass builds on the previous one. Do NOT skip passes or jump straight to page production — the foundational work determines quality.

## Art Modes

Two approaches, can run side-by-side for comparison:

### Mode A: Deterministic SVG (Consistency Guaranteed)
- Characters are hand-coded SVG shapes — same shapes every panel, zero drift
- Simple cartoon style (Calvin & Hobbes / Peanuts level)
- Backgrounds are geometric SVG shapes
- Best for: long-form adaptations where character consistency across hundreds of panels matters most
- Trade-off: art is simple, poses are manual work

### Mode B: AI-Generated via DrawThings (Richer Art)
- Use DrawThings MCP to generate panel backgrounds and scenes
- Can generate character reference sheets with consistent style prompts
- Use seed pinning for reproducibility within a session
- Best for: shorter adaptations, atmospheric/cinematic feel, testing visual styles
- Trade-off: character consistency requires careful prompt engineering and may drift

### Mode C: Hybrid (Recommended Starting Point)
- AI-generated backgrounds via DrawThings for atmosphere
- SVG character overlays on top for consistency
- Gets the best of both: rich environments + reliable characters
- Implementation: generate background image, embed as `<image>` in SVG, layer character shapes on top

## Pipeline

### Pass 0: Extract Text
**Goal:** Get clean chapter text from the source file.

1. **EPUB**: Run `extract-epub.py` (included below) — outputs one `.txt` per chapter to scratchpad
2. **PDF**: Use the Read tool with page ranges
3. **Plain text**: Split on chapter markers

Save extracted text to scratchpad directory. Note chapter sizes — this determines comic length.

**Rule of thumb:** ~5,000 words of prose ≈ 8-15 comic pages depending on dialogue density.

### Pass 1: Book Structure Map
**Goal:** Understand the whole book before touching any chapter.

Read every chapter (at minimum: opening, middle, ending sections). Produce a structure document:

```markdown
# [Book Title] — Structure Map

## Overview
- Genre, tone, themes
- Total chapters, approximate word count
- POV structure (first person? rotating? etc.)
- Time span of the story

## Chapter Breakdown
For each chapter:
- Chapter N: [Title/Label]
  - POV character
  - Time period / age
  - Setting(s)
  - Narrative role (setup / rising action / climax / resolution)
  - Key events (3-5 bullets)
  - Estimated comic pages needed
```

Save as `planning/01-structure-map.md` in the project directory.

### Pass 2: Beat Maps
**Goal:** Scene-by-scene breakdown of each chapter with key dialogue preserved.

For each chapter, produce:

```markdown
# Chapter N — Beat Map

## Scene 1: [Scene Name]
- Location: where
- Characters present: who
- What happens: narrative summary (2-3 sentences)
- Key dialogue to preserve (exact quotes that reveal character or advance plot):
  - "Quote" — why it matters
  - "Quote" — why it matters
- Concepts to explain to the reader: (any world-building the reader needs)
- Visual moments: what would make a strong panel
- Emotional arc: what the reader should feel

## Scene 2: ...
```

Critical rules for beat mapping:
- **Preserve character voice.** Dialogue that showcases personality (wit, dismissiveness, warmth, fear) must be kept verbatim or very close. Cutting dialogue that reveals who a character IS makes them generic.
- **Flag concepts that need explanation.** A new reader doesn't know the book's world. If a scene references something (a Zone artifact, a magic system, a political structure), note that the comic must explain it — visually or via narrator box.
- **Don't compress too aggressively.** Chapters can be long in comic form. That's fine. A 20-page chapter that preserves the story beats is better than a 5-page chapter that loses them.
- **Mark emotional peaks.** These get full-width panels or splash pages.

Save as `planning/02-beats-chN.md` for each chapter.

### Pass 3: Character Bible
**Goal:** Every character with physical description, personality, relationships, and arc.

```markdown
# Character Bible

## [Character Name]
- **Also known as:** nicknames, titles
- **Physical description from text:** (exact quotes describing appearance)
- **Age:** at each chapter appearance
- **Role:** protagonist / antagonist / supporting / minor
- **Personality traits:** 3-5 defining characteristics with evidence from text
- **Speech patterns:** how they talk (formal? slang? short sentences? lectures?)
- **Key relationships:** with other characters
- **Arc:** how they change across the story
- **Visual design notes:** distinguishing features for comic (what makes them instantly recognizable at small scale)
  - Body type: stocky / thin / heavy / round / huge
  - Hair: color, style (THE #1 identifier at comic scale)
  - Signature clothing: one item they always wear
  - Face detail: glasses, facial hair, scars, etc.
  - Expression default: what's their resting face? (smirk, frown, neutral, worried)
```

Save as `planning/03-character-bible.md`.

### Pass 4: Character Design
**Goal:** Visual reference for every character.

#### Mode A (SVG):
Create `characters/characters.svg` — a reference sheet with each character drawn in the SVG template style. Each character needs:
- Full body view with labeled features
- 2-3 distinguishing visual features that work at small scale
- Characters must be **maximally distinct from each other** (vary height, width, hair color, clothing color)

Use the SVG character template (see Templates section below).

#### Mode B (DrawThings):
Generate character reference sheets:
```
prompt: "character design sheet, [character description], multiple poses, 
         front view side view, simple cartoon style, white background, 
         consistent design, comic book character"
negative_prompt: "realistic, photographic, 3d render, complex background"
seed: [pin a seed per character for consistency]
```

Save generated images to `characters/` directory.

#### Mode C (Hybrid):
Do both — SVG for the actual panel overlays, DrawThings reference for visual inspiration and style guidance.

### Pass 5: Panel Scripts
**Goal:** Detailed script for every page before any art is produced.

For each page:

```markdown
## Page N — [Scene Description]

### Row 1 (height: 200px)
**Panel 1 (wide):** [Establishing shot — location description]
- Background: [what's visible]
- Characters: [who, where positioned, what pose]
- Narrator box: "[text]"

**Panel 2 (narrow):** [Close-up on character face]  
- Expression: [which expression]
- Bubble: "[dialogue]" — tail pointing [direction]

### Row 2 (height: 180px)
...
```

Panel scripting rules (learned from prototype):
1. **Max 6 panels per page.** More than 6 = cramped. Add another page instead.
2. **Panels must be large enough for their content.** The problem is never font size — it's panel size relative to content. A dialogue-heavy panel needs to be big. A wordless action panel can be smaller.
3. **Speech bubbles should not cover more than ~40% of a panel's background.** If dialogue needs more space, the panel needs to be bigger, or split the dialogue across panels.
4. **Preserve the source material's voice.** Adapted dialogue should sound like the character wrote it, not like a summary. If a character is witty, their wit must come through. If they're dismissive, that tone must be there.
5. **Full-width panels for:** chapter openings, establishing shots, emotional climaxes, dramatic reveals, atmospheric moments.
6. **Close-up face panels when:** emotion matters more than environment, a character's reaction IS the story beat.
7. **When in doubt, add another page** rather than cramming content.

Save as `planning/05-script-chN.md` for each chapter.

### Pass 6: Page Production
**Goal:** Build the actual HTML comic pages.

Each page is a standalone HTML file. See Templates section for the full page template.

Production workflow per page:
1. Open the panel script for this page
2. Build the HTML structure (panel rows, sizes)
3. For each panel:
   - **Mode A:** Code the SVG scene (background shapes + character SVG from reference)
   - **Mode B:** Generate the panel image via DrawThings, embed as `<img>`
   - **Mode C:** Generate background via DrawThings, overlay SVG characters
4. Add speech bubbles, narrator boxes, thought bubbles
5. Preview in browser, verify readability and visual clarity
6. Iterate if panels are too cramped or dialogue is obscured

### Pass 7: Assembly & Reader
**Goal:** Combine all pages into a navigable reader.

Create `reader.html`:
- Embeds all pages via iframes
- Sticky navigation header with chapter/page links
- Auto-resize iframes to content height
- Scroll-based navigation highlighting (IntersectionObserver)
- Each page also works standalone

## Templates

### EPUB Extraction Script

Save as `scripts/extract-epub.py` in the project:

```python
#!/usr/bin/env python3
# extract-epub.py — Extract readable text from an EPUB file
# Usage: python3 extract-epub.py <path-to-epub> [output-dir]
# Requires: Python 3 standard library only (no pip packages)
#
# Outputs one .txt file per chapter into output-dir (default: ./extracted/)
# Also prints chapter list with character counts to stdout.
#
# Gotchas:
# - EPUB is just a zip file with XHTML inside. No special libraries needed.
# - Chapter order comes from the OPF spine, not filesystem order.
# - Some EPUBs use .html not .xhtml — this handles both.
# - Images are skipped (we're after text only).

import sys, os, re, html, zipfile
from xml.etree import ElementTree as ET

def strip_html(text):
    text = re.sub(r'<[^>]+>', '\n', text)
    text = html.unescape(text)
    lines = [l.strip() for l in text.split('\n')]
    text = '\n'.join(lines)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def extract_epub(epub_path, output_dir='extracted'):
    if not os.path.exists(epub_path):
        print(f"Error: {epub_path} not found"); sys.exit(1)
    os.makedirs(output_dir, exist_ok=True)
    with zipfile.ZipFile(epub_path, 'r') as zf:
        container = zf.read('META-INF/container.xml').decode('utf-8')
        opf_match = re.search(r'full-path="([^"]+)"', container)
        if not opf_match:
            print("Error: Can't find OPF file"); sys.exit(1)
        opf_path = opf_match.group(1)
        opf_dir = os.path.dirname(opf_path)
        opf_content = zf.read(opf_path).decode('utf-8')
        opf_clean = re.sub(r'\sxmlns="[^"]+"', '', opf_content, count=1)
        root = ET.fromstring(opf_clean)
        manifest = {}
        for item in root.findall('.//manifest/item'):
            item_id = item.get('id')
            href = item.get('href')
            media = item.get('media-type', '')
            if 'html' in media or 'xhtml' in media:
                manifest[item_id] = href
        spine_ids = [ref.get('idref') for ref in root.findall('.//spine/itemref')]
        chapters = []
        for i, sid in enumerate(spine_ids):
            if sid not in manifest: continue
            href = manifest[sid]
            full_path = os.path.join(opf_dir, href) if opf_dir else href
            full_path = full_path.replace('\\', '/')
            try:
                raw = zf.read(full_path).decode('utf-8')
            except KeyError:
                print(f"  Warning: {full_path} not found, skipping"); continue
            text = strip_html(raw)
            if len(text) < 50: continue
            first_line = text.split('\n')[0][:80] if text else os.path.basename(href)
            chapter_name = f"chapter-{i:02d}"
            out_file = os.path.join(output_dir, f"{chapter_name}.txt")
            with open(out_file, 'w') as f:
                f.write(text)
            chapters.append({'index': i, 'name': chapter_name, 'file': out_file,
                             'chars': len(text), 'preview': first_line})
        print(f"\nExtracted {len(chapters)} chapters from: {os.path.basename(epub_path)}\n")
        for ch in chapters:
            print(f"  {ch['name']}: {ch['chars']:,} chars — {ch['preview']}")
        print(f"\nOutput: {os.path.abspath(output_dir)}/")
        return chapters

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 extract-epub.py <path-to-epub> [output-dir]"); sys.exit(1)
    extract_epub(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else 'extracted')
```

### SVG Character Template

Base structure for Mode A characters. Adjust for each character's body type:

```svg
<g transform="translate(X, Y) scale(S)">
  <!-- Body -->
  <rect x="15" y="55" width="50" height="60" rx="5" fill="CLOTHING_COLOR" stroke="#222" stroke-width="2"/>
  <!-- Arms (adjust endpoints for pose) -->
  <line x1="15" y1="70" x2="-5" y2="95" stroke="#222" stroke-width="4" stroke-linecap="round"/>
  <line x1="65" y1="70" x2="85" y2="95" stroke="#222" stroke-width="4" stroke-linecap="round"/>
  <!-- Hands -->
  <circle cx="-5" cy="97" r="5" fill="SKIN_COLOR" stroke="#222" stroke-width="1.5"/>
  <circle cx="85" cy="97" r="5" fill="SKIN_COLOR" stroke="#222" stroke-width="1.5"/>
  <!-- Legs -->
  <line x1="30" y1="115" x2="25" y2="150" stroke="#222" stroke-width="4" stroke-linecap="round"/>
  <line x1="50" y1="115" x2="55" y2="150" stroke="#222" stroke-width="4" stroke-linecap="round"/>
  <!-- Head -->
  <circle cx="40" cy="30" r="25" fill="SKIN_COLOR" stroke="#222" stroke-width="2"/>
  <!-- HAIR — #1 identifier at small scale -->
  <path d="M15,22 Q20,5 30,8 Q35,2 42,6 Q50,0 55,8 Q62,5 65,20" fill="HAIR_COLOR" stroke="HAIR_DARK" stroke-width="1.5"/>
  <!-- Eyes / Mouth — vary per character and expression -->
</g>
```

**Body type variations:** Adjust rect width/height for stocky (w:60 h:55), thin (w:35 h:65), heavy (w:70 h:55), round (use ellipse instead), huge (scale everything 1.3x).

**Pose variations:** Modify arm/leg line endpoints:
- Standing: arms at sides (default above)
- Talking: mouth open ellipse, one arm angled up to gesture
- Walking: legs spread, alternate arm swing
- Sitting: shorter legs, body lower in frame
- Pointing: one arm extended straight
- Arms crossed: arm lines curve inward to chest
- Slumped/sad: head shifted down, arms hanging lower
- Excited: arms angled up, mouth as big arc

**Expression library (face swaps):**
- Neutral: small dot eyes, straight line mouth
- Happy: dot eyes, upward arc mouth
- Talking: dot eyes, open ellipse mouth
- Sad: angled-down eyebrow lines, downward arc mouth
- Angry: V-shaped eyebrows, tight line mouth
- Shocked: large circle eyes, O-shaped mouth
- Smirk: one raised eyebrow line, half-arc mouth

### DrawThings Panel Generation

For Mode B/C, use these prompt patterns:

**Backgrounds/environments:**
```
prompt: "[scene description], comic book panel, [art style], detailed background, 
         no characters, no text, no speech bubbles"
negative_prompt: "text, words, letters, speech bubble, realistic photo, 3d render"
width: 680  (matches panel width)
height: [match panel height]
seed: [pin for consistency within a scene]
```

**Full panels with characters (Mode B only):**
```
prompt: "[scene with characters], comic book art style, [describe each character by 
         their visual design], [action/pose], [environment]"
negative_prompt: "text, words, speech bubbles, realistic, photographic"
```

**Style consistency tip:** Pick one art style prompt suffix and use it for ALL panels:
- Clean line art: `"clean ink lines, flat colors, comic book coloring"`
- Manga-influenced: `"manga style, screentone shading, black and white"`  
- Watercolor: `"watercolor comic, soft colors, ink outlines"`
- Franco-Belgian: `"ligne claire, clear line art, tintin style, flat colors"`

### Page Template (HTML)

Save as `scripts/page-template.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Comic Page — TEMPLATE</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Bangers&family=Patrick+Hand&display=swap');
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: #f5f0e8;
    display: flex;
    justify-content: center;
    padding: 20px;
    font-family: 'Patrick Hand', cursive;
  }
  .page {
    width: 700px;
    background: white;
    border: 3px solid #222;
    padding: 12px;
    display: grid;
    gap: 8px;
  }
  .panel-row { display: flex; gap: 8px; }
  .panel {
    border: 2.5px solid #222;
    border-radius: 3px;
    overflow: hidden;
    position: relative;
    background: #fff;
  }
  .panel-wide { flex: 2; }
  .panel-narrow { flex: 1; }
  .panel-full { flex: 1; }
  .panel-inner { width: 100%; height: 100%; position: relative; }
  
  /* Speech bubbles */
  .bubble {
    position: absolute;
    background: white;
    border: 2px solid #222;
    border-radius: 18px;
    padding: 6px 10px;
    font-size: 13px;
    line-height: 1.3;
    max-width: 180px;
    z-index: 10;
  }
  .bubble::after {
    content: '';
    position: absolute;
    bottom: -12px; left: 25px;
    width: 0; height: 0;
    border-left: 8px solid transparent;
    border-right: 8px solid transparent;
    border-top: 12px solid white;
  }
  .bubble::before {
    content: '';
    position: absolute;
    bottom: -15px; left: 24px;
    width: 0; height: 0;
    border-left: 9px solid transparent;
    border-right: 9px solid transparent;
    border-top: 14px solid #222;
  }
  .bubble.right::after { left: auto; right: 25px; }
  .bubble.right::before { left: auto; right: 24px; }
  .bubble.thought { border-radius: 20px; }
  .bubble.thought::after {
    border: none; width: 8px; height: 8px;
    background: white; border-radius: 50%;
    bottom: -10px; border: 2px solid #222;
  }
  .bubble.thought::before {
    border: none; width: 5px; height: 5px;
    background: white; border-radius: 50%;
    bottom: -18px; left: 30px; border: 2px solid #222;
  }
  
  /* Narrator boxes */
  .narrator {
    position: absolute;
    background: #f8f0d0;
    border: 2px solid #222;
    padding: 5px 8px;
    font-size: 12px;
    line-height: 1.3;
    z-index: 10;
    max-width: 200px;
  }
  
  .caption {
    font-family: 'Bangers', cursive;
    font-size: 11px;
    letter-spacing: 1px;
    color: #666;
    text-align: center;
    padding: 2px 0;
  }
</style>
</head>
<body>
<div class="page">
  <!-- Panel rows go here. See panel scripting rules. -->
  <!-- Max 6 panels per page. -->
  <!-- Each .panel-row needs explicit height: style="height: Xpx" -->
  <!-- Typical heights: 140-260px depending on content -->
</div>
</body>
</html>
```

## Project File Structure

```
[book-name]-comic/
├── CLAUDE.md                    # Project status, roadmap, character list
├── planning/
│   ├── 01-structure-map.md      # Pass 1 output
│   ├── 02-beats-ch0.md          # Pass 2 output (one per chapter)
│   ├── 02-beats-ch1.md
│   ├── 03-character-bible.md    # Pass 3 output
│   └── 05-script-ch1.md         # Pass 5 output (one per chapter)
├── characters/
│   ├── characters.svg           # Mode A: SVG reference sheet
│   └── *.png                    # Mode B: DrawThings character refs
├── pages/
│   ├── page-00-prologue.html
│   ├── page-01.html
│   └── ...
├── assets/
│   └── *.png                    # Mode B/C: generated panel backgrounds
├── reader.html                  # Combined reader with navigation
└── scripts/
    ├── extract-epub.py          # EPUB text extraction
    └── page-template.html       # Starter template for pages
```

## Lessons Learned (from prototype)

These are hard-won from building and reviewing actual comic pages:

1. **Panel size is the bottleneck, not font size.** When text feels cramped, the panel is too small for its content. Making font bigger makes it worse. Make the panel bigger or split content across panels.

2. **Never skip the planning passes.** Jumping straight to page production produces pages that miss key story beats, lose character voice, and fail to explain world-building concepts to new readers.

3. **Dialogue adaptation is the hardest part.** It's tempting to summarize, but summary kills character. A character's specific word choices, their rhythm, their humor — that's what makes them a person in the reader's mind. Preserve it.

4. **6 panels maximum per page.** Every time we went over 6, the page suffered. The constraint forces better storytelling choices.

5. **Chapters can be long.** A 15,000-word chapter might need 15-25 comic pages. That's fine. Don't compress a chapter into 5 pages — you'll lose everything that matters.

6. **Explain the world.** A comic reader hasn't read the book. If a scene references a concept (an artifact, a place, a backstory), the comic must explain it — through a narrator box, a visual diagram, or dialogue. Never assume prior knowledge.

7. **DrawThings seed pinning helps but doesn't guarantee consistency.** Same seed + same prompt = same image, but changing the prompt even slightly can shift character appearance. For long-form work, SVG characters (Mode A/C) are more reliable.

8. **Preview every page in a browser before moving on.** Check: Can you read all dialogue? Is >40% of each panel's background visible? Do the character gestures communicate the emotion? Does the page flow left-to-right, top-to-bottom naturally?

## Getting Started (Quick Reference)

When invoked with a book:

1. Create project directory: `[book-name]-comic/`
2. Extract text (Pass 0) — save chapters to scratchpad
3. Read all chapters, write structure map (Pass 1)
4. Write beat maps for each chapter (Pass 2)
5. Write character bible (Pass 3)
6. Ask user which art mode (A/B/C) or test all three on one page
7. Design characters (Pass 4)
8. Script panels chapter by chapter (Pass 5)
9. Produce pages (Pass 6)
10. Assemble reader (Pass 7)
11. Preview in browser, iterate based on visual review

Between each pass, update CLAUDE.md with current status.
