# Mistakes & Lessons Learned
# For any new chat/session — read this FIRST before doing any work.

## Mistake 1: Building pages before solidifying the approach
**What happened**: Jumped straight into producing 12 pages (3 prologue + 9 chapter 1) with
an unproven layout system, SVG characters, and DrawThings backgrounds.
**Why it was wrong**: Each page was a one-off with manual pixel positioning. None of it was
reusable. When problems were found (bubble overlap, bad characters, broken backgrounds),
fixing one page didn't fix the others.
**Do instead**: Design the complete system on paper first. Get one page perfect as a
template. Only then scale.

## Mistake 2: DrawThings for complex/directional scenes
**What happened**: Used DrawThings SDXL to generate backgrounds for scenes that require
specific spatial relationships — e.g., "a bolt hitting a globe," "characters walking in
a specific direction." The results were useless — AI image generation cannot reliably
produce images with correct spatial/directional composition.
**Why it was wrong**: SDXL is a diffusion model. It generates plausible-looking images but
has no understanding of physics, direction, or spatial relationships. A "bullet hitting a
globe" looked nothing like that.
**Do instead**: Use DrawThings ONLY for generic/ambient backgrounds where accuracy doesn't
matter: sky, abstract atmosphere, simple room interior, landscape, texture. For anything
requiring spatial accuracy (object interactions, directions, specific compositions),
use simplified SVG illustrations or just skip the background entirely.

## Mistake 3: One-size-fits-all character expressions
**What happened**: Created a character template system with 7 generic expressions and 6
accessories, applied uniformly to all characters.
**Why it was wrong**: Not every character needs 7 expressions. The book text determines
what expressions exist. Character A might show 10 different emotions across the book
while Character B might only appear stoic throughout. Making 7 expressions for both
wastes effort and misses the ones actually needed.
**Do instead**: First pass — analyze the ENTIRE book. For each character, extract every
emotion/expression actually described. Build exactly those, nothing more, nothing less.

## Mistake 4: Speech bubbles positioned with absolute CSS over character art
**What happened**: Used `position: absolute` to place speech bubbles on top of character
SVGs. Required per-pixel manual adjustment per panel, and bubbles frequently obscured
character faces.
**Why it was wrong**: Not templatizable. Every panel needed custom coordinates. Any
change to character or panel size broke the bubble positions.
**Do instead**: Zone-based layout — speech zone (top, CSS flexbox) and art zone (bottom)
are separate containers. Bubbles flow in reading order within their zone. Characters
live in art zone below. No overlap is structurally possible.

## Mistake 5: SVG characters too simplistic without key identifiers
**What happened**: Characters were basic geometric shapes — circle head, rectangle body.
Multiple characters in the same outfit (red hazmat suits) were indistinguishable.
**Why it was wrong**: The visual storytelling failed. Reader can't tell who's talking.
**Do instead**: Every character needs 2-3 KEY visual identifiers that persist across all
appearances. Even in matching uniforms: Red = red hair + stocky, Kirill = glasses + thin,
Tender = round + big worried eyes. These identifiers come from the book's character
descriptions — mine the text for them.

## Mistake 6: Regenerating DrawThings images
**What happened**: Re-running DrawThings generation produced different images each time,
even with similar prompts. Wasted time trying to get consistency.
**Why it was wrong**: Diffusion models are stochastic. Same prompt ≠ same image unless
you pin the seed AND use identical parameters.
**Do instead**: Generate once with a pinned seed. Save the image. Reference it by file
path forever. Never regenerate. If you need a variation, use a different seed.

## Mistake 7: Not analyzing the book deeply enough before production
**What happened**: Created beat maps and scripts, but didn't do a thorough inventory of
all characters, all expressions, all settings, and all character interactions across the
entire book.
**Why it was wrong**: Discovered missing expressions and settings mid-production. Had to
backtrack and create assets ad-hoc.
**Do instead**: The VERY FIRST step is a complete book inventory:
- Every character + their frequency + their described emotions/expressions
- Every unique setting/location
- Every character pairing (who talks to whom and how often)
- Scene types: dialogue, action, establishing, montage
Only then plan assets.

## Mistake 8: Asset paths broke when pages moved to subdirectory
**What happened**: Pages referenced `assets/foo.png` but pages were in `pages/` subdirectory.
All background images 404'd.
**Why it was wrong**: Should have used relative paths (`../assets/`) from the start, or a
base URL system.
**Do instead**: Always use paths relative to the page's actual location. Or use a CSS
variable for the asset root.

## Mistake 9: Not reusing panel compositions for dialogue scenes
**What happened**: Every panel was unique — new character placement, new background, new
composition. Even simple dialogue exchanges got unique layouts.
**Why it was wrong**: Real comics reuse the same "two-shot" or "close-up" composition
across multiple panels in a conversation. Only the speech bubbles change. This is faster
to produce AND easier to read.
**Do instead**: For dialogue sequences, create ONE panel composition (characters + background)
and reuse it across 2-4 panels with only the speech bubbles changing. This is standard
comic practice and massively reduces asset creation.

## Mistake 10: Starting from scratch each session
**What happened**: Context loss between chat sessions meant re-deriving decisions already made.
**Why it was wrong**: Wasted tokens and time on the same dead ends.
**Do instead**: This file exists. Read it. The CLAUDE.md has the current state. The
approach document has the plan. Don't re-derive.
