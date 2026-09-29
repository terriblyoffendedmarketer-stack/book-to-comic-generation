# verify-character.py — Scores a generated character image against trait checklist
# Usage: python verify-character.py <image-path> <traits-json>
# Requires: anthropic SDK (pip install anthropic)
#
# Takes a generated character image and a JSON trait checklist, uses Claude vision
# to score each trait as PASS/FAIL/PARTIAL. Returns structured results.
#
# This is the verification half of the generate-verify loop (Step 3a in APPROACH.md).
# The generation half uses DrawThings MCP. This script validates the output.
#
# Gotchas:
# - VTracer Python bindings crash on Python 3.14 (SIGSEGV). Use Python 3.12.
# - SDXL commonly drops: negation ("no whites"), rare features (fur on skin),
#   unusual color combos (golden hair on a child). These are the traits most
#   likely to need retries.
# - Claude vision is very reliable at recognition — the bottleneck is generation,
#   not verification.

import json
import sys
import base64
import os

def load_image_as_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8")

def get_media_type(image_path):
    ext = os.path.splitext(image_path)[1].lower()
    return {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".gif": "image/gif",
    }.get(ext, "image/png")

def build_verification_prompt(traits):
    lines = ["You are evaluating a character design image against a trait checklist.",
             "For each trait, determine if the image matches the expected description.",
             "Be strict — 'close enough' is not PASS for critical traits.",
             "",
             "Score each trait as:",
             "- PASS: The trait is clearly visible and matches the description",
             "- FAIL: The trait is missing, wrong, or contradicts the description",
             "- PARTIAL: The trait is somewhat present but not fully matching",
             "",
             "Traits to check:"]

    for i, trait in enumerate(traits, 1):
        priority = trait.get("priority", "important")
        lines.append(f"{i}. [{priority.upper()}] {trait['name']}: expected \"{trait['expected']}\"")

    lines.extend([
        "",
        "Respond in JSON format:",
        '{',
        '  "scores": [',
        '    {"name": "<trait_name>", "score": "PASS|FAIL|PARTIAL", "observed": "<what you actually see>", "suggestion": "<how to fix if FAIL>"}',
        '  ],',
        '  "overall": "ACCEPT|RETRY|INPAINT",',
        '  "summary": "<one sentence summary>",',
        '  "prompt_adjustments": ["<specific prompt changes to try on retry>"]',
        '}'
    ])

    return "\n".join(lines)

def verify_character(image_path, traits, api_key=None):
    try:
        import anthropic
    except ImportError:
        print("ERROR: anthropic SDK not installed. Run: pip install anthropic")
        sys.exit(1)

    if api_key is None:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: Set ANTHROPIC_API_KEY environment variable")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    image_data = load_image_as_base64(image_path)
    media_type = get_media_type(image_path)
    prompt = build_verification_prompt(traits)

    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": media_type,
                        "data": image_data,
                    }
                },
                {
                    "type": "text",
                    "text": prompt
                }
            ]
        }]
    )

    response_text = response.content[0].text

    # Extract JSON from response (may be wrapped in markdown code block)
    if "```json" in response_text:
        response_text = response_text.split("```json")[1].split("```")[0]
    elif "```" in response_text:
        response_text = response_text.split("```")[1].split("```")[0]

    return json.loads(response_text.strip())

def main():
    if len(sys.argv) < 3:
        print("Usage: python verify-character.py <image-path> <traits-json-file>")
        print("  traits-json-file: JSON array of {name, expected, priority} objects")
        sys.exit(1)

    image_path = sys.argv[1]
    traits_path = sys.argv[2]

    if not os.path.exists(image_path):
        print(f"ERROR: Image not found: {image_path}")
        sys.exit(1)

    with open(traits_path) as f:
        traits = json.load(f)

    print(f"Verifying {os.path.basename(image_path)} against {len(traits)} traits...")
    result = verify_character(image_path, traits)

    print("\n=== VERIFICATION RESULTS ===")
    for score in result.get("scores", []):
        icon = {"PASS": "✓", "FAIL": "✗", "PARTIAL": "~"}.get(score["score"], "?")
        print(f"  {icon} {score['name']}: {score['score']}")
        print(f"    Expected: (see traits)")
        print(f"    Observed: {score['observed']}")
        if score.get("suggestion"):
            print(f"    Fix: {score['suggestion']}")

    print(f"\nOverall: {result.get('overall', 'UNKNOWN')}")
    print(f"Summary: {result.get('summary', '')}")

    if result.get("prompt_adjustments"):
        print("\nPrompt adjustments for retry:")
        for adj in result["prompt_adjustments"]:
            print(f"  → {adj}")

    # Also dump raw JSON for pipeline consumption
    print(f"\n=== RAW JSON ===")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
