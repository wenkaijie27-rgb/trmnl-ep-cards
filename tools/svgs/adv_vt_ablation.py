"""SVG generators for Advanced Domains 7 & 8: Wide QRS Differential & Ablation Safety (Cards 19-24)."""

from __future__ import annotations

from .primitives import (
    arrow_polygon,
    egm_biphasic,
    grid_lines,
    label_box,
    rect_hatch_lines,
    scale_bar,
)


def svg_ashman_long_short(uid: str = "ashman") -> str:
    """Adv 19. vt-ashman-long-short-diagram (ultrawide_3_1, Issa 3e Ch.10 Fig. 10.3)."""
    g = grid_lines(110, 710, 60, 18, 174)
    # Irregular AF beats: V1=146, V2=416 (Long cycle = 270px!), V3=506 (Short cycle = 90px!) -> Wide RBBB aberrant beat at x=506!
    short_hatch = rect_hatch_lines(416, 22, 90, 96, spacing=6.5, angle_deg=-45.0, stroke_width=1.1)
    return f"""<svg class="ep-svg ep-svg--banner" viewBox="0 0 740 205" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="房颤长短周期序列后右束支不应期未恢复产生Ashman差传宽搏图">
  <rect x="0" y="0" width="740" height="205" fill="#ffffff"/>
  {g}

  <text x="14" y="64" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:13px;font-weight:700;">体表 V1</text>
  <text x="14" y="79" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:10.5px;font-weight:600;">房颤无规则 P</text>
  <text x="14" y="148" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:12px;font-weight:700;">右束支不应</text>

  <!-- Highlight Short Cycle (416..506) -->
  <rect x="416" y="22" width="90" height="96" rx="4" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.2"/>
  {short_hatch}

  <!-- AF Fibrillatory Strip: narrow QRS at 146, narrow QRS at 416 (long cycle), wide rSR' RBBB-like beat at 506 (short cycle!) -->
  <path d="M 106 68 L 146 68 L 151 74 L 157 34 L 163 76 L 169 68 C 194 64, 218 71, 244 67 C 270 63, 296 71, 324 67 C 350 64, 384 70, 416 68 L 421 74 L 427 34 L 433 76 L 439 68 C 464 64, 488 70, 506 68"
        fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.3" stroke-linejoin="round"/>
  <!-- Wide RBBB Aberrant Beat at 506..554 -->
  <path d="M 506 68 L 512 46 L 519 78 L 529 26 L 542 74 L 550 68 C 578 65, 608 71, 636 68 L 708 68"
        fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="2.9" stroke-linejoin="round"/>

  <!-- Shared middle beat onset cursors -->
  <line x1="146" y1="24" x2="146" y2="118" class="ep-ink-stroke" stroke="#000000" stroke-width="1.5" stroke-dasharray="4,2"/>
  <line x1="416" y1="22" x2="416" y2="156" class="ep-ink-stroke" stroke="#000000" stroke-width="1.8" stroke-dasharray="4,2"/>
  <line x1="506" y1="22" x2="506" y2="156" class="ep-accent-stroke" stroke="#000000" stroke-width="2.0"/>

  <!-- Long Cycle bracket (146..416) & Short Cycle bracket (416..506) -->
  <line x1="146" y1="106" x2="416" y2="106" class="ep-ink-stroke" stroke="#000000" stroke-width="1.8"/>
  {label_box(281, 106, "长周期 (延长右束支不应期)", width=172, height=16, font_size=11.5, font_weight=800)}
  {label_box(461, 106, "短周期", width=52, height=16, font_size=11.5, font_weight=800)}

  <!-- Simplified RB Refractoriness Bar -->
  <rect x="416" y="136" width="116" height="16" rx="3" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="1.4" stroke-dasharray="4,2"/>
  <line x1="506" y1="136" x2="506" y2="152" class="ep-accent-stroke" stroke="#000000" stroke-width="2.2"/>
  {label_box(474, 166, "右束支尚在不应期", width=108, height=14, font_size=10.5)}

  {label_box(416, 16, "室搏起点", width=56, height=14, font_size=11)}
  {label_box(556, 28, "差传搏 (多呈 RBBB 型)", width=136, height=16, anchor="start", font_size=11.5, font_weight=800, role="accent")}
  {scale_bar(556, 668, 192, "200 ms", "长后短亦可见室早，需结合形态")}
</svg>"""


