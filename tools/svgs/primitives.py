"""Shared sanitizer-proof SVG primitives for EP Knowledge Cards.

Strictly avoids <defs>, <pattern>, <marker>, <clipPath>, and XML typography attrs
so all generated SVGs pass Terminus config/sanitize.yml without alteration.
"""

from __future__ import annotations

import math


def arrow_polygon(
    tip_x: float,
    tip_y: float,
    angle_deg: float,
    length: float = 9.0,
    half_width: float = 4.2,
    css_class: str = "ep-ink-fill",
    fallback_fill: str = "#000000",
) -> str:
    """Return an explicit <polygon> arrowhead pointing along angle_deg (0=+x, 90=+y)."""
    rad = math.radians(angle_deg)
    ux, uy = math.cos(rad), math.sin(rad)
    px, py = -uy, ux
    bx, by = tip_x - ux * length, tip_y - uy * length
    p1x, p1y = bx + px * half_width, by + py * half_width
    p2x, p2y = bx - px * half_width, by - py * half_width
    pts = f"{tip_x:.1f},{tip_y:.1f} {p1x:.1f},{p1y:.1f} {p2x:.1f},{p2y:.1f}"
    return f'<polygon points="{pts}" class="{css_class}" fill="{fallback_fill}"/>'


def rect_hatch_lines(
    x: float,
    y: float,
    w: float,
    h: float,
    spacing: float = 7.0,
    angle_deg: float = -45.0,
    stroke_width: float = 1.3,
) -> str:
    """Generate explicit diagonal hatch <line> segments clipped inside rectangle (x, y, w, h)."""
    lines: list[str] = []
    if angle_deg < 0:
        c = x + y + spacing * 0.5
        c_max = (x + w) + (y + h) - spacing * 0.5
        while c <= c_max:
            pts: list[tuple[float, float]] = []
            y_left = c - x
            if y <= y_left <= y + h:
                pts.append((x, y_left))
            y_right = c - (x + w)
            if y <= y_right <= y + h:
                pts.append((x + w, y_right))
            x_top = c - y
            if x < x_top < x + w:
                pts.append((x_top, y))
            x_bot = c - (y + h)
            if x < x_bot < x + w:
                pts.append((x_bot, y + h))
            if len(pts) >= 2:
                (x1, y1), (x2, y2) = pts[0], pts[1]
                lines.append(
                    f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                    f'class="ep-hatch-line" stroke="#000000" stroke-width="{stroke_width}"/>'
                )
            c += spacing
    else:
        c = y - (x + w) + spacing * 0.5
        c_max = (y + h) - x - spacing * 0.5
        while c <= c_max:
            pts = []
            y_left = x + c
            if y <= y_left <= y + h:
                pts.append((x, y_left))
            y_right = (x + w) + c
            if y <= y_right <= y + h:
                pts.append((x + w, y_right))
            x_top = y - c
            if x < x_top < x + w:
                pts.append((x_top, y))
            x_bot = (y + h) - c
            if x < x_bot < x + w:
                pts.append((x_bot, y + h))
            if len(pts) >= 2:
                (x1, y1), (x2, y2) = pts[0], pts[1]
                lines.append(
                    f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                    f'class="ep-hatch-line" stroke="#000000" stroke-width="{stroke_width}"/>'
                )
            c += spacing
    return '<g class="ep-hatch-group">' + "".join(lines) + "</g>"


def ellipse_hatch_lines(
    cx: float,
    cy: float,
    rx: float,
    ry: float,
    spacing: float = 7.0,
    rot_deg: float = 0.0,
    stroke_width: float = 1.3,
) -> str:
    """Generate explicit 45-degree hatch <line> segments clipped inside a rotated ellipse."""
    rad = math.radians(rot_deg)
    cos_r, sin_r = math.cos(rad), math.sin(rad)
    c_lim = math.sqrt(rx * rx + ry * ry)
    c = -c_lim + spacing * 0.6
    lines: list[str] = []
    denom = rx * rx + ry * ry
    while c <= c_lim - spacing * 0.6:
        a = denom
        b = -2.0 * c * (rx * rx)
        k = (rx * rx) * (c * c - ry * ry)
        disc = b * b - 4.0 * a * k
        if disc > 1e-6:
            sq = math.sqrt(disc)
            u1 = (-b - sq) / (2.0 * a)
            u2 = (-b + sq) / (2.0 * a)
            v1 = c - u1
            v2 = c - u2
            u1_i, v1_i = u1 * 0.94, v1 * 0.94
            u2_i, v2_i = u2 * 0.94, v2 * 0.94
            x1 = cx + u1_i * cos_r - v1_i * sin_r
            y1 = cy + u1_i * sin_r + v1_i * cos_r
            x2 = cx + u2_i * cos_r - v2_i * sin_r
            y2 = cy + u2_i * sin_r + v2_i * cos_r
            lines.append(
                f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                f'class="ep-hatch-line" stroke="#000000" stroke-width="{stroke_width}"/>'
            )
        c += spacing
    return '<g class="ep-hatch-group">' + "".join(lines) + "</g>"


