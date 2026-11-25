"""SVG generators for Domains 7 & 8: Wide-QRS / VT & Ablation Safety (Cards 19-24)."""

from __future__ import annotations

from .primitives import (
    arrow_polygon,
    egm_biphasic,
    ellipse_hatch_lines,
    grid_lines,
    label_box,
    rect_hatch_lines,
    scale_bar,
)


def svg_precordial_r_to_s(uid: str = "r2s") -> str:
    """19. vt-precordial-r-to-s-diagram (wide_2_1, Brugada 1991 Fig. 6-7)."""
    # Scale: 1 ms = 1.2 px -> 100 ms = 120 px
    # Wide RS beat: R onset at x=230, slow downstroke to S nadir at x=382 (RS interval = 152 px = 127 ms > 100 ms!)
    g = grid_lines(110, 710, 60, 22, 184)
    rs_hatch = rect_hatch_lines(230, 128, 152, 26, spacing=7.0, angle_deg=-45.0, stroke_width=1.2)
    return f"""<svg class="ep-svg ep-svg--banner" viewBox="0 0 740 205" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="胸导联R起点到S谷超过100 ms支持VT测量图">
  <rect x="0" y="0" width="740" height="205" fill="#ffffff"/>
  {g}

  <text x="16" y="78" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:14px;font-weight:800;">胸导联 (V1–V6)</text>
  <text x="16" y="96" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:11.5px;font-weight:600;">取最长 RS 导联</text>

  <!-- Wide QRS with slow downstroke from R onset (230) to S nadir (382) -->
  <path d="M 120 84 L 230 84 L 258 26 L 284 44 L 382 124 L 418 84 L 474 84 C 498 84, 518 64, 544 64 C 570 64, 588 84, 616 84 L 710 84"
        fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.8" stroke-linejoin="round" stroke-linecap="round"/>

  <!-- R onset & S nadir vertical cursors -->
  <line x1="230" y1="22" x2="230" y2="162" class="ep-ink-stroke" stroke="#000000" stroke-width="1.8" stroke-dasharray="5,3"/>
  <line x1="382" y1="22" x2="382" y2="162" class="ep-accent-stroke" stroke="#000000" stroke-width="2.2"/>
  <circle cx="230" cy="84" r="4.5" class="ep-ink-fill" fill="#000000"/>
  <circle cx="382" cy="124" r="5" class="ep-accent-fill" fill="#000000"/>

  <!-- Measurement Band -->
  <rect x="230" y="128" width="152" height="26" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.3"/>
  {rs_hatch}
  <line x1="236" y1="141" x2="376" y2="141" class="ep-ink-stroke" stroke="#000000" stroke-width="1.4"/>
  {arrow_polygon(233, 141, 180.0, 6.5, 3.2)}
  {arrow_polygon(379, 141, 0.0, 6.5, 3.2)}
  {label_box(306, 146, "RS > 100 ms", width=82, height=17, font_size=12.5, font_weight=800)}

  {label_box(224, 17, "R 起点", width=54, height=16, anchor="end", font_size=13)}
  {label_box(390, 17, "S 谷 (最深点)", width=94, height=16, anchor="start", font_size=13, font_weight=800, role="accent")}
  {label_box(306, 174, "本例示意 RS ≈ 127 ms（支持 VT）", width=188, height=16, font_size=12, role="accent")}
  {scale_bar(570, 690, 191, "100 ms", "同比例毫秒标尺")}
</svg>"""


