# 前期实机 QA 脚本

目标：验证新角色/新世界从进入游戏到 Troll、Quirrell、Basilisk 前期链路是否自然、可理解、不卡门槛。

## 本轮收口记录（2026-06-28）

结论：前期引导与 Troll -> Quirrell -> Basilisk 三 Boss 主线，按“流程 QA”标准收口通过。后续除非出现崩溃、存档回退、文本错配或召唤链断裂，不再继续扩大前期链路改动。

本轮已验证：

- `/wwdebug early` 能清楚给出当前门槛和下一步建议。
- Troll、Quirrell、Basilisk 三段召唤链可依次推进。
- Quirrell 和 Basilisk 的原版 boss 门槛能通过 `/wwdebug vanilla eye`、`/wwdebug vanilla skeletron` 正确打开。
- Basilisk 击败后，Birch、Red Oak、后 Basilisk 商店阶段和早期 arc 完成提示能正确出现。
- 同一世界 Save & Exit 后重开，Troll、Quirrell、Basilisk 与 Eye of Cthulhu、Skeletron 的关键门槛状态仍保持。
- 召唤物英文显示名已统一为 Smelly Sock、Suspicious Turban、Serpent's Diary 等实际物品名，不再使用泛化的 `* Summon Item` 名称。

本轮不作为结论：

- Boss 数值、玩家强度、武器伤害和药水消耗的自然平衡。测试期间使用过 `/wwdebug god on` 和 `/wwdebug kit weapon`。
- 新角色从零开始自然收集 Life Crystal、材料、附魔桌的完整耗时。
- 城镇 NPC 实际入住等待时间的体感，只确认了门槛和商店解锁链路。

收口后的维护规则：

- QA-only 工具继续保留给后续复现，但不把它们当作正常玩家体验的一部分。
- 若要回测前期，只做最小抽查：物品名、`/wwdebug early` 输出、三 Boss flag、Save & Exit 持久化。
- 下一阶段 QA 焦点转到 Aragog、Fluffy、Horntail 与 hardmode pacing。

## 记录格式

每发现一个问题，记录这四项：

```text
阶段:
实际现象:
预期:
截图/聊天输出:
```

如果使用了 `/wwdebug early`，直接把输出里异常的几行发给我。

## 测试前提

- 使用单人世界，不使用多人客户端。
- 推荐新角色 + 新世界。
- 音效已经通过初听，不需要再专门测 `/wwdebug audio`，除非你觉得某个声音在流程里太响或太频繁。
- 不要先用 `/wwdebug kit` 做自然路线。`kit` 只用于后面的加速复现。

## A. 自然路线

### 1. 初始进入世界

操作：

```text
/wwdebug early
```

通过标准：

- Hogwarts Letter trigger 应该未完成，除非角色已经有 120 最大生命或世界已有早期 boss 击杀。
- Suggested next step 应该指向 120 最大生命或击杀早期原版 boss。
- 不应该凭空拥有 Oak Wand 或 Hogwarts Letter。

失败记录：

- 如果一进世界就收到信，记录角色最大生命、世界 boss 状态、`/wwdebug early` 输出。

### 2. 触发霍格沃茨来信

操作：

- 自然找到并使用 Life Crystal，使最大生命到 120；或击败一个早期原版 boss。
- 收到 Hogwarts Letter 后再次运行：

```text
/wwdebug early
```

通过标准：

- 聊天出现猫头鹰送信文本。
- 背包获得 Hogwarts Letter。
- 背包获得 Oak Wand。
- `Letter delivered` 为通过。
- `Any spell wand in inventory` 为通过。

失败记录：

- 未收到信。
- 收到信但没给 Oak Wand。
- 重复收到信。
- 文本缺失、乱码、语言不一致。

### 3. 附魔桌路径

操作：

- 按自然游玩收集材料。
- 每次觉得材料差不多时运行：

```text
/wwdebug early
```

通过标准：

- Route A 或 Route B 的材料提示清楚。
- 能理解缺什么材料。
- 获得 Enchanting Table 后，`Enchanting Table item` 为通过。
- 附近有附魔桌时，`MagicHum` 只应偶尔出现，不能频繁打断操作。

失败记录：

- 材料需求和实际配方不一致。
- 提示说能做但做不了。
- 提示说不能做但实际能做。
- 环境音过响、过密或位置感奇怪。

### 4. Ollivander / Hagrid 解锁

操作：

- 拥有 Oak Wand 后观察 Ollivander 是否满足入住逻辑。
- 击败 Troll 前后分别检查 Hagrid 条件。
- 运行：

```text
/wwdebug early
```

通过标准：

