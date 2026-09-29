# AI SVG Generation Tools Research
# Date: 2026-09-21
# Purpose: Find tools to generate more expressive SVG character art for comics

## Problem
Our hand-coded Persepolis-style SVG characters are too simplified. We need more
expressive character illustrations while keeping the deterministic/modular benefits
of SVG (no drift, reusable parts, expression swapping).

## Tools Investigated (7 total)

### Tier 1: Purpose-Built SVG Models

**OmniSVG** (NeurIPS 2025) — https://github.com/OmniSVG/OmniSVG
- Built on Qwen2.5-VL, trained on 2M SVG dataset including anime characters
- 4B and 8B parameter models on HuggingFace (Apache 2.0)
- The ONLY model that targets character-level SVG generation
- **Mac feasibility: Poor.** 3B model needs 17GB VRAM, CUDA 12.1 required.
  Might work via CPU inference on high-memory M-series but extremely slow.
  No official MPS support.
- **Verdict: BEST quality, but can't run locally on Mac today.**
  Worth revisiting if we get cloud GPU access.

**StarVector** (CVPR 2025) — https://github.com/joanrod/star-vector
- Vision Transformer + StarCoder decoder for SVG code generation
- **Explicitly NOT trained for illustrations.** Icons, logos, diagrams only.
- CUDA-only. **Verdict: Dead end for our use case.**

### Tier 2: Diffusion/Optimization-Based

**SVGDreamer** (CVPR 2024) — https://github.com/ximinng/SVGDreamer
- Diffusion-guided optimization of SVG paths using Stable Diffusion 2.1
- Produces painterly blobs, not clean line art — wrong style for comics
- Hard CUDA 11.3 dependency, Ubuntu-only install
- **Verdict: No. CUDA-locked + wrong output style.**

**svg-generator (JosefKuchar)** — https://github.com/JosefKuchar/svg-generator
- Two-stage: raster generation with LoRA → vectorization
- CUDA-dependent, Python 3.13 + FlashAttention
- **Verdict: No. CUDA-locked + auto-traced output, not clean art.**

### Tier 3: LLM-Based Code Generation

**Text2SVG (CTLab-ITMO)** — https://github.com/CTLab-ITMO/Text2SVG
- Fine-tuned Qwen2.5-Coder-32B to output SVG code
- Mac-portable in theory (just PyTorch + Transformers, 20GB RAM for 4-bit)
- BUT: output quality tops out at icon-level, not characters
- **Verdict: Maybe for simple elements, not for character art.**

**SVG ORA Studio** — https://github.com/SVG-ORA-Studio
- React UI wrapper that sends prompts to cloud LLMs (Gemini, OpenRouter)
- Not a local model at all — just "ask an LLM to write SVG" with nice UI
- **Verdict: Skip. We already have Claude.**

### Tier 4: Our Own Tools (Most Practical)

**Claude SVG Generation (improved prompting)**
- Claude already generates flat vector illustrations well
- Cartoon characters are the weak spot: "disconnected shapes, off proportions"
- BUT with iterative refinement and style-locked prompting, quality is moderate
- Key prompting techniques: name the style explicitly, set palette, use
  `<defs>` and `<use>`, iterate one change at a time
- **Verdict: TRY FIRST. Zero cost, we're already using Claude.**

**DrawThings + VTracer Pipeline**
- Generate character PNG with SD (flat-color/cel-shaded style)
- Vectorize with VTracer (Rust, open source, runs locally, full-color)
- Produces faithful SVGs but they're opaque traced paths — can't easily
  swap expressions by editing SVG elements
- **Verdict: TRY SECOND for base character poses. Won't work for
  expression swapping (our core modular design).**

## Ranked Approach for Our Pipeline

1. **Claude with structured prompting** — Try immediately. Generate a
   test character (e.g. Monkey) with detailed art direction prompts.
   Compare quality to our current hand-coded SVGs. Zero setup cost.

2. **DrawThings → VTracer for REFERENCE ART** — Generate raster character
   reference sheets, vectorize them, then use the traced SVGs as visual
   guides while hand-refining the modular expression system.

3. **OmniSVG via cloud GPU** — If we need production-quality character
   SVGs and have access to a GPU server or Google Colab, this is the
   best model. 4B version on HuggingFace.

4. **Hybrid approach** — Use OmniSVG or DrawThings+VTracer to generate
   a detailed base character, then manually extract modular `<defs>`
   parts (head, body, hair) and create expression variants from that
   higher-quality base.

## Key Insight
The fundamental tension: expressive AI-generated SVGs are opaque (traced paths,
no semantic structure), while our modular system (named `<defs>`, swappable
expressions) requires semantic structure. The best path forward is probably
a hybrid: AI generates high-quality reference art → we build modular SVGs
from that reference, using the AI output as a visual quality target rather
than a direct drop-in.

## About svgs.app
No public disclosure of tech stack. Appears to use the same LLM-writes-SVG
approach with polished prompt engineering and a custom UI. Nothing proprietary
or replicable beyond what we can do with Claude directly.
