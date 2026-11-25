"""SVG generators for Domains 3 & 4: Basic EP Mechanisms & SVT Triage (Cards 7-12)."""

from __future__ import annotations

import math

from .primitives import (
    arrow_polygon,
    egm_biphasic,
    ellipse_hatch_lines,
    grid_lines,
    label_box,
    rect_hatch_lines,
    scale_bar,
)


def svg_reentry(uid: str = "reentry") -> str:
    """7. mechanisms-reentry-diagram (square_1_1, Issa 3e Ch.3)."""
    slow_hatch = ellipse_hatch_lines(255, 175, 18, 52, spacing=6.5, rot_deg=0.0, stroke_width=1.3)
    return f"""<svg class="ep-svg ep-svg--square" viewBox="0 0 360 350" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="折返三要素：单向阻滞、慢传导与环行闭合示意图">
  <rect x="0" y="0" width="360" height="350" fill="#ffffff"/>

  <!-- Premature trigger impulse from top -->
  <line x1="180" y1="22" x2="180" y2="70" class="ep-ink-stroke" stroke="#000000" stroke-width="3.2"/>
  {arrow_polygon(180, 74, 90.0, 9.0, 4.4)}

  <!-- Ring Circuit Outer & Inner Boundaries -->
  <ellipse cx="180" cy="175" rx="94" ry="96" fill="none" class="ep-muted-stroke" stroke="#555555" stroke-width="1.4" stroke-dasharray="3,3"/>
  <ellipse cx="180" cy="175" rx="54" ry="56" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="2.0"/>

  <!-- Slow Conduction Zone on Right Limb -->
  <ellipse cx="255" cy="175" rx="18" ry="52" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.3" stroke-dasharray="4,2.5"/>
  {slow_hatch}

  <!-- Left Limb: Unidirectional Antegrade Block (Red X / Double Bar) -->
  <path d="M 164 80 C 122 86, 104 114, 102 142" fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="2.8" stroke-dasharray="6,4"/>
  <!-- Block bar + X -->
  <line x1="88" y1="146" x2="118" y2="146" class="ep-accent-stroke" stroke="#000000" stroke-width="3.4"/>
  <line x1="94" y1="132" x2="112" y2="150" class="ep-accent-stroke" stroke="#000000" stroke-width="2.6"/>
  <line x1="112" y1="132" x2="94" y2="150" class="ep-accent-stroke" stroke="#000000" stroke-width="2.6"/>

  <!-- Right Limb: Slow Antegrade Propagation (wavy/stepped slow arrow down) -->
  <path d="M 196 80 C 236 88, 255 120, 255 162" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="3.0"/>
  {arrow_polygon(255, 168, 90.0, 9.0, 4.4)}
  <path d="M 255 186 C 254 230, 228 258, 190 264" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="3.0"/>
  {arrow_polygon(184, 265, 175.0, 9.0, 4.4)}

  <!-- Return Limb: Retrograde up recovered Left Limb closing the loop -->
  <path d="M 166 264 C 122 256, 104 222, 104 178" fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="3.0" stroke-dasharray="8,4"/>
  {arrow_polygon(104, 172, -90.0, 9.0, 4.4, css_class="ep-accent-fill")}
  <!-- Distal exit arrow downward -->
  <line x1="180" y1="272" x2="180" y2="314" class="ep-ink-stroke" stroke="#000000" stroke-width="2.6"/>
  {arrow_polygon(180, 320, 90.0, 8.5, 4.0)}

  <!-- Labels (5 schema labels) -->
  {label_box(180, 17, "触发波前 (早搏)", width=106, height=18, font_size=13)}
  {label_box(180, 179, "中心隔离区", width=76, height=19, font_size=12.5, role="muted", border=True)}
  {label_box(58, 122, "单向阻滞", width=66, height=18, font_size=13, role="accent")}
  {label_box(56, 206, "绕行波前返回", width=88, height=18, font_size=13, role="accent")}
  {label_box(54, 166, "已恢复可传", width=74, height=18, font_size=12.5)}
  {label_box(292, 175, "慢传导", width=58, height=22, font_size=13, highlight_bg=True)}
  {label_box(180, 340, "环形通路传出", width=96, height=18, font_size=13)}
</svg>"""


