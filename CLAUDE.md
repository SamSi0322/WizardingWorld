# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is **Wizarding World**, a Harry Potter-themed content mod for Terraria via tModLoader 1.4.4+. It is a large-scale mod (593 C# files, 12 bosses, 78 enemies, 24 active wands, 65 accessories; `release_manifest.json` has the current counts) with three-language localization (English, Simplified Chinese, Traditional Chinese).

## Build & Run

```bash
# Build (requires tModLoader + .NET 8 SDK)
dotnet build

# Launch client (uses tModLoader steam path)
dotnet run --launch-profile Terraria

# Launch server
dotnet run --launch-profile TerrariaServer
```

The project uses `tModLoader.targets` from the tModLoader SDK. See `Properties/launchSettings.json` for launch configuration using `tMLPath`/`tMLSteamPath` environment variables.

## Guide PDF Generation

Two Python scripts generate guide PDFs from hardcoded content data (not auto-extracted from code). After content changes, **you must manually update the generators to match**:

```bash
py generate_english_pdf.py   # -> WizardingWorld_Guide_EN.pdf
py generate_chinese_pdf.py   # -> WizardingWorld_Guide_ZH.pdf
```

Requires `fpdf2` (`pip install fpdf2`). Chinese PDF requires `SimHei` font at `C:\Windows\Fonts\simhei.ttf`.

**Critical**: Stats on the cover page, table of contents counts, section body tables, and appendix totals are all manually written in the generators. When counts change, you must update ALL locations — they will not auto-synchronize.

## Architecture

### Namespace & Directory Structure

```
WizardingWorld/
├── Common/
│   ├── Players/          # ModPlayer subclasses (per-player state)
│   │   ├── WizardPlayer.cs           # Central player state hub
│   │   └── DarkArtsCorruptionPlayer.cs  # Corruption meter (0.0-1.0)
│   └── Systems/          # ModSystem, GlobalItem, GlobalNPC, GlobalProjectile
│       ├── HorcruxHuntSystem.cs      # World-saved Horcrux flags + Voldemort scaling
│       ├── HallowsSystem.cs         # Deathly Hallows questline flags
│       ├── DownedBossSystem.cs       # 12 boss progression flags
│       ├── WandMasteryGlobalItem.cs  # Mastery tooltips + damage/mana modifiers
│       ├── WandMasteryGlobalProjectile.cs  # XP gain on spell hit
│       ├── SpellComboSystem.cs       # 6-combo registry (GlobalProjectile)
│       ├── AzkabanDespairEvent.cs    # Late-game Dementor event
│       └── ... (36 total system files)
├── Content/
│   ├── Biomes/            # ForbiddenForestBiome (ModBiome)
│   ├── Buffs/Debuffs/     # PetrifiedDebuff, JinxedDebuff, DarkCurseDebuff
│   ├── DamageClasses/     # SpellDamage (custom damage class, inherits Generic)
│   ├── Items/
│   │   ├── Accessories/   # 65 accessories including Deathly Hallows and Horcruxes
│   │   ├── Armor/[House]/ # 8 armor sets (3 pieces each)
│   │   ├── BossLoot/[Boss]/ # Per-boss loot (Bag, Trophy, Expert item)
│   │   ├── Consumables/   # Potions/, summon items, crafting materials
│   │   ├── Placeable/     # EnchantingTableItem, FelixCauldron, GobletOfFire
│   │   └── Weapons/
│   │       └── Wands/     # 26 wand files (23 active + 1 upgrade + 2 legacy stubs)
│   ├── Mounts/            # 5 mounts (Nimbus, Firebolt, Hippogriff, Thestral, Nimbus 2001)
│   ├── NPCs/
│   │   ├── Bosses/[Boss]/ # 12 bosses, each in own folder
│   │   ├── Enemies/       # 78 enemies
│   │   └── Town/          # 7 town NPCs
│   ├── Pets/[Pet]/        # 6 pets (3 files each: Item, Projectile, Buff)
│   ├── Projectiles/Spells/ # 26 spell projectiles
│   └── Tiles/             # EnchantingTable (3x2 crafting station)
└── Localization/          # HJSON files for en-US, zh-Hans, zh-Hant
```

### State Management Pattern

**ModPlayer (WizardPlayer.cs)** — per-player, per-frame state:
- Equipment flags: `hasElderWand`, `hasInvisibilityCloak`, `hasResurrectionStone`, `hasDeathlyHallows`
- Combat state: `patronusActive`, `patronusTimer`, `despair` (0.0-1.0 float), `timeTurnerCooldown`
- Progression: `houseSet` (0-5), `wandMasteryXP` (Dictionary<int,int>)
- All boolean flags are **reset every frame** in `ResetEffects()` and re-set by active equipment in `UpdateAccessory`/`HoldItem`

**ModSystem (world-saved)** — persistent world state:
- `DownedBossSystem`: 12 static bools for defeated bosses, saved via TagCompound
- `HorcruxHuntSystem`: Horcrux destruction flags, `horcruxesDestroyed` counter, Voldemort power scaling
- `HallowsSystem`: `invisibilityCloakClaimed`, `resurrectionStoneAwakened`, `hallowsAttuned`
- Events: `AzkabanDespairEvent.eventActive/eventProgress` (not persisted across sessions)

**Important**: Deathly Hallows detection does NOT scan armor slots directly in a single accessor. Instead, each Hallow item sets a flag on WizardPlayer during its UpdateAccessory/HoldItem, and `PostUpdateEquips` resolves the combined `hasDeathlyHallows` state centrally.

### Key Progression Systems

