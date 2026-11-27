#!/usr/bin/env python3
"""Build distributable artifacts for both Terminus BYOS and TRMNL Cloud Recipe
from the tiered EP Knowledge Card deck (default: decks/basic-24.json):

- dist/cards.json & dist/current.json
- dist/basic/cards.json & dist/basic/current.json
- dist/cards/<id>.json (all 24 pinned endpoints)
- terminus/configuration.yml & terminus/template.html.liquid
- dist/ep-cards-terminus-extension.zip
- trmnl-recipe/src/*
"""

from __future__ import annotations

import datetime as dt
import json
import re
import zipfile
from pathlib import Path

from generate_svgs import render_svg

ROOT = Path(__file__).resolve().parent.parent
BASIC_DECK_PATH = ROOT / "decks" / "basic-24.json"
ADV_DECK_PATH = ROOT / "decks" / "advanced-24.json"
CSS_PATH = ROOT / "shared" / "ep_cards.css"
DIST_DIR = ROOT / "dist"
DIST_ALL_DIR = DIST_DIR / "all"
DIST_BASIC_DIR = DIST_DIR / "basic"
DIST_ADV_DIR = DIST_DIR / "advanced"
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
    "intro": "入门",
    "bridge": "桥接",
}

TIER_LABELS = {
    "basic": "基础组",
    "advanced": "进阶组",
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
    tier = raw_card.get("tier") or "basic"

    expanded = zh.get("expanded") or {}
    mini_table = expanded.get("mini_table")
    table_payload = None
    if mini_table:
        table_payload = {
            "headers": [cjk_space(h) for h in mini_table["headers"]],
            "rows": [[cjk_space(cell) for cell in row] for row in mini_table["rows"]],
        }

    legend_mode = ""
    if raw_card["id"] == "anatomy-koch-triangle":
        legend_mode = "koch"
    elif raw_card["id"] == "anatomy-his-purkinje":
        legend_mode = "his_purkinje"
    elif raw_card["id"] == "anatomy-cs-mitral-annulus":
        legend_mode = "cs_annulus"
    elif raw_card["id"] == "mechanisms-reentry":
        legend_mode = "reentry"
    elif raw_card["id"] == "mechanisms-excitable-gap":
        legend_mode = "excitable_gap"
    elif raw_card["id"] == "ablation-avoid-conduction-axis":
        legend_mode = "ablation_axis"
    elif raw_card["id"] == "anatomy-inferoseptal-recess":
        legend_mode = "inferoseptal_recess"
    elif raw_card["id"] == "anatomy-marshall-cs-sleeve":
        legend_mode = "marshall_sleeve"
    elif raw_card["id"] == "anatomy-left-bundle-variants":
        legend_mode = "left_bundle_variants"
    elif raw_card["id"] == "wpw-mahaim-insertions":
        legend_mode = "mahaim_insertions"
    elif raw_card["id"] == "ablation-para-hisian-target":
        legend_mode = "para_hisian_target"
    elif raw_card["id"] == "ablation-coronary-vein-distance":
        legend_mode = "coronary_vein_distance"

    return {
        "id": raw_card["id"],
        "tier": tier,
        "tier_label": TIER_LABELS.get(tier, tier),
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
        "split_note": cjk_space(zh["split_note"]) if zh.get("split_note") else "",
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
        "legend_mode": legend_mode,
        "svg": svg_markup,
        "updated_at": generated_at,
    }


def _header_block(p: str) -> str:
    return f"""<div class="ep-header">
  <div class="ep-header-top">
    <div class="ep-title-row">
      <span class="ep-kicker">{{{{ {p}kicker }}}}</span>
      <h1 class="ep-title">{{{{ {p}title }}}}</h1>
    </div>
    {{% if {p}key_metrics.size > 0 %}}
      <div class="ep-metrics">
        {{% for m in {p}key_metrics limit:2 %}}
          <span class="ep-metric-pill"><span class="ep-metric-name">{{{{ m.name }}}}</span><span class="ep-metric-value">{{{{ m.value }}}}</span></span>
        {{% endfor %}}
      </div>
    {{% endif %}}
  </div>
  <div class="ep-insight">{{{{ {p}core_insight }}}}</div>
</div>"""


def _expanded_block(p: str) -> str:
    return f"""{{% if {p}clinical_context != blank %}}
  <div class="ep-x-section hidden lg:flex">
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
      <span>TRMNL X 扩展卡面（{{{{ {p}tier_label }}}} · 10.3" 4-bit）</span>
      <span>出处：{{{{ {p}reference_note }}}}</span>
    </div>
  </div>
{{% endif %}}"""


def _full_body_liquid(var_prefix: str) -> str:
    """Return Liquid body using official TRMNL Framework v3.4.6 classes."""
    p = f"{var_prefix}." if var_prefix else ""
    header = _header_block(p)
    expanded = _expanded_block(p)
    return f"""<div class="view view--full ep-view">
  <div class="layout layout--col ep-layout">
    {{% if {p}template == 'split_left' or {p}template == 'split_right' %}}
      <div class="ep-tpl--{{{{ {p}template }}}} flex flex--col w--full h--full">
        <div class="flex flex--row portrait:flex--col ep-split-main-row w--full">
          {{% if {p}template == 'split_left' %}}
            <div class="ep-diagram-box ep-split-diagram">{{{{ {p}svg }}}}</div>
          {{% endif %}}
          <div class="ep-split-text">
            <div class="ep-split-main">
              {header}
              <ul class="ep-bullets ep-bullets--stack">
                {{% for b in {p}bullets %}}
                  <li class="ep-bullet"><span class="ep-bullet-label">{{{{ b.label }}}}</span><span class="ep-bullet-text">{{{{ b.text }}}}</span></li>
                {{% endfor %}}
              </ul>
              {{% if {p}split_note != blank %}}
                <div class="ep-split-note"><span class="ep-split-note-badge">临床锚点</span><span>{{{{ {p}split_note }}}}</span></div>
              {{% endif %}}
            </div>
            <div class="ep-split-footer">
              {{% if {p}legend_mode == 'koch' %}}
                <div class="ep-mini-legend">
                  <span class="ep-leg-item"><i class="ep-leg-swatch ep-leg-solid"></i>实线：隔瓣附着</span>
                  <span class="ep-leg-item"><i class="ep-leg-swatch ep-leg-accent"></i>红/虚线：Todaro 腱</span>
                  <span class="ep-leg-item"><i class="ep-leg-swatch ep-leg-hl"></i>黄/网纹：传导轴邻域</span>
                </div>
              {{% elsif {p}legend_mode == 'his_purkinje' %}}
                <div class="ep-mini-legend">
                  <span class="ep-leg-item"><i class="ep-leg-swatch ep-leg-hl"></i>黄/网纹：纤维体</span>
                  <span class="ep-leg-item"><i class="ep-leg-swatch ep-leg-solid"></i>实线：His 与主干</span>
                  <span class="ep-leg-item"><i class="ep-leg-swatch ep-leg-accent"></i>虚线：远端束支网</span>
                </div>
              {{% elsif {p}legend_mode == 'cs_annulus' %}}
                <div class="ep-mini-legend">
                  <span class="ep-leg-item"><i class="ep-leg-swatch ep-leg-hl"></i>黄/网纹：左房室沟</span>
                  <span class="ep-leg-item"><i class="ep-leg-swatch ep-leg-accent"></i>红/虚线：冠状窦走向</span>
                </div>
              {{% elsif {p}legend_mode == 'reentry' %}}
                <div class="ep-mini-legend">
                  <span class="ep-leg-item"><i class="ep-leg-swatch ep-leg-accent"></i>叉/虚线：单向阻滞处</span>
                  <span class="ep-leg-item"><i class="ep-leg-swatch ep-leg-hl"></i>黄/网纹：慢传导区</span>
                </div>
              {{% elsif {p}legend_mode == 'excitable_gap' %}}
                <div class="ep-mini-legend">
                  <span class="ep-leg-item"><i class="ep-leg-swatch ep-leg-hl"></i>黄/网纹：兴奋间隙</span>
                  <span class="ep-leg-item"><i class="ep-leg-swatch ep-leg-solid"></i>斜纹环：不应尾</span>
                </div>
              {{% elsif {p}legend_mode == 'ablation_axis' %}}
                <div class="ep-mini-legend">
                  <span class="ep-leg-item"><i class="ep-leg-swatch ep-leg-hl"></i>黄/网纹：常用安全靶区</span>
                  <span class="ep-leg-item"><i class="ep-leg-swatch ep-leg-accent"></i>红/叉标：传导轴高危区</span>
                </div>
              {{% elsif {p}legend_mode == 'inferoseptal_recess' %}}
                <div class="ep-mini-legend">
                  <span class="ep-leg-item"><i class="ep-leg-swatch ep-leg-hl"></i>黄/网纹：左室隐窝 (腔内)</span>
                  <span class="ep-leg-item"><i class="ep-leg-swatch ep-leg-accent"></i>红/虚线：房室传导轴</span>
                </div>
              {{% elsif {p}legend_mode == 'marshall_sleeve' %}}
                <div class="ep-mini-legend">
                  <span class="ep-leg-item"><i class="ep-leg-swatch ep-leg-accent"></i>红/虚线：Marshall 肌束</span>
                  <span class="ep-leg-item"><i class="ep-leg-swatch ep-leg-hl"></i>黄/网纹：肌性接入点</span>
                </div>
              {{% elsif {p}legend_mode == 'left_bundle_variants' %}}
                <div class="ep-mini-legend">
                  <span class="ep-leg-item"><i class="ep-leg-swatch ep-leg-accent"></i>红/虚线：间隔纤维变异</span>
                  <span class="ep-leg-item"><i class="ep-leg-swatch ep-leg-hl"></i>黄/网纹：后间隔标测区</span>
                </div>
              {{% elsif {p}legend_mode == 'mahaim_insertions' %}}
                <div class="ep-mini-legend">
                  <span class="ep-leg-item"><i class="ep-leg-swatch ep-leg-accent"></i>红/虚线：常见房束支旁路</span>
                  <span class="ep-leg-item"><i class="ep-leg-swatch ep-leg-hl"></i>黄/网纹：远端右束支接入</span>
                </div>
              {{% elsif {p}legend_mode == 'para_hisian_target' %}}
                <div class="ep-mini-legend">
                  <span class="ep-leg-item"><i class="ep-leg-swatch ep-leg-accent"></i>红/虚线：正常传导轴</span>
                  <span class="ep-leg-item"><i class="ep-leg-swatch ep-leg-hl"></i>黄/网纹：靶端 His 观察窗</span>
                </div>
              {{% elsif {p}legend_mode == 'coronary_vein_distance' %}}
                <div class="ep-mini-legend">
                  <span class="ep-leg-item"><i class="ep-leg-swatch ep-leg-accent"></i>红/虚线：邻近冠状动脉</span>
                  <span class="ep-leg-item"><i class="ep-leg-swatch ep-leg-hl"></i>黄/网纹：最近分离距离</span>
                </div>
              {{% endif %}}
              <div class="ep-callout"><span class="ep-callout-badge">{{{{ {p}callout_badge }}}}</span><span>{{{{ {p}callout_text }}}}</span></div>
            </div>
          </div>
          {{% if {p}template == 'split_right' %}}
            <div class="ep-diagram-box ep-split-diagram">{{{{ {p}svg }}}}</div>
          {{% endif %}}
        </div>
        {expanded}
      </div>
    {{% else %}}
      {{% if {p}template == 'compare_two' %}}
        {{% assign wrap_cls = 'ep-tpl--compare_two' %}}
        {{% if {p}bullets.size == 3 %}}
          {{% assign diag_cls = 'ep-diagram-box ep-compare-diagram ep-compare-diagram--compact' %}}
        {{% else %}}
          {{% assign diag_cls = 'ep-diagram-box ep-compare-diagram' %}}
        {{% endif %}}
        {{% assign body_cls = 'ep-compare-body' %}}
      {{% else %}}
        {{% assign wrap_cls = 'ep-tpl--top_banner' %}}
        {{% if {p}bullets.size == 3 %}}
          {{% assign diag_cls = 'ep-diagram-box ep-banner-diagram ep-banner-diagram--compact' %}}
        {{% else %}}
          {{% assign diag_cls = 'ep-diagram-box ep-banner-diagram' %}}
        {{% endif %}}
        {{% assign body_cls = 'ep-banner-body' %}}
      {{% endif %}}
      <div class="{{{{ wrap_cls }}}} flex flex--col w--full h--full">
        {header}
        <div class="{{{{ diag_cls }}}}">{{{{ {p}svg }}}}</div>
        <div class="{{{{ body_cls }}}}">
          {{% if {p}bullets.size == 3 %}}
            <ul class="ep-bullets ep-bullets--row3 grid grid--cols-3 w--full">
              {{% for b in {p}bullets %}}
                <li class="ep-bullet"><span class="ep-bullet-label">{{{{ b.label }}}}</span><span class="ep-bullet-text">{{{{ b.text }}}}</span></li>
              {{% endfor %}}
            </ul>
          {{% else %}}
            <ul class="ep-bullets ep-bullets--row2 grid grid--cols-2 w--full">
              {{% for b in {p}bullets %}}
                <li class="ep-bullet"><span class="ep-bullet-label">{{{{ b.label }}}}</span><span class="ep-bullet-text">{{{{ b.text }}}}</span></li>
              {{% endfor %}}
            </ul>
          {{% endif %}}
          <div class="ep-callout"><span class="ep-callout-badge">{{{{ {p}callout_badge }}}}</span><span>{{{{ {p}callout_text }}}}</span></div>
        </div>
        {expanded}
      </div>
    {{% endif %}}
  </div>

  <div class="title_bar ep-title-bar">
    <svg class="ep-title-icon" viewBox="0 0 24 24">
      <polyline points="2 12 6 12 8.5 5 11.5 19 14.5 9 17 12 22 12" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    <span class="title">心脏电生理 · {{{{ {p}category_label }}}}</span>
    <span class="instance"><span class="ep-tier-tag ep-tier-tag--{{{{ {p}tier }}}}">{{{{ {p}tier_label }}}}</span><span>{{{{ {p}card_index }}}}/{{{{ {p}card_total }}}} · {{{{ {p}updated_at }}}}</span></span>
  </div>
</div>"""


def build_terminus_files(css_text: str) -> None:
    TERMINUS_DIR.mkdir(parents=True, exist_ok=True)
    config_yml = """version: "0.84.0"
name: "ep_cards"
label: "心脏电生理知识卡"
description: "面向医学生与青年EP医师的心脏电生理知识卡片（基础组 24 卡 + 进阶组 24 卡 = 48 卡）"
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
polling_url: https://wenkaijie27-rgb.github.io/trmnl-ep-cards/{{ trmnl.plugin_settings.custom_fields_values.tier | default: 'all' }}/current.json
polling_headers: ''
name: Cardiac EP Knowledge Cards
description: Illustrated cardiac electrophysiology learning cards (48 cards: Foundations + Advanced tiers) for TRMNL 1-bit, 2-bit, TRMNL X 4-bit, and 4-color BWRY screens.
refresh_interval: 60
custom_fields:
  - keyname: tier
    field_type: select
    name: Deck Tier / 知识层级
    default: all
    options:
      - All Tiers (全部 48 卡): all
      - Foundations (基础组 24 卡): basic
      - Advanced (进阶组 24 卡): advanced
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
    <span class="title">心脏电生理 · {{ category_label }}</span>
    <span class="instance">{{ tier_label }} · {{ card_index }}/{{ card_total }}</span>
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
    <ul class="ep-bullets ep-bullets--stack">
      {% for b in bullets limit:2 %}
        <li class="ep-bullet"><span class="ep-bullet-label">{{ b.label }}</span><span class="ep-bullet-text">{{ b.text }}</span></li>
      {% endfor %}
    </ul>
    <div class="ep-callout"><span class="ep-callout-badge">{{ callout_badge }}</span><span>{{ callout_text }}</span></div>
  </div>
  <div class="title_bar ep-title-bar">
    <span class="title">心脏电生理 · {{ category_label }}</span>
    <span class="instance">{{ tier_label }} · {{ card_index }}/{{ card_total }}</span>
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
    <span class="instance">{{ tier_label }} · {{ card_index }}/{{ card_total }}</span>
  </div>
</div>
"""
    (RECIPE_SRC_DIR / "quadrant.liquid").write_text(quadrant, encoding="utf-8")
    print(f"Built TRMNL Recipe in: {RECIPE_SRC_DIR}")


def _write_tier_outputs(
    out_dir: Path,
    deck_id: str,
    tier_name: str,
    schema_version: str,
    raw_cards: list[dict],
    now_iso: str,
    now_hhmm: str,
    slot_hour: int,
) -> tuple[list[dict], dict]:
    out_dir.mkdir(parents=True, exist_ok=True)
    total = len(raw_cards)
    enriched = [enrich_card(c, i + 1, total, now_hhmm) for i, c in enumerate(raw_cards)]
    payload = {
        "schema_version": schema_version,
        "deck_id": deck_id,
        "tier": tier_name,
        "generated_at": now_iso,
        "count": total,
        "cards": enriched,
    }
    (out_dir / "cards.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    current_card = enriched[slot_hour % total]
    (out_dir / "current.json").write_text(json.dumps(current_card, ensure_ascii=False, indent=2), encoding="utf-8")
    return enriched, current_card


def main() -> None:
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    DIST_CARDS_DIR.mkdir(parents=True, exist_ok=True)

    basic_deck = json.loads(BASIC_DECK_PATH.read_text(encoding="utf-8"))
    adv_deck = json.loads(ADV_DECK_PATH.read_text(encoding="utf-8"))
    css_text = CSS_PATH.read_text(encoding="utf-8")

    now_utc = dt.datetime.now(dt.timezone.utc)
    now_iso = now_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
    now_hhmm = (now_utc + dt.timedelta(hours=8)).strftime("%m-%d %H:%M")
    slot_hour = int(now_utc.timestamp() // 3600)

    basic_raw = basic_deck["cards"]
    adv_raw = adv_deck["cards"]
    # Interleave or concatenate? Keep basic (1..24) followed by advanced (1..24 -> 25..48) deterministically,
    # and assign tier-specific 1..24 indices in /basic/ & /advanced/!
    all_raw = basic_raw + adv_raw

    all_enriched, all_current = _write_tier_outputs(
        DIST_DIR, "ep-cards-all-48", "all", basic_deck["schema_version"], all_raw, now_iso, now_hhmm, slot_hour
    )
    _write_tier_outputs(
        DIST_ALL_DIR, "ep-cards-all-48", "all", basic_deck["schema_version"], all_raw, now_iso, now_hhmm, slot_hour
    )
    basic_enriched, _ = _write_tier_outputs(
        DIST_BASIC_DIR, basic_deck["deck_id"], "basic", basic_deck["schema_version"], basic_raw, now_iso, now_hhmm, slot_hour
    )
    adv_enriched, _ = _write_tier_outputs(
        DIST_ADV_DIR, adv_deck["deck_id"], "advanced", adv_deck["schema_version"], adv_raw, now_iso, now_hhmm, slot_hour
    )

    for item in all_enriched:
        (DIST_CARDS_DIR / f"{item['id']}.json").write_text(
            json.dumps(item, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    build_terminus_files(css_text)
    build_trmnl_recipe(css_text)
    print(
        f"Built dist/cards.json ({len(all_enriched)} cards: {len(basic_enriched)} basic + {len(adv_enriched)} advanced) "
        f"and dist/current.json (active={all_current['id']})"
    )


if __name__ == "__main__":
    main()