def svg_ah_jump(uid: str = "ahjump") -> str:
    """8. mechanisms-ah-jump-diagram (wide_2_1, Issa 3e Ch.17 p.572)."""
    # Left panel (x=8..440): Dual-beat comparison (S1S2=320 -> AH=110; S1S2=310 -> AH=190 Jump!)
    # Right panel (x=456..732): Discontinuous A1A2 vs AH recovery curve showing >=50 ms vertical jump
    jump_hatch = rect_hatch_lines(582, 54, 28, 88, spacing=6.0, angle_deg=-45.0, stroke_width=1.2)
    return f"""<svg class="ep-svg ep-svg--banner" viewBox="0 0 740 215" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="房室结双径路AH跳跃现象阶梯与恢复曲线图">
  <rect x="0" y="0" width="740" height="215" fill="#ffffff"/>

  <!-- Left Panel: Two His-Channel Sweeps Aligned on A2 -->
  <rect x="8" y="8" width="434" height="199" rx="7" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="1.5"/>
  <text x="20" y="28" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:13.5px;font-weight:800;">联律间期仅缩短 10 ms，AH 骤增 ≥50 ms</text>

  <!-- Track 1: Fast pathway conduction (A1-A2 = 320, AH = 100) -->
  <text x="20" y="64" fill="#4d4d4d" class="ep-svg-label ep-muted-fill" style="font-size:12px;font-weight:700;">快径下传</text>
  <text x="20" y="79" fill="#4d4d4d" class="ep-svg-label ep-muted-fill" style="font-size:11px;font-weight:600;">A1-A2 320</text>
  <path d="M 88 70 L 110 70 {egm_biphasic(110, 70, 20, 18)} L 198 70 {egm_biphasic(198, 70, 20, 18)} L 254 70 {egm_biphasic(254, 70, 14, 20)} L 274 70 {egm_biphasic(274, 70, 22, 22)} L 426 70"
        fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.1" stroke-linejoin="round"/>
  {label_box(120, 46, "前次房波", width=58, height=15, font_size=11.5, role="muted")}
  {label_box(208, 46, "早搏房波", width=58, height=15, font_size=11.5)}
  {label_box(261, 46, "His", width=26, height=15, font_size=11.5)}
  <line x1="200" y1="88" x2="254" y2="88" class="ep-ink-stroke" stroke="#000000" stroke-width="1.6"/>
  {arrow_polygon(200, 88, 180.0, 5.5, 2.8)}
  {arrow_polygon(254, 88, 0.0, 5.5, 2.8)}
  <text x="227" y="102" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:11.5px;font-weight:700;text-anchor:middle;">AH 100</text>

  <line x1="20" y1="114" x2="430" y2="114" class="ep-muted-stroke" stroke="#555555" stroke-width="1" stroke-dasharray="3,3"/>

  <!-- Track 2: Slow pathway jump (A1-A2 = 310, AH = 185!) -->
  <text x="20" y="144" fill="#000000" class="ep-svg-label ep-accent-fill" style="font-size:12px;font-weight:800;">快径遇阻</text>
  <text x="20" y="159" fill="#000000" class="ep-svg-label ep-accent-fill" style="font-size:11px;font-weight:700;">A1-A2 310</text>
  <path d="M 88 150 L 110 150 {egm_biphasic(110, 150, 20, 18)} L 193 150 {egm_biphasic(193, 150, 20, 18)} L 336 150 {egm_biphasic(336, 150, 14, 20)} L 356 150 {egm_biphasic(356, 150, 22, 22)} L 426 150"
        fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.1" stroke-linejoin="round"/>
  <line x1="254" y1="118" x2="254" y2="190" class="ep-muted-stroke" stroke="#555555" stroke-width="1.2" stroke-dasharray="3,3"/>
  <line x1="336" y1="118" x2="336" y2="190" class="ep-accent-stroke" stroke="#000000" stroke-width="1.8" stroke-dasharray="4,2"/>
  <rect x="254" y="164" width="82" height="20" rx="3" fill="#ffffff" class="ep-hl-area ep-accent-stroke" stroke="#000000" stroke-width="1.2"/>
  {rect_hatch_lines(254, 164, 82, 20, spacing=6.0, angle_deg=-45.0, stroke_width=1.1)}
  {label_box(295, 178, "AH 骤增 ≥50", width=76, height=15, font_size=11.5, font_weight=800, role="accent")}
  <text x="434" y="132" fill="#000000" class="ep-svg-label ep-accent-fill" style="font-size:11.5px;font-weight:800;text-anchor:end;">His 明显后移</text>

  <!-- Right Panel: Discontinuous AVN Recovery Curve -->
  <rect x="454" y="8" width="278" height="199" rx="7" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="1.5"/>
  <text x="466" y="28" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:13.5px;font-weight:800;">双径路恢复曲线 (跳跃)</text>

  <!-- Axes -->
  <line x1="494" y1="172" x2="710" y2="172" class="ep-ink-stroke" stroke="#000000" stroke-width="1.8"/>
  <line x1="494" y1="44" x2="494" y2="172" class="ep-ink-stroke" stroke="#000000" stroke-width="1.8"/>
  <text x="602" y="196" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:11.5px;font-weight:700;text-anchor:middle;">联律间期 A1-A2 (缩短 →)</text>
  <text x="476" y="112" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:12px;font-weight:700;text-anchor:middle;">AH</text>

  <!-- Jump zone highlight -->
  <rect x="582" y="54" width="28" height="88" fill="#ffffff" class="ep-hl-area" stroke="none"/>
  {jump_hatch}

  <!-- Fast pathway curve (left/longer A1A2) -->
  <path d="M 508 148 Q 554 146, 588 134" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.8" stroke-linecap="round"/>
  <circle cx="588" cy="134" r="3.5" class="ep-ink-fill" fill="#000000"/>

  <!-- Vertical Jump dashed arrow -->
  <line x1="596" y1="132" x2="596" y2="76" class="ep-accent-stroke" stroke="#000000" stroke-width="2.2" stroke-dasharray="4,2.5"/>
  {arrow_polygon(596, 70, -90.0, 8.0, 3.8, css_class="ep-accent-fill")}

  <!-- Slow pathway curve (right/shorter A1A2) -->
  <path d="M 604 68 Q 642 62, 694 52" fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="2.8" stroke-dasharray="7,3.5" stroke-linecap="round"/>
  <circle cx="604" cy="68" r="3.5" class="ep-accent-fill" fill="#000000"/>

  {label_box(546, 160, "快径", width=36, height=15, font_size=11.5)}
  {label_box(666, 76, "慢径", width=36, height=15, font_size=11.5, role="accent")}
  {label_box(646, 114, "跳跃 ≥50 ms", width=76, height=16, font_size=11.5, font_weight=800, role="accent")}
</svg>"""


