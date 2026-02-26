---
name: pptx-drawio-builder
description: "Programmatic PPTX presentation builder using drawio for complex diagrams and python-pptx for slide assembly. Cross-platform (Linux/macOS/Windows). Use when: (1) creating slide decks or presentations with complex diagrams, flowcharts, or architecture visuals, (2) building academic or technical presentations programmatically, (3) user mentions drawio + pptx workflow, diagram-to-slide pipeline, or EMF embedding, (4) user wants to generate repeatable, version-controlled presentations from code. Covers the full pipeline: write .drawio XML files directly → drawio Desktop CLI export to EMF/PNG → python-pptx script for slide composition with design tokens, helpers, and speaker notes."
---

# PPTX + Drawio Builder

Build presentation decks programmatically: write `.drawio` XML files directly, export via drawio Desktop CLI, assemble slides with python-pptx. Cross-platform: Linux, macOS, Windows.

## Workflow Overview

```
1. Diagram Authoring    Write .drawio XML files directly (mxGraphModel format)
        ↓
2. Export Pipeline      drawio CLI → PDF → SVG → EMF (vector) or direct PNG
        ↓
3. Slide Assembly       python-pptx script with design tokens + helpers
        ↓
4. Output               .pptx with embedded diagrams, videos, speaker notes
```

## Step 1: Diagram Authoring

Write `.drawio` files directly as XML. See `references/drawio-style.md` for the complete design guide including color palette, typography, arrow routing rules, and layout patterns.

Quick example:

```xml
<mxfile>
  <diagram name="Page-1">
    <mxGraphModel dx="1422" dy="800" grid="1" gridSize="10">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <mxCell id="2" value="Module A" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#EFF6FF;strokeColor=#3B82F6;fontFamily=微软雅黑;fontSize=14;fontStyle=1;fontColor=#0F172A;arcSize=12;" vertex="1" parent="1">
          <mxGeometry x="100" y="100" width="180" height="70" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

Key practices:
- IDs start from "2" (0 and 1 are reserved root cells)
- Set `fontFamily=微软雅黑` in every cell style (Windows default; swap for your platform)
- Use `source` and `target` on edges with explicit `exitX/exitY/entryX/entryY` to prevent crossing
- Two arrow styles: orthogonal (straight 90° turns) or curved corners (`curved=1;rounded=1`)
- The `.drawio` file is the version-controlled source of truth

## Step 2: Export Pipeline

### Cross-Platform drawio CLI Paths

```
Linux:   drawio  (or /usr/bin/drawio, /opt/drawio/drawio)
macOS:   /Applications/draw.io.app/Contents/MacOS/draw.io
Windows: "C:\Program Files\draw.io\draw.io.exe"
```

### Export Options

Direct PNG export (simplest, works everywhere):
```bash
drawio --export --format png --scale 2 --crop --output out.png diagram.drawio
```

EMF export for best PPTX quality (Linux only, requires pdftocairo + inkscape):
```bash
drawio --export --format pdf --crop --output out.pdf diagram.drawio
pdftocairo -svg out.pdf out.svg
inkscape out.svg --export-type=emf --export-filename=out.emf
```

SVG export (cross-platform, good for web/preview):
```bash
drawio --export --format svg --crop --output out.svg diagram.drawio
```

Use `scripts/drawio_export.py` for cross-platform batch conversion with auto-detection of drawio CLI path and available toolchain.

### When to Use Which Format

| Format | Quality in PPTX | Cross-Platform | Dependencies |
|--------|-----------------|----------------|--------------|
| EMF    | Lossless vector | Linux only     | pdftocairo, inkscape |
| PNG    | Good (use --scale 2+) | All platforms | None |
| SVG    | Not embeddable in PPTX | All platforms | None |

Recommendation: Use EMF on Linux for maximum quality. Use PNG with `--scale 2` on macOS/Windows.

## Step 3: Slide Assembly with python-pptx

Run with: `uv run --no-project --with python-pptx --with Pillow python make_ppt.py`

Or on Windows/macOS: `pip install python-pptx Pillow && python make_ppt.py`

### Project Structure

```
project/
├── diagrams/          .drawio source files
├── assets/            images, videos, screenshots
├── build/
│   ├── make_ppt.py    slide assembly script
│   ├── *.emf / *.png  converted diagrams
├── build.sh           orchestration (Linux/macOS)
├── build.ps1          orchestration (Windows, optional)
└── output.pptx
```

### Slide Layout Drafts

See `references/layouts.md` for 17 ready-to-use layout templates (Clarity design system):

- Cover, Section Divider, TOC/Agenda, Closing
- Title + Bullets, Title + Full Diagram
- Two-Column (text+image, image+text)
- Two Cards, Three Cards (numbered)
- Stats Row, Timeline, Comparison Table
- Quote, Video Demo, Video + Side Cards
- Tags + Feature List

### Drawio Diagram Style Guide

See `references/drawio-style.md` for full-page diagram design rules:

- Coordinated color palette (Primary/Secondary/Tertiary/Neutral fills)
- Typography: 微软雅黑, size hierarchy 10-20pt
- Two arrow styles: orthogonal or curved-corner, with anti-crossing rules
- 5 layout patterns: Layered Architecture, Pipeline, Hub-and-Spoke, Comparison, Decision Tree
- Copy-paste ready style strings for all element types

### Design System ("Clarity")

### Design System ("Clarity")

Modern, minimal design. See `references/helpers.md` for the full helper library:

- `_tb` — textbox with font/color/alignment
- `title_area` — clean title + optional subtitle (no decorative bars)
- `img_fit` — insert image scaled to fit bounds, centered
- `card` / `accent_card` / `num_card` / `side_card` — minimal cards (surface fill, no borders)
- `tag` — outlined tag (not filled pill)
- `bullets` / `kv_list` — bullet lists and key-value lists
- `stat_block` — big accent number + label
- `timeline` — horizontal numbered steps with cards
- `add_table` — clean table with minimal styling
- `panel` / `divider` — tinted background area / thin separator
- `section_slide` / `new_slide` — slide constructors
- `embed_video` — embed MP4 with auto poster frame (requires ffmpeg)

### Speaker Notes

```python
notes = ["Note for slide 0", "Note for slide 1", ...]
for i, text in enumerate(notes):
    if i < len(prs.slides) and text:
        prs.slides[i].notes_slide.notes_text_frame.text = text
