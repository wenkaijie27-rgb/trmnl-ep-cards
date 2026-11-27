"""SVG generators for Advanced Domains 1 & 2: Conduction Anatomy & Interval Traps (Cards 1-6)."""

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


def svg_inferoseptal_recess(uid: str = "recess") -> str:
    """Adv 1. anatomy-inferoseptal-recess-diagram (square_1_1, Cabrera 2020 Fig. 3A)."""
    # Oblique section looking at LV cavity (left), muscular IVS (bottom center),
    # membranous septum & mitral leaflet continuity (upper-mid), and Right Atrium + Inferior Pyramidal Space (right/bottom-right).
    recess_hatch = ellipse_hatch_lines(150, 146, 22, 34, spacing=6.5, rot_deg=14.0, stroke_width=1.3)
    return f"""<svg class="ep-svg ep-svg--square" viewBox="0 0 360 350" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="左室下间隔隐窝、心腔外锥形间隙与房室传导轴关系图">
  <rect x="0" y="0" width="360" height="350" fill="#ffffff"/>

  <!-- Left Ventricular Wall & Cavity (left side) -->
  <path d="M 38 46 C 48 134, 68 206, 94 268" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.6" stroke-linecap="round"/>
  <!-- Muscular Interventricular Septum (separating LV recess on left from Pyramidal Space on right) -->
  <path d="M 136 286 C 148 242, 166 190, 184 134" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.6" stroke-linecap="round"/>
  <path d="M 190 296 C 194 238, 198 184, 206 130" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.4" stroke-linecap="round"/>

  <!-- Membranous septum + fibrous body at apex -->
  <path d="M 184 134 C 192 98, 202 72, 214 54" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.2"/>
  <path d="M 206 130 C 216 96, 226 70, 240 52" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.2"/>
  <ellipse cx="198" cy="112" rx="14" ry="20" transform="rotate(14 198 112)" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="1.6" stroke-dasharray="3,2"/>

  <!-- Mitral Valve Septal/Anterior Leaflet bordering the LV Inferoseptal Recess -->
  <path d="M 122 52 C 122 98, 126 154, 134 198" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="3.0" stroke-linecap="round"/>
  <path d="M 134 198 C 118 228, 114 258, 118 282" fill="none" class="ep-muted-stroke" stroke="#555555" stroke-width="1.5" stroke-dasharray="3,3"/>

  <!-- Highlighted LV Inferoseptal Recess (intracavitary cleft between mitral leaflet & muscular IVS) -->
  <ellipse cx="150" cy="146" rx="22" ry="34" transform="rotate(14 150 146)" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.4" stroke-dasharray="4,2.5"/>
  {recess_hatch}

  <!-- Extracavitary Inferior Pyramidal Space (right of IVS, below Right Atrium, outlined with dashed border per Cabrera Fig. 3A) -->
  <path d="M 206 136 L 194 294 L 284 294 C 266 238, 240 176, 206 136 Z" fill="#ffffff" class="ep-muted-stroke" stroke="#555555" stroke-width="1.8" stroke-dasharray="5,3"/>

  <!-- Right Atrial Endocardial Contour (right side) -->
  <path d="M 248 56 C 284 82, 314 134, 318 202 C 320 248, 306 286, 286 306" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.4" stroke-linecap="round"/>
  <!-- Tricuspid septal hinge separating RA from RV/septum -->
  <path d="M 224 128 C 254 148, 276 178, 288 214" fill="none" class="ep-muted-stroke" stroke="#555555" stroke-width="1.6"/>

  <!-- Conduction Axis (Compact node -> Penetrating bundle -> Non-branching -> Branching AV bundle) -->
  <path d="M 252 240 C 232 204, 214 162, 198 112 C 192 88, 186 68, 178 46" fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="3.6" stroke-dasharray="8,4" stroke-linecap="round"/>
  {arrow_polygon(177, 42, -104.0, 9.0, 4.2, css_class="ep-accent-fill")}
  <ellipse cx="246" cy="228" rx="9" ry="14" transform="rotate(-24 246 228)" fill="#ffffff" class="ep-accent-stroke" stroke="#000000" stroke-width="2.2"/>

  <!-- Labels -->
  {label_box(58, 28, "斜切断面观", width=82, height=20, font_size=12, role="muted", border=True)}
  {label_box(68, 114, "二尖瓣叶", width=62, height=17, font_size=12.5)}
  <line x1="94" y1="114" x2="124" y2="114" class="ep-ink-stroke" stroke="#000000" stroke-width="1.2"/>

  {label_box(76, 178, "左室隐窝", width=68, height=19, font_size=12.5, highlight_bg=True)}
  <line x1="108" y1="172" x2="142" y2="152" class="ep-ink-stroke" stroke="#000000" stroke-width="1.2"/>

  {label_box(160, 48, "膜部间隔", width=64, height=17, font_size=12)}
  <line x1="184" y1="54" x2="196" y2="96" class="ep-ink-stroke" stroke="#000000" stroke-width="1.2"/>

  {label_box(286, 102, "右房", width=42, height=18, font_size=13)}
  {label_box(286, 166, "传导轴", width=56, height=18, font_size=12.5, font_weight=800, role="accent")}
  <line x1="258" y1="164" x2="218" y2="154" class="ep-accent-stroke" stroke="#000000" stroke-width="1.3"/>

  {label_box(238, 318, "锥形间隙 (腔外)", width=110, height=18, font_size=12, border=True)}
  <line x1="238" y1="308" x2="238" y2="278" class="ep-ink-stroke" stroke="#000000" stroke-width="1.2"/>
  {label_box(84, 318, "左室腔 (腔内)", width=94, height=18, font_size=12, role="muted")}
</svg>"""


