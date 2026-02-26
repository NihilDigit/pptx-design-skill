# Drawio Diagram Design Guide — "Clarity" Style

Full-page diagram design rules for drawio. Ensures diagrams match the PPTX design system and render cleanly when exported to EMF/PNG.

## Color Palette

Coordinated with the PPTX Clarity tokens. Use these exact hex values in drawio styles.

### Module Fill Colors (light fills, dark text)

| Role | Fill | Stroke | Text | Usage |
|------|------|--------|------|-------|
| Primary | #EFF6FF | #3B82F6 | #0F172A | Main modules, key components |
| Secondary | #F0FDF4 | #22C55E | #0F172A | Data stores, outputs, results |
| Tertiary | #FFF7ED | #F97316 | #0F172A | External services, APIs |
| Neutral | #F8FAFC | #CBD5E1 | #334155 | Background groups, containers |
| Highlight | #FEF3C7 | #F59E0B | #0F172A | Key decisions, critical paths |

### Dark Fill Variants (for emphasis headers)

| Role | Fill | Stroke | Text |
|------|------|--------|------|
| Primary Dark | #3B82F6 | #2563EB | #FFFFFF |
| Secondary Dark | #22C55E | #16A34A | #FFFFFF |
| Tertiary Dark | #F97316 | #EA580C | #FFFFFF |
| Ink | #0F172A | #0F172A | #FFFFFF |

### Arrow & Line Colors

| Type | Color | Usage |
|------|-------|-------|
| Primary flow | #3B82F6 | Main data/control flow |
| Secondary flow | #94A3B8 | Supporting connections |
| Highlight flow | #F97316 | Critical path emphasis |

## Typography

### Font

```
fontFamily=微软雅黑;
```

Use `微软雅黑` for all text. It renders well on Windows, macOS (if installed), and Linux (with fallback). For Linux-only projects, `HarmonyOS Sans SC` or `Noto Sans CJK SC` are alternatives.

### Size Hierarchy

| Level | Size | Weight | Usage |
|-------|------|--------|-------|
| Diagram title | 18-20 | Bold | Top-level title (if needed) |
| Module header | 14-16 | Bold | Box/group titles |
| Body text | 12-13 | Regular | Descriptions inside boxes |
| Label | 11 | Regular | Arrow labels, annotations |
| Caption | 10 | Regular | Footnotes, version info |

Minimum readable size after export: 10pt. Never go below this.

## Canvas & Layout

### Canvas Size

Design for full-page PPTX embedding. Target aspect ratio 16:9.

Recommended mxGraphModel dimensions:
```xml
<mxGraphModel dx="1422" dy="800" grid="1" gridSize="10" guides="1">
```

Content area: roughly 1400 × 780 px. Leave 20-30px margin on all sides.

### Layout Principles

1. **Top-to-bottom or left-to-right flow** — pick one direction per diagram, don't mix
2. **Align to grid** — snap all shapes to 10px grid for clean alignment
3. **Consistent spacing** — 40px between sibling modules, 60px between layers
4. **Group related items** — use container rectangles (Neutral fill) to visually cluster
5. **Hierarchy through size** — important modules are larger, not just differently colored
6. **Whitespace is structure** — gaps between groups communicate separation

### Module Sizing

| Type | Width | Height | Notes |
|------|-------|--------|-------|
| Standard module | 160-200 | 60-80 | Single-line title + optional subtitle |
| Wide module | 240-320 | 60-80 | Multi-word titles |
| Group container | 300-500 | varies | Wraps 2-4 child modules |
| Small label box | 100-140 | 40-50 | Annotations, tags |

## Shape Styles

### Standard Module

```
style="rounded=1;whiteSpace=wrap;html=1;fillColor=#EFF6FF;strokeColor=#3B82F6;fontFamily=微软雅黑;fontSize=14;fontStyle=1;fontColor=#0F172A;arcSize=12;"
```

### Group Container

```
style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#CBD5E1;strokeWidth=1;dashed=0;fontFamily=微软雅黑;fontSize=13;fontStyle=1;fontColor=#334155;verticalAlign=top;spacingTop=8;arcSize=8;container=1;collapsible=0;"
```

