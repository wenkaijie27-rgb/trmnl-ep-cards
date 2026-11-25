# 心脏电生理墨水屏知识卡片 — GPT 文献筛选与初稿生成 Prompt

## 如何使用本 Prompt

1. **推荐运行模式**：使用支持联网检索或深度研究模式的模型（如 GPT Thinking / Deep Research）。
2. **可选本地投喂（强烈建议）**：如果希望优先提炼你自己网站和文献库里的精华，可以把以下文件（或其中几个章节）一并上传或粘贴到 Prompt 末尾的 `【可选：本地参考资料】` 中：
   - `/Users/wenkaijie/my-website/site/src/data/ep-tree/curated.json`（窄 QRS 鉴别树，可按步骤分段投喂）
   - `/Users/wenkaijie/my-website/site/src/assets/reading_notes/` 下你最关心的经典综述笔记（如 `katritsis2016.md`、`accahahrs2015svt.md`）
   - 若直接不附本地文件、让 GPT 结合经典教材/指南与文献库检索，也可直接开跑。
3. **跑完之后怎么做**：
   - 将 GPT 返回报告中的 **JSON 代码块** 保存为 `/Users/wenkaijie/Documents/Trmnl/ep-cards/decks/batch-01-draft.json`（完整报告可存为 `decks/batch-01-report.md`）；
   - 运行校验脚本检查字数、缩写白名单、版式兼容性与证据完整性：
     ```bash
     python3 /Users/wenkaijie/Documents/Trmnl/ep-cards/tools/validate_cards.py /Users/wenkaijie/Documents/Trmnl/ep-cards/decks/batch-01-draft.json
     ```
   - 然后把报告与 JSON 交给我审核医学细节与选定 **3 张黄金样板卡**，进入墨水屏原型渲染阶段。

---

## 复制下方 Prompt 发给 GPT

````markdown
# 任务：为「心脏电生理墨水屏知识卡片」筛选文献并生成首批 24 张卡片初稿

你正在协助一个开源的 **TRMNL 墨水屏插件项目（800×480 主屏 + 10.3 寸 TRMNL X 扩展屏 + 四色/黑白墨水屏兼容）** 构建心脏电生理（EP）教学知识卡片库。你的任务是检索/梳理权威电生理文献与经典教材，产出首批 **24 张结构化知识卡片初稿**（仅做内容筛选、事实核验、结构化文案与配图蓝图；**不要**编写 HTML/CSS/SVG 代码，也**不要**画 ASCII 示意图）。

---

## 一、受众与选题定位（最重要）

- **目标读者**：**刚进入心脏电生理领域的医学生**（已掌握基础内科学与常规体表心电图判读，正在导管室见习或初学电生理，需要建立“体表表现 ↔ 腔内电图 ↔ 解剖与折返机制”的桥梁）。
- **核心原则（一卡一顿悟）**：每张卡片只讲透**一个**看懂后能立刻用在读图或理解机制上的关键知识点。
- **选题分布**：请覆盖以下 **8 个主题域，每个主题域严格产出 3 张卡片（共 24 张）**，难度以入门核心（`intro`）为主，允许少量从入门跨向导管室实操的桥接卡（`bridge`）：
  1. `conduction_anatomy`（传导解剖：如 Koch 三角边界、希浦系统解剖分布、冠状窦与二尖瓣环关系）
  2. `basic_intervals`（基础间期与腔内读图：如 AH vs HV 的物理意义、H 波为何是房室传导的“分水岭”、CS 从近端到远端的激动顺序）
  3. `ep_mechanisms`（基础电生理机制：如折返三要素、房室结递减传导与“跳跃”现象、不应期与兴奋间隙）
  4. `svt_triage`（室上速体表与腔内鉴别：如典型 AVNRT 为何超短 VA、短 RP vs 长 RP 一级分诊、V1 假性 r' 与下壁假性 s）
  5. `wpw_preexcitation`（预激与旁路基础：如 delta 波形成的电生理本质、顺向型 vs 逆向型 AVRT 的宽窄 QRS 切换、显性 vs 隐匿旁路）
  6. `pacing_maneuvers`（经典起搏手法直觉：如“室早撞击 His 不应期还能提前激动心房”为何锁定旁路、心室超速起搏停止后看 V-A-V vs V-A-A-V 的直觉原理）
  7. `wide_qrs_vt`（宽 QRS 与室速基础：如室上速伴差传 vs 室速的核心时间差、房室分离与融合波的机制意义）
  8. `ablation_safety`（消融靶点与安全：如慢径消融为什么看交界性逸搏心律、房室阻滞高危解剖区识别）
