"""SVG generators for Domains 1 & 2: Conduction Anatomy & Basic Intervals (Cards 1-6)."""

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


def svg_koch_triangle(uid: str = "koch") -> str:
    """1. anatomy-koch-triangle-diagram (square_1_1, Cabrera 2020 Fig. 3B)."""
    apex_hatch = ellipse_hatch_lines(236, 128, 36, 13, spacing=6.5, rot_deg=-48.0, stroke_width=1.4)
    bundle_arrow = arrow_polygon(318, 74, 2.0, length=9.5, half_width=4.4)
    return f"""<svg class="ep-svg ep-svg--square" viewBox="0 0 360 350" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Koch三角右房腔内观解剖简笔画">
  <rect x="0" y="0" width="360" height="350" fill="#ffffff"/>
  <path d="M 22 252 C 18 168, 56 88, 146 42 C 208 12, 282 14, 336 42" fill="none" class="ep-muted-stroke" stroke="#555555" stroke-width="1.4" stroke-dasharray="3,3"/>
  <path d="M 336 42 C 344 128, 344 226, 326 308" fill="none" class="ep-muted-stroke" stroke="#555555" stroke-width="1.2" stroke-dasharray="3,3"/>
  <path d="M 22 252 C 38 302, 86 328, 174 328 C 242 328, 294 318, 326 308" fill="none" class="ep-muted-stroke" stroke="#555555" stroke-width="1.4" stroke-dasharray="3,3"/>
  <path d="M 244 52 C 266 42, 294 46, 314 66" fill="none" class="ep-muted-stroke" stroke="#555555" stroke-width="1.6"/>
  <path d="M 256 76 C 272 68, 292 70, 306 82" fill="none" class="ep-muted-stroke" stroke="#555555" stroke-width="1.2"/>

  <ellipse cx="236" cy="128" rx="36" ry="13" transform="rotate(-48 236 128)" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.5" stroke-dasharray="4,2.5"/>
  {apex_hatch}
  <circle cx="268" cy="88" r="4" fill="#ffffff" class="ep-paper-fill ep-ink-stroke" stroke="#000000" stroke-width="1.8"/>
  <path d="M 271 86 C 284 78, 298 74, 312 74" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.6" stroke-linecap="round"/>
  {bundle_arrow}
  <path d="M 118 232 L 258 100 L 256 266 Z" fill="none" class="ep-muted-stroke" stroke="#555555" stroke-width="0.9" stroke-dasharray="2,4"/>
  <path d="M 284 134 C 304 146, 316 162, 314 182 C 312 198, 300 212, 292 224 C 310 236, 318 256, 306 276" fill="none" class="ep-muted-stroke" stroke="#555555" stroke-width="1.5"/>
  <path d="M 314 182 L 336 190 M 304 208 L 334 218 M 308 254 L 334 264" fill="none" class="ep-muted-stroke" stroke="#555555" stroke-width="1.1"/>

  <path d="M 286 292 C 268 236, 266 164, 268 94" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="3.2" stroke-linecap="round"/>
  <path d="M 60 256 C 118 206, 194 142, 263 92" fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="3.2" stroke-dasharray="9,5" stroke-linecap="round"/>

  <g transform="translate(122, 264) rotate(-14)">
    <ellipse cx="0" cy="0" rx="30" ry="20" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="2.8"/>
    <path d="M -20 -4 C -8 -13, 10 -12, 20 -3" fill="none" class="ep-muted-stroke" stroke="#555555" stroke-width="1.4"/>
    <path d="M -17 6 C -6 12, 8 12, 18 5" fill="none" class="ep-muted-stroke" stroke="#555555" stroke-width="1.2"/>
  </g>

  {label_box(57, 28, "右房腔内观", width=88, height=22, font_size=12.5, role="muted", border=True)}
  <line x1="271" y1="84" x2="294" y2="54" class="ep-ink-stroke" stroke="#000000" stroke-width="1.3"/>
  {label_box(296, 48, "三角尖", width=50, height=18, font_size=14)}
  <line x1="224" y1="120" x2="176" y2="76" class="ep-ink-stroke" stroke="#000000" stroke-width="1.3"/>
  {label_box(140, 70, "传导轴邻域", width=88, height=23, font_size=13, highlight_bg=True)}
  <line x1="138" y1="186" x2="94" y2="150" class="ep-accent-stroke" stroke="#000000" stroke-width="1.4"/>
  {label_box(74, 144, "Todaro 腱", width=82, height=18, font_size=14, role="accent")}
  <line x1="266" y1="216" x2="226" y2="216" class="ep-ink-stroke" stroke="#000000" stroke-width="1.3"/>
  {label_box(184, 221, "隔瓣附着线", width=80, height=18, font_size=13.5)}
  <line x1="118" y1="285" x2="96" y2="314" class="ep-ink-stroke" stroke="#000000" stroke-width="1.3"/>
  {label_box(90, 333, "冠状窦口", width=72, height=18, font_size=14)}
</svg>"""


