#!/usr/bin/env python3
"""Build distributable artifacts for both Terminus BYOS and TRMNL Cloud Recipe:

- dist/cards.json (enriched active deck for HAOS / GitHub Pages)
- dist/current.json (deterministic UTC-rotated single card for TRMNL polling)
- dist/cards/<id>.json (per-card pinned endpoints)
- terminus/configuration.yml & terminus/template.html.liquid
- dist/ep-cards-terminus-extension.zip
- trmnl-recipe/src/* (settings.yml, shared.liquid, full.liquid, half_horizontal.liquid, half_vertical.liquid, quadrant.liquid)
"""

from __future__ import annotations

import datetime as dt
import html
import json
import re
import zipfile
from pathlib import Path

from generate_svgs import render_svg

ROOT = Path(__file__).resolve().parent.parent
DECK_PATH = ROOT / "decks" / "golden-3.json"
CSS_PATH = ROOT / "shared" / "ep_cards.css"
DIST_DIR = ROOT / "dist"
DIST_CARDS_DIR = DIST_DIR / "cards"
TERMINUS_DIR = ROOT / "terminus"
RECIPE_SRC_DIR = ROOT / "trmnl-recipe" / "src"

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
    return text


def enrich_card(raw_card: dict, index: int, total: int, generated_at: str) -> dict:
    zh = raw_card["content"]["zh"]
    svg_id = raw_card["diagram"]["svg_id"]
    svg_markup = render_svg(svg_id, raw_card["id"].replace("-", "_")) if svg_id else ""

    pop = zh["pearl_or_pitfall"]
    callout_badge = "记忆点" if pop["kind"] == "pearl" else "易错点"

    expanded = zh.get("expanded") or {}
    mini_table = expanded.get("mini_table")
    table_payload = None
    if mini_table:
        table_payload = {
            "headers": [cjk_space(h) for h in mini_table["headers"]],
            "rows": [[cjk_space(cell) for cell in row] for row in mini_table["rows"]],
        }

    return {
        "id": raw_card["id"],
        "card_index": index,
        "card_total": total,
        "category": raw_card["category"],
        "category_label": CATEGORY_LABELS.get(raw_card["category"], raw_card["category"]),
        "difficulty": raw_card["difficulty"],
        "difficulty_label": DIFFICULTY_LABELS.get(raw_card["difficulty"], raw_card["difficulty"]),
        "template": raw_card["layout"]["preferred_template"],
        "diagram_aspect_ratio": raw_card["layout"]["diagram_aspect_ratio"],
        "kicker": cjk_space(zh["kicker"]),
        "title": cjk_space(zh["title"]),
        "core_insight": cjk_space(zh["core_insight"]),
        "bullets": [
            {"label": cjk_space(b["label"]), "text": cjk_space(b["text"])}
            for b in zh["bullets"]
        ],
        "key_metrics": [
            {"name": cjk_space(m["name"]), "value": cjk_space(m["value"])}
            for m in zh.get("key_metrics", [])
        ],
        "callout_kind": pop["kind"],
        "callout_badge": callout_badge,
        "callout_text": cjk_space(pop["text"]),
        "quadrant_summary": cjk_space(zh["quadrant_summary"]),
        "clinical_context": cjk_space(expanded["clinical_context"]) if expanded.get("clinical_context") else "",
        "reference_note": cjk_space(expanded["reference_note"]) if expanded.get("reference_note") else "",
        "mini_table": table_payload,
        "show_anatomy_legend": raw_card["id"] == "anatomy-koch-triangle",
        "svg": svg_markup,
        "updated_at": generated_at,
    }