- **黄金样板候选标注**：从这 24 张卡中，挑选 **4–6 张** 最直观、最具代表性的卡片标注 `"golden_prototype_candidate": true`，且必须至少覆盖：
  - 1 张适合**左右分栏 + 解剖简笔画**（如 Koch 三角/双径路）；
  - 1 张适合**上下分栏 + 波形/腔内图**（如典型 AVNRT 的短 VA 或 AH/HV）；
  - 1 张适合**双图对比卡**（如 AVNRT vs AVRT 或顺向型 vs 逆向型 AVRT）。

---

## 二、好卡 vs 坏卡对照标尺（严格校准深浅度）

- ❌ **反例 1（太浅 / 科普流水账，禁止）**：
  - 标题：「什么是室上速」
  - 内容：「室上速就是心跳过快，常见症状有心慌、胸闷，一般可以通过射频消融治疗。」
  - *问题*：没有电生理机制增量，医学生不需要花墨水屏看内科常识。
- ❌ **反例 2（太晦涩 / 堆砌冷门缩写与深水特例，禁止）**：
  - 标题：「PJRT 与 NV/NF 纤维的 SA-VA 陷阱」
  - 内容：「当存在具有递减逆传特性的隐匿性后间隔旁路或 NV 纤维时，PPI-TCL 常假性延长，需联合 ΔHA 与双位点差值拖带剔除假性 A-A-V 反应……」
  - *问题*：3 个未解释的冷门缩写 + 二阶陷阱叠加，刚入门的医学生直接看不懂。
- ✅ **正例（黄金标尺）**：
  - 标题：「典型AVNRT的短VA机制」
  - 核心结论：「快慢径折返上行传房与下行传室几乎同步，使腔内VA常≤70 ms。」
  - 要点：「激动经慢径前传心室，同时经快径逆传回心房」→「心房与心室几乎同时除极，V波常埋住逆行A波」→「逆行P波常藏于QRS终末，V1导联可呈假性r'」。
  - *优点*：用 1 个清晰图像 + 3 句话打通“为什么体表看不见 P 波”和“为什么腔内 VA ≤ 70 ms”两个困惑，既有真实阈值，又不炫技。

---

## 三、缩写白名单与术语红线

为了不让初学者被缩写墙劝退，**正文中仅允许以下 23 个常用缩写直接出现**：
`AVNRT`, `AVRT`, `AT`, `SVT`, `WPW`, `ECG`, `AH`, `HV`, `VA`, `RP`, `PR`, `QRS`, `ERP`, `CS`, `His`, `PVC`, `PAC`, `RBBB`, `LBBB`, `VT`, `AF`, `SA`, `AVN`
（常规心电图导联名如 `V1`、`II`、`III`、`aVF` 及单位 `ms`、`mV`、`bpm` 豁免。）

**硬性规则**：
1. 任何**不在此白名单中的英文缩写**（如 `PJRT`、`PPI`、`TCL`、`ORT`、`ART`、`CTI`、`NV`、`AP` 等）：
   - 如果它不是该卡片的教学主角：**严禁使用缩写**，一律写中文全称（例如写「顺向型房室折返」或直接写「经旁路前传/逆传」；写「三尖瓣峡部」而不是 `CTI`）；
   - 如果它就是本卡片要讲的核心概念：**每卡最多引入 2 个**，必须登记到 `abbreviations.defined_in_card`，且正文首次出现时用简短括号写出中文。

---

## 四、医学严谨性与防幻觉铁律

1. **只写可核对的事实**：每个数值、界值、百分比或解剖描述，必须在 `evidence` 中给出可核查出处：
   - 经典教材须注明书名、版次、章节（如 *Josephson's Clinical Cardiac Electrophysiology, 6th ed.* / *Issa Clinical Arrhythmology, 3rd ed.* / *Ho & Ernst Anatomy for Cardiac Electrophysiologists* / *Zipes, 7th ed.*）；
   - 指南或论文须注明第一作者、年份、期刊及 **DOI 或 PMID**，并给出原文关键句或核对后的阈值表述（`supporting_quote`）。
