#!/usr/bin/env python3
"""Unified entry point for all 24+ sanitizer-proof semantic EP SVGs."""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT_TOOLS = Path(__file__).resolve().parent
if str(_ROOT_TOOLS) not in sys.path:
    sys.path.insert(0, str(_ROOT_TOOLS))

from svgs import ALL_BUILDERS  # noqa: E402

SVG_BUILDERS = ALL_BUILDERS


def render_svg(svg_id: str, uid_prefix: str = "ep") -> str:
    if svg_id not in SVG_BUILDERS:
        raise KeyError(f"Unknown svg_id: {svg_id}")
    return SVG_BUILDERS[svg_id](uid_prefix)


def main() -> None:
    out_dir = Path("/Users/wenkaijie/Documents/Trmnl/ep-cards/prototype/svgs")
    out_dir.mkdir(parents=True, exist_ok=True)
    for svg_id, builder in SVG_BUILDERS.items():
        path = out_dir / f"{svg_id}.svg"
        path.write_text(builder(svg_id.replace("-", "_")), encoding="utf-8")
    print(f"Generated {len(SVG_BUILDERS)} sanitizer-proof SVGs in {out_dir}")


if __name__ == "__main__":
    main()
