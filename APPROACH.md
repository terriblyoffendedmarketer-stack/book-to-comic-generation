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

### Step 3: CHARACTER DESIGN (Parametric SVG Assembly)
- Input: Character inventory from Step 2
- Output: SVG character sheets — one per character, all in same art style
- **Key rule**: Each character gets EXACTLY the expressions found in the book.
- **Key identifiers**: Mined from the text's physical descriptions.
  Not invented — extracted from the author's words.
- **Pipeline**: Component selection → SVG assembly → (optional) AI enhancement
- AI budget: 0 for assembly. Optional ~1 DrawThings call per character for polish.

**Why parametric, not AI generation:**
SDXL text-to-image was tested and FAILED — 3 attempts on one character proved that
diffusion models ignore unusual features (golden hair → black hair, no-whites eyes
→ normal eyes). Each retry fixes one trait and breaks another. The verification
loop helps detect failures but can't make the generator reliable. The fundamental
problem: diffusion models are pattern completers, not instruction followers.

Parametric assembly solves this by SELECTING features, not GENERATING them.
"Golden hair" = pick the golden hair component. 100% accurate. Zero randomness.

### Step 3a: THE COMPONENT LIBRARY (one-time build, reusable across all books)

Art style: **Bold Outlined** (Persepolis/Tintin-inspired)
- Thick black outlines (stroke-width 2-3px at character scale)
- Flat color fills (no gradients on characters)
- Deliberate simplicity — readable at comic panel size
- Key identifiers EXAGGERATED (bigger glasses, bolder scars, wilder hair)

The library is EXTENSIBLE — start with core set, add components as new books
need them. Each new component is drawn in the same style, so it integrates
seamlessly. Components are organized by category:

```
BODY TEMPLATES (~8):
  adult-male, adult-female, child, teen, elderly-male, elderly-female,
  large-heavy, thin-tall
  (Each template: full body outline with neutral pose)
  (Variants per template: standing, sitting, walking, gesturing)

HEADS/FACES (~10 shapes):
  round, oval, angular, square, long, heart, wide, narrow, childish, gaunt
  (Head shape affects the entire face — this is the biggest differentiator)

HAIRSTYLES (~25):
  male-short, male-medium, male-long, male-bald, male-buzz, male-slicked,
  male-mohawk, male-messy, male-curly, male-ponytail, male-receding,
  female-short, female-medium, female-long, female-bob, female-curly,
  female-braids, female-ponytail, female-bun, female-flowing, female-afro,
  child-short, child-messy, child-pigtails, wild-unkempt
  (Color is a FILL attribute — any color on any style)

EYES (~10 types):
  normal, wide, narrow, squinting, glasses, sunglasses, closed, sleepy,
  all-dark (alien/supernatural), heterochromia
  (Each type has expression variants: neutral, angry, surprised, sad, happy)

NOSES (~6): small, large, pointed, flat, upturned, hooked
MOUTHS (~8): neutral, smile, frown, open, gritted, smirk, grimace, laugh
BROWS (~5): neutral, raised, furrowed, one-raised, thick

FACIAL HAIR (~6): none, stubble, short-beard, full-beard, mustache, goatee
SKIN FEATURES (~8): freckles, wrinkles, scar-cheek, scar-eye, mole,
  blush, fur-texture, radiation-marks

CLOTHING (~20):
  t-shirt, button-shirt, polo, jacket, coat, hoodie, suit, uniform,
  lab-coat, apron, dress-simple, dress-formal, robe, tank-top, sweater,
  hazmat-suit, armor-simple, cloak, overalls, jumpsuit
  (Color/pattern is a FILL attribute)

ACCESSORIES (~15):
  glasses, sunglasses, hat-cap, hat-formal, hat-military, pipe, cigarette,
  scarf, tie, bowtie, badge, earring, headband, bandage, necklace

SPECIAL/UNUSUAL (~10):
  fur-overlay (body), scales-overlay, cybernetic-arm, wings-small,
  tail, horns, pointed-ears, extra-eyes, tattoo-pattern, prosthetic
  (For non-standard characters — fantasy, sci-fi, supernatural)

PROPS (held items, ~10):
  book, weapon-sword, weapon-gun, bag, cane, phone, drink, tool,
  musical-instrument, umbrella
```

Estimated total: ~130+ components across categories.
Core set (enough for most realistic fiction): ~60-80 components.
Full set (fantasy, sci-fi, supernatural coverage): ~130+ components.

### Step 3b: DIFFERENTIATING SIMILAR CHARACTERS

The hardest case: two characters who SHOULD look similar (siblings, twins,
same-ethnicity colleagues). The pipeline must make them visually distinct.