2. **严禁凭记忆编造数字或文献**：如果某条数字找不到可靠出处，宁可换用有确切来源的数值，或将该卡标出并在 `review.uncertainties` 与文末「我不确定的地方」如实写明。
3. **诚实标注阅读范围**：`reading_scope` 严格如实填写 `full_text` / `textbook_chapter` / `guideline` / `abstract_only` / `local_note`。
4. **不要替不同教材强行调和矛盾**：如果不同权威教材对同一阈值有差异（例如体表 RP 90 ms vs 腔内 VA 70 ms，或某些学者用 VA ≤ 70 ms 另一些研究取 60 ms），如实写入 `uncertainties` 或做对照说明。

---

## 五、800×480 硬字数预算与屏幕分层

墨水屏（800×480）为保证中文汉字清晰不糊笔（字号 ≥ 15–16 px），必须严格遵守以下**字符上限**（按中文字符+英文/数字/标点总字符数计算，**绝不可超限**）：

| JSON 字段 (`content.zh.*`) | 硬上限 | 说明 |
| :--- | :---: | :--- |
| `kicker` | `≤ 10` 字符 | 顶部短分类标签 |
| `title` | `≤ 14` 字符 | 主标题（尽量 1 行放得下） |
| `core_insight` | `≤ 38` 字符 | 一句话点透核心机制或临床顿悟 |
| `bullets` | `2–3` 条 | 每条 `label ≤ 6` 字符，`text ≤ 28` 字符 |
| `key_metrics` | `0–3` 个 | `name ≤ 14`、`value ≤ 18` 字符 |
| `pearl_or_pitfall.text` | `≤ 36` 字符 | `kind` 取 `"pearl"`（记忆锚点）或 `"pitfall"`（常见误区） |
| `quadrant_summary` | `≤ 22` 字符 | 1/4 屏极简模式专用一句话 |
| `expanded.clinical_context` | `≤ 75` 字符 | **仅 10.3" TRMNL X 屏显示**的进阶临床背景 |
| `expanded.mini_table` | `≤ 3列 × 4行` | 可选；**仅 TRMNL X 显示**的对比小表（表头≤16，单元格≤24） |
| `expanded.reference_note` | `≤ 60` 字符 | 仅 TRMNL X 底栏显示的精简文献出处 |

> **语言策略**：本轮请将全部精力放在 `content.zh` 的医学精度、文字精炼度与字数达标上，**本批 JSON 中暂不生成 `content.en`**（等中文审核定稿后再统一精译）。

---

## 六、版式选择与“简笔画 / 矢量图”配图蓝图规格

请为每张卡片设计清晰的配图规格，供后续用**代码生成矢量 SVG** 或 **极简轮廓简笔画（黑白线条 + 四色墨水点缀）** 制作：

1. **版式与图幅匹配规则（`layout`）**：
   - `split_left` 或 `split_right`：适合近似方形/竖向的**解剖简笔画、折返环示意图** → `diagram_aspect_ratio` 只能选 `square_1_1`、`portrait_4_5` 或 `landscape_4_3`。
   - `top_banner`：适合宽幅**体表心电图 / 腔内电图 / 梯形图** → `diagram_aspect_ratio` 只能选 `wide_2_1`、`ultrawide_3_1` 或 `landscape_4_3`。
   - `compare_two`：适合**双图机制对照** → `diagram_aspect_ratio` 只能选 `wide_2_1`、`landscape_4_3` 或 `square_1_1`。
   - `focus_concept`：仅用于少数无需大图的定量法则卡 → `diagram_aspect_ratio` 选 `none` 或 `square_1_1`。
2. **配图生产路线（`diagram.production_route`）**：
   - `code_generated_svg`：所有心电波形、腔内电图、梯形图、时序尺（确保毫秒/顺序绝对精确）；
   - `sketch_to_svg`：所有心脏解剖轮廓、Koch 三角、瓣环旁路位置简笔画；
   - `redrawn_clinical_svg`：重绘经典临床图例。
3. **语义配色与黑白兼容（`semantic_color_plan`）**：
   - 我们的插图需要**同一份 SVG 同时兼容黑白 1-bit/2-bit 墨水屏与四色（黑/白/红/黄）墨水屏**。
   - 请明确写出：`black_primary`（主轮廓/正常路径）、`red_accent`（四色屏亮红的部分，**同时必须说明在黑白屏用什么线型如粗虚线/双线箭头来区分**）、`yellow_highlight`（四色屏用黄色标出的安全靶区或关键时间带，**同时说明在黑白屏用斜线网纹或灰底替代**）。
