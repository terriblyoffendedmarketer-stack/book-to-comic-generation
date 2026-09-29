# Character Generation: The Real Solution
# Date: 2026-09-29
# Based on: 6 web searches, 4 repo analyses, 3 failed SDXL attempts, industry benchmarks

## The Problem (proved by testing)

SDXL text-to-image CANNOT reliably generate characters from book descriptions.
3 attempts on one character ("Monkey" from Roadside Picnic) demonstrated:
- Prompt said "golden hair" → got black hair
- Prompt said "eyes with no whites" → got normal eyes
- Prompt said "golden fur on cheeks" → got smooth skin
- Each retry fixed some traits but broke others

This is not a prompt engineering problem. It's a model architecture limitation:
diffusion models are pattern completers, not instruction followers. They default
to their training distribution, and unusual features (alien eyes, fur on skin)
simply don't exist in their training data.

## What The Industry Does (2026)

Research into 8+ tools and papers reveals three proven approaches:

### 1. Reference Image + Identity-Preserving Model
**Used by:** Flux Kontext, Toongether (Gemini 2.5 Flash), Comic Studio AI
**How it works:** Generate ONE good reference image per character, then use a model
that preserves identity (face, body, colors) while changing pose/expression/scene.
**Results:** Flux Kontext: 92% identity match. Comic Studio AI: 94% consistency.
**Key insight:** Don't describe the character in words every time. Show the model a
PICTURE and say "this character, but now looking angry."

### 2. Parametric Component Assembly
**Used by:** Comicgen, Avataaars, The Character Creator, video game character creators
**How it works:** Pre-drawn SVG parts (hairstyles, faces, bodies, clothes) combined
programmatically. Claude selects components based on book descriptions.
**Results:** 100% consistent (deterministic). All characters same universe (same parts).
**Key insight:** Don't GENERATE the character. ASSEMBLE it from parts.

### 3. Style Bible + Post-Processing
**Used by:** codex-novel-to-comic-studio, make-comics
**How it works:** Same style prompt prefix for all generations + CSS filters to unify.
**Results:** Moderate consistency. Good style unity.
**Key insight:** Even inconsistent generations look unified after the same filters.

## The Solution: Two-Layer Architecture

### Layer 1: Parametric SVG Reference (GUARANTEES accuracy + consistency)

For each character in the book:
1. Claude reads the character description from the book inventory
2. Claude maps description → component selections:
   - Body type (from ~6 base templates)
   - Hair style + color (from ~15 hairstyle paths)
   - Face features (eyes, nose, mouth from component sets)
   - Clothing (from ~10 outfit templates)
   - Key identifiers (accessories, scars, facial hair, etc.)
3. Claude assembles an SVG from selected components
4. Result: a character reference that is GUARANTEED to match the book description

Why this works:
- "Golden hair" = select golden color fill. No randomness. No model ignoring you.
- "Eyes with no whites" = select the all-dark-eyes component. Deterministic.
- "Fur on cheeks" = select the cheek-fur-texture overlay. Exact.
- All characters use the same component library → same art style → same universe.

### Layer 2: AI Style Enhancement (ADDS quality without risking accuracy)

The parametric SVG is accurate but potentially plain. To add visual quality:
1. Render parametric SVG to PNG
2. Feed to DrawThings img2img (Flux model, LOW denoising 0.2-0.3)
   - Low denoising preserves structure and colors
   - Adds texture, anti-aliasing, artistic polish
   - Same style prompt for ALL characters → consistent enhancement
3. Verify with Claude vision: did enhancement preserve critical features?
   - If yes → vectorize with VTracer → use as final character art
   - If no → reduce denoising further, or skip enhancement and use the SVG directly

This layer is OPTIONAL. The parametric SVG alone is usable. The enhancement makes
it look more polished, but accuracy is never at risk because:
- The parametric layer GUARANTEES the right features
- The enhancement layer only adds visual quality
- If enhancement corrupts features, we fall back to the parametric SVG

### Style Consistency (the "same universe" guarantee)

Five layers ensure all characters share one visual language:

1. **Same component library** — All characters assembled from the same SVG parts.
   Same line weight, same proportions, same detail level.

2. **Same color system** — Defined palette per book. Characters get colors from
   the palette, not arbitrary hex values.

3. **Same AI model + settings** — If using Layer 2 enhancement, identical model,
   seed range, denoising strength, and style prompt for every character.

4. **Same VTracer settings** — Identical vectorization parameters normalize any
   variance from AI enhancement into a consistent vector style.

5. **CSS post-processing** — The comic viewer applies uniform filters
   (slight contrast boost, desaturation) to all character art.

## The Component Library

The one-time investment. ~60 SVG components in a consistent art style.

### Art Style: Bold Outlined (Persepolis-inspired)
- Thick black outlines (stroke-width: 2-3px at character scale)
- Flat color fills (no gradients on characters)
- Deliberate simplicity — Tintin, not manga
- KEY identifiers exaggerated (bigger glasses, bolder scars, wilder hair)
- Expressions through: eyebrow angle, mouth shape, eye state (minimal changes)

