#!/usr/bin/env python3
"""Render all 24 Advanced EP cards with TRMNL Framework v3.4.6 + shared/ep_cards.css
into 4 high-res 2x3 contact sheets (1:1 800x480 per card) plus full-resolution multi-screen samples.
"""

from __future__ import annotations

import html
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST_ADV_JSON = ROOT / "dist" / "advanced" / "cards.json"
OUT_HTML = ROOT / "prototype" / "out" / "adv24_html"
OUT_PNG = ROOT / "prototype" / "out" / "adv24_screenshots"

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FRAMEWORK_CSS = "file:///Users/wenkaijie/Documents/Trmnl/reference/upstream/trmnl-framework/public/css/3.4.6/plugins.min.css"
FRAMEWORK_JS = "file:///Users/wenkaijie/Documents/Trmnl/reference/upstream/trmnl-framework/public/js/3.4.6/plugins.min.js"
EP_CSS = "file:///Users/wenkaijie/Documents/Trmnl/ep-cards/shared/ep_cards.css"
INTER_FONT = "file:///Users/wenkaijie/Documents/Trmnl/reference/upstream/trmnl-framework/public/fonts/Inter.ttf"

LEGEND_MAP = {
    "inferoseptal_recess": (
        '<span class="ep-leg-item"><i class="ep-leg-swatch ep-leg-hl"></i>黄/网纹：左室隐窝 (腔内)</span>'
        '<span class="ep-leg-item"><i class="ep-leg-swatch ep-leg-accent"></i>红/虚线：房室传导轴</span>'
    ),
    "marshall_sleeve": (
        '<span class="ep-leg-item"><i class="ep-leg-swatch ep-leg-accent"></i>红/虚线：Marshall 肌束</span>'
        '<span class="ep-leg-item"><i class="ep-leg-swatch ep-leg-hl"></i>黄/网纹：肌性接入点</span>'
    ),
    "left_bundle_variants": (
        '<span class="ep-leg-item"><i class="ep-leg-swatch ep-leg-accent"></i>红/虚线：间隔纤维变异</span>'
        '<span class="ep-leg-item"><i class="ep-leg-swatch ep-leg-hl"></i>黄/网纹：后间隔标测区</span>'
    ),
    "mahaim_insertions": (
        '<span class="ep-leg-item"><i class="ep-leg-swatch ep-leg-accent"></i>红/虚线：常见房束支旁路</span>'
        '<span class="ep-leg-item"><i class="ep-leg-swatch ep-leg-hl"></i>黄/网纹：远端右束支接入</span>'
    ),
    "para_hisian_target": (
        '<span class="ep-leg-item"><i class="ep-leg-swatch ep-leg-accent"></i>红/虚线：正常传导轴</span>'
        '<span class="ep-leg-item"><i class="ep-leg-swatch ep-leg-hl"></i>黄/网纹：靶端 His 观察窗</span>'
    ),
    "coronary_vein_distance": (
        '<span class="ep-leg-item"><i class="ep-leg-swatch ep-leg-accent"></i>红/虚线：邻近冠状动脉</span>'
        '<span class="ep-leg-item"><i class="ep-leg-swatch ep-leg-hl"></i>黄/网纹：最近分离距离</span>'
    ),
}


