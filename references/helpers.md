# python-pptx Helper Library — "Clarity" Design System

Modern, minimal design system. High contrast, generous whitespace, clean typography.

## Design Tokens

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image
import os, subprocess
from pptx.oxml import parse_xml
from pptx.oxml.ns import qn
from pptx.opc.package import Part, PackURI

# === Clarity Design Tokens ===
INK       = RGBColor(0x0F, 0x17, 0x2A)  # near-black, titles
BODY      = RGBColor(0x33, 0x41, 0x55)  # dark slate, body text
MUTED     = RGBColor(0x94, 0xA3, 0xB8)  # medium gray, captions
ACCENT    = RGBColor(0x3B, 0x82, 0xF6)  # vibrant blue, highlights
ACC_SOFT  = RGBColor(0xEF, 0xF6, 0xFF)  # blue tint, card backgrounds
SURFACE   = RGBColor(0xF8, 0xFA, 0xFC)  # off-white, panels
BORDER    = RGBColor(0xE2, 0xE8, 0xF0)  # subtle border
WHITE     = RGBColor(0xFF, 0xFF, 0xFF)
SUCCESS   = RGBColor(0x10, 0xB9, 0x81)  # green, positive
WARN      = RGBColor(0xF5, 0x9E, 0x0B)  # amber, caution
FONT      = "微软雅黑"  # cross-platform CJK; swap to system font as needed

HERE  = os.path.dirname(os.path.abspath(__file__))
IMG   = lambda name: os.path.join(HERE, name)
DIAG  = lambda name: os.path.join(HERE, "..", "diagrams", name)
ASSET = lambda name: os.path.join(HERE, "..", "assets", name)

prs = Presentation()
prs.slide_width  = Inches(13.333)  # 16:9
prs.slide_height = Inches(7.5)
BL = prs.slide_layouts[6]  # blank

# Layout constants
L_MARGIN = 1.2   # left margin (inches)
R_EDGE   = 12.1  # right content edge
C_WIDTH  = R_EDGE - L_MARGIN  # usable content width
```

## Core Helpers

### _tb — Textbox (unchanged API, new defaults)
```python
def _tb(slide, left, top, w, h, text, size=18, color=BODY, bold=False, align=PP_ALIGN.LEFT):
    tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = text
    p.font.size = Pt(size); p.font.color.rgb = color
    p.font.bold = bold; p.font.name = FONT; p.alignment = align
    return tf
```

### title_area — Clean Title (no underline bar)
```python
def title_area(slide, title, subtitle=None):
    """Large bold title + optional muted subtitle. No decorative lines."""
    _tb(slide, L_MARGIN, 0.5, C_WIDTH, 0.7, title, size=32, color=INK, bold=True)
    if subtitle:
        _tb(slide, L_MARGIN, 1.15, C_WIDTH, 0.4, subtitle, size=15, color=MUTED)
```

### img_fit — Auto-Scaled Image
```python
def img_fit(slide, path, top_in, max_w_in=C_WIDTH, max_h_in=None, left_in=None):
    if max_h_in is None:
        max_h_in = 7.5 - top_in - 0.3
    if path.lower().endswith(('.png', '.jpg', '.jpeg')):
        im = Image.open(path)
        w_px, h_px = im.size
        ratio = min(max_w_in / (w_px / 96), max_h_in / (h_px / 96))
        w_in = w_px / 96 * ratio; h_in = h_px / 96 * ratio
    else:
        pic = slide.shapes.add_picture(path, 0, Inches(top_in), Inches(max_w_in))
        w_in = pic.width / 914400; h_in = pic.height / 914400
        if h_in > max_h_in:
            scale = max_h_in / h_in
            pic.width = int(pic.width * scale); pic.height = int(pic.height * scale)
            w_in *= scale; h_in *= scale
        pic.left = int(Inches(left_in if left_in is not None else (13.333 - w_in) / 2))
        return
    left = left_in if left_in is not None else (13.333 - w_in) / 2
    slide.shapes.add_picture(path, Inches(left), Inches(top_in), Inches(w_in), Inches(h_in))
```

## Card & List Helpers

### card — Minimal Card (no visible border, surface fill)
```python
def card(slide, left, top, w, h):
    """Subtle card: surface fill, no border. Returns shape for further customization."""
    sh = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(left), Inches(top), Inches(w), Inches(h))
    sh.fill.solid(); sh.fill.fore_color.rgb = SURFACE
    sh.line.fill.background()
    # Adjust corner radius via XML for tighter rounding
    sp = sh._element
    prstGeom = sp.find(qn('a:prstGeom'))
    if prstGeom is not None:
        avLst = prstGeom.find(qn('a:avLst'))
        if avLst is None:
            avLst = parse_xml('<a:avLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>')
            prstGeom.append(avLst)
    return sh
