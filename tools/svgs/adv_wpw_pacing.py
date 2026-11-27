"""SVG generators for Advanced Domains 5 & 6: WPW Risk & Entrainment/Para-Hisian Pacing (Cards 13-18)."""

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


def svg_mahaim_insertions(uid: str = "mahaim") -> str:
    """Adv 13. wpw-mahaim-insertions-diagram (portrait_4_5, McClelland 1994 & ESC 2019 §11.3.9)."""
    dist_hatch = ellipse_hatch_lines(116, 256, 26, 15, spacing=5.5, rot_deg=-15.0, stroke_width=1.3)
    return f"""<svg class="ep-svg ep-svg--portrait" viewBox="0 0 340 370" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="常见右侧房束支Mahaim旁路连接右房游离壁至远端右束支示意图">
  <rect x="0" y="0" width="340" height="370" fill="#ffffff"/>

  <!-- Right Heart Chambers Silhouette (RA above tricuspid annulus, RV below; Septum on right) -->
  <path d="M 62 152 C 52 94, 88 52, 162 46 C 232 42, 286 76, 294 146" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.2" stroke-linecap="round"/>
  <path d="M 62 152 C 48 214, 68 294, 152 326 C 218 338, 282 292, 294 146" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.2" stroke-linecap="round"/>

  <!-- Tricuspid Annulus horizontal band (separating RA and RV) -->
  <path d="M 62 152 C 118 164, 174 166, 224 152" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.6" stroke-dasharray="6,4"/>
  <!-- Septal border -->
  <path d="M 224 152 C 216 206, 206 258, 172 316" fill="none" class="ep-muted-stroke" stroke="#555555" stroke-width="1.6"/>

  <!-- Normal AV Node + His + RBB -->
  <ellipse cx="222" cy="128" rx="18" ry="11" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="2.2"/>
  <path d="M 222 139 C 214 162, 198 186, 176 214 C 154 242, 134 252, 116 256" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.8" stroke-linecap="round"/>
  {arrow_polygon(182, 206, 130.0, 7.5, 3.5)}

  <!-- Highlighted Distal Right Bundle Insertion Site -->
  <ellipse cx="116" cy="256" rx="26" ry="15" transform="rotate(-15 116 256)" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.4"/>
  {dist_hatch}

  <!-- Typical Atriofascicular Mahaim Pathway (RA free wall -> lateral annulus -> distal RBB, decremental anterograde) -->
  <path d="M 94 108 C 76 146, 78 202, 102 248" fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="3.6" stroke-dasharray="8,4" stroke-linecap="round"/>
  {arrow_polygon(104, 250, 62.0, 9.5, 4.4, css_class="ep-accent-fill")}

  <!-- Labels -->
  {label_box(58, 26, "右心游离壁至室间隔观", width=134, height=19, font_size=11.5, role="muted", border=True)}
  {label_box(164, 80, "右房 (RA)", width=64, height=18, font_size=13)}
  {label_box(254, 118, "房室结", width=52, height=18, font_size=12)}
  {label_box(156, 154, "三尖瓣环", width=62, height=17, font_size=12)}
  {label_box(246, 206, "正常希浦", width=62, height=17, font_size=11.5, role="muted")}
  <line x1="216" y1="204" x2="188" y2="202" class="ep-muted-stroke" stroke="#555555" stroke-width="1.1"/>

  {label_box(156, 196, "常见房束支旁路", width=104, height=19, font_size=12, font_weight=800, role="accent")}
  {label_box(156, 214, "(前传慢 · 有递减性)", width=112, height=15, font_size=10.5, role="accent")}

  {label_box(122, 286, "远端右束支", width=84, height=19, font_size=12.5, highlight_bg=True)}
  <line x1="120" y1="274" x2="118" y2="268" class="ep-ink-stroke" stroke="#000000" stroke-width="1.2"/>
  {label_box(228, 286, "室肌", width=42, height=17, font_size=12)}
  {label_box(170, 346, "结-束支 / 结室等其他端点见文字说明", width=224, height=16, font_size=11, role="muted")}
</svg>"""