def svg_his_purkinje(uid: str = "hp") -> str:
    """2. anatomy-his-purkinje-diagram (portrait_4_5, Ho & Ernst Ch.5 Fig. 5.3)."""
    cfb_hatch = ellipse_hatch_lines(160, 128, 34, 17, spacing=6.0, rot_deg=-8.0, stroke_width=1.3)
    return f"""<svg class="ep-svg ep-svg--portrait" viewBox="0 0 320 380" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="希浦系统冠状切面传导轴示意图">
  <rect x="0" y="0" width="320" height="380" fill="#ffffff"/>

  <!-- Subtle 4-chamber heart silhouette (coronal septum perspective) -->
  <path d="M 52 142 C 26 92, 60 28, 126 32 C 148 34, 158 54, 160 72 C 166 44, 194 26, 238 36 C 282 46, 294 102, 266 144"
        fill="none" class="ep-muted-stroke" stroke="#555555" stroke-width="1.5"/>
  <path d="M 52 142 C 30 198, 52 308, 154 352 C 186 364, 232 346, 266 290 C 292 246, 292 186, 266 144"
        fill="none" class="ep-muted-stroke" stroke="#555555" stroke-width="1.8"/>

  <!-- Fibrofatty AV insulation plane (left & right AV grooves) -->
  <path d="M 50 142 C 88 136, 118 136, 134 140" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="3.4" stroke-linecap="round"/>
  <path d="M 188 136 C 216 132, 242 136, 268 144" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="3.4" stroke-linecap="round"/>

  <!-- Ventricular septum outline (muscular septum between RV & LV) -->
  <path d="M 142 152 C 138 202, 138 262, 152 316" fill="none" class="ep-muted-stroke" stroke="#555555" stroke-width="1.3" stroke-dasharray="3,3"/>
  <path d="M 182 148 C 186 202, 190 264, 174 318" fill="none" class="ep-muted-stroke" stroke="#555555" stroke-width="1.3" stroke-dasharray="3,3"/>

  <!-- Central fibrous body (highlight zone around penetrating His) -->
  <ellipse cx="160" cy="128" rx="34" ry="17" transform="rotate(-8 160 128)"
           fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.4" stroke-dasharray="4,2.5"/>
  {cfb_hatch}

  <!-- AV Node (right atrial side above fibrous body) -->
  <ellipse cx="130" cy="108" rx="16" ry="10" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="2.4"/>

  <!-- Penetrating His bundle piercing central fibrous body -->
  <path d="M 144 114 C 154 120, 162 132, 162 156" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="3.8" stroke-linecap="round"/>

  <!-- Right Bundle Branch (thin cord along right side of septum -> RV apex) -->
  <path d="M 161 156 C 148 186, 138 238, 136 286 C 134 308, 118 318, 96 306"
        fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="2.8" stroke-dasharray="7,3.5" stroke-linecap="round"/>
  {arrow_polygon(136, 268, 92.0, length=8.0, half_width=3.8, css_class="ep-accent-fill")}

  <!-- Left Bundle Branch (broad fanning fascicles on left side of septum -> LV wall) -->
  <path d="M 163 156 C 178 176, 188 216, 190 274 C 192 310, 218 320, 242 290"
        fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="3.2" stroke-dasharray="7,3.5" stroke-linecap="round"/>
  <path d="M 168 168 C 192 184, 212 222, 220 264"
        fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="2.2" stroke-dasharray="5,3" stroke-linecap="round"/>
  {arrow_polygon(190, 260, 88.0, length=8.0, half_width=3.8, css_class="ep-accent-fill")}

  <!-- Distal Subendocardial Purkinje Network (arborizing upward along outer walls) -->
  <path d="M 96 306 C 68 282, 56 236, 62 182 M 74 276 L 56 254 M 62 228 L 48 206"
        fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="1.9" stroke-linecap="round"/>
  <path d="M 242 290 C 264 260, 272 214, 258 170 M 258 262 L 274 238 M 266 222 L 276 196"
        fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="1.9" stroke-linecap="round"/>

  <!-- Labels (6 schema labels, clear non-overlapping layout) -->
  {label_box(26, 22, "心室传导轴", width=78, height=20, anchor="start", font_size=12, role="muted", border=True)}

  <line x1="116" y1="102" x2="88" y2="78" class="ep-ink-stroke" stroke="#000000" stroke-width="1.3"/>
  {label_box(84, 72, "房室结", width=56, height=18, font_size=13.5)}

  <line x1="188" y1="118" x2="226" y2="86" class="ep-ink-stroke" stroke="#000000" stroke-width="1.3"/>
  {label_box(246, 78, "纤维体", width=66, height=21, font_size=13, highlight_bg=True)}

  <line x1="170" y1="150" x2="224" y2="152" class="ep-ink-stroke" stroke="#000000" stroke-width="1.3"/>
  {label_box(248, 157, "His 主干", width=68, height=18, font_size=13.5)}

  <line x1="138" y1="224" x2="96" y2="212" class="ep-accent-stroke" stroke="#000000" stroke-width="1.3"/>
  {label_box(84, 206, "右束支", width=56, height=18, font_size=13.5, role="accent")}

  <line x1="198" y1="224" x2="232" y2="208" class="ep-accent-stroke" stroke="#000000" stroke-width="1.3"/>
  {label_box(248, 202, "左束支", width=56, height=18, font_size=13.5, role="accent")}

  <line x1="104" y1="312" x2="132" y2="342" class="ep-ink-stroke" stroke="#000000" stroke-width="1.3"/>
  <line x1="228" y1="306" x2="188" y2="342" class="ep-ink-stroke" stroke="#000000" stroke-width="1.3"/>
  {label_box(160, 358, "心室内膜下浦肯野网", width=136, height=19, font_size=13)}
</svg>"""