def svg_excitable_gap(uid: str = "egap") -> str:
    """9. mechanisms-excitable-gap-diagram (square_1_1, Issa 3e Ch.3 Fig. 3.12)."""
    # Annular reentry track centered at (180, 178), r_in=58, r_out=106
    # Angles (deg, 0=+x, clockwise +y):
    # - Refractory tail: 25° to 215° (heavy shaded/dark solid arc)
    # - Excitable gap (recovered): 215° to 335° (yellow / hatched highlight!)
    # - Active wavefront head: 335° to 25° (bold red arrow)
    def arc_ring(a1_deg: float, a2_deg: float, r_in: float = 58.0, r_out: float = 104.0, cx: float = 180.0, cy: float = 180.0) -> str:
        r1, r2 = math.radians(a1_deg), math.radians(a2_deg)
        large = 1 if ((a2_deg - a1_deg) % 360) > 180 else 0
        x1o, y1o = cx + r_out * math.cos(r1), cy + r_out * math.sin(r1)
        x2o, y2o = cx + r_out * math.cos(r2), cy + r_out * math.sin(r2)
        x2i, y2i = cx + r_in * math.cos(r2), cy + r_in * math.sin(r2)
        x1i, y1i = cx + r_in * math.cos(r1), cy + r_in * math.sin(r1)
        return (
            f"M {x1o:.1f} {y1o:.1f} A {r_out} {r_out} 0 {large} 1 {x2o:.1f} {y2o:.1f} "
            f"L {x2i:.1f} {y2i:.1f} A {r_in} {r_in} 0 {large} 0 {x1i:.1f} {y1i:.1f} Z"
        )

    gap_hatch = ellipse_hatch_lines(180, 96, 54, 18, spacing=6.5, rot_deg=0.0, stroke_width=1.2)
    return f"""<svg class="ep-svg ep-svg--square" viewBox="0 0 360 350" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="折返环推进波前、不应尾与兴奋间隙示意图">
  <rect x="0" y="0" width="360" height="350" fill="#ffffff"/>

  <!-- Outer & Inner Ring Borders -->
  <circle cx="180" cy="180" r="104" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="2.0"/>
  <circle cx="180" cy="180" r="58" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="2.0"/>

  <!-- 1. Refractory Tail (bottom & left-lower arc: 20 deg to 210 deg) -->
  <path d="{arc_ring(20, 210)}" fill="#d4d4d4" class="ep-muted-stroke" stroke="#000000" stroke-width="1.4"/>
  <!-- Hatch extra density for 1-bit legibility on refractory tail -->
  <path d="M 88 228 L 122 204 M 98 248 L 132 220 M 118 264 L 144 234 M 148 276 L 164 242 M 182 282 L 182 240 M 214 274 L 198 238 M 244 256 L 216 226 M 264 226 L 228 206"
        class="ep-ink-stroke" stroke="#000000" stroke-width="2.2"/>

  <!-- 2. Excitable Gap (top arc: 210 deg to 335 deg) -->
  <path d="{arc_ring(210, 335)}" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.5" stroke-dasharray="4,2"/>
  {gap_hatch}

  <!-- 3. Active Wavefront Head (right-top arc: 335 deg to 20 deg) -->
  <path d="M 254 146 A 81 81 0 0 1 256 208" fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="5.0" stroke-linecap="round"/>
  {arrow_polygon(255, 215, 102.0, 11.0, 5.2, css_class="ep-accent-fill")}

  <!-- External Pacing Stimulus entering the Excitable Gap from Top-Left -->
  <path d="M 82 42 L 138 102" fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="2.6" stroke-dasharray="6,3"/>
  {arrow_polygon(142, 107, 47.0, 9.0, 4.2, css_class="ep-accent-fill")}

  <!-- Labels (5 schema labels) -->
  {label_box(180, 184, "折返环核心", width=78, height=20, font_size=13, role="muted", border=True)}
  {label_box(70, 34, "适时刺激", width=72, height=19, font_size=13, role="accent")}
  {label_box(210, 74, "兴奋间隙 (可夺获)", width=118, height=21, font_size=12.5, highlight_bg=True)}
  {label_box(314, 176, "推进波前", width=68, height=19, font_size=13, role="accent")}
  {label_box(180, 322, "不应尾 (尚未恢复，不可刺激)", width=186, height=19, font_size=12.5)}
</svg>"""


