# C2 · AI for Math — 从自然语言到可验证推理

本仓库是 C2「AI for Math」论文挑战的交付物。论文提出一个**三层架构**：在自然语言生成与形式化证明器之间插入一层**语义规约层（Typed IR）**，把数学陈述先「编译」为可校验的中间表示，再送入证明器，从而提升 LLM 数学推理的可靠性。

## 目录结构

```
C2_AI4Math/
├── paper/
│   ├── paper.tex            # 论文主源文件（9 节，沿用老师大纲）
│   ├── references.bib       # 14 篇一手文献
│   ├── 文献检索记录.md        # 文献检索与逐条核验记录
│   ├── 文献核验表.md          # 作者/标题/出处/链接 独立核验表
│   ├── validate_tex.py      # 编译前自检脚本
│   └── paper.pdf            # 编译产物
├── tools/
│   ├── tectonic.exe         # 独立 LaTeX 编译引擎（无需安装 TeXLive）
│   └── tectonic.zip         # 同上的压缩包
├── AI日志.md                 # AI 协作日志（prompt / 输出 / 校验证据）
├── AAR复盘.md                # 七维 AAR 复盘
└── 挑战_C2 AI for Math 论文_8ot0ji_材料/   # 题目与材料
```

## 依赖

- **编译引擎**：`tools/tectonic.exe`（自包含，首次编译需联网自动下载宏包；之后可离线）。
- **运行自检脚本**：Python 3（标准库即可，无需第三方包）。
- 无需安装 TeXLive / MiKTeX。

## 编译步骤

在仓库根目录执行（Windows PowerShell）：

```powershell
# 一键编译（tectonic 会自动跑完 bibtex/多轮排版，输出 paper/paper.pdf）
& ".\tools\tectonic.exe" ".\paper\paper.tex"
```

若使用系统自带的 TeXLive，等价命令为：

```bash
cd paper
pdflatex paper && bibtex paper && pdflatex paper && pdflatex paper
```

> 论文使用 `natbib`（`\bibliographystyle{plainnat}` + `\bibliography{references}`），
> 引用全部来自 `paper/references.bib`，共 14 篇一手文献。

## 编译前自检

提交/发布前先跑一遍自检脚本，核对环境配对、引用 key、label/ref：

```powershell
python ".\paper\validate_tex.py"
```

正常输出应满足：`begin/end` 全部配对、无「引用但 bib 缺失」的 key、无「ref 无对应 label」、`$` 数学模式数量为偶数。

## 复现路径

1. 阅读 `paper/paper.tex` 的三层架构与语义规约层（Typed IR）定义。
2. 用 `tectonic` 编译得到 `paper.pdf`。
3. 对照 `paper/文献核验表.md` 核验每篇引用是否真实可溯源。
4. 查看 `AI日志.md` 了解 AI 参与过程与校验证据，`AAR复盘.md` 了解复盘结论。