- Ollivander can move in：拥有法杖或 3 个城镇 NPC 后通过。
- Hagrid can move in：Troll defeated、Basilisk defeated 或 5 个城镇 NPC 后通过。
- 商店提示和实际售卖阶段一致。

失败记录：

- NPC 条件输出通过但 NPC 长时间不来。
- NPC 来了但商店没有对应物品。
- 商店提前卖出后期物品。

### 5. Troll 召唤链

操作：

- 检查 Smelly Sock 材料：

```text
/wwdebug early
```

- 自然收集并制作 TrollSummonItem。
- 尝试召唤 Mountain Troll。

通过标准：

- `Smelly Sock materials` 清楚显示缺少 silk、evil chunk、star 或 station。
- 有召唤物后能正常召唤 Troll。
- Troll 战斗没有加载错误、贴图缺失、音效明显异常。
- 击败后 `Mountain Troll defeated` 为通过。

失败记录：

- 召唤物配方和 debug 输出不一致。
- 有召唤物但无法使用，且没有清楚原因。
- Troll 击败后旗标不更新。

### 6. Quirrell 召唤链

操作：

- 击败 Troll 和 Eye of Cthulhu 后检查：

```text
/wwdebug early
```

- 制作 Suspicious Turban。
- 尝试召唤 Quirrell。

通过标准：

- `Quirrell summon usable` 只在 Troll + Eye 都满足后通过。
- 召唤失败时应能从 debug 输出看懂缺哪个门槛。
- 击败后 `Quirrell defeated` 为通过。

失败记录：

- 未打 Eye 就能召唤。
- Troll/Eye 都满足仍不能召唤。
- 击败后商店或下一阶段未更新。

### 7. Basilisk 召唤链

操作：

- 击败 Quirrell 和 Skeletron 后检查：

```text
/wwdebug early
```

- 制作 Serpent's Diary。
- 尝试召唤 Basilisk。

通过标准：

- `Basilisk summon usable` 只在 Quirrell + Skeletron 都满足后通过。
- Basilisk 击败后 `Basilisk defeated` 为通过。
- 前期主线到这里没有明显断层。

失败记录：

- Quirrell/Skeletron 门槛不一致。
- 召唤物有但不可用且无清楚原因。
- Basilisk 击败后 Hagrid/Ollivander/Fred & George 等商店阶段异常。

## B. 加速复现路线

只在你已经发现问题、需要快速复现时使用。

```text
/wwdebug kit intro
/wwdebug kit troll
/wwdebug kit quirrell
/wwdebug kit basilisk
/wwdebug kit weapon
/wwdebug god status
/wwdebug vanilla eye
/wwdebug vanilla skeletron
/wwdebug bossflag troll
/wwdebug early
```

注意：

- `kit` 只给物品，不改 boss flag。
- `kit intro` 会让 `/wwdebug early` 标记为手动跳过 Intro；这表示自然猫头鹰来信尚未验证，但可以继续测试 Crafting、NPC 和 Troll 召唤链。
- `kit troll` 会额外给 160 最大生命下限、80 魔力下限、空护甲槽自动穿铁甲、Willow Wand、治疗/魔力/基础增益药水、平台和营火，并自动开启当前会话的 `/wwdebug god on`；这只用于验证 Troll 战斗流程，不是自然路线平衡结论。
- `kit weapon` 会给仅用于 QA 的 600 伤害测试魔杖；不属于正常流程。
- `/wwdebug god off` 可关闭无敌；无敌状态不保存到角色。
- `/wwdebug vanilla eye` 和 `/wwdebug vanilla skeletron` 只打开原版 QA 门槛，不改 Wizarding World boss flag。
- `/wwdebug bossflag troll` 可恢复已验证过但丢失的 Wizarding World boss flag；这不是自然路线平衡结论。
- 如果问题依赖 boss 击败状态，不能只靠 `kit` 判断。
- 加速路线结论必须标记为“加速复现”，不能当作自然流程平衡结论。

## 通过标准

这轮 QA 可以算通过，当且仅当：

- 新玩家能自然获得 Hogwarts Letter 和 Oak Wand。
- Enchanting Table 的材料提示、配方、实际制作一致。
- Troll、Quirrell、Basilisk 三段召唤链没有隐藏门槛。
- Ollivander 和 Hagrid 的入住/商店阶段与 debug 输出一致。
- 文本没有明显缺失、乱码、误导。
- 音效在实际流程中不吵、不抢、不重复刷。

## 停止条件

遇到以下情况直接停，不要继续往后测：

- 客户端崩溃或回主菜单。
- 召唤链卡死，无法靠自然方式继续。
- 关键物品缺失或无法制作。
- `/wwdebug early` 输出和实际行为矛盾。

把停止点、输出和现象发给我，我会先修阻塞问题。