def svg_intermittent_delta(uid: str = "interm") -> str:
    """Adv 14. wpw-intermittent-delta-diagram (compare_two, ESC 2019 §11.3.11)."""
    def _panel(x0: int, is_gradual: bool) -> str:
        title = "逐搏变浅 (融合占比改变)" if is_gradual else "突然消失 (真正间歇/突断)"
        sub = "可因结下传比例改变，勿误判" if is_gradual else "delta 完全消失 + PR 相应延长"
        if not is_gradual:
            # Beat 1 (48..96) short PR + strong delta; Beat 2 (138..186) short PR + strong delta;
            # Beat 3 (228..304) LONG PR + clean narrow QRS (NO delta!)
            strip = (
                "M 20 124 L 38 124 C 44 124, 48 112, 54 112 C 60 112, 64 124, 68 124 L 84 96 L 90 66 L 96 130 L 102 124 "
                "L 124 124 C 130 124, 134 112, 140 112 C 146 112, 150 124, 154 124 L 170 96 L 176 66 L 182 130 L 188 124 "
                "L 210 124 C 216 124, 220 112, 226 112 C 232 112, 236 124, 240 124 L 270 124 L 274 130 L 280 66 L 286 132 L 292 124 L 336 124"
            )
            deltas = (
                '<path d="M 68 124 L 84 96" fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="3.6" stroke-linecap="round"/>'
                + '<path d="M 154 124 L 170 96" fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="3.6" stroke-linecap="round"/>'
            )
            hl = '<rect x="208" y="54" width="90" height="94" rx="4" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.2" stroke-dasharray="3,2"/>' + rect_hatch_lines(208, 54, 90, 94, 7.0, -45.0, 1.1)
            pr_marks = (
                '<line x1="50" y1="142" x2="68" y2="142" class="ep-ink-stroke" stroke="#000000" stroke-width="1.6"/>'
                + '<line x1="222" y1="142" x2="274" y2="142" class="ep-accent-stroke" stroke="#000000" stroke-width="2.0"/>'
                + label_box(59, 156, "短 PR", width=36, height=14, font_size=10.5)
                + label_box(248, 156, "PR 延长", width=48, height=14, font_size=10.5, font_weight=800, role="accent")
            )
            badge = label_box(253, 174, "转变搏：无 delta", width=96, height=15, font_size=11, font_weight=800)
            foot = "提示旁路可能传导不稳，但仍须排查其他指标"
        else:
            # Gradual fading: Beat 1 strong delta -> Beat 2 moderate delta -> Beat 3 subtle slurred delta (fusion!)
            strip = (
                "M 20 124 L 38 124 C 44 124, 48 112, 54 112 C 60 112, 64 124, 68 124 L 84 96 L 90 66 L 96 130 L 102 124 "
                "L 124 124 C 130 124, 134 112, 140 112 C 146 112, 150 124, 154 124 L 166 124 L 176 106 L 182 66 L 188 130 L 194 124 "
                "L 210 124 C 216 124, 220 112, 226 112 C 232 112, 236 124, 240 124 L 260 124 L 268 114 L 274 66 L 280 130 L 286 124 L 336 124"
            )
            deltas = (
                '<path d="M 68 124 L 84 96" fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="3.6" stroke-linecap="round"/>'
                + '<path d="M 166 124 L 176 106" fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="3.0" stroke-linecap="round"/>'
                + '<path d="M 260 124 L 268 114" fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="2.4" stroke-linecap="round"/>'
            )
            hl = '<rect x="122" y="54" width="174" height="94" rx="4" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.2" stroke-dasharray="3,2"/>' + rect_hatch_lines(122, 54, 174, 94, 8.0, -45.0, 1.0)
            pr_marks = (
                '<line x1="138" y1="142" x2="166" y2="142" class="ep-ink-stroke" stroke="#000000" stroke-width="1.5"/>'
                + '<line x1="224" y1="142" x2="260" y2="142" class="ep-ink-stroke" stroke="#000000" stroke-width="1.5"/>'
                + label_box(152, 156, "渐短", width=32, height=14, font_size=10.5, role="muted")
                + label_box(242, 156, "仍偏短", width=40, height=14, font_size=10.5, role="muted")
            )
            badge = label_box(209, 174, "残存微弱 delta 融合", width=118, height=15, font_size=11, role="accent")
            foot = "左游离壁旁路等常见结下传加速后预激难辨"

        return f"""  <g transform="translate({x0}, 0)">
    <rect x="6" y="6" width="346" height="203" rx="8" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="1.6"/>
    <text x="18" y="26" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:13.5px;font-weight:800;">{title}</text>
    <text x="338" y="26" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:10.5px;font-weight:600;text-anchor:end;">{sub}</text>
    {hl}
    <path d="{strip}" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.2" stroke-linejoin="round"/>
    {deltas}
    {pr_marks}
    {label_box(80, 56, "delta 波", width=52, height=14, font_size=11, font_weight=800, role="accent")}
    {badge}
    <text x="180" y="198" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:10.5px;font-weight:600;text-anchor:middle;">{foot}</text>
  </g>"""

    return f"""<svg class="ep-svg ep-svg--compare" viewBox="0 0 740 215" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="同导联同增益对比预激突然消失与逐搏融合变浅">
  <rect x="0" y="0" width="740" height="215" fill="#ffffff"/>
  {_panel(0, False)}
  <line x1="370" y1="14" x2="370" y2="201" class="ep-muted-stroke" stroke="#555555" stroke-width="1.4" stroke-dasharray="4,4"/>
  {_panel(382, True)}
</svg>"""


