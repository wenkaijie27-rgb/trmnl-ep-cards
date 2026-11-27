"""SVG generators for Advanced Domains 3 & 4: EP Mechanisms & SVT Triage (Cards 7-12)."""

from __future__ import annotations

from .primitives import (
    arrow_polygon,
    egm_biphasic,
    grid_lines,
    label_box,
    rect_hatch_lines,
    scale_bar,
)


def svg_atypical_avnrt_limits(uid: str = "atyp") -> str:
    """Adv 7. mechanisms-atypical-avnrt-limits-diagram (compare_two, Katritsis 2015 & ESC 2019)."""
    def _panel(x0: int, is_ss: bool) -> str:
        title = "慢慢型时距例 (Slow–Slow)" if is_ss else "快慢型时距例 (Fast–Slow)"
        sub = "均须先确立非典型 AVNRT"
        # Same cycle A1 -> H -> A2 (total cycle = 220 px -> A1 at 46, A2 at 266)
        if not is_ss:
            # Fast-Slow: Short AH (x=46..118 -> 72 px < 200 ms), Long His-to-A (x=118..266 -> 148 px)
            hx = 118
            ah_w = 72
            ha_w = 148
            ah_lbl = "AH < 200 ms (较短)"
            ha_lbl = "His 至房波较长"
            note = "满足 AH < His 至房波 且 AH < 200 ms"
        else:
            # Slow-Slow: Long AH (x=46..204 -> 158 px >= 200 ms), Shorter His-to-A (x=204..266 -> 62 px)
            hx = 204
            ah_w = 158
            ha_w = 62
            ah_lbl = "AH > 200 ms (较长)"
            ha_lbl = "His 至房波"
            note = "两项指标可分歧，此时应留未分型"

        ah_hatch = rect_hatch_lines(46, 56, ah_w, 24, spacing=6.5, angle_deg=-45.0, stroke_width=1.2)
        return f"""  <g transform="translate({x0}, 0)">
    <rect x="6" y="6" width="346" height="203" rx="8" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="1.6"/>
    <text x="18" y="26" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:13.5px;font-weight:800;">{title}</text>
    <text x="338" y="26" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:10.5px;font-weight:600;text-anchor:end;">{sub}</text>

    <!-- Same cycle markers A1=46, H=hx, A2=266 -->
    <line x1="46" y1="44" x2="46" y2="152" class="ep-ink-stroke" stroke="#000000" stroke-width="1.6" stroke-dasharray="4,2"/>
    <line x1="{hx}" y1="44" x2="{hx}" y2="152" class="ep-ink-stroke" stroke="#000000" stroke-width="1.8"/>
    <line x1="266" y1="44" x2="266" y2="152" class="ep-ink-stroke" stroke="#000000" stroke-width="1.6" stroke-dasharray="4,2"/>

    <!-- AH Interval Band -->
    <rect x="46" y="56" width="{ah_w}" height="24" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.2"/>
    {ah_hatch}
    {label_box(46 + ah_w / 2, 72, ah_lbl, width=max(64, ah_w - 6), height=15, font_size=10.5, font_weight=800)}

    <!-- His-to-Atrial Band (Red/Dashed Accent) -->
    <rect x="{hx}" y="86" width="{ha_w}" height="22" fill="#ffffff" class="ep-accent-stroke" stroke="#000000" stroke-width="1.8" stroke-dasharray="5,2.5"/>
    {label_box(hx + ha_w / 2, 101, ha_lbl, width=max(56, ha_w - 6), height=15, font_size=10.5, font_weight=800, role="accent")}

    <!-- His-channel trace -->
    <path d="M 20 138 L 46 138 {egm_biphasic(46, 138, 16, 17)} L {hx} 138 {egm_biphasic(hx, 138, 14, 21)} L {hx + 22} 138 {egm_biphasic(hx + 22, 138, 20, 20)} L 266 138 {egm_biphasic(266, 138, 16, 17)} L 332 138"
          fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.0" stroke-linejoin="round"/>
    <text x="54" y="164" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:11px;font-weight:700;text-anchor:middle;">房波 A1</text>
    <text x="{hx}" y="164" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:11px;font-weight:800;text-anchor:middle;">His</text>
    <text x="274" y="164" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:11px;font-weight:700;text-anchor:middle;">下一房波 A2</text>

    <text x="180" y="196" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:11px;font-weight:700;text-anchor:middle;">{note}</text>
  </g>"""

    return f"""<svg class="ep-svg ep-svg--compare" viewBox="0 0 740 215" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="非典型AVNRT快慢型与慢慢型同一周期AH和His至房波时距对照图">
  <rect x="0" y="0" width="740" height="215" fill="#ffffff"/>
  {_panel(0, False)}
  <line x1="370" y1="14" x2="370" y2="201" class="ep-muted-stroke" stroke="#555555" stroke-width="1.4" stroke-dasharray="4,4"/>
  {_panel(382, True)}
</svg>"""


