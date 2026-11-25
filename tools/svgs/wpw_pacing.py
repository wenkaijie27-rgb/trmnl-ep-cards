"""SVG generators for Domains 5 & 6: WPW Pre-excitation & Pacing Maneuvers (Cards 13-18)."""

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


def svg_delta_fusion(uid: str = "delta") -> str:
    """13. wpw-delta-fusion-diagram (wide_2_1, Page 2015 Table 2)."""
    delta_hatch = rect_hatch_lines(296, 134, 72, 46, spacing=6.0, angle_deg=-45.0, stroke_width=1.2)
    return f"""<svg class="ep-svg ep-svg--banner" viewBox="0 0 740 205" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="旁路提前除极与希浦下传融合形成delta波示意图">
  <rect x="0" y="0" width="740" height="205" fill="#ffffff"/>

  <!-- Left Half: Dual-Pathway Anatomical Ladder (Atrium -> AP vs AVN-His -> Ventricle Fusion) -->
  <rect x="8" y="8" width="356" height="189" rx="7" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="1.5"/>
  <text x="20" y="28" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:13.5px;font-weight:800;">双径路激动时序：旁路先到 + 希浦合流</text>

  <!-- Chambers -->
  <rect x="34" y="40" width="304" height="26" rx="8" fill="#ffffff" class="ep-muted-stroke" stroke="#555555" stroke-width="1.3"/>
  <text x="48" y="57" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:12px;font-weight:700;">心房</text>

  <!-- Annulus -->
  <line x1="30" y1="78" x2="108" y2="78" class="ep-ink-stroke" stroke="#000000" stroke-width="2.2"/>
  <line x1="146" y1="78" x2="246" y2="78" class="ep-ink-stroke" stroke="#000000" stroke-width="2.2"/>
  <line x1="282" y1="78" x2="342" y2="78" class="ep-ink-stroke" stroke="#000000" stroke-width="2.2"/>

  <!-- Ventricle Box -->
  <rect x="34" y="90" width="304" height="92" rx="10" fill="#ffffff" class="ep-muted-stroke" stroke="#555555" stroke-width="1.3"/>

  <!-- Normal Axis (AVN delay -> fast His-Purkinje) -->
  <ellipse cx="127" cy="78" rx="14" ry="8" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="2"/>
  <line x1="127" y1="54" x2="127" y2="142" class="ep-ink-stroke" stroke="#000000" stroke-width="2.8"/>
  {arrow_polygon(127, 148, 90.0, 9.0, 4.2)}
  <path d="M 127 148 L 178 164" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.4"/>
  {arrow_polygon(184, 165, 16.0, 8.0, 3.8)}
  {label_box(76, 128, "房室结—希浦", width=76, height=16, font_size=11.5)}

  <!-- Accessory Pathway (No AVN delay -> early local myocardial creep) -->
  <line x1="264" y1="54" x2="264" y2="118" class="ep-accent-stroke" stroke="#000000" stroke-width="3.0" stroke-dasharray="6,3.5"/>
  {arrow_polygon(264, 124, 90.0, 9.0, 4.2, css_class="ep-accent-fill")}
  <!-- Early slow spread into local myocardium -->
  <ellipse cx="238" cy="146" rx="44" ry="20" fill="#ffffff" class="ep-hl-area ep-accent-stroke" stroke="#000000" stroke-width="1.4" stroke-dasharray="3,2"/>
  {ellipse_hatch_lines(238, 146, 44, 20, spacing=6.5, rot_deg=0.0, stroke_width=1.2)}
  <path d="M 254 132 L 204 160" fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="2.2" stroke-dasharray="5,3"/>
  {arrow_polygon(198, 163, 150.0, 8.0, 3.8, css_class="ep-accent-fill")}
  {label_box(296, 108, "旁路", width=36, height=16, font_size=12, role="accent")}
  {label_box(246, 174, "局部室肌预激", width=84, height=16, font_size=11.5, role="accent")}
  {label_box(192, 134, "融合", width=38, height=16, font_size=12, font_weight=800, border=True)}

  <!-- Right Half: Resulting Surface ECG Fusion Beat -->
  <rect x="376" y="8" width="356" height="189" rx="7" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="1.5"/>
  <text x="388" y="28" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:13.5px;font-weight:800;">体表投影：PR 缩短 + 粗钝 delta 波</text>

  <!-- Normal reference beat (dashed muted) -->
  <path d="M 396 154 L 444 154 C 454 154, 462 136, 476 136 C 490 136, 498 154, 508 154 L 552 154 L 558 162 L 568 74 L 578 164 L 584 154 L 714 154"
        fill="none" class="ep-muted-stroke" stroke="#555555" stroke-width="1.4" stroke-dasharray="4,3"/>

  <!-- Delta wave highlight box on right panel: x=508..564 -->
  <rect x="508" y="114" width="56" height="48" rx="4" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.2" stroke-dasharray="3,2"/>
  {rect_hatch_lines(508, 114, 56, 48, spacing=6.5, angle_deg=-45.0, stroke_width=1.1)}

  <!-- Pre-excited ECG (short PR -> slurred delta upstroke from x=508 to x=558 -> rapid His-Purkinje peak) -->
  <path d="M 396 154 L 444 154 C 454 154, 462 136, 476 136 C 490 136, 498 154, 508 154"
        fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/>
  <path d="M 508 154 L 558 122" fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="3.6" stroke-linecap="round"/>
  <path d="M 558 122 L 568 74 L 582 162 L 592 154 L 630 154 C 648 154, 662 168, 680 168 C 698 168, 708 154, 718 154"
        fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.5" stroke-linejoin="round"/>

  {label_box(476, 126, "P 波", width=34, height=15, font_size=11.5, role="muted")}
  {label_box(526, 98, "delta 波 (旁路早激)", width=114, height=17, font_size=12, font_weight=800, role="accent")}
  {label_box(634, 88, "希浦合流后快速主波", width=118, height=16, font_size=11.5)}
  {scale_bar(564, 672, 184, "100 ms", "短 PR + 起始粗钝")}
</svg>"""