def svg_asymptomatic_ep_risk(uid: str = "wpwrisk") -> str:
    """Adv 15. wpw-asymptomatic-ep-risk-diagram (wide_2_1, ESC 2019 §11.3.11 Fig. 22 & AHA/ACC 2015)."""
    g = grid_lines(140, 710, 55, 16, 178)
    af_hatch = rect_hatch_lines(228, 30, 128, 52, spacing=6.5, angle_deg=-45.0, stroke_width=1.1)
    erp_hatch = rect_hatch_lines(348, 114, 92, 48, spacing=6.5, angle_deg=-45.0, stroke_width=1.1)
    return f"""<svg class="ep-svg ep-svg--banner" viewBox="0 0 740 205" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="无症状预激两把标尺：房颤最短预激间隔与程序刺激旁路前传ERP">
  <rect x="0" y="0" width="740" height="205" fill="#ffffff"/>
  {g}

  <!-- Strip 1: Atrial Fibrillation SPERRI (y=58) -->
  <text x="14" y="46" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:13px;font-weight:800;">1. 房颤最短预激间隔</text>
  <text x="14" y="61" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:10.5px;font-weight:600;">欧 ≤250 / 美 &lt;250 ms</text>
  <rect x="228" y="30" width="128" height="52" rx="4" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.2"/>
  {af_hatch}
  <!-- Irregular AF baseline: pre-excited beat (234), pre-excited beat (304), non-pre-excited narrow beat (460), pre-excited beat (580) -->
  <path d="M 148 64 L 160 62 L 168 66 L 178 63 L 188 66 L 234 64 L 248 42 L 256 26 L 266 76 L 274 64 L 284 62 L 292 66 L 304 64 L 318 42 L 326 26 L 336 76 L 344 64 C 362 60, 386 67, 404 64 L 460 64 L 464 69 L 470 30 L 476 70 L 482 64 L 516 62 L 542 66 L 580 64 L 594 42 L 602 26 L 612 76 L 620 64 L 708 64"
        fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.2" stroke-linejoin="round"/>
  <!-- Highlight adjacent pre-excited beats cursor (x=234 to x=304) -->
  <line x1="234" y1="16" x2="234" y2="86" class="ep-accent-stroke" stroke="#000000" stroke-width="2.0"/>
  <line x1="304" y1="16" x2="304" y2="86" class="ep-accent-stroke" stroke="#000000" stroke-width="2.0"/>
  <line x1="234" y1="22" x2="304" y2="22" class="ep-accent-stroke" stroke="#000000" stroke-width="2.0"/>
  {label_box(269, 16, "最短预激间隔 (相邻)", width=118, height=15, font_size=11, font_weight=800, role="accent")}
  {label_box(470, 20, "非预激 QRS (不跨测)", width=116, height=15, font_size=11, role="muted")}
  {label_box(602, 20, "预激 QRS", width=60, height=15, font_size=11)}

  <line x1="14" y1="96" x2="720" y2="96" class="ep-muted-stroke" stroke="#555555" stroke-width="1" stroke-dasharray="3,3"/>

  <!-- Strip 2: Programmed Atrial Stimulation for Antegrade AP ERP (y=146) -->
  <text x="14" y="132" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:13px;font-weight:800;">2. 旁路前传 ERP</text>
  <text x="14" y="147" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:10.5px;font-weight:600;">欧 ≤250 / 美 &lt;240 ms</text>
  <rect x="348" y="114" width="92" height="48" rx="4" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.2"/>
  {erp_hatch}
  <!-- S1 pre-excited beat at x=190 -> S2 paced beat at x=356 loses delta (narrow AVN QRS!) -->
  <path d="M 148 148 L 180 148 L 180 120 L 182 148 L 194 148 L 208 130 L 216 112 L 226 160 L 234 148 L 356 148 L 356 120 L 358 148 L 402 148 L 406 154 L 412 116 L 418 156 L 424 148 L 708 148"
        fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.2" stroke-linejoin="round"/>
  {label_box(182, 166, "S1 (仍预激)", width=64, height=14, font_size=10.5, role="muted")}
  {label_box(394, 166, "S2 后失去旁路前传", width=112, height=15, font_size=11, font_weight=800)}
  {label_box(556, 134, "经正常结下传窄 QRS", width=120, height=16, font_size=11, role="muted")}
  {scale_bar(556, 668, 192, "250 ms", "注意各指南比较符号与单位")}
</svg>"""