def svg_cardiac_memory(uid: str = "memory") -> str:
    """Adv 8. mechanisms-cardiac-memory-diagram (ultrawide_3_1, Goyal 1998 Fig. 4-7)."""
    g = grid_lines(40, 710, 65, 22, 165)
    pace_hatch = rect_hatch_lines(220, 32, 232, 122, spacing=8.0, angle_deg=-45.0, stroke_width=1.1)
    return f"""<svg class="ep-svg ep-svg--banner" viewBox="0 0 740 205" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="心脏电记忆：恢复窄QRS后动作电位时程变化致T波改变滞后图">
  <rect x="0" y="0" width="740" height="205" fill="#ffffff"/>
  {g}

  <!-- Phase 2 Highlight Window: Abnormal Ventricular Pacing (x=220..452) -->
  <rect x="220" y="32" width="232" height="122" rx="4" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.2" stroke-dasharray="3,2"/>
  {pace_hatch}

  <!-- Continuous Single-Lead Strip across Baseline -> RV Pacing -> Recovery -->
  <!-- Baseline (x=28..210): Narrow QRS + Upright T wave -->
  <path d="M 28 96 L 62 96 L 67 102 L 75 56 L 83 104 L 90 96 L 116 96 C 132 96, 142 74, 158 74 C 174 74, 184 96, 200 96 L 220 96"
        fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.4" stroke-linejoin="round"/>
  <!-- RV Pacing (x=220..452): Spike + Wide negative discordant QRS + Tall secondary T -->
  <path d="M 220 96 L 246 96 L 246 66 L 248 96 L 260 136 L 274 134 L 290 96 L 310 96 C 322 96, 330 70, 344 70 C 356 70, 366 96, 376 96 L 386 96 L 386 66 L 388 96 L 400 136 L 414 134 L 430 96 L 452 96"
        fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.4" stroke-linejoin="round"/>
  <!-- Post-pacing Recovery (x=452..712): IDENTICAL narrow QRS (510, 624), INVERTED/DEEP T wave (residual cardiac memory!) -->
  <path d="M 452 96 L 502 96 L 507 102 L 515 56 L 523 104 L 530 96 L 548 96"
        fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.4" stroke-linejoin="round"/>
  <path d="M 548 96 C 562 96, 574 138, 592 138 C 608 138, 616 96, 626 96"
        fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="3.4" stroke-dasharray="6,3" stroke-linecap="round"/>
  <path d="M 626 96 L 638 96 L 643 102 L 651 56 L 659 104 L 666 96 L 676 96"
        fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.4" stroke-linejoin="round"/>
  <path d="M 676 96 C 686 96, 696 132, 710 132"
        fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="3.2" stroke-dasharray="6,3" stroke-linecap="round"/>

  <!-- Phase Labels at Top -->
  {label_box(122, 22, "1. 基线 (窄 QRS · 正向 T)", width=152, height=16, font_size=12)}
  {label_box(336, 22, "2. 异常室起搏 (宽 QRS · 继发复极)", width=204, height=16, font_size=12, highlight_bg=True)}
  {label_box(592, 22, "3. 恢复后 (QRS 一致)", width=136, height=16, font_size=12, font_weight=800)}

  <!-- Residual T-wave & APD note -->
  {label_box(592, 162, "残留 T 波改变 (动作电位时程滞后恢复)", width=232, height=16, font_size=11.5, font_weight=800, role="accent")}
  {label_box(336, 162, "起搏期局部激动顺序改变", width=156, height=16, font_size=11.5, role="muted")}
  {label_box(370, 192, "同导联对比：局部复极时刻 = 局部激动时刻 + 动作电位时程", width=360, height=16, font_size=11.5, role="muted")}
</svg>"""


