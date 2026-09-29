# assemble-character.py — Assembles a character from SVG components
# Usage: python3 assemble-character.py <character-spec.json> <output.svg>
# Requires: Python 3 stdlib only (no external deps)
#
# Takes a JSON spec file describing which components to use and what colors
# to apply, reads individual SVG component files, composites them into one
# SVG with proper layering and color variables.
#
# Spec format:
# {
#   "name": "Red Schuhart",
#   "body": "adult-male",
#   "head": "square",
#   "hair": "male-messy",
#   "eyes": "squinting",
#   "nose": "large",
#   "mouth": "smirk",
#   "brows": "furrowed",
#   "clothing": "jacket",
#   "facial_hair": "stubble",
#   "accessories": ["cigarette"],
#   "special": [],
#   "colors": {
#     "skin": "#e8c39e",
#     "hair": "#c0392b",
#     "eye_color": "#5a6e28",
#     "clothing_primary": "#3d6b4f",
#     "clothing_secondary": "#888",
#     "accessory_color": "#333"
#   }
# }
#
# Gotchas:
# - Components must all use the same 200x400 viewBox
# - Layer order matters: body → clothing → head → hair → face features → accessories → special
# - CSS custom properties (var(--skin)) are set via style attribute on root <g>
# - Some components need the head to be drawn first (eyes, nose, mouth sit on it)

import json
import sys
import os
import re

COMPONENTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "components")

LAYER_ORDER = [
    ("bodies", "body"),
    ("clothing", "clothing"),
    ("heads", "head"),
    ("hair", "hair"),
    ("facial-hair", "facial_hair"),
    ("eyes", "eyes"),
    ("noses", "nose"),
    ("mouths", "mouth"),
    ("brows", "brows"),
    ("accessories", "accessories"),
    ("special", "special"),
]

def extract_inner_svg(svg_content):
    """Extract the content between <svg> tags, removing the wrapper."""
    match = re.search(r'<svg[^>]*>(.*)</svg>', svg_content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return svg_content

def load_component(category_dir, component_name):
    """Load an SVG component file and return its inner content."""
    path = os.path.join(COMPONENTS_DIR, category_dir, f"{component_name}.svg")
    if not os.path.exists(path):
        print(f"  WARNING: Component not found: {path}")
        return None
    with open(path, 'r') as f:
        return extract_inner_svg(f.read())

def build_color_style(colors):
    """Build CSS custom property string from color dict."""
    props = []
    mapping = {
        "skin": "--skin",
        "hair": "--hair",
        "eye_color": "--eye-color",
        "clothing_primary": "--clothing-primary",
        "clothing_secondary": "--clothing-secondary",
        "accessory_color": "--accessory-color",
        "fur_color": "--fur-color",
    }
    for key, css_var in mapping.items():
        if key in colors:
            props.append(f"{css_var}: {colors[key]}")
    return "; ".join(props)

def assemble(spec):
    """Assemble a character SVG from a spec dict."""
    colors = spec.get("colors", {})
    style_str = build_color_style(colors)

    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 400" width="400" height="800">')
    parts.append(f'  <!-- Character: {spec.get("name", "unnamed")} -->')
    parts.append(f'  <g style="{style_str}">')

    for category_dir, spec_key in LAYER_ORDER:
        value = spec.get(spec_key)
        if not value:
            continue

        if isinstance(value, list):
            for item in value:
                content = load_component(category_dir, item)
                if content:
                    parts.append(f'    <!-- {category_dir}/{item} -->')
                    parts.append(f'    {content}')
        else:
            content = load_component(category_dir, value)
            if content:
                parts.append(f'    <!-- {category_dir}/{value} -->')
                parts.append(f'    {content}')

    parts.append('  </g>')
    parts.append('</svg>')

    return '\n'.join(parts)

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 assemble-character.py <spec.json> <output.svg>")
        print("  spec.json: Character specification (components + colors)")
        print("  output.svg: Where to write the assembled character")
        sys.exit(1)

    spec_path = sys.argv[1]
    output_path = sys.argv[2]

    if not os.path.exists(spec_path):
        print(f"ERROR: Spec file not found: {spec_path}")
        sys.exit(1)

    with open(spec_path) as f:
        spec = json.load(f)

    print(f"Assembling: {spec.get('name', 'unnamed')}")
    print(f"  Body: {spec.get('body')}")
    print(f"  Head: {spec.get('head')}")
    print(f"  Hair: {spec.get('hair')}")
    print(f"  Eyes: {spec.get('eyes')}")
    print(f"  Clothing: {spec.get('clothing')}")

    svg = assemble(spec)

    with open(output_path, 'w') as f:
        f.write(svg)

    print(f"Output: {output_path} ({len(svg)} bytes)")

if __name__ == "__main__":
    main()