def _full_body_liquid(var_prefix: str) -> str:
    """Return Liquid body markup compatible with both Terminus (source_1) and TRMNL Cloud (root)."""
    p = f"{var_prefix}." if var_prefix else ""
    return f"""<div class="view view--full ep-view">
  <div class="layout ep-layout">
    {{% if {p}template == 'split_left' %}}
      <div class="ep-tpl--split_left">
        <div class="ep-diagram-box">{{{{ {p}svg }}}}</div>
        <div class="ep-split-text">
          <div class="ep-split-main">
            <div class="ep-header">
              <div class="ep-header-top">
                <div class="ep-title-row">
                  <span class="ep-kicker">{{{{ {p}kicker }}}}</span>
                  <h1 class="ep-title">{{{{ {p}title }}}}</h1>
                </div>
                {{% if {p}key_metrics.size > 0 %}}
                  <div class="ep-metrics">
                    {{% for m in {p}key_metrics %}}
                      <span class="ep-metric-pill"><span class="ep-metric-name">{{{{ m.name }}}}</span><span class="ep-metric-value">{{{{ m.value }}}}</span></span>
                    {{% endfor %}}
                  </div>
                {{% endif %}}
              </div>
              <div class="ep-insight">{{{{ {p}core_insight }}}}</div>
            </div>
            <ul class="ep-bullets">
              {{% for b in {p}bullets %}}
                <li class="ep-bullet"><span class="ep-bullet-label">{{{{ b.label }}}}</span><span class="ep-bullet-text">{{{{ b.text }}}}</span></li>
              {{% endfor %}}
            </ul>
          </div>
          <div class="ep-split-footer">
            {{% if {p}show_anatomy_legend %}}
              <div class="ep-mini-legend">
                <span class="ep-leg-item"><i class="ep-leg-swatch ep-leg-solid"></i>实线：隔瓣附着</span>
                <span class="ep-leg-item"><i class="ep-leg-swatch ep-leg-accent"></i>红/虚线：Todaro 腱</span>
                <span class="ep-leg-item"><i class="ep-leg-swatch ep-leg-hl"></i>黄/网纹：传导轴邻域</span>
              </div>
            {{% endif %}}
            <div class="ep-callout"><span class="ep-callout-badge">{{{{ {p}callout_badge }}}}</span><span>{{{{ {p}callout_text }}}}</span></div>
          </div>
        </div>
        {{% if {p}clinical_context != blank %}}
          <div class="ep-x-section">
            <div class="ep-x-context"><strong>进阶临床视角：</strong>{{{{ {p}clinical_context }}}}</div>
            {{% if {p}mini_table %}}
              <table class="ep-x-table">
                <thead><tr>{{% for h in {p}mini_table.headers %}}<th>{{{{ h }}}}</th>{{% endfor %}}</tr></thead>
                <tbody>
                  {{% for row in {p}mini_table.rows %}}
                    <tr>{{% for cell in row %}}<td>{{{{ cell }}}}</td>{{% endfor %}}</tr>
                  {{% endfor %}}
                </tbody>
              </table>
            {{% endif %}}
            <div class="ep-x-ref">
              <span>TRMNL X 扩展卡面（10.3" 4-bit 实色灰阶）</span>
              <span>出处：{{{{ {p}reference_note }}}}</span>
            </div>
          </div>
        {{% endif %}}
      </div>
    {{% else %}}
      {{% if {p}template == 'compare_two' %}}
        {{% assign wrap_cls = 'ep-tpl--compare_two' %}}
        {{% assign diag_cls = 'ep-diagram-box ep-compare-diagram' %}}
        {{% assign body_cls = 'ep-compare-body' %}}
      {{% else %}}
        {{% assign wrap_cls = 'ep-tpl--top_banner' %}}
        {{% assign diag_cls = 'ep-diagram-box ep-banner-diagram' %}}
        {{% assign body_cls = 'ep-banner-body' %}}
      {{% endif %}}
      <div class="{{{{ wrap_cls }}}}">
        <div class="ep-header">
          <div class="ep-header-top">
            <div class="ep-title-row">
              <span class="ep-kicker">{{{{ {p}kicker }}}}</span>
              <h1 class="ep-title">{{{{ {p}title }}}}</h1>
            </div>
            {{% if {p}key_metrics.size > 0 %}}
              <div class="ep-metrics">
                {{% for m in {p}key_metrics %}}
                  <span class="ep-metric-pill"><span class="ep-metric-name">{{{{ m.name }}}}</span><span class="ep-metric-value">{{{{ m.value }}}}</span></span>
                {{% endfor %}}
              </div>
            {{% endif %}}
          </div>
          <div class="ep-insight">{{{{ {p}core_insight }}}}</div>
        </div>
        <div class="{{{{ diag_cls }}}}">{{{{ {p}svg }}}}</div>
        <div class="{{{{ body_cls }}}}">
          <ul class="ep-bullets ep-bullets--row">
            {{% for b in {p}bullets %}}
              <li class="ep-bullet"><span class="ep-bullet-label">{{{{ b.label }}}}</span><span class="ep-bullet-text">{{{{ b.text }}}}</span></li>
            {{% endfor %}}
          </ul>
          <div class="ep-callout"><span class="ep-callout-badge">{{{{ {p}callout_badge }}}}</span><span>{{{{ {p}callout_text }}}}</span></div>
        </div>
        {{% if {p}clinical_context != blank %}}
          <div class="ep-x-section">
            <div class="ep-x-context"><strong>进阶临床视角：</strong>{{{{ {p}clinical_context }}}}</div>
            {{% if {p}mini_table %}}
              <table class="ep-x-table">
                <thead><tr>{{% for h in {p}mini_table.headers %}}<th>{{{{ h }}}}</th>{{% endfor %}}</tr></thead>
                <tbody>
                  {{% for row in {p}mini_table.rows %}}
                    <tr>{{% for cell in row %}}<td>{{{{ cell }}}}</td>{{% endfor %}}</tr>
                  {{% endfor %}}
                </tbody>
              </table>
            {{% endif %}}
            <div class="ep-x-ref">
              <span>TRMNL X 扩展卡面（10.3" 4-bit 实色灰阶）</span>
              <span>出处：{{{{ {p}reference_note }}}}</span>
            </div>
          </div>
        {{% endif %}}
      </div>
    {{% endif %}}
  </div>

  <div class="title_bar ep-title-bar">
    <svg class="ep-title-icon" viewBox="0 0 24 24">
      <polyline points="2 12 6 12 8.5 5 11.5 19 14.5 9 17 12 22 12" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    <span class="title">心脏电生理卡片 · {{{{ {p}category_label }}}}</span>
    <span class="instance">{{{{ {p}difficulty_label }}}} · {{{{ {p}card_index }}}}/{{{{ {p}card_total }}}} · {{{{ {p}updated_at }}}}</span>
  </div>
</div>"""