def svg_outflow_transition_vs_sinus(uid: str = "rvot") -> str:
    """Adv 20. vt-outflow-transition-vs-sinus-diagram (compare_two, Betensky 2011 Fig. 6-7)."""
    def _panel(x0: int, is_pvc: bool) -> str:
        title = "室性搏 (流出道搏)" if is_pvc else "同人窦律参照 (无束支阻滞)"
        sub = "V3 才移行 (晚于窦律 → 倾向 RVOT)" if is_pvc else "胸导 V2 即移行 R>S"
        # 4 precordial boxes V1..V4 horizontally: x = 22, 100, 178, 256 (each w=70)
        leads = ["V1", "V2", "V3", "V4"]
        trans_idx = 2 if is_pvc else 1
        items = []
        for idx, name in enumerate(leads):
            lx = 22 + idx * 78
            if not is_pvc:
                # Sinus: V1 rS, V2 RS/Rs (transition!), V3 Rs, V4 R
                shapes = [
                    "M 8 100 L 24 100 L 28 92 L 34 134 L 40 100 L 62 100",
                    "M 8 100 L 22 100 L 28 70 L 35 120 L 42 100 L 62 100",
                    "M 8 100 L 22 100 L 28 62 L 35 112 L 42 100 L 62 100",
                    "M 8 100 L 22 100 L 28 56 L 35 106 L 42 100 L 62 100",
                ]
            else:
                # Outflow PVC (RVOT V3 transition): V1 rS, V2 rS (R<S!), V3 R>S (transition!), V4 R
                shapes = [
                    "M 8 100 L 20 100 L 24 94 L 32 142 L 40 100 L 62 100",
                    "M 8 100 L 20 100 L 25 84 L 34 138 L 42 100 L 62 100",
                    "M 8 100 L 20 100 L 27 64 L 35 116 L 42 100 L 62 100",
                    "M 8 100 L 20 100 L 28 54 L 36 106 L 42 100 L 62 100",
                ]
            is_tr = idx == trans_idx
            box_cls = "ep-hl-area ep-accent-stroke" if (is_tr and is_pvc) else ("ep-hl-area ep-ink-stroke" if is_tr else "ep-muted-stroke")
            box_sw = "2.2" if is_tr else "1.1"
            hatch = rect_hatch_lines(lx, 46, 70, 108, 7.0, -45.0, 1.0) if is_tr else ""
            tag = ("室性移行" if is_pvc else "窦律移行") if is_tr else ("R < S" if idx < trans_idx else "R > S")
            items.append(
                f'<g transform="translate({lx}, 0)">'
                f'<rect x="0" y="46" width="70" height="108" rx="4" fill="#ffffff" class="{box_cls}" stroke="#000000" stroke-width="{box_sw}"/>'
                f'</g>{hatch}<g transform="translate({lx}, 0)">'
                f'<text x="35" y="62" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:12px;font-weight:800;text-anchor:middle;">{name}</text>'
                f'<path d="{shapes[idx]}" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.4" stroke-linejoin="round"/>'
                f'<text x="35" y="148" fill="#000000" class="ep-svg-label {"ep-accent-fill" if (is_tr and is_pvc) else "ep-ink-fill"}" style="font-size:10.5px;font-weight:800;text-anchor:middle;">{tag}</text>'
                f'</g>'
            )
        foot = "均以 V3 移行 + 窦律无束支阻滞队列为参照" if is_pvc else "同人同胸导位置与同增益比对"
        return f"""  <g transform="translate({x0}, 0)">
    <rect x="6" y="6" width="346" height="203" rx="8" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="1.6"/>
    <text x="18" y="26" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:13.5px;font-weight:800;">{title}</text>
    <text x="338" y="26" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:10.5px;font-weight:600;text-anchor:end;">{sub}</text>
    {"".join(items)}
    <text x="180" y="186" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:11px;font-weight:700;text-anchor:middle;">{foot}</text>
  </g>"""

    return f"""<svg class="ep-svg ep-svg--compare" viewBox="0 0 740 215" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="同人窦律V2移行对照流出道室性搏V3移行提示右侧流出道">
  <rect x="0" y="0" width="740" height="215" fill="#ffffff"/>
  {_panel(0, False)}
  <line x1="370" y1="14" x2="370" y2="201" class="ep-muted-stroke" stroke="#555555" stroke-width="1.4" stroke-dasharray="4,4"/>
  {_panel(382, True)}
</svg>"""