def svg_corrected_ppi_tcl(uid: str = "cppi") -> str:
    """Adv 16. pace-corrected-ppi-tcl-diagram (ultrawide_3_1, González-Torrecilla 2006 Fig. 2)."""
    g = grid_lines(110, 710, 55, 20, 178)
    # Left (baseline tachycardia): TCL=116px (representative 300ms), Baseline AH=40px (representative 80ms)
    # Right (RV Apex pacing stop): Last S at x=394 -> Last entrained HRA at x=478 -> Return His at x=538 (Return AH=60px, +ΔAH!) -> Return V at x=562 (PPI=168px -> 440ms!)
    ret_hatch = rect_hatch_lines(394, 24, 168, 136, spacing=8.0, angle_deg=-45.0, stroke_width=1.0)
    return f"""<svg class="ep-svg ep-svg--banner" viewBox="0 0 740 205" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="右室心尖拖带后PPI减TCL扣除首个回归周期AH增量示意图">
  <rect x="0" y="0" width="740" height="205" fill="#ffffff"/>
  {g}

  <text x="12" y="48" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:12.5px;font-weight:700;">高位右房 A</text>
  <text x="12" y="96" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:12.5px;font-weight:700;">His (H)</text>
  <text x="12" y="144" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:12.5px;font-weight:700;">右室心尖 V</text>

  <!-- Return Cycle Highlight Window (Last S at 394 to Return V at 562) -->
  <rect x="394" y="24" width="168" height="136" rx="4" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.2" stroke-dasharray="3,2"/>
  {ret_hatch}

  <!-- Baseline Tachycardia (left side, TCL 300 ms, Basal AH 80 ms) -->
  <!-- HRA A at 142, 258 -->
  <!-- His H at 178, 294 ; V at 204, 320 -->
  <line x1="142" y1="30" x2="142" y2="108" class="ep-muted-stroke" stroke="#555555" stroke-width="1.1" stroke-dasharray="2,3"/>
  <line x1="178" y1="80" x2="178" y2="114" class="ep-muted-stroke" stroke="#555555" stroke-width="1.1" stroke-dasharray="2,3"/>

  <!-- Pacing & Return Alignment Lines -->
  <line x1="394" y1="20" x2="394" y2="176" class="ep-ink-stroke" stroke="#000000" stroke-width="2.0" stroke-dasharray="4,2"/>
  <line x1="478" y1="30" x2="478" y2="112" class="ep-accent-stroke" stroke="#000000" stroke-width="2.0"/>
  <line x1="538" y1="74" x2="538" y2="112" class="ep-accent-stroke" stroke="#000000" stroke-width="2.0"/>
  <line x1="562" y1="24" x2="562" y2="176" class="ep-ink-stroke" stroke="#000000" stroke-width="2.0" stroke-dasharray="4,2"/>

  <!-- Track 1: HRA Atrial Signals -->
  <path d="M 96 46 L 140 46 {egm_biphasic(140, 46, 16, 16)} L 256 46 {egm_biphasic(256, 46, 16, 16)} L 330 46 L 350 46 {egm_biphasic(350, 46, 14, 15)} L 476 46 {egm_biphasic(476, 46, 16, 16)} L 634 46 {egm_biphasic(634, 46, 16, 16)} L 710 46"
        fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.0" stroke-linejoin="round"/>
  <!-- Track 2: His Channel -->
  <path d="M 96 94 L 176 94 {egm_biphasic(176, 94, 13, 18)} L 292 94 {egm_biphasic(292, 94, 13, 18)} L 536 94 {egm_biphasic(536, 94, 13, 18)} L 680 94 {egm_biphasic(680, 94, 13, 18)} L 710 94"
        fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.0" stroke-linejoin="round"/>
  <!-- Track 3: RV Apex Channel (Tachy V at 204, 320 -> Last Pace Spike at 394 -> Return V at 562) -->
  <path d="M 96 142 L 202 142 {egm_biphasic(202, 142, 18, 20)} L 318 142 {egm_biphasic(318, 142, 18, 20)} L 394 142 L 394 114 L 396 142 {egm_biphasic(402, 142, 16, 18)} L 560 142 {egm_biphasic(560, 142, 18, 21)} L 704 142"
        fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.1" stroke-linejoin="round"/>

  <!-- Calipers: Baseline TCL, Baseline AH, Return AH, PPI -->
  <line x1="204" y1="166" x2="320" y2="166" class="ep-ink-stroke" stroke="#000000" stroke-width="1.6"/>
  {label_box(262, 166, "发作 TCL 300", width=78, height=15, font_size=11)}
  <line x1="142" y1="112" x2="178" y2="112" class="ep-ink-stroke" stroke="#000000" stroke-width="1.6"/>
  {label_box(160, 124, "发作 AH 80", width=68, height=14, font_size=10.5)}

  <line x1="478" y1="108" x2="538" y2="108" class="ep-accent-stroke" stroke="#000000" stroke-width="2.2"/>
  {label_box(478, 122, "回归 AH 130 (增量 +50)", width=138, height=15, font_size=11, font_weight=800, role="accent")}

  <line x1="394" y1="166" x2="562" y2="166" class="ep-ink-stroke" stroke="#000000" stroke-width="2.0"/>
  {arrow_polygon(396, 166, 180.0, 5.5, 2.8)}
  {arrow_polygon(560, 166, 0.0, 5.5, 2.8)}
  {label_box(478, 166, "PPI 440", width=60, height=15, font_size=11.5, font_weight=800)}

  {label_box(394, 16, "末次刺激", width=56, height=14, font_size=11, font_weight=800)}
  {label_box(478, 22, "末次受拖带房波", width=96, height=14, font_size=11, font_weight=800, role="accent")}
  {label_box(544, 68, "回归 His", width=56, height=14, anchor="start", font_size=11, font_weight=800, role="accent")}
  {label_box(568, 134, "起搏点返室波", width=80, height=14, anchor="start", font_size=11)}
  {label_box(370, 192, "示例：校正 PPI−TCL = 440 − 300 − (130 − 80) = 90 ms (<110 ms)", width=390, height=16, font_size=11.5, font_weight=800, border=True)}
</svg>"""


