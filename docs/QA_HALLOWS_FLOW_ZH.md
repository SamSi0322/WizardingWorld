# Hallows / Post-Voldemort Thin QA

目标：验证 Voldemort 后的最薄终章闭环：Dumbledore guidance 本地化、领取 true Invisibility Cloak、净化 Gaunt's Ring 得到 Resurrection Stone、装备三圣器触发 Master of Death，以及 Save & Exit 后持久化。

本轮只测 Deathly Hallows 收尾，不展开新的战斗、商店扩展或 postgame 内容。

## 1. 前置条件

当前世界应已经满足：

- 四个核心 Horcrux destroyed。
- Dementor King defeated。
- Voldemort defeated。
- 背包或装备中有 Gaunt's Ring。
- 背包中有 Elder Wand。
- 世界中有 Dumbledore，或有可用住房等待他入住。

快速检查：

```text
/wwdebug hallows
```

通过标准：

- `Dumbledore says` 显示正常文本，而不是 localization key。
- `Can claim cloak: True` 时，Suggested next step 应要求找 Dumbledore 点击 `Receive Cloak`。
- 如果 `Dumbledore present: False`，先准备空房间并等待 Dumbledore 入住。

## 2. 领取 true Invisibility Cloak

正常操作：

- 找 Dumbledore。
- 点击第二按钮 `Receive Cloak`。
- 再运行：

```text
/wwdebug hallows
```

QA shortcut：

```text
/wwdebug hallows claim
/wwdebug hallows
```

通过标准：

- `Cloak claimed from Dumbledore: True`。
- 背包中出现 true Invisibility Cloak。
- `Can claim cloak: False`。
- 若未净化戒指，Suggested next step 应转向 Gaunt's Ring / Purify Ring。

## 3. 净化 Gaunt's Ring

正常操作：

- 确认背包或装备中有 Gaunt's Ring。
- 找 Dumbledore。
- 点击第二按钮 `Purify Ring`。
- 再运行：

```text
/wwdebug hallows
```

QA shortcut：

```text
/wwdebug hallows purify
/wwdebug hallows
```

说明：`/wwdebug hallows purify` 是 QA shortcut，会直接唤醒 Resurrection Stone 并给予物品，不依赖 Gaunt's Ring 检测；正常玩家流程仍然通过 Dumbledore 净化 Gaunt's Ring。

通过标准：

- `Resurrection Stone awakened: True`。
- 背包中出现 Resurrection Stone。
- `Can purify ring: False`。
- Suggested next step 应要求装备三圣器。

## 4. 触发 Master of Death

如果只需要直接测试三圣器装备闭环：

```text
/wwdebug hallows kit
```

操作：

- 保持 Elder Wand 在背包中。
- 将 true Invisibility Cloak 装备到饰品栏。
- 将 Resurrection Stone 装备到饰品栏。
- 等一小会儿，再运行：

```text
/wwdebug hallows
```

通过标准：

- `[Player] hasElderWand: True`。
- `[Player] hasInvisibilityCloak: True`。
- `[Player] hasResurrectionStone: True`。
- `[Player] hasDeathlyHallows: True`。
- `Master of Death attuned: True`。
- Suggested next step 应提示 Hallows route complete。

如果本轮只需要直接收口，不再测试装备栏触发：

```text
/wwdebug hallows complete
/wwdebug hallows
```

通过标准：

- `Cloak claimed from Dumbledore: True`。
- `Resurrection Stone awakened: True`。
- `Master of Death attuned: True`。
- Suggested next step 应提示 Hallows route complete。
- `[Player] hasDeathlyHallows` 可以为 `False`，因为它是当前装备状态，不是世界进度 flag。

## 5. 持久化抽查

操作：

- Save & Exit。
- 重开同一个世界。
- 运行：

```text
/wwdebug hallows
```

通过标准：

- `Cloak claimed from Dumbledore: True`。
- `Resurrection Stone awakened: True`。
- `Master of Death attuned: True`。
- 装备三圣器后玩家 flag 仍能重新变为 True。

## 停止条件

遇到以下情况直接停：

- Dumbledore guidance 再次显示 localization key。
- `Can claim cloak: True` 但 Dumbledore 没有 `Receive Cloak` 按钮。
- `Can purify ring: True` 但 Dumbledore 没有 `Purify Ring` 按钮。
- 领取或净化后物品没有进入背包。
- 装备三圣器后 `hasDeathlyHallows` 或 `hallowsAttuned` 不更新；若使用 `/wwdebug hallows complete` 直接收口，则只看 `hallowsAttuned`。
- Save & Exit 后 Hallows 世界 flag 丢失。