def svg_av_dissociation(uid: str = "avdiss") -> str:
    """20. vt-av-dissociation-diagram (ultrawide_3_1, ESC 2019 §9.2.1.1)."""
    # Fast regular wide-QRS VT beats at x=120, 224, 328, 432, 536, 640 (period = 104px)
    # Slower independent sinus P waves at x=176, 342, 508, 674 (period = 166px) -> marching through QRS/ST!
    g = grid_lines(110, 710, 60, 22, 182)
    vt_beats = []
    for bx in (120, 224, 328, 432, 536, 640):
        vt_beats.append(
            f"L {bx} 112 L {bx + 14} 58 L {bx + 28} 68 L {bx + 42} 142 L {bx + 54} 112 "
            f"C {bx + 62} 112, {bx + 68} 122, {bx + 76} 122 C {bx + 84} 122, {bx + 90} 112, {bx + 98} 112"
        )
    ecg_d = "M 92 112 " + " ".join(vt_beats) + " L 724 112"

    # Independent P markers (arrows & highlights at top atrial rhythm track y=32)
    p_marks = []
    for i, px in enumerate((176, 342, 508, 674)):
        is_hidden = i == 1  # x=342 falls right inside Beat 3's QRS!
        if is_hidden:
            p_marks.append(
                f'<line x1="{px}" y1="36" x2="{px}" y2="152" class="ep-accent-stroke" stroke="#000000" stroke-width="1.6" stroke-dasharray="3,3"/>'
                + arrow_polygon(px, 50, 90.0, 7.5, 3.6, css_class="ep-accent-fill")
            )
        else:
            p_marks.append(
                f'<path d="M {px - 10} 112 C {px - 6} 112, {px - 3} 94, {px} 94 C {px + 3} 94, {px + 6} 112, {px + 10} 112" '
                f'fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="3.0"/>'
                f'<line x1="{px}" y1="36" x2="{px}" y2="88" class="ep-accent-stroke" stroke="#000000" stroke-width="1.6" stroke-dasharray="3,3"/>'
                + arrow_polygon(px, 90, 90.0, 7.5, 3.6, css_class="ep-accent-fill")
            )
    p_strip = "".join(p_marks)
    p_caliper = (
        '<line x1="176" y1="26" x2="342" y2="26" class="ep-accent-stroke" stroke="#000000" stroke-width="1.8"/>'
        '<line x1="342" y1="26" x2="508" y2="26" class="ep-accent-stroke" stroke="#000000" stroke-width="1.8"/>'
        '<line x1="508" y1="26" x2="674" y2="26" class="ep-accent-stroke" stroke="#000000" stroke-width="1.8"/>'
        + "".join(f'<circle cx="{px}" cy="26" r="4" class="ep-accent-fill" fill="#000000"/>' for px in (176, 342, 508, 674))
    )
    return f"""<svg class="ep-svg ep-svg--banner" viewBox="0 0 740 205" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="室速房室分离：较慢独立P波与较快宽QRS各自规律">
  <rect x="0" y="0" width="740" height="205" fill="#ffffff"/>
  {g}

  <text x="14" y="30" fill="#000000" class="ep-svg-label ep-accent-fill" style="font-size:12.5px;font-weight:800;">心房节拍 (较慢)</text>
  <text x="14" y="116" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:13px;font-weight:800;">宽 QRS (VT)</text>

  {p_caliper}
  <path d="{ecg_d}" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.3" stroke-linejoin="round"/>
  {p_strip}

  {label_box(176, 17, "独立 P 波", width=66, height=15, font_size=11.5, font_weight=800, role="accent")}
  {label_box(342, 17, "预计 P 波 (埋入 QRS)", width=124, height=15, font_size=11.5, role="muted")}
  {label_box(508, 17, "独立 P 波", width=66, height=15, font_size=11.5, font_weight=800, role="accent")}
  {label_box(674, 17, "独立 P 波", width=66, height=15, font_size=11.5, font_weight=800, role="accent")}

  <line x1="120" y1="158" x2="224" y2="158" class="ep-ink-stroke" stroke="#000000" stroke-width="1.6"/>
  {arrow_polygon(120, 158, 180.0, 5.5, 2.8)}
  {arrow_polygon(224, 158, 0.0, 5.5, 2.8)}
  {label_box(172, 174, "室速规律 RR", width=80, height=15, font_size=11.5)}

  {scale_bar(560, 680, 191, "600 ms", "P-P 独立慢于 R-R（互不夺获）")}
</svg>"""


