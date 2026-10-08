# Barty Crouch Jr 单点闭环 QA 脚本

目标：验证 Bellatrix 后、Plantera 后的 Barty Crouch Jr 入口是否闭合：Suspicious Flask 获取/制作/商店 gate、Boss Compass / Wizard's Almanac 指引、Barty 召唤与击杀 flag、以及击败后向 Dementor King / Azkaban's Despair 的交接。

本轮只测 Barty 单点闭环，不进入 Dementor King、Voldemort 的完整 QA。

## 测试前提

- 使用已经完成 Bellatrix 的同一个测试世界。
- 如果是一次性 QA 世界，先使用：

```text
/wwdebug bossflag early
/wwdebug bossflag mid
/wwdebug bossflag umbridge
/wwdebug bossflag fenrir
/wwdebug bossflag bellatrix
/wwdebug vanilla plantera
```

- 每个阶段先运行：

```text
/wwdebug barty
```

## 1. 门槛与导航

通过标准：

- `Hardmode` 为 OK。
- `Bellatrix defeated` 为 OK。
- `Plantera defeated` 为 OK。
- `Barty gate open` 为 OK。
- Boss Compass 在 Barty 未击败前指向 Barty Crouch Jr。
- Wizard's Almanac 的 Boss 页显示 Suspicious Flask 为 post-Bellatrix + Plantera。

失败记录：

- Bellatrix 未击败时 Suspicious Flask 可购买、可制作或可使用。
- Plantera 未击败时 Suspicious Flask 可购买、可制作或可使用。
- `/wwdebug barty` 与物品 tooltip / Almanac / Boss Compass 说法不一致。
- Boss Compass 仍指向 Bellatrix 或跳过 Barty。

## 2. 召唤物路线

操作：

```text
/wwdebug vanilla plantera
/wwdebug kit barty
/wwdebug barty
```

通过标准：

- `Suspicious Flask item` 为 OK。
- `Suspicious Flask materials` 为 OK。
- `Hagrid shop gate` 为 OK。
- `Summon usable now` 为 OK。

失败记录：

- 背包里有 Suspicious Flask 但不可使用，且 Bellatrix + Plantera gate 已满足。
- 物品 tooltip 未说明 Bellatrix + Plantera。
- Hagrid 商店 gate 与召唤物 `CanUseItem` 不一致。

## 3. Boss 实战薄切

操作：

```text
/wwdebug god on
```

- 使用 Suspicious Flask。
- 用 QA Test Wand 击败 Barty。
- 再运行：

```text
/wwdebug barty
/wwdebug bosses
```

通过标准：

- Barty 可成功召唤。
- 击败后 `Barty defeated` 为 OK。
- `/wwdebug bosses` 中 `10. Barty Crouch: True`。
- Boss Compass 应转向 Dementor King / Azkaban's Despair。
- Suggested next step 要求 Save & Exit 重开验证持久化。

失败记录：

- 召唤失败或无反馈。
- 击败提示出现但 flag 不更新。
- 击败后下一步仍指向 Barty。

## 4. 持久化抽查

操作：

- Save & Exit。
- 重开同一个世界。
- 运行：

```text
/wwdebug bosses
/wwdebug barty
```

通过标准：

- Barty flag 仍为 True。
- `/wwdebug barty` 的下一步不再要求打 Barty。
- Boss Compass 应转向 Dementor King / Azkaban's Despair。

## 停止条件

遇到以下情况直接停：

- Suspicious Flask 的获取、tooltip、使用 gate、debug gate 不一致。
- Plantera QA gate 不生效。
- Barty 击败 flag 不更新或重开丢失。
- 击败后导航没有交给 Dementor King / Azkaban's Despair。

## 2026-06-30 实测收口

测试结论：Barty 单点闭环通过。

实测记录：

- `/wwdebug barty` 显示 Boss Compass 与 Wizard's Almanac 都指向 Barty / Suspicious Flask 的 post-Bellatrix + Plantera 路线。
- `/wwdebug kit barty` 能发放 Suspicious Flask 与 Barty 入口所需 QA 物品。
- Suspicious Flask 可成功召唤 Barty Crouch Jr。
- Barty 可被击败，击败提示正常出现。
- 击败后 `/wwdebug barty` 显示路线交接到 Dementor King / Azkaban's Despair。
- Save & Exit 后重开同一世界，`/wwdebug barty` 仍显示 Barty 已击败并交接到 Dementor King / Azkaban's Despair，持久化通过。

备注：

- `/wwdebug bosses` 的截图只覆盖到后半段，未完整截出第 10 行 Barty；本轮以 Barty 专项诊断的持久化 handoff 作为收口依据。
- 下一自然 QA 点是 Dementor King / Azkaban's Despair 入口，因为当前路线已交接到 Dementor King，但召唤物、商店与 Almanac 仍主要是 Golem gate，尚未接入 Barty 前置。