def svg_cs_mitral_annulus(uid: str = "csma") -> str:
    """3. anatomy-cs-mitral-annulus-diagram (landscape_4_3, Issa 3e Ch.4 Fig. 4.18 right)."""
    groove_hatch = rect_hatch_lines(76, 134, 178, 30, spacing=7.0, angle_deg=-45.0, stroke_width=1.2)
    cs_arrow = arrow_polygon(88, 152, 185.0, length=8.5, half_width=4.0, css_class="ep-accent-fill")
    return f"""<svg class="ep-svg ep-svg--landscape" viewBox="0 0 360 280" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="心脏后面观冠状窦与二尖瓣环邻近关系示意图">
  <rect x="0" y="0" width="360" height="280" fill="#ffffff"/>

  <!-- Posterior cardiac silhouette: LA (top-left/mid), RA (right), LV (bottom-left) -->
  <path d="M 64 134 C 54 88, 92 42, 166 42 C 212 42, 240 58, 250 86" fill="none" class="ep-muted-stroke" stroke="#555555" stroke-width="1.6"/>
  <path d="M 244 54 C 294 56, 324 94, 314 148 C 308 178, 286 194, 260 198" fill="none" class="ep-muted-stroke" stroke="#555555" stroke-width="1.6"/>
  <path d="M 64 148 C 52 198, 96 254, 164 256 C 216 256, 252 224, 266 188" fill="none" class="ep-muted-stroke" stroke="#555555" stroke-width="1.8"/>

  <!-- Left AV Groove highlight band (between LA and LV) -->
  <rect x="76" y="134" width="178" height="30" rx="12" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.2" stroke-dasharray="3,2"/>
  {groove_hatch}

  <!-- Mitral Annulus (tilted fibrous ring beneath LA/CS plane) -->
  <ellipse cx="152" cy="160" rx="76" ry="18" transform="rotate(-4 152 160)" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.6"/>

  <!-- Coronary Sinus coursing along posterior left AV groove ~superior to mitral annulus -->
  <path d="M 256 154 C 214 148, 148 144, 92 152 C 74 155, 62 172, 60 192"
        fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="4.2" stroke-dasharray="9,4" stroke-linecap="round"/>
  {cs_arrow}
  <!-- Tributary cardiac veins -->
  <path d="M 192 146 L 178 198 M 136 146 L 122 204" fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="1.8" stroke-dasharray="4,3"/>

  <!-- Coronary Sinus Ostium opening into Right Atrium -->
  <ellipse cx="262" cy="154" rx="11" ry="14" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="2.8"/>

  <!-- Labels (5 schema labels + orientation badge) -->
  {label_box(52, 25, "心脏后面观", width=84, height=21, font_size=12.5, role="muted", border=True)}
  {label_box(292, 92, "右房", width=44, height=18, font_size=13.5)}
  {label_box(156, 86, "左房", width=44, height=18, font_size=13, role="muted")}

  <line x1="158" y1="140" x2="158" y2="114" class="ep-ink-stroke" stroke="#000000" stroke-width="1.3"/>
  {label_box(158, 110, "左房室沟", width=74, height=21, font_size=13, highlight_bg=True)}

  <line x1="212" y1="146" x2="230" y2="112" class="ep-accent-stroke" stroke="#000000" stroke-width="1.3"/>
  {label_box(242, 108, "冠状窦 (近→远)", width=102, height=18, font_size=13, role="accent")}

  <line x1="268" y1="168" x2="288" y2="212" class="ep-ink-stroke" stroke="#000000" stroke-width="1.3"/>
  {label_box(286, 228, "冠状窦口", width=72, height=18, font_size=13.5)}

  <line x1="148" y1="179" x2="148" y2="226" class="ep-ink-stroke" stroke="#000000" stroke-width="1.3"/>
  {label_box(148, 242, "二尖瓣环", width=72, height=18, font_size=13.5)}
</svg>"""


