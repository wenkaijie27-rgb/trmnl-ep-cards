#!/usr/bin/env python3
"""Validate EP knowledge card JSON files against Schema v1.0.0, layout compatibility,
800x480 character budgets, abbreviation whitelist, and evidence completeness.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "1.0.0"

CATEGORIES = {
    "conduction_anatomy",
    "basic_intervals",
    "ep_mechanisms",
    "svt_triage",
    "wpw_preexcitation",
    "pacing_maneuvers",
    "wide_qrs_vt",
    "ablation_safety",
}

DIFFICULTIES = {"intro", "bridge"}

TEMPLATES = {
    "split_left",
    "split_right",
    "top_banner",
    "compare_two",
    "focus_concept",
}

ASPECT_RATIOS = {
    "square_1_1",
    "portrait_4_5",
    "landscape_4_3",
    "wide_2_1",
    "ultrawide_3_1",
    "none",
}

TEXT_DENSITIES = {"compact", "balanced", "rich_x_only"}

DIAGRAM_KINDS = {
    "ecg_egm_waveform",
    "ladder_diagram",
    "anatomy_sketch",
    "reentry_circuit",
    "comparison_pair",
    "none",
}

PRODUCTION_ROUTES = {
    "code_generated_svg",
    "sketch_to_svg",
    "redrawn_clinical_svg",
    "none",
}

LABEL_ROLES = {"primary", "accent_red", "highlight_yellow", "muted"}

READING_SCOPES = {
    "full_text",
    "textbook_chapter",
    "guideline",
    "abstract_only",
    "local_note",
}

REVIEW_STATUSES = {"draft", "audited", "approved"}

LAYOUT_COMPATIBILITY = {
    "split_left": {"square_1_1", "portrait_4_5", "landscape_4_3"},
    "split_right": {"square_1_1", "portrait_4_5", "landscape_4_3"},
    "top_banner": {"wide_2_1", "ultrawide_3_1", "landscape_4_3"},
    "compare_two": {"wide_2_1", "landscape_4_3", "square_1_1"},
    "focus_concept": {"none", "square_1_1"},
}

WHITELIST_ABBRS = {
    "AVNRT",
    "AVRT",
    "AT",
    "SVT",
    "WPW",
    "ECG",
    "AH",
    "HV",
    "VA",
    "RP",
    "PR",
    "QRS",
    "ERP",
    "CS",
    "His",
    "PVC",
    "PAC",
    "RBBB",
    "LBBB",
    "VT",
    "AF",
    "SA",
    "AVN",
}

EXEMPT_UPPER_TOKENS = {
    "II",
    "III",
    "IV",
    "VI",
    "ST",
    "QT",
    "RR",
    "HR",
    "BP",
    "LED",
}

BUDGETS = {
    "zh": {
        "kicker": 10,
        "title": 14,
        "core_insight": 38,
        "bullet_label": 6,
        "bullet_text": 28,
        "metric_name": 14,
        "metric_value": 18,
        "pearl_or_pitfall": 36,
        "quadrant_summary": 22,
        "clinical_context": 75,
        "table_header": 16,
        "table_cell": 24,
        "reference_note": 60,
    },
    "en": {
        "kicker": 24,
        "title": 36,
        "core_insight": 95,
        "bullet_label": 16,
        "bullet_text": 72,
        "metric_name": 22,
        "metric_value": 24,
        "pearl_or_pitfall": 90,
        "quadrant_summary": 55,
        "clinical_context": 180,
        "table_header": 24,
        "table_cell": 36,
        "reference_note": 60,
    },
}

ID_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)+$")
SVG_ID_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
UPPER_TOKEN_RE = re.compile(r"(?<![A-Za-z0-9])[A-Z]{2,}(?![A-Za-z0-9])")


def check_budget(
    value: Any,
    limit: int,
    field_path: str,
    errors: list[str],
    warnings: list[str],
) -> None:
    if not isinstance(value, str):
        errors.append(f"{field_path}: expected string, got {type(value).__name__}")
        return
    length = len(value.strip())
    if length == 0:
        errors.append(f"{field_path}: must not be empty")
        return
    if length > limit:
        errors.append(f"{field_path}: length {length} exceeds hard limit {limit} ({value!r})")
    elif length > int(limit * 0.9):
        warnings.append(f"{field_path}: length {length} is close to limit {limit} (>90%)")


def scan_zh_abbreviations(
    zh: dict[str, Any],
    allowed_defined: set[str],
    errors: list[str],
) -> None:
    texts: list[tuple[str, str]] = []
    for key in ("kicker", "title", "core_insight", "quadrant_summary"):
        if isinstance(zh.get(key), str):
            texts.append((f"content.zh.{key}", zh[key]))

    for idx, bullet in enumerate(zh.get("bullets") or []):
        if isinstance(bullet, dict):
            if isinstance(bullet.get("label"), str):
                texts.append((f"content.zh.bullets[{idx}].label", bullet["label"]))
            if isinstance(bullet.get("text"), str):
                texts.append((f"content.zh.bullets[{idx}].text", bullet["text"]))

    for idx, metric in enumerate(zh.get("key_metrics") or []):
        if isinstance(metric, dict):
            if isinstance(metric.get("name"), str):
                texts.append((f"content.zh.key_metrics[{idx}].name", metric["name"]))
            if isinstance(metric.get("value"), str):
                texts.append((f"content.zh.key_metrics[{idx}].value", metric["value"]))

    pop = zh.get("pearl_or_pitfall")
    if isinstance(pop, dict) and isinstance(pop.get("text"), str):
        texts.append(("content.zh.pearl_or_pitfall.text", pop["text"]))

    expanded = zh.get("expanded")
    if isinstance(expanded, dict):
        if isinstance(expanded.get("clinical_context"), str):
            texts.append(("content.zh.expanded.clinical_context", expanded["clinical_context"]))
        mini_table = expanded.get("mini_table")
        if isinstance(mini_table, dict):
            for h_idx, h in enumerate(mini_table.get("headers") or []):
                if isinstance(h, str):
                    texts.append((f"content.zh.expanded.mini_table.headers[{h_idx}]", h))
            for r_idx, row in enumerate(mini_table.get("rows") or []):
                if isinstance(row, list):
                    for c_idx, cell in enumerate(row):
                        if isinstance(cell, str):
                            texts.append(
                                (f"content.zh.expanded.mini_table.rows[{r_idx}][{c_idx}]", cell)
                            )

    allowed = WHITELIST_ABBRS | EXEMPT_UPPER_TOKENS | allowed_defined
    for path, text in texts:
        for match in UPPER_TOKEN_RE.findall(text):
            if match not in allowed:
                errors.append(
                    f"{path}: unlisted uppercase abbreviation '{match}' "
                    f"(neither in whitelist nor in abbreviations.defined_in_card)"
                )


def validate_localized_block(
    lang: str,
    block: Any,
    errors: list[str],
    warnings: list[str],
) -> None:
    if not isinstance(block, dict):
        errors.append(f"content.{lang}: must be an object")
        return

    b = BUDGETS[lang]
    for field in ("kicker", "title", "core_insight", "quadrant_summary"):
        if field not in block:
            errors.append(f"content.{lang}.{field}: missing required field")
        else:
            check_budget(block[field], b[field], f"content.{lang}.{field}", errors, warnings)

    bullets = block.get("bullets")
    if not isinstance(bullets, list) or not (2 <= len(bullets) <= 3):
        errors.append(f"content.{lang}.bullets: must contain 2 to 3 items")
    else:
        for i, item in enumerate(bullets):
            if not isinstance(item, dict):
                errors.append(f"content.{lang}.bullets[{i}]: must be an object")
                continue
            check_budget(item.get("label"), b["bullet_label"], f"content.{lang}.bullets[{i}].label", errors, warnings)
            check_budget(item.get("text"), b["bullet_text"], f"content.{lang}.bullets[{i}].text", errors, warnings)

    metrics = block.get("key_metrics")
    if metrics is not None:
        if not isinstance(metrics, list) or len(metrics) > 3:
            errors.append(f"content.{lang}.key_metrics: must be an array of at most 3 items")
        else:
            for i, m in enumerate(metrics):
                if not isinstance(m, dict):
                    errors.append(f"content.{lang}.key_metrics[{i}]: must be an object")
                    continue
                check_budget(m.get("name"), b["metric_name"], f"content.{lang}.key_metrics[{i}].name", errors, warnings)
                check_budget(m.get("value"), b["metric_value"], f"content.{lang}.key_metrics[{i}].value", errors, warnings)

    pop = block.get("pearl_or_pitfall")
    if not isinstance(pop, dict):
        errors.append(f"content.{lang}.pearl_or_pitfall: missing required object")
    else:
        if pop.get("kind") not in {"pearl", "pitfall"}:
            errors.append(f"content.{lang}.pearl_or_pitfall.kind: must be 'pearl' or 'pitfall'")
        check_budget(pop.get("text"), b["pearl_or_pitfall"], f"content.{lang}.pearl_or_pitfall.text", errors, warnings)

    expanded = block.get("expanded")
    if expanded is not None:
        if not isinstance(expanded, dict):
            errors.append(f"content.{lang}.expanded: must be an object")
        else:
            if "clinical_context" not in expanded:
                errors.append(f"content.{lang}.expanded.clinical_context: missing required field")
            else:
                check_budget(
                    expanded["clinical_context"],
                    b["clinical_context"],
                    f"content.{lang}.expanded.clinical_context",
                    errors,
                    warnings,
                )
            if "reference_note" not in expanded:
                errors.append(f"content.{lang}.expanded.reference_note: missing required field")
            else:
                check_budget(
                    expanded["reference_note"],
                    b["reference_note"],
                    f"content.{lang}.expanded.reference_note",
                    errors,
                    warnings,
                )
            mini_table = expanded.get("mini_table")
            if mini_table is not None:
                if not isinstance(mini_table, dict):
                    errors.append(f"content.{lang}.expanded.mini_table: must be an object")
                else:
                    headers = mini_table.get("headers")
                    rows = mini_table.get("rows")
                    if not isinstance(headers, list) or not (2 <= len(headers) <= 3):
                        errors.append(f"content.{lang}.expanded.mini_table.headers: must have 2 to 3 columns")
                    else:
                        for hi, hv in enumerate(headers):
                            check_budget(
                                hv,
                                b["table_header"],
                                f"content.{lang}.expanded.mini_table.headers[{hi}]",
                                errors,
                                warnings,
                            )
                    if not isinstance(rows, list) or not (1 <= len(rows) <= 4):
                        errors.append(f"content.{lang}.expanded.mini_table.rows: must have 1 to 4 rows")
                    else:
                        col_count = len(headers) if isinstance(headers, list) else None
                        for ri, row in enumerate(rows):
                            if not isinstance(row, list) or not (2 <= len(row) <= 3):
                                errors.append(f"content.{lang}.expanded.mini_table.rows[{ri}]: must have 2 to 3 cells")
                                continue
                            if col_count is not None and len(row) != col_count:
                                errors.append(
                                    f"content.{lang}.expanded.mini_table.rows[{ri}]: cell count {len(row)} != header count {col_count}"
                                )
                            for ci, cell in enumerate(row):
                                check_budget(
                                    cell,
                                    b["table_cell"],
                                    f"content.{lang}.expanded.mini_table.rows[{ri}][{ci}]",
                                    errors,
                                    warnings,
                                )


def validate_card(card: Any, index: int | None = None) -> tuple[str, list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    label = f"card[{index}]" if index is not None else "card"

    if not isinstance(card, dict):
        return label, [f"{label}: card must be a JSON object"], warnings

    card_id = card.get("id")
    if isinstance(card_id, str) and card_id:
        label = card_id
        if not ID_RE.match(card_id):
            errors.append("id: must match kebab-case pattern ^[a-z0-9]+(-[a-z0-9]+)+$")
    else:
        errors.append("id: missing or empty string")

    if card.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version: expected {SCHEMA_VERSION!r}, got {card.get('schema_version')!r}")

    if card.get("category") not in CATEGORIES:
        errors.append(f"category: invalid value {card.get('category')!r}")

    if card.get("difficulty") not in DIFFICULTIES:
        errors.append(f"difficulty: invalid value {card.get('difficulty')!r}")

    tags = card.get("tags")
    if not isinstance(tags, list) or not (2 <= len(tags) <= 5) or any(not isinstance(t, str) or not t.strip() for t in tags):
        errors.append("tags: must be an array of 2 to 5 non-empty strings")

    # Abbreviations
    abbrs = card.get("abbreviations")
    defined_set: set[str] = set()
    if not isinstance(abbrs, dict):
        errors.append("abbreviations: missing required object")
    else:
        wl = abbrs.get("whitelisted")
        if not isinstance(wl, list):
            errors.append("abbreviations.whitelisted: must be an array")
        else:
            invalid_wl = [a for a in wl if a not in WHITELIST_ABBRS]
            if invalid_wl:
                errors.append(f"abbreviations.whitelisted: contains non-whitelisted tokens {invalid_wl}")
        dic = abbrs.get("defined_in_card")
        if not isinstance(dic, list) or len(dic) > 2:
            errors.append("abbreviations.defined_in_card: must be an array of at most 2 items")
        else:
            for i, entry in enumerate(dic):
                if not isinstance(entry, dict) or not all(
                    isinstance(entry.get(k), str) and entry.get(k).strip() for k in ("abbr", "zh", "en")
                ):
                    errors.append(f"abbreviations.defined_in_card[{i}]: requires non-empty abbr, zh, en")
                else:
                    defined_set.add(entry["abbr"].strip())

    # Content
    content = card.get("content")
    if not isinstance(content, dict) or "zh" not in content:
        errors.append("content: missing required 'zh' block")
    else:
        validate_localized_block("zh", content["zh"], errors, warnings)
        if isinstance(content["zh"], dict):
            scan_zh_abbreviations(content["zh"], defined_set, errors)
        if "en" in content and content["en"] is not None:
            validate_localized_block("en", content["en"], errors, warnings)

    # Layout & compatibility
    layout = card.get("layout")
    template = None
    aspect = None
    if not isinstance(layout, dict):
        errors.append("layout: missing required object")
    else:
        template = layout.get("preferred_template")
        aspect = layout.get("diagram_aspect_ratio")
        density = layout.get("text_density")
        if template not in TEMPLATES:
            errors.append(f"layout.preferred_template: invalid value {template!r}")
        if aspect not in ASPECT_RATIOS:
            errors.append(f"layout.diagram_aspect_ratio: invalid value {aspect!r}")
        if density not in TEXT_DENSITIES:
            errors.append(f"layout.text_density: invalid value {density!r}")
        if template in LAYOUT_COMPATIBILITY and aspect in ASPECT_RATIOS:
            if aspect not in LAYOUT_COMPATIBILITY[template]:
                errors.append(
                    f"layout compatibility: template '{template}' is incompatible with diagram_aspect_ratio '{aspect}' "
                    f"(allowed: {sorted(LAYOUT_COMPATIBILITY[template])})"
                )

    # Diagram
    diagram = card.get("diagram")
    if not isinstance(diagram, dict):
        errors.append("diagram: missing required object")
    else:
        req = diagram.get("required")
        kind = diagram.get("kind")
        route = diagram.get("production_route")
        svg_id = diagram.get("svg_id")
        if not isinstance(req, bool):
            errors.append("diagram.required: must be boolean")
        if kind not in DIAGRAM_KINDS:
            errors.append(f"diagram.kind: invalid value {kind!r}")
        if route not in PRODUCTION_ROUTES:
            errors.append(f"diagram.production_route: invalid value {route!r}")
        if svg_id is not None and (not isinstance(svg_id, str) or not SVG_ID_RE.match(svg_id)):
            errors.append(f"diagram.svg_id: invalid kebab-case id {svg_id!r}")

        if req is True:
            if kind == "none":
                errors.append("diagram.kind: cannot be 'none' when diagram.required is true")
            if route == "none":
                errors.append("diagram.production_route: cannot be 'none' when diagram.required is true")
            if aspect == "none":
                errors.append("layout.diagram_aspect_ratio: cannot be 'none' when diagram.required is true")
        elif req is False:
            if aspect is not None and aspect != "none":
                warnings.append("layout.diagram_aspect_ratio should be 'none' when diagram.required is false")

        if not isinstance(diagram.get("visual_goal"), str) or not diagram["visual_goal"].strip():
            errors.append("diagram.visual_goal: must be a non-empty string")
        mse = diagram.get("must_show_elements")
        if not isinstance(mse, list) or (req is True and len(mse) == 0):
            errors.append("diagram.must_show_elements: must be a non-empty array when diagram is required")

        labels = diagram.get("labels")
        if not isinstance(labels, list):
            errors.append("diagram.labels: must be an array")
        elif len(labels) > 8:
            errors.append(f"diagram.labels: {len(labels)} labels exceeds max 8")
        else:
            for i, lbl in enumerate(labels):
                if not isinstance(lbl, dict):
                    errors.append(f"diagram.labels[{i}]: must be an object")
                    continue
                if not isinstance(lbl.get("zh"), str) or not lbl["zh"].strip():
                    errors.append(f"diagram.labels[{i}].zh: must be non-empty string")
                if not isinstance(lbl.get("en"), str) or not lbl["en"].strip():
                    errors.append(f"diagram.labels[{i}].en: must be non-empty string")
                if lbl.get("role") not in LABEL_ROLES:
                    errors.append(f"diagram.labels[{i}].role: invalid role {lbl.get('role')!r}")

        scp = diagram.get("semantic_color_plan")
        if not isinstance(scp, dict):
            errors.append("diagram.semantic_color_plan: missing required object")
        else:
            for k in ("black_primary", "red_accent", "yellow_highlight"):
                if not isinstance(scp.get(k), str) or (req is True and not scp[k].strip()):
                    errors.append(f"diagram.semantic_color_plan.{k}: must be non-empty string")

        checks = diagram.get("medical_accuracy_checks")
        if not isinstance(checks, list):
            errors.append("diagram.medical_accuracy_checks: must be an array")
        elif req is True:
            if len(checks) == 0:
                errors.append("diagram.medical_accuracy_checks: must not be empty when diagram.required is true")
            elif len(checks) < 2:
                warnings.append("diagram.medical_accuracy_checks: recommend at least 2 concrete verification items")

    # Evidence
    evidence = card.get("evidence")
    if not isinstance(evidence, list) or len(evidence) == 0:
        errors.append("evidence: must contain at least 1 evidence item")
    else:
        for i, ev in enumerate(evidence):
            if not isinstance(ev, dict):
                errors.append(f"evidence[{i}]: must be an object")
                continue
            for k in ("source", "identifier", "supporting_quote"):
                if not isinstance(ev.get(k), str) or not ev[k].strip():
                    errors.append(f"evidence[{i}].{k}: must be a non-empty string")
            if ev.get("reading_scope") not in READING_SCOPES:
                errors.append(f"evidence[{i}].reading_scope: invalid value {ev.get('reading_scope')!r}")
            if not isinstance(ev.get("verified_by_human"), bool):
                errors.append(f"evidence[{i}].verified_by_human: must be boolean")

    # Review
    review = card.get("review")
    if not isinstance(review, dict):
        errors.append("review: missing required object")
    else:
        if review.get("status") not in REVIEW_STATUSES:
            errors.append(f"review.status: invalid value {review.get('status')!r}")
        if not isinstance(review.get("golden_prototype_candidate"), bool):
            errors.append("review.golden_prototype_candidate: must be boolean")
        if not isinstance(review.get("uncertainties"), list):
            errors.append("review.uncertainties: must be an array")

    return label, errors, warnings


def validate_payload(payload: Any) -> tuple[list[tuple[str, list[str], list[str]]], list[str]]:
    top_errors: list[str] = []
    results: list[tuple[str, list[str], list[str]]] = []

    if not isinstance(payload, dict):
        return results, ["Root JSON value must be an object (Deck or Card)"]

    if "cards" in payload:
        if payload.get("schema_version") != SCHEMA_VERSION:
            top_errors.append(f"deck.schema_version: expected {SCHEMA_VERSION!r}")
        if not isinstance(payload.get("deck_id"), str) or not SVG_ID_RE.match(payload["deck_id"]):
            top_errors.append("deck.deck_id: must be non-empty kebab-case string")
        if not isinstance(payload.get("generated_at"), str) or not payload["generated_at"].strip():
            top_errors.append("deck.generated_at: missing ISO timestamp")
        cards = payload.get("cards")
        if not isinstance(cards, list) or len(cards) == 0:
            top_errors.append("deck.cards: must be a non-empty array")
        else:
            seen_ids: set[str] = set()
            for idx, card in enumerate(cards):
                lbl, errs, warns = validate_card(card, idx)
                if isinstance(card, dict) and isinstance(card.get("id"), str):
                    cid = card["id"]
                    if cid in seen_ids:
                        errs.append(f"duplicate card id: {cid}")
                    seen_ids.add(cid)
                results.append((lbl, errs, warns))
    else:
        results.append(validate_card(payload))

    return results, top_errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate EP Knowledge Cards JSON")
    parser.add_argument("path", nargs="?", help="Path to card or deck JSON file")
    parser.add_argument("--stdin", action="store_true", help="Read JSON payload from stdin")
    args = parser.parse_args()

    if args.stdin:
        raw = sys.stdin.read()
        source_name = "<stdin>"
    elif args.path:
        p = Path(args.path)
        if not p.is_file():
            print(f"ERROR: File not found: {p}", file=sys.stderr)
            return 1
        raw = p.read_text(encoding="utf-8")
        source_name = str(p)
    else:
        parser.print_help()
        return 1

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"ERROR: Invalid JSON in {source_name}: {exc}", file=sys.stderr)
        return 1

    results, top_errors = validate_payload(payload)
    total_errors = len(top_errors)
    total_warnings = 0

    if top_errors:
        print("Deck-level errors:")
        for err in top_errors:
            print(f"  [ERROR] {err}")

    for lbl, errs, warns in results:
        total_errors += len(errs)
        total_warnings += len(warns)
        status = "PASS" if not errs else "FAIL"
        print(f"[{status}] {lbl} (errors={len(errs)}, warnings={len(warns)})")
        for err in errs:
            print(f"  [ERROR] {err}")
        for warn in warns:
            print(f"  [WARN]  {warn}")

    print(
        f"\nSummary for {source_name}: {len(results)} card(s), "
        f"{total_errors} error(s), {total_warnings} warning(s)."
    )
    return 0 if total_errors == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