def _avrt_panel(x0: int, mode: str) -> str:
    """Shared panel helper for wpw-avrt-directions (ortho vs anti)."""
    is_ortho = mode == "ortho"
    title = "顺向型 AVRT" if is_ortho else "逆向型 AVRT"
    sub = "经房室结—希浦下行" if is_ortho else "经旁路下行 · 逆传房室结"

    if is_ortho:
        avn_arrow = arrow_polygon(118, 106, 90.0, 9.0, 4.4)
        ap_arrow = arrow_polygon(256, 46, -90.0, 9.0, 4.4, css_class="ep-accent-fill")
        top_loop = '<path d="M 244 38 Q 186 24 134 37" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2"/>' + arrow_polygon(128, 38, 166.0, 8.5, 4.0)
        bot_loop = '<path d="M 134 114 Q 190 128 240 114" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2"/>' + arrow_polygon(246, 112, -16.0, 8.5, 4.0)
        hl_cx, hl_cy, hl_rx, hl_ry = 118, 108, 34, 15
        qrs_path = "M 24 176 L 86 176 C 92 176, 96 164, 104 164 C 112 164, 116 176, 122 176 L 146 176 L 151 182 L 158 144 L 165 184 L 170 176 L 200 176 C 214 176, 226 165, 240 165 C 254 165, 266 176, 280 176 L 326 176"
        qrs_badge, qrs_w_x1, qrs_w_x2, qrs_tag = "窄 QRS（经希浦同步）", 146, 170, "窄"
    else:
        avn_arrow = arrow_polygon(118, 46, -90.0, 9.0, 4.4)
        ap_arrow = arrow_polygon(256, 106, 90.0, 9.0, 4.4, css_class="ep-accent-fill")
        top_loop = '<path d="M 128 38 Q 186 24 238 37" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2"/>' + arrow_polygon(244, 38, 14.0, 8.5, 4.0)
        bot_loop = '<path d="M 246 112 Q 190 128 140 115" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2"/>' + arrow_polygon(134, 114, -166.0, 8.5, 4.0)
        hl_cx, hl_cy, hl_rx, hl_ry = 256, 108, 34, 15
        qrs_path = "M 24 176 L 86 176 C 92 176, 96 164, 104 164 C 112 164, 116 176, 122 176 L 132 176 C 142 172, 152 161, 162 145 L 176 154 L 194 185 L 204 176 L 220 176 C 236 176, 246 187, 260 187 C 274 187, 284 176, 298 176 L 326 176"
        qrs_badge, qrs_w_x1, qrs_w_x2, qrs_tag = "宽 QRS · 完全预激", 132, 204, "宽"

    exit_hatch = ellipse_hatch_lines(hl_cx, hl_cy, hl_rx, hl_ry, spacing=7.0, rot_deg=0.0, stroke_width=1.2)
    return f"""  <g transform="translate({x0}, 0)">
    <rect x="6" y="6" width="346" height="203" rx="8" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="1.6"/>
    <text x="20" y="27" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:14.5px;font-weight:800;">{title}</text>
    <text x="338" y="27" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:11.5px;font-weight:600;text-anchor:end;">{sub}</text>
    <rect x="40" y="36" width="278" height="28" rx="10" fill="#ffffff" class="ep-muted-stroke" stroke="#555555" stroke-width="1.3"/>
    <text x="52" y="54" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:11.5px;font-weight:700;">心房</text>
    <line x1="36" y1="74" x2="98" y2="74" class="ep-ink-stroke" stroke="#000000" stroke-width="2.4"/>
    <line x1="138" y1="74" x2="238" y2="74" class="ep-ink-stroke" stroke="#000000" stroke-width="2.4"/>
    <line x1="274" y1="74" x2="322" y2="74" class="ep-ink-stroke" stroke="#000000" stroke-width="2.4"/>
    <rect x="40" y="84" width="278" height="48" rx="12" fill="#ffffff" class="ep-muted-stroke" stroke="#555555" stroke-width="1.3"/>
    <text x="52" y="112" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:11.5px;font-weight:700;">心室</text>
    <ellipse cx="{hl_cx}" cy="{hl_cy}" rx="{hl_rx}" ry="{hl_ry}" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.2" stroke-dasharray="3,2"/>
    {exit_hatch}
    <ellipse cx="118" cy="74" rx="14" ry="8" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="2"/>
    <line x1="118" y1="50" x2="118" y2="100" class="ep-ink-stroke" stroke="#000000" stroke-width="2.8"/>
    {avn_arrow}
    {label_box(178, 96, "房室结—希浦", width=76, height=15, font_size=11.5)}
    <line x1="256" y1="50" x2="256" y2="100" class="ep-accent-stroke" stroke="#000000" stroke-width="3.0" stroke-dasharray="6,3.5"/>
    {ap_arrow}
    {label_box(290, 96, "旁路", width=28, height=15, font_size=12, font_weight=800, role="accent")}
    {top_loop}
    {bot_loop}
    <line x1="18" y1="138" x2="340" y2="138" class="ep-muted-stroke" stroke="#555555" stroke-width="1" stroke-dasharray="2,3"/>
    <line x1="{qrs_w_x1}" y1="145" x2="{qrs_w_x1}" y2="190" class="ep-muted-stroke" stroke="#555555" stroke-width="1" stroke-dasharray="2,2"/>
    <line x1="{qrs_w_x2}" y1="145" x2="{qrs_w_x2}" y2="190" class="ep-muted-stroke" stroke="#555555" stroke-width="1" stroke-dasharray="2,2"/>
    <line x1="{qrs_w_x1}" y1="191" x2="{qrs_w_x2}" y2="191" class="ep-accent-stroke" stroke="#000000" stroke-width="2"/>
    <path d="{qrs_path}" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.3" stroke-linejoin="round"/>
    <text x="22" y="201" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:12.5px;font-weight:700;">{qrs_badge}</text>
    <text x="336" y="201" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:11px;font-weight:600;text-anchor:end;">QRS宽度: {qrs_tag}（同时间尺）</text>
  </g>"""


