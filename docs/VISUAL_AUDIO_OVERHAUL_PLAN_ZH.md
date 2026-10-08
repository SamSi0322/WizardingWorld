# 视觉与音场重制计划

## 目标

这次重制不做“全世界换皮”。目标是在玩家最容易感受到模组身份的地方增加哈利波特风格视觉层，并把 Boss 从“功能可用”推进到“有轮廓、有压迫感、有记忆点”的状态。

范围控制原则：

- 优先改关键阶段、关键区域、主线 Boss。
- 不重写主线流程，不扩大数值系统。
- 不全局替换泰拉瑞亚原版背景，避免和原版/其他 Mod 冲突。
- 新资源必须服务已有内容，不为了堆资产而新增系统。
- 先做样板切片，确认画风和实机效果后再批量替换。

## 分层方案

| 层级 | 内容 | 推荐程度 | 说明 |
| --- | --- | --- | --- |
| 场景滤镜 | 色调、雾气、光照、粒子、环境音 | 必做 | 已有系统可扩展，风险低 |
| 关键区域背景 | 禁林、阿兹卡班、霍格沃茨战场、魔法部/乌姆里奇线 | 必做 | 不改全世界，只覆盖剧情节点 |
| 地标建筑 | 霍格沃茨轮廓、霍格莫德、古灵阁、圣芒戈、尖叫棚屋 | 分批做 | 适合用已有 Landmark tile 系统承接 |
| Boss 贴图 | 12 个 Boss 的 spritesheet + boss head icon | 必做 | 当前最影响品质感 |
| 全局世界替换 | 原版森林/地牢/天空全部换皮 | 暂缓 | 体量大、风险高、不适合当前收口方向 |

## 场景优先级

| 优先级 | 场景 | 触发节点 | 视觉目标 | 音场目标 |
| --- | --- | --- | --- | --- |
| P0 | Forbidden Forest | Basilisk 后的夜晚森林 | 深色树冠、绿色雾、蛛网、发光眼睛 | 风声、远处猫头鹰、偶发低吼 |
| P0 | Voldemort / Battle of Hogwarts | 终局战与战场事件 | 绿黑天空、远处城堡轮廓、火光、咒语残影 | 远处爆炸、龙吼、幽灵般战场声 |
| P1 | Azkaban | Dementor King 与阿兹卡班事件 | 冷蓝灰滤镜、黑雾、摄魂怪残影 | 冷风、摄魂怪尖啸、低频压迫声 |
| P1 | Ministry / Umbridge | Umbridge 线 | 粉色法令、纸张/印章、魔法部审判感 | 纸张翻动、印章、低压人声/魔法嗡鸣 |
| P1 | Shrieking Shack | Fenrir / 狼人线 | 月光、破屋剪影、幽灵白雾 | 狼嚎、木屋嘎吱、远处低吼 |
| P2 | Gringotts / Diagon / Knockturn | 古灵阁、翻倒巷、对角巷任务 | 金色地下金库、歪斜店铺、魔法伦敦 | 金属回声、低语、暗巷风声 |
| P2 | St Mungo's | post-Horntail 医院入口 | 旧百货橱窗、治疗魔法、绿色白光 | 轻微魔法治疗声、病房氛围 |

## Boss 重绘规格

当前 Boss spritesheet 多为 36-80px 宽，很多接近玩家尺寸。重绘目标是扩大“视觉占图”，但命中框不一定等于整张图，避免战斗变得不公平。

| Boss | 当前视觉问题 | 新视觉目标 | 建议帧规格 | 建议命中框 |
| --- | --- | --- | --- | --- |
| Mountain Troll | 像普通人形怪 | 巨型驼背、粗腿、木棒、笨重前压 | 128x128, 6 frames | 72x96 |
| Quirrell | 人形太小 | 人形本体 + 头巾黑魔法裂影，二阶段扩大暗影 | 80x104, 6 frames | 44x64 |
| Basilisk | 太短太圆 | 巨大蛇头 + 盘绕身体，黄色凝视和毒牙 | 192x112, 6 frames | 96x70 |
| Aragog | 蜘蛛辨识弱 | 巨大八足蜘蛛，腿部横向铺开，蛛网拖尾 | 160x112, 6 frames | 100x76 |
| Fluffy | 三头犬不明显 | 大型三头犬，三个头有独立表情和攻击姿态 | 160x116, 6 frames | 104x84 |
| Horntail | 龙还不够占屏 | 黑鳞火龙，翅膀、角、尾刺突出 | 192x136, 6 frames | 112x88 |
| Umbridge | 人形 Boss 不能硬放大 | 人形保持小体型，法令、粉色屏障和审判投影扩大占图 | 72x96, 6 frames + effect | 42x62 |
| Fenrir | 狼人压迫不足 | 大型狼人，弓背、利爪、月光剪影 | 120x116, 6 frames | 76x90 |
| Bellatrix | 人形辨识不足 | 黑色乱发、长袍、紫黑咒刃，让斗篷和魔法扩大轮廓 | 88x108, 6 frames | 44x66 |
| Barty Crouch Jr | 人形辨识不足 | 人形 + 变形/伪装残影，瓶剂与黑魔法特征 | 80x104, 6 frames | 44x64 |
| Dementor King | 可以更高更空洞 | 高大破斗篷、无脸黑洞、冰蓝手、黑雾拖尾 | 128x160, 6 frames | 72x112 |
| Voldemort | 终局压迫不足 | 瘦高本体 + 巨大绿黑魔法外轮廓 + 纳吉尼/黑魔标记元素 | 112x132, 6 frames + aura | 48x76 |

