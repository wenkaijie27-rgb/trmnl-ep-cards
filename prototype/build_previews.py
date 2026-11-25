#!/usr/bin/env python3
"""Render standalone multi-screen TRMNL HTML previews and a combined gallery
for the 3 golden EP knowledge cards using TRMNL Framework v3.4.6.
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

from generate_svgs import render_svg

BASE_DIR = Path("/Users/wenkaijie/Documents/Trmnl/ep-cards/prototype")
DECK_PATH = BASE_DIR / "golden-3.json"
OUT_HTML_DIR = BASE_DIR / "out" / "html"
GALLERY_PATH = BASE_DIR / "preview_gallery.html"

FRAMEWORK_CSS = "file:///Users/wenkaijie/Documents/Trmnl/reference/upstream/trmnl-framework/public/css/3.4.6/plugins.min.css"
FRAMEWORK_JS = "file:///Users/wenkaijie/Documents/Trmnl/reference/upstream/trmnl-framework/public/js/3.4.6/plugins.min.js"
EP_CSS = "file:///Users/wenkaijie/Documents/Trmnl/ep-cards/shared/ep_cards.css"
INTER_FONT_URL = "file:///Users/wenkaijie/Documents/Trmnl/reference/upstream/trmnl-framework/public/fonts/Inter.ttf"

MODES = [
    {
        "key": "og_1bit",
        "label": "7.5\" 黑白 1-bit (800×480)",
        "width": 800,
        "height": 480,
        "screen_classes": "screen screen--ogv2 screen--md screen--density-1x screen--1bit screen--no-bleed ep-screen-card",
    },
    {
        "key": "og_2bit",
        "label": "7.5\" 四灰阶 2-bit (800×480)",
        "width": 800,
        "height": 480,
        "screen_classes": "screen screen--ogv2 screen--md screen--density-1x screen--2bit screen--no-bleed ep-screen-card",
    },
    {
        "key": "og_4bwry",
        "label": "四色墨水屏 BWRY (800×480)",
        "width": 800,
        "height": 480,
        "screen_classes": "screen screen--og screen--md screen--density-1x screen--color-4bwry screen--no-bleed ep-screen-card",
    },
    {
        "key": "trmnl_x",
        "label": "10.3\" TRMNL X 4-bit (1040×780)",
        "width": 1040,
        "height": 780,
        "screen_classes": "screen screen--v2 screen--lg screen--density-2x screen--4bit screen--1x screen--no-bleed ep-screen-card",
    },
]

CATEGORY_LABELS = {
    "conduction_anatomy": "传导解剖",
    "basic_intervals": "基础间期",
    "ep_mechanisms": "电生理机制",
    "svt_triage": "室上速鉴别",
    "wpw_preexcitation": "预激与旁路",
    "pacing_maneuvers": "起搏手法",
    "wide_qrs_vt": "宽波心动过速",
    "ablation_safety": "消融与安全",
}

DIFFICULTY_LABELS = {
    "intro": "入门核心",
    "bridge": "临床桥接",
}


def cjk_space(text: str) -> str:
    """Insert clean spacing between CJK characters and Latin/digit tokens for display."""
    text = re.sub(r"([\u4e00-\u9fff])([A-Za-z0-9≤≥<>±])", r"\1 \2", text)
    text = re.sub(r"([A-Za-z0-9%])([\u4e00-\u9fff])", r"\1 \2", text)
    return html.escape(text)


def render_expanded_section(zh: dict) -> str:
    expanded = zh.get("expanded")
    if not expanded:
        return ""
    ctx = cjk_space(expanded["clinical_context"])
    ref = cjk_space(expanded["reference_note"])
    table_html = ""
    mini_table = expanded.get("mini_table")
    if mini_table:
        ths = "".join(f"<th>{cjk_space(h)}</th>" for h in mini_table["headers"])
        rows_html = "".join(
            "<tr>" + "".join(f"<td>{cjk_space(cell)}</td>" for cell in row) + "</tr>"
            for row in mini_table["rows"]
        )
        table_html = f"""<table class="ep-x-table">
          <thead><tr>{ths}</tr></thead>
          <tbody>{rows_html}</tbody>
        </table>"""

    return f"""<div class="ep-x-section">
      <div class="ep-x-context"><strong>进阶临床视角：</strong>{ctx}</div>
      {table_html}
      <div class="ep-x-ref">
        <span>TRMNL X 扩展卡面（10.3" 4-bit 实色灰阶）</span>
        <span>出处：{ref}</span>
      </div>
    </div>"""


def render_header(zh: dict) -> str:
    metrics_html = ""
    if zh.get("key_metrics"):
        pills = "".join(
            f'<span class="ep-metric-pill"><span class="ep-metric-name">{cjk_space(m["name"])}</span>'
            f'<span class="ep-metric-value">{cjk_space(m["value"])}</span></span>'
            for m in zh["key_metrics"]
        )
        metrics_html = f'<div class="ep-metrics">{pills}</div>'

    return f"""<div class="ep-header">
      <div class="ep-header-top">
        <div class="ep-title-row">
          <span class="ep-kicker">{cjk_space(zh["kicker"])}</span>
          <h1 class="ep-title">{cjk_space(zh["title"])}</h1>
        </div>
        {metrics_html}
      </div>
      <div class="ep-insight">{cjk_space(zh["core_insight"])}</div>
    </div>"""


def render_bullets(zh: dict, row_mode: bool = False) -> str:
    cls = "ep-bullets ep-bullets--row" if row_mode else "ep-bullets"
    items = "".join(
        f'<li class="ep-bullet"><span class="ep-bullet-label">{cjk_space(b["label"])}</span>'
        f'<span class="ep-bullet-text">{cjk_space(b["text"])}</span></li>'
        for b in zh["bullets"]
    )
    return f'<ul class="{cls}">{items}</ul>'


def render_callout(zh: dict) -> str:
    pop = zh["pearl_or_pitfall"]
    badge = "记忆点" if pop["kind"] == "pearl" else "易错点"
    return f'<div class="ep-callout"><span class="ep-callout-badge">{badge}</span><span>{cjk_space(pop["text"])}</span></div>'


def render_card_inner(card: dict, mode_key: str) -> str:
    zh = card["content"]["zh"]
    tpl = card["layout"]["preferred_template"]
    svg_id = card["diagram"]["svg_id"]
    uid = f"{card['id'].replace('-', '_')}_{mode_key}"
    svg_markup = render_svg(svg_id, uid)

    if tpl == "split_left":
        legend_html = (
            '<div class="ep-mini-legend">'
            '<span class="ep-leg-item"><i class="ep-leg-swatch ep-leg-solid"></i>实线：隔瓣附着</span>'
            '<span class="ep-leg-item"><i class="ep-leg-swatch ep-leg-accent"></i>红/虚线：Todaro 腱</span>'
            '<span class="ep-leg-item"><i class="ep-leg-swatch ep-leg-hl"></i>黄/网纹：传导轴邻域</span>'
            '</div>'
        )
        body = f"""<div class="ep-tpl--split_left">
          <div class="ep-diagram-box">{svg_markup}</div>
          <div class="ep-split-text">
            <div class="ep-split-main">
              {render_header(zh)}
              {render_bullets(zh, row_mode=False)}
            </div>
            <div class="ep-split-footer">
              {legend_html}
              {render_callout(zh)}
            </div>
          </div>
          {render_expanded_section(zh)}
        </div>"""
    elif tpl == "top_banner":
        body = f"""<div class="ep-tpl--top_banner">
          {render_header(zh)}
          <div class="ep-diagram-box ep-banner-diagram">{svg_markup}</div>
          <div class="ep-banner-body">
            {render_bullets(zh, row_mode=True)}
            {render_callout(zh)}
          </div>
          {render_expanded_section(zh)}
        </div>"""
    elif tpl == "compare_two":
        body = f"""<div class="ep-tpl--compare_two">
          {render_header(zh)}
          <div class="ep-diagram-box ep-compare-diagram">{svg_markup}</div>
          <div class="ep-compare-body">
            {render_bullets(zh, row_mode=True)}
            {render_callout(zh)}
          </div>
          {render_expanded_section(zh)}
        </div>"""
    else:
        raise ValueError(f"Unsupported prototype template: {tpl}")

    cat_label = CATEGORY_LABELS.get(card["category"], card["category"])
    diff_label = DIFFICULTY_LABELS.get(card["difficulty"], card["difficulty"])
    return f"""<div class="view view--full ep-view">
      <div class="layout ep-layout">
        {body}
      </div>
      <div class="title_bar ep-title-bar">
        <svg class="ep-title-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="2 12 6 12 8.5 5 11.5 19 14.5 9 17 12 22 12"/>
        </svg>
        <span class="title">心脏电生理卡片 · {cat_label}</span>
        <span class="instance">{diff_label} · {card["id"]}</span>
      </div>
    </div>"""


def render_standalone_page(card: dict, mode: dict) -> str:
    inner = render_card_inner(card, mode["key"])
    w, h = mode["width"], mode["height"]
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <title>{html.escape(card["id"])} — {html.escape(mode["key"])}</title>
  <link rel="stylesheet" href="{FRAMEWORK_CSS}">
  <link rel="stylesheet" href="{EP_CSS}">
  <style>
    @font-face {{
      font-family: "Inter Variable";
      font-style: normal;
      font-weight: 100 900;
      src: url("{INTER_FONT_URL}") format("truetype");
    }}
    html, body {{
      margin: 0;
      padding: 0;
      width: {w}px;
      height: {h}px;
      overflow: hidden;
      background: #ffffff;
    }}
  </style>
</head>
<body class="trmnl">
  <div class="{mode["screen_classes"]}">
    {inner}
  </div>
  <script src="{FRAMEWORK_JS}"></script>
</body>
</html>
"""


