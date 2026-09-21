# Book-to-Comic: The Refined Approach
# Last updated: 2026-09-18

## Core Philosophy
Simple is fine. Oversimplified is fine. What is NOT fine is sacrificing storytelling.
The goal is: a person who "doesn't like reading" picks this up and follows the story.
Every decision filters through: does this help tell the story?

## The Constraint: Limited AI Budget
We cannot afford to brute-force-generate images. Every DrawThings call costs time.
Every Claude call costs tokens. The approach must minimize waste by:
1. Analyzing everything BEFORE generating anything
2. Reusing assets across panels (dialogue scenes = same composition, different bubbles)
3. Using DrawThings ONLY where it adds value (simple ambient backgrounds)
4. Using SVG for everything that needs to be accurate (characters, objects, directions)
5. Skipping backgrounds entirely when they don't add storytelling value

## The 10-Step Pipeline (layer by layer)

### Step 1: BOOK EXTRACTION
- Input: EPUB/PDF/text file
- Output: Clean text, one file per chapter
- Tool: `scripts/extract-epub.py` (already built, works)
- No AI budget spent

### Step 2: FULL BOOK INVENTORY (meta-level analysis)
- Input: All chapter text
- Output: A structured JSON/markdown with:
  ```
  characters: [
    { name, frequency, first_appearance_chapter,
      described_appearance: "exact quotes from text",
      key_identifiers: ["red hair", "stocky"],
      emotions_expressed: ["angry", "nervous", "smirking", "terrified"],
      appears_in_chapters: [1, 2, 3, 4] }
  ]
  settings: [
    { name, description_from_text, chapters_used_in,
      complexity: "simple" | "complex",
      drawthings_viable: true/false,
      reason: "just a bar interior, generic" | "needs specific spatial layout" }
  ]
  character_pairings: [
    { characters: ["Red", "Kirill"], scene_count: 12, relationship: "friends/colleagues" }
  ]
  scene_types: {
    dialogue: 45,     # scenes that are mostly talking
    action: 8,        # scenes with physical movement/danger
    establishing: 12, # setting the scene, atmosphere
    montage: 3,       # time passing, multiple quick beats
    internal: 15      # character's inner thoughts
  }
  ```
- **THIS STEP IS CRITICAL** — it determines the entire asset budget
- AI budget: ~1 Claude call analyzing the full book text

### Step 3: CHARACTER DESIGN
- Input: Character inventory from Step 2
- Output: SVG character sheets — one per character
- **Key rule**: Each character gets EXACTLY the expressions found in the book.
  If Red has 10 emotions across the book, Red gets 10 expression SVGs.
  If Gutalin only appears stoic/intense, Gutalin gets 1-2 expressions.
- **Key identifiers**: Mined from the text's physical descriptions.
  Not invented — extracted from the author's words.
- **Simplicity level**: Think Cyanide & Happiness, XKCD, or Persepolis.
  Simple line drawings with strong identifiers. Not aiming for manga or superhero art.
  The simpler the style, the more CONSISTENT it is across panels, and the easier
  to template.
- **Poses**: Map from scene types. Dialogue scenes need: standing, sitting, gesturing.
  Action scenes need: running, ducking, reaching. Count what's needed from the beat maps.
- AI budget: 0 — SVG is hand-coded (by the LLM, but no image generation)

### Step 4: BACKGROUND ASSET PLANNING
- Input: Settings inventory from Step 2
- For each setting, decide:
  - **Skip**: No background needed (dialogue-heavy, emotion-focused)
  - **Solid color/gradient**: Simple mood setting (warm interior = amber gradient, night = dark blue)
  - **Simple SVG**: Basic line-art scenery (table, window, buildings silhouette)
  - **DrawThings**: ONLY for generic ambient shots where accuracy doesn't matter
    (sky, landscape, abstract texture, simple room)
- **DrawThings rules**:
  - NEVER use for: specific object interactions, directional movement, spatial relationships
  - ALWAYS pin seed. NEVER regenerate. Save once, reference forever.
  - Best for: establishing shots, atmosphere, texture overlays
- AI budget: Only the DrawThings calls for qualifying backgrounds

### Step 5: BEAT MAPPING (chapter-level)
- Input: Chapter text + character inventory + settings
- Output: Per-chapter beat map — sequence of visual moments
- Each beat has:
  ```
  { scene_type, characters_present, setting, mood,
    dialogue: ["line 1", "line 2"],
    key_visual: "what the reader MUST see in this panel",
    panel_type: "close-up" | "two-shot" | "establishing" | "wide" | "inset" }
  ```
- **Dialogue optimization**: Consecutive dialogue beats between the same characters
  in the same setting → mark as "reuse composition". Only the first beat in a dialogue
  sequence needs a unique panel composition. The rest reuse it with different bubbles.