def svg_capture_and_fusion(uid: str = "capfus") -> str:
    """21. vt-capture-and-fusion-diagram (compare_two, Issa 3e Ch.21 Fig. 21.5)."""
    def _panel(x0: int, is_fusion: bool) -> str:
        title = "融合搏 (两股波前共激)" if is_fusion else "完全夺获搏 (窦搏独激)"
        sub = "形态介于窦律与室速间" if is_fusion else "形态接近窦律窄 QRS"
        # Reference strip at top (y=46..92): Sinus ref (left) + VT ref (right)
        # Main strip at bottom (y=114..186): VT beat 1 -> Sinus P + Capture/Fusion beat (highlighted!) -> VT beat 3
        hl_x, hl_w = 148, 66
        hl_hatch = rect_hatch_lines(hl_x, 114, hl_w, 66, spacing=6.5, angle_deg=-45.0, stroke_width=1.2)
        if not is_fusion:
            # Complete capture: P wave at x=142 -> sharp narrow sinus QRS at x=166..182
            mid_qrs = "L 164 152 L 168 158 L 174 118 L 180 159 L 184 152 L 210 152"
            wave_desc = "纯窦性下传 (1 股波前)"
        else:
            # Fusion beat: P wave at x=148 -> intermediate hybrid QRS (initial slurred VT + sharper mid/late sinus fusion)
            mid_qrs = "L 158 152 L 168 128 L 178 134 L 188 168 L 198 152 L 210 152"
            wave_desc = "窦性 + 室速同时激动 (2 股波前)"

        main_strip = (
            "M 20 152 L 54 152 L 64 122 L 76 126 L 88 172 L 98 152 "
            "L 124 152 C 130 152, 134 140, 141 140 C 148 140, 152 152, 158 152 "
            f"{mid_qrs} "
            "L 252 152 L 262 122 L 274 126 L 286 172 L 296 152 L 336 152"
        )
        return f"""  <g transform="translate({x0}, 0)">
    <rect x="6" y="6" width="346" height="203" rx="8" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="1.6"/>
    <text x="20" y="27" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:14px;font-weight:800;">{title}</text>
    <text x="338" y="27" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:11px;font-weight:600;text-anchor:end;">{sub}</text>

    <!-- Top Reference Strip: Sinus Ref vs VT Ref -->
    <text x="18" y="64" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:11px;font-weight:700;">窦律参照</text>
    <path d="M 68 62 L 88 62 C 92 62, 95 54, 100 54 C 105 54, 108 62, 112 62 L 122 62 L 125 67 L 130 40 L 135 68 L 139 62 L 160 62"
          fill="none" class="ep-muted-stroke" stroke="#555555" stroke-width="1.8" stroke-linejoin="round"/>
    <text x="186" y="64" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:11px;font-weight:700;">室速参照</text>
    <path d="M 238 62 L 254 62 L 264 38 L 276 42 L 288 78 L 298 62 L 332 62"
          fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="1.9" stroke-linejoin="round"/>

    <line x1="18" y1="88" x2="340" y2="88" class="ep-muted-stroke" stroke="#555555" stroke-width="1" stroke-dasharray="2,3"/>

    <!-- Target Beat Window -->
    <rect x="{hl_x}" y="114" width="{hl_w}" height="66" rx="4" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.2" stroke-dasharray="3,2"/>
    {hl_hatch}
    <path d="{main_strip}" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.2" stroke-linejoin="round"/>

    <!-- P wave accent & expected VT tick -->
    <path d="M 124 152 C 130 152, 134 140, 141 140 C 148 140, 152 152, 158 152" fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="2.8"/>
    <line x1="141" y1="98" x2="141" y2="136" class="ep-accent-stroke" stroke="#000000" stroke-width="1.6"/>
    {arrow_polygon(141, 138, 90.0, 6.5, 3.2, css_class="ep-accent-fill")}

    {label_box(58, 188, "室速波前", width=54, height=15, font_size=11, role="muted")}
    {label_box(138, 104, "窦性下传 P", width=66, height=15, font_size=11, font_weight=800, role="accent")}
    {label_box(218, 194, wave_desc, width=168, height=15, font_size=11.5, font_weight=800)}
  </g>"""

    return f"""<svg class="ep-svg ep-svg--compare" viewBox="0 0 740 215" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="室速中完全夺获搏与融合搏形态对比图">
  <rect x="0" y="0" width="740" height="215" fill="#ffffff"/>
  {_panel(0, False)}
  <line x1="370" y1="14" x2="370" y2="201" class="ep-muted-stroke" stroke="#555555" stroke-width="1.4" stroke-dasharray="4,4"/>
  {_panel(382, True)}
</svg>"""


