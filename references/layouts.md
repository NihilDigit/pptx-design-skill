# Slide Layout Drafts — "Clarity" Design System

Modern, minimal layouts. All use the Clarity design tokens and helpers from `helpers.md`.

16:9 widescreen (13.333 × 7.5 in). Left margin 1.2", content width 10.9".

## 1. Cover (封面)

```python
def slide_cover(prs, title, subtitle, logo_path=None):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    if logo_path and os.path.exists(logo_path):
        img_fit(s, logo_path, top_in=0.4, max_w_in=2.0, max_h_in=2.0, left_in=10.5)
    _tb(s, L_MARGIN, 2.0, 8.0, 1.5, title, size=48, color=INK, bold=True)
    _tb(s, L_MARGIN, 3.8, 8.0, 0.6, subtitle, size=18, color=MUTED)
    # thin accent line below subtitle
    divider(s, L_MARGIN, 4.6, width=3.0)
    return s
```

## 2. Section Divider (章节页)

```python
def slide_section(prs, title, num=None):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid(); bg.fill.fore_color.rgb = INK; bg.line.fill.background()
    if num:
        _tb(s, L_MARGIN, 2.4, C_WIDTH, 0.5, num,
            size=15, color=ACCENT, bold=True)
    _tb(s, L_MARGIN, 3.0 if num else 3.2, C_WIDTH, 1.2, title,
        size=40, color=WHITE, bold=True)
    return s
```

## 3. TOC / Agenda (目录)

```python
def slide_toc(prs, title, items):
    """items: [(num_str, item_title, item_desc), ...]"""
    s = prs.slides.add_slide(prs.slide_layouts[6])
    title_area(s, title)
    for i, (num, it, desc) in enumerate(items):
        y = 1.8 + i * 1.2
        # large number
        _tb(s, L_MARGIN, y, 0.8, 0.5, num, size=28, color=ACCENT, bold=True)
        _tb(s, L_MARGIN + 0.9, y + 0.02, 9, 0.4, it, size=22, color=INK, bold=True)
        _tb(s, L_MARGIN + 0.9, y + 0.45, 9, 0.35, desc, size=14, color=MUTED)
        if i < len(items) - 1:
            divider(s, L_MARGIN + 0.9, y + 0.95, width=9.0)
    return s
```

## 4. Title + Bullets (标题 + 要点)

```python
def slide_title_bullets(prs, title, items, subtitle=None):
    s = new_slide(prs, title, subtitle)
    bullets(s, items, top=1.8 if not subtitle else 2.1)
    return s
```

## 5. Title + Full Diagram (标题 + 整页图)

```python
def slide_title_diagram(prs, title, image_path):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    title_area(s, title)
    img_fit(s, image_path, top_in=1.5)
    return s
```

## 6. Two-Column: Text + Image (左文右图)

```python
def slide_text_image(prs, title, text_items, image_path):
    s = new_slide(prs, title)
    kv_list(s, text_items, L_MARGIN, 1.8, 5.0, 5.0, size=16)
    img_fit(s, image_path, top_in=1.8, max_w_in=5.2, max_h_in=5.0, left_in=6.8)
    return s
```

## 7. Two-Column: Image + Text (左图右文)

```python
def slide_image_text(prs, title, image_path, text_items):
    s = new_slide(prs, title)
    img_fit(s, image_path, top_in=1.8, max_w_in=5.2, max_h_in=5.0, left_in=L_MARGIN)
    kv_list(s, text_items, 7.0, 1.8, 5.0, 5.0, size=16)
    return s
```

## 8. Three Cards (三栏卡片)

```python
def slide_three_cards(prs, title, cards):
    """cards: [(num, card_title, desc), ...]"""
    s = new_slide(prs, title)
    cw = 3.4; gap = (C_WIDTH - 3 * cw) / 2
    for i, (num, ct, cd) in enumerate(cards[:3]):
        x = L_MARGIN + i * (cw + gap)
        num_card(s, x, 1.8, cw, 4.8, num, ct, cd)
    return s
```

## 9. Two Cards (双栏卡片)

```python
def slide_two_cards(prs, title, cards):
    """cards: [(num, card_title, desc), ...]"""
    s = new_slide(prs, title)
    cw = 5.2; gap = C_WIDTH - 2 * cw
    for i, (num, ct, cd) in enumerate(cards[:2]):
        x = L_MARGIN + i * (cw + gap)
        num_card(s, x, 1.8, cw, 4.8, num, ct, cd)
    return s
```

## 10. Stats Row (数据指标)

