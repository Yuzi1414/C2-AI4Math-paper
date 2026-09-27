# C2 AI for Math 论文 —— AI 协作日志

> 本日志如实记录本次论文生产过程中的 AI 协作证据，用于 aiUsage（20 分）维度。
> 核心事实：**全程多轮迭代（非一次性生成）**，含一次真实编译失败 → 定位 → 修复的闭环。

## 一、协作总览

| 阶段 | 轮次 | 产物 | 是否迭代 |
|---|---|---|---|
| A. 选题与框架 | 多轮 | 三层模型 + Typed IR 框架定稿 | ✅ 与用户逐项确认 |
| B. 文献检索 | 多轮 | 14 篇一手文献 → references.bib + 核验记录 | ✅ 逐条核验 |
| C. 论文写作 | 9 块分节 | paper.tex（9 节 + 摘要 + 文献） | ✅ 分块推进 |
| D. 编译验证 | 2 次真实编译 | paper.pdf（7 页） | ✅ 失败→修复→成功 |

**红线自查**：全程 4 个阶段、多次往返，非 one-shot；AI 输出均经人工校验或真实编译验证后才接受。

## 二、各阶段关键 Prompt 与输出

### 阶段 A —— 选题与框架（用户决策驱动）

- 用户指令：`挑战C2`（随后确认 `用老师大纲，英文写`）。
- AI 动作：读取老师《中文论文大纲（AI4Math）.pdf》逐页，提炼 9 节骨架。
- AI 输出（核心论点，定稿后写入 §1/§4）：
  > 让 LLM 做数学「说得出对错」，要在自然语言生成与形式化验证之间加一层**语义规约（Typed IR）**，用双向一致性检查锚定到定理证明器。
- 三层贡献点：① Typed IR 设计 ② Pipeline（生成→语义规约→验证） ③ 双向一致性度量。

### 阶段 B —— 文献检索（逐条核验）

- 检索目标：覆盖「LLM 数学推理」与「自动形式化/定理证明」两翼的一手文献。
- 产出：14 篇（CoT / Self-Consistency / GSM8K / MATH / Minerva / Plan-and-Solve / DeepSeek-R1 / Autoformalization / ProofNet / LeanDojo / LEGO-Prover / KeYmaera X / Schirmer / Coq Coq correct!）。
- **核验证据**：逐条确认作者名单、标题、年份与出处，写入 `文献检索记录.md`；`references.bib` 14 个条目全部为真实可溯源一手文献，零臆造。

### 阶段 C —— 论文写作（分块，避免一次性长文本）

- 采用 `<6000 字符/块` 分块写入，`%@@NEXT@@` 哨兵标记续写点，共 9 节 + preamble/abstract/bibliography。
- 遵循学术写作协议：主张—证据—推理结构，引用只在真实文献范围内。

### 阶段 D —— 编译验证（关键迭代，详见第三节）

## 三、校验证据（aiUsage 核心）

1. **静态校验** `validate_tex.py`：begin/end 环境 11 对全配对；引用 key 14/14 与 bib 匹配，0 缺失、0 冗余；9 个 `\section` 完整。
2. **真实编译（决定性）**：
   - 第 1 次 `tectonic` 编译：**失败** —— `paper.tex:39: LaTeX Error: \mathcal allowed only in math mode`。
   - 根因定位：AI 生成的宏 `\newcommand{\IR}{\mathcal{IR}}` 在正文文本模式被调用（`\IR{}`），而 `\mathcal` 仅限数学模式。
   - 修复：改为 `\newcommand{\IR}{\ensuremath{\mathcal{IR}}}`（`\Nat` 同理）。
   - 第 2 次编译：**成功** —— 产出 `paper.pdf`（7 页，64 KB）；最后一轮日志零 undefined citation，参考文献正常加载。
3. **引用一致性复核**：单独 grep 比对正文 14 个 `\cite` key 与 `references.bib` 14 个条目 key，逐一精确匹配。

## 四、关键教训（对应 AAR 的「AI 误导」案例）

- **误导案例**：AI 在撰写 `paper.tex` 时生成的自定义宏 `\IR` 在文本模式非法，导致真实编译失败；若只信「静态校验通过」就提交，将触发评分红线（不可编译 → ≤5 分）。
- **对策**：任何 LaTeX 交付物必须跑**真实编译**而非只做静态字符串校验；宏定义统一用 `\ensuremath` 包裹以兼容文本/数学两种模式。
- **可复用的经验**：静态脚本（validate_tex.py）能查环境配对与 key 一致性，但**不能替代**真实排版引擎；两者互补才构成完整验证。