**Horcrux Hunt** (HorcruxHuntSystem.cs):
- 4 destroyable Horcruxes (Diary, Locket, Cup, Diadem) + Nagini flag
- Destruction requires Basilisk Fang or Sword of Gryffindor in inventory
- Each destruction weakens Voldemort: 100% → 85% → 70% → 55% → 40% power
- Affects HP, damage, defense, teleport frequency, minion count, bolt count

**Deathly Hallows** (HallowsSystem.cs):
- True Invisibility Cloak: unique quest reward (not craftable), claimed from Dumbledore post-Dementor King + all Horcruxes
- Gaunt's Ring → Resurrection Stone: purified after Voldemort defeated + all Horcruxes
- Elder Wand: Voldemort guaranteed drop
- Master of Death: all 3 equipped → survival-oriented bonuses + corruption immunity

**Wand Mastery** (WandMasteryGlobalItem.cs):
- 1 XP per enemy hit → Level 0 (New) / 1 (Familiar, 100 XP) / 2 (Attuned, 400) / 3 (Mastered, 1000)
- Bonuses: -5% mana per level, +5% damage at level 2-3
- Persisted per wand type in player save data
- Replaces the old ShadowElderWand/WandOfDestiny upgrade path

**Boss Order** (BossChecklistIntegration.cs):
1. Mountain Troll (1.5) → 2. Quirrell (3.5) → 3. Basilisk (4.5) → 4. Aragog (6.0) → 5. Fluffy (7.5) → 6. Horntail (8.0) → 7. Umbridge (9.0) → 8. Fenrir (9.5) → 9. Bellatrix (11.0) → 10. Barty Crouch Jr (12.0) → 11. **Dementor King (13.0, post-Golem)** → 12. **Lord Voldemort (17.0, post-Lunatic Cultist, TRUE FINAL BOSS)**

### Dark Arts Corruption (DarkArtsCorruptionPlayer.cs)

A 0.0-1.0 meter that increases when using Unforgivable Curses or Horcruxes:
- Tier 1 (0.05-0.3): +spell damage, dark aura visual
- Tier 2 (0.3-0.5): Patronus weakened to 75%, NPC prices +10%
- Tier 3 (0.5-0.7): Random Confused debuff, Patronus 50%
- Tier 4 (0.7-0.9): Life regen reduced, spell damage +20%
- Tier 5 (0.9+): Healing devastated, Patronus nearly impossible (5%)

Decays naturally at -0.001/sec. Cleansed by Patronus, Phoenix Tears, Horcrux destruction.

### Despair System (WizardPlayer.UpdateDespair)

A 0.0-1.0 float on players, primarily driven by Azkaban events:
- Mitigated by: Patronus (45%), Warden's Key (25%), Ward of Hope (20%)
- Thresholds: 0.1 (unease) → 0.35 (darkness/weakness) → 0.65 (crushing) → 0.85 (blackout)
- Decays at 0.005/sec baseline, faster with Patronus active

## Canon Tier Labels

Content is tagged with canon fidelity levels in code comments:
- **Canon-faithful**: Directly from the books/films
- **Canon-inspired**: Based on canon concepts but with gameplay liberties
- **Mod-original**: Fully original content for this mod

## Key Conventions

- Wands: `[WoodType]Wand.cs`, all use `SpellDamage` type
- Spell projectiles: `[SpellName]Projectile.cs` in `Content/Projectiles/Spells/`
- Custom debuffs: `[Name]Debuff.cs` in `Content/Buffs/Debuffs/`
- Boss folders: `Content/NPCs/Bosses/[BossName]/[BossName]Boss.cs`
- Boss loot: `Content/Items/BossLoot/[BossName]/` contains Bag, Trophy, Expert item
- Armor sets: `Content/Items/Armor/[HouseName]/[HouseName]{Hood,Robes,Leggings}.cs`
- Pet triplets: `Content/Pets/[Pet]/{[Pet]Item,[Pet]Projectile,[Pet]Buff}.cs`
- Global hooks: `[System]Global[Item|NPC|Projectile]` naming in `Common/Systems/`

## Legacy Items

`ShadowElderWand.cs` and `WandOfDestiny.cs` are marked `[Obsolete]` — they exist as migration stubs for old saves. The "Wand of Destiny" is canonically just another name for the Elder Wand; the Wand Mastery system replaced the old item upgrade chain. Never reintroduce these as separate items.

## Localization

HJSON files in `Localization/` for three languages. Structure:
```hjson
Mods.WizardingWorld: {
  Items: {
    OakWand: {
      DisplayName: Oak Wand
      Tooltip: "'A sturdy first wand'\nCasts Stupefy"
    }
  }
}
```

When renaming items, update all three HJSON files AND the `Bestiary` section if the entity has a bestiary entry.

## Common Pitfalls

1. **Guide count drift**: The PDF generators have hardcoded counts in ~5 separate places (cover, TOC, section titles, body, appendix). Missing one creates inconsistency.
2. **ResetEffects pattern**: All equipment flags on WizardPlayer are cleared every frame. If you add a new flag, you must reset it in `ResetEffects()` and set it in the item's `UpdateAccessory`/`HoldItem`.
3. **Horcrux scaling**: Changes to `HorcruxHuntSystem` directly affect Voldemort's HP, damage, defense, and AI behavior. Test the full scaling range (0-4 destroyed).
4. **Spell school registration**: New spell projectiles must be registered in `WandloreSystem.SpellSchoolRegistry.PostSetupContent()` or the combo system won't recognize them.
5. **Network sync**: World-saved flags in HorcruxHuntSystem and DownedBossSystem use `BitsByte` packing in `NetSend`/`NetReceive`. Adding new flags may require expanding the byte allocation.
6. **The Enchanting Table** (`Content/Tiles/EnchantingTable.cs`) is the central crafting station. Most mod recipes use `.AddTile<Tiles.EnchantingTable>()`.