**The Differentiation Algorithm:**
```
For each character pair in the book:
  1. Compute visual similarity:
     - Same gender? Same age range? Same build? Same hair color?
     - Count shared component selections

  2. If similarity > threshold (e.g., 3+ shared major components):
     - Extract ALL text-described differences, however subtle
     - Assign differentiators from this priority list:

     Priority 1 (from book text):
       Physical differences the author describes ("Greg is taller",
       "Finn has a scar on his chin")

     Priority 2 (color coding):
       Assign different primary colors to their clothing.
       This is the strongest visual differentiator in comics.
       Reader learns: blue = Greg, green = Finn.

     Priority 3 (signature accessory):
       Give one character an accessory the other doesn't have.
       One wears glasses, the other doesn't. One has a hat.
       Only if it doesn't contradict the book.

     Priority 4 (silhouette difference):
       Different hairstyle. Different posture. Different build variation.
       Even within "adult-male" template, one can be broader-shouldered.

     Priority 5 (face shape):
       Different head shape — round vs angular. This is subtle but
       effective. Real siblings have different face shapes.

  3. SILHOUETTE TEST: Render both characters as solid black silhouettes.
     Can you tell them apart? If no → add another differentiator.

  4. COLOR TEST: Are their primary colors distinct?
     No two characters should share the same primary clothing color.
```

**The "unpredictable differentiator" problem:**
The user correctly notes: you can't predict WHAT will make two characters different
in an arbitrary book. One book might distinguish them by shoes, another by posture,
another by a tiny scar.

Solution: The component library doesn't need to contain every possible differentiator.
It needs:
1. A RICH SET of standard differentiators (hair, face, clothing color, accessories)
2. A FREEFORM OVERLAY slot — an SVG layer where Claude can place a custom small
   detail (a specific scar, a unique pin, a distinctive belt) by writing a small
   SVG path. This is where Claude's SVG-writing ability is actually useful — not
   for whole characters, but for ONE small distinguishing detail.
3. On-demand component generation: if a book needs "a character with a monocle"
   and there's no monocle component, DrawThings generates JUST the monocle
   (simple isolated object on white background — Tier 1 easy for AI), VTracer
   vectorizes it, and it joins the library permanently.

### Step 3c: AI ENHANCEMENT LAYER (optional)

After parametric assembly, each character SVG can optionally be enhanced:
1. Render SVG to PNG
2. DrawThings img2img with Flux model, LOW denoising (0.2-0.3)
   - Adds texture, anti-aliasing, artistic depth
   - Same style prompt for ALL characters → consistent enhancement
   - Low denoising preserves structure and colors
3. Claude vision verifies: did enhancement preserve all critical features?
   - Yes → VTracer vectorize → use as final art
   - No → reduce denoising or skip enhancement, use plain SVG
4. The parametric SVG is always the SAFETY NET — if AI messes up, fall back to it

This layer is optional. The parametric SVG alone is usable. Enhancement adds
visual polish but accuracy is never at risk.

### Step 4: BACKGROUND ASSET PLANNING
- Input: Settings inventory from Step 2
- Backgrounds are EASIER than characters: they don't need cross-panel consistency
  (different scenes = different backgrounds). They just set atmosphere.

**Background tiers (decide per setting):**
  - **Tier 0 — Skip**: No background. Solid white or character's color behind them.
    Use for: pure dialogue, emotional close-ups. Most panels use this.
  - **Tier 1 — Solid/gradient**: CSS gradient or flat color. Warm amber for interiors,
    dark blue for night, grey for tension. Zero generation cost.
  - **Tier 2 — Simple SVG scenery**: Line-art buildings, simple table, window frame.
    Claude writes these — simple shapes work fine for backgrounds (unlike characters).
  - **Tier 3 — DrawThings AI**: For establishing shots and atmosphere ONLY.
    Generic bar interior, cityscape, forest, sky. Never for specific spatial layouts.

**Style consistency between backgrounds and characters:**
  Characters are bold-outlined SVGs. Backgrounds must not clash.
  - Tier 0-1: Automatic — solid colors can't clash with anything
  - Tier 2: SVG backgrounds use same line weight as characters → unified
  - Tier 3 (AI): Apply CSS filters to AI backgrounds to harmonize:
    `filter: contrast(1.1) saturate(0.7) opacity(0.85)`
    Plus slight blur to push backgrounds visually behind sharp character outlines.
    This "background recession" makes characters pop and hides AI inconsistencies.

**DrawThings background rules (unchanged):**
  - NEVER use for: object interactions, directional movement, spatial relationships
  - ALWAYS pin seed. Save once, reference forever.
  - Use Flux with same style preamble as character enhancement (if used)
  - Best for: establishing shots, atmosphere, texture overlays
- AI budget: Only the DrawThings calls for qualifying Tier 3 backgrounds

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