def svg_marshall_cs_sleeve(uid: str = "marshall") -> str:
    """Adv 2. anatomy-marshall-cs-sleeve-diagram (portrait_4_5, Han 2010 & Chauvin 2000)."""
    conn1 = ellipse_hatch_lines(178, 232, 20, 12, spacing=5.5, rot_deg=0.0, stroke_width=1.3)
    conn2 = ellipse_hatch_lines(116, 134, 18, 11, spacing=5.5, rot_deg=-20.0, stroke_width=1.3)
    return f"""<svg class="ep-svg ep-svg--portrait" viewBox="0 0 340 370" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Marshall韧带内左房斜静脉、Marshall肌束连接CS肌袖与左房示意图">
  <rect x="0" y="0" width="340" height="370" fill="#ffffff"/>

  <!-- Left Atrium posterior-lateral silhouette + left PVs -->
  <path d="M 86 84 C 122 52, 212 50, 266 86 C 304 114, 310 184, 280 236 C 242 276, 146 286, 86 246 C 58 214, 54 134, 86 84 Z"
        fill="#ffffff" class="ep-muted-stroke" stroke="#555555" stroke-width="1.8"/>
  <!-- Left Superior & Inferior PVs on upper-left -->
  <path d="M 76 116 L 34 94 M 68 142 L 26 128" fill="none" class="ep-muted-stroke" stroke="#555555" stroke-width="2.0" stroke-linecap="round"/>
  <path d="M 62 178 L 24 172 M 64 202 L 28 206" fill="none" class="ep-muted-stroke" stroke="#555555" stroke-width="2.0" stroke-linecap="round"/>

  <!-- Coronary Sinus (horizontal lower tube with muscular sleeve border) -->
  <path d="M 72 252 Q 178 272 292 252" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="14.0" stroke-linecap="round"/>
  <path d="M 72 252 Q 178 272 292 252" fill="none" class="ep-paper-fill" stroke="#ffffff" stroke-width="9.5" stroke-linecap="round"/>

  <!-- Vein of Marshall (Oblique Vein of LA lumen) coursing obliquely upward-left from CS -->
  <path d="M 164 258 C 148 218, 128 172, 108 118" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="8.0" stroke-linecap="round"/>
  <path d="M 164 258 C 148 218, 128 172, 108 118" fill="none" class="ep-paper-fill" stroke="#ffffff" stroke-width="4.4" stroke-linecap="round"/>

  <!-- Ligament sheath outline -->
  <path d="M 146 248 C 130 208, 112 162, 92 108" fill="none" class="ep-muted-stroke" stroke="#555555" stroke-width="1.2" stroke-dasharray="3,3"/>

  <!-- Highlighted Muscular Connection Points (CS sleeve insertion + LA/LPV variant insertion) -->
  <ellipse cx="178" cy="232" rx="20" ry="12" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.4"/>
  {conn1}
  <ellipse cx="116" cy="134" rx="18" ry="11" transform="rotate(-20 116 134)" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.4" stroke-dasharray="3,2"/>
  {conn2}

  <!-- Epicardial Marshall Bundle (alongside vein, red/thick dashed + conduction arrows) -->
  <path d="M 180 250 C 168 214, 146 168, 122 126" fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="3.6" stroke-dasharray="7,4" stroke-linecap="round"/>
  {arrow_polygon(147, 174, -118.0, 9.0, 4.2, css_class="ep-accent-fill")}
  <!-- Optional distal variant insertion into LA/LPV neighbor -->
  <path d="M 122 126 Q 98 118 82 126" fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="2.6" stroke-dasharray="4,3"/>

  <!-- Labels -->
  {label_box(58, 28, "心脏后外侧观", width=96, height=20, font_size=12, role="muted", border=True)}
  {label_box(204, 88, "左房", width=46, height=18, font_size=13.5)}
  {label_box(42, 72, "左肺静脉", width=62, height=16, font_size=11.5, role="muted")}

  {label_box(66, 178, "左房斜静脉", width=78, height=17, font_size=12)}
  <line x1="106" y1="176" x2="132" y2="176" class="ep-ink-stroke" stroke="#000000" stroke-width="1.2"/>

  {label_box(240, 150, "Marshall 肌束", width=102, height=19, font_size=12.5, font_weight=800, role="accent")}
  <line x1="188" y1="154" x2="152" y2="168" class="ep-accent-stroke" stroke="#000000" stroke-width="1.3"/>

  {label_box(224, 198, "肌性接入 (可变异)", width=116, height=19, font_size=12, highlight_bg=True)}
  <line x1="186" y1="206" x2="180" y2="222" class="ep-ink-stroke" stroke="#000000" stroke-width="1.2"/>

  {label_box(188, 300, "冠状窦 (CS 肌袖)", width=116, height=18, font_size=12.5)}
  <line x1="188" y1="286" x2="188" y2="268" class="ep-ink-stroke" stroke="#000000" stroke-width="1.2"/>
  {label_box(170, 344, "条数与远端接入存在个体差异", width=188, height=17, font_size=11.5, role="muted")}
</svg>"""