def svg_junctional_rhythm(uid: str = "junc") -> str:
    """22. ablation-junctional-rhythm-diagram (wide_2_1, Issa 3e Ch.17 Fig. 17.26)."""
    g = grid_lines(110, 710, 60, 22, 184)
    # RF delivery window x=290..690 -> baseline sinus (left, A before V) transitions to accelerated junctional beats (QRS narrow, A closely follows/coincides with V, 1:1 VA preserved!)
    rf_hatch = rect_hatch_lines(290, 22, 408, 22, spacing=8.0, angle_deg=-45.0, stroke_width=1.2)
    return f"""<svg class="ep-svg ep-svg--banner" viewBox="0 0 740 205" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="慢径射频消融时出现交界性心律示意图">
  <rect x="0" y="0" width="740" height="205" fill="#ffffff"/>
  {g}

  <!-- RF Delivery Band at top -->
  <rect x="290" y="22" width="408" height="22" rx="4" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.3"/>
  {rf_hatch}
  {label_box(494, 37, "射频放电时段 (持续监测 1:1 室房逆传)", width=232, height=16, font_size=12, font_weight=800)}

  <text x="16" y="84" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:13.5px;font-weight:700;">体表 QRS</text>
  <text x="16" y="152" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:13.5px;font-weight:700;">房电图 (A)</text>

  <!-- Surface ECG: Sinus beats at x=140, 250 -> Accelerated Junctional beats (faster, narrow QRS) at x=340, 424, 508, 592, 676 -->
  <path d="M 100 82 L 116 82 C 122 82, 126 70, 134 70 C 142 70, 146 82, 152 82 L 166 82 L 171 89 L 178 52 L 185 90 L 190 82 L 222 82 C 228 82, 232 70, 240 70 C 248 70, 252 82, 258 82 L 272 82 L 277 89 L 284 52 L 291 90 L 296 82 L 336 82 L 341 89 L 348 52 L 355 90 L 360 82 L 420 82 L 425 89 L 432 52 L 439 90 L 444 82 L 504 82 L 509 89 L 516 52 L 523 90 L 528 82 L 588 82 L 593 89 L 600 52 L 607 90 L 612 82 L 672 82 L 677 89 L 684 52 L 691 90 L 696 82 L 716 82"
        fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.3" stroke-linejoin="round"/>

  <!-- Atrial EGM: Sinus A precedes QRS (124, 230) -> Junctional beats have 1:1 retrograde A right after V (362, 446, 530, 614, 698) -->
  <path d="M 100 150 L 122 150 {egm_biphasic(122, 150, 20, 20)} L 228 150 {egm_biphasic(228, 150, 20, 20)} L 360 150 {egm_biphasic(360, 150, 18, 19)} L 444 150 {egm_biphasic(444, 150, 18, 19)} L 528 150 {egm_biphasic(528, 150, 18, 19)} L 612 150 {egm_biphasic(612, 150, 18, 19)} L 696 150 L 716 150"
        fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.1" stroke-linejoin="round"/>

  <!-- Accent lines linking Junctional V -> 1:1 Retrograde A -->
  <line x1="290" y1="48" x2="290" y2="174" class="ep-accent-stroke" stroke="#000000" stroke-width="2.0" stroke-dasharray="5,3"/>
  <line x1="348" y1="92" x2="366" y2="128" class="ep-accent-stroke" stroke="#000000" stroke-width="1.8"/>
  <line x1="432" y1="92" x2="450" y2="128" class="ep-accent-stroke" stroke="#000000" stroke-width="1.8"/>
  <line x1="516" y1="92" x2="534" y2="128" class="ep-accent-stroke" stroke="#000000" stroke-width="1.8"/>

  {label_box(188, 184, "窦律 (A 先于 V)", width=96, height=16, font_size=12, role="muted")}
  {label_box(436, 184, "交界搏起搏点主导：保持 1:1 室房逆传", width=224, height=16, font_size=12, font_weight=800, role="accent")}
  {scale_bar(592, 672, 191, "500 ms", "")}
</svg>"""