def build_terminus_files(css_text: str) -> None:
    TERMINUS_DIR.mkdir(parents=True, exist_ok=True)
    config_yml = """version: "0.84.0"
name: "ep_cards"
label: "心脏电生理知识卡"
description: "面向入门医学生的心脏电生理知识卡片（TRMNL Framework + 语义内联 SVG，兼容 1-bit / 2-bit / TRMNL X / 四色墨水屏）"
mode: "text"
kind: "poll"
tags: []
static_body: {}
fields: []
data: {}
interval: 15
unit: "minute"
days: []
last_day_of_month: false
start_at: "2026-11-25T00:00:00"
exchanges:
  - headers: {}
    verb: "get"
    template: "http://192.168.10.135:8080/EPCards/card.json"
    body: {}
"""
    (TERMINUS_DIR / "configuration.yml").write_text(config_yml, encoding="utf-8")

    liquid = f"""<style>
{css_text.strip()}
</style>
{_full_body_liquid("source_1")}
"""
    (TERMINUS_DIR / "template.html.liquid").write_text(liquid, encoding="utf-8")

    zip_path = DIST_DIR / "ep-cards-terminus-extension.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.write(TERMINUS_DIR / "configuration.yml", arcname="configuration.yml")
        zf.write(TERMINUS_DIR / "template.html.liquid", arcname="template.html.liquid")
    print(f"Built Terminus extension ZIP: {zip_path}")