def render_card_markup(c: dict) -> str:
    tpl = c["template"]
    metrics_html = ""
    if c.get("key_metrics"):
        pills = "".join(
            f'<span class="ep-metric-pill"><span class="ep-metric-name">{html.escape(m["name"])}</span>'
            f'<span class="ep-metric-value">{html.escape(m["value"])}</span></span>'
            for m in c["key_metrics"][:2]
        )
        metrics_html = f'<div class="ep-metrics">{pills}</div>'

    header = f"""<div class="ep-header">
  <div class="ep-header-top">
    <div class="ep-title-row">
      <span class="ep-kicker">{html.escape(c["kicker"])}</span>
      <h1 class="ep-title">{html.escape(c["title"])}</h1>
    </div>
    {metrics_html}
  </div>
  <div class="ep-insight">{html.escape(c["core_insight"])}</div>
</div>"""

    expanded_html = ""
    if c.get("clinical_context"):
        tbl_html = ""
        if c.get("mini_table"):
            ths = "".join(f"<th>{html.escape(h)}</th>" for h in c["mini_table"]["headers"])
            rows = "".join(
                "<tr>" + "".join(f"<td>{html.escape(cell)}</td>" for cell in row) + "</tr>"
                for row in c["mini_table"]["rows"]
            )
            tbl_html = f'<table class="ep-x-table"><thead><tr>{ths}</tr></thead><tbody>{rows}</tbody></table>'
        expanded_html = f"""<div class="ep-x-section hidden lg:flex">
  <div class="ep-x-context"><strong>进阶临床视角：</strong>{html.escape(c["clinical_context"])}</div>
  {tbl_html}
  <div class="ep-x-ref">
    <span>TRMNL X 扩展卡面（{html.escape(c["tier_label"])} · 10.3" 4-bit）</span>
    <span>出处：{html.escape(c["reference_note"])}</span>
  </div>
</div>"""

    callout = f'<div class="ep-callout"><span class="ep-callout-badge">{html.escape(c["callout_badge"])}</span><span>{html.escape(c["callout_text"])}</span></div>'

    if tpl in ("split_left", "split_right"):
        bullets_li = "".join(
            f'<li class="ep-bullet"><span class="ep-bullet-label">{html.escape(b["label"])}</span>'
            f'<span class="ep-bullet-text">{html.escape(b["text"])}</span></li>'
            for b in c["bullets"]
        )
        split_note_html = ""
        if c.get("split_note"):
            split_note_html = f'<div class="ep-split-note"><span class="ep-split-note-badge">临床锚点</span><span>{html.escape(c["split_note"])}</span></div>'
        legend_items = LEGEND_MAP.get(c.get("legend_mode", ""), "")
        legend_html = f'<div class="ep-mini-legend">{legend_items}</div>' if legend_items else ""
        diag = f'<div class="ep-diagram-box ep-split-diagram">{c["svg"]}</div>'
        text_col = f"""<div class="ep-split-text">
  <div class="ep-split-main">
    {header}
    <ul class="ep-bullets ep-bullets--stack">{bullets_li}</ul>
    {split_note_html}
  </div>
  <div class="ep-split-footer">
    {legend_html}
    {callout}
  </div>
</div>"""
        row_inner = f"{diag}{text_col}" if tpl == "split_left" else f"{text_col}{diag}"
        body = f"""<div class="ep-tpl--{tpl} flex flex--col w--full h--full">
  <div class="flex flex--row portrait:flex--col ep-split-main-row w--full">{row_inner}</div>
  {expanded_html}
</div>"""
    else:
        is_cmp = tpl == "compare_two"
        wrap_cls = "ep-tpl--compare_two" if is_cmp else "ep-tpl--top_banner"
        is_three = len(c["bullets"]) == 3
        if is_cmp:
            diag_cls = "ep-diagram-box ep-compare-diagram ep-compare-diagram--compact" if is_three else "ep-diagram-box ep-compare-diagram"
            body_cls = "ep-compare-body"
        else:
            diag_cls = "ep-diagram-box ep-banner-diagram ep-banner-diagram--compact" if is_three else "ep-diagram-box ep-banner-diagram"
            body_cls = "ep-banner-body"
        row_cls = "ep-bullets ep-bullets--row3 grid grid--cols-3 w--full" if is_three else "ep-bullets ep-bullets--row2 grid grid--cols-2 w--full"
        bullets_li = "".join(
            f'<li class="ep-bullet"><span class="ep-bullet-label">{html.escape(b["label"])}</span>'
            f'<span class="ep-bullet-text">{html.escape(b["text"])}</span></li>'
            for b in c["bullets"]
        )
        body = f"""<div class="{wrap_cls} flex flex--col w--full h--full">
  {header}
  <div class="{diag_cls}">{c["svg"]}</div>
  <div class="{body_cls}">
    <ul class="{row_cls}">{bullets_li}</ul>
    {callout}
  </div>
  {expanded_html}
</div>"""

    tier_cls = f'ep-tier-tag ep-tier-tag--{html.escape(c.get("tier", "advanced"))}'
    return f"""<div class="view view--full ep-view">
  <div class="layout layout--col ep-layout">{body}</div>
  <div class="title_bar ep-title-bar">
    <svg class="ep-title-icon" viewBox="0 0 24 24">
      <polyline points="2 12 6 12 8.5 5 11.5 19 14.5 9 17 12 22 12" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    <span class="title">心脏电生理 · {html.escape(c["category_label"])}</span>
    <span class="instance"><span class="{tier_cls}">{html.escape(c["tier_label"])}</span><span>{c["card_index"]}/{c["card_total"]} · {html.escape(c["updated_at"])}</span></span>
  </div>
</div>"""


def wrap_page(body_html: str, width: int, height: int, title: str, extra_css: str = "") -> str:
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <title>{html.escape(title)}</title>
  <link rel="stylesheet" href="{FRAMEWORK_CSS}">
  <link rel="stylesheet" href="{EP_CSS}">
  <style>
    @font-face {{
      font-family: "Inter Variable";
      font-style: normal;
      font-weight: 100 900;
      src: url("{INTER_FONT}") format("truetype");
    }}
    html, body {{
      margin: 0;
      padding: 0;
      width: {width}px;
      height: {height}px;
      overflow: hidden;
      background: #e5e7eb;
    }}
    {extra_css}
  </style>
</head>
<body>
  {body_html}
  <script src="{FRAMEWORK_JS}"></script>
