#!/usr/bin/env python3
"""Generate Terminus-sanitizer-proof semantic inline SVGs for EP knowledge cards.

Design constraints enforced for Terminus Sanitizer (config/sanitize.yml) + multi-screen TRMNL:
- Allowed SVG tags only: svg, g, path, line, rect, ellipse, circle, polygon, polyline, text, tspan.
- NO <defs>, <pattern>, <marker>, <clipPath>, marker-start, or marker-end.
- Arrowheads are explicit <polygon> shapes computed geometrically.
- Monochrome diagonal hatch fills are explicit clipped <line> segments inside <g class="ep-hatch-group">
  layered over <path/rect/ellipse class="ep-hl-area">. On 4-bit & 4-color screens, CSS hides
  .ep-hatch-group and swaps .ep-hl-area fill to smooth gray or yellow.
- All <text> typography lives in style="..." (not XML attributes like font-size/text-anchor).
- Every shape carries explicit monochrome fallback stroke/fill attributes.
"""

from __future__ import annotations

import math
from pathlib import Path


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
    stroke_width: float = 1.4,
) -> str:
    """Generate explicit diagonal hatch <line> segments clipped inside rectangle (x, y, w, h)."""
    lines: list[str] = []
    # Support -45 deg (slope -1: x + y = c) and +45 deg (slope +1: y - x = c)
    if angle_deg < 0:
        c_min = x + y + spacing * 0.5
        c_max = (x + w) + (y + h) - spacing * 0.5
        c = c_min
        while c <= c_max:
            pts: list[tuple[float, float]] = []
            # Intersect x + y = c with rect edges
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
        c_min = y - (x + w) + spacing * 0.5
        c_max = (y + h) - x - spacing * 0.5
        c = c_min
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
    stroke_width: float = 1.4,
) -> str:
    """Generate explicit 45-degree hatch <line> segments clipped inside a rotated ellipse."""
    # In local unrotated coords (u, v) inside (u/rx)^2 + (v/ry)^2 <= 1,
    # scan diagonal u + v = c, then rotate back by rot_deg around (cx, cy).
    rad = math.radians(rot_deg)
    cos_r, sin_r = math.cos(rad), math.sin(rad)
    c_lim = math.sqrt(rx * rx + ry * ry)
    c = -c_lim + spacing * 0.6
    lines: list[str] = []
    denom = rx * rx + ry * ry
    while c <= c_lim - spacing * 0.6:
        # Solve (u/rx)^2 + ((c - u)/ry)^2 = 1
        # (rx^2 + ry^2) u^2 - 2 c rx^2 u + rx^2 (c^2 - ry^2) = 0
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
            # Inset slightly by 1px so lines stay strictly inside border
            u1_i = u1 * 0.94
            v1_i = v1 * 0.94
            u2_i = u2 * 0.94
            v2_i = v2 * 0.94
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


