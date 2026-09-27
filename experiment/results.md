# 最小可行实验结果（自动生成，可复现）

运行命令：`python experiment/minimal_experiment.py`

| 指标 | 定义 | 数值 |
|---|---|---|
| 样例总数 | 手工构造玩具数学陈述 | 24 |
| 类型检查通过率（autoformalization/type-check rate） | 通过 L2 类型门的比例 | 18/24 = 75.0% |
| 归约成功率（proof/reduction rate） | 类型正确且前置条件满足的比例 | 12/24 = 50.0% |
| 最终接受率（acceptance rate） | 类型正确、可归约、且与题意一致的样例比例 | 6/24 = 25.0% |

## 失败案例分布

| 失败类型 | 数量 | 说明 |
|---|---|---|
| 类型错误（TYPE_ERROR） | 6 | 操作作用于错误 sort，被类型门拒绝 |
| 前置条件违反（PRECONDITION_VIOLATION） | 6 | 除零 / 自然数下溢，归约时拒绝 |
| 规约漂移（SPEC_DRIFT） | 6 | 类型正确但与题意不符，被一致性检查捕获 |
| 接受（ACCEPT） | 6 | 类型正确、可归约、与题意一致 |

## 消融：类型门 + 一致性检查的收益

| 策略 | 接受数 | 正确数 | 精确率 |
|---|---|---|---|
| 全信（无门，接受所有候选 IR） | 24 | 6 | 25.0% |
| 加门（类型门 + 一致性检查） | 6 | 6 | 100.0% |

> 结论：类型门 + 一致性检查把「接受的答案全对」的精确率从 25.0% 提升到 100.0%，同时拒绝 18/24 条不安全候选，验证了论文核心主张——把信任建立在「可检查的 IR」上而非「模型听起来对不对」。

## 逐条明细

| ID | 自然语言陈述 | 类别 | 结果 | 详情 |
|---|---|---|---|---|
| S01 | 3 个苹果加 4 个苹果，共多少个？ | clean | ACCEPT | value=7 |
| S02 | 7 减 2 等于多少？ | clean | ACCEPT | value=5 |
| S03 | 3 乘 5 是多少？ | clean | ACCEPT | value=15 |
| S04 | 判断：5 是否大于 3？ | clean | ACCEPT | value=True |
| S05 | 实数 6.0 除以 3.0？ | clean | ACCEPT | value=2.0 |
| S06 | 判断：2 加 2 是否等于 4？ | clean | ACCEPT | value=True |
| S07 | 苹果数是否大于‘是’？ | type_error | TYPE_ERROR | gt applied to ('Nat', 'Bool'): no matching signature |
| S08 | 3 加上‘是’？ | type_error | TYPE_ERROR | add applied to ('Nat', 'Bool'): no matching signature |
| S09 | 非 5？ | type_error | TYPE_ERROR | not applied to ('Nat',): no matching signature |
| S10 | 5 且 3？ | type_error | TYPE_ERROR | and applied to ('Nat', 'Nat'): no matching signature |
| S11 | 7.0 除以‘否’？ | type_error | TYPE_ERROR | div applied to ('Real', 'Bool'): no matching signature |
| S12 | ‘是’减去 2？ | type_error | TYPE_ERROR | sub applied to ('Bool', 'Nat'): no matching signature |
| S13 | 5 个苹果，吃掉 7 个，还剩几个？ | precondition | PRECONDITION_VIOLATION | sub[5, 7] violates precondition |
| S14 | 实数 1.0 除以 0.0？ | precondition | PRECONDITION_VIOLATION | div[1.0, 0.0] violates precondition |
| S15 | 2 减 3（自然数）？ | precondition | PRECONDITION_VIOLATION | sub[2, 3] violates precondition |
| S16 | 0 个苹果，拿走 1 个？ | precondition | PRECONDITION_VIOLATION | sub[0, 1] violates precondition |
| S17 | 5.0 除以 0.0？ | precondition | PRECONDITION_VIOLATION | div[5.0, 0.0] violates precondition |
| S18 | 3 减 9（自然数）？ | precondition | PRECONDITION_VIOLATION | sub[3, 9] violates precondition |
| S19 | 3 个苹果加 4 个苹果，共多少个？ | drift | SPEC_DRIFT | IR=12 vs ground_truth=7 |
| S20 | 7 减 2 等于多少？ | drift | SPEC_DRIFT | IR=9 vs ground_truth=5 |
| S21 | 判断：5 是否大于 3？ | drift | SPEC_DRIFT | IR=False vs ground_truth=True |
| S22 | 3 乘 5 是多少？ | drift | SPEC_DRIFT | IR=8 vs ground_truth=15 |
| S23 | 6.0 除以 3.0？ | drift | SPEC_DRIFT | IR=18.0 vs ground_truth=2.0 |
| S24 | 2 加 2 是否等于 4？ | drift | SPEC_DRIFT | IR=False vs ground_truth=True |