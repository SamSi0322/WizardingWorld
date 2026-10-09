<p align="center">
  <img src="release_assets/wizardingworld-banner-wide.png" alt="Wizarding World: pixel-art banner with Hogwarts, the Deathly Hallows symbol and a Golden Snitch" width="100%">
</p>

# Wizarding World — A Harry Potter Mod for Terraria

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![tModLoader 1.4.4+](https://img.shields.io/badge/tModLoader-1.4.4+-blue.svg)](https://www.tmodloader.net/)
[![.NET 8](https://img.shields.io/badge/.NET-8.0-512BD4.svg)](https://dotnet.microsoft.com/)
[![Status: fan project](https://img.shields.io/badge/status-unofficial%20fan%20project-orange.svg)](#license--ip-disclaimer)

By **Xinyue (Lily) Feng** · [Project page](https://samsi0322.github.io/xinyue-feng/work/wizarding-world/) · [Player guide (EN)](WizardingWorld_Guide_EN.pdf) · [玩家指南 (中文)](WizardingWorld_Guide_ZH.pdf)

> **Disclaimer.** This is an **unofficial fan project**. Harry Potter, Hogwarts, the wizarding-world setting, and all related names, characters, places, and indicia are trademarks of Warner Bros. Entertainment Inc., J.K. Rowling, and other rights holders. This mod is **not affiliated with, endorsed by, or sponsored by** any rights holder. Non-commercial fan use only — see [License & IP disclaimer](#license--ip-disclaimer) at the bottom.

> **Project status — release candidate.** The primary single-player progression route has been smoke-tested in tModLoader from early game through Voldemort and the Deathly Hallows ending. The mod is **not yet on Steam Workshop**; remaining release work is focused on wider balance, multiplayer sync, and packaging checks.

A comprehensive Harry Potter Hogwarts experience mod for Terraria via tModLoader. **597 C# source files, 624 PNG sprites, 1,546 project files.** Canon-audited and redesigned with cleaner Hallows/Horcrux progression and stronger late-game consistency.

**Core Identity:** You are a Hogwarts student experiencing memories from across wizarding history through a Pensieve, learning spells, mastering your wand, and facing the rising darkness.

**Highlights:**
- **12 multi-phase bosses** with Voldemort as the true final boss (Horcrux Hunt mechanic)
- **Dark Arts Corruption System** — dark magic is tempting but genuinely costly
- **Wandlore System** — 18 wood types, 5 cores, 9 spell schools
- **Pensieve Memory Framework** — solves mixed-era lore, enables boss replay
- **Horcrux Hunt** — destroy the 4 core Horcruxes, hunt Nagini, and weaken Voldemort before the final battle
- **Master of Death** — survival/fate-oriented hidden set bonus (not raw DPS)
- **Utility Magic** — Alohomora (opens doors), Reparo (ward/room repair), Accio (item attraction)
- **Class Quest System** — DADA, Potions, Creatures, Charms with mastery levels
- **Quidditch Season** — Seeker ranks, multi-Snitch events, broom trials
- **Hogsmeade Village** — worldgen town with Shrieking Shack
- **Forbidden Forest** — 3-zone depth scaling with progressive danger
- 78 enemies, 64 accessories, 8 armor sets, 5 mounts, 6 pets total, 19 potions
- 3-language support (English, Chinese Simplified, Chinese Traditional)
- Canon-audited: true Invisibility Cloak is unique, Gaunt's Ring awakens the Resurrection Stone, Demiguise gear is ordinary stealth gear

## Release QA summary

As of July 1, 2026, Wizarding World is treated as a **1.0.0 release candidate**. The focus is no longer adding new systems; the current scope is packaging, publishing, and wider community validation.

Completed content and packaging:

- Core content is in place: 12 Wizarding World bosses, 24 active wands, 78 enemies, 64 accessories, 16 town NPCs, 8 armor sets, 5 mounts, 6 pets, 19 potions, and three-language localization.
- In-game PNG asset coverage is complete and tracked by `scripts/verify_assets.py`.
- Custom spell, boss, enemy, and ambient audio has been generated, wired, and smoke-tested.
- Release packaging is ready: public Release builds omit `/wwdebug`, `WizardDebugCommand`, and the QA-only test wand.
- Workshop / Mod Browser copy, release checklist, and release manifest are maintained in `description.txt`, `docs/WORKSHOP_PAGE.md`, `docs/RELEASE_CHECKLIST.md`, and `release_manifest.json`.

Completed smoke-test coverage:

- Early route: Hogwarts Letter, first wand, Enchanting Table, Ollivander/Hagrid unlocks, Mountain Troll, Quirrell, and Basilisk.
- Mid route: Aragog, Fluffy, Horntail, mechanical boss gate, and post-Horntail entry systems.
- Late-hardmode route: Umbridge, Fenrir, Bellatrix, Barty Crouch Jr, Dementor King, and Voldemort readiness.
- Final route: Horcrux Hunt, Nagini / Battle of Hogwarts gates, Lord Voldemort summon and defeat, Deathly Hallows claim / purification / Master of Death attunement.
- Persistence checks: key boss defeat flags and final-route flags were verified after Save & Exit / reload.
- Release smoke: `dotnet build -c Release --no-restore` succeeds with 0 warnings / 0 errors, the generated `.tmod` loads in tModLoader, and `Mod Load Completed` appears in `client.log`.

Current verification snapshot:

- `python scripts/verify_assets.py` passes.
- `python scripts/verify_guide.py --strict` passes with `665 passed, 0 failed, 0 warnings`.
- `python scripts/scan_content.py --pretty` reports `597 C# files`, `624 PNGs`, and `1546 total` project files.

Remaining pre-public-release confidence work is limited to fresh-machine installs, longer balance runs, multiplayer sync checks, and native-speaker proofreading.

## Installation

1. Install **tModLoader** from Steam (free DLC for Terraria)
2. Install the **.NET 8 SDK** if not already installed
3. Copy the `WizardingWorld` folder to your tModLoader mod development directory:
   - Windows: `%userprofile%\Documents\My Games\Terraria\tModLoader\ModSources\`
4. Open tModLoader, go to **Workshop > Develop Mods > Build + Reload**
5. The mod will compile and load automatically

## Getting Started

When you first use a Life Crystal or defeat a boss, an owl will deliver your **Hogwarts Acceptance Letter** at dawn. This gives you a free **Oak Wand** and introduces the mod's systems.

**Your first steps:**
1. Craft an **Enchanting Table** (Wood + Books + Fallen Stars + Amethyst) at a Workbench
2. Use the Enchanting Table to craft better wands, potions, and magical gear
3. **Ollivander** the wandmaker will move in once you have a wand
4. Explore the world — a **Wizard Tower** has spawned with starter loot
5. Defeat magical creatures to collect **Essence of Magic** (universal crafting material)
6. Follow the **Boss Compass** and **Wizard's Almanac** through the 12-boss route, ending with **Lord Voldemort** and the Deathly Hallows finale

## Content Overview

### Wands (24: 19 combat, 4 utility, 1 upgrade)
| Tier | Wands | Spells |
|------|-------|--------|
| Pre-Boss | Oak, Alder, Willow | Stupefy, Expelliarmus |
| Post-Eye | Ash, Holly, Vine, Rowan, Birch, Red Oak | Incendio, Protego, Wingardium, Aguamenti, Bombarda, Levicorpus, Riddikulus |
| Post-Skeletron | Phoenix Feather, Dragon Heartstring, Hawthorn, Blackthorn, Cedar, Cypress, Larch | Sectumsempra, Chain Stupefy, Impedimenta, Conjunctivitis, Lumos Maxima, Finite Incantatem, Accio |
| Hardmode | Unicorn Hair, Yew, Elm, Ebony | Patronus, Crucio, Reducto, Reparo, Apparition |
| Post-Golem | Elder Wand, Fiendfyre Wand | Avada Kedavra, Fiendfyre |
| Mastery Path | Elder Wand mastery title | "Wand of Destiny" remains flavor text, not a separate item |

### House Signature Weapons
| House | Weapon | Playstyle |
|-------|--------|-----------|
| Gryffindor | Sword of Gryffindor | Melee + Venom |
| Slytherin | Slytherin's Dagger | Fast crit + Jinxed |
| Ravenclaw | Ravenclaw's Staff | Low-mana spell + mana reduction |
| Hufflepuff | Hufflepuff's Mace | Life steal + defense |

### Boss Route
| # | Boss | Main Gate |
|---|------|-----------|
| 1 | **Mountain Troll** | Early-game summon chain |
| 2 | **Quirrell** | Troll defeated + early vanilla progression |
| 3 | **Basilisk** | Quirrell defeated + Skeletron gate |
| 4 | **Aragog** | Hardmode entry |
| 5 | **Fluffy** | Mechanical boss gate |
| 6 | **Hungarian Horntail** | Mechanical boss gate |
| 7 | **Umbridge** | Post-Horntail |
| 8 | **Fenrir Greyback** | Post-Umbridge + Blood Moon |
| 9 | **Bellatrix Lestrange** | Post-Fenrir + Plantera |
| 10 | **Barty Crouch Jr** | Post-Bellatrix + Plantera |
| 11 | **Dementor King** | Post-Barty + Golem + night |
| 12 | **Lord Voldemort** | Post-Dementor King + Horcrux/Battle/Cultist readiness |

### Enemies (78; a selection)
Dementor, Acromantula, Cornish Pixie, Mountain Troll, Inferius, Thestral, Death Eater, Mandrake, Boggart, Doxy, Werewolf, Grindylow, Peeves, Nagini (mini-boss), Obscurus, Blast-Ended Skrewt, Sphinx, Giant, Snow Wraith, Cursed Mummy, Fwooper, Merfolk, Azkaban Guard, Bowtruckle (critter), Flobberworm (critter)

### Town NPCs (16; core examples)
| NPC | Condition | Sells |
|-----|-----------|-------|
| **Ollivander** | Own a wand | Wands, Spell Book, crafting materials |
| **Hagrid** | Defeat Basilisk | Creature items, pets, boss summons |
| **Potions Master** | 4+ NPCs | All potions, ingredients |
| **Dobby** | 6+ NPCs | Sweets, utility items, consumables |
| **Fred & George** | Defeat Basilisk | ALL Weasley products, Marauder items |
| **Centaur** | Defeat any boss | Detection/divination items |
| **Dumbledore** | Defeat Dementor King | Hallows guidance, later endgame items |

### Accessories (64; highlights)
- **Deathly Hallows**: true Invisibility Cloak, Resurrection Stone, Elder Wand
- **Stealth Gear**: Demiguise Weave Cloak, Camouflage Cloak, Stealth Draught
- **Horcruxes**: Riddle's Diary, Slytherin's Locket, Hufflepuff's Cup, Diadem of Ravenclaw
- **Iconic Items**: Philosopher's Stone, Time Turner, Marauder's Map, Triwizard Cup, Sorting Hat, Patronus Charm, Remembrall, Pensieve, Deluminator, Sneakoscope
- **Marauder Items**: Padfoot's Amulet (speed/stealth), Prongs' Charm (spell/summon boost)
- **Weasley Products**: Shield Hat, Extendable Ears
- **Expert Boss Drops**: Basilisk Eye, Dragon Heart, Soul Fragment
- **Endgame**: Master Wizard's Banner, Unbreakable Vow, Apparition Charm
- **Vanity**: Wizard Spectacles, Lightning Scar, Long Wizard Beard

### Armor Sets (8)
| Set | Theme | Set Bonus |
|-----|-------|-----------|
| Gryffindor | Damage | +15% damage, +10% melee speed |
| Slytherin | Crit | +12% crit chance |
| Ravenclaw | Magic | +20% spell damage, +40 mana, mana regen |
| Hufflepuff | Tank | +8 defense, +4 life regen, 30% thorns |
| Dark Wizard | Spell Power | +25% spell damage, +15% spell crit |
| Dragon Scale | Hardmode Spell | Fire/lava immunity, +18% spell damage |
| Wizard Robes | Vanity | Classic wizard aesthetic |
| Wizengamot | Endgame Spell | Arcane Authority: +30% spell damage, −20% mana cost, +60 mana, +8 mana regen |

### Mounts & Pets
- **Mounts**: Nimbus 2000 → Firebolt → Hippogriff → Nimbus 2001 (all flying, clear upgrade path)
- **Pets**: 6 total, including 1 light pet — Golden Snitch, Niffler, Hedwig, Kneazle, Pygmy Puff, Baby Dragon
- **Minions**: Phoenix (heals + attacks), House-Elf (teleports), Patronus Guardian (anti-Dementor, 2 slots)

### Potions (19)
Butterbeer, Felix Felicis, Polyjuice, Wolfsbane, Veritaserum, Amortentia, Gillyweed, Pepperup, Skele-Gro, and more

### Events & Systems
- **Death Eater Invasion** — 3-wave night event, trigger with Dark Mark or random
- **Azkaban's Despair** — prison-break survival event with despair buildup, Patronus dependence, and ward play
- **Quidditch Snitch Chase** — catch the Golden Snitch on a broomstick for rewards
- **Forbidden Forest Biome** — unique spawn pool at night in forests (post-Basilisk), exclusive Unicorn Blood drops
- **Wizard Tower** — world-gen structure with starter loot
- **Hogwarts Letter** — intro system for new players
- **Essence of Magic** — universal crafting material from all magical creatures
- **ModConfig** — customizable spawn rates, boss HP, damage scaling

### Custom Debuffs
| Debuff | Effect | Applied By |
|--------|--------|-----------|
| **Petrified** | Complete immobility | Basilisk, Sphinx, Giant |
| **Jinxed** | -20% damage, -15% speed, -5 defense | Impedimenta, Boggart, Decoy Detonator |
| **Dark Curse** | 8 HP/sec DoT, blocks healing, -10 defense | Voldemort, Death Eaters, Cursed Mummy |

## Configuration

Access mod settings via **Settings > Mod Configuration > Wizarding World**:
- Enemy Spawn Multiplier (0.1x - 5.0x)
- Boss Health Multiplier (0.5x - 5.0x)
- Spell Damage Multiplier (0.5x - 3.0x)
- Death Eater Invasion Chance (0x - 5.0x)
- Essence Drop Multiplier (0.5x - 5.0x)

## Sprite Art

The included in-game sprites are complete and release-checked. Asset coverage is tracked in `tools/generated_batches/manual_review_done.txt`, and `scripts/verify_assets.py` checks PNG readability, manual-review coverage, key-color residue, Buff icon sizing, and unexpected oversized files.

## Credits

- **Developer**: Xinyue (Lily) Feng
- **Tools**: code written with Claude Code (Anthropic); sprites generated with AI image generation from the prompts in `SPRITE_PROMPTS.md`
- **Game**: Terraria by Re-Logic
- **Modding Framework**: tModLoader
- **Inspiration**: J.K. Rowling's Harry Potter series, Fantastic Beasts

## Looking for help

This mod is in release-candidate shape. The core content pass is complete: in-game assets are present, release packaging is ready, debug-only QA tools are excluded from public Release builds, and the primary single-player route has been tested from early game through all 12 bosses, Voldemort, and the Deathly Hallows ending.

The remaining help wanted is focused on wider release confidence rather than adding more content. If any of these match what you'd like to work on, browse [open issues](https://github.com/SamSi0322/WizardingWorld/issues) or open a new one. See [CONTRIBUTING.md](CONTRIBUTING.md) for build setup.

Already completed:

- Primary single-player route QA from Hogwarts Letter through Voldemort and Deathly Hallows.
- Early, mid, post-Horntail, Umbridge, Fenrir, Bellatrix, Barty, Dementor King, Voldemort, and Hallows QA slices.
- Sprite coverage and asset verification.
- Custom spell, boss, enemy, and ambient audio pass.
- Release packaging, Workshop copy, and upload checklist.

| Need | What it looks like | Label |
|------|--------------------|-------|
| **Fresh-machine testers** | Install from a clean clone or Workshop-style package and confirm the mod builds, loads, and starts correctly outside the maintainer machine. | `fresh-install` |
| **Multiplayer-sync verifiers** | Specifically test `Common/Players/` and `Common/Systems/` paths in 2+ player co-op (save/load, host-vs-client desyncs). | `multiplayer-sync` |
| **Balance reviewers** | Run longer normal play sessions and flag obvious outliers in wand DPS, mana cost, boss HP curves, shop timing, drops, and summon costs. | `balance` |
| **Localization proofreaders** | Native-speaker proofreading for English, Simplified Chinese, and Traditional Chinese text in `Localization/`, especially quest guidance and boss route text. | `localization` |
| **Multiplayer playtesters** | Play the boss route or major systems in co-op and report progression, NPC shop, event, or world-save issues. | `co-op-test` |
| **Sprite polish artists** | Optional polish pass on existing generated sprites while preserving current content coverage and item readability. | `sprite-polish` |
| **Canon-audit reviewers** | Optional review for tone, naming, and lore consistency. Avoid large new content proposals unless they come with a clear scope. | `audit` |

Issues are tagged with the labels above. The maintainer has limited bandwidth, so:

- **Take ownership** — comment "I'll take this" on an issue, work on a fork, open a PR.
- **Small first PR** — a single sprite polish, a typo fix, a balance tweak with rationale. Big rewrites need an issue first.
- **Discussions** — design questions / ideas / "should we do X?" go in [GitHub Discussions](https://github.com/SamSi0322/WizardingWorld/discussions), not issues.

## License & IP disclaimer

The original code, configuration, and self-created assets in this repository (C# source, build scripts, SVG sprites, audio created for this mod) are released under the [MIT License](LICENSE).

This is an **unofficial fan project**. Harry Potter, Hogwarts, the wizarding-world setting, and all related names, characters, places, and indicia are trademarks of Warner Bros. Entertainment Inc., J.K. Rowling, and other rights holders. This mod is **not affiliated with, endorsed by, or sponsored by** any rights holder. The MIT license above applies only to the original code and self-created assets — it does not, and cannot, license any third-party intellectual property referenced by name within the mod.

Terraria is © Re-Logic. tModLoader is community-maintained. Neither is affiliated with this mod.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for build setup, code style, and what's in / out of scope. Architecture-level guidance lives in [CLAUDE.md](CLAUDE.md) and [AGENTS.md](AGENTS.md).
