#!/usr/bin/env python3
"""Verify that generated Terminus template CSS and all embedded SVGs pass
Terminus config/sanitize.yml allowlists without stripping tags, attributes, or CSS.
"""

from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CARDS_JSON = ROOT / "dist" / "cards.json"
TERMINUS_TEMPLATE = ROOT / "terminus" / "template.html.liquid"

# Mirrored from terminus/config/sanitize.yml + Sanitize::Config::RELAXED core tags
ALLOWED_TAGS = {
    "div", "span", "h1", "h2", "h3", "h4", "p", "ul", "ol", "li",
    "table", "thead", "tbody", "tr", "th", "td", "strong", "em", "b", "i", "br",
    "style", "svg", "g", "path", "line", "rect", "ellipse", "circle",
    "polygon", "polyline", "text", "tspan", "canvas", "link", "source",
}

FORBIDDEN_SVG_TAGS = {"defs", "pattern", "marker", "clippath", "use", "image", "foreignobject"}

ALLOWED_GLOBAL_ATTRS = {
    "class", "dir", "hidden", "id", "lang", "style", "tabindex", "title", "translate",
}

ALLOWED_SVG_ATTRS = {
    "svg": {"height", "width", "x", "y", "version", "viewbox", "shape-rendering", "xmlns", "role", "aria-label"},
    "g": {"stroke", "stroke-width", "fill", "transform"},
    "path": {"d", "stroke", "stroke-dasharray", "stroke-dashoffset", "stroke-linecap", "stroke-linejoin", "stroke-opacity", "stroke-width", "fill", "fill-opacity", "shape-rendering", "transform"},
    "line": {"x1", "x2", "y1", "y2", "stroke", "stroke-dasharray", "stroke-dashoffset", "stroke-linecap", "stroke-opacity", "stroke-width", "shape-rendering", "transform"},
    "rect": {"x", "y", "width", "height", "rx", "ry", "stroke", "stroke-dasharray", "stroke-dashoffset", "stroke-linejoin", "stroke-opacity", "stroke-width", "fill", "fill-opacity", "shape-rendering", "transform"},
    "ellipse": {"cx", "cy", "rx", "ry", "stroke", "stroke-dasharray", "stroke-dashoffset", "stroke-opacity", "stroke-width", "fill", "fill-opacity", "shape-rendering", "transform"},
    "circle": {"cx", "cy", "r", "stroke", "stroke-dasharray", "stroke-dashoffset", "stroke-opacity", "stroke-width", "fill", "fill-opacity", "shape-rendering", "transform"},
    "polygon": {"points", "stroke", "stroke-dasharray", "stroke-dashoffset", "stroke-linejoin", "stroke-opacity", "stroke-width", "fill", "fill-opacity", "shape-rendering", "transform"},
    "polyline": {"points", "stroke", "stroke-dasharray", "stroke-dashoffset", "stroke-linecap", "stroke-linejoin", "stroke-opacity", "stroke-width", "fill", "fill-opacity", "shape-rendering", "transform"},
    "text": {"x", "y", "dx", "dy", "rotate", "stroke", "stroke-dasharray", "stroke-dashoffset", "stroke-linecap", "stroke-linejoin", "stroke-opacity", "stroke-width", "fill", "fill-opacity", "transform"},
    "tspan": {"x", "y", "dx", "dy", "rotate", "stroke", "stroke-dasharray", "stroke-dashoffset", "stroke-linecap", "stroke-linejoin", "stroke-opacity", "stroke-width", "fill", "fill-opacity"},
}

ALLOWED_CUSTOM_CSS_VARS = {
    "--screen-w", "--screen-h", "--pixel-ratio", "--dither-pixel-ratio", "--ui-scale", "--gap-scale",
}


class SanitizeAuditParser(HTMLParser):
    def __init__(self, label: str) -> None:
        super().__init__(convert_charrefs=True)
        self.label = label
        self.errors: list[str] = []
        self.in_style = False
        self.style_chunks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        t = tag.lower()
        if t in FORBIDDEN_SVG_TAGS:
            self.errors.append(f"{self.label}: forbidden SVG tag <{tag}> (stripped by Terminus sanitizer)")
        elif t not in ALLOWED_TAGS:
            self.errors.append(f"{self.label}: unallowlisted tag <{tag}>")

        if t == "style":
            self.in_style = True

        allowed_for_tag = ALLOWED_GLOBAL_ATTRS | ALLOWED_SVG_ATTRS.get(t, set())
        for attr_name, attr_val in attrs:
            an = attr_name.lower()
            if an.startswith("data-") or an.startswith("aria-") or an == "role" or an == "xmlns":
                continue
            if t in ALLOWED_SVG_ATTRS and an not in allowed_for_tag:
                self.errors.append(
                    f"{self.label}: attribute '{attr_name}' on <{tag}> is not allowed in Terminus sanitize.yml"
                )
            if an == "style" and attr_val:
                for custom_var in re.findall(r"--[a-zA-Z0-9_-]+", attr_val):
                    if custom_var not in ALLOWED_CUSTOM_CSS_VARS:
                        self.errors.append(f"{self.label}: disallowed CSS custom property '{custom_var}' in inline style")

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "style":
            self.in_style = False

    def handle_data(self, data: str) -> None:
        if self.in_style:
            self.style_chunks.append(data)


def check_css(css_text: str, label: str) -> list[str]:
    errs: list[str] = []
    cleaned = re.sub(r"/\*.*?\*/", "", css_text, flags=re.S)
    custom_props = set(re.findall(r"(?<![.\w-])(--[a-zA-Z0-9_-]+)\s*:", cleaned))
    custom_props |= set(re.findall(r"var\(\s*(--[a-zA-Z0-9_-]+)", cleaned))
    for custom_var in sorted(custom_props):
        if custom_var not in ALLOWED_CUSTOM_CSS_VARS:
            errs.append(f"{label}: disallowed CSS custom property '{custom_var}' in <style>")
    return errs


def main() -> int:
    if not CARDS_JSON.is_file():
        print(f"ERROR: Missing {CARDS_JSON}; run tools/build_dist.py first.", file=sys.stderr)
        return 1
    if not TERMINUS_TEMPLATE.is_file():
        print(f"ERROR: Missing {TERMINUS_TEMPLATE}.", file=sys.stderr)
        return 1

    all_errors: list[str] = []

    tpl_text = TERMINUS_TEMPLATE.read_text(encoding="utf-8")
    # Strip Liquid tags to inspect static HTML + <style> wrapper
    static_html = re.sub(r"\{\%.*?\%\}|\{\{.*?\}\}", "", tpl_text, flags=re.S)
    tpl_parser = SanitizeAuditParser("terminus/template.html.liquid")
    tpl_parser.feed(static_html)
    all_errors.extend(tpl_parser.errors)
    all_errors.extend(check_css("".join(tpl_parser.style_chunks), "terminus/template.html.liquid"))

    deck = json.loads(CARDS_JSON.read_text(encoding="utf-8"))
    for card in deck["cards"]:
        cid = card["id"]
        svg = card.get("svg", "")
        if not svg.strip():
            all_errors.append(f"{cid}: missing svg payload")
            continue
        svg_parser = SanitizeAuditParser(f"svg:{cid}")
        svg_parser.feed(svg)
        all_errors.extend(svg_parser.errors)

    if all_errors:
        print("Terminus sanitizer audit FAILED:")
        for e in all_errors:
            print(f"  [ERROR] {e}")
        return 1

    print(
        f"[PASS] Terminus sanitizer audit passed for template.html.liquid + "
        f"{len(deck['cards'])} embedded SVG(s) (0 errors)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