- AI budget: ~1 Claude call per chapter

### Step 6: PANEL SCRIPTING
- Input: Beat maps
- Output: Per-page panel scripts
- Rules:
  - Max 6 panels per page (project constraint, not 9)
  - Dialogue pages: 4-6 panels (most common)
  - Action pages: 2-4 panels
  - Establishing: 1-2 large panels
  - Max 3 speech bubbles per panel
  - Z-pattern reading flow: first speaker upper-left, responses descend
- **Composition types** (the reusable templates):
  1. **Single character close-up**: One character, expression, 1-2 bubbles above
  2. **Two-shot dialogue**: Two characters facing each other, bubbles in speech zone
  3. **Group shot**: 3+ characters, narrator box + 1-2 bubbles
  4. **Establishing wide**: Setting background (DrawThings or SVG), floating caption
  5. **Action panel**: Character in motion, minimal or no dialogue
  6. **Internal monologue**: Character close-up + thought bubble (cloud border)
  7. **Narrator-only**: No characters, just narrator box over background or solid color
- AI budget: ~1 Claude call per chapter

### Step 7: LAYOUT GENERATION
- Input: Panel scripts
- Output: HTML/CSS page layouts (empty frames)
- **Template system**: Flexible 3-row grid
  ```
  Page = [Tier1, Tier2, Tier3]
  Tier = { panels: [Panel], tier_height: "33%" | "50%" | "auto" }
  Panel = { width: "50%" | "33%" | "66%" | "100%", type: composition_type }
  ```
- This step is pure CSS — no AI budget
- The zone-based layout applies: each panel has speech-zone (top flex) + art-zone (bottom)

### Step 8: ASSET ASSEMBLY
- Input: Layouts + character SVGs + backgrounds
- Output: Populated HTML pages
- For each panel:
  - Insert background (color/gradient, SVG, or DrawThings PNG)
  - Insert character SVGs with correct expression and pose
  - Insert speech bubbles with dialogue text in reading order
- **Dialogue scene optimization**: For consecutive dialogue panels, COPY the
  art-zone content and only change the speech-zone content
- AI budget: 0 for assembly, just template filling

### Step 9: PAGE ASSEMBLY
- Combine into reader.html with navigation
- Verify all asset paths resolve
- Serve via local HTTP server for testing

### Step 10: REVIEW & ITERATE
- Visual inspection of every page
- Check: Can you tell who's speaking? Can you follow the story?
- Check: Are characters distinguishable? Are expressions readable?
- Fix specific panels, not wholesale redesigns

## DrawThings: When to Use and When Not To

### USE DrawThings for:
- Landscape/cityscape establishing shots (no specific objects needed)
- Abstract atmosphere (fog, glow, darkness, rain)
- Simple room interiors (generic bar, office, lab — no specific items)
- Texture overlays (brick wall, wood grain, metal surface)
- Sky/weather backgrounds

### DO NOT use DrawThings for:
- Scenes requiring specific spatial relationships between objects
- Anything with directionality (bullets, movement, pointing)
- Character-containing scenes (characters are SVG, always)
- Scenes where a specific object must be recognizable
- Anything where "close enough" isn't good enough

### DrawThings parameters (when used):
- Model: SDXL Base v1.0 (8-bit)
- Port: 7860
- ALWAYS pin seed
- ALWAYS save to assets/ with descriptive name
- NEVER regenerate — if result is bad, use a different approach (SVG or skip)

## Style Guide: Simplicity That Tells Stories

### Character art style:
- Think: Persepolis, Maus, XKCD, Cyanide & Happiness
- Line drawings with strong outlines
- KEY IDENTIFIERS that persist across every appearance
- Expressions conveyed through: eyes, mouth, posture (not fine detail)
- Color: flat fills, no gradients on characters (fast, consistent, scalable)

### When NO background is better than a bad background:
- Pure dialogue scenes between 2 characters → solid color or gradient
- Internal monologue → character on blank/gradient
- Tense moments → character on black
- It's a valid comic choice. Many acclaimed comics use this extensively.

### Reuse is a feature:
- Same two-shot composition across a 4-panel dialogue? That's professional pacing.
- Same establishing shot at the start of every scene in the same location? That's consistency.
- Same character pose for extended dialogue? That's how comics work.

## Future: Claude API Integration
Once the approach is proven on one chapter:
- Connect to Claude API (Messages API)
- Send book text + pipeline instructions
- Generate all planning docs (inventory, beats, scripts) in batch
- Still need manual DrawThings calls (local, not API-accessible remotely)
- Assembly could be automated with a script reading the panel scripts as JSON