def svg_papillary_vs_fascicular(uid: str = "papfas") -> str:
    """Adv 21. vt-papillary-vs-fascicular-diagram (compare_two, Al'Aref 2015 Table 2)."""
    def _panel(x0: int, is_fasc: bool) -> str:
        title = "分支起源" if is_fasc else "乳头肌起源"
        sub = "早期募集希浦 → 常较窄" if is_fasc else "先经室肌扩布 → QRS 常更宽"
        # Equal time-scale RBBB-morphology beats in V1: papillary width = 128 px vs fascicular width = 84 px!
        q_start = 104
        q_end = 188 if is_fasc else 232
        qw = q_end - q_start
        hl = rect_hatch_lines(q_start, 52, qw, 94, 6.5, -45.0, 1.1)
        if not is_fasc:
            wave = "M 32 108 L 104 108 L 122 68 L 142 120 L 176 52 L 210 116 L 232 108 L 326 108"
            width_lbl = "完整 QRS 明显较宽"
            role = "accent"
        else:
            wave = "M 32 108 L 104 108 L 116 64 L 128 118 L 154 52 L 176 114 L 188 108 L 326 108"
            width_lbl = "完整 QRS 相对较窄"
            role = "primary"
        return f"""  <g transform="translate({x0}, 0)">
    <rect x="6" y="6" width="346" height="203" rx="8" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="1.6"/>
    <text x="18" y="26" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:13.5px;font-weight:800;">{title}</text>
    <text x="338" y="26" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:10.5px;font-weight:600;text-anchor:end;">{sub}</text>

    <text x="20" y="64" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:12px;font-weight:800;">V1</text>
    <text x="20" y="79" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:10.5px;font-weight:600;">RBBB 样外观</text>

    <rect x="{q_start}" y="52" width="{qw}" height="94" rx="4" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.2"/>
    {hl}
    <path d="{wave}" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.6" stroke-linejoin="round"/>
    <line x1="{q_start}" y1="44" x2="{q_start}" y2="162" class="ep-ink-stroke" stroke="#000000" stroke-width="1.6" stroke-dasharray="4,2"/>
    <line x1="{q_end}" y1="44" x2="{q_end}" y2="162" class="ep-accent-stroke" stroke="#000000" stroke-width="1.8" stroke-dasharray="4,2"/>
    <line x1="{q_start}" y1="158" x2="{q_end}" y2="158" class="{"ep-accent-stroke" if not is_fasc else "ep-ink-stroke"}" stroke="#000000" stroke-width="2.0"/>
    {label_box((q_start + q_end) / 2, 174, width_lbl, width=max(106, qw), height=15, font_size=11, font_weight=800, role=role)}
    {scale_bar(210, 270, 194, "100 ms", "起止比对 (宽度有重叠)")}
  </g>"""

    return f"""<svg class="ep-svg ep-svg--compare" viewBox="0 0 740 215" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="同呈RBBB外观的乳头肌起源与分支起源室性搏完整QRS宽度比较">
  <rect x="0" y="0" width="740" height="215" fill="#ffffff"/>
  {_panel(0, False)}
  <line x1="370" y1="14" x2="370" y2="201" class="ep-muted-stroke" stroke="#555555" stroke-width="1.4" stroke-dasharray="4,4"/>
  {_panel(382, True)}
</svg>"""


