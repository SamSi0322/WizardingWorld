# Bellatrix 单点闭环 QA 脚本

目标：验证 Fenrir 后、Plantera 后的 Bellatrix 入口是否闭合：Azkaban Prisoner Tag 获取/制作/商店 gate、Boss Compass / Wizard's Almanac 指引、Bellatrix 召唤与击杀 flag、以及击败后向 Barty Crouch Jr 的交接。

本轮只测 Bellatrix 单点闭环，不进入 Barty Crouch Jr、Dementor King、Voldemort 的完整 QA。

## 测试前提

- 使用已经完成 Fenrir 的同一个测试世界。
- 如果是一次性 QA 世界，先使用：

```text
/wwdebug bossflag early
/wwdebug bossflag mid
/wwdebug bossflag umbridge
/wwdebug bossflag fenrir
/wwdebug vanilla plantera
```

- 每个阶段先运行：

```text
/wwdebug bellatrix
```

## 1. 门槛与导航

通过标准：

- `Hardmode` 为 OK。
- `Fenrir defeated` 为 OK。
- `Plantera defeated` 为 OK。
- `Bellatrix gate open` 为 OK。
- Boss Compass 在 Bellatrix 未击败前指向 Bellatrix Lestrange。
- Wizard's Almanac 的 Boss 页显示 Azkaban Prisoner Tag 为 post-Fenrir + Plantera。

失败记录：

- Fenrir 未击败时 Azkaban Prisoner Tag 可购买、可制作或可使用。
- Plantera 未击败时 Azkaban Prisoner Tag 可购买、可制作或可使用。
- `/wwdebug bellatrix` 与物品 tooltip / Almanac / Boss Compass 说法不一致。
- Boss Compass 仍指向 Fenrir 或跳过 Bellatrix。

## 2. 召唤物路线

操作：

```text
/wwdebug vanilla plantera
/wwdebug kit bellatrix
/wwdebug bellatrix
```

通过标准：

- `Azkaban Prisoner Tag item` 为 OK。
- `Azkaban Prisoner Tag materials` 为 OK。
- `Hagrid shop gate` 为 OK。
- `Summon usable now` 为 OK。

失败记录：

- 背包里有 Azkaban Prisoner Tag 但不可使用，且 Fenrir + Plantera gate 已满足。
- 物品 tooltip 未说明 Fenrir + Plantera。
- Hagrid 商店 gate 与召唤物 `CanUseItem` 不一致。

## 3. Boss 实战薄切

操作：

```text
/wwdebug god on
```

- 使用 Azkaban Prisoner Tag。
- 用 QA Test Wand 击败 Bellatrix。
- 再运行：

```text
/wwdebug bellatrix
/wwdebug bosses
```

通过标准：

- Bellatrix 可成功召唤。
- 阶段文本不显示 raw localization key。
- 击败后 `Bellatrix defeated` 为 OK。
- `/wwdebug bosses` 中 `9. Bellatrix: True`。
- Boss Compass 应转向 Barty Crouch Jr。
- Suggested next step 要求 Save & Exit 重开验证持久化。

失败记录：

- 召唤失败或无反馈。
- Boss 阶段文本显示 `Mods.WizardingWorld...` raw key。
- 击败提示出现但 flag 不更新。
- 击败后下一步仍指向 Bellatrix。

## 4. 持久化抽查

操作：

- Save & Exit。
- 重开同一个世界。
- 运行：

```text
/wwdebug bosses
/wwdebug bellatrix
```

通过标准：

- Bellatrix flag 仍为 True。
- `/wwdebug bellatrix` 的下一步不再要求打 Bellatrix。
- Boss Compass 应转向 Barty Crouch Jr。

## 停止条件

遇到以下情况直接停：

- Azkaban Prisoner Tag 的获取、tooltip、使用 gate、debug gate 不一致。
- Plantera QA gate 不生效。
- Bellatrix 击败 flag 不更新或重开丢失。
- 击败后导航没有交给 Barty Crouch Jr。

## 2026-06-29 实测收口

测试结论：Bellatrix 单点闭环通过。

实测记录：

- `/wwdebug vanilla plantera` 能正确打开 Plantera QA gate。
- `/wwdebug bellatrix` 显示 Boss Compass 与 Wizard's Almanac 都指向 Bellatrix / Azkaban Prisoner Tag 的 post-Fenrir + Plantera 路线。
- Azkaban Prisoner Tag 可成功召唤 Bellatrix。
- Bellatrix 可被击败，击败后 `/wwdebug bellatrix` 显示路线交接到 Barty Crouch Jr。
- Save & Exit 后重开同一世界，`/wwdebug bellatrix` 仍显示 Bellatrix 已击败并交接到 Barty Crouch Jr，持久化通过。

备注：

- `/wwdebug bosses` 的截图只覆盖到后半段，未完整截出第 9 行 Bellatrix；本轮以 Bellatrix 专项诊断的持久化 handoff 作为收口依据。
- 下一自然 QA 点是 Barty Crouch Jr 入口，因为当前路线已交接到 Barty，但 Barty 的召唤物、商店与 Almanac 仍是纯 Plantera gate，尚未接入 Bellatrix 前置。