def svg_koch_triangle(uid: str = "koch") -> str:
    """Right atrial endocardial view of Koch's triangle (aligned to Cabrera 2020 Fig. 3B)."""
    apex_hatch = ellipse_hatch_lines(236, 128, 36, 13, spacing=6.5, rot_deg=-48.0, stroke_width=1.4)
    badge_hatch = rect_hatch_lines(96, 54, 88, 23, spacing=6.0, angle_deg=45.0, stroke_width=1.1)
    bundle_arrow = arrow_polygon(318, 74, 2.0, length=9.5, half_width=4.4, css_class="ep-ink-fill", fallback_fill="#000000")

    return f"""<svg class="ep-svg ep-svg--square" viewBox="0 0 360 350" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Koch三角右房腔内观解剖简笔画">
  <rect x="0" y="0" width="360" height="350" fill="#ffffff"/>

  <!-- Subtle outer anatomical right atrial endocardial frame -->
  <path d="M 22 252 C 18 168, 56 88, 146 42 C 208 12, 282 14, 336 42" fill="none" class="ep-muted-stroke" stroke="#555555" stroke-width="1.4" stroke-dasharray="3,3"/>
  <path d="M 336 42 C 344 128, 344 226, 326 308" fill="none" class="ep-muted-stroke" stroke="#555555" stroke-width="1.2" stroke-dasharray="3,3"/>
  <path d="M 22 252 C 38 302, 86 328, 174 328 C 242 328, 294 318, 326 308" fill="none" class="ep-muted-stroke" stroke="#555555" stroke-width="1.4" stroke-dasharray="3,3"/>

  <!-- Membranous septum / aortic root hint at upper-right apex -->
  <path d="M 244 52 C 266 42, 294 46, 314 66" fill="none" class="ep-muted-stroke" stroke="#555555" stroke-width="1.6"/>
  <path d="M 256 76 C 272 68, 292 70, 306 82" fill="none" class="ep-muted-stroke" stroke="#555555" stroke-width="1.2"/>

  <!-- Conduction axis neighborhood (compact AVN + penetrating bundle zone near apex) -->
  <ellipse cx="236" cy="128" rx="36" ry="13" transform="rotate(-48 236 128)"
           fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.5" stroke-dasharray="4,2.5"/>
  {apex_hatch}
  <circle cx="268" cy="88" r="4" fill="#ffffff" class="ep-paper-fill ep-ink-stroke" stroke="#000000" stroke-width="1.8"/>

  <!-- Penetrating bundle continuation upward-right past apex -->
  <path d="M 271 86 C 284 78, 298 74, 312 74" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.6" stroke-linecap="round"/>
  {bundle_arrow}

  <!-- Triangle of Koch inner subtle guide -->
  <path d="M 118 232 L 258 100 L 256 266 Z" fill="none" class="ep-muted-stroke" stroke="#555555" stroke-width="0.9" stroke-dasharray="2,4"/>

  <!-- Tricuspid septal leaflet cusps & chordae hints on right side -->
  <path d="M 284 134 C 304 146, 316 162, 314 182 C 312 198, 300 212, 292 224 C 310 236, 318 256, 306 276"
        fill="none" class="ep-muted-stroke" stroke="#555555" stroke-width="1.5"/>
  <path d="M 314 182 L 336 190 M 304 208 L 334 218 M 308 254 L 334 264" fill="none" class="ep-muted-stroke" stroke="#555555" stroke-width="1.1"/>

  <!-- 1. Septal leaflet hinge line (solid bold primary ink) -->
  <path d="M 286 292 C 268 236, 266 164, 268 94"
        fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="3.2" stroke-linecap="round"/>

  <!-- 2. Tendon of Todaro (accent red on 4-color, thick dashed on monochrome) -->
  <path d="M 60 256 C 118 206, 194 142, 263 92"
        fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="3.2" stroke-dasharray="9,5" stroke-linecap="round"/>

  <!-- 3. Coronary sinus ostium (base of triangle, lower-left) -->
  <g transform="translate(122, 264) rotate(-14)">
    <ellipse cx="0" cy="0" rx="30" ry="20" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="2.8"/>
    <path d="M -20 -4 C -8 -13, 10 -12, 20 -3" fill="none" class="ep-muted-stroke" stroke="#555555" stroke-width="1.4"/>
    <path d="M -17 6 C -6 12, 8 12, 18 5" fill="none" class="ep-muted-stroke" stroke="#555555" stroke-width="1.2"/>
  </g>

  <!-- Corner view badge: 右房腔内观 -->
  <rect x="12" y="12" width="90" height="24" rx="4" fill="#ffffff" class="ep-muted-stroke" stroke="#555555" stroke-width="1.2"/>
  <text x="57" y="28" fill="#444444" class="ep-svg-label ep-muted-fill" style="font-size:12.5px;font-weight:700;text-anchor:middle;">右房腔内观</text>

  <!-- Label: 三角尖 -->
  <line x1="271" y1="84" x2="294" y2="54" class="ep-ink-stroke" stroke="#000000" stroke-width="1.3"/>
  <rect x="271" y="34" width="50" height="18" rx="3" fill="#ffffff"/>
  <text x="296" y="48" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:14px;font-weight:700;text-anchor:middle;">三角尖</text>

  <!-- Label: 传导轴邻域 (highlight) -->
  <line x1="224" y1="120" x2="176" y2="76" class="ep-ink-stroke" stroke="#000000" stroke-width="1.3"/>
  <rect x="96" y="54" width="88" height="23" rx="4" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.2"/>
  {badge_hatch}
  <rect x="103" y="57" width="74" height="17" rx="2" fill="#ffffff" class="ep-hl-label-bg"/>
  <text x="140" y="70" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:13px;font-weight:700;text-anchor:middle;">传导轴邻域</text>

  <!-- Label: Todaro 腱 (accent) -->
  <line x1="138" y1="186" x2="94" y2="150" class="ep-accent-stroke" stroke="#000000" stroke-width="1.4"/>
  <rect x="33" y="130" width="82" height="18" rx="3" fill="#ffffff"/>
  <text x="74" y="144" fill="#000000" class="ep-svg-label ep-accent-fill" style="font-size:14px;font-weight:700;text-anchor:middle;">Todaro 腱</text>

  <!-- Label: 隔瓣附着线 -->
  <line x1="266" y1="216" x2="226" y2="216" class="ep-ink-stroke" stroke="#000000" stroke-width="1.3"/>
  <rect x="144" y="207" width="80" height="18" rx="3" fill="#ffffff"/>
  <text x="184" y="221" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:13.5px;font-weight:700;text-anchor:middle;">隔瓣附着线</text>

  <!-- Label: 冠状窦口 -->
  <line x1="118" y1="285" x2="96" y2="314" class="ep-ink-stroke" stroke="#000000" stroke-width="1.3"/>
  <rect x="54" y="318" width="72" height="18" rx="3" fill="#ffffff"/>
  <text x="90" y="333" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:14px;font-weight:700;text-anchor:middle;">冠状窦口</text>
</svg>"""