</body>
</html>"""


def capture(html_path: Path, png_path: Path, w: int, h: int) -> None:
    cmd = [
        CHROME_BIN,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--hide-scrollbars",
        "--force-device-scale-factor=1",
        "--virtual-time-budget=2500",
        f"--window-size={w},{h}",
        f"--screenshot={png_path}",
        html_path.as_uri(),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Captured {png_path.name} ({w}x{h})")


def main() -> None:
    OUT_HTML.mkdir(parents=True, exist_ok=True)
    OUT_PNG.mkdir(parents=True, exist_ok=True)
    deck = json.loads(DIST_ADV_JSON.read_text(encoding="utf-8"))
    cards = deck["cards"]

    sheet_css = """
      .sheet { display: grid; grid-template-columns: 800px 800px; gap: 20px; padding: 18px 20px; background: #e5e7eb; }
      .cell { display: flex; flex-direction: column; gap: 4px; }
      .cell-hdr { font-family: "Inter Variable", "PingFang SC", sans-serif; font-size: 13px; font-weight: 700; color: #111827; }
      .cell-frame { width: 800px; height: 480px; border: 2px solid #111827; background: #fff; overflow: hidden; }
    """
    for s_idx in range(4):
        chunk = cards[s_idx * 6 : (s_idx + 1) * 6]
        cells = []
        for c in chunk:
            cls = "screen screen--ogv2 screen--md screen--density-1x screen--1bit screen--no-bleed ep-screen-card"
            inner = render_card_markup(c)
            cells.append(
                f'<div class="cell"><div class="cell-hdr">#{c["card_index"]} {html.escape(c["id"])} · {html.escape(c["template"])} ({len(c["bullets"])} bullets)</div>'
                f'<div class="cell-frame trmnl"><div class="{cls}">{inner}</div></div></div>'
            )
        html_path = OUT_HTML / f"adv_contact_sheet_{s_idx + 1}.html"
        png_path = OUT_PNG / f"adv_contact_sheet_{s_idx + 1}.png"
        html_path.write_text(
            wrap_page(f'<div class="sheet">{"".join(cells)}</div>', 1660, 1570, f"Advanced Contact Sheet {s_idx + 1}", sheet_css),
            encoding="utf-8",
        )
        capture(html_path, png_path, 1660, 1570)

    by_id = {c["id"]: c for c in cards}
    samples = [
        ("anatomy-inferoseptal-recess", "og_1bit", 800, 480, "screen screen--ogv2 screen--md screen--density-1x screen--1bit screen--no-bleed ep-screen-card"),
        ("anatomy-inferoseptal-recess", "og_4bwry", 800, 480, "screen screen--og screen--md screen--density-1x screen--color-4bwry screen--no-bleed ep-screen-card"),
        ("anatomy-inferoseptal-recess", "trmnl_x", 1040, 780, "screen screen--v2 screen--lg screen--density-2x screen--4bit screen--1x screen--no-bleed ep-screen-card"),
        ("intervals-rp-vs-va-cutoffs", "og_1bit", 800, 480, "screen screen--ogv2 screen--md screen--density-1x screen--1bit screen--no-bleed ep-screen-card"),
        ("intervals-rp-vs-va-cutoffs", "og_4bwry", 800, 480, "screen screen--og screen--md screen--density-1x screen--color-4bwry screen--no-bleed ep-screen-card"),
        ("mechanisms-cardiac-memory", "og_4bwry", 800, 480, "screen screen--og screen--md screen--density-1x screen--color-4bwry screen--no-bleed ep-screen-card"),
        ("pace-corrected-ppi-tcl", "og_1bit", 800, 480, "screen screen--ogv2 screen--md screen--density-1x screen--1bit screen--no-bleed ep-screen-card"),
        ("pace-corrected-ppi-tcl", "og_4bwry", 800, 480, "screen screen--og screen--md screen--density-1x screen--color-4bwry screen--no-bleed ep-screen-card"),
        ("pace-corrected-ppi-tcl", "trmnl_x", 1040, 780, "screen screen--v2 screen--lg screen--density-2x screen--4bit screen--1x screen--no-bleed ep-screen-card"),
        ("ablation-coronary-vein-distance", "og_1bit", 800, 480, "screen screen--ogv2 screen--md screen--density-1x screen--1bit screen--no-bleed ep-screen-card"),
        ("ablation-coronary-vein-distance", "og_4bwry", 800, 480, "screen screen--og screen--md screen--density-1x screen--color-4bwry screen--no-bleed ep-screen-card"),
        ("wpw-asymptomatic-ep-risk", "og_4bwry", 800, 480, "screen screen--og screen--md screen--density-1x screen--color-4bwry screen--no-bleed ep-screen-card"),
        ("wpw-asymptomatic-ep-risk", "trmnl_x", 1040, 780, "screen screen--v2 screen--lg screen--density-2x screen--4bit screen--1x screen--no-bleed ep-screen-card"),
    ]
    for cid, tag, w, h, cls in samples:
        c = by_id[cid]
        inner = render_card_markup(c)
        html_path = OUT_HTML / f"{cid}__{tag}.html"
        png_path = OUT_PNG / f"{cid}__{tag}.png"
        html_path.write_text(
            wrap_page(f'<div class="trmnl" style="width:{w}px;height:{h}px;"><div class="{cls}">{inner}</div></div>', w, h, f"{cid} {tag}"),
            encoding="utf-8",
        )
        capture(html_path, png_path, w, h)


if __name__ == "__main__":
    main()
