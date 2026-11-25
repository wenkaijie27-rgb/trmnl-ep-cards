# 心脏电生理墨水屏知识卡片 — 进阶组（Advanced Tier）GPT 文献筛选 Prompt

## 如何使用本 Prompt

本 Prompt 用于生产 **进阶组（`tier: "advanced"`）24 张卡片**，与首批 **基础组（`tier: "basic"`）** 严格区分：
- **基础组**面向刚入门医学生（Koch 三角、AH/HV、典型短 VA、顺逆向 AVRT 等）；
- **进阶组**面向**已有入门基础、进入导管室跟台或独立判读腔内电图的医学生/电生理初学者**，聚焦“实操陷阱、定量差值、非典型变异与特殊解剖”。

运行后将 JSON 保存至 `decks/advanced-24-draft.json`，跑 `python3 tools/validate_cards.py decks/advanced-24-draft.json` 校验即可合并进双层卡组。

---

## 复制下方 Prompt 发给 GPT

````markdown
# 任务：为「心脏电生理墨水屏知识卡片·进阶组」筛选文献并生成 24 张卡片初稿

你正在协助开源 **TRMNL 墨水屏插件项目** 制作 **进阶组（`tier: "advanced"`）** 心脏电生理知识卡片。基础组（`basic`）已经覆盖了 Koch 三角、AH/HV、折返三要素、典型 AVNRT 短 VA、顺逆向 AVRT 等入门概念——**请勿重复基础组选题**。

---

## 一、受众与 8 大主题域选题（共 24 张，每域 3 张）

- **目标受众**：已掌握基础腔内间期与常规室上速机制、正在深入导管室鉴别与标测的**高年级医学生 / 青年电生理医师**。
- **核心原则（一卡一实操直觉）**：仍然遵循 800×480 极简可读原则，不写长篇综述，但内容必须给出“上台能用的边界条件或常见陷阱”。
- **8 个主题域 × 3 卡**：
  1. `conduction_anatomy`：下移锥室（Infero-septal recess）与心室基底部邻近关系、冠状窦肌袖与 Marshall 韧带静脉的房性传导连接、左束支三分支分布与消融区毗邻。
  2. `basic_intervals`：体表 RP 90 ms 与腔内 VA 70 ms 为何不等同、近端与远端 His 记录混入右束支电位导致假短 HV、CS 电极插入过深导致近远端看似“同步”的假象。
  3. `ep_mechanisms`：房室结快慢径逆传恢复曲线与非典型 AVNRT（快-慢/慢-慢）机制、动作电位时程与激动时间的心脏电记忆（Cardiac Memory）直觉、慢传导旁路（递减性逆传）与普通旁路的本质差异。
  4. `svt_triage`：非典型 AVNRT 与间隔旁路 AVRT 的鉴别要点、长 RP 心动过速三兄弟（AT vs 非典型 AVNRT vs 慢传导旁路）初筛、交界性心动过速（JT）如何伪装成典型/非典型 AVNRT。
  5. `wpw_preexcitation`：Mahaim（房室结室/束室）旁路特征（仅慢前传、左束支阻滞型宽波、无逆传）、多旁路或间歇性预激的风险提示、无症状预激高危电生理分层（诱发 AF 时最短预激 RR < 250 ms 或旁路 ERP < 240 ms）。
  6. `pacing_maneuvers`：心室拖带起搏后间期差值（`PPI-TCL`）需扣除房室结递减延长的校正原理、单次拖带 vs 差值拖带（右室基底部 vs 心尖部）逻辑、旁 His 起搏在左侧游离壁旁路或近端右束支阻滞时的失效场景。
  7. `wide_qrs_vt`：室上速伴功能性束支阻滞（Ashman 现象与初始几跳差传）vs 室速、流出道室早/室速（V1–V3 移行点与左/右室流出道鉴别直觉）、乳头肌或分支性室速的基础形态线索。
  8. `ablation_safety`：交界区/前间隔旁路消融时希氏束电位损伤预警与冷冻消融权衡、冠状窦内或心大静脉远端消融邻近冠状动脉的解剖安全距离意识、消融后残余双径路“跳跃”与单个回波允许存在但无持续折返的急性终点意义。

---

## 二、缩写白名单与新缩写规范

**通用白名单（免定义）**：
`AVNRT`, `AVRT`, `AT`, `SVT`, `WPW`, `ECG`, `AH`, `HV`, `VA`, `RP`, `PR`, `QRS`, `ERP`, `CS`, `His`, `PVC`, `PAC`, `RBBB`, `LBBB`, `VT`, `AF`, `SA`, `AVN`

**进阶组专属规则**：
- 若卡片核心主题需要引入 `PPI`、`TCL`、`PJRT`、`JT`、`RVOT`、`LVOT`、`SPERRI` 等进阶缩写，**每张卡最多引入 2 个**，必须在 `abbreviations.defined_in_card` 中给出准确中英文全称，并在正文首次出现时用简短括号释义；非本卡主角的术语一律写中文。

---

## 三、字数预算、字段与配图硬规范

1. **JSON 结构与基础组完全一致**，每张卡强制写入：
   - `"tier": "advanced"`
   - `"difficulty": "bridge"`（核心实操桥接）或 `"intro"`
   - 若 `layout.preferred_template` 为 `split_left` 或 `split_right`，**必须填写 `content.zh.split_note`（≤ 34 字）**，填补 800×480 右侧/左侧纵栏的呼吸区并给出核心临床动作或解剖提醒。
2. **字数硬上限（绝不超限）**：
   - `kicker ≤ 10`，`title ≤ 14`，`core_insight ≤ 38`，`bullets`（2–3 条，`label ≤ 6`，`text ≤ 28`），`key_metrics`（0–3 个），`pearl_or_pitfall.text ≤ 36`，`quadrant_summary ≤ 22`，`split_note ≤ 34`（split 版式必写），`expanded.clinical_context ≤ 75`，`expanded.reference_note ≤ 60`。
3. **医学严谨性**：每条数值与阈值必须附 `evidence`（书名版次章节或 DOI/PMID、如实标注 `reading_scope`、`supporting_quote`），不确定或存疑处写入 `review.uncertainties` 与第三部分人工复核清单。
4. **版式与配图蓝图**：
   - 波形/梯形图/拖带时序图优先 `code_generated_svg` + `top_banner` / `compare_two`；
   - 解剖图优先 `sketch_to_svg` + `split_left` / `split_right`；
   - 明确 `semantic_color_plan`（黑主线 + 红/粗虚线强调 + 黄/斜线网纹高亮）与 `medical_accuracy_checks`（2–4 条）。

---

## 四、三部分输出格式

1. **第一部分**：24 卡总览表 + 3–5 张最具代表性进阶卡推荐；
2. **第二部分**：单个合法 JSON 代码块（`deck_id: "ep-cards-advanced-24-draft"`，含 `"tier": "advanced"`）；
3. **第三部分**：「我不确定的地方与人工复核清单」。
````
