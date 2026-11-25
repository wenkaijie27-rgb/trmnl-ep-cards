#!/usr/bin/env python3
"""HAOS TRMNL Custom Serve generator for Cardiac EP Knowledge Cards."""

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
    return {"index": 0, "last_updated": None}


def generate(advance: bool = True) -> dict:
    if not ASSETS_DECK.is_file():
        raise FileNotFoundError(f"EP cards deck not found at {ASSETS_DECK}")

    deck = json.loads(ASSETS_DECK.read_text(encoding="utf-8"))
    cards = deck.get("cards") or []
    if not cards:
        raise ValueError("EP cards deck is empty")

    total = len(cards)
    state = _load_state()
    idx = int(state.get("index", 0)) % total
    if advance and state.get("last_updated") is not None:
        idx = (idx + 1) % total

    now_local = dt.datetime.now(dt.timezone(dt.timedelta(hours=8))).strftime("%m-%d %H:%M")

    # Write deck index & per-card pinned files
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    _atomic_write_json(PUBLIC_DIR / "cards.json", deck)

    active_card = None
    for i, item in enumerate(cards):
        card_copy = dict(item)
        card_copy["updated_at"] = now_local
        _atomic_write_json(PUBLIC_DIR / f"{card_copy['id']}.json", card_copy)
        if i == idx:
            active_card = card_copy

    assert active_card is not None
    _atomic_write_json(PUBLIC_DIR / "card.json", active_card)

    new_state = {
        "index": idx,
        "active_id": active_card["id"],
        "last_updated": now_local,
    }
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(new_state, ensure_ascii=False), encoding="utf-8")
    return active_card


if __name__ == "__main__":
    card = generate(advance=True)
    print(f"[EPCards] active={card['id']} ({card['card_index']}/{card['card_total']})")