def svg_typical_avnrt_short_va(uid: str = "avnrtva") -> str:
    """10. svt-typical-avnrt-short-va-diagram (wide_2_1, ESC 2019 Table 12)."""
    g = grid_lines(130, 710, 60, 22, 184)
    va_hatch = rect_hatch_lines(344, 72, 34, 28, spacing=5.5, angle_deg=-45.0, stroke_width=1.2)
    return f"""<svg class="ep-svg ep-svg--banner" viewBox="0 0 740 205" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="典型AVNRT短VA与体表逆行P波埋没示意图">
  <rect x="0" y="0" width="740" height="205" fill="#ffffff"/>
  {g}
  <text x="16" y="50" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:14px;font-weight:700;">体表导联</text>
  <text x="16" y="65" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:11.5px;font-weight:600;">窄 QRS</text>
  <text x="16" y="138" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:14px;font-weight:700;">His 导联</text>
  <text x="16" y="153" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:11.5px;font-weight:600;">近同步房室波</text>

  <!-- Short VA band (x=344..378 -> 34px ~ 30 ms <= 60 ms!) -->
  <rect x="344" y="72" width="34" height="28" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.2"/>
  {va_hatch}
  {label_box(361, 90, "VA", width=22, height=15, font_size=12, font_weight=800)}

  <!-- Vertical Alignment Cursors -->
  <line x1="344" y1="22" x2="344" y2="176" class="ep-ink-stroke" stroke="#000000" stroke-width="1.8" stroke-dasharray="5,3"/>
  <line x1="378" y1="22" x2="378" y2="176" class="ep-accent-stroke" stroke="#000000" stroke-width="2.2"/>

  <!-- Top Trace: Regular narrow QRS tachycardia (Beat 1 at x=160, Beat 2 at x=344, Beat 3 at x=530) -->
  <path d="M 105 52 L 160 52 L 166 59 L 176 18 L 186 62 L 194 52 L 240 52 C 254 52, 266 38, 280 38 C 294 38, 306 52, 320 52 L 344 52 L 350 59 L 360 18 L 370 62 L 377 45 L 383 52 L 428 52 C 442 52, 454 38, 468 38 C 482 38, 494 52, 508 52 L 530 52 L 536 59 L 546 18 L 556 62 L 564 52 L 710 52"
        fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.4" stroke-linejoin="round"/>
  <!-- Highlight buried retrograde P at terminal QRS -->
  <path d="M 370 62 L 377 45 L 383 52" fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="2.8"/>

  <!-- Bottom Trace: His Channel (H precedes V, and Retrograde A sits tightly at x=378 right inside QRS!) -->
  <path d="M 105 140 L 138 140 {egm_biphasic(138, 140, 14, 18)} L 164 140 {egm_biphasic(164, 140, 18, 20)} L 190 140 {egm_biphasic(190, 140, 20, 22)} L 322 140 {egm_biphasic(322, 140, 14, 18)} L 348 140 {egm_biphasic(348, 140, 18, 20)} L 378 140 {egm_biphasic(378, 140, 20, 24)} L 508 140 {egm_biphasic(508, 140, 14, 18)} L 534 140 {egm_biphasic(534, 140, 18, 20)} L 560 140 {egm_biphasic(560, 140, 20, 22)} L 710 140"
        fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.1" stroke-linejoin="round"/>

  {label_box(336, 16, "QRS 起点", width=62, height=16, anchor="end", font_size=12.5)}
  {label_box(385, 16, "逆行房波 (几乎紧贴 QRS)", width=148, height=16, anchor="start", font_size=12.5, font_weight=800, role="accent")}
  {label_box(392, 174, "His 道逆行 A 波 (VA ≤ 60 ms 示例)", width=190, height=16, anchor="start", font_size=12, role="accent")}
  {scale_bar(556, 668, 192, "100 ms", "短 VA 典型示例")}
</svg>"""