def svg_ah_hv_intervals(uid: str = "ahhv") -> str:
    """4. intervals-ah-hv-diagram (ultrawide_3_1, Issa 3e Fig. 4.19)."""
    g = grid_lines(126, 706, 60, 24, 178)
    ah_hatch = rect_hatch_lines(186, 76, 114, 26, spacing=7.0, angle_deg=-45.0, stroke_width=1.3)
    hv_hatch = rect_hatch_lines(300, 76, 54, 26, spacing=6.0, angle_deg=45.0, stroke_width=1.2)
    ah_arrows = arrow_polygon(188, 89, 180.0, 6.5, 3.2) + arrow_polygon(296, 89, 0.0, 6.5, 3.2)
    hv_arrows = arrow_polygon(304, 89, 180.0, 6.0, 3.0) + arrow_polygon(352, 89, 0.0, 6.0, 3.0)
    return f"""<svg class="ep-svg ep-svg--banner" viewBox="0 0 740 205" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="同步体表与His导联AH与HV间期测量示意图">
  <rect x="0" y="0" width="740" height="205" fill="#ffffff"/>
  {g}
  <text x="14" y="54" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:14px;font-weight:700;">体表导联</text>
  <text x="14" y="69" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:11.5px;font-weight:600;">Surface ECG</text>
  <text x="14" y="138" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:14px;font-weight:700;">His 导联</text>
  <text x="14" y="153" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:11.5px;font-weight:600;">His prox</text>

  <rect x="186" y="76" width="114" height="26" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.2"/>
  {ah_hatch}
  <line x1="192" y1="89" x2="292" y2="89" class="ep-ink-stroke" stroke="#000000" stroke-width="1.3"/>
  {ah_arrows}
  {label_box(243, 94, "AH", width=28, height=18, font_size=14, font_weight=800)}

  <rect x="300" y="76" width="54" height="26" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.2"/>
  {hv_hatch}
  <line x1="307" y1="89" x2="348" y2="89" class="ep-ink-stroke" stroke="#000000" stroke-width="1.3"/>
  {hv_arrows}
  {label_box(327, 94, "HV", width=26, height=18, font_size=14, font_weight=800)}

  <line x1="186" y1="28" x2="186" y2="172" class="ep-ink-stroke" stroke="#000000" stroke-width="1.5" stroke-dasharray="5,3"/>
  <line x1="298.5" y1="22" x2="298.5" y2="176" class="ep-accent-stroke" stroke="#000000" stroke-width="2.0"/>
  <line x1="302.5" y1="22" x2="302.5" y2="176" class="ep-accent-stroke" stroke="#000000" stroke-width="2.0"/>
  <line x1="354" y1="22" x2="354" y2="176" class="ep-ink-stroke" stroke="#000000" stroke-width="1.8" stroke-dasharray="5,3"/>
  <line x1="384" y1="112" x2="384" y2="172" class="ep-muted-stroke" stroke="#555555" stroke-width="1.3" stroke-dasharray="2,3"/>

  <path d="M 105 56 L 146 56 C 158 56, 166 41, 182 41 C 198 41, 206 56, 218 56 L 354 56 L 362 63 L 376 14 L 390 68 L 398 56 L 478 56 C 504 56, 524 38, 550 38 C 576 38, 594 56, 624 56 L 720 56"
        fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>
  <path d="M 105 142 L 186 142 L 192 122 L 199 160 L 207 128 L 214 150 L 220 142 L 300 142 L 304 118 L 309 162 L 314 134 L 318 142 L 384 142 L 391 112 L 399 170 L 407 120 L 415 154 L 422 142 L 720 142"
        fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.3" stroke-linejoin="round" stroke-linecap="round"/>

  {label_box(292, 16, "His 起点 (共用界标)", width=122, height=16, anchor="end", font_size=13.5, font_weight=800, role="accent")}
  {label_box(361, 16, "体表 QRS 起点（最早室激动）", width=194, height=16, anchor="start", font_size=13)}
  {label_box(180, 175, "局部房波 A", width=76, height=17, anchor="end", font_size=13)}
  {label_box(385, 176, "局部室波 V (较迟)", width=112, height=17, anchor="start", font_size=12.5, role="muted")}
  {scale_bar(560, 680, 191, "100 ms", "等比例时标（示例 AH 95 ms · HV 45 ms）")}
</svg>"""


