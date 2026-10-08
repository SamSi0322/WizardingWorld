# Umbridge 单点闭环 QA 脚本

目标：验证 Horntail 后的下一 Boss 门槛是否闭合：Educational Decree 获取/制作/商店 gate、Boss Compass / Wizard's Almanac 指引、Umbridge 召唤与击杀 flag、以及击败后向 Fenrir 的交接。

本轮只测 Umbridge 单点闭环，不进入 Fenrir、Bellatrix、Dementor King、Voldemort 的完整 QA。

## 测试前提

- 使用已经完成 post-Horntail thin-slice 的测试世界。
- 如需一次性 QA 世界，先用：

```text
/wwdebug bossflag early
/wwdebug bossflag mid
/wwdebug vanilla mech
/wwdebug kit umbridge
```

- 每个阶段先运行：

```text
/wwdebug umbridge
```

## 1. 门槛与导航

通过标准：

- `Hardmode` 为 OK。
- `Mechanical boss defeated` 为 OK。
- `Horntail defeated` 为 OK。
- `Umbridge gate open` 为 OK。
- Boss Compass 在 Umbridge 未击败前指向 Dolores Umbridge。
- Wizard's Almanac 的 Boss 页显示 Educational Decree 为 post-Horntail + Mech。

失败记录：

- Horntail 未击败时 Educational Decree 可购买或可使用。
- `/wwdebug umbridge` 与物品 tooltip / Almanac / Boss Compass 说法不一致。
- Boss Compass 仍指向 Horntail 或跳过 Umbridge。

## 2. 召唤物路线

操作：

```text
/wwdebug kit umbridge
/wwdebug umbridge
```

通过标准：

- `Educational Decree item` 为 OK。
- `Educational Decree materials` 为 OK。
- `Hagrid shop gate` 为 OK。
- `Summon usable now` 为 OK。

失败记录：

- 背包里有 Educational Decree 但不可使用，且 gate 已满足。
- 物品 tooltip 未说明 Horntail + mechanical boss。
- Hagrid 商店 gate 与召唤物 `CanUseItem` 不一致。

## 3. Boss 实战薄切

操作：

- 开启必要测试辅助：

```text
/wwdebug god on
```

- 使用 Educational Decree。
- 用 QA Test Wand 击败 Umbridge。
- 再运行：

```text
/wwdebug umbridge
/wwdebug bosses
```

通过标准：

- Umbridge 可成功召唤。
- 阶段文本不出现 `Mods.WizardingWorld...` raw key。
- 击败后 `Umbridge defeated` 为 OK。
- `/wwdebug bosses` 中 `7. Umbridge: True`。
- Suggested next step 要求 Save & Exit 重开验证持久化。

失败记录：

- 召唤失败或无反馈。
- 阶段文本 raw key。
- 击败提示出现但 flag 不更新。
- 击败后下一步仍指向 Umbridge。

## 4. 持久化抽查

操作：

- Save & Exit。
- 重开同一个世界。
- 运行：

```text
/wwdebug bosses
/wwdebug umbridge
```

通过标准：

- Umbridge flag 仍为 True。
- `/wwdebug umbridge` 的下一步不再要求打 Umbridge。
- Boss Compass 应转向 Fenrir Greyback。

## 停止条件

遇到以下情况直接停：

- Educational Decree 的获取、tooltip、使用 gate、debug gate 不一致。
- Umbridge 击败 flag 不更新或重开丢失。
- 对话出现 raw key。
- 击败后导航没有交给 Fenrir。

## 2026-06-29 实测收口

状态：已完成。

已通过项目：

- `/wwdebug umbridge` 能识别 Hardmode、mechanical boss、Horntail 后的 Umbridge gate。
- `/wwdebug kit umbridge` 能提供 Educational Decree、材料、Boss Compass、Wizard's Almanac 和 QA Test Wand。
- Educational Decree 可成功召唤 Dolores Umbridge。
- Umbridge 阶段文本、decree 文本、召唤小怪文本均正常显示，没有 raw key。
- Umbridge 可被击败，击败提示出现。
- 击败后 `/wwdebug umbridge` 显示 Boss Compass 已转向 Fenrir。
- Save & Exit 后重开同一个世界，Umbridge 状态保持，导航仍指向 Fenrir。

本轮发现并已修复：

- Umbridge gate 原本只依赖 Hardmode / mechanical boss，已统一为 Hardmode + 任意机械 Boss + Horntail defeated。
- Hagrid 商店 gate、召唤物 `CanUseItem`、BossChecklist、Wizard's Almanac、tooltip 已统一。
- Umbridge BossDialogue 文本加入 fallback，避免 raw key。
- `/wwdebug umbridge` 的完成提示已改为：若这是 Save & Exit 后的结果，即可判定持久化通过并转 Fenrir。

收口结论：

- Umbridge 单点闭环 QA 已完成。
- 下一阶段可以讨论 Fenrir 入口/单点闭环；建议仍保持最小 QA 范围，不一次性展开所有 late-hardmode Boss。