def svg_avrt_directions(uid: str = "avrt") -> str:
    """14. wpw-avrt-directions-diagram (compare_two)."""
    return f"""<svg class="ep-svg ep-svg--compare" viewBox="0 0 740 215" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="顺向型与逆向型AVRT回路与QRS宽窄对照图">
  <rect x="0" y="0" width="740" height="215" fill="#ffffff"/>
  {_avrt_panel(0, "ortho")}
  <line x1="370" y1="14" x2="370" y2="201" class="ep-muted-stroke" stroke="#555555" stroke-width="1.4" stroke-dasharray="4,4"/>
  {_avrt_panel(382, "anti")}
</svg>"""


def svg_manifest_concealed(uid: str = "mancap") -> str:
    """15. wpw-manifest-concealed-diagram (compare_two, Page 2015 Table 2 & §6)."""
    def _panel(x0: int, concealed: bool) -> str:
        title = "隐匿旁路 (仅逆传)" if concealed else "显性旁路 (能前传)"
        sub = "窦律无 delta 波" if concealed else "窦律可见预激"
        if not concealed:
            # Antegrade arrow down AP + bidir note; Sinus ECG has delta wave
            ap_arrows = arrow_polygon(256, 102, 90.0, 9.0, 4.4, css_class="ep-accent-fill") + arrow_polygon(256, 52, -90.0, 7.0, 3.4, css_class="ep-muted-fill")
            ap_tag = "能前传 (双向多见)"
            hl_box = '<rect x="132" y="146" width="52" height="36" rx="4" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.2" stroke-dasharray="3,2"/>' + rect_hatch_lines(132, 146, 52, 36, 6.0, -45.0, 1.1)
            ecg = "M 30 176 L 80 176 C 88 176, 94 162, 104 162 C 114 162, 120 176, 128 176 L 134 176 L 160 152 L 166 142 L 174 182 L 182 176 L 210 176 C 226 176, 238 186, 254 186 C 270 186, 282 176, 298 176 L 326 176"
            delta_hl = '<path d="M 134 176 L 160 152" fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="3.2" stroke-linecap="round"/>'
            foot = "窦律可见预激 (WPW 表现)"
        else:
            # Retrograde-only arrow UP AP; Sinus ECG is completely normal narrow QRS
            ap_arrows = arrow_polygon(256, 48, -90.0, 9.5, 4.5, css_class="ep-accent-fill")
            ap_tag = "仅逆传 (前传阻滞)"
            hl_box = ""
            ecg = "M 30 176 L 80 176 C 88 176, 94 162, 104 162 C 114 162, 120 176, 128 176 L 154 176 L 159 182 L 166 142 L 173 184 L 178 176 L 210 176 C 226 176, 238 164, 254 164 C 270 164, 282 176, 298 176 L 326 176"
            delta_hl = ""
            foot = "窦律体表正常，仍可顺向折返"

        return f"""  <g transform="translate({x0}, 0)">
    <rect x="6" y="6" width="346" height="203" rx="8" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="1.6"/>
    <text x="20" y="27" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:14.5px;font-weight:800;">{title}</text>
    <text x="338" y="27" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:11.5px;font-weight:600;text-anchor:end;">{sub}</text>

    <rect x="38" y="38" width="280" height="26" rx="9" fill="#ffffff" class="ep-muted-stroke" stroke="#555555" stroke-width="1.3"/>
    <text x="50" y="55" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:11.5px;font-weight:700;">心房</text>
    <line x1="34" y1="74" x2="96" y2="74" class="ep-ink-stroke" stroke="#000000" stroke-width="2.4"/>
    <line x1="136" y1="74" x2="236" y2="74" class="ep-ink-stroke" stroke="#000000" stroke-width="2.4"/>
    <line x1="274" y1="74" x2="322" y2="74" class="ep-ink-stroke" stroke="#000000" stroke-width="2.4"/>
    <rect x="38" y="84" width="280" height="44" rx="10" fill="#ffffff" class="ep-muted-stroke" stroke="#555555" stroke-width="1.3"/>
    <text x="50" y="110" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:11.5px;font-weight:700;">心室</text>

    <!-- Normal system -->
    <ellipse cx="116" cy="74" rx="14" ry="8" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="2"/>
    <line x1="116" y1="50" x2="116" y2="100" class="ep-ink-stroke" stroke="#000000" stroke-width="2.8"/>
    {arrow_polygon(116, 105, 90.0, 8.5, 4.2)}
    {label_box(164, 98, "正常系统", width=56, height=15, font_size=11.5)}

    <!-- Accessory pathway -->
    <line x1="256" y1="52" x2="256" y2="98" class="ep-accent-stroke" stroke="#000000" stroke-width="3.0" stroke-dasharray="6,3.5"/>
    {ap_arrows}
    {label_box(256, 121, ap_tag, width=96, height=15, font_size=11.5, font_weight=800, role="accent")}

    <line x1="18" y1="136" x2="340" y2="136" class="ep-muted-stroke" stroke="#555555" stroke-width="1" stroke-dasharray="2,3"/>
    {hl_box}
    <path d="{ecg}" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.2" stroke-linejoin="round"/>
    {delta_hl}
    <text x="180" y="200" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:12px;font-weight:700;text-anchor:middle;">{foot}</text>
  </g>"""

    return f"""<svg class="ep-svg ep-svg--compare" viewBox="0 0 740 215" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="显性旁路与隐匿旁路传导方向及窦律表现对照图">
  <rect x="0" y="0" width="740" height="215" fill="#ffffff"/>
  {_panel(0, False)}
  <line x1="370" y1="14" x2="370" y2="201" class="ep-muted-stroke" stroke="#555555" stroke-width="1.4" stroke-dasharray="4,4"/>
  {_panel(382, True)}
</svg>"""