4. **标签克制与医学核查点**：
   - `diagram.labels` **最多 8 个**，否则 800×480 画面会拥挤；
   - `medical_accuracy_checks` 写 **2–4 条**具体核查条目（例如“His 电极远端先于右室心肌记录到尖锐 H 波，HV 正常 35–55 ms”），供后续画图验收使用。

---

## 七、输出格式要求（请严格分三部分输出）

### 第一部分：人类审阅总览（Markdown）
1. 一张 24 卡汇总表：`序号 | ID | 领域 | 标题 | 核心顿悟 | 版式/图幅 | 配图路线 | 是否样板候选 | 主要证据来源`。
2. 针对被你标为 `golden_prototype_candidate: true` 的 4–6 张候选卡，额外写 2 句话说明“为什么它最适合做首轮墨水屏视觉样板”。

### 第二部分：结构化卡片 JSON（单个合法 JSON 代码块）
输出**一个**完整合法的 `json` 代码块，根结构如下（字段名与枚举值必须严格匹配）：

```json
{
  "schema_version": "1.0.0",
  "deck_id": "ep-cards-batch-01",
  "generated_at": "2026-11-24T00:00:00Z",
  "cards": [
    {
      "id": "domain-short-kebab-slug",
      "schema_version": "1.0.0",
      "category": "conduction_anatomy | basic_intervals | ep_mechanisms | svt_triage | wpw_preexcitation | pacing_maneuvers | wide_qrs_vt | ablation_safety",
      "difficulty": "intro | bridge",
      "tags": ["标签1", "标签2", "标签3"],
      "abbreviations": {
        "whitelisted": ["AVNRT", "VA"],
        "defined_in_card": []
      },
      "content": {
        "zh": {
          "kicker": "≤10字",
          "title": "≤14字",
          "core_insight": "≤38字",
          "bullets": [
            { "label": "≤6字", "text": "≤28字" },
            { "label": "≤6字", "text": "≤28字" }
          ],
          "key_metrics": [
            { "name": "≤14字", "value": "≤18字" }
          ],
          "pearl_or_pitfall": {
            "kind": "pearl | pitfall",
            "text": "≤36字"
          },
          "quadrant_summary": "≤22字",
          "expanded": {
            "clinical_context": "≤75字",
            "mini_table": {
              "headers": ["列1", "列2", "列3"],
              "rows": [["a", "b", "c"]]
            },
            "reference_note": "≤60字符"
          }
        }
      },
      "layout": {
        "preferred_template": "split_left | split_right | top_banner | compare_two | focus_concept",
        "diagram_aspect_ratio": "square_1_1 | portrait_4_5 | landscape_4_3 | wide_2_1 | ultrawide_3_1 | none",
        "text_density": "compact | balanced | rich_x_only"
      },
      "diagram": {
        "required": true,
        "kind": "ecg_egm_waveform | ladder_diagram | anatomy_sketch | reentry_circuit | comparison_pair | none",
        "production_route": "code_generated_svg | sketch_to_svg | redrawn_clinical_svg | none",
        "svg_id": "kebab-case-svg-id",
        "visual_goal": "3秒内让读者看懂的核心视觉目标",
        "must_show_elements": ["元素1", "元素2"],
        "labels": [
          { "zh": "中文标注", "en": "EN Label", "role": "primary | accent_red | highlight_yellow | muted" }
        ],
        "semantic_color_plan": {
          "black_primary": "纯黑线条部分",
          "red_accent": "四色屏红色部分 + 黑白屏线型退化方案",
          "yellow_highlight": "四色屏黄色部分 + 黑白屏灰阶/网纹退化方案"
        },
        "medical_accuracy_checks": ["核查点1", "核查点2"]
      },
      "evidence": [
        {
          "source": "作者/指南/教材名称与版次章节",
          "identifier": "doi:... 或 PMID:... 或 textbook",
          "reading_scope": "full_text | textbook_chapter | guideline | abstract_only | local_note",
          "supporting_quote": "原文关键句或已核实界值依据",
          "verified_by_human": false
        }
      ],
      "review": {
        "status": "draft",
        "golden_prototype_candidate": false,
        "uncertainties": []
      }
    }
  ]
}
```

### 第三部分：我不确定的地方与人工复核清单
集中列出本批筛选中任何存疑的界值、只能读到摘要的文献、不同教材间的表述分歧，以及需要我人工确认解剖细节的配图。

---

## 【可选：本地参考资料投喂区】
（若你准备粘贴/上传本地 `curated.json` 或 `reading_notes/*.md`，放在这里；若留空则请直接基于权威教材、指南及可检索全文作答。）
````
