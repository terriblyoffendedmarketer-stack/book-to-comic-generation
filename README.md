# Book to Comic Generation

Convert any book (EPUB, PDF, or plain text) into a comic book using Claude Code.

## What This Is

A Claude Code skill + supporting scripts that take a book and produce a readable HTML comic. Feed it an EPUB, and it walks through a structured multi-pass pipeline to produce comic pages with proper storytelling, character consistency, and faithful dialogue adaptation.

## Art Modes

| Mode | How It Works | Best For |
|------|-------------|----------|
| **A: SVG** | Deterministic SVG character shapes — same shapes every panel | Long-form, guaranteed consistency |
| **B: DrawThings** | AI-generated panels via local DrawThings MCP | Rich cinematic art, shorter works |
| **C: Hybrid** | AI backgrounds + SVG character overlays | Best of both (recommended) |

## Pipeline

1. **Extract** — Pull clean text from EPUB/PDF
2. **Structure Map** — Understand the whole book's arc
3. **Beat Maps** — Scene-by-scene breakdown with key dialogue
4. **Character Bible** — Every character with personality, speech patterns, visual design
5. **Character Design** — Visual references (SVG sheets / AI-generated refs)
6. **Panel Scripts** — Detailed script for every page before any art
7. **Page Production** — Build HTML comic pages
8. **Assembly** — Navigable reader with all pages

## Getting Started

### Install the Skill

Copy `SKILL.md` to your Claude Code skills directory:

```bash
mkdir -p ~/.claude/skills/book-to-comic
cp SKILL.md ~/.claude/skills/book-to-comic/SKILL.md
```

### Use It

In any Claude Code session, provide a book and ask to make a comic:

> "Here's an EPUB in my Downloads folder. Turn it into a comic."

The skill triggers automatically and walks through each pass.

### Extract Text Manually

```bash
python3 scripts/extract-epub.py ~/Downloads/my-book.epub extracted/
```

## Project Structure

```
├── SKILL.md                          # The skill file (install to ~/.claude/skills/)
├── scripts/
│   └── extract-epub.py               # EPUB text extraction (Python 3, no deps)
├── templates/
│   ├── page-template.html            # Starter HTML template for comic pages
│   └── character-templates.svg       # SVG body types, expressions, accessories
└── examples/
    └── roadside-picnic-comic/        # Prototype: Roadside Picnic adaptation
        ├── CLAUDE.md                  # Project status for the prototype
        ├── REVISION-NOTES.md          # Lessons learned from prototype review
        ├── reader.html               # Combined reader
        ├── pages/                    # Produced comic pages
        └── characters/               # Character reference SVGs
```

## Requirements

- **Claude Code** with tool access (Read, Write, Edit, Bash)
- **Python 3** (standard library only — no pip packages needed)
- **DrawThings** (optional, for Mode B/C AI-generated art) — requires DrawThings MCP server

## Example Output

The `examples/roadside-picnic-comic/` directory contains a prototype adaptation of *Roadside Picnic* by Arkady & Boris Strugatsky. Open `reader.html` in a browser to see the comic pages.

## Key Lessons (from prototype)

- Panel size is the bottleneck, not font size — when text feels cramped, make the panel bigger
- Never skip planning passes — jumping to production loses story beats and character voice
- Dialogue adaptation is the hardest part — preserve the character's actual word choices and wit
- 6 panels max per page — going over always hurts readability
- Chapters can be long in comic form — 15-25 pages for a dense chapter is fine
- Always preview in browser before moving on