def svg_decremental_retrograde_pathway(uid: str = "decap") -> str:
    """Adv 9. mechanisms-decremental-retrograde-pathway-diagram (compare_two, Issa 3e p.627)."""
    def _panel(x0: int, is_dec: bool) -> str:
        title = "递减逆传旁路 (越早越慢)" if is_dec else "典型非递减旁路 (相对固定)"
        sub = "局部 VA 随提前明显延长" if is_dec else "联律提前但局部 VA 几乎不变"
        # Top beat: V2 at x=178, A at x=228 (local VA = 50px)
        # Bottom beat: Earlier V2 at x=138 (40px earlier!), A at x=188 (non-dec) vs x=258 (dec -> VA=120px!)
        va2_end = 258 if is_dec else 188
        va2_w = va2_end - 138
        va_cls = "ep-accent-stroke" if is_dec else "ep-ink-stroke"
        hl = rect_hatch_lines(138, 118, 40, 26, 6.0, -45.0, 1.1)
        return f"""  <g transform="translate({x0}, 0)">
    <rect x="6" y="6" width="346" height="203" rx="8" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="1.6"/>
    <text x="18" y="26" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:13.5px;font-weight:800;">{title}</text>
    <text x="338" y="26" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:10.5px;font-weight:600;text-anchor:end;">{sub}</text>

    <!-- Track 1: Baseline Ventricular Beat (V1 at 66, V2 at 178, A at 228) -->
    <text x="16" y="64" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:11px;font-weight:700;">常规室搏</text>
    <path d="M 74 62 L 88 62 {egm_biphasic(88, 62, 16, 18)} L 176 62 {egm_biphasic(176, 62, 18, 20)} L 228 62 {egm_biphasic(228, 62, 18, 18)} L 332 62"
          fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.0" stroke-linejoin="round"/>
    <line x1="178" y1="42" x2="178" y2="98" class="ep-muted-stroke" stroke="#555555" stroke-width="1.2" stroke-dasharray="3,3"/>
    <line x1="178" y1="84" x2="228" y2="84" class="ep-ink-stroke" stroke="#000000" stroke-width="1.6"/>
    <text x="203" y="96" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:10.5px;font-weight:700;text-anchor:middle;">局部 VA</text>

    <line x1="16" y1="108" x2="338" y2="108" class="ep-muted-stroke" stroke="#555555" stroke-width="1" stroke-dasharray="2,3"/>

    <!-- Track 2: Earlier Ventricular Beat (Coupling shortened x=178 -> 138) -->
    <text x="16" y="138" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:11px;font-weight:700;">较早室搏</text>
    <rect x="138" y="118" width="40" height="26" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.1"/>
    {hl}
    <path d="M 74 148 L 88 148 {egm_biphasic(88, 148, 16, 18)} L 136 148 {egm_biphasic(136, 148, 18, 20)} L {va2_end} 148 {egm_biphasic(va2_end, 148, 18, 18)} L 332 148"
          fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.0" stroke-linejoin="round"/>
    <line x1="138" y1="114" x2="138" y2="180" class="ep-ink-stroke" stroke="#000000" stroke-width="1.4" stroke-dasharray="3,2"/>
    <line x1="178" y1="114" x2="178" y2="144" class="ep-muted-stroke" stroke="#555555" stroke-width="1.1" stroke-dasharray="2,2"/>
    <line x1="138" y1="172" x2="{va2_end}" y2="172" class="{va_cls}" stroke="#000000" stroke-width="2.2" stroke-dasharray="5,2.5"/>
    {arrow_polygon(138, 172, 180.0, 5.5, 2.8, css_class="ep-accent-fill" if is_dec else "ep-ink-fill")}
    {arrow_polygon(va2_end, 172, 0.0, 5.5, 2.8, css_class="ep-accent-fill" if is_dec else "ep-ink-fill")}
    {label_box(138 + va2_w / 2, 186, "局部 VA 明显延长" if is_dec else "局部 VA 接近", width=max(76, va2_w), height=15, font_size=11, font_weight=800, role="accent" if is_dec else "primary")}
  </g>"""

    return f"""<svg class="ep-svg ep-svg--compare" viewBox="0 0 740 215" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="典型非递减与递减逆传旁路随着室性联律提前局部VA变化对比图">
  <rect x="0" y="0" width="740" height="215" fill="#ffffff"/>
  {_panel(0, False)}
  <line x1="370" y1="14" x2="370" y2="201" class="ep-muted-stroke" stroke="#555555" stroke-width="1.4" stroke-dasharray="4,4"/>
  {_panel(382, True)}
</svg>"""