def svg_base_minus_apex(uid: str = "baseminapex") -> str:
    """Adv 17. pace-base-minus-apex-diagram (compare_two, Segal 2009 & Issa 3e p.585)."""
    def _panel(x0: int, is_apex: bool) -> str:
        title = "右室心尖拖带 (cPPI−TCL 较短)" if is_apex else "右室基底拖带 (cPPI−TCL 较长)"
        sub = "经希浦较快进结区" if is_apex else "距结区折返常更远"
        hl_w = 112 if is_apex else 168
        hl_x = 114
        hl_hatch = rect_hatch_lines(hl_x, 96, hl_w, 28, spacing=6.0, angle_deg=-45.0, stroke_width=1.2)
        dot_y = 176 if is_apex else 148
        dot_x = 58 if is_apex else 48
        val = "校正差值 115 ms" if is_apex else "校正差值 175 ms"
        return f"""  <g transform="translate({x0}, 0)">
    <rect x="6" y="6" width="346" height="203" rx="8" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="1.6"/>
    <text x="18" y="26" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:13.5px;font-weight:800;">{title}</text>
    <text x="338" y="26" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:10.5px;font-weight:600;text-anchor:end;">{sub}</text>

    <!-- Equal-scale Pacing & Return Strip (Last S at x=76, Return V at x=76+134=210 or 76+204=280) -->
    <path d="M 24 68 L 76 68 L 76 40 L 78 68 {egm_biphasic(84, 68, 16, 18)} L {hl_x + hl_w} 68 {egm_biphasic(hl_x + hl_w, 68, 18, 20)} L 332 68"
          fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.1" stroke-linejoin="round"/>
    <line x1="76" y1="36" x2="76" y2="128" class="ep-ink-stroke" stroke="#000000" stroke-width="1.6" stroke-dasharray="4,2"/>
    <line x1="{hl_x + hl_w}" y1="48" x2="{hl_x + hl_w}" y2="128" class="ep-ink-stroke" stroke="#000000" stroke-width="1.6" stroke-dasharray="4,2"/>

    <!-- TCL Baseline portion (76..114) + Corrected cPPI-TCL portion (hl_x .. hl_x+hl_w) -->
    <rect x="76" y="96" width="38" height="28" fill="#ffffff" class="ep-muted-stroke" stroke="#555555" stroke-width="1.2"/>
    <text x="95" y="114" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:10.5px;font-weight:700;text-anchor:middle;">TCL</text>
    <rect x="{hl_x}" y="96" width="{hl_w}" height="28" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.3"/>
    {hl_hatch}
    {label_box(hl_x + hl_w / 2, 114, val, width=max(90, hl_w - 8), height=16, font_size=10.5, font_weight=800)}

    {label_box(76, 138, "末次刺激", width=52, height=14, font_size=10.5)}
    {label_box(hl_x + hl_w, 46, "各自回归室波", width=76, height=14, font_size=10.5)}

    <!-- Mini RV Anatomy Contour locating Base vs Apex pacing site -->
    <path d="M 32 142 C 56 138, 86 144, 88 164 C 82 180, 58 190, 46 184 C 34 174, 28 156, 32 142 Z" fill="#ffffff" class="ep-muted-stroke" stroke="#555555" stroke-width="1.3"/>
    <circle cx="{dot_x}" cy="{dot_y}" r="4.5" class="ep-accent-fill" fill="#000000"/>
    <text x="102" y="162" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:11px;font-weight:700;">{"定位：右室心尖 (分别扣 AH 增量)" if is_apex else "定位：右室基底 (分别扣 AH 增量)"}</text>
    <text x="210" y="192" fill="#000000" class="ep-svg-label ep-accent-fill" style="font-size:11.5px;font-weight:800;text-anchor:middle;">{"基底减心尖 = +60 ms (>30 ms 支持 AVNRT)" if is_apex else "两处须用相同或相近拖带周期"}</text>
  </g>"""

    return f"""<svg class="ep-svg ep-svg--compare" viewBox="0 0 740 215" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="右室基底与心尖分别行AH校正拖带及基底减心尖差值方向图">
  <rect x="0" y="0" width="740" height="215" fill="#ffffff"/>
  {_panel(0, False)}
  <line x1="370" y1="14" x2="370" y2="201" class="ep-muted-stroke" stroke="#555555" stroke-width="1.4" stroke-dasharray="4,4"/>
  {_panel(382, True)}
</svg>"""


