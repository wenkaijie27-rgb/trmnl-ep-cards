# EP Knowledge Cards — 数据规范与多屏适配契约（v1.0.0）

> 本文档定义「心脏电生理墨水屏知识卡片」的唯一数据源契约（[card.schema.json](file:///Users/wenkaijie/Documents/Trmnl/ep-cards/schema/card.schema.json)），同时服务于：
> 1. **自托管 BYOS（Terminus + TRMNL Custom Serve）**
> 2. **官方 TRMNL Cloud Recipe（`trmnlp`）与 GitHub 开源静态数据端**
> 3. **多尺寸/多灰阶/多色墨水屏**：7.5" `800×480`（1-bit / 2-bit）、10.3" **TRMNL X** `1040×780`（4-bit）、**4 色 BWRY** 与 **6 色 Spectra 6**。

---

## 1. 设计目标与核心原则

1. **受众定位**：刚进入心脏电生理（EP）领域的医学生——具备基础内科学与常规体表 ECG 知识，正在建立腔内电图、传导解剖、折返机制与起搏推理直觉。
2. **一卡一顿悟（One-Insight Card）**：每张卡只解决一个核心机制或临床困惑，不做百科词条式堆砌，也不深陷罕见特例与生僻缩写。
3. **单一真相源（Single Source of Truth）**：所有文案、排版提示、配图蓝图与文献证据均固化于 JSON；HTML/Liquid 模板只负责按屏幕能力做响应式裁剪与语义染色，不硬编码医学内容。
4. **中文可读性红线**：在 `800×480` 屏上，汉字正文坚持 `≥ 15–16 px`（`Inter Variable` + `Noto Sans CJK SC` 混排，字重 `500` 防细笔画二值化断笔），因此用**严格字数预算**倒逼内容精炼，而不是靠缩小字号硬塞。

---

## 2. 完整字段字典与字数预算表

### 2.1 顶层 Deck 包装与卡片元数据

| 字段 | 类型 / 枚举 | 说明 |
| :--- | :--- | :--- |
| `schema_version` | 常量 `"1.0.0"` | Schema 版本号 |
| `deck_id` | kebab-case 字符串 | 卡组标识，如 `ep-cards-batch-01` |
| `generated_at` | ISO 8601 date-time | 生成时间 |
| `id` | kebab-case 字符串 | 卡片唯一 ID，如 `svt-typical-avnrt-short-va` |
| `category` | 8 个领域枚举 | `conduction_anatomy` / `basic_intervals` / `ep_mechanisms` / `svt_triage` / `wpw_preexcitation` / `pacing_maneuvers` / `wide_qrs_vt` / `ablation_safety` |
| `difficulty` | `intro` \| `bridge` | 首批 MVP 聚焦 `intro`（入门必懂），少量核心桥接为 `bridge` |
| `tier` | `basic` \| `advanced`（可选，默认 `basic`） | 卡组层级：**基础组（`basic`）** 面向入门医学生；**进阶组（`advanced`）** 面向导管室进阶实操与高阶鉴别 |
| `tags` | `string[2..5]` | 2–5 个短标签 |

### 2.2 本地化内容与字数预算（`content.zh` / `content.en`）

> `content.zh` 为必填；`content.en` 为可选（初筛阶段可先留空以把模型注意力集中在中文精确度，定稿后统一补齐英文以支持国际开源用户）。

| 字段 | 中文上限 | 英文上限 | 排版角色与屏显去向 |
| :--- | :---: | :---: | :--- |
| `kicker` | `≤ 10` 字 | `≤ 24` chars | 顶部眉标（如「室上速鉴别」） |
| `title` | `≤ 14` 字 | `≤ 36` chars | 卡片主标题（单行/至多两行高对比标题） |
| `core_insight` | `≤ 38` 字 | `≤ 95` chars | 粗体/底纹核心结论条：读完这一句即掌握本卡主旨 |
| `bullets` | `2–3` 条；`label ≤ 6` 字，`text ≤ 28` 字 | `label ≤ 16`，`text ≤ 72` | 机制分点说明；`800×480` 半屏视图可仅取前 2 条 |
| `key_metrics` | `0–3` 个；`name ≤ 14`，`value ≤ 18` | `name ≤ 22`，`value ≤ 24` | 紧凑数值胶囊（如 `腔内VA界值: ≤ 70 ms`） |
| `pearl_or_pitfall` | `kind`: `pearl`\|`pitfall`；`text ≤ 36` 字 | `≤ 90` chars | 底部记忆锚点或常见临床误区提示 |
| `quadrant_summary` | `≤ 22` 字 | `≤ 55` chars | 1/4 屏 Mashup 视图专用极简摘要 |
| `split_note` | `≤ 34` 字（可选） | `≤ 85` chars | 仅用于 `split_left` / `split_right` 填补右侧纵向呼吸区，给出定位或临床锚点 |
| `expanded.clinical_context` | `≤ 75` 字 | `≤ 180` chars | **仅 TRMNL X（`lg:` `1040×780`）** 解锁的进阶临床背景 |
| `expanded.mini_table` | 最多 `3` 列 × `4` 行 | 同左 | **仅 TRMNL X（`lg:`）** 展示的对照小表 |
| `expanded.reference_note` | `≤ 60` 字符 | `≤ 60` chars | **仅 TRMNL X（`lg:`）** 底栏精简文献出处 |

---

## 3. 版式路由矩阵（`layout` × `diagram`）

模板引擎依据 `layout.preferred_template` 与 `layout.diagram_aspect_ratio` 自动分配画面比例，保证“图看清、字不挤、面不空”：

| `preferred_template` | 适用 `diagram_aspect_ratio` | 适用内容特征 | `800×480` 空间分配 |
| :--- | :--- | :--- | :--- |
| `split_left` / `split_right` | `square_1_1`、`portrait_4_5`、`landscape_4_3` | 解剖简笔画、Koch 三角、折返环示意图 | 图占一侧 `42%–46%` 宽度，文字占另一侧 |
| `top_banner` | `wide_2_1`、`ultrawide_3_1`、`landscape_4_3` | ECG / 腔内电图、梯形图、连续激动时序 | 上方全宽占高 `46%–52%`，下方文字双栏排布 |
| `compare_two` | `wide_2_1`、`landscape_4_3`、`square_1_1` | 机制两两对照（如 AVNRT vs AVRT、显性 vs 隐匿旁路） | 左右对称双子图 + 底部对照结论 |
| `focus_concept` | `none`、`square_1_1` | 纯概念/定量法则记忆卡（可配小矢量徽标） | 居中大结论区 + 要点卡片网格 |

> 校验脚本 `validate_cards.py` 会主动拦截不兼容的组合（例如 `top_banner` 配 `portrait_4_5` 或 `required: true` 却设 `none`）。

---

## 4. 多墨水屏与四色屏语义配色契约

为了确保同一套内联 SVG 在 **1-bit 黑白**、**2-bit 四灰阶**、**4-bit TRMNL X（16 灰阶）**、**4 色 BWRY（黑/白/红/黄）** 和 **6 色 Spectra 6** 上都清晰锐利、绝不糊成一团灰，强制遵循两项工程原则：

1. **禁止写死物理颜色，统一使用语义角色（`role`）**：
   - `primary`（对应 `semantic_color_plan.black_primary`）：主解剖轮廓、基线、正常传导路径、QRS/H/V 主波 → 映射为纯黑实线。
   - `accent_red`（对应 `semantic_color_plan.red_accent`）：异常折返环、旁路、逆行激动箭头、危险阈值 → 在 `screen--color-4bwry` / `screen--color-6a` 上高亮为**红色**；在黑白屏退化为**粗虚线 / 双线箭头 / 加粗轮廓**。
   - `highlight_yellow`（对应 `semantic_color_plan.yellow_highlight`）：安全消融靶区、关键时间窗带（如 `VA ≤ 70 ms`） → 在多色屏上使用**黄色**；在黑白与 4-bit 灰阶屏上退化为**斜线网纹或浅灰底带**。
   - `muted`：辅助参照线与次要刻度。
2. **绝不单靠颜色区分医学含义**：即便把四色图转成纯 1-bit 黑白，读者也必须能通过**线型（实线/虚线/双线）、箭头方向与底纹**独立看懂。
3. **三类配图生产路线（`production_route`）**：
   - `code_generated_svg`：波形、腔内电图、梯形图、折返环等时序图——**必须用脚本参数化生成**，严禁用文生图 AI 直接绘制波形。
   - `sketch_to_svg`：心脏解剖简笔画（类似简洁轮廓插画风格）——可先生成极简线稿再矢量化精修，标注图层独立叠加并经过解剖核验。
   - `redrawn_clinical_svg`：源于经典教材或临床图例的**原创重绘矢量图**，既消除彩色抖动噪点，也避免开源版权争议。

---

## 5. 缩写白名单与编辑红线

为防止医学生被缩写墙劝退，除以下 **23 个电生理入门通用缩写**外，其余英文缩写禁止未经解释直接出现在正文或图注中：

```text
AVNRT, AVRT, AT, SVT, WPW, ECG,
AH, HV, VA, RP, PR, QRS, ERP,
CS, His, PVC, PAC, RBBB, LBBB, VT, AF, SA, AVN
```

- **白名单外缩写处理规则**：
  1. 若该术语**不是**本卡片的教学主角：一律写中文全称（如写「起搏后间期差值」而非孤立写 `PPI-TCL`；写「永久性交界区反复性心动过速」或干脆在入门卡中避免引入）。
  2. 若该术语**就是**本卡片要教的核心概念：必须写入 `abbreviations.defined_in_card`（每卡最多 2 个），并在正文首次出现时用简短括号给出中文释义。
- **导联与单位豁免**：常规心电导联（如 `V1`–`V6`、`I`、`II`、`III`、`aVR`、`aVL`、`aVF`）与物理单位（`ms`、`mV`、`bpm`、`mm`）可直接使用。

---

## 6. 证据分级与审核状态流转

每张卡片至少包含 1 条 `evidence`：
- **来源优先级**：① 经典电生理教材章节（Josephson 6e、Issa 3e、Ho & Ernst 解剖、Zipes 7e、郭继鸿等）与国际权威指南（ACC/AHA/HRS、ESC）；② 用户本地 `curated.json` / `reading_notes` 已核验文献；③ PubMed/DOI 可核对的综述或临床研究。
- **状态流转**：
  - `draft`：GPT 初筛产出，`verified_by_human: false`；
  - （执行 `python3 tools/validate_cards.py` 通过结构、字数、缩写与版式校验）
  - `audited`：经人工/辅助核验文献出处、医学阈值与配图检查点无误；
  - `approved`：配图 SVG 已生成并实机预览通过，可发布到卡组。