def svg_para_hisian_target(uid: str = "phab") -> str:
    """Adv 22. ablation-para-hisian-target-diagram (landscape_4_3 inside split_left, Liberman 2014 Fig. 1-2)."""
    his_hatch = rect_hatch_lines(178, 250, 42, 46, spacing=5.5, angle_deg=-45.0, stroke_width=1.1)
    return f"""<svg class="ep-svg ep-svg--square" viewBox="0 0 360 350" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="前间隔旁路靶导管贴近正常房室传导轴并直接记录到靶端His示意图">
  <rect x="0" y="0" width="360" height="350" fill="#ffffff"/>

  <!-- Top Section (y=12..196): Anteroseptal Tricuspid Anatomy + Axis + Pathway + Ablation Catheter -->
  <rect x="12" y="12" width="336" height="184" rx="8" fill="#ffffff" class="ep-muted-stroke" stroke="#555555" stroke-width="1.2"/>
  {label_box(68, 28, "三尖瓣隔侧观", width=88, height=18, font_size=11.5, role="muted", border=True)}

  <!-- Septal tricuspid annulus hinge -->
  <path d="M 52 152 C 138 118, 230 112, 316 142" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.6" stroke-linecap="round"/>

  <!-- Normal Conduction Axis (red/thick dashed) passing through septal junction -->
  <ellipse cx="144" cy="84" rx="16" ry="10" fill="#ffffff" class="ep-accent-stroke" stroke="#000000" stroke-width="2.0"/>
  <path d="M 158 88 C 176 98, 192 114, 210 144" fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="3.6" stroke-dasharray="7,3.5" stroke-linecap="round"/>
  {arrow_polygon(214, 150, 56.0, 8.5, 4.0, css_class="ep-accent-fill")}

  <!-- Anteroseptal Accessory Pathway (adjacent but separate!) -->
  <path d="M 222 86 C 232 104, 240 124, 246 150" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.6" stroke-linecap="round"/>

  <!-- Ablation Catheter Tip positioned at the Anteroseptal Target (close to Normal Axis!) -->
  <path d="M 320 66 Q 272 86 226 106" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="5.2" stroke-linecap="round"/>
  <circle cx="224" cy="107" r="4.5" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="2.2"/>

  {label_box(92, 62, "正常传导轴", width=74, height=16, font_size=11.5, font_weight=800, role="accent")}
  {label_box(274, 52, "靶导管远端", width=74, height=16, font_size=11.5, font_weight=800)}
  {label_box(282, 166, "前间隔旁路", width=72, height=16, font_size=11.5)}
  {label_box(114, 158, "三尖瓣隔侧", width=72, height=16, font_size=11.5, role="muted")}

  <!-- Bottom Section (y=208..336): Separate EGM Inset showing Target Distal His vs Reference His -->
  <rect x="12" y="206" width="336" height="132" rx="8" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="1.5"/>
  <text x="24" y="226" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:12.5px;font-weight:800;">电图窗：靶导管自身见 His 电位</text>

  <!-- Highlight Target His Window -->
  <rect x="178" y="250" width="42" height="46" rx="4" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.2"/>
  {his_hatch}

  <text x="24" y="268" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:11.5px;font-weight:700;">靶导管远端</text>
  <path d="M 102 266 L 138 266 {egm_biphasic(138, 266, 14, 15)} L 188 266 {egm_biphasic(188, 266, 14, 18)} L 214 266 {egm_biphasic(214, 266, 22, 19)} L 330 266"
        fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.0" stroke-linejoin="round"/>

  <text x="24" y="302" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:11.5px;font-weight:700;">参考 His 道</text>
  <path d="M 102 300 L 138 300 {egm_biphasic(138, 300, 16, 14)} L 190 300 {egm_biphasic(190, 300, 14, 16)} L 246 300 {egm_biphasic(246, 300, 20, 17)} L 330 300"
        fill="none" class="ep-muted-stroke" stroke="#555555" stroke-width="1.7" stroke-linejoin="round"/>

  {label_box(199, 246, "靶端 His", width=56, height=15, font_size=11, font_weight=800, highlight_bg=True)}
  {label_box(286, 286, "旁路提前 V", width=66, height=14, font_size=10.5)}
  {label_box(180, 329, "冷冻测试并行监测正常前传与复发", width=188, height=14, font_size=10, role="muted")}
</svg>"""