def build_trmnl_recipe(css_text: str) -> None:
    RECIPE_SRC_DIR.mkdir(parents=True, exist_ok=True)
    settings_yml = """---
strategy: polling
no_screen_padding: 'yes'
dark_mode: 'no'
static_data: ''
polling_verb: get
framework_version: latest
polling_url: https://wenkaijie27-rgb.github.io/trmnl-ep-cards/current.json
polling_headers: ''
name: Cardiac EP Knowledge Cards
description: Illustrated cardiac electrophysiology learning cards for medical students (multi-screen 1-bit/2-bit/4-bit/BWRY e-ink).
refresh_interval: 60
"""
    (RECIPE_SRC_DIR / "settings.yml").write_text(settings_yml, encoding="utf-8")
    (RECIPE_SRC_DIR / "shared.liquid").write_text(f"<style>\n{css_text.strip()}\n</style>\n", encoding="utf-8")
    (RECIPE_SRC_DIR / "full.liquid").write_text(_full_body_liquid("") + "\n", encoding="utf-8")

    half_h = """<div class="ep-subview">
  <div class="ep-subview-body">
    <div class="ep-header">
      <div class="ep-header-top">
        <div class="ep-title-row">
          <span class="ep-kicker">{{ kicker }}</span>
          <h1 class="ep-title" style="font-size:20px;">{{ title }}</h1>
        </div>
        {% if key_metrics.size > 0 %}
          <span class="ep-metric-pill"><span class="ep-metric-name">{{ key_metrics[0].name }}</span><span class="ep-metric-value">{{ key_metrics[0].value }}</span></span>
        {% endif %}
      </div>
      <div class="ep-insight" style="font-size:14.5px;">{{ core_insight }}</div>
    </div>
    <div class="ep-callout"><span class="ep-callout-badge">{{ callout_badge }}</span><span>{{ callout_text }}</span></div>
  </div>
  <div class="title_bar ep-title-bar">
    <span class="title">心脏电生理卡片 · {{ category_label }}</span>
    <span class="instance">{{ card_index }}/{{ card_total }}</span>
  </div>
</div>
"""
    (RECIPE_SRC_DIR / "half_horizontal.liquid").write_text(half_h, encoding="utf-8")

    half_v = """<div class="ep-subview">
  <div class="ep-subview-body">
    <div class="ep-header">
      <div class="ep-title-row">
        <span class="ep-kicker">{{ kicker }}</span>
      </div>
      <h1 class="ep-title" style="font-size:21px;">{{ title }}</h1>
      <div class="ep-insight" style="font-size:14.5px;">{{ core_insight }}</div>
    </div>
    <ul class="ep-bullets">
      {% for b in bullets limit:2 %}
        <li class="ep-bullet"><span class="ep-bullet-label">{{ b.label }}</span><span class="ep-bullet-text">{{ b.text }}</span></li>
      {% endfor %}
    </ul>
    <div class="ep-callout"><span class="ep-callout-badge">{{ callout_badge }}</span><span>{{ callout_text }}</span></div>
  </div>
  <div class="title_bar ep-title-bar">
    <span class="title">心脏电生理 · {{ category_label }}</span>
    <span class="instance">{{ card_index }}/{{ card_total }}</span>
  </div>
</div>
"""
    (RECIPE_SRC_DIR / "half_vertical.liquid").write_text(half_v, encoding="utf-8")

    quadrant = """<div class="ep-subview">
  <div class="ep-subview-body">
    <div class="ep-header">
      <div class="ep-header-top">
        <span class="ep-kicker">{{ kicker }}</span>
        {% if key_metrics.size > 0 %}
          <span class="ep-metric-pill" style="font-size:12px;"><span class="ep-metric-value">{{ key_metrics[0].value }}</span></span>
        {% endif %}
      </div>
      <h1 class="ep-title" style="font-size:19px;">{{ title }}</h1>
    </div>
    <div class="ep-quad-summary">{{ quadrant_summary }}</div>
  </div>
  <div class="title_bar ep-title-bar">
    <span class="title">EP 卡片</span>
    <span class="instance">{{ card_index }}/{{ card_total }}</span>
  </div>
</div>
"""
    (RECIPE_SRC_DIR / "quadrant.liquid").write_text(quadrant, encoding="utf-8")
    print(f"Built TRMNL Recipe in: {RECIPE_SRC_DIR}")


def main() -> None:
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    DIST_CARDS_DIR.mkdir(parents=True, exist_ok=True)

    deck = json.loads(DECK_PATH.read_text(encoding="utf-8"))
    css_text = CSS_PATH.read_text(encoding="utf-8")

    now_utc = dt.datetime.now(dt.timezone.utc)
    now_iso = now_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
    now_hhmm = (now_utc + dt.timedelta(hours=8)).strftime("%m-%d %H:%M")

    raw_cards = deck["cards"]
    total = len(raw_cards)
    enriched = [enrich_card(c, i + 1, total, now_hhmm) for i, c in enumerate(raw_cards)]

    cards_payload = {
        "schema_version": deck["schema_version"],
        "deck_id": deck["deck_id"],
        "generated_at": now_iso,
        "count": total,
        "cards": enriched,
    }
    (DIST_DIR / "cards.json").write_text(
        json.dumps(cards_payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    for item in enriched:
        (DIST_CARDS_DIR / f"{item['id']}.json").write_text(
            json.dumps(item, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    slot = int(now_utc.timestamp() // 3600) % total
    current_card = enriched[slot]
    (DIST_DIR / "current.json").write_text(
        json.dumps(current_card, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    build_terminus_files(css_text)
    build_trmnl_recipe(css_text)
    print(f"Built dist/cards.json ({total} cards) and dist/current.json (active={current_card['id']})")


if __name__ == "__main__":
    main()