def svg_rp_first_split(uid: str = "rpsplit") -> str:
    """11. svt-rp-first-split-diagram (compare_two, ESC 2019 Fig. 1)."""
    def _panel(x0: int, is_long: bool) -> str:
        title = "长 RP (RP ≥ PR)" if is_long else "短 RP (RP < PR)"
        sub = "P 波紧靠下一跳 QRS" if is_long else "P 波紧跟前一跳 QRS"
        # Two QRS beats at x=76 and x=284
        if not is_long:
            p_x = 128
            rp_x1, rp_x2 = 82, 128
            pr_x1, pr_x2 = 128, 278
            rp_hl = True
        else:
            p_x = 226
            rp_x1, rp_x2 = 82, 226
            pr_x1, pr_x2 = 226, 278
            rp_hl = True

        ecg = (
            f"M 24 108 L 72 108 L 77 115 L 86 64 L 95 117 L 101 108 "
            f"L {p_x - 16} 108 C {p_x - 10} 108, {p_x - 6} 122, {p_x} 122 C {p_x + 6} 122, {p_x + 10} 108, {p_x + 16} 108 "
            f"L 276 108 L 281 115 L 290 64 L 299 117 L 305 108 L 336 108"
        )
        rp_w = rp_x2 - rp_x1
        rp_hatch = rect_hatch_lines(rp_x1, 134, rp_w, 22, spacing=6.0, angle_deg=-45.0, stroke_width=1.1)
        return f"""  <g transform="translate({x0}, 0)">
    <rect x="6" y="6" width="346" height="203" rx="8" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="1.6"/>
    <text x="20" y="28" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:14.5px;font-weight:800;">{title}</text>
    <text x="338" y="28" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:11.5px;font-weight:600;text-anchor:end;">{sub}</text>

    <!-- Vertical Reference Lines: QRS1 (82), P (p_x), QRS2 (278) -->
    <line x1="82" y1="48" x2="82" y2="178" class="ep-ink-stroke" stroke="#000000" stroke-width="1.4" stroke-dasharray="4,3"/>
    <line x1="{p_x}" y1="48" x2="{p_x}" y2="178" class="ep-accent-stroke" stroke="#000000" stroke-width="2.0"/>
    <line x1="278" y1="48" x2="278" y2="178" class="ep-ink-stroke" stroke="#000000" stroke-width="1.4" stroke-dasharray="4,3"/>

    <!-- RP Highlight Band -->
    <rect x="{rp_x1}" y="134" width="{rp_w}" height="22" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.2"/>
    {rp_hatch}
    <line x1="{rp_x1 + 3}" y1="145" x2="{rp_x2 - 3}" y2="145" class="ep-ink-stroke" stroke="#000000" stroke-width="1.3"/>
    {arrow_polygon(rp_x1 + 2, 145, 180.0, 5.5, 2.8)}
    {arrow_polygon(rp_x2 - 2, 145, 0.0, 5.5, 2.8)}
    {label_box((rp_x1 + rp_x2) / 2, 149, "RP", width=24, height=15, font_size=12, font_weight=800)}

    <!-- PR Band -->
    <rect x="{pr_x1}" y="160" width="{pr_x2 - pr_x1}" height="20" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="1.1"/>
    <line x1="{pr_x1 + 3}" y1="170" x2="{pr_x2 - 3}" y2="170" class="ep-ink-stroke" stroke="#000000" stroke-width="1.2"/>
    {label_box((pr_x1 + pr_x2) / 2, 174, "PR", width=24, height=14, font_size=11.5)}

    <!-- ECG Strip -->
    <path d="{ecg}" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.3" stroke-linejoin="round"/>
    <!-- Highlight Retrograde P wave -->
    <path d="M {p_x - 14} 108 C {p_x - 9} 108, {p_x - 5} 122, {p_x} 122 C {p_x + 5} 122, {p_x + 9} 108, {p_x + 14} 108"
          fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="3.0"/>

    {label_box(p_x, 54, "逆行 P 波", width=62, height=16, font_size=12, role="accent")}
    {label_box(180, 198, "短 RP (≤90 ms 多提示典型 AVNRT)" if not is_long else "长 RP (提示 AT / 非典型 AVNRT)", width=220, height=15, font_size=11.5, role="muted")}
  </g>"""

    return f"""<svg class="ep-svg ep-svg--compare" viewBox="0 0 740 215" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="短RP与长RP室上速体表分流对比图">
  <rect x="0" y="0" width="740" height="215" fill="#ffffff"/>
  {_panel(0, False)}
  <line x1="370" y1="14" x2="370" y2="201" class="ep-muted-stroke" stroke="#555555" stroke-width="1.4" stroke-dasharray="4,4"/>
  {_panel(382, True)}
</svg>"""