```

### accent_card — Card with Top Accent Stripe
```python
def accent_card(slide, left, top, w, h, title, desc, stripe_color=ACCENT):
    """Card with thin colored stripe at top, title + description."""
    card(slide, left, top, w, h)
    # top stripe (3px)
    stripe = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
        Inches(left + 0.15), Inches(top), Inches(w - 0.3), Inches(0.04))
    stripe.fill.solid(); stripe.fill.fore_color.rgb = stripe_color
    stripe.line.fill.background()
    _tb(slide, left + 0.3, top + 0.25, w - 0.6, 0.35,
        title, size=18, color=INK, bold=True)
    _tb(slide, left + 0.3, top + 0.65, w - 0.6, h - 0.85,
        desc, size=14, color=BODY)
```

### num_card — Numbered Feature Card (modern)
```python
def num_card(slide, left, top, w, h, num, title, desc):
    """Card with large accent number, title, description."""
    card(slide, left, top, w, h)
    # large number
    _tb(slide, left + 0.3, top + 0.2, 0.6, 0.5,
        str(num).zfill(2), size=28, color=ACCENT, bold=True)
    # title + desc
    _tb(slide, left + 0.3, top + 0.7, w - 0.6, 0.3,
        title, size=17, color=INK, bold=True)
    _tb(slide, left + 0.3, top + 1.05, w - 0.6, h - 1.25,
        desc, size=13, color=BODY)
```

### side_card — Card with Left Accent Bar (modern)
```python
def side_card(slide, left, top, w, h, title, desc):
    """Card with thin left accent bar."""
    card(slide, left, top, w, h)
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
        Inches(left), Inches(top + 0.12), Inches(0.05), Inches(h - 0.24))
    bar.fill.solid(); bar.fill.fore_color.rgb = ACCENT
    bar.line.fill.background()
    _tb(slide, left + 0.3, top + 0.15, w - 0.45, 0.3,
        title, size=17, color=INK, bold=True)
    _tb(slide, left + 0.3, top + 0.5, w - 0.45, h - 0.65,
        desc, size=13, color=BODY)
```

### bullets — Clean Bullet List
```python
def bullets(slide, items, top=1.8, left=L_MARGIN, width=C_WIDTH, size=18):
    tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(5.5))
    tf = tb.text_frame; tf.word_wrap = True
    for i, txt in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = txt; p.font.size = Pt(size); p.font.color.rgb = BODY
        p.font.name = FONT; p.space_after = Pt(14)
        p.space_before = Pt(4)
    return tf
```

### kv_list — Key-Value List (bold key + normal value)
```python
def kv_list(slide, items, left, top, w, h, size=15):
    """items: [(key, value), ...]. Key in INK bold, value in BODY."""
    tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True
    for i, (k, v) in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        r1 = p.add_run(); r1.text = k + "  "
        r1.font.size = Pt(size); r1.font.color.rgb = INK
        r1.font.bold = True; r1.font.name = FONT
        r2 = p.add_run(); r2.text = v
        r2.font.size = Pt(size); r2.font.color.rgb = BODY; r2.font.name = FONT
        p.space_after = Pt(12)
    return tf
```

### tag — Outlined Tag (not filled pill)
```python
def tag(slide, left, top, text, w=1.4, h=0.32, size=11, color=ACCENT):
    """Outlined tag: accent border, transparent fill, accent text."""
    sh = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(left), Inches(top), Inches(w), Inches(h))
    sh.fill.background()
    sh.line.color.rgb = color; sh.line.width = Pt(1.2)
    tf = sh.text_frame; tf.word_wrap = False
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    p.text = text; p.font.size = Pt(size); p.font.color.rgb = color; p.font.name = FONT
    tf._txBody.find(qn('a:bodyPr')).set('anchor', 'ctr')
    return sh
```

### stat_block — Stat with Big Number
```python
def stat_block(slide, left, top, value, label, w=2.4, h=1.4):
    """Big accent number + muted label, on surface card."""
    card(slide, left, top, w, h)
    _tb(slide, left + 0.2, top + 0.15, w - 0.4, 0.6,
        value, size=36, color=ACCENT, bold=True, align=PP_ALIGN.CENTER)
    _tb(slide, left + 0.2, top + 0.8, w - 0.4, 0.4,
        label, size=12, color=MUTED, align=PP_ALIGN.CENTER)
```

## Layout Helpers

### divider — Thin Horizontal Line
```python
def divider(slide, left=L_MARGIN, top=1.0, width=C_WIDTH):
    ln = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
        Inches(left), Inches(top), Inches(width), Inches(0.015))
    ln.fill.solid(); ln.fill.fore_color.rgb = BORDER
    ln.line.fill.background()
```

### panel — Tinted Background Area
```python
def panel(slide, left, top, w, h, color=ACC_SOFT):
    bg = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(left), Inches(top), Inches(w), Inches(h))
    bg.fill.solid(); bg.fill.fore_color.rgb = color
    bg.line.fill.background()
    return bg