def render_gallery(cards: list[dict]) -> str:
    sections = []
    for idx, card in enumerate(cards, start=1):
        zh = card["content"]["zh"]
        mode_blocks = []
        for mode in MODES:
            inner = render_card_inner(card, mode["key"])
            w, h = mode["width"], mode["height"]
            scale = 0.72 if w == 1040 else 0.85
            disp_w = int(round(w * scale))
            disp_h = int(round(h * scale))
            mode_blocks.append(f"""<div class="gal-item">
              <div class="gal-meta">
                <strong>{html.escape(mode["label"])}</strong>
                <a href="out/html/{card['id']}__{mode['key']}.html" target="_blank">1:1 原尺寸打开</a>
              </div>
              <div class="gal-viewport" style="width:{disp_w}px;height:{disp_h}px;">
                <div class="trmnl gal-scale" style="width:{w}px;height:{h}px;transform:scale({scale});transform-origin:top left;">
                  <div class="{mode["screen_classes"]}">
                    {inner}
                  </div>
                </div>
              </div>
            </div>""")

        sections.append(f"""<section class="gal-section">
          <h2>样板 {idx}：{cjk_space(zh["title"])} <code>{card["id"]}</code> · <code>{card["layout"]["preferred_template"]}</code></h2>
          <div class="gal-grid">
            {''.join(mode_blocks)}
          </div>
        </section>""")

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <title>EP Cards — 3 张黄金样板多墨水屏预览画廊</title>
  <link rel="stylesheet" href="{FRAMEWORK_CSS}">
  <link rel="stylesheet" href="{EP_CSS}">
  <style>
    @font-face {{
      font-family: "Inter Variable";
      font-style: normal;
      font-weight: 100 900;
      src: url("{INTER_FONT_URL}") format("truetype");
    }}
    body {{
      margin: 0;
      padding: 28px 36px;
      background: #eceef1;
      color: #111827;
      font-family: "Inter Variable", "Noto Sans CJK SC", "PingFang SC", sans-serif;
    }}
    header {{
      margin-bottom: 24px;
    }}
    header h1 {{
      margin: 0 0 6px 0;
      font-size: 24px;
    }}
    header p {{
      margin: 0;
      color: #4b5563;
      font-size: 14px;
    }}
    .gal-section {{
      background: #ffffff;
      border-radius: 12px;
      padding: 20px 24px 26px;
      margin-bottom: 28px;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
    }}
    .gal-section h2 {{
      margin: 0 0 16px 0;
      font-size: 18px;
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .gal-section h2 code {{
      font-size: 12.5px;
      background: #f3f4f6;
      padding: 2px 7px;
      border-radius: 4px;
      font-weight: 600;
    }}
    .gal-grid {{
      display: flex;
      flex-wrap: wrap;
      gap: 24px;
      align-items: flex-start;
    }}
    .gal-item {{
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}
    .gal-meta {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 13px;
    }}
    .gal-meta a {{
      color: #2563eb;
      text-decoration: none;
      font-weight: 600;
    }}
    .gal-viewport {{
      border: 3px solid #1f2937;
      border-radius: 6px;
      overflow: hidden;
      background: #ffffff;
      box-shadow: 0 6px 18px rgba(0, 0, 0, 0.12);
    }}
  </style>
</head>
<body>
  <header>
    <h1>心脏电生理墨水屏知识卡片 — 黄金样板多屏原型预览</h1>
    <p>基于 TRMNL Framework v3.4.6 本地编译资源渲染 · 同源 JSON + 同源语义 SVG 自适应 1-bit / 2-bit / 4-color BWRY (800×480) 与 TRMNL X 4-bit (1040×780)</p>
  </header>
  {''.join(sections)}
  <script src="{FRAMEWORK_JS}"></script>
</body>
</html>
"""


def main() -> None:
    OUT_HTML_DIR.mkdir(parents=True, exist_ok=True)
    deck = json.loads(DECK_PATH.read_text(encoding="utf-8"))
    cards = deck["cards"]

    count = 0
    for card in cards:
        for mode in MODES:
            out_path = OUT_HTML_DIR / f"{card['id']}__{mode['key']}.html"
            out_path.write_text(render_standalone_page(card, mode), encoding="utf-8")
            count += 1

    GALLERY_PATH.write_text(render_gallery(cards), encoding="utf-8")
    print(f"Generated {count} standalone HTML pages in {OUT_HTML_DIR}")
    print(f"Generated gallery at {GALLERY_PATH}")


if __name__ == "__main__":
    main()