### Dark Header Module

```
style="rounded=1;whiteSpace=wrap;html=1;fillColor=#3B82F6;strokeColor=#2563EB;fontFamily=微软雅黑;fontSize=14;fontStyle=1;fontColor=#FFFFFF;arcSize=12;"
```

## Arrow Styles

Two permitted arrow forms. Never mix within a single diagram unless semantically justified.

### Style A: Orthogonal (直角折线)

Straight horizontal/vertical segments with 90° turns. Best for structured architecture diagrams.

```
style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#3B82F6;strokeWidth=1.5;endArrow=classic;endFill=1;fontFamily=微软雅黑;fontSize=11;fontColor=#334155;"
```

### Style B: Curved Corners (圆角折线)

Straight segments with rounded corners at turns. Best for flowcharts and process diagrams.

```
style="edgeStyle=orthogonalEdgeStyle;curved=1;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#3B82F6;strokeWidth=1.5;endArrow=classic;endFill=1;fontFamily=微软雅黑;fontSize=11;fontColor=#334155;"
```

The key difference is `curved=1;rounded=1` which adds smooth curves at bend points.

### Arrow Anti-Crossing Rules

These rules prevent visual clutter from overlapping or crossing arrows:

1. **Explicit exit/entry points** — always specify `exitX`, `exitY`, `entryX`, `entryY` in edge style to control exactly where arrows connect:
   ```
   exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;
   ```

2. **Stagger parallel arrows** — when two arrows run in the same direction between nearby modules, offset their exit/entry Y values:
   ```
   Arrow 1: exitY=0.3  entryY=0.3
   Arrow 2: exitY=0.7  entryY=0.7
   ```

3. **Use waypoints for routing** — add explicit `Array` points in mxGeometry to route around obstacles:
   ```xml
   <mxGeometry relative="1" as="geometry">
     <Array as="points">
       <mxPoint x="400" y="200"/>
       <mxPoint x="400" y="350"/>
     </Array>
   </mxGeometry>
   ```

4. **Bidirectional connections** — route on opposite sides of the modules:
   ```
   A→B: exitX=1;exitY=0.3  entryX=0;entryY=0.3  (top path)
   B→A: exitX=0;exitY=0.7  entryX=1;entryY=0.7  (bottom path)
   ```

5. **Minimum clearance** — keep arrows at least 20px away from any shape they don't connect to

6. **No diagonal segments** — all segments must be horizontal or vertical (enforced by orthogonalEdgeStyle)

## Diagram Layout Patterns

### Pattern A: Layered Architecture (分层架构)

Top-to-bottom layers. Each layer is a group container spanning full width.

```
┌─────────────────────────────────────────┐  ← Neutral container "用户层"
│  [Module A]    [Module B]    [Module C]  │  ← Primary fill
└─────────────────────────────────────────┘
         ↓              ↓            ↓        ← Orthogonal arrows
┌─────────────────────────────────────────┐  ← Neutral container "服务层"
│  [Service X]         [Service Y]         │  ← Secondary fill
└─────────────────────────────────────────┘
         ↓              ↓
┌─────────────────────────────────────────┐  ← Neutral container "数据层"
│  [DB]    [Cache]    [Queue]              │  ← Tertiary fill
└─────────────────────────────────────────┘
```

Rules:
- All containers same width, stacked vertically with 60px gap
- Child modules evenly spaced within container
- Arrows exit bottom of source, enter top of target
- Layer labels: bold 14pt, top-left of container

### Pattern B: Pipeline / Flow (流水线)

Left-to-right sequential flow. Single row of processing stages.

```
[Input] → [Stage 1] → [Stage 2] → [Stage 3] → [Output]
```

Rules:
- All modules same height, aligned on horizontal center
- Arrows: `exitX=1;exitY=0.5` → `entryX=0;entryY=0.5`
- 40px gap between modules
- Use Dark Header for first and last nodes (input/output)
- Use Primary fill for processing stages

### Pattern C: Hub-and-Spoke (中心辐射)

Central module with connections to surrounding modules.

```
              [Module B]
                  ↑
[Module A] ← [  Core  ] → [Module C]
                  ↓
              [Module D]
```

