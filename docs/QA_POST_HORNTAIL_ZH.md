# Post-Horntail 解锁面 QA 脚本

目标：验证 Horntail 击败后，玩家能看懂并进入下一批系统：Triwizard、St Mungo's、Forbidden Forest 后续状态、商店解锁和导航提示。

本轮只做“入口可见性 / 解锁面”QA，不测完整 Triwizard 三任务、不测 St Mungo's 完整循环，也不进入 late Hardmode Boss 数值平衡。

## 测试前提

- 使用已经完成 Horntail 的同一个测试世界。
- 如果是一次性 QA 世界，先用：

```text
/wwdebug bossflag early
/wwdebug bossflag mid
/wwdebug vanilla mech
/wwdebug kit posthorntail
```

- 每个阶段都先运行：

```text
/wwdebug posthorntail
```

## 1. 入口物品和总状态

操作：

```text
/wwdebug posthorntail
/wwdebug kit posthorntail
/wwdebug posthorntail
```

通过标准：

- `Horntail defeated` 为通过。
- Goblet of Fire、St Mungo's Pass、Forest Lantern、Boss Compass、Wizard's Almanac 都能被检测到。
- Suggested next step 指向 Triwizard 或 St Mungo's，而不是回到 Horntail。

失败记录：

- 已击败 Horntail 但 `/wwdebug posthorntail` 不承认。
- kit 给出的入口物品缺失。
- Suggested next step 和实际状态矛盾。

## 2. Triwizard 入口

操作：

- 使用 Goblet of Fire。
- 再运行：

```text
/wwdebug posthorntail
```

通过标准：

- 聊天出现 Triwizard 解锁/选中冠军/第一项任务提示。
- `Tournament unlocked` 为通过。
- `currentTask` 应进入 1。
- `can start next` 应为 yes，或使用 Goblet 后进入 task active。

失败记录：

- Horntail 已击败但 Goblet 只给 buff，没有解锁 Triwizard。
- 解锁文本缺失或误导。
- `/wwdebug posthorntail` 中 tournament 状态不更新。

## 3. St Mungo's 入口

操作：

- 使用 St Mungo's Pass。
- 再运行：

```text
/wwdebug posthorntail
```

通过标准：

- 聊天出现 St Mungo's 解锁文本。
- `Hospital unlocked / Healer can move in` 为通过。
- Healer 具备入住资格；不要求马上自然入住。

失败记录：

- Horntail 已击败但 pass 不解锁医院。
- 解锁后 Healer 条件仍为 false。
- pass 反馈只显示状态文本，没有解释下一步。

## 4. Forest 与商店解锁面

操作：

- 使用 Forest Lantern。
- 查看 `/wwdebug posthorntail` 中 forest/shop 部分。

通过标准：

- Forest expedition 至少能解锁；是否立即 start 取决于夜晚和 Forbidden Forest biome。
- Hagrid post-Horntail items 显示 DragonScaleRing yes、BeastHuntersCharm yes。
- Potions Master post-Horntail item 显示 DraconisElixir yes。
- Boss Compass 的下一 Boss 方向应是 Umbridge。

失败记录：

- Forest Lantern、Hagrid、Potions Master、Boss Compass 的提示互相矛盾。
- post-Horntail shop gate 显示 yes 但实店不出现。
- Boss Compass 仍指向 Horntail。

## 停止条件

遇到以下情况直接停：

- `/wwdebug posthorntail` 与实际物品/系统状态矛盾。
- Goblet 或 St Mungo's Pass 在 Horntail 后无法解锁对应系统。
- 解锁后 Save & Exit 重开丢失状态。
- 文本让玩家不知道下一步该做什么。

## 2026-06-29 实测收口

状态：已完成。

已通过项目：

- `/wwdebug posthorntail` 正确识别 Horntail 后状态，Boss Compass / Wizard's Almanac 都可见，下一 Boss 指向 Umbridge。
- Goblet of Fire 可解锁 Triwizard，并可启动 Task 1。
- Golden Egg 可完成 Triwizard Task 1，任务提示和完成文本正常。
- St Mungo's Pass 可解锁医院，并可启动 first triage mission。
- Spell Damage Ward triage 可生成 3 个节点，击破 3/3 后完成，完成文本正常。
- Forest Lantern 可解锁 Forbidden Forest expedition 入口；完整森林任务留到后续阶段，不纳入本轮收口。
- post-Horntail 商店/导航面没有再指回 Horntail。

本轮发现并已修复：

- Triwizard / St Mungo's / Forest 系统文本 raw key 兜底。
- Goblet of Fire `UseMessage` raw key 兜底。
- Triwizard Task 1 无法从 `currentTask=1` 启动的问题。
- Golden Egg 只能靠拾取完成 Task 1 的不自然 QA 路径；现在 Task 1 active 时可直接使用。
- Death Eater Invasion 在 St Mungo's 限时任务中随机插入的问题；限时任务 active 时不再随机启动。
- Daily Challenge 把 St Mungo's ward nodes 当作普通击杀计数的问题。
- Daily Challenge / Death Eater Invasion / Golden Snitch event 文本 raw key 兜底。
- `/wwdebug posthorntail` 的 Suggested next step 会根据 Task 1 / triage 完成状态更新。

收口结论：

- Post-Horntail thin-slice QA 已完成。
- 下一阶段可以讨论 Umbridge 入口、late-hardmode pacing、以及是否只做最小可上线闭环。