def svg_avoid_conduction_axis(uid: str = "ablsafe") -> str:
    """23. ablation-avoid-conduction-axis-diagram (square_1_1, ESC 2019 §11.2.1.2.2 & Cabrera Fig. 3B)."""
    safe_hatch = ellipse_hatch_lines(196, 232, 34, 20, spacing=6.5, rot_deg=-10.0, stroke_width=1.4)
    return f"""<svg class="ep-svg ep-svg--square" viewBox="0 0 360 350" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Koch三角安全慢径靶区与房室阻滞高危区分布图">
  <rect x="0" y="0" width="360" height="350" fill="#ffffff"/>

  <!-- Subtle Right Atrial Endocardial Context -->
  <path d="M 22 252 C 18 168, 56 88, 146 42 C 208 12, 282 14, 336 42" fill="none" class="ep-muted-stroke" stroke="#555555" stroke-width="1.3" stroke-dasharray="3,3"/>
  <path d="M 22 252 C 38 302, 86 328, 174 328 C 242 328, 294 318, 326 308" fill="none" class="ep-muted-stroke" stroke="#555555" stroke-width="1.3" stroke-dasharray="3,3"/>

  <!-- Koch Triangle Landmarks (Septal Leaflet Hinge + Tendon of Todaro + CS Ostium) -->
  <path d="M 286 292 C 268 236, 266 164, 268 94" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="3.0" stroke-linecap="round"/>
  <path d="M 60 256 C 118 206, 194 142, 263 92" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.6" stroke-dasharray="7,4" stroke-linecap="round"/>

  <!-- CS Ostium at base -->
  <g transform="translate(116, 262) rotate(-14)">
    <ellipse cx="0" cy="0" rx="28" ry="18" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="2.6"/>
  </g>

  <!-- SAFE INFERIOR TARGET ZONE (Yellow / Hatch) near base between CS ostium & septal leaflet -->
  <ellipse cx="196" cy="232" rx="34" ry="20" transform="rotate(-10 196 232)"
           fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="2.0"/>
  {safe_hatch}

  <!-- HIGH-RISK AVOIDANCE ZONES (Red / Double-dashed danger markers) -->
  <!-- 1. Apex / His recording zone -->
  <circle cx="256" cy="112" r="22" fill="#ffffff" class="ep-accent-stroke" stroke="#000000" stroke-width="2.4" stroke-dasharray="5,3"/>
  <line x1="244" y1="100" x2="268" y2="124" class="ep-accent-stroke" stroke="#000000" stroke-width="2.0"/>
  <line x1="268" y1="100" x2="244" y2="124" class="ep-accent-stroke" stroke="#000000" stroke-width="2.0"/>

  <!-- 2. Mid-septum risk zone -->
  <circle cx="222" cy="166" r="16" fill="#ffffff" class="ep-accent-stroke" stroke="#000000" stroke-width="2.2" stroke-dasharray="4,3"/>
  <line x1="213" y1="157" x2="231" y2="175" class="ep-accent-stroke" stroke="#000000" stroke-width="1.8"/>
  <line x1="231" y1="157" x2="213" y2="175" class="ep-accent-stroke" stroke="#000000" stroke-width="1.8"/>

  <!-- 3. CS Roof (superior rim of CS) -->
  <path d="M 92 238 C 108 228, 128 228, 144 238" fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="3.2" stroke-dasharray="4,3"/>

  <!-- Labels (6 schema labels) -->
  {label_box(58, 26, "避让房室传导轴", width=98, height=21, font_size=12, role="muted", border=True)}

  <line x1="268" y1="90" x2="294" y2="56" class="ep-ink-stroke" stroke="#000000" stroke-width="1.3"/>
  {label_box(296, 50, "三角尖", width=50, height=18, font_size=13.5)}

  <line x1="236" y1="104" x2="172" y2="76" class="ep-accent-stroke" stroke="#000000" stroke-width="1.3"/>
  {label_box(134, 72, "His 记录区 (高危)", width=106, height=18, font_size=12.5, font_weight=800, role="accent")}

  <line x1="206" y1="162" x2="148" y2="136" class="ep-accent-stroke" stroke="#000000" stroke-width="1.3"/>
  {label_box(106, 132, "中间隔 (慎融)", width=94, height=18, font_size=12.5, role="accent")}

  <line x1="116" y1="232" x2="72" y2="196" class="ep-accent-stroke" stroke="#000000" stroke-width="1.3"/>
  {label_box(64, 190, "CS 顶部 (避让)", width=92, height=18, font_size=12.5, role="accent")}

  <line x1="112" y1="282" x2="88" y2="314" class="ep-ink-stroke" stroke="#000000" stroke-width="1.3"/>
  {label_box(84, 330, "CS 口", width=52, height=18, font_size=13.5)}

  <line x1="204" y1="252" x2="216" y2="296" class="ep-ink-stroke" stroke="#000000" stroke-width="1.3"/>
  {label_box(224, 314, "常用安全靶区 (偏下)", width=124, height=22, font_size=12.5, highlight_bg=True)}
</svg>"""