Rules:
- Core module: Dark Header, 1.5× size of spokes
- Spokes: Primary fill, evenly distributed around core
- Arrows radiate from core edges: top/bottom/left/right
- Minimum 80px between core and spokes

### Pattern D: Comparison / Side-by-Side (对比)

Two parallel columns with optional cross-connections.

```
┌──── Path A ────┐    ┌──── Path B ────┐
│ [Step A1]      │    │ [Step B1]      │
│     ↓          │    │     ↓          │
│ [Step A2]      │    │ [Step B2]      │
│     ↓          │    │     ↓          │
│ [Step A3]      │    │ [Step B3]      │
└────────────────┘    └────────────────┘
         ↘                    ↙
              [Merge Point]
```

Rules:
- Two group containers side by side, same width
- Internal flows are vertical within each column
- Cross-connections (if any) use Highlight flow color
- Merge point centered below both columns

### Pattern E: Decision Tree (决策树)

Top-down branching with condition labels on arrows.

```
         [Decision]
        /    |     \
    Yes/   Maybe|    \No
      /      |       \
  [Act A] [Act B]  [Act C]
```

Rules:
- Decision nodes: Highlight fill (diamond or rounded rect)
- Branch labels on arrows, not in separate boxes
- Align leaf nodes on same Y coordinate
- Use waypoints to prevent arrow crossing at branch points

## Contrast Checklist

Before exporting, verify:

1. All text on light fills uses `fontColor=#0F172A` or `#334155` (WCAG AA: 7:1+ ratio)
2. All text on dark fills uses `fontColor=#FFFFFF` (WCAG AA: 7:1+ ratio)
3. Arrow labels use `fontColor=#334155` on white background
4. No text smaller than 10pt
5. Stroke colors are darker than fill colors (not the same)

## Export Settings

For PPTX embedding, export with `--crop` to remove whitespace:

```bash
# PNG (cross-platform)
drawio --export --format png --scale 2 --crop --output out.png diagram.drawio

# PDF → EMF (Linux)
drawio --export --format pdf --crop --output out.pdf diagram.drawio
```

The `--crop` flag trims to content bounds, ensuring the diagram fills the slide when placed via `img_fit()`.

## Quick Reference: Style Strings

Copy-paste ready style strings for common elements:

```
# Primary module
rounded=1;whiteSpace=wrap;html=1;fillColor=#EFF6FF;strokeColor=#3B82F6;fontFamily=微软雅黑;fontSize=14;fontStyle=1;fontColor=#0F172A;arcSize=12;

# Secondary module
rounded=1;whiteSpace=wrap;html=1;fillColor=#F0FDF4;strokeColor=#22C55E;fontFamily=微软雅黑;fontSize=14;fontStyle=1;fontColor=#0F172A;arcSize=12;

# Tertiary module
rounded=1;whiteSpace=wrap;html=1;fillColor=#FFF7ED;strokeColor=#F97316;fontFamily=微软雅黑;fontSize=14;fontStyle=1;fontColor=#0F172A;arcSize=12;

# Dark header
rounded=1;whiteSpace=wrap;html=1;fillColor=#3B82F6;strokeColor=#2563EB;fontFamily=微软雅黑;fontSize=14;fontStyle=1;fontColor=#FFFFFF;arcSize=12;

# Group container
rounded=1;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#CBD5E1;strokeWidth=1;fontFamily=微软雅黑;fontSize=13;fontStyle=1;fontColor=#334155;verticalAlign=top;spacingTop=8;arcSize=8;container=1;collapsible=0;

# Arrow (orthogonal)
edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#3B82F6;strokeWidth=1.5;endArrow=classic;endFill=1;fontFamily=微软雅黑;fontSize=11;fontColor=#334155;

# Arrow (curved corners)
edgeStyle=orthogonalEdgeStyle;curved=1;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#3B82F6;strokeWidth=1.5;endArrow=classic;endFill=1;fontFamily=微软雅黑;fontSize=11;fontColor=#334155;

# Secondary arrow
edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#94A3B8;strokeWidth=1;endArrow=classic;endFill=1;dashed=1;fontFamily=微软雅黑;fontSize=11;fontColor=#94A3B8;
```