def grid_lines(x_start: int, x_end: int, step: int, y1: int, y2: int) -> str:
    return "\n".join(
        f'  <line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" class="ep-grid-line" stroke="#dddddd" stroke-width="1" stroke-dasharray="2,4"/>'
        for x in range(x_start, x_end + 1, step)
    )


def label_box(
    x: float,
    y: float,
    text: str,
    width: float | None = None,
    height: float = 17.0,
    anchor: str = "middle",
    font_size: float = 13.0,
    font_weight: int = 700,
    role: str = "primary",
    border: bool = False,
    highlight_bg: bool = False,
) -> str:
    """Render crisp text over a clean white (or highlight) backing box."""
    fill_cls = {
        "primary": "ep-ink-fill",
        "accent": "ep-accent-fill",
        "muted": "ep-muted-fill",
    }.get(role, "ep-ink-fill")
    fb_fill = "#444444" if role == "muted" else "#000000"

    if width is None:
        # Approximate compact backing box width
        est = 0.0
        for ch in text:
            est += font_size * (0.98 if ord(ch) > 127 else 0.56)
        width = est + 10.0

    if anchor == "middle":
        rx = x - width / 2.0
    elif anchor == "end":
        rx = x - width + 3.0
    else:
        rx = x - 3.0
    ry = y - height * 0.78

    parts: list[str] = []
    if highlight_bg:
        parts.append(
            f'<rect x="{rx:.1f}" y="{ry:.1f}" width="{width:.1f}" height="{height:.1f}" rx="3" '
            f'fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.2"/>'
        )
        parts.append(rect_hatch_lines(rx, ry, width, height, spacing=6.0, angle_deg=45.0, stroke_width=1.0))
        parts.append(
            f'<rect x="{rx + 4:.1f}" y="{ry + 2:.1f}" width="{max(8.0, width - 8):.1f}" height="{max(8.0, height - 4):.1f}" '
            f'rx="2" fill="#ffffff" class="ep-hl-label-bg"/>'
        )
    else:
        stroke_attr = ' class="ep-muted-stroke" stroke="#555555" stroke-width="1.2"' if border else ""
        parts.append(
            f'<rect x="{rx:.1f}" y="{ry:.1f}" width="{width:.1f}" height="{height:.1f}" rx="3" fill="#ffffff"{stroke_attr}/>'
        )
    parts.append(
        f'<text x="{x:.1f}" y="{y:.1f}" fill="{fb_fill}" class="ep-svg-label {fill_cls}" '
        f'style="font-size:{font_size}px;font-weight:{font_weight};text-anchor:{anchor};">{text}</text>'
    )
    return "".join(parts)


def scale_bar(x1: float, x2: float, y: float, label_right: str, note_left: str = "") -> str:
    parts = [
        f'<line x1="{x1:.1f}" y1="{y:.1f}" x2="{x2:.1f}" y2="{y:.1f}" class="ep-ink-stroke" stroke="#000000" stroke-width="2"/>',
        f'<line x1="{x1:.1f}" y1="{y - 4.5:.1f}" x2="{x1:.1f}" y2="{y + 4.5:.1f}" class="ep-ink-stroke" stroke="#000000" stroke-width="2"/>',
        f'<line x1="{x2:.1f}" y1="{y - 4.5:.1f}" x2="{x2:.1f}" y2="{y + 4.5:.1f}" class="ep-ink-stroke" stroke="#000000" stroke-width="2"/>',
        f'<text x="{x2 + 7:.1f}" y="{y + 4:.1f}" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:12px;font-weight:700;text-anchor:start;">{label_right}</text>',
    ]
    if note_left:
        parts.append(
            f'<text x="{x1 - 8:.1f}" y="{y + 4:.1f}" fill="#4d4d4d" class="ep-svg-label ep-muted-fill" style="font-size:11.5px;font-weight:600;text-anchor:end;">{note_left}</text>'
        )
    return "".join(parts)


def egm_biphasic(x0: float, y0: float, width: float = 24.0, amp: float = 22.0, css_class: str = "ep-ink-stroke", fb: str = "#000000") -> str:
    """Return a sharp high-frequency EGM deflection path segment starting at (x0, y0)."""
    w = width / 4.0
    return (
        f"M {x0:.1f} {y0:.1f} "
        f"L {x0 + w * 0.8:.1f} {y0 - amp:.1f} "
        f"L {x0 + w * 1.8:.1f} {y0 + amp * 0.85:.1f} "
        f"L {x0 + w * 2.8:.1f} {y0 - amp * 0.55:.1f} "
        f"L {x0 + w * 3.5:.1f} {y0 + amp * 0.28:.1f} "
        f"L {x0 + width:.1f} {y0:.1f}"
    )