```

### Page Numbers (skip cover + closing)

```python
total = len(prs.slides)
for idx, slide in enumerate(prs.slides):
    if idx == 0 or idx == total - 1:
        continue
    _tb(slide, 12.2, 7.0, 0.8, 0.4, str(idx), size=14, color=ACCENT, align=PP_ALIGN.RIGHT)
```

## Step 4: Build Orchestration

Use `scripts/drawio_export.py` (cross-platform Python) or `scripts/drawio_to_emf.sh` (Linux/macOS bash):

```bash
# Python (cross-platform)
python scripts/drawio_export.py diagrams/ build/ --format png --scale 2
python scripts/drawio_export.py diagrams/ build/ --format emf          # Linux only
python scripts/drawio_export.py diagrams/ build/ --filter p4           # selective

# Bash (Linux/macOS)
scripts/drawio_to_emf.sh diagrams/ build/
scripts/drawio_to_emf.sh diagrams/ build/ p4    # selective
```

## Key Practices

- Write `.drawio` XML directly — no MCP server dependency needed
- Set `fontFamily=微软雅黑` in every drawio cell style (Windows); swap to platform font as needed
- Use the Clarity color palette consistently across drawio diagrams and PPTX slides
- Two arrow styles only: orthogonal or curved-corner; never let arrows cross or overlap
- EMF gives the best quality for vector diagrams in PPTX (lossless scaling, Linux only)
- PNG with `--scale 2` is the cross-platform fallback (good quality)
- Conditional slides: check `os.path.exists()` before adding optional content
- Keep the make_ppt.py script as the single source of truth for slide layout
- Version control `.drawio` source files, not generated intermediates
- Video embedding requires `ffmpeg` for poster frame extraction + OOXML manipulation