def svg_his_block(uid: str = "hisblk") -> str:
    """5. intervals-his-block-diagram (compare_two, Narula 1971 Fig. 2-3)."""
    def _panel(x0: int, is_infra: bool) -> str:
        title = "记录点远侧阻滞 (希浦侧)" if is_infra else "记录点近侧阻滞 (房室结)"
        sub = "漏搏有 A + H，缺 V" if is_infra else "漏搏有 A，缺 H 与 V"
        # Beat 1 (Conducted reference) at x=75..155, Beat 2 (Blocked) at x=210..275
        if is_infra:
            his2 = egm_biphasic(244, 152, width=16, amp=20)
            v2_note = "无 V"
            hl_x, hl_w = 236, 30
            hl_tag = "H 后阻滞"
        else:
            his2 = ""
            v2_note = "无 H · 无 V"
            hl_x, hl_w = 226, 34
            hl_tag = "H 缺失"

        ecg_path = (
            "M 46 66 L 62 66 C 68 66, 72 56, 80 56 C 88 56, 92 66, 98 66 "
            "L 124 66 L 128 71 L 134 38 L 140 73 L 144 66 C 154 66, 162 56, 172 56 C 182 56, 190 66, 200 66 "
            "L 208 66 C 214 66, 218 56, 226 56 C 234 56, 238 66, 244 66 L 336 66"
        )
        his_path = (
            f"{egm_biphasic(72, 152, 22, 18)} L 116 152 "
            f"{egm_biphasic(116, 152, 14, 20)} L 134 152 "
            f"{egm_biphasic(134, 152, 22, 24)} L 218 152 "
            f"{egm_biphasic(218, 152, 22, 18)} "
            f"{('L 244 152 ' + his2) if his2 else ''} L 336 152"
        )
        hatch = rect_hatch_lines(hl_x, 122, hl_w, 56, spacing=6.0, angle_deg=-45.0, stroke_width=1.2)
        return f"""  <g transform="translate({x0}, 0)">
    <rect x="6" y="6" width="346" height="203" rx="8" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="1.6"/>
    <text x="20" y="27" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:14px;font-weight:800;">{title}</text>
    <text x="338" y="27" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:11.5px;font-weight:600;text-anchor:end;">{sub}</text>

    <text x="14" y="69" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:11.5px;font-weight:700;">体表</text>
    <text x="14" y="155" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:11.5px;font-weight:700;">His</text>

    <rect x="{hl_x}" y="122" width="{hl_w}" height="56" rx="4" fill="#ffffff" class="ep-hl-area ep-accent-stroke" stroke="#000000" stroke-width="1.3" stroke-dasharray="4,2.5"/>
    {hatch}
    <path d="{ecg_path}" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.2" stroke-linejoin="round"/>
    <path d="{his_path}" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.1" stroke-linejoin="round"/>

    {label_box(116, 114, "下传参照 (A-H-V)", width=96, height=16, font_size=11.5, role="muted")}
    {label_box(82, 188, "A", width=16, height=15, font_size=12)}
    {label_box(123, 188, "H", width=16, height=15, font_size=12)}
    {label_box(146, 188, "V", width=16, height=15, font_size=12)}

    {label_box(228, 188, "A", width=16, height=15, font_size=12)}
    {label_box(252, 114, hl_tag, width=60, height=16, font_size=11.5, role="accent")}
    {label_box(286, 188, v2_note, width=70, height=15, font_size=12, role="accent")}
  </g>"""

    return f"""<svg class="ep-svg ep-svg--compare" viewBox="0 0 740 215" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="未下传房波时His电位定位近侧与远侧阻滞对比图">
  <rect x="0" y="0" width="740" height="215" fill="#ffffff"/>
  {_panel(0, False)}
  <line x1="370" y1="14" x2="370" y2="201" class="ep-muted-stroke" stroke="#555555" stroke-width="1.4" stroke-dasharray="4,4"/>
  {_panel(382, True)}
</svg>"""