def svg_ah_hv_intervals(uid: str = "ahhv") -> str:
    """Synchronized Surface ECG + His EGM showing AH and HV cursors (aligned to Issa 3e Fig. 4.19)."""
    grid_lines = "\n".join(
        f'  <line x1="{x}" y1="24" x2="{x}" y2="178" class="ep-grid-line" stroke="#dddddd" stroke-width="1" stroke-dasharray="2,4"/>'
        for x in range(126, 710, 60)
    )
    ah_hatch = rect_hatch_lines(186, 76, 114, 26, spacing=7.0, angle_deg=-45.0, stroke_width=1.3)
    hv_hatch = rect_hatch_lines(300, 76, 54, 26, spacing=6.0, angle_deg=45.0, stroke_width=1.2)
    ah_arrows = (
        arrow_polygon(188, 89, 180.0, length=6.5, half_width=3.2)
        + arrow_polygon(296, 89, 0.0, length=6.5, half_width=3.2)
    )
    hv_arrows = (
        arrow_polygon(304, 89, 180.0, length=6.0, half_width=3.0)
        + arrow_polygon(352, 89, 0.0, length=6.0, half_width=3.0)
    )

    return f"""<svg class="ep-svg ep-svg--banner" viewBox="0 0 740 205" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="同步体表与His导联AH与HV间期测量示意图">
  <rect x="0" y="0" width="740" height="205" fill="#ffffff"/>

  <!-- Subtle 50ms vertical time grid -->
  {grid_lines}

  <!-- Track Labels (Left Margin) -->
  <text x="14" y="54" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:14px;font-weight:700;">体表导联</text>
  <text x="14" y="69" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:11.5px;font-weight:600;">Surface ECG</text>

  <text x="14" y="138" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:14px;font-weight:700;">His 导联</text>
  <text x="14" y="153" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:11.5px;font-weight:600;">His prox</text>

  <!-- Caliper Measurement Bands between tracks (y=76..102) -->
  <!-- AH Band: x=186..300 -->
  <rect x="186" y="76" width="114" height="26" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.2"/>
  {ah_hatch}
  <line x1="192" y1="89" x2="292" y2="89" class="ep-ink-stroke" stroke="#000000" stroke-width="1.3"/>
  {ah_arrows}
  <rect x="229" y="79" width="28" height="20" rx="3" fill="#ffffff"/>
  <text x="243" y="94" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:14px;font-weight:800;text-anchor:middle;">AH</text>

  <!-- HV Band: x=300..354 -->
  <rect x="300" y="76" width="54" height="26" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.2"/>
  {hv_hatch}
  <line x1="307" y1="89" x2="348" y2="89" class="ep-ink-stroke" stroke="#000000" stroke-width="1.3"/>
  {hv_arrows}
  <rect x="314" y="79" width="26" height="20" rx="3" fill="#ffffff"/>
  <text x="327" y="94" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:14px;font-weight:800;text-anchor:middle;">HV</text>

  <!-- Vertical Alignment Cursors -->
  <line x1="186" y1="28" x2="186" y2="172" class="ep-ink-stroke" stroke="#000000" stroke-width="1.5" stroke-dasharray="5,3"/>
  <line x1="298.5" y1="22" x2="298.5" y2="176" class="ep-accent-stroke" stroke="#000000" stroke-width="2.0"/>
  <line x1="302.5" y1="22" x2="302.5" y2="176" class="ep-accent-stroke" stroke="#000000" stroke-width="2.0"/>
  <line x1="354" y1="22" x2="354" y2="176" class="ep-ink-stroke" stroke="#000000" stroke-width="1.8" stroke-dasharray="5,3"/>
  <line x1="384" y1="112" x2="384" y2="172" class="ep-muted-stroke" stroke="#555555" stroke-width="1.3" stroke-dasharray="2,3"/>

  <!-- Top Waveform: Surface ECG (P - QRS - T) -->
  <path d="M 105 56 L 146 56 C 158 56, 166 41, 182 41 C 198 41, 206 56, 218 56 L 354 56 L 362 63 L 376 14 L 390 68 L 398 56 L 478 56 C 504 56, 524 38, 550 38 C 576 38, 594 56, 624 56 L 720 56"
        fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>

  <!-- Bottom Waveform: His Channel (Local A -> H -> Delayed Local V) -->
  <path d="M 105 142 L 186 142 L 192 122 L 199 160 L 207 128 L 214 150 L 220 142 L 300 142 L 304 118 L 309 162 L 314 134 L 318 142 L 384 142 L 391 112 L 399 170 L 407 120 L 415 154 L 422 142 L 720 142"
        fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.3" stroke-linejoin="round" stroke-linecap="round"/>

  <!-- Cursor & Peak Labels -->
  <rect x="172" y="3" width="122" height="16" rx="2" fill="#ffffff"/>
  <text x="292" y="16" fill="#000000" class="ep-svg-label ep-accent-fill" style="font-size:13.5px;font-weight:800;text-anchor:end;">His 起点 (共用界标)</text>

  <rect x="359" y="3" width="194" height="16" rx="2" fill="#ffffff"/>
  <text x="361" y="16" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:13px;font-weight:700;text-anchor:start;">体表 QRS 起点（最早室激动）</text>

  <rect x="106" y="161" width="76" height="17" rx="2" fill="#ffffff"/>
  <text x="180" y="175" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:13px;font-weight:700;text-anchor:end;">局部房波 A</text>

  <rect x="383" y="162" width="112" height="17" rx="2" fill="#ffffff"/>
  <text x="385" y="176" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:12.5px;font-weight:700;text-anchor:start;">局部室波 V (较迟)</text>

  <!-- Bottom Time Scale Bar (120px = 100ms) -->
  <line x1="560" y1="191" x2="680" y2="191" class="ep-ink-stroke" stroke="#000000" stroke-width="2"/>
  <line x1="560" y1="186" x2="560" y2="196" class="ep-ink-stroke" stroke="#000000" stroke-width="2"/>
  <line x1="680" y1="186" x2="680" y2="196" class="ep-ink-stroke" stroke="#000000" stroke-width="2"/>
  <text x="552" y="195" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:11.5px;font-weight:600;text-anchor:end;">等比例时标（示例 AH 95 ms · HV 45 ms）</text>
  <text x="688" y="195" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:12px;font-weight:700;text-anchor:start;">100 ms</text>
</svg>"""