def svg_ventricle_not_required(uid: str = "vnor") -> str:
    """Adv 10. svt-ventricle-not-required-diagram (wide_2_1, Ho 2013 Methods & Results)."""
    g = grid_lines(120, 710, 60, 22, 180)
    win_hatch = rect_hatch_lines(332, 22, 86, 156, spacing=7.0, angle_deg=-45.0, stroke_width=1.2)
    return f"""<svg class="ep-svg ep-svg--banner" viewBox="0 0 740 205" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="已证实结依赖快律中室搏真脱落但房波与His仍按原周期持续">
  <rect x="0" y="0" width="740" height="205" fill="#ffffff"/>
  {g}

  <text x="14" y="48" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:13px;font-weight:700;">体表 QRS</text>
  <text x="14" y="106" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:13px;font-weight:700;">房波 + His</text>
  <text x="14" y="162" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:13px;font-weight:700;">独立室电图</text>

  <!-- Central Expected Ventricular Window (x=332..418) -> Dropped QRS + Dropped RV EGM! -->
  <rect x="332" y="22" width="86" height="156" rx="4" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.3" stroke-dasharray="4,2"/>
  {win_hatch}
  {label_box(375, 42, "预期室搏窗", width=74, height=16, font_size=11.5, font_weight=800, border=True)}

  <!-- Regular A + His tachycardia timing ticks (160, 268, 376, 484, 592) -->
  <line x1="160" y1="68" x2="160" y2="122" class="ep-accent-stroke" stroke="#000000" stroke-width="1.6" stroke-dasharray="3,2"/>
  <line x1="268" y1="68" x2="268" y2="122" class="ep-accent-stroke" stroke="#000000" stroke-width="1.6" stroke-dasharray="3,2"/>
  <line x1="376" y1="68" x2="376" y2="122" class="ep-accent-stroke" stroke="#000000" stroke-width="2.2" stroke-dasharray="3,2"/>
  <line x1="484" y1="68" x2="484" y2="122" class="ep-accent-stroke" stroke="#000000" stroke-width="1.6" stroke-dasharray="3,2"/>
  <line x1="592" y1="68" x2="592" y2="122" class="ep-accent-stroke" stroke="#000000" stroke-width="1.6" stroke-dasharray="3,2"/>

  <!-- Surface QRS (beats at 176, 284, DROPPED at 392, resumes 500, 608) -->
  <path d="M 110 46 L 168 46 L 173 52 L 180 20 L 187 53 L 192 46 L 276 46 L 281 52 L 288 20 L 295 53 L 300 46 L 492 46 L 497 52 L 504 20 L 511 53 L 516 46 L 600 46 L 605 52 L 612 20 L 619 53 L 624 46 L 706 46"
        fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.3" stroke-linejoin="round"/>

  <!-- A + His Track: Unbroken! (A at 150,258,366,474,582 ; His at 166,274,382,490,598) -->
  <path d="M 110 102 L 146 102 {egm_biphasic(146, 102, 14, 17)} L 166 102 {egm_biphasic(166, 102, 12, 19)} L 254 102 {egm_biphasic(254, 102, 14, 17)} L 274 102 {egm_biphasic(274, 102, 12, 19)} L 362 102 {egm_biphasic(362, 102, 14, 17)} L 382 102 {egm_biphasic(382, 102, 12, 19)} L 470 102 {egm_biphasic(470, 102, 14, 17)} L 490 102 {egm_biphasic(490, 102, 12, 19)} L 578 102 {egm_biphasic(578, 102, 14, 17)} L 598 102 {egm_biphasic(598, 102, 12, 19)} L 706 102"
        fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.0" stroke-linejoin="round"/>

  <!-- Independent Ventricular Recording (beats at 176, 284, FLAT at 392, resumes 500, 608) -->
  <path d="M 110 158 L 172 158 {egm_biphasic(172, 158, 22, 22)} L 280 158 {egm_biphasic(280, 158, 22, 22)} L 496 158 {egm_biphasic(496, 158, 22, 22)} L 604 158 {egm_biphasic(604, 158, 22, 22)} L 706 158"
        fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.1" stroke-linejoin="round"/>

  {label_box(168, 16, "已证实结依赖性快律", width=124, height=15, font_size=11.5, border=True)}
  {label_box(375, 134, "A · His 按原节拍续行", width=116, height=16, font_size=11.5, font_weight=800, role="accent", border=True)}
  {label_box(375, 174, "体表与室轨均缺搏", width=112, height=16, font_size=11.5, font_weight=800)}
  {scale_bar(556, 668, 192, "200 ms", "非典型 AVNRT 可续发")}
</svg>"""