def svg_his_refractory_pvc(uid: str = "hisspvc") -> str:
    """16. pacing-his-refractory-pvc-diagram (wide_2_1, Miles 1986)."""
    g = grid_lines(110, 710, 60, 22, 186)
    # Ladder / event tiers: Atrium (y=46), His (y=110), Ventricle (y=170)
    # Tachycardia beats: Beat 1 (A=140, H=165, V=195 -> retrograde A=230), Beat 2 (H=370 -> His-refractory PVC at V=382! -> Expected A=435 vs Actual advanced A*=408!)
    ref_hatch = rect_hatch_lines(348, 86, 56, 48, spacing=6.0, angle_deg=-45.0, stroke_width=1.2)
    return f"""<svg class="ep-svg ep-svg--banner" viewBox="0 0 740 205" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="His不应期室早提前激动心房提示逆传旁路示意图">
  <rect x="0" y="0" width="740" height="205" fill="#ffffff"/>
  {g}

  <!-- 3 Ladder Tracks -->
  <text x="16" y="48" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:13.5px;font-weight:700;">心房 (A)</text>
  <line x1="90" y1="44" x2="718" y2="44" class="ep-muted-stroke" stroke="#555555" stroke-width="1.3"/>

  <text x="16" y="114" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:13.5px;font-weight:700;">His (H)</text>
  <line x1="90" y1="110" x2="718" y2="110" class="ep-muted-stroke" stroke="#555555" stroke-width="1.3"/>

  <text x="16" y="176" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:13.5px;font-weight:700;">心室 (V)</text>
  <line x1="90" y1="172" x2="718" y2="172" class="ep-muted-stroke" stroke="#555555" stroke-width="1.3"/>

  <!-- Beat 1 (Baseline SVT cycle) -->
  <line x1="150" y1="44" x2="172" y2="110" class="ep-ink-stroke" stroke="#000000" stroke-width="2.4"/>
  <line x1="172" y1="110" x2="192" y2="172" class="ep-ink-stroke" stroke="#000000" stroke-width="2.4"/>
  <line x1="192" y1="172" x2="232" y2="44" class="ep-ink-stroke" stroke="#000000" stroke-width="2.2" stroke-dasharray="5,3"/>
  <circle cx="150" cy="44" r="5" class="ep-ink-fill" fill="#000000"/>
  <circle cx="172" cy="110" r="5" class="ep-ink-fill" fill="#000000"/>
  <circle cx="192" cy="172" r="5" class="ep-ink-fill" fill="#000000"/>
  <circle cx="232" cy="44" r="5" class="ep-ink-fill" fill="#000000"/>

  <!-- Beat 2 leading into His-refractory window -->
  <line x1="232" y1="44" x2="368" y2="110" class="ep-ink-stroke" stroke="#000000" stroke-width="2.4"/>
  <line x1="368" y1="110" x2="388" y2="172" class="ep-ink-stroke" stroke="#000000" stroke-width="2.4"/>
  <circle cx="368" cy="110" r="5.5" class="ep-ink-fill" fill="#000000"/>

  <!-- His Refractory Window Highlight Box -->
  <rect x="348" y="86" width="56" height="48" rx="5" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.3" stroke-dasharray="3,2"/>
  {ref_hatch}
  {label_box(376, 148, "His 不应窗", width=78, height=18, font_size=11.5, font_weight=800, border=True)}

  <!-- His-synchronous PVC injected at x=376 (inside His refractory window!) -->
  <polygon points="376,172 370,192 382,192" class="ep-accent-fill" fill="#000000"/>
  {label_box(376, 200, "His 同步室早 (PVC)", width=118, height=15, font_size=12, font_weight=800, role="accent")}

  <!-- Blocked retrograde path through His (cannot go back through refractory His) -->
  <line x1="376" y1="168" x2="376" y2="128" class="ep-muted-stroke" stroke="#555555" stroke-width="1.8" stroke-dasharray="3,3"/>
  <line x1="368" y1="128" x2="384" y2="128" class="ep-ink-stroke" stroke="#000000" stroke-width="2.5"/>

  <!-- Retrograde Accessory Pathway bypasses His -> advances next Atrial beat A*! -->
  <line x1="376" y1="170" x2="432" y2="50" class="ep-accent-stroke" stroke="#000000" stroke-width="3.2" stroke-dasharray="7,3.5"/>
  {arrow_polygon(435, 45, -66.0, 9.0, 4.4, css_class="ep-accent-fill")}
  <circle cx="436" cy="44" r="5.5" class="ep-accent-fill" fill="#000000"/>

  <!-- Expected Atrial Timing Ghost (x=492) -->
  <line x1="492" y1="28" x2="492" y2="70" class="ep-muted-stroke" stroke="#555555" stroke-width="1.5" stroke-dasharray="3,3"/>
  <circle cx="492" cy="44" r="5" fill="#ffffff" class="ep-muted-stroke" stroke="#555555" stroke-width="1.8" stroke-dasharray="2,2"/>

  <!-- Advancement bracket -->
  <line x1="442" y1="28" x2="486" y2="28" class="ep-accent-stroke" stroke="#000000" stroke-width="2"/>
  {arrow_polygon(440, 28, 180.0, 6.0, 3.0, css_class="ep-accent-fill")}

  <!-- Subsequent resumed beat -->
  <line x1="436" y1="44" x2="572" y2="110" class="ep-ink-stroke" stroke="#000000" stroke-width="2.2"/>
  <line x1="572" y1="110" x2="594" y2="172" class="ep-ink-stroke" stroke="#000000" stroke-width="2.2"/>
  <circle cx="572" cy="110" r="4.5" class="ep-ink-fill" fill="#000000"/>
  <circle cx="594" cy="172" r="4.5" class="ep-ink-fill" fill="#000000"/>

  {label_box(426, 18, "提前房波 (A*)", width=88, height=16, anchor="end", font_size=12, font_weight=800, role="accent")}
  {label_box(498, 18, "预计房波位置", width=86, height=16, anchor="start", font_size=12, role="muted")}
  {label_box(454, 98, "经旁路绕过 His 逆传", width=116, height=16, anchor="start", font_size=11.5, role="accent")}
</svg>"""