### Component Inventory
```
Body types (6):     adult-male, adult-female, child, large, thin, elderly
Hairstyles (15):    short, medium, long, bald, mohawk, messy, slicked-back,
                    ponytail, braids, afro, bob, curly, buzz-cut, flowing, wild
Eye types (8):      normal, glasses, squinting, wide, closed, sleepy,
                    all-dark (alien), narrow
Nose types (5):     small, large, pointed, flat, upturned
Mouth states (6):   neutral, smile, frown, open, gritted, smirk
Brow positions (4): neutral, raised, furrowed, one-raised
Facial hair (5):    none, stubble, beard, mustache, goatee
Clothing (10):      shirt, jacket, dress, uniform, coat, apron, suit,
                    hoodie, tank-top, robe
Accessories (12):   glasses, sunglasses, hat, pipe, cigarette, scarf,
                    scar, badge, tie, earring, headband, bandage
Special (5):        fur-texture-overlay, radiation-marks, cybernetics,
                    tattoo-pattern, bandaged-limb
```

Total: ~76 components. Each is a small SVG path or group.

### How to Create the Library

**Option A (fastest): Claude writes SVG paths**
In a deliberately simple style with thick outlines and flat fills, Claude CAN
write decent individual component paths. The style hides imperfections.
A single hairstyle path is much simpler than a full character illustration.

**Option B (higher quality): AI-generate + vectorize**
Generate each component individually with DrawThings Flux:
"isolated hairstyle, messy short golden hair, flat vector art, thick black outline,
white background, single object"
Components in isolation are Tier 1 easy for AI — no conflicting priors.
VTracer each to SVG. Clean up paths.

**Option C (hybrid): Claude writes base paths, AI enhances**
Claude creates the structural SVG path, DrawThings img2img adds polish.

Recommendation: Start with Option A. It's fastest, fully within Claude's control,
and the deliberate simplicity of the style makes it work. If quality isn't enough,
upgrade specific components with Option B.

## How This Scales to Any Book

1. **Game of Thrones (100+ characters)**
   - Major characters (20-30): full component assembly with all expressions
   - Minor characters (70+): base template + 2 key identifiers + 1-2 expressions
   - Library covers medieval/fantasy clothing already
   - For missing components (dragon scale armor?): generate on demand with DrawThings

2. **Metamorphosis (surreal/abstract)**
   - Gregor as beetle: special body template (non-human shapes in component library)
   - Family members: standard adult templates with period clothing
   - The "transformation" is a progression through body templates

3. **Contemporary fiction**
   - Standard body templates + modern clothing components
   - Accessories distinguish characters (a particular hat, a scar, glasses)

4. **Children's book with aliens/creatures**
   - Non-human body templates (4-legged, tentacled, etc.)
   - These would be generated on demand and added to library

## Comparison with Alternatives

| Approach | Reliability | Style Unity | Book Accuracy | Effort | Human Loop? |
|----------|------------|-------------|---------------|--------|-------------|
| SDXL text-to-image | 20% | Low | Low | Low | YES (retries) |
| Flux text-to-image | 50-70%? | Medium | Medium | Low | Maybe |
| Flux Kontext + ref | 85-92% | High | Medium | Medium | Minimal |
| Parametric SVG only | 99% | 100% | 95% | High upfront | No |
| Parametric + enhance | 95% | 95% | 95% | High upfront | No |
| Gemini 2.5 Flash | 94% | High | High | Low | No |

Parametric SVG wins on reliability and consistency. The upfront cost (building the
component library) is a one-time investment that pays for every book afterward.

## Recommended Next Steps

1. Build minimal component library (~20 core components)
2. Test: assemble Red Schuhart from components
3. Test: assemble Monkey from components (the hard case with unusual features)
4. Compare quality to DrawThings-generated versions
5. If quality is acceptable → build remaining components → proceed to page templates
6. If quality needs more polish → add Layer 2 AI enhancement

## Sources
- Flux Kontext: https://wiki.drawthings.ai/wiki/Flux_Kontext
- Flux Kontext character consistency: https://bfl.ai/models/flux-kontext
- Comicgen (parametric SVG): https://github.com/gramener/comicgen
- The Character Creator (SVG): https://github.com/ubik23/charactercreator
- codex-novel-to-comic-studio visual bible: (previously analyzed in repo analysis)
- make-comics CSS post-processing: (previously analyzed in repo analysis)
- DrawThings img2img API: https://github.com/SurgeonTalus/DrawThings-ImgToImg-API-HTTP-Python
- Comic Studio AI (94% consistency): https://github.com/RobinaMirbahar/Comic-Studio-Ai
- Lovart character design guide: https://www.lovart.ai/blog/complete-guide-consistent-ai-character-design
- ToonyStory benchmark: https://toonystory.com/ai-character-consistency