def svg_long_rp_mechanisms(uid: str = "longrp") -> str:
    """Adv 11. svt-long-rp-mechanisms-diagram (ultrawide_3_1, ESC 2019 Fig. 1)."""
    def _row(y_mid: int, title: str, kind: str) -> str:
        # Columns: Atrium (166), AVN/Loop (256..370), Ventricle (460..496), Right note (516..722)
        if kind == "at":
            src = '<circle cx="166" cy="0" r="10" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="2.0"/>' + rect_hatch_lines(159, -7, 14, 14, 4.5, -45.0, 1.0)
            path = (
                '<path d="M 178 0 L 254 0" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.2"/>'
                + arrow_polygon(258, 0, 0.0, 7.5, 3.4)
                + '<rect x="262" y="-12" width="110" height="24" rx="5" fill="#ffffff" class="ep-muted-stroke" stroke="#555555" stroke-width="1.3"/>'
                + '<text x="317" y="4" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:11px;font-weight:700;text-anchor:middle;">顺行结下传</text>'
                + '<path d="M 374 0 L 452 0" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.2"/>'
                + arrow_polygon(456, 0, 0.0, 7.5, 3.4)
            )
            desc = "房内首放 → 依下传定 RP"
        elif kind == "avnrt":
            src = '<circle cx="166" cy="0" r="8" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="1.8"/>'
            path = (
                '<rect x="258" y="-14" width="118" height="28" rx="12" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="1.8"/>'
                + '<text x="317" y="4" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:11px;font-weight:800;text-anchor:middle;">结内折返环</text>'
                # Slow return to atrium (red/dashed arrow left)
                + '<path d="M 256 -4 L 180 -4" fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="2.8" stroke-dasharray="5,3"/>'
                + arrow_polygon(176, -4, 180.0, 7.5, 3.5, css_class="ep-accent-fill")
                # Ventricle is bystander output (line to V, no return from V!)
                + '<path d="M 378 0 L 452 0" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.2"/>'
                + arrow_polygon(456, 0, 0.0, 7.5, 3.4)
            )
            desc = "结内慢径逆传，心室在环外"
        else:
            src = '<circle cx="166" cy="0" r="8" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="1.8"/>'
            path = (
                '<path d="M 176 -7 L 452 -7" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.2"/>'
                + arrow_polygon(456, -7, 0.0, 7.5, 3.4)
                + '<rect x="262" y="-16" width="110" height="17" rx="4" fill="#ffffff" class="ep-muted-stroke" stroke="#555555" stroke-width="1.2"/>'
                + '<text x="317" y="-4" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:10.5px;font-weight:700;text-anchor:middle;">正常结下传</text>'
                # Slow retrograde AP from Ventricle back to Atrium (red/dashed arrow left)
                + '<path d="M 456 10 L 180 10" fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="2.8" stroke-dasharray="6,3"/>'
                + arrow_polygon(176, 10, 180.0, 7.5, 3.5, css_class="ep-accent-fill")
                + label_box(317, 14, "递减旁路慢返回", width=94, height=14, font_size=10.5, font_weight=800, role="accent")
            )
            desc = "经结下传心室，慢旁路回房"

        return f"""  <g transform="translate(0, {y_mid})">
    <rect x="10" y="-22" width="720" height="44" rx="6" fill="#ffffff" class="ep-muted-stroke" stroke="#555555" stroke-width="1.1"/>
    <text x="22" y="4" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:13px;font-weight:800;">{title}</text>
    {src}
    {path}
    <rect x="460" y="-12" width="38" height="24" rx="4" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="1.6"/>
    <text x="479" y="4" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:11px;font-weight:800;text-anchor:middle;">QRS</text>
    <text x="720" y="4" fill="#4d4d4d" class="ep-svg-label ep-muted-fill" style="font-size:11px;font-weight:600;text-anchor:end;">{desc}</text>
  </g>"""

    return f"""<svg class="ep-svg ep-svg--banner" viewBox="0 0 740 205" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="长RP窄QRS心动过速三类来源与慢返回机制对比梯形图">
  <rect x="0" y="0" width="740" height="205" fill="#ffffff"/>
  <text x="166" y="16" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:11px;font-weight:700;text-anchor:middle;">心房 / 房波源</text>
  <text x="317" y="16" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:11px;font-weight:700;text-anchor:middle;">房室结 / 传导链路</text>
  <text x="479" y="16" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:11px;font-weight:700;text-anchor:middle;">心室</text>
  {_row(48, "1. 局灶房速", "at")}
  {_row(102, "2. 结区折返", "avnrt")}
  {_row(156, "3. 旁路折返", "avrt")}
  <text x="370" y="196" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:11.5px;font-weight:700;text-anchor:middle;">黄/网纹：房波源 · 粗虚/红线：慢返回通路 · 体表长 RP 还需结合腔内时序验证</text>
</svg>"""