def svg_cs_sequence(uid: str = "csseq") -> str:
    """6. intervals-cs-sequence-diagram (wide_2_1, Issa 3e Fig. 4.18 & 4.20)."""
    g = grid_lines(130, 710, 60, 20, 200)
    # Atrial activation window across CS prox (x=216) -> CS mid (x=250) -> CS dist (x=284)
    win_hatch = rect_hatch_lines(212, 72, 80, 120, spacing=8.0, angle_deg=-45.0, stroke_width=1.1)
    slope_arrow = arrow_polygon(290, 174, 42.0, length=8.5, half_width=4.0, css_class="ep-accent-fill")
    return f"""<svg class="ep-svg ep-svg--banner" viewBox="0 0 740 215" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="窦性心律冠状窦从近端到远端激动顺序示意图">
  <rect x="0" y="0" width="740" height="215" fill="#ffffff"/>
  {g}
  <!-- Highlight Atrial Window across CS channels -->
  <rect x="212" y="72" width="80" height="120" rx="4" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.2" stroke-dasharray="3,2"/>
  {win_hatch}

  <!-- Track Labels -->
  <text x="16" y="47" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:13.5px;font-weight:700;">体表导联</text>
  <text x="16" y="96" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:13.5px;font-weight:700;">CS 近端 (近CS口)</text>
  <text x="16" y="138" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:13.5px;font-weight:700;">CS 中段</text>
  <text x="16" y="180" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:13.5px;font-weight:700;">CS 远端 (偏左室)</text>

  <!-- Surface ECG (P wave 170..250, QRS 340..405, T wave 470..560) -->
  <path d="M 140 44 L 172 44 C 184 44, 192 28, 210 28 C 228 28, 236 44, 248 44 L 340 44 L 346 51 L 358 14 L 370 54 L 378 44 L 465 44 C 485 44, 502 28, 524 28 C 546 28, 562 44, 584 44 L 710 44"
        fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.4" stroke-linejoin="round"/>

  <!-- CS Proximal: LARGE sharp A at x=216, small far-field V at x=352 -->
  <path d="M 140 92 L 216 92 {egm_biphasic(216, 92, 22, 22)} L 352 92 L 358 84 L 364 100 L 370 92 L 710 92"
        fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.1" stroke-linejoin="round"/>

  <!-- CS Mid: medium A at x=244, medium V at x=350 -->
  <path d="M 140 134 L 244 134 {egm_biphasic(244, 134, 22, 16)} L 348 134 L 355 119 L 363 149 L 370 134 L 710 134"
        fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.1" stroke-linejoin="round"/>

  <!-- CS Distal: smaller/later A at x=272, LARGE sharp LV V at x=346 -->
  <path d="M 140 176 L 272 176 {egm_biphasic(272, 176, 22, 11)} L 344 176 {egm_biphasic(344, 176, 28, 25)} L 710 176"
        fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.1" stroke-linejoin="round"/>

  <!-- Proximal-to-Distal Activation Cascade Slope Line -->
  <line x1="216" y1="68" x2="216" y2="192" class="ep-ink-stroke" stroke="#000000" stroke-width="1.4" stroke-dasharray="4,3"/>
  <line x1="218" y1="98" x2="285" y2="170" class="ep-accent-stroke" stroke="#000000" stroke-width="2.6" stroke-dasharray="6,3"/>
  {slope_arrow}

  {label_box(216, 63, "首个房波", width=62, height=16, font_size=12)}
  {label_box(254, 205, "房波时间窗 (近→远)", width=124, height=16, font_size=12, role="accent")}
  {label_box(360, 68, "室波 (远端更大)", width=100, height=16, font_size=12, role="muted")}
  {scale_bar(570, 690, 200, "100 ms", "窦律典型 CS 激动顺序")}
</svg>"""


BUILDERS = {
    "anatomy-koch-triangle-diagram": svg_koch_triangle,
    "anatomy-his-purkinje-diagram": svg_his_purkinje,
    "anatomy-cs-mitral-annulus-diagram": svg_cs_mitral_annulus,
    "intervals-ah-hv-diagram": svg_ah_hv_intervals,
    "intervals-his-block-diagram": svg_his_block,
    "intervals-cs-sequence-diagram": svg_cs_sequence,
}
