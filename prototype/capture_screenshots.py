#!/usr/bin/env python3
"""Capture exact-viewport PNG screenshots for all standalone prototype HTML files
using headless Google Chrome and verify output PNG dimensions.
"""

from __future__ import annotations

import struct
import subprocess
from pathlib import Path

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
HTML_DIR = Path("/Users/wenkaijie/Documents/Trmnl/ep-cards/prototype/out/html")
PNG_DIR = Path("/Users/wenkaijie/Documents/Trmnl/ep-cards/prototype/out/screenshots")


def png_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"Not a PNG file: {path}")
    w, h = struct.unpack(">II", data[16:24])
    return w, h


def main() -> None:
    PNG_DIR.mkdir(parents=True, exist_ok=True)
    html_files = sorted(HTML_DIR.glob("*.html"))
    if not html_files:
        raise RuntimeError(f"No HTML files found in {HTML_DIR}")

    for html_file in html_files:
        stem = html_file.stem
        is_x = stem.endswith("__trmnl_x")
        w, h = (1040, 780) if is_x else (800, 480)
        out_png = PNG_DIR / f"{stem}.png"
        cmd = [
            CHROME_BIN,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--hide-scrollbars",
            "--force-device-scale-factor=1",
            "--virtual-time-budget=2500",
            f"--window-size={w},{h}",
            f"--screenshot={out_png}",
            html_file.as_uri(),
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        actual_w, actual_h = png_dimensions(out_png)
        assert (actual_w, actual_h) == (w, h), f"Mismatch for {out_png}: got {(actual_w, actual_h)}, expected {(w, h)}"
        print(f"Captured {out_png.name} ({actual_w}x{actual_h})")


if __name__ == "__main__":
    main()