def svg_left_bundle_variants(uid: str = "lbbvar") -> str:
    """Adv 3. anatomy-left-bundle-variants-diagram (square_1_1, Cabrera LBB 2020 Fig. 2A)."""
    map_hatch = ellipse_hatch_lines(206, 232, 46, 30, spacing=6.5, rot_deg=-15.0, stroke_width=1.3)
    return f"""<svg class="ep-svg ep-svg--square" viewBox="0 0 360 350" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="左室间隔面左束支前后分支与可变间隔纤维示意图">
  <rect x="0" y="0" width="360" height="350" fill="#ffffff"/>

  <!-- Left Ventricular Septal Endocardial Surface Outline -->
  <path d="M 78 58 C 122 36, 224 36, 272 62 C 306 116, 294 234, 212 318 C 192 332, 166 332, 146 318 C 72 238, 52 122, 78 58 Z"
        fill="#ffffff" class="ep-muted-stroke" stroke="#555555" stroke-width="2.0"/>
  <!-- Aortic root upper landmark -->
  <path d="M 144 48 C 166 72, 198 72, 220 48" fill="none" class="ep-muted-stroke" stroke="#555555" stroke-width="1.5" stroke-dasharray="3,3"/>

  <!-- Highlighted Posterior-Septal Mapping Area (for local Purkinje signals) -->
  <ellipse cx="206" cy="232" rx="46" ry="30" transform="rotate(-15 206 232)" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.4" stroke-dasharray="4,2.5"/>
  {map_hatch}

  <!-- Left Bundle Trunk -->
  <path d="M 184 74 C 180 94, 178 112, 176 126" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="4.2" stroke-linecap="round"/>

  <!-- Anterior Fascicle fan (leftward/anterior) -->
  <path d="M 176 126 C 146 150, 114 196, 98 248" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="3.0" stroke-linecap="round"/>
  <path d="M 134 176 C 118 196, 108 214, 102 232" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="1.8"/>
  {arrow_polygon(97, 252, 110.0, 8.5, 3.8)}

  <!-- Posterior Fascicle fan (rightward/inferior-posterior) -->
  <path d="M 176 126 C 208 152, 240 198, 252 248" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="3.0" stroke-linecap="round"/>
  <path d="M 218 176 C 234 198, 244 218, 248 234" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="1.8"/>
  {arrow_polygon(253, 252, 74.0, 8.5, 3.8)}

  <!-- Variable Interconnecting Septal Fibers (from common trunk, anterior, & posterior network) -->
  <path d="M 176 126 C 174 170, 172 216, 174 268" fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="2.8" stroke-dasharray="6,3.5" stroke-linecap="round"/>
  <path d="M 142 170 C 160 186, 172 198, 198 202" fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="2.2" stroke-dasharray="4,3"/>
  <path d="M 216 172 C 198 192, 186 218, 152 240" fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="2.2" stroke-dasharray="4,3"/>
  <path d="M 174 236 C 194 244, 212 240, 232 224" fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="2.0" stroke-dasharray="4,3"/>

  <!-- Labels -->
  {label_box(58, 26, "室间隔左侧观", width=96, height=20, font_size=12, role="muted", border=True)}
  {label_box(248, 86, "左束支主干", width=80, height=18, font_size=12.5)}
  <line x1="208" y1="86" x2="186" y2="96" class="ep-ink-stroke" stroke="#000000" stroke-width="1.2"/>

  {label_box(66, 160, "前分支", width=52, height=18, font_size=12.5)}
  <line x1="94" y1="162" x2="128" y2="174" class="ep-ink-stroke" stroke="#000000" stroke-width="1.2"/>

  {label_box(286, 156, "后分支", width=52, height=18, font_size=12.5)}
  <line x1="260" y1="158" x2="224" y2="172" class="ep-ink-stroke" stroke="#000000" stroke-width="1.2"/>

  {label_box(106, 286, "间隔纤维 (多变互联)", width=124, height=18, font_size=12, font_weight=800, role="accent")}
  <line x1="154" y1="274" x2="170" y2="254" class="ep-accent-stroke" stroke="#000000" stroke-width="1.2"/>

  {label_box(264, 288, "标测区", width=62, height=20, font_size=12.5, highlight_bg=True)}
  <line x1="242" y1="274" x2="222" y2="256" class="ep-ink-stroke" stroke="#000000" stroke-width="1.2"/>
</svg>"""


