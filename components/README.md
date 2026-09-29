# Component Library — Parametric SVG Character Assembly
# Style: Bold Outlined (Persepolis/Tintin-inspired)
# Coordinate system: all components use a 200x400 viewBox
#   - (100,0) is top center of character
#   - Head centered at (100, 60), radius ~40
#   - Body starts at y=120, ends at y=380
#   - Components are layered: body → clothing → head → hair → face features → accessories
#
# Color convention:
#   - Fill colors use CSS custom properties: var(--skin), var(--hair), var(--clothing-primary)
#   - Fallback values provided for standalone viewing
#   - Stroke is always #1a1a1a (near-black), width 2.5px
#
# Usage:
#   1. Pick one body template
#   2. Pick one head shape
#   3. Pick one hairstyle (set --hair color)
#   4. Pick eyes, nose, mouth, brows
#   5. Add clothing, accessories, special features
#   6. Wrap in container SVG with color variables on root
#
# Gotchas:
# - Hair components include the scalp area — they sit ON TOP of the head shape
# - Eye/nose/mouth positions are relative to the head shape center (100, 60)
# - Clothing overlaps the body template from y=120 down — body provides the shape,
#   clothing provides the visible fill
# - Use stroke-linejoin="round" everywhere for the rounded Persepolis look