def svg_postventricular_sequence(uid: str = "pvseq") -> str:
    """17. pacing-postventricular-sequence-diagram (compare_two, Knight 1999 & Ho 2013)."""
    def _panel(x0: int, is_at: bool) -> str:
        title = "V-A-A-V (室房房室)" if is_at else "V-A-V (室房室)"
        sub = "停起搏后常提示房速 (AT)" if is_at else "提示 AVNRT / AVRT"
        # Last paced V at x=76 -> last entrained A at x=126
        # If V-A-V: next beat returns to V (x=216) -> A (x=264)
        # If V-A-A-V: atrial tachycardia fires own return A' (x=206) BEFORE next V (x=256)!
        hl_x, hl_w = (176, 66) if is_at else (196, 48)
        hl_hatch = rect_hatch_lines(hl_x, 38, hl_w, 134, spacing=6.5, angle_deg=-45.0, stroke_width=1.2)

        if not is_at:
            a_trace = f"M 24 64 L 122 64 {egm_biphasic(122, 64, 22, 20)} L 260 64 {egm_biphasic(260, 64, 22, 20)} L 336 64"
            v_trace = f"M 24 146 L 72 146 {egm_biphasic(72, 146, 24, 24)} L 212 146 {egm_biphasic(212, 146, 24, 24)} L 336 146"
            links = (
                '<line x1="84" y1="138" x2="128" y2="74" class="ep-ink-stroke" stroke="#000000" stroke-width="2.0"/>'
                + arrow_polygon(130, 70, -56.0, 7.5, 3.6)
                + '<line x1="136" y1="72" x2="216" y2="138" class="ep-ink-stroke" stroke="#000000" stroke-width="2.0"/>'
                + arrow_polygon(220, 142, 40.0, 7.5, 3.6)
            )
            ret_labels = (
                label_box(84, 184, "末次室起搏 V", width=80, height=15, font_size=11)
                + label_box(133, 38, "末个受驱房波 A", width=94, height=15, font_size=11)
                + label_box(224, 184, "返回室波 V", width=68, height=15, font_size=11.5, font_weight=800, role="accent")
                + label_box(274, 38, "A", width=20, height=15, font_size=11.5)
            )
        else:
            a_trace = f"M 24 64 L 122 64 {egm_biphasic(122, 64, 22, 20)} L 198 64 {egm_biphasic(198, 64, 22, 22)} L 336 64"
            v_trace = f"M 24 146 L 72 146 {egm_biphasic(72, 146, 24, 24)} L 254 146 {egm_biphasic(254, 146, 24, 24)} L 336 146"
            links = (
                '<line x1="84" y1="138" x2="128" y2="74" class="ep-ink-stroke" stroke="#000000" stroke-width="2.0"/>'
                + arrow_polygon(130, 70, -56.0, 7.5, 3.6)
                + '<line x1="210" y1="74" x2="258" y2="138" class="ep-accent-stroke" stroke="#000000" stroke-width="2.2" stroke-dasharray="5,3"/>'
                + arrow_polygon(262, 142, 52.0, 7.5, 3.6, css_class="ep-accent-fill")
            )
            ret_labels = (
                label_box(84, 184, "末次室起搏 V", width=80, height=15, font_size=11)
                + label_box(112, 38, "末个受驱 A", width=72, height=15, font_size=11)
                + label_box(226, 38, "房速回归房波 A*", width=102, height=15, font_size=11.5, font_weight=800, role="accent")
                + label_box(268, 184, "下传 V", width=48, height=15, font_size=11.5)
            )

        return f"""  <g transform="translate({x0}, 0)">
    <rect x="6" y="6" width="346" height="203" rx="8" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="1.6"/>
    <text x="20" y="27" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:14.5px;font-weight:800;">{title}</text>
    <text x="338" y="27" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:11.5px;font-weight:600;text-anchor:end;">{sub}</text>

    <rect x="{hl_x}" y="38" width="{hl_w}" height="134" rx="4" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.1" stroke-dasharray="3,2"/>
    {hl_hatch}

    <text x="14" y="68" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:11.5px;font-weight:700;">心房</text>
    <text x="14" y="150" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:11.5px;font-weight:700;">心室</text>

    <path d="{a_trace}" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.1" stroke-linejoin="round"/>
    <path d="{v_trace}" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.1" stroke-linejoin="round"/>
    {links}
    {ret_labels}
  </g>"""

    return f"""<svg class="ep-svg ep-svg--compare" viewBox="0 0 740 215" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="停止心室超速起搏后V-A-V与V-A-A-V序列对照图">
  <rect x="0" y="0" width="740" height="215" fill="#ffffff"/>
  {_panel(0, False)}
  <line x1="370" y1="14" x2="370" y2="201" class="ep-muted-stroke" stroke="#555555" stroke-width="1.4" stroke-dasharray="4,4"/>
  {_panel(382, True)}
</svg>"""