def svg_rp_vs_va_cutoffs(uid: str = "rpva") -> str:
    """Adv 4. intervals-rp-vs-va-cutoffs-diagram (wide_2_1, ESC 2019 Fig. 1 & Table 12)."""
    g = grid_lines(120, 710, 60, 22, 182)
    rp_hatch = rect_hatch_lines(220, 64, 168, 22, spacing=6.5, angle_deg=-45.0, stroke_width=1.2)
    va_hatch = rect_hatch_lines(220, 102, 118, 22, spacing=6.5, angle_deg=-45.0, stroke_width=1.2)
    return f"""<svg class="ep-svg ep-svg--banner" viewBox="0 0 740 205" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="同搏共用QRS起点分别测量体表RP与腔内VA示意图">
  <rect x="0" y="0" width="740" height="205" fill="#ffffff"/>
  {g}

  <text x="14" y="48" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:13.5px;font-weight:700;">体表导联</text>
  <text x="14" y="63" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:11px;font-weight:600;">可见 P 波</text>
  <text x="14" y="142" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:13.5px;font-weight:700;">腔内通道</text>
  <text x="14" y="157" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:11px;font-weight:600;">指定房波电极</text>

  <!-- Shared QRS Onset Cursor at x=220 -->
  <line x1="220" y1="20" x2="220" y2="178" class="ep-ink-stroke" stroke="#000000" stroke-width="2.0" stroke-dasharray="5,3"/>

  <!-- End Cursor 1: Intracardiac Atrial Onset (VA endpoint) at x=338 -->
  <line x1="338" y1="98" x2="338" y2="178" class="ep-accent-stroke" stroke="#000000" stroke-width="2.2"/>
  <!-- End Cursor 2: Surface P Onset (RP endpoint) at x=388 -->
  <line x1="388" y1="20" x2="388" y2="92" class="ep-accent-stroke" stroke="#000000" stroke-width="2.2"/>

  <!-- RP Span Band (x=220..388, y=64..86) -->
  <rect x="220" y="64" width="168" height="22" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.2"/>
  {rp_hatch}
  <line x1="224" y1="75" x2="384" y2="75" class="ep-ink-stroke" stroke="#000000" stroke-width="1.4"/>
  {arrow_polygon(222, 75, 180.0, 5.5, 2.8)}
  {arrow_polygon(386, 75, 0.0, 5.5, 2.8)}
  {label_box(304, 79, "RP (体表分诊 90 ms)", width=118, height=15, font_size=11.5, font_weight=800)}

  <!-- VA Span Band (x=220..338, y=102..124) -->
  <rect x="220" y="102" width="118" height="22" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.2"/>
  {va_hatch}
  <line x1="224" y1="113" x2="334" y2="113" class="ep-ink-stroke" stroke="#000000" stroke-width="1.4"/>
  {arrow_polygon(222, 113, 180.0, 5.5, 2.8)}
  {arrow_polygon(336, 113, 0.0, 5.5, 2.8)}
  {label_box(279, 117, "VA (腔内 70 ms)", width=96, height=15, font_size=11.5, font_weight=800)}

  <!-- Top Surface ECG Trace: QRS at 220..256, T at 290..350, Retrograde P starting at x=388 -->
  <path d="M 110 48 L 220 48 L 228 54 L 238 18 L 248 58 L 256 48 L 292 48 C 308 48, 322 36, 338 36 C 354 36, 368 48, 382 48 L 388 48 L 398 58 L 412 40 L 424 48 L 710 48"
        fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.4" stroke-linejoin="round"/>
  <path d="M 388 48 L 398 58 L 412 40 L 424 48" fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="2.8" stroke-linejoin="round"/>

  <!-- Bottom Intracardiac Trace: H at 196, V starting at 222, Earliest Retrograde A at x=338 -->
  <path d="M 110 144 L 194 144 {egm_biphasic(194, 144, 14, 18)} L 222 144 {egm_biphasic(222, 144, 24, 22)} L 338 144 {egm_biphasic(338, 144, 22, 22)} L 710 144"
        fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.1" stroke-linejoin="round"/>

  {label_box(212, 16, "QRS 起点 (共用)", width=88, height=15, anchor="end", font_size=12, font_weight=800)}
  {label_box(394, 16, "P 波起点", width=58, height=15, anchor="start", font_size=12, font_weight=800, role="accent")}
  {label_box(344, 174, "腔内房波起点 (标明通道)", width=148, height=16, anchor="start", font_size=11.5, font_weight=800, role="accent")}
  {scale_bar(556, 668, 192, "100 ms", "两尺终点各自测量")}
</svg>"""