def svg_pseudo_r_s(uid: str = "pseudors") -> str:
    """12. svt-pseudo-r-s-diagram (wide_2_1, Page 2015 §2.3.2)."""
    # Left Half = V1 Lead (Sinus rS vs SVT rSr' pseudo-r'); Right Half = Inferior Lead II/aVF (Sinus qR vs SVT qRs pseudo-s)
    hl_v1 = rect_hatch_lines(264, 114, 34, 42, spacing=6.0, angle_deg=-45.0, stroke_width=1.2)
    hl_inf = rect_hatch_lines(612, 134, 34, 40, spacing=6.0, angle_deg=-45.0, stroke_width=1.2)
    return f"""<svg class="ep-svg ep-svg--banner" viewBox="0 0 740 205" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="窦律与快律对照识别V1假性r'与下壁假性s波示意图">
  <rect x="0" y="0" width="740" height="205" fill="#ffffff"/>

  <!-- Left Half: V1 Lead Comparison -->
  <rect x="8" y="8" width="352" height="189" rx="7" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="1.5"/>
  <text x="20" y="28" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:14px;font-weight:800;">V1 导联对照：QRS 末段多出小向上波</text>

  <text x="24" y="66" fill="#4d4d4d" class="ep-svg-label ep-muted-fill" style="font-size:12px;font-weight:700;">窦律</text>
  <text x="24" y="148" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:12px;font-weight:800;">快律</text>

  <!-- V1 Sinus: clean rS -->
  <path d="M 64 64 L 112 64 C 120 64, 126 52, 134 52 C 142 52, 148 64, 156 64 L 222 64 L 230 48 L 244 96 L 254 64 L 336 64"
        fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.3" stroke-linejoin="round"/>
  {label_box(276, 54, "末段平坦", width=62, height=16, font_size=11.5, role="muted")}

  <!-- V1 SVT: rSr' (pseudo-r' at x=268..286!) -->
  <rect x="264" y="114" width="34" height="42" rx="4" fill="#ffffff" class="ep-hl-area ep-accent-stroke" stroke="#000000" stroke-width="1.2" stroke-dasharray="3,2"/>
  {hl_v1}
  <path d="M 64 146 L 222 146 L 230 130 L 244 176 L 256 146 L 268 146 L 276 124 L 286 146 L 336 146"
        fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.3" stroke-linejoin="round"/>
  <path d="M 268 146 L 276 124 L 286 146" fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="3.2" stroke-linejoin="round"/>
  {label_box(282, 182, "假性 r′ (实为逆行 P)", width=116, height=16, font_size=12, font_weight=800, role="accent")}

  <!-- Right Half: Inferior Lead (II / aVF) Comparison -->
  <rect x="380" y="8" width="352" height="189" rx="7" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="1.5"/>
  <text x="392" y="28" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:14px;font-weight:800;">下壁导联对照：QRS 末段多出小向下波</text>

  <text x="396" y="66" fill="#4d4d4d" class="ep-svg-label ep-muted-fill" style="font-size:12px;font-weight:700;">窦律</text>
  <text x="396" y="148" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:12px;font-weight:800;">快律</text>

  <!-- Inferior Sinus: clean R -->
  <path d="M 436 64 L 484 64 C 492 64, 498 50, 506 50 C 514 50, 520 64, 528 64 L 584 64 L 598 28 L 610 64 L 708 64"
        fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.3" stroke-linejoin="round"/>
  {label_box(644, 54, "末段无 s 波", width=70, height=16, font_size=11.5, role="muted")}

  <!-- Inferior SVT: Rs (pseudo-s at x=614..636!) -->
  <rect x="612" y="134" width="34" height="40" rx="4" fill="#ffffff" class="ep-hl-area ep-accent-stroke" stroke="#000000" stroke-width="1.2" stroke-dasharray="3,2"/>
  {hl_inf}
  <path d="M 436 146 L 584 146 L 598 110 L 610 146 L 616 146 L 626 168 L 636 146 L 708 146"
        fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.3" stroke-linejoin="round"/>
  <path d="M 616 146 L 626 168 L 636 146" fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="3.2" stroke-linejoin="round"/>
  {label_box(634, 188, "假性 s (下壁逆行 P)", width=116, height=16, font_size=12, font_weight=800, role="accent")}
</svg>"""


BUILDERS = {
    "mechanisms-reentry-diagram": svg_reentry,
    "mechanisms-ah-jump-diagram": svg_ah_jump,
    "mechanisms-excitable-gap-diagram": svg_excitable_gap,
    "svt-typical-avnrt-short-va-diagram": svg_typical_avnrt_short_va,
    "svt-rp-first-split-diagram": svg_rp_first_split,
    "svt-pseudo-r-s-diagram": svg_pseudo_r_s,
}
