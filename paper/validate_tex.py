import re, pathlib
from collections import Counter

base = pathlib.Path(r"D:\.cogseed\userWorkSpace\我的挑战有哪些\C2_AI4Math\paper")
tex = (base / "paper.tex").read_text(encoding="utf-8")
bib = (base / "references.bib").read_text(encoding="utf-8")

print("=== 1. 环境配对 (begin/end) ===")
begins = re.findall(r"\\begin\{([^}]+)\}", tex)
ends = re.findall(r"\\end\{([^}]+)\}", tex)
cb, ce = Counter(begins), Counter(ends)
mismatch = []
for k in sorted(set(cb) | set(ce)):
    if cb[k] != ce[k]:
        mismatch.append((k, cb[k], ce[k]))
print("begin 环境数:", len(begins), "| end 环境数:", len(ends))
print("配对不一致:", mismatch if mismatch else "无 (全部配对)")

print("\n=== 2. 引用 key 核对 ===")
cite_keys = set()
for m in re.finditer(r"\\cite[pt]?(?:\[[^\]]*\])?\{([^}]+)\}", tex):
    for k in m.group(1).split(","):
        k = k.strip()
        if k:
            cite_keys.add(k)
bib_keys = set(re.findall(r"@\w+\{([^,]+),", bib))
print("论文引用 key 数:", len(cite_keys), "| bib 条目数:", len(bib_keys))
print("引用但 bib 缺失 (会导致 ? 未解析):", sorted(cite_keys - bib_keys))
print("bib 有但正文未引用:", sorted(bib_keys - cite_keys))

print("\n=== 3. label/ref 核对 ===")
labels = set(re.findall(r"\\label\{([^}]+)\}", tex))
refs = set(re.findall(r"\\ref\{([^}]+)\}", tex))
print("labels:", sorted(labels))
print("refs:", sorted(refs))
print("ref 无对应 label:", sorted(refs - labels))
print("label 未被引用:", sorted(labels - refs))

print("\n=== 4. 结构完整性 ===")
print("有 \\begin{document}:", "\\begin{document}" in tex)
print("有 \\end{document}:", "\\end{document}" in tex)
print("有 \\bibliography{references}:", "\\bibliography{references}" in tex)
print("有 \\bibliographystyle{plainnat}:", "\\bibliographystyle{plainnat}" in tex)
print("章节数 (\\section):", len(re.findall(r"\\section\{", tex)))
print("未闭合 $ 数学模式 (奇数个 $ 为异常):", tex.count("$") % 2 != 0)