def _avrt_panel(x0: int, mode: str) -> str:
    """Render one isomorphic panel for Orthodromic or Antidromic AVRT."""
    is_ortho = mode == "ortho"
    title = "顺向型 AVRT" if is_ortho else "逆向型 AVRT"
    sub = "经房室结—希浦下行" if is_ortho else "经旁路下行 · 逆传房室结"

    if is_ortho:
        avn_arrow = arrow_polygon(118, 106, 90.0, length=9.0, half_width=4.4, css_class="ep-ink-fill", fallback_fill="#000000")
        ap_arrow = arrow_polygon(256, 46, -90.0, length=9.0, half_width=4.4, css_class="ep-accent-fill", fallback_fill="#000000")
        top_loop = (
            '<path d="M 244 38 Q 186 24 134 37" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2"/>'
            + arrow_polygon(128, 38, 166.0, length=8.5, half_width=4.0, css_class="ep-ink-fill", fallback_fill="#000000")
        )
        bot_loop = (
            '<path d="M 134 114 Q 190 128 240 114" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2"/>'
            + arrow_polygon(246, 112, -16.0, length=8.5, half_width=4.0, css_class="ep-ink-fill", fallback_fill="#000000")
        )
        hl_cx, hl_cy, hl_rx, hl_ry = 118, 108, 34, 15
        qrs_path = (
            "M 24 176 L 86 176 C 92 176, 96 164, 104 164 C 112 164, 116 176, 122 176 "
            "L 146 176 L 151 182 L 158 144 L 165 184 L 170 176 "
            "L 200 176 C 214 176, 226 165, 240 165 C 254 165, 266 176, 280 176 L 326 176"
        )
        qrs_badge = "窄 QRS（经希浦同步）"
        qrs_w_x1, qrs_w_x2 = 146, 170
        qrs_tag = "窄"
    else:
        avn_arrow = arrow_polygon(118, 46, -90.0, length=9.0, half_width=4.4, css_class="ep-ink-fill", fallback_fill="#000000")
        ap_arrow = arrow_polygon(256, 106, 90.0, length=9.0, half_width=4.4, css_class="ep-accent-fill", fallback_fill="#000000")
        top_loop = (
            '<path d="M 128 38 Q 186 24 238 37" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2"/>'
            + arrow_polygon(244, 38, 14.0, length=8.5, half_width=4.0, css_class="ep-ink-fill", fallback_fill="#000000")
        )
        bot_loop = (
            '<path d="M 246 112 Q 190 128 140 115" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2"/>'
            + arrow_polygon(134, 114, -166.0, length=8.5, half_width=4.0, css_class="ep-ink-fill", fallback_fill="#000000")
        )
        hl_cx, hl_cy, hl_rx, hl_ry = 256, 108, 34, 15
        qrs_path = (
            "M 24 176 L 86 176 C 92 176, 96 164, 104 164 C 112 164, 116 176, 122 176 "
            "L 132 176 C 142 172, 152 161, 162 145 L 176 154 L 194 185 L 204 176 "
            "L 220 176 C 236 176, 246 187, 260 187 C 274 187, 284 176, 298 176 L 326 176"
        )
        qrs_badge = "宽 QRS · 完全预激"
        qrs_w_x1, qrs_w_x2 = 132, 204
        qrs_tag = "宽"

    exit_hatch = ellipse_hatch_lines(hl_cx, hl_cy, hl_rx, hl_ry, spacing=7.0, rot_deg=0.0, stroke_width=1.2)

    return f"""  <g transform="translate({x0}, 0)">
    <!-- Panel Frame -->
    <rect x="6" y="6" width="346" height="203" rx="8" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="1.6"/>

    <!-- Panel Header -->
    <text x="20" y="27" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:14.5px;font-weight:800;">{title}</text>
    <text x="338" y="27" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:11.5px;font-weight:600;text-anchor:end;">{sub}</text>

    <!-- Upper Atrium & Lower Ventricle Chambers -->
    <rect x="40" y="36" width="278" height="28" rx="10" fill="#ffffff" class="ep-muted-stroke" stroke="#555555" stroke-width="1.3"/>
    <text x="52" y="54" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:11.5px;font-weight:700;">心房</text>

    <!-- Fibrous Annulus (Insulating Barrier) -->
    <line x1="36" y1="74" x2="98" y2="74" class="ep-ink-stroke" stroke="#000000" stroke-width="2.4"/>
    <line x1="138" y1="74" x2="238" y2="74" class="ep-ink-stroke" stroke="#000000" stroke-width="2.4"/>
    <line x1="274" y1="74" x2="322" y2="74" class="ep-ink-stroke" stroke="#000000" stroke-width="2.4"/>

    <rect x="40" y="84" width="278" height="48" rx="12" fill="#ffffff" class="ep-muted-stroke" stroke="#555555" stroke-width="1.3"/>
    <text x="52" y="112" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:11.5px;font-weight:700;">心室</text>

    <!-- Ventricular Activation Exit Zone Highlight -->
    <ellipse cx="{hl_cx}" cy="{hl_cy}" rx="{hl_rx}" ry="{hl_ry}" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.2" stroke-dasharray="3,2"/>
    {exit_hatch}

    <!-- Normal Axis: AVN + His-Purkinje (solid black) -->
    <ellipse cx="118" cy="74" rx="14" ry="8" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="2"/>
    <line x1="118" y1="50" x2="118" y2="100" class="ep-ink-stroke" stroke="#000000" stroke-width="2.8"/>
    {avn_arrow}
    <rect x="140" y="84" width="76" height="15" rx="2" fill="#ffffff"/>
    <text x="142" y="96" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:11.5px;font-weight:700;">房室结—希浦</text>

    <!-- Accessory Pathway (accent red on 4-color, thick dashed on monochrome) -->
    <line x1="256" y1="50" x2="256" y2="100" class="ep-accent-stroke" stroke="#000000" stroke-width="3.0" stroke-dasharray="6,3.5"/>
    {ap_arrow}
    <rect x="276" y="84" width="28" height="15" rx="2" fill="#ffffff"/>
    <text x="278" y="96" fill="#000000" class="ep-svg-label ep-accent-fill" style="font-size:12px;font-weight:800;">旁路</text>

    <!-- Top & Bottom Loop Connectors -->
    {top_loop}
    {bot_loop}

    <!-- Divider between diagram and ECG strip -->
    <line x1="18" y1="138" x2="340" y2="138" class="ep-muted-stroke" stroke="#555555" stroke-width="1" stroke-dasharray="2,3"/>

    <!-- QRS Duration Bracket -->
    <line x1="{qrs_w_x1}" y1="145" x2="{qrs_w_x1}" y2="190" class="ep-muted-stroke" stroke="#555555" stroke-width="1" stroke-dasharray="2,2"/>
    <line x1="{qrs_w_x2}" y1="145" x2="{qrs_w_x2}" y2="190" class="ep-muted-stroke" stroke="#555555" stroke-width="1" stroke-dasharray="2,2"/>
    <line x1="{qrs_w_x1}" y1="191" x2="{qrs_w_x2}" y2="191" class="ep-accent-stroke" stroke="#000000" stroke-width="2"/>

    <!-- Identical-scale single beat ECG strip -->
    <path d="{qrs_path}" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.3" stroke-linejoin="round" stroke-linecap="round"/>

    <!-- Bottom QRS Description -->
    <text x="22" y="201" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:12.5px;font-weight:700;">{qrs_badge}</text>
    <text x="336" y="201" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:11px;font-weight:600;text-anchor:end;">QRS宽度: {qrs_tag}（同时间尺）</text>
  </g>"""


def svg_avrt_directions(uid: str = "avrt") -> str:
    """Isomorphic two-panel comparison of Orthodromic vs Antidromic AVRT."""
    return f"""<svg class="ep-svg ep-svg--compare" viewBox="0 0 740 215" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="顺向型与逆向型AVRT回路与QRS宽窄对照图">
  <rect x="0" y="0" width="740" height="215" fill="#ffffff"/>
  {_avrt_panel(0, "ortho")}
  <line x1="370" y1="14" x2="370" y2="201" class="ep-muted-stroke" stroke="#555555" stroke-width="1.4" stroke-dasharray="4,4"/>
  {_avrt_panel(382, "anti")}
</svg>"""


SVG_BUILDERS = {
    "anatomy-koch-triangle-diagram": svg_koch_triangle,
    "intervals-ah-hv-diagram": svg_ah_hv_intervals,
    "wpw-avrt-directions-diagram": svg_avrt_directions,
}


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
        print(f"Generated {path}")


if __name__ == "__main__":
    main()