## Boss 贴图实装规则

- 保留每个 Boss 当前 6 帧结构，先不改 AI 节奏。
- 每个 Boss 同时替换 `Boss.png` 和 `_Head_Boss.png`。
- 大图必须同步检查：
  - `NPC.width` / `NPC.height`
  - draw origin / rotation
  - dust 范围
  - projectile spawn point
  - contact damage 是否合理
  - Boss Checklist / health bar head icon
- 人形 Boss 不做“巨人化”，用斗篷、法阵、投影、召唤物和场景压迫扩大视觉占图。

## 音场方案

短期先复用现有自定义音效，在关键系统中按低频冷却触发。长期再补专属 Ambient OGG。

| 场景 | 短期已接入/可接入 | 长期应补专属音效 |
| --- | --- | --- |
| Forbidden Forest | ForestWind, OwlHoot | ForbiddenForestNightBed.ogg, SpiderRustle.ogg |
| Azkaban | DementorScream | AzkabanColdWind.ogg, SoulDrainBed.ogg |
| Battle of Hogwarts | DragonRoar, GhostWail | CastleSiegeBed.ogg, DistantSpellWar.ogg |
| Gringotts | MagicHum | VaultEcho.ogg, CartRumble.ogg |
| Knockturn Alley | GhostWail | KnockturnWhisper.ogg, CursedShopHum.ogg |
| Shrieking Shack | WerewolfHowl, GhostWail | ShackCreak.ogg, FullMoonWind.ogg |
| Ministry / Umbridge | 暂缺专属 cue | DecreeStamp.ogg, PaperFlutter.ogg |
| Voldemort final | AvadaKedavra, GhostWail | FinalBattleBed.ogg, DarkMarkPulse.ogg |

## 推荐实施顺序

## 已落地的第一批场景贴图

- Forbidden Forest: `Assets/Backgrounds/ForbiddenForestFar.png`, `ForbiddenForestMiddle.png`, `ForbiddenForestClose.png`，已接入 `ForbiddenForestBiome`。
- Battle of Hogwarts: `Assets/Backgrounds/BattleOfHogwartsFar.png`, `BattleOfHogwartsMiddle.png`, `BattleOfHogwartsClose.png`，已接入 `BattleSceneEffect`。
- 场景贴图已升级到 v2 半写实像素风：禁林增加树皮、蛛网、雾带、月光和远景城堡；霍格沃茨之战增加石墙纹理、火光、烟柱、咒语弧线和废墟。
- 预览合成图：`release_assets/visual_preview/preview_scene_background_slice_v2.png`。

### 第一切片：证明画风和技术管线

1. 重绘 Mountain Troll。
2. 重绘 Basilisk。
3. 强化 Forbidden Forest 视觉层：背景色、雾、蛛网/眼睛粒子、夜间音场。
4. 实机确认 Boss 尺寸、命中框、旋转、粒子范围、音量。

这个切片覆盖“巨型人形 Boss + 非人型蛇类 Boss + 关键生物群系”，最适合验证后续 12 Boss 重绘是否可行。

### 第二切片：中期主线观感

1. Aragog、Fluffy、Horntail 三个大型生物 Boss。
2. St Mungo's / Triwizard / Forbidden Forest post-Horntail 场景提示。
3. 龙、蜘蛛、三头犬的专属咆哮/动作音。

### 第三切片：后期人形 Boss 表现

1. Umbridge、Fenrir、Bellatrix、Barty。
2. 魔法部、尖叫棚屋、阿兹卡班视觉层。
3. 人形 Boss 通过法阵、投影、斗篷、屏幕氛围扩大视觉占图。

### 第四切片：终局包装

1. Dementor King、Voldemort。
2. Battle of Hogwarts / Voldemort final 背景与音场。
3. Hallows 完成后的结尾视觉提示。

## 当前结论

最自然的下一步是先做第一切片：Mountain Troll + Basilisk + Forbidden Forest。它能最快验证玩家第一眼感受到的变化，同时不把项目拖成无限资产工程。