def svg_junctional_pac_timing(uid: str = "jtpac") -> str:
    """Adv 12. svt-junctional-pac-timing-diagram (compare_two, Padanilam 2008 & Gilge 2021)."""
    def _panel(x0: int, is_avnrt: bool) -> str:
        title = "结折返 (AVNRT 例)" if is_avnrt else "交界灶 (JT 例)"
        sub = "下一拍 His 相对预计时点推移" if is_avnrt else "下一拍 His 留在预计时点"
        ref_hatch = rect_hatch_lines(112, 114, 34, 38, spacing=5.5, angle_deg=-45.0, stroke_width=1.1)
        # Same-cycle His at x=126 (unaffected!), Expected next His at x=258
        if not is_avnrt:
            next_his_x = 258
            slow_line = '<line x1="126" y1="68" x2="126" y2="112" class="ep-muted-stroke" stroke="#555555" stroke-width="1.4" stroke-dasharray="3,3"/>'
            next_lbl = label_box(258, 174, "下一拍 His 仍在预计点", width=132, height=15, font_size=11, font_weight=700)
        else:
            next_his_x = 232  # Advanced (or perturbed) relative to expected 258
            slow_line = (
                '<line x1="126" y1="68" x2="232" y2="132" class="ep-accent-stroke" stroke="#000000" stroke-width="2.6" stroke-dasharray="6,3"/>'
                + arrow_polygon(230, 130, 32.0, 7.5, 3.5, css_class="ep-accent-fill")
            )
            next_lbl = label_box(246, 174, "下一拍 His 推移 (支持折返)", width=148, height=15, font_size=11, font_weight=800, role="accent")

        return f"""  <g transform="translate({x0}, 0)">
    <rect x="6" y="6" width="346" height="203" rx="8" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="1.6"/>
    <text x="18" y="26" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:13.5px;font-weight:800;">{title}</text>
    <text x="338" y="26" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:10.5px;font-weight:600;text-anchor:end;">{sub}</text>

    <text x="14" y="66" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:11.5px;font-weight:700;">心房</text>
    <text x="14" y="138" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:11.5px;font-weight:700;">His</text>

    <!-- Same-cycle His Refractory Window at x=112..146 -->
    <rect x="112" y="114" width="34" height="38" rx="4" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.2" stroke-dasharray="3,2"/>
    {ref_hatch}

    <!-- Expected next His Ghost at x=258 -->
    <line x1="258" y1="108" x2="258" y2="160" class="ep-muted-stroke" stroke="#555555" stroke-width="1.5" stroke-dasharray="3,3"/>

    <!-- Atrial trace: Beat 1 at 58, PAC at 124 (during same-cycle His refractory!) -->
    <path d="M 42 62 L 56 62 {egm_biphasic(56, 62, 16, 17)} L 122 62 {egm_biphasic(122, 62, 18, 20)} L 332 62"
          fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.0" stroke-linejoin="round"/>
    <!-- His trace: Beat 1 at 58, Same-cycle His at 126, Next His at next_his_x -->
    <path d="M 42 134 L 56 134 {egm_biphasic(56, 134, 14, 19)} L 124 134 {egm_biphasic(124, 134, 14, 21)} L {next_his_x} 134 {egm_biphasic(next_his_x, 134, 14, 21)} L 332 134"
          fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.1" stroke-linejoin="round"/>
    {slow_line}

    {label_box(126, 44, "房早 (PAC)", width=64, height=15, font_size=11, font_weight=800)}
    {label_box(129, 104, "本拍不应窗", width=74, height=15, font_size=10.5, border=True)}
    {label_box(258, 104, "预计时点", width=54, height=15, font_size=10.5, role="muted")}
    {label_box(126, 158, "同拍 His (未变)", width=82, height=14, font_size=10.5, role="muted")}
    {next_lbl}
    <text x="180" y="198" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:10px;font-weight:600;text-anchor:middle;">方法示意；无推移或双径路不典型反应时需结合其他证据</text>
  </g>"""

    return f"""<svg class="ep-svg ep-svg--compare" viewBox="0 0 740 215" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="His不应期房早对比交界灶与AVNRT对同拍及下一拍His的影响">
  <rect x="0" y="0" width="740" height="215" fill="#ffffff"/>
  {_panel(0, False)}
  <line x1="370" y1="14" x2="370" y2="201" class="ep-muted-stroke" stroke="#555555" stroke-width="1.4" stroke-dasharray="4,4"/>
  {_panel(382, True)}
</svg>"""


BUILDERS = {
    "mechanisms-atypical-avnrt-limits-diagram": svg_atypical_avnrt_limits,
    "mechanisms-cardiac-memory-diagram": svg_cardiac_memory,
    "mechanisms-decremental-retrograde-pathway-diagram": svg_decremental_retrograde_pathway,
    "svt-ventricle-not-required-diagram": svg_ventricle_not_required,
    "svt-long-rp-mechanisms-diagram": svg_long_rp_mechanisms,
    "svt-junctional-pac-timing-diagram": svg_junctional_pac_timing,
}