```python
def slide_stats(prs, title, stats, subtitle=None):
    """stats: [(value, label), ...]"""
    s = new_slide(prs, title, subtitle)
    n = len(stats)
    bw = min(2.8, (C_WIDTH - 0.3 * (n - 1)) / n)
    gap = (C_WIDTH - n * bw) / max(n - 1, 1)
    for i, (val, lbl) in enumerate(stats):
        x = L_MARGIN + i * (bw + gap)
        stat_block(s, x, 2.5, val, lbl, w=bw, h=2.0)
    return s
```

## 11. Timeline (时间线)

```python
def slide_timeline(prs, title, steps):
    """steps: [(step_title, step_desc), ...]"""
    s = new_slide(prs, title)
    timeline(s, steps, left=L_MARGIN, top=2.0, w=C_WIDTH)
    return s
```

## 12. Comparison Table (对比表格)

```python
def slide_table(prs, title, headers, rows):
    s = new_slide(prs, title)
    data = [headers] + rows
    add_table(s, len(data), len(headers), data, top=1.8)
    return s
```

## 13. Quote (引用页)

```python
def slide_quote(prs, quote, attribution=""):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    # large left quote mark
    _tb(s, L_MARGIN, 1.8, 1.0, 1.0, "\u201c", size=72, color=ACCENT, bold=True)
    _tb(s, L_MARGIN + 0.6, 2.5, 9.0, 2.5, quote,
        size=26, color=INK, bold=True)
    if attribution:
        _tb(s, L_MARGIN + 0.6, 5.2, 9.0, 0.5,
            f"— {attribution}", size=16, color=MUTED)
    return s
```

## 14. Video Demo (视频演示)

```python
def slide_video(prs, title, video_path, tags=None):
    """tags: [(text, color), ...] shown below video."""
    s = new_slide(prs, title)
    embed_video(s, video_path, 2.0, 1.6, 9.3, 5.2)
    if tags:
        for i, (txt, clr) in enumerate(tags):
            tag(s, 2.0 + i * 1.8, 7.0, txt, color=clr)
    return s
```

## 15. Video + Side Cards (视频 + 侧栏卡片)

```python
def slide_video_cards(prs, title, video_path, cards, tags=None):
    """cards: [(card_title, card_desc), ...], tags: [str, ...]"""
    s = new_slide(prs, title)
    if tags:
        for i, txt in enumerate(tags):
            tag(s, L_MARGIN + i * 1.8, 1.55, txt)
    # left cards
    for i, (ct, cd) in enumerate(cards):
        y = 2.2 + i * 1.2
        side_card(s, L_MARGIN, y, 5.0, 1.0, ct, cd)
    # right video
    embed_video(s, video_path, 6.8, 1.6, 5.3, 5.2)
    return s
```

## 16. Closing (尾页)

```python
def slide_closing(prs, main_text, subtitle=""):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid(); bg.fill.fore_color.rgb = INK; bg.line.fill.background()
    _tb(s, L_MARGIN, 2.6, C_WIDTH, 1.2, main_text,
        size=40, color=WHITE, bold=True)
    if subtitle:
        divider_ln = s.shapes.add_shape(MSO_SHAPE.RECTANGLE,
            Inches(L_MARGIN), Inches(4.2), Inches(3.0), Inches(0.03))
        divider_ln.fill.solid(); divider_ln.fill.fore_color.rgb = ACCENT
        divider_ln.line.fill.background()
        _tb(s, L_MARGIN, 4.5, C_WIDTH, 0.6, subtitle,
            size=18, color=MUTED)
    return s
```

## 17. Tags + Feature List (标签 + 功能列表)

```python
def slide_tags_features(prs, title, tagline, tags_list, features):
    """tags_list: [str, ...], features: [(feat_title, feat_desc), ...]"""
    s = new_slide(prs, title)
    _tb(s, L_MARGIN, 1.5, 6.0, 0.4, tagline, size=16, color=MUTED)
    for i, txt in enumerate(tags_list):
        tag(s, L_MARGIN + i * 1.8, 2.1, txt)
    for i, (ft, fd) in enumerate(features):
        y = 2.8 + i * 0.7
        _tb(s, L_MARGIN + 0.3, y, 5.5, 0.3, ft, size=17, color=INK, bold=True)
        _tb(s, L_MARGIN + 0.3, y + 0.3, 5.5, 0.3, fd, size=13, color=BODY)
    return s
```

## Design Principles

- Left-aligned titles (not centered) — more modern, easier to scan
- No decorative underline bars — use font weight and size for hierarchy
- Cards use surface fill, no visible borders — cleaner look
- Tags are outlined (not filled pills) — lighter visual weight
- Generous whitespace: 1.2" left margin, 14pt+ line spacing
- Section dividers are left-aligned on dark background
- Stats use large accent numbers, not colored boxes
- Limit to 2-3 colors per slide: INK + ACCENT + MUTED
