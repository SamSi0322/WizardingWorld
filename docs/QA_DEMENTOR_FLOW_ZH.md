# Dementor King 单点闭环 QA 脚本

目标：验证 Barty 后、Golem 后、夜晚的 Dementor King / Azkaban's Despair 入口是否闭合：Frozen Soul Lantern 获取/制作/商店 gate、Boss Compass / Wizard's Almanac 指引、Dementor King 召唤与击杀 flag、以及击败后向 Voldemort readiness 的交接。

本轮只测 Dementor King 单点闭环，不进入 Voldemort / Horcrux / Hallows 的完整 QA。

## 测试前提

- 使用已经完成 Barty 的同一个测试世界。
- 如果是一次性 QA 世界，先使用：

```text
/wwdebug bossflag early
/wwdebug bossflag mid
/wwdebug bossflag umbridge
/wwdebug bossflag fenrir
/wwdebug bossflag bellatrix
/wwdebug bossflag barty
/wwdebug vanilla golem
/wwdebug vanilla night
```

- 每个阶段先运行：

```text
/wwdebug dementor
```

## 1. 门槛与导航

通过标准：

- `Hardmode` 为 OK。
- `Barty defeated` 为 OK。
- `Golem defeated` 为 OK。
- `Night` 为 OK。
- `Dementor gate open` 为 OK。
- Boss Compass 在 Dementor King 未击败前指向 Azkaban's Despair / Dementor King。
- Wizard's Almanac 的 Boss 页显示 Frozen Soul Lantern 为 post-Barty + Golem + night。

失败记录：

- Barty 未击败时 Frozen Soul Lantern 可购买、可制作或可使用。
- Golem 未击败时 Frozen Soul Lantern 可购买、可制作或可使用。
- 白天可使用 Frozen Soul Lantern。
- `/wwdebug dementor` 与物品 tooltip / Almanac / Boss Compass 说法不一致。

## 2. 召唤物路线

操作：

```text
/wwdebug vanilla golem
/wwdebug vanilla night
/wwdebug kit dementor
/wwdebug dementor
```

通过标准：

- `Frozen Soul Lantern item` 为 OK。
- `Frozen Soul Lantern materials` 为 OK。
- `Hagrid shop gate` 为 OK。
- `Summon usable now` 为 OK。
- `Azkaban event active` 不影响 Boss 召唤判断。

失败记录：

- 背包里有 Frozen Soul Lantern 但不可使用，且 Barty + Golem + night gate 已满足。
- 物品 tooltip 未说明 Barty + Golem + night。
- Hagrid 商店 gate 与召唤物 `CanUseItem` 不一致。

## 3. Boss 实战薄切

操作：

```text
/wwdebug god on
```

- 使用 Frozen Soul Lantern。
- 用 QA Test Wand 击败 Dementor King / Azkaban's Despair。
- 再运行：

```text
/wwdebug dementor
/wwdebug bosses
```

通过标准：

- Dementor King 可成功召唤。
- 击败后 `Dementor King defeated` 为 OK。
- `/wwdebug bosses` 中 `11. Dementor King: True`。
- Boss Compass 应转向 Voldemort readiness。
- Suggested next step 要求 Save & Exit 重开验证持久化。

失败记录：

- 召唤失败或无反馈。
- 击败提示出现但 flag 不更新。
- 击败后下一步仍指向 Dementor King。

## 4. 持久化抽查

操作：

- Save & Exit。
- 重开同一个世界。
- 运行：

```text
/wwdebug bosses
/wwdebug dementor
```

通过标准：

- Dementor King flag 仍为 True。
- `/wwdebug dementor` 的下一步不再要求打 Dementor King。
- Boss Compass 应转向 Voldemort readiness。

## 停止条件

遇到以下情况直接停：

- Frozen Soul Lantern 的获取、tooltip、使用 gate、debug gate 不一致。
- Golem 或 night QA gate 不生效。
- Dementor King 击败 flag 不更新或重开丢失。
- 击败后导航没有交给 Voldemort readiness。

## 2026-06-30 实测收口

当前结论：Dementor King / Azkaban's Despair 召唤、击杀、路线交接与重开后持久化均通过，本 QA slice 收口。

实测记录：

- `/wwdebug vanilla golem` 能正确打开 Golem QA gate。
- `/wwdebug vanilla night` 能正确切到夜晚且不触发 Blood Moon。
- `/wwdebug dementor` 显示 Boss Compass 与 Wizard's Almanac 都指向 Dementor King / Frozen Soul Lantern 的 post-Barty + Golem + night 路线。
- Frozen Soul Lantern 可成功召唤 Dementor King / Azkaban's Despair。
- Dementor King 可被击败，击败后 `/wwdebug dementor` 显示路线交接到 Voldemort readiness。
- Save & Exit 后重开同一世界，`/wwdebug dementor` 仍显示 Boss Compass 指向 Voldemort readiness，并提示本 slice complete，确认 Dementor King 击败状态与路线交接已持久化。

收口判定：

- Barty -> Golem/night -> Frozen Soul Lantern -> Dementor King -> Voldemort readiness 的单点闭环成立。
- 下一轮 QA 可以进入 Voldemort readiness，但应先补齐最终战专用 debug route 与 QA kit，避免 Horcrux / Battle of Hogwarts / Cultist 多重 gate 让实测流程变得不透明。
