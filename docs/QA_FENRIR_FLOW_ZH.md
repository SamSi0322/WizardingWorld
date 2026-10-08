# Fenrir 单点闭环 QA 脚本

目标：验证 Umbridge 后的 Blood Moon Boss 门槛是否闭合：Bloodied Claw 获取/制作/商店 gate、Blood Moon 使用条件、Boss Compass / Wizard's Almanac 指引、Fenrir 召唤与击杀 flag、以及击败后向 Bellatrix 的交接。

本轮只测 Fenrir 单点闭环，不进入 Bellatrix、Barty、Dementor King、Voldemort 的完整 QA。

## 测试前提

- 使用已经完成 Umbridge 的同一个测试世界。
- 如需一次性 QA 世界，先用：

```text
/wwdebug bossflag early
/wwdebug bossflag mid
/wwdebug bossflag umbridge
/wwdebug vanilla mech
/wwdebug kit umbridge
```

- 每个阶段先运行：

```text
/wwdebug fenrir
```

## 1. 门槛与导航

通过标准：

- `Hardmode` 为 OK。
- `Umbridge defeated` 为 OK。
- `Fenrir gate open` 为 OK。
- Boss Compass 在 Fenrir 未击败前指向 Fenrir Greyback。
- Wizard's Almanac 的 Boss 页显示 Bloodied Claw 为 post-Umbridge + Blood Moon。

失败记录：

- Umbridge 未击败时 Bloodied Claw 可购买、可制作或可使用。
- `/wwdebug fenrir` 与物品 tooltip / Almanac / Boss Compass 说法不一致。
- Boss Compass 仍指向 Umbridge 或跳过 Fenrir。

## 2. 血月与召唤物路线

操作：

```text
/wwdebug vanilla bloodmoon
/wwdebug kit fenrir
/wwdebug fenrir
```

通过标准：

- `Blood Moon active` 为 OK。
- `Bloodied Claw item` 为 OK。
- `Bloodied Claw materials` 为 OK。
- `Hagrid shop gate` 为 OK。
- `Summon usable now` 为 OK。

失败记录：

- 背包里有 Bloodied Claw 但不可使用，且 Umbridge + Blood Moon gate 已满足。
- 物品 tooltip 未说明 Umbridge + Blood Moon。
- Hagrid 商店 gate 与召唤物 `CanUseItem` 不一致。

## 3. Boss 实战薄切

操作：

```text
/wwdebug god on
```

- 使用 Bloodied Claw。
- 用 QA Test Wand 击败 Fenrir。
- 再运行：

```text
/wwdebug fenrir
/wwdebug bosses
```

通过标准：

- Fenrir 可成功召唤。
- 击败后 `Fenrir defeated` 为 OK。
- `/wwdebug bosses` 中 `8. Fenrir: True`。
- Boss Compass 应转向 Bellatrix Lestrange。
- Suggested next step 要求 Save & Exit 重开验证持久化。

失败记录：

- 召唤失败或无反馈。
- 击败提示出现但 flag 不更新。
- 击败后下一步仍指向 Fenrir。

## 4. 持久化抽查

操作：

- Save & Exit。
- 重开同一个世界。
- 运行：

```text
/wwdebug bosses
/wwdebug fenrir
```

通过标准：

- Fenrir flag 仍为 True。
- `/wwdebug fenrir` 的下一步不再要求打 Fenrir。
- Boss Compass 应转向 Bellatrix Lestrange。

## 停止条件

遇到以下情况直接停：

- Bloodied Claw 的获取、tooltip、使用 gate、debug gate 不一致。
- Blood Moon QA gate 不生效。
- Fenrir 击败 flag 不更新或重开丢失。
- 击败后导航没有交给 Bellatrix。

## 2026-06-29 实测收口

测试结论：Fenrir 单点闭环通过。

实测记录：

- `/wwdebug vanilla bloodmoon` 能正确把当前 QA 世界切到 Blood Moon gate。
- `/wwdebug kit fenrir` 能发放 Bloodied Claw 与 Fenrir 入口所需 QA 物品。
- Bloodied Claw 可成功召唤 Fenrir Greyback。
- Fenrir 可被击败，击败提示正常出现。
- 击败后 `/wwdebug fenrir` 显示路线交接到 Bellatrix Lestrange。
- Save & Exit 后重开同一世界，`/wwdebug fenrir` 仍显示 Fenrir 已击败并交接到 Bellatrix，持久化通过。

备注：

- `/wwdebug bosses` 的截图只覆盖到后半段，未完整截出第 8 行 Fenrir，但 Fenrir 专项诊断已读取到击败态并完成 Bellatrix handoff，因此本轮以专项诊断作为收口依据。
- 强制 Blood Moon 时会伴随 Death Eater 入侵提示；本轮没有阻断 Fenrir QA，但它会增加后续 late-hardmode QA 的噪音，建议下一步做一个很小的 QA-only 清理或在进入 Bellatrix 前确认是否接受这类噪音。
