#!/usr/bin/env python3
"""HAOS TRMNL Custom Serve generator for Cardiac EP Knowledge Cards (Basic + Advanced tiers)."""

from __future__ import annotations

import datetime as dt
import json
import os
import tempfile
from pathlib import Path

ASSETS_DECK = Path(os.environ.get("EP_CARDS_ASSETS", "/app/assets/EPCards/cards.json"))
PUBLIC_DIR = Path(os.environ.get("EP_CARDS_PUBLIC", "/data/public/EPCards"))
STATE_FILE = Path(os.environ.get("EP_CARDS_STATE", "/data/private/ep_cards_state.json"))


def _atomic_write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(payload, ensure_ascii=False, indent=2)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(raw)
        os.chmod(tmp_name, 0o644)
        os.replace(tmp_name, path)
    except Exception:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)
        raise


def _load_state() -> dict:
    if STATE_FILE.is_file():
        try:
            data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return data
        except Exception:
            pass
    return {"index": 0, "basic_index": 0, "advanced_index": 0, "last_updated": None}


def _write_tier_slice(
    out_dir: Path,
    base_deck: dict,
    tier_name: str,
    cards: list[dict],
    idx_key: str,
    state: dict,
    advance: bool,
    now_local: str,
) -> tuple[int, dict]:
    total = len(cards)
    idx = int(state.get(idx_key, 0)) % total
    if advance and state.get("last_updated") is not None:
        idx = (idx + 1) % total

    reindexed = []
    for i, item in enumerate(cards):
        c = dict(item)
        c["card_index"] = i + 1
        c["card_total"] = total
        c["updated_at"] = now_local
        reindexed.append(c)

    tier_deck = {
        "schema_version": base_deck.get("schema_version", "1.0.0"),
        "deck_id": f"ep-cards-{tier_name}-{total}",
        "tier": tier_name,
        "generated_at": base_deck.get("generated_at", ""),
        "count": total,
        "cards": reindexed,
    }
    _atomic_write_json(out_dir / "cards.json", tier_deck)
    active = reindexed[idx]
    _atomic_write_json(out_dir / "card.json", active)
    return idx, active


def generate(advance: bool = True) -> dict:
    if not ASSETS_DECK.is_file():
        raise FileNotFoundError(f"EP cards deck not found at {ASSETS_DECK}")

    deck = json.loads(ASSETS_DECK.read_text(encoding="utf-8"))
    cards = deck.get("cards") or []
    if not cards:
        raise ValueError("EP cards deck is empty")

    now_local = dt.datetime.now(dt.timezone(dt.timedelta(hours=8))).strftime("%m-%d %H:%M")
    state = _load_state()

    # Combined 48-card endpoints (/EPCards/cards.json & /EPCards/card.json)
    all_idx, active_card = _write_tier_slice(
        PUBLIC_DIR, deck, "all", cards, "index", state, advance, now_local
    )

    # Individual pinned card endpoints (/EPCards/<id>.json)
    for item in cards:
        card_copy = dict(item)
        card_copy["updated_at"] = now_local
        _atomic_write_json(PUBLIC_DIR / f"{card_copy['id']}.json", card_copy)

    # Tier-specific endpoints (/EPCards/basic/ & /EPCards/advanced/)
    basic_cards = [c for c in cards if c.get("tier", "basic") == "basic"]
    adv_cards = [c for c in cards if c.get("tier") == "advanced"]

    basic_idx = 0
    if basic_cards:
        basic_idx, _ = _write_tier_slice(
            PUBLIC_DIR / "basic", deck, "basic", basic_cards, "basic_index", state, advance, now_local
        )
    adv_idx = 0
    if adv_cards:
        adv_idx, _ = _write_tier_slice(
            PUBLIC_DIR / "advanced", deck, "advanced", adv_cards, "advanced_index", state, advance, now_local
        )

    new_state = {
        "index": all_idx,
        "basic_index": basic_idx,
        "advanced_index": adv_idx,
        "active_id": active_card["id"],
        "last_updated": now_local,
    }
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(new_state, ensure_ascii=False), encoding="utf-8")
    return active_card


if __name__ == "__main__":
    card = generate(advance=True)
    print(f"[EPCards] active={card['id']} ({card['card_index']}/{card['card_total']})")