```

### timeline — Horizontal Step Indicator
```python
def timeline(slide, steps, left=L_MARGIN, top=2.0, w=C_WIDTH):
    """Horizontal numbered steps connected by lines.
    steps: [(title, desc), ...]. All on one row, cards below."""
    n = len(steps)
    node_r = 0.22  # radius of numbered circle
    card_w = (w - 0.5) / n
    card_h = 2.8
    card_top = top + node_r * 2 + 0.6

    for i, (title, desc) in enumerate(steps):
        cx = left + card_w * i + card_w / 2
        # connecting line (skip first)
        if i > 0:
            prev_cx = left + card_w * (i - 1) + card_w / 2
            ln = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                Inches(prev_cx + node_r), Inches(top + node_r - 0.015),
                Inches(cx - prev_cx - node_r * 2), Inches(0.03))
            ln.fill.solid(); ln.fill.fore_color.rgb = BORDER
            ln.line.fill.background()
        # numbered circle
        dot = slide.shapes.add_shape(MSO_SHAPE.OVAL,
            Inches(cx - node_r), Inches(top),
            Inches(node_r * 2), Inches(node_r * 2))
        dot.fill.solid(); dot.fill.fore_color.rgb = ACCENT
        dot.line.fill.background()
        dtf = dot.text_frame; dtf.word_wrap = False
        dtf.margin_left = dtf.margin_right = dtf.margin_top = dtf.margin_bottom = 0
        dtf._txBody.find(qn('a:bodyPr')).set('anchor', 'ctr')
        dp = dtf.paragraphs[0]; dp.alignment = PP_ALIGN.CENTER
        dr = dp.add_run(); dr.text = str(i + 1)
        dr.font.size = Pt(14); dr.font.color.rgb = WHITE
        dr.font.bold = True; dr.font.name = FONT
        # card below
        cl = cx - card_w / 2 + 0.1
        accent_card(slide, cl, card_top, card_w - 0.2, card_h, title, desc)
```

### add_table — Clean Table (modern)
```python
def add_table(slide, rows, cols, data, top=1.8, left=L_MARGIN, width=C_WIDTH, row_h=0.55):
    """data = list of lists (header + body rows). Minimal styling."""
    h = row_h * rows
    tbl_shape = slide.shapes.add_table(rows, cols, Inches(left), Inches(top),
        Inches(width), Inches(h))
    tbl = tbl_shape.table
    for r in range(rows):
        for c in range(cols):
            cell = tbl.cell(r, c); cell.text = data[r][c]
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(16); p.font.name = FONT
                p.font.color.rgb = BODY; p.alignment = PP_ALIGN.CENTER
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            if r == 0:
                cell.fill.solid(); cell.fill.fore_color.rgb = INK
                for p in cell.text_frame.paragraphs:
                    p.font.color.rgb = WHITE; p.font.bold = True
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = WHITE if r % 2 == 1 else SURFACE
    return tbl
```

## Slide Constructors

### section_slide — Section Divider (gradient feel)
```python
def section_slide(prs, title, num=None):
    """Dark background section divider. Optional section number."""
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid(); bg.fill.fore_color.rgb = INK; bg.line.fill.background()
    if num:
        _tb(s, L_MARGIN, 2.2, C_WIDTH, 0.6, num,
            size=16, color=ACCENT, bold=True, align=PP_ALIGN.LEFT)
    y = 2.8 if num else 3.0
    _tb(s, L_MARGIN, y, C_WIDTH, 1.2, title,
        size=40, color=WHITE, bold=True, align=PP_ALIGN.LEFT)
    return s
```

### new_slide — Blank with Optional Title
```python
def new_slide(prs, title=None, subtitle=None):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    if title:
        title_area(s, title, subtitle)
    return s
```

## Video Embedding

### embed_video — Embed MP4 with Auto Poster Frame
Requires `ffmpeg` for poster extraction and low-level OOXML manipulation.

```python
_video_idx = 0

def embed_video(slide, video_path, left, top, w, h):
    global _video_idx; _video_idx += 1
    poster = os.path.join(HERE, f"_poster{_video_idx}.png")
    subprocess.run(["ffmpeg", "-y", "-i", video_path, "-vframes", "1", "-q:v", "2", poster],
                   capture_output=True)
    pic = slide.shapes.add_picture(poster, Inches(left), Inches(top), Inches(w), Inches(h))
    os.unlink(poster)
    with open(video_path, "rb") as f: blob = f.read()
    partname = PackURI(f"/ppt/media/video{_video_idx}.mp4")
    video_part = Part(partname, "video/mp4", prs.part.package, blob)
    vid_rId = slide.part.relate_to(video_part,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/video")
    media_rId = slide.part.relate_to(video_part,
        "http://schemas.microsoft.com/office/2007/relationships/media")
    nvPr = pic._element.find(qn("p:nvPicPr")).find(qn("p:nvPr"))
    nvPr.append(parse_xml(
        f'<a:videoFile xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'
        f' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
        f' r:link="{vid_rId}"/>'))
    nvPr.append(parse_xml(
        f'<p:extLst xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
        f'<p:ext uri="{{DAA4B4D4-6D71-4841-9C94-3DE7FCFB9230}}">'
        f'<p14:media xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main"'
        f' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
        f' r:embed="{media_rId}"/>'
        f'</p:ext></p:extLst>'))
    return pic
```