def svg_falsely_short_hv(uid: str = "shorthv") -> str:
    """Adv 5. intervals-falsely-short-hv-diagram (wide_2_1, Issa 3e Fig. 4.19)."""
    g = grid_lines(120, 710, 60, 22, 180)
    true_hatch = rect_hatch_lines(296, 60, 64, 22, spacing=6.0, angle_deg=-45.0, stroke_width=1.2)
    false_hatch = rect_hatch_lines(334, 138, 26, 20, spacing=5.0, angle_deg=-45.0, stroke_width=1.1)
    return f"""<svg class="ep-svg ep-svg--banner" viewBox="0 0 740 205" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="误把较晚右束支尖波当近端His造成假短HV示意图">
  <rect x="0" y="0" width="740" height="205" fill="#ffffff"/>
  {g}

  <text x="14" y="42" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:13px;font-weight:700;">体表 QRS</text>
  <text x="14" y="96" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:13px;font-weight:700;">近端 His 轨</text>
  <text x="14" y="110" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:10.5px;font-weight:600;">含较大房波</text>
  <text x="14" y="160" fill="#000000" class="ep-svg-label ep-accent-fill" style="font-size:13px;font-weight:800;">远端 / 右束支</text>
  <text x="14" y="174" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:10.5px;font-weight:600;">房波很小</text>

  <!-- True Proximal His Onset at x=296; Wrong Distal RB Spike at x=334; Shared Earliest V at x=360 -->
  <line x1="296" y1="54" x2="296" y2="122" class="ep-ink-stroke" stroke="#000000" stroke-width="2.0" stroke-dasharray="5,3"/>
  <line x1="334" y1="126" x2="334" y2="182" class="ep-accent-stroke" stroke="#000000" stroke-width="2.2"/>
  <line x1="360" y1="18" x2="360" y2="182" class="ep-ink-stroke" stroke="#000000" stroke-width="2.0" stroke-dasharray="5,3"/>

  <!-- True HV span (296..360) -->
  <rect x="296" y="60" width="64" height="22" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.2"/>
  {true_hatch}
  {label_box(328, 75, "正确 HV", width=52, height=15, font_size=11.5, font_weight=800)}

  <!-- False short HV span (334..360) -->
  <rect x="334" y="138" width="26" height="20" fill="#ffffff" class="ep-hl-area ep-accent-stroke" stroke="#000000" stroke-width="1.2"/>
  {false_hatch}

  <!-- Surface ECG (P at 170..220, QRS at x=360) -->
  <path d="M 110 42 L 154 42 C 166 42, 174 28, 190 28 C 206 28, 214 42, 226 42 L 360 42 L 366 48 L 378 12 L 390 50 L 398 42 L 710 42"
        fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.4" stroke-linejoin="round"/>

  <!-- Proximal His Track (Large A at 190, Proximal His at x=296, V at 368) -->
  <path d="M 110 100 L 186 100 {egm_biphasic(186, 100, 22, 21)} L 296 100 {egm_biphasic(296, 100, 14, 20)} L 366 100 {egm_biphasic(366, 100, 22, 22)} L 710 100"
        fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.1" stroke-linejoin="round"/>

  <!-- Distal / Right Bundle Track (Tiny A at 194, Later RB spike at x=334, V at 362) -->
  <path d="M 110 162 L 194 162 L 198 156 L 202 167 L 206 162 L 334 162 {egm_biphasic(334, 162, 12, 18)} L 362 162 {egm_biphasic(362, 162, 22, 22)} L 710 162"
        fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.1" stroke-linejoin="round"/>

  {label_box(197, 124, "局部房波 (辅助定位)", width=116, height=15, font_size=11.5, role="muted")}
  {label_box(288, 60, "近端 His", width=56, height=15, anchor="end", font_size=12, font_weight=800)}
  {label_box(366, 16, "最早室激动 (两尺共同终点)", width=166, height=15, anchor="start", font_size=12, font_weight=800)}
  {label_box(326, 186, "误用右束支尖波 → 假短 HV", width=158, height=15, anchor="end", font_size=11.5, font_weight=800, role="accent")}
  {scale_bar(556, 668, 192, "100 ms", "确认近端尖波")}
</svg>"""


