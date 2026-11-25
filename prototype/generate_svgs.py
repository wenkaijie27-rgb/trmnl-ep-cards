#!/usr/bin/env python3
"""Delegate SVG generation to tools/generate_svgs.py so there is a single SVG source of truth."""

from __future__ import annotations

import importlib.util
from pathlib import Path

_TOOLS_SCRIPT = Path(__file__).resolve().parent.parent / "tools" / "generate_svgs.py"
_SPEC = importlib.util.spec_from_file_location("_tools_generate_svgs", _TOOLS_SCRIPT)
assert _SPEC and _SPEC.loader
_MOD = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MOD)

SVG_BUILDERS = _MOD.SVG_BUILDERS
main = _MOD.main
render_svg = _MOD.render_svg

__all__ = ["SVG_BUILDERS", "main", "render_svg"]

if __name__ == "__main__":
    main()