def svg_para_hisian(uid: str = "parahis") -> str:
    """18. pacing-para-hisian-diagram (compare_two, Hirao 1996 Fig. 1 & 5)."""
    # Left Panel = Nodal Retrograde (His+V capture narrow QRS -> short S-A vs V-only capture wide QRS -> S-A lengthens!)
    # Right Panel = Accessory Pathway Retrograde (narrow vs wide QRS -> S-A stays unchanged!)
    def _panel(x0: int, is_ap: bool) -> str:
        title = "旁路型逆传 (S-A 不变)" if is_ap else "结型逆传 (S-A 明显延长)"
        sub = "失去 His 捕获仍经旁路" if is_ap else "失去 His 捕获须先绕室肌"
        # Top beat: High output (His+V capture) -> narrow QRS, Stim at x=90, A at x=162 (SA=72px)
        # Bottom beat: Low output (V-only capture) -> wide QRS, Stim at x=90, A at x=162 (AP) vs x=228 (Nodal!)
        sa2_x = 162 if is_ap else 232
        sa_note = "到房时距近似不变" if is_ap else "到房时距明显拉长"
        hl_w = sa2_x - 90
        hl1 = rect_hatch_lines(90, 56, 72, 22, 6.0, -45.0, 1.1)
        hl2 = rect_hatch_lines(90, 134, hl_w, 22, 6.0, -45.0, 1.1)

        return f"""  <g transform="translate({x0}, 0)">
    <rect x="6" y="6" width="346" height="203" rx="8" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="1.6"/>
    <text x="20" y="27" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:14px;font-weight:800;">{title}</text>
    <text x="338" y="27" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:11px;font-weight:600;text-anchor:end;">{sub}</text>

    <!-- Stim vertical reference at x=90 -->
    <line x1="90" y1="42" x2="90" y2="180" class="ep-ink-stroke" stroke="#000000" stroke-width="1.8" stroke-dasharray="4,3"/>
    <text x="90" y="194" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:11.5px;font-weight:700;text-anchor:middle;">刺激 S</text>

    <!-- Row 1: His + V Capture (Narrow QRS) -->
    <text x="16" y="62" fill="#4d4d4d" class="ep-svg-label ep-muted-fill" style="font-size:11px;font-weight:700;">夺获 His</text>
    <text x="16" y="75" fill="#4d4d4d" class="ep-svg-label ep-muted-fill" style="font-size:10.5px;font-weight:600;">窄 QRS</text>
    <rect x="90" y="56" width="72" height="22" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.1"/>
    {hl1}
    <path d="M 70 86 L 90 86 L 90 52 L 92 86 L 104 86 L 108 92 L 114 62 L 120 93 L 125 86 L 160 86 {egm_biphasic(160, 86, 20, 18)} L 328 86"
          fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.1" stroke-linejoin="round"/>
    <text x="170" y="52" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:11.5px;font-weight:700;">A</text>

    <line x1="16" y1="112" x2="338" y2="112" class="ep-muted-stroke" stroke="#555555" stroke-width="1" stroke-dasharray="2,3"/>

    <!-- Row 2: V-only Capture (Wide QRS) -->
    <text x="16" y="140" fill="#000000" class="ep-svg-label ep-accent-fill" style="font-size:11px;font-weight:800;">仅局部室</text>
    <text x="16" y="153" fill="#000000" class="ep-svg-label ep-accent-fill" style="font-size:10.5px;font-weight:700;">宽 QRS</text>
    <rect x="90" y="134" width="{hl_w}" height="22" fill="#ffffff" class="ep-hl-area ep-accent-stroke" stroke="#000000" stroke-width="1.2"/>
    {hl2}
    <path d="M 70 166 L 90 166 L 90 130 L 92 166 L 106 166 C 114 166, 122 138, 130 138 C 138 138, 146 176, 156 176 L 164 166 L {sa2_x} 166 {egm_biphasic(sa2_x, 166, 20, 18)} L 328 166"
          fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.1" stroke-linejoin="round"/>
    <line x1="{sa2_x}" y1="130" x2="{sa2_x}" y2="180" class="ep-accent-stroke" stroke="#000000" stroke-width="2.0"/>
    {label_box(sa2_x + 12, 130, f"A ({sa_note})", width=106, height=15, anchor="start" if not is_ap else "middle", font_size=11, font_weight=800, role="accent")}
  </g>"""

    return f"""<svg class="ep-svg ep-svg--compare" viewBox="0 0 740 215" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="旁His起搏窄宽QRS对比刺激至房波时距图">
  <rect x="0" y="0" width="740" height="215" fill="#ffffff"/>
  {_panel(0, False)}
  <line x1="370" y1="14" x2="370" y2="201" class="ep-muted-stroke" stroke="#555555" stroke-width="1.4" stroke-dasharray="4,4"/>
  {_panel(382, True)}
</svg>"""


BUILDERS = {
    "wpw-delta-fusion-diagram": svg_delta_fusion,
    "wpw-avrt-directions-diagram": svg_avrt_directions,
    "wpw-manifest-concealed-diagram": svg_manifest_concealed,
    "pacing-his-refractory-pvc-diagram": svg_his_refractory_pvc,
    "pacing-postventricular-sequence-diagram": svg_postventricular_sequence,
    "pacing-para-hisian-diagram": svg_para_hisian,
}