def svg_deep_cs_simultaneity(uid: str = "deepcs") -> str:
    """Adv 6. intervals-deep-cs-simultaneity-diagram (compare_two, Issa 3e Fig. 4.20)."""
    def _panel(x0: int, is_deep: bool) -> str:
        title = "深置导管 (患者 B 例)" if is_deep else "常规窦口置管 (患者 A 例)"
        sub = "两端近同步，中段较晚" if is_deep else "由近端依次排到远端"
        if not is_deep:
            # Ostial CS: prox=178, mid=214, dist=250 (clean diagonal!)
            ax_p, ax_m, ax_d = 178, 214, 250
            seq = '<path d="M 184 52 L 220 96 L 256 140" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="1.8" stroke-dasharray="4,2.5"/>'
            cath_arc = '<path d="M 104 186 C 118 190, 128 186, 134 176" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="2.4" stroke-linecap="round"/>'
            hl = ""
            foot = "近端在 CS 口 → 房波顺次后延"
        else:
            # Deep CS: prox=190 (past ostium), dist=196 (near-simultaneous!), mid=246 (latest chevron!)
            ax_p, ax_m, ax_d = 190, 246, 196
            seq = '<path d="M 196 52 L 252 96 L 202 140" fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="2.0" stroke-dasharray="5,2.5"/>'
            cath_arc = '<path d="M 116 186 C 132 184, 144 170, 136 154" fill="none" class="ep-accent-stroke" stroke="#000000" stroke-width="2.8" stroke-dasharray="5,3" stroke-linecap="round"/>'
            hl = (
                '<rect x="180" y="38" width="34" height="24" rx="3" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.1"/>'
                + rect_hatch_lines(180, 38, 34, 24, 5.5, -45.0, 1.0)
                + '<rect x="184" y="126" width="34" height="24" rx="3" fill="#ffffff" class="ep-hl-area ep-ink-stroke" stroke="#000000" stroke-width="1.1"/>'
                + rect_hatch_lines(184, 126, 34, 24, 5.5, -45.0, 1.0)
            )
            foot = "近端越过 CS 口 → 两端接近，中段偏晚"

        return f"""  <g transform="translate({x0}, 0)">
    <rect x="6" y="6" width="346" height="203" rx="8" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="1.6"/>
    <text x="18" y="26" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:13.5px;font-weight:800;">{title}</text>
    <text x="338" y="26" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:11px;font-weight:600;text-anchor:end;">{sub}</text>

    {hl}
    <text x="16" y="54" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:11.5px;font-weight:700;">CS 近端</text>
    <text x="16" y="98" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:11.5px;font-weight:700;">CS 中段</text>
    <text x="16" y="142" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:11.5px;font-weight:700;">CS 远端</text>

    <path d="M 74 50 L {ax_p} 50 {egm_biphasic(ax_p, 50, 18, 17)} L 298 50 {egm_biphasic(298, 50, 14, 15)} L 336 50" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="1.9" stroke-linejoin="round"/>
    <path d="M 74 94 L {ax_m} 94 {egm_biphasic(ax_m, 94, 18, 17)} L 298 94 {egm_biphasic(298, 94, 16, 17)} L 336 94" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="1.9" stroke-linejoin="round"/>
    <path d="M 74 138 L {ax_d} 138 {egm_biphasic(ax_d, 138, 18, 17)} L 298 138 {egm_biphasic(298, 138, 18, 20)} L 336 138" fill="none" class="ep-ink-stroke" stroke="#000000" stroke-width="1.9" stroke-linejoin="round"/>
    {seq}
    {label_box(307, 118, "室波 V", width=40, height=14, font_size=10.5, role="muted")}

    <!-- Mini Valve Ring Position Inset at Bottom-Left (Issa Fig. 4.20 bottom) -->
    <ellipse cx="78" cy="172" rx="18" ry="13" fill="#ffffff" class="ep-muted-stroke" stroke="#555555" stroke-width="1.3"/>
    <ellipse cx="124" cy="172" rx="18" ry="13" fill="#ffffff" class="ep-muted-stroke" stroke="#555555" stroke-width="1.3"/>
    <circle cx="98" cy="186" r="3" fill="#ffffff" class="ep-ink-stroke" stroke="#000000" stroke-width="1.4"/>
    {cath_arc}
    <text x="64" y="198" fill="#555555" class="ep-svg-label ep-muted-fill" style="font-size:10px;font-weight:700;">CS 口</text>
    <text x="234" y="196" fill="#000000" class="ep-svg-label ep-ink-fill" style="font-size:11px;font-weight:700;text-anchor:middle;">{foot}</text>
  </g>"""

    return f"""<svg class="ep-svg ep-svg--compare" viewBox="0 0 740 215" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="不同病例下窦口放置与深置CS导管的三道房波顺序比较">
  <rect x="0" y="0" width="740" height="215" fill="#ffffff"/>
  {_panel(0, False)}
  <line x1="370" y1="14" x2="370" y2="201" class="ep-muted-stroke" stroke="#555555" stroke-width="1.4" stroke-dasharray="4,4"/>
  {_panel(382, True)}
</svg>"""


BUILDERS = {
    "anatomy-inferoseptal-recess-diagram": svg_inferoseptal_recess,
    "anatomy-marshall-cs-sleeve-diagram": svg_marshall_cs_sleeve,
    "anatomy-left-bundle-variants-diagram": svg_left_bundle_variants,
    "intervals-rp-vs-va-cutoffs-diagram": svg_rp_vs_va_cutoffs,
    "intervals-falsely-short-hv-diagram": svg_falsely_short_hv,
    "intervals-deep-cs-simultaneity-diagram": svg_deep_cs_simultaneity,
}