def svg_coronary_vein_distance(uid: str = "cvdist") -> str:
    """Adv 23. ablation-coronary-vein-distance-diagram (square_1_1, Stavrakis 2014 Fig. 2 & 5)."""
    dist_hatch = rect_hatch_lines(170, 156, 44, 34, spacing=5.5, angle_deg=-45.0, stroke_width=1.2)
    return f"""<svg class="ep-svg ep-svg--square" viewBox="0 0 360 350" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="后间隔心中静脉消融靶电极与邻近冠状动脉最近距离测量示意图">
  <rect x="0" y="0" width="360" height="350" fill="#ffffff"/>

  <!-- Subtle epicardial sulcus context -->
  <path d="M 38 118 C 98 86, 214 78, 326 98" fill="none" class="ep-muted-stroke" stroke="#555555" stroke-width="1.3" stroke-dasharray="3,3"/>

  <!-- Coronary Sinus Ostium (left) + CS body curving into Middle Cardiac Vein (MCV) descending down -->
  <ellipse cx="86" cy="134" rx="22" ry="15" transform="rotate(-18 86 134)" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="2.6"/>
  <!-- MCV vessel walls (black solid separate tube) -->
  <path d="M 106 126 C 148 118, 174 134, 172 178 C 170 220, 166 258, 172 302" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.4" stroke-linecap="round"/>
  <path d="M 94 148 C 128 144, 144 156, 142 188 C 140 226, 138 260, 142 302" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.4" stroke-linecap="round"/>

  <!-- Target Ablation Catheter inside MCV -->
  <path d="M 88 134 C 132 134, 156 142, 156 184" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="4.4" stroke-linecap="round"/>
  <circle cx="156" cy="184" r="5.5" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="2.4"/>

  <!-- Adjacent Coronary Artery Branch (double contour, red/dashed accent, completely separate vessel!) -->
  <path d="M 244 82 C 232 128, 214 168, 224 218 C 232 252, 246 278, 260 302" fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="2.4" stroke-dasharray="6,3.5" stroke-linecap="round"/>
  <path d="M 262 86 C 250 132, 232 170, 242 216 C 250 250, 264 274, 278 298" fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="2.4" stroke-dasharray="6,3.5" stroke-linecap="round"/>

  <!-- Highlighted Closest Separation Caliper Window (from Target Tip x=162 to Closest Arterial Wall x=218) -->
  <rect x="170" y="156" width="44" height="34" rx="4" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.2"/>
  {dist_hatch}
  <line x1="162" y1="184" x2="218" y2="184" class="ep-ink-stroke" stroke="#000000" stroke-width="2.0"/>
  {arrow_polygon(162, 184, 180.0, 5.5, 2.8)}
  {arrow_polygon(218, 184, 0.0, 5.5, 2.8)}

  <!-- Labels -->
  {label_box(66, 26, "后间隔局部示意", width=96, height=19, font_size=11.5, role="muted", border=True)}
  {label_box(76, 86, "冠状窦口", width=62, height=18, font_size=12)}
  <line x1="78" y1="96" x2="84" y2="116" class="ep-ink-stroke" stroke="#000000" stroke-width="1.2"/>

  {label_box(74, 216, "靶电极", width=52, height=18, font_size=12, font_weight=800)}
  <line x1="102" y1="210" x2="148" y2="188" class="ep-ink-stroke" stroke="#000000" stroke-width="1.2"/>

  {label_box(84, 286, "心中静脉 (后间隔)", width=106, height=18, font_size=11.5)}
  <line x1="128" y1="274" x2="146" y2="256" class="ep-ink-stroke" stroke="#000000" stroke-width="1.2"/>

  {label_box(282, 128, "邻近冠脉", width=68, height=18, font_size=12.5, font_weight=800, role="accent")}
  <line x1="252" y1="138" x2="236" y2="152" class="ep-accent-stroke" stroke="#000000" stroke-width="1.2"/>

  {label_box(226, 232, "最近距离 (无比例)", width=114, height=19, font_size=11.5, highlight_bg=True)}
  <line x1="196" y1="218" x2="192" y2="192" class="ep-ink-stroke" stroke="#000000" stroke-width="1.2"/>

  {label_box(180, 330, "远端心大静脉/前室间静脉属另一拓扑，同样需造影", width=278, height=16, font_size=10.5, role="muted")}
</svg>"""


