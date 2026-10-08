# 中期入口实机 QA 脚本

目标：验证早期 arc 完成后，Hardmode 入口到 Aragog、Fluffy、Horntail 的召唤链、商店解锁、文本和存档状态是否顺畅。

本轮只做流程 QA，不做 Boss 数值平衡结论。允许使用 `/wwdebug god on` 和 `/wwdebug kit weapon` 保证能通关验证。

## 本轮收口记录（2026-06-29）

结论：中期入口 Aragog -> Fluffy -> Horntail 三 Boss 主线，按“流程 QA”标准收口通过。后续除非出现崩溃、召唤链断裂、存档回退或商店/文本门槛不一致，不再继续扩大这段改动。

本轮已验证：

- `/wwdebug mid` 能清楚报告 Hardmode、机械 Boss、三件召唤物、Boss active 状态、Hagrid 商店门槛和下一步建议。
- Aragog 在 Hardmode 后可召唤、可击败，击败后流程推进到机械 Boss gate。
- `/wwdebug vanilla mech` 可打开机械 Boss QA gate，Fluffy 与 Horntail 的商店/召唤门槛随之打开。
- Fluffy 可召唤、可击败，击败后流程推进到 Horntail。
- Horntail 召唤失败原因已可解释；修复后 Dragon Egg (Cracked) 可召唤 Horntail，Horntail 可击败。
- Save & Exit 后重开同一世界，`/wwdebug mid` 仍显示 `[OK] Horntail defeated` 与 `The mid entrance arc is complete`。

本轮不作为结论：

- Aragog、Fluffy、Horntail 的自然战斗数值、玩家装备强度和药水消耗平衡。
- 从自然 Hardmode 到机械 Boss、再到三件召唤物材料的完整耗时。
- post-Horntail 系统、Triwizard、St Mungo's、late Hardmode pacing 的体验质量。

收口后的维护规则：

- QA-only gate 和 kit 继续保留给回归验证，但不代表正常玩家路线。
- 若要回测中期，只做最小抽查：`/wwdebug mid`、三 Boss flag、Dragon Egg (Cracked) 失败原因、Save & Exit 持久化。
- 下一阶段 QA 焦点转到 post-Horntail systems 与 late Hardmode pacing。

## 测试前提

- 使用已完成 Troll、Quirrell、Basilisk 的同一个测试世界。
- 如果需要从一次性 QA 世界跳点，先用：

```text
/wwdebug bossflag early
/wwdebug vanilla hardmode
/wwdebug god on
/wwdebug kit weapon
```

- 每个阶段都先运行：

```text
/wwdebug mid
```

把输出中异常的几行截图或贴给我。

## 1. Hardmode 入口与 Aragog

操作：

```text
/wwdebug mid
/wwdebug kit aragog
```

通过标准：

- `Hardmode` 为通过。
- `Aragog summon usable` 为通过。
- Hagrid 商店应在 Hardmode 后出售 Acromantula Egg。
- 使用 Acromantula Egg 可以召唤 Aragog。
- 击败后 `/wwdebug mid` 中 `Aragog defeated` 为通过。

失败记录：

- Hardmode 已开但 Acromantula Egg 不可用。
- Hagrid 商店和 `/wwdebug mid` 门槛不一致。
- Aragog 击败后 flag 不更新或 Save & Exit 后丢失。

## 2. 机械 Boss 门槛与 Fluffy

操作：

```text
/wwdebug vanilla mech
/wwdebug mid
/wwdebug kit fluffy
```

通过标准：

- `Mechanical boss defeated` 为通过。
- `Fluffy summon usable` 为通过。
- Hagrid 商店应在任意机械 Boss 击败后出售 Enchanted Flute。
- 使用 Enchanted Flute 可以召唤 Fluffy。
- 击败后 `/wwdebug mid` 中 `Fluffy defeated` 为通过。

失败记录：

- 未击败机械 Boss 时 Fluffy 可用。
- 已击败机械 Boss 时 Fluffy 不可用。
- 商店显示、物品 tooltip、`/wwdebug mid` 三者说法不一致。

## 3. Horntail

操作：

```text
/wwdebug mid
/wwdebug kit horntail
```

通过标准：

- `Horntail summon usable` 在任意机械 Boss 击败后通过。
- Hagrid 商店应在任意机械 Boss 击败后出售 Dragon Egg (Cracked)。
- Dragon Egg (Cracked) tooltip 应说明需要击败任意机械 Boss。
- 使用 Dragon Egg (Cracked) 可以召唤 Hungarian Horntail。
- 击败后 `/wwdebug mid` 中 `Horntail defeated` 为通过。

失败记录：

- 刚进 Hardmode、未击败机械 Boss 时可以买到或使用 Dragon Egg (Cracked)。
- 已击败机械 Boss 后仍不可用。
- Horntail 击败后 Hagrid/Ollivander/药水等后续商店阶段异常。

## 4. 持久化抽查

操作：

- 正常 Save & Exit。
- 重开同一个世界。
- 运行：

```text
/wwdebug bosses
/wwdebug mid
```

通过标准：

- Aragog、Fluffy、Horntail 已击败状态保持。
- Hardmode 与机械 Boss 状态保持。
- `/wwdebug mid` 的 Suggested next step 不再指向已完成的中期 Boss。

## 停止条件

遇到以下情况直接停：

- 客户端崩溃或回主菜单。
- 召唤物有但无法使用，且 `/wwdebug mid` 显示门槛已满足。
- Boss 击败提示出现，但 `/wwdebug mid` 或 `/wwdebug bosses` 不更新。
- Save & Exit 后中期 Boss flag 或机械 Boss gate 丢失。