def svg_test_noninducibility(uid: str = "nonind") -> str:
    """24. ablation-test-noninducibility-diagram (compare_two, Katritsis 2019 & Issa 3e Ch.17)."""
    def _panel(x0: int, is_post: bool) -> str:
        title = "术后复测：不再诱发" if is_post else "术前诱发：持续折返"
        sub = "最多单个回波即终止" if is_post else "程序刺激引出持续 SVT"
        hl_hatch = rect_hatch_lines(144, 52, 186, 118, spacing=8.0, angle_deg=-45.0, stroke_width=1.2)
        if not is_post:
            # S1 S1 S2 (x=46, 86, 118) -> Sustained rapid narrow QRS SVT beats (154, 194, 234, 274, 314)
            ecg = (
                "M 20 120 L 42 120 L 46 82 L 50 120 L 82 120 L 86 82 L 90 120 L 114 120 L 118 82 L 122 120 "
                "L 150 120 L 154 76 L 159 124 L 163 120 "
                "L 190 120 L 194 76 L 199 124 L 203 120 "
                "L 230 120 L 234 76 L 239 124 L 243 120 "
                "L 270 120 L 274 76 L 279 124 L 283 120 "
                "L 310 120 L 314 76 L 319 124 L 323 120 L 338 120"
            )
            hl_overlay = '<path d="M 150 120 L 154 76 L 159 124 L 163 120 L 190 120 L 194 76 L 199 124 L 203 120 L 230 120 L 234 76 L 239 124 L 243 120 L 270 120 L 274 76 L 279 124 L 283 120 L 310 120 L 314 76 L 319 124 L 323 120" fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="2.6" stroke-linejoin="round"/>'
            win_lbl = "持续折返 (SVT 维持)"
            win_role = "accent"
        else:
            # S1 S1 S2 (x=46, 86, 118) -> Single echo beat (154) then clean flat sinus return (240, 310)
            ecg = (
                "M 20 120 L 42 120 L 46 82 L 50 120 L 82 120 L 86 82 L 90 120 L 114 120 L 118 82 L 122 120 "
                "L 150 120 L 154 80 L 159 124 L 164 120 "
                "L 228 120 C 234 120, 238 110, 244 110 C 250 110, 254 120, 260 120 L 274 120 L 278 82 L 282 120 L 338 120"
            )
            hl_overlay = ""
            win_lbl = "仅 1 个回波后终止 (急性成功)"
            win_role = "primary"

        return f"""  <g transform="translate({x0}, 0)">
    <rect x="6" y="6" width="346" height="203" rx="8" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="1.6"/>
    <text x="20" y="27" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:14px;font-weight:800;">{title}</text>
    <text x="338" y="27" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:11px;font-weight:600;text-anchor:end;">{sub}</text>

    <!-- Programmed Stimulation pacing spikes -->
    <line x1="46" y1="54" x2="46" y2="152" class="ep-muted-stroke" stroke="#555555" stroke-width="1.2" stroke-dasharray="3,3"/>
    <line x1="86" y1="54" x2="86" y2="152" class="ep-muted-stroke" stroke="#555555" stroke-width="1.2" stroke-dasharray="3,3"/>
    <line x1="118" y1="54" x2="118" y2="152" class="ep-ink-stroke" stroke="#000000" stroke-width="1.6" stroke-dasharray="4,2"/>
    {label_box(82, 166, "程序刺激 (S1-S2)", width=96, height=15, font_size=11)}

    <!-- Observation Window -->
    <rect x="144" y="52" width="186" height="118" rx="4" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.2" stroke-dasharray="3,2"/>
    {hl_hatch}
    <path d="{ecg}" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.3" stroke-linejoin="round"/>
    {hl_overlay}

    {label_box(237, 69, "观察窗", width=54, height=18, font_size=11.5, role="muted", border=True)}
    {label_box(237, 194, win_lbl, width=164, height=16, font_size=11.5, font_weight=800, role=win_role)}
  </g>"""

    return f"""<svg class="ep-svg ep-svg--compare" viewBox="0 0 740 215" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="消融前后程序刺激诱发对比：持续折返与不可诱发">
  <rect x="0" y="0" width="740" height="215" fill="#ffffff"/>
  {_panel(0, False)}
  <line x1="370" y1="14" x2="370" y2="201" class="ep-muted-stroke" stroke="#555555" stroke-width="1.4" stroke-dasharray="4,4"/>
  {_panel(382, True)}
</svg>"""


BUILDERS = {
    "vt-precordial-r-to-s-diagram": svg_precordial_r_to_s,
    "vt-av-dissociation-diagram": svg_av_dissociation,
    "vt-capture-and-fusion-diagram": svg_capture_and_fusion,
    "ablation-junctional-rhythm-diagram": svg_junctional_rhythm,
    "ablation-avoid-conduction-axis-diagram": svg_avoid_conduction_axis,
    "ablation-test-noninducibility-diagram": svg_test_noninducibility,
}
