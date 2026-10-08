# Voldemort Readiness / Final Boss QA

目标：验证 Dementor King 后的最终战入口是否闭合：Horcrux / Battle of Hogwarts / Nagini 准备链、Lunatic Cultist 与夜晚 gate、Dark Mark 召唤物、Boss Compass / Wizard's Almanac / Horcrux Tracker 指引、Voldemort 召唤与击杀 flag、以及 Save & Exit 后持久化。

本轮只测 Voldemort readiness 与最终 Boss 单点闭环，不展开 Deathly Hallows / post-Voldemort 奖励终章。

## 1. 推荐自然路线

自然流程应是：

1. 击败 Dementor King / Azkaban's Despair。
2. 摧毁四个核心 Horcrux：Riddle's Diary、Slytherin's Locket、Hufflepuff's Cup、Diadem of Ravenclaw。
3. 通过 Horcrux Tracker / Battle of Hogwarts 路线解决 Nagini。
4. 击败 Lunatic Cultist。
5. 夜晚使用 boss Dark Mark 召唤 Voldemort。

注意：`Dark Mark` 有两个相关物品：

- `VoldemortSummonItem`：boss 召唤物，显示为 Dark Mark。
- `DarkMarkSummon`：Death Eater invasion 事件物品，显示为 Dark Mark (Morsmordre)，不是 Voldemort 召唤物。

## 2. QA 快速准备

在 disposable QA world 或当前测试世界中：

```text
/wwdebug voldemort
```

如果缺少最终战测试物品：

```text
/wwdebug kit voldemort
```

如果只想快速打开最终战准备状态：

```text
/wwdebug horcruxes core
/wwdebug battle win
/wwdebug vanilla cultist
/wwdebug vanilla night
/wwdebug god on
```

然后重新运行：

```text
/wwdebug voldemort
```

通过标准：

- Core Horcruxes destroyed 为 OK。
- Nagini defeated 为 OK。
- Battle of Hogwarts won 为 OK。
- Lunatic Cultist defeated 为 OK。
- Night 为 OK。
- Dark Mark boss item 为 OK。
- Summon usable now 为 OK。
- Suggested next step 要求使用 Dark Mark 召唤 Voldemort。

## 3. Boss 实战薄切

操作：

```text
/wwdebug god on
```

- 使用 boss Dark Mark。
- 用 QA Test Wand 击败 Voldemort。
- 再运行：

```text
/wwdebug voldemort
/wwdebug bosses
/wwdebug horcruxes
```

通过标准：

- Voldemort 可成功召唤。
- 击败后 `Voldemort defeated` 为 OK。
- `/wwdebug bosses` 中 `12. Voldemort: True`。
- Boss Compass 应进入 post-Voldemort / Hallows 后续指引，不再指向 Voldemort。
- Suggested next step 要求 Save & Exit 重开验证持久化。

## 4. 持久化抽查

操作：

- Save & Exit。
- 重开同一个世界。
- 运行：

```text
/wwdebug bosses
/wwdebug voldemort
/wwdebug hallows
```

通过标准：

- Voldemort flag 仍为 True。
- `/wwdebug voldemort` 的下一步不再要求打 Voldemort。
- `/wwdebug hallows` 能显示 post-Voldemort 的 Hallows 后续状态或 Dumbledore guidance。

## 停止条件

遇到以下情况直接停：

- boss Dark Mark 与 Death Eater Dark Mark (Morsmordre) 混淆。
- Dark Mark 白天可用，或夜晚/Cultist gate 不生效。
- Horcrux / Battle / Nagini 状态与 Boss Compass 指引相矛盾。
- Voldemort 击败提示出现但 flag 不更新。
- 击败后 Save & Exit 重开丢失 flag。
- 击败后导航仍指向 Voldemort。

## 2026-06-30 实测收口

当前结论：Voldemort readiness、召唤、击杀、Horcrux/Battle/Nagini/Cultist/night gate 与 Save & Exit 后持久化均已通过，本 QA slice 收口。

实测记录：

- `/wwdebug kit voldemort` 能正确给予最终战 QA 物品；boss Dark Mark 图标较小，容易和 `Dark Mark (Morsmordre)` 事件物品混淆。
- `/wwdebug horcruxes core` 能正确标记四个核心 Horcrux destroyed，并保持 Nagini defeated / power 状态可见。
- `/wwdebug battle win` 能正确标记 Battle of Hogwarts won、wardsDefended、unlocked 与 Nagini。
- `/wwdebug vanilla cultist` 能正确打开 Lunatic Cultist gate。
- 白天无法召唤，`/wwdebug voldemort` 能明确提示需要 `/wwdebug vanilla night`。
- 夜晚后使用 boss Dark Mark 可成功召唤 Voldemort。
- Voldemort 可被击败，击败后 `/wwdebug voldemort` 显示 `Voldemort defeated` 为 OK。
- `/wwdebug bosses` 显示 `12. Voldemort: True`。
- `/wwdebug horcruxes` 显示四个核心 Horcrux、Nagini、Voldemort power multiplier 与 preparation score 状态正确。
- Save & Exit 后重开同一世界，`/wwdebug bosses` 仍显示 `12. Voldemort: True`。
- Save & Exit 后重开同一世界，`/wwdebug voldemort` 仍显示 `Voldemort defeated` 为 OK，并提示 persistence verified / QA slice complete。

附带发现：

- `/wwdebug hallows` 能正确显示 `Can claim cloak: True`，说明 Hallows 终章入口已经打开。
- `/wwdebug hallows` 的 Dumbledore guidance 当前显示原始 localization key：`Mods.WizardingWorld.Hallows.GuidanceCloak`。这是 Hallows 文本路径问题，不影响 Voldemort 主线收口，但应在 Hallows 薄切 QA 前修正。

收口判定：

- Voldemort 最终 Boss 主线闭环成立。
- 下一轮 QA 可以进入 Hallows / post-Voldemort 最薄一层检查：领取 true Invisibility Cloak、净化 Gaunt's Ring、装备三圣器触发 Master of Death。