def svg_echo_window_vs_repeat(uid: str = "echowin") -> str:
    """Adv 24. ablation-echo-window-vs-repeat-diagram (compare_two, Nikoo 2018 & Katritsis 2019)."""
    win_hatch = rect_hatch_lines(54, 72, 240, 86, spacing=8.0, angle_deg=-45.0, stroke_width=1.0)
    left = f"""  <g transform="translate(0, 0)">
    <rect x="6" y="6" width="346" height="203" rx="8" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="1.6"/>
    <text x="18" y="26" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:13.5px;font-weight:800;">回波窗 (跨独立试次)</text>
    <text x="338" y="26" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:10.5px;font-weight:600;text-anchor:end;">每改变一次联律分别计数</text>

    <rect x="54" y="72" width="240" height="86" rx="4" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.2" stroke-dasharray="3,2"/>
    {win_hatch}
    {label_box(174, 58, "回波窗 (沿刺激联律间期轴的跨度)", width=196, height=16, font_size=11, font_weight=800, border=True)}

    <!-- 3 Stacked Independent Coupling-Interval Trials -> Each yields at most 1 Single Echo -->
    <text x="16" y="90" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:10.5px;font-weight:700;">试次1</text>
    <path d="M 60 88 L 116 88 L 116 74 L 118 88 L 154 88 L 154 74 L 156 88 L 204 88 {egm_biphasic(204, 88, 16, 13)} L 290 88" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="1.9" stroke-linejoin="round"/>
    <text x="314" y="90" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:10.5px;font-weight:700;text-anchor:middle;">单回波</text>

    <text x="16" y="118" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:10.5px;font-weight:700;">试次2</text>
    <path d="M 60 116 L 116 116 L 116 102 L 118 116 L 144 116 L 144 102 L 146 116 L 194 116 {egm_biphasic(194, 116, 16, 13)} L 290 116" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="1.9" stroke-linejoin="round"/>
    <text x="314" y="118" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:10.5px;font-weight:700;text-anchor:middle;">单回波</text>

    <text x="16" y="146" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:10.5px;font-weight:700;">试次3</text>
    <path d="M 60 144 L 116 144 L 116 130 L 118 144 L 134 144 L 134 130 L 136 144 L 184 144 {egm_biphasic(184, 144, 16, 13)} L 290 144" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="1.9" stroke-linejoin="round"/>
    <text x="314" y="146" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:10.5px;font-weight:700;text-anchor:middle;">单回波</text>

    <text x="136" y="174" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:11px;font-weight:700;text-anchor:middle;">← 联律间期逐步缩短</text>
    <text x="180" y="198" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:11px;font-weight:700;text-anchor:middle;">可与不可诱发持续折返并存</text>
  </g>"""

    right = f"""  <g transform="translate(382, 0)">
    <rect x="6" y="6" width="346" height="203" rx="8" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="1.6"/>
    <text x="18" y="26" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:13.5px;font-weight:800;">连发 (同一次刺激后)</text>
    <text x="338" y="26" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:10.5px;font-weight:600;text-anchor:end;">单次试次内连续房性回波</text>

    <rect x="136" y="72" width="190" height="72" rx="4" fill="#ffffff" class="ep-accent-stroke" stroke="#000000" stroke-width="1.8" stroke-dasharray="5,3"/>
    {label_box(231, 58, "同次连续回波 (另行记录个数)", width=176, height=16, font_size=11, font_weight=800, role="accent")}

    <!-- One S1-S2 trial followed by 3 consecutive echoes inside the same trial -->
    <path d="M 24 114 L 56 114 L 56 84 L 58 114 L 84 114 L 84 84 L 86 114 L 112 114 L 112 80 L 114 114 L 146 114" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.1"/>
    <path d="M 146 114 {egm_biphasic(146, 114, 18, 22)} L 198 114 {egm_biphasic(198, 114, 18, 22)} L 250 114 {egm_biphasic(250, 114, 18, 22)} L 320 114" fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="2.2" stroke-linejoin="round"/>

    {label_box(84, 140, "单次刺激", width=56, height=15, font_size=11)}
    <text x="155" y="136" fill="#000000" class="ep-svg-label ep-accent-fill" style="font-size:10.5px;font-weight:800;text-anchor:middle;">第1</text>
    <text x="207" y="136" fill="#000000" class="ep-svg-label ep-accent-fill" style="font-size:10.5px;font-weight:800;text-anchor:middle;">第2</text>
    <text x="259" y="136" fill="#000000" class="ep-svg-label ep-accent-fill" style="font-size:10.5px;font-weight:800;text-anchor:middle;">第3…</text>
    <text x="180" y="174" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:11px;font-weight:700;text-anchor:middle;">激发条件与允许回波数随方案不同</text>
    <text x="180" y="198" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:10.5px;font-weight:600;text-anchor:middle;">回波窗宽度 ≠ 同次回波数 ≠ 持续折返</text>
  </g>"""

    return f"""<svg class="ep-svg ep-svg--compare" viewBox="0 0 740 215" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="消融后跨试次单回波窗与同一次刺激后连续回波对比图">
  <rect x="0" y="0" width="740" height="215" fill="#ffffff"/>
  {left}
  <line x1="370" y1="14" x2="370" y2="201" class="ep-muted-stroke" stroke="#555555" stroke-width="1.4" stroke-dasharray="4,4"/>
  {right}
</svg>"""


BUILDERS = {
    "vt-ashman-long-short-diagram": svg_ashman_long_short,
    "vt-outflow-transition-vs-sinus-diagram": svg_outflow_transition_vs_sinus,
    "vt-papillary-vs-fascicular-diagram": svg_papillary_vs_fascicular,
    "ablation-para-hisian-target-diagram": svg_para_hisian_target,
    "ablation-coronary-vein-distance-diagram": svg_coronary_vein_distance,
    "ablation-echo-window-vs-repeat-diagram": svg_echo_window_vs_repeat,
}