def svg_para_his_masked(uid: str = "phmask") -> str:
    """Adv 18. pacing-para-his-masked-diagram (compare_two, Hirao 1996 & Jastrzebski 2018)."""
    def _panel(x0: int, is_capture_trap: bool) -> str:
        if not is_capture_trap:
            title = "失效 1：结逆传遮蔽旁路"
            sub = "远侧旁路晚于快结逆传"
            hatch = rect_hatch_lines(88, 60, 82, 54, 6.5, -45.0, 1.1)
            body = f"""    <rect x="88" y="60" width="82" height="54" rx="4" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.1"/>
    {hatch}
    <text x="16" y="72" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:11px;font-weight:700;">结逆传 (快)</text>
    <path d="M 86 74 L 166 74 {egm_biphasic(166, 74, 18, 17)} L 328 74" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.1"/>
    <text x="16" y="128" fill="#000000" class="ep-svg-label ep-accent-fill" style="font-size:11px;font-weight:800;">远侧旁路</text>
    <path d="M 86 128 L 228 128 {egm_biphasic(228, 128, 18, 17)} L 328 128" fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="2.2" stroke-dasharray="6,3"/>
    <text x="16" y="168" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:11px;font-weight:700;">局部室波</text>
    <path d="M 86 168 L 86 146 L 88 168 {egm_biphasic(92, 168, 16, 17)} L 328 168" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.0"/>
    <line x1="170" y1="50" x2="170" y2="146" class="ep-ink-stroke" stroke="#000000" stroke-width="1.6" stroke-dasharray="4,2"/>
    {label_box(170, 46, "结路径先到 → 遮蔽旁路", width=130, height=15, font_size=11, font_weight=800)}
    {label_box(236, 148, "存在但未先激动心房", width=124, height=15, font_size=10.5, role="accent")}
    <text x="180" y="198" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:11px;font-weight:700;text-anchor:middle;">结型反应只说明此次结逆传占优，未排除远侧旁路</text>"""
        else:
            title = "失效 2：束内捕获陷阱"
            sub = "同位室肌捕获并查 His"
            hatch = rect_hatch_lines(104, 52, 142, 102, 7.5, -45.0, 1.0)
            body = f"""    <rect x="104" y="52" width="142" height="102" rx="4" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.1"/>
    {hatch}
    <text x="14" y="72" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:10.5px;font-weight:700;">远侧束支捕获</text>
    <text x="14" y="86" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:10px;font-weight:600;">宽 QRS / 未提前</text>
    <path d="M 102 74 L 102 50 L 104 74 L 118 74 C 126 74, 134 54, 144 54 C 154 54, 162 86, 172 86 L 182 74 L 254 74 {egm_biphasic(254, 74, 18, 16)} L 330 74" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.1"/>

    <text x="14" y="138" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:10.5px;font-weight:700;">近端 His 捕获</text>
    <text x="14" y="152" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:10px;font-weight:600;">窄 QRS · 核实</text>
    <path d="M 102 142 L 102 118 L 104 142 L 118 142 L 124 118 L 130 148 L 136 142 L 198 142 {egm_biphasic(198, 142, 18, 16)} L 330 142" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.1"/>
    {label_box(178, 108, "核实捕获 + 查近端逆行 His", width=152, height=16, font_size=11, font_weight=800, border=True)}
    <text x="180" y="198" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:11px;font-weight:700;text-anchor:middle;">近端 RBBB 下宽窄变可因捕获位置切换，防误判</text>"""

        return f"""  <g transform="translate({x0}, 0)">
    <rect x="6" y="6" width="346" height="203" rx="8" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="1.6"/>
    <text x="18" y="26" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:13.5px;font-weight:800;">{title}</text>
    <text x="338" y="26" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:10.5px;font-weight:600;text-anchor:end;">{sub}</text>
    {body}
  </g>"""

    return f"""<svg class="ep-svg ep-svg--compare" viewBox="0 0 740 215" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="旁His起搏的两类判读陷阱：结逆传遮蔽与束内阻滞捕获变化">
  <rect x="0" y="0" width="740" height="215" fill="#ffffff"/>
  {_panel(0, False)}
  <line x1="370" y1="14" x2="370" y2="201" class="ep-muted-stroke" stroke="#555555" stroke-width="1.4" stroke-dasharray="4,4"/>
  {_panel(382, True)}
</svg>"""


BUILDERS = {
    "wpw-mahaim-insertions-diagram": svg_mahaim_insertions,
    "wpw-intermittent-delta-diagram": svg_intermittent_delta,
    "wpw-asymptomatic-ep-risk-diagram": svg_asymptomatic_ep_risk,
    "pace-corrected-ppi-tcl-diagram": svg_corrected_ppi_tcl,
    "pace-base-minus-apex-diagram": svg_base_minus_apex,
    "pacing-para-his-masked-diagram": svg_para_his_masked,
}
