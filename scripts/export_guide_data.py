#!/usr/bin/env python3
"""
Wizarding World  -- Guide Content Exporter

Produces scripts/guide_content.json containing ALL curated guide data:
wand tables, boss data, enemy tables, NPC lists, accessory tables,
progression text, system descriptions, and lore-sensitive content.

This file is the SINGLE SOURCE OF TRUTH for guide narrative content.
The PDF generators read this file instead of hardcoding arrays.

IMPORTANT: This is manually maintained content, NOT auto-derived from code.
When you change game content, update this file to match.
The verification script checks for common stale patterns.

NOTE (2026): scripts/guide_content.json is now edited directly and is newer than the
snapshot below, which is kept only for reference. The script therefore refuses to
overwrite the JSON unless --force is given, and --check validates the JSON itself.

Usage:
    python scripts/export_guide_data.py --check     # validate guide_content.json's structure
    python scripts/export_guide_data.py --output x  # write the old snapshot elsewhere
    python scripts/export_guide_data.py --force     # overwrite guide_content.json with it
"""

import argparse
import json
import os
import sys
from pathlib import Path


def find_repo_root():
    here = Path(__file__).resolve().parent.parent
    if (here / "WizardingWorld.csproj").exists():
        return here
    for p in Path(__file__).resolve().parents:
        if (p / "WizardingWorld.csproj").exists():
            return p
    sys.exit("ERROR: cannot find WizardingWorld.csproj")


def build_guide_content() -> dict:
    """Build the complete guide content structure."""

    return {
        "_meta": {
            "generator": "scripts/export_guide_data.py",
            "type": "curated",
            "description": (
                "Manually maintained guide content. Update this file when game "
                "content changes. Verification checks for common stale patterns."
            ),
        },

        # ================================================================
        # SECTION 1: Getting Started
        # ================================================================
        "getting_started": {
            "hogwarts_letter": (
                "When you first reach 100 max HP (after using a Life Crystal) or defeat "
                "your first boss, an owl delivers a Hogwarts Acceptance Letter. This grants "
                "a free Oak Wand and unlocks Enchanting Table recipe knowledge."
            ),
            "enchanting_table": (
                "The Enchanting Table is the mod's core crafting station. Nearly every wand, "
                "armor piece, potion, and accessory requires it. Craft it early from basic "
                "materials at a Work Bench."
            ),
            "wizard_tower": (
                "A small Wizard Tower generates on the surface during world creation. It "
                "contains a chest with starter wizard loot: a wand, potions, and Essence "
                "of Magic. Only one spawns per world."
            ),
            "spell_damage": (
                "The mod adds a custom damage class: Spell Damage. All wands deal Spell "
                "Damage. Armor, accessories, and buffs that boost spell damage are clearly "
                "labeled. Spell Damage benefits from generic damage bonuses but has its own modifiers."
            ),
            "forbidden_forest": (
                "A custom biome that replaces normal forest spawns with magical creatures. "
                "Spawn diversity increases as more wizard bosses are defeated. The biome has "
                "increased spawn rates and drops exclusive materials like Unicorn Blood."
            ),
        },

        # ================================================================
        # SECTION 2: Wands
        # ================================================================
        "wands": {
            "intro": (
                "Wands are the primary weapons of the Wizarding World mod. All deal Spell "
                "Damage and require mana to cast. They are organized into tiers matching "
                "Terraria progression."
            ),
            "headers": ["Wand", "Spell", "Dmg", "Use", "Mana", "KB", "Rarity", "Notes"],
            "tiers": {
                "tier1": {
                    "name": "Tier 1 - Starter Wands (Pre-Boss)",
                    "col_widths": [32, 24, 10, 10, 12, 10, 14, 78],
                    "rows": [
                        ["Oak Wand", "Stupefy", "12", "30", "6", "3", "White", "Starter wand, basic stun bolt"],
                        ["Willow Wand", "Expelliarmus", "16", "25", "7", "7", "Blue", "High knockback disarming bolt"],
                        ["Alder Wand", "Stupefy", "17", "24", "6", "4", "Blue", "Faster Stupefy than Oak"],
                    ],
                },
                "tier2": {
                    "name": "Tier 2 - Early Game (Pre-Skeletron)",
                    "col_widths": [32, 36, 10, 10, 12, 10, 14, 66],
                    "rows": [
                        ["Ash Wand", "Incendio", "22", "20", "8", "4", "Blue", "Fire bolt, faster cast"],
                        ["Vine Wand", "Wingardium + Aguamenti", "25", "22", "9", "4", "Orange", "Hermione's wand, alternates spells"],
                        ["Holly Wand", "Expelliarmus + Protego", "28", "25", "10", "5", "Orange", "Harry's wand, 25% chance shield"],
                        ["Cedar Wand", "Lumos Maxima", "15", "35", "15", "2", "Orange", "Light + undead bonus damage"],
                        ["Red Oak Wand", "Riddikulus", "32", "22", "10", "4", "Orange", "Anti-Boggart charm; use Patronus for Dementors"],
                        ["Rowan Wand", "Bombarda", "30", "30", "12", "8", "Orange", "Explosive, high knockback"],
                        ["Phoenix Feather", "Incendio (double)", "30", "18", "10", "4", "Orange", "Chance for double fire shot"],
                    ],
                },
                "tier3": {
                    "name": "Tier 3 - Mid Game (Hardmode Entry)",
                    "col_widths": [32, 30, 10, 10, 12, 10, 14, 72],
                    "rows": [
                        ["Birch Wand", "Levicorpus", "28", "20", "10", "10", "Lt Red", "Flips enemies, highest KB wand"],
                        ["Blackthorn Wand", "Impedimenta", "35", "28", "14", "3", "Lt Red", "AoE slow jinx"],
                        ["Hawthorn Wand", "Chain Stupefy", "38", "22", "12", "4", "Lt Red", "Draco's wand, bounces between foes"],
                        ["Cypress Wand", "Conjunctivitis", "30", "35", "15", "2", "Lt Red", "Blinding curse"],
                        ["Dragon Heartstring", "Sectumsempra", "42", "15", "12", "5", "Lt Red", "Dark slashing curse, fast"],
                        ["Elm Wand", "Reparo", "1", "40", "25", "0", "Lt Red", "Repairs Protego shields, Room buffs, and wards"],
                        ["Larch Wand", "Finite Incantatem", "1", "30", "20", "0", "Lt Red", "Cleanse/dispel utility"],
                    ],
                },
                "tier4": {
                    "name": "Tier 4 - Late Hardmode",
                    "col_widths": [32, 32, 10, 10, 12, 10, 16, 68],
                    "rows": [
                        ["Unicorn Hair", "Expecto Patronum", "55", "35", "20", "3", "Pink", "Homing guardian, the anti-Dementor answer"],
                        ["Yew Wand", "Crucio + Reducto", "48", "8", "5", "2", "Lt Purple", "Voldemort's wand, channel beam + explosions"],
                        ["Ebony Wand", "Apparition", "1", "25", "30", "0", "Lt Purple", "Teleport spell (Rod of Discord-like)"],
                    ],
                },
                "tier5": {
                    "name": "Tier 5 - Endgame (Post-Boss)",
                    "col_widths": [32, 30, 10, 10, 12, 10, 14, 72],
                    "rows": [
                        ["Fiendfyre Wand", "Fiendfyre", "95", "25", "20", "4", "Yellow", "Cursed flames that grow + home"],
                        ["Elder Wand", "Avada Kedavra", "150", "18", "40", "6", "Red", "Drops from Voldemort, scales with missing mana (+20%)"],
                        ["Infernal Phoenix", "Incendio (triple)", "52", "16", "12", "4", "Lt Purple", "Upgrade of Phoenix Feather Wand, triple fire spread"],
                    ],
                },
            },
            "upgrade_note": (
                "* The Elder Wand drops from Voldemort. The Infernal Phoenix Wand is an "
                "upgrade of the Phoenix Feather Wand. The formerly separate Shadow Elder "
                "Wand and Wand of Destiny upgrade items have been retired into the Wand "
                "Mastery system. 'Wand of Destiny' persists only as Elder Wand mastery flavor."
            ),
        },

        # ================================================================
        # SECTION 3: Bosses
        # ================================================================
        "bosses": {
            "intro": (
                "The mod adds 12 bosses spanning Pre-Hardmode through endgame. Each has "
                "multiple phases, unique mechanics, and exclusive drops."
            ),
            "overview_headers": ["Boss", "Tier", "HP", "Dmg", "Def"],
            "overview_col_widths": [36, 42, 22, 18, 18],
            "list": [
                {
                    "name": "Mountain Troll",
                    "tier": "Pre-Eye of Cthulhu",
                    "hp": "2,000", "dmg": "30", "def": "8",
                    "phases": "P1: Walks slowly, club swings, shockwave stomps. P2 (<50%): Enraged, faster, throws rocks.",
                    "drops": "Troll Hide, Troll Club, Enchanted Troll Club",
                    "expert": "Troll Hide (+8 def, +10% KB resist)",
                },
                {
                    "name": "Professor Quirrell",
                    "tier": "Post-Eye of Cthulhu",
                    "hp": "3,500", "dmg": "35", "def": "12",
                    "phases": "P1 (Quirrell): Nervous, weak bolts. P2 (<60%, Voldemort reveals): Flies, green curses. P3 (<25%): Teleports, ring of projectiles.",
                    "drops": "Quirrell's Turban, spell components",
                    "expert": "Quirrell's Turban (+5% spell dmg, detect creatures)",
                },
                {
                    "name": "Basilisk",
                    "tier": "Pre-Hardmode (Post-Skeletron)",
                    "hp": "4,500", "dmg": "40", "def": "16",
                    "phases": "P1: Burrows underground, lunges. P2 (<50%): Fast charges + petrification gaze.",
                    "drops": "Basilisk Fang, Sword of Gryffindor, Basilisk Eye",
                    "expert": "Basilisk Eye (petrification gaze)",
                },
                {
                    "name": "Aragog",
                    "tier": "Early Hardmode",
                    "hp": "8,000", "dmg": "45", "def": "18",
                    "phases": "P1: Crawls toward player, spawns Acromantula minions. P2 (<40%): Web spit, faster, more spiders.",
                    "drops": "Aragog's Fang, Spider Silk Weave",
                    "expert": "Aragog's Fang (summon Acromantula minions)",
                },
                {
                    "name": "Fluffy",
                    "tier": "Post-Mechanical Bosses",
                    "hp": "18,000", "dmg": "60", "def": "25",
                    "phases": "P1: 3 cycling attacks (bite, pounce, bark shockwave). P2 (<50%): All heads attack, Jinxed on howl. P3 (<20%): Continuous charging + boulder barrage + pushback shockwaves. Music is its thematic weakness.",
                    "drops": "Three-Headed Collar, Cerberus Fang",
                    "expert": "Three-Headed Collar (+5 def, +3 max minions)",
                },
                {
                    "name": "Hungarian Horntail",
                    "tier": "Mid Hardmode",
                    "hp": "28,000", "dmg": "70", "def": "30",
                    "phases": "P1: Flies, shoots fireballs. P2 (<55%): Enraged charges, tail swipe, fire breath. P3 (<25%): Rapid attacks, fire rain.",
                    "drops": "Dragon Heart, Dragon Scale (x8+)",
                    "expert": "Dragon Heart (fire/lava immune, +12% spell dmg)",
                },
                {
                    "name": "Fenrir Greyback",
                    "tier": "Blood Moon Boss",
                    "hp": "25,000", "dmg": "75", "def": "22",
                    "phases": "P1: Fast charges, claw swipes, Bleeding. P2 (<50%): Full werewolf, howl spawns Werewolves. P3 (<20%): Berserk.",
                    "drops": "Lycan's Bite Mark, Werewolf Pelt",
                    "expert": "Lycan's Bite Mark (+20% melee, +15% night speed)",
                },
                {
                    "name": "Dolores Umbridge",
                    "tier": "Post-Mech Bosses",
                    "hp": "20,000", "dmg": "40", "def": "35",
                    "phases": "P1: Hovers, Educational Decree (Jinxed). P2 (<50%): Petrified on contact, summons swords. P3 (<20%): Panic, rapid teleport.",
                    "drops": "Ministry Badge, Umbridge's Quill",
                    "expert": "Ministry Badge (immune Jinxed/Confused, +5 def)",
                },
                {
                    "name": "Barty Crouch Jr",
                    "tier": "Post-Plantera",
                    "hp": "30,000", "dmg": "65", "def": "28",
                    "phases": "P1 (Moody disguise): Walks, bolts, heals. P2 (<70%, true form): Flies, rapid dark curses. P3 (<30%): Teleports, Death Eater minions.",
                    "drops": "Polyjuice Flask",
                    "expert": "Polyjuice Flask (+12% all dmg, +10% speed)",
                },
                {
                    "name": "Bellatrix Lestrange",
                    "tier": "Post-Plantera",
                    "hp": "35,000", "dmg": "70", "def": "30",
                    "phases": "P1: Hovers, Crucio/Stupefy, teleports. P2 (<60%): +Fiendfyre, faster teleport. P3 (<25%): Rapid-fire, 2 Death Eaters.",
                    "drops": "Bellatrix's Wand Hand, Blackthorn Wand",
                    "expert": "Bellatrix's Wand Hand (+20% spell dmg, -15% mana cost)",
                },
                {
                    "name": "Dementor King",
                    "tier": "Post-Golem (Penultimate Boss)",
                    "hp": "45,000", "dmg": "85", "def": "35",
                    "phases": "P1: Hovers, dark energy waves, spawns Dementors. P2 (<60%): 'The Kiss' beam drains HP. P3 (<25%): 'Soul Harvest' dark vortex, pull effect. Patronus active = +30% dmg to this boss.",
                    "drops": "Soul Siphon, Dementor's Shroud",
                    "expert": "Soul Siphon (3% life steal, enemies -5 def near you)",
                },
                {
                    "name": "Lord Voldemort",
                    "tier": "Post-Lunatic Cultist (True Final Boss)",
                    "hp": "60,000", "dmg": "80", "def": "40",
                    "phases": "P1: Teleports, killing curses. P2 (<55%): Death Eater minions, rapid barrage. P3 (<20%): Desperate fury, Horcrux shields, 12-bolt ring AoE. Weakened by Horcrux Hunt (100% -> 40% power).",
                    "drops": "Elder Wand (100%), Gaunt's Ring (100%), Soul Fragment (Expert)",
                    "expert": "Soul Fragment (+20% all dmg, +100 mana, +5% life steal, -20% max HP)",
                },
            ],
        },

        # ================================================================
        # SECTION 7: Town NPCs
        # ================================================================
        "town_npcs": {
            "intro": (
                "Sixteen town NPCs move in as you progress through the mod. "
                "Together they cover wandcraft, beasts, potions, travel, healing, "
                "resistance support, and late-game wizard services."
            ),
            "headers": ["NPC", "Shop Type", "Description"],
            "col_widths": [30, 30, 130],
            "rows": [
                ["Ollivander", "Wand Shop", "Sells basic wands and spell components. Check daily challenges here."],
                ["Hagrid", "Creature Shop", "Sells creature-related items, eggs, beast materials, and pet items."],
                ["Dobby", "Utility Shop", "Free house-elf. Sells utility items and socks. Loyal helper."],
                ["Potions Master", "Potion Shop", "Sells potion ingredients and pre-brewed potions."],
                ["Fred and George", "Joke/Combat Shop", "Weasleys' Wizard Wheezes. Sells pranks and combat consumables."],
                ["Dumbledore", "Endgame Shop + Hallows Guide", "Appears after defeating Voldemort. Hallows questline hub."],
                ["Centaur", "Nature Shop", "Forest-dwelling NPC. Sells nature and stargazing items."],
                ["Madam Rosmerta", "Hospitality / Owl Post", "Runs the Hogsmeade tavern, handles Owl Post, and anchors village-side errands."],
                ["Madam Hooch", "Quidditch Shop", "Provides Quidditch supplies, broom support items, and match-focused utility gear."],
                ["Kingsley Shacklebolt", "Order / Ministry Shop", "Supplies Order-aligned mission gear for Ministry and resistance operations."],
                ["Remus Lupin", "Defense / Moonward Shop", "Offers defensive tools and moonward support tied to the Whomping Willow and Shrieking Shack loop."],
                ["Aberforth Dumbledore", "Resistance Supply Shop", "Backroom resistance contact supporting D.A. operations and Battle of Hogwarts preparation."],
                ["Neville Longbottom", "Herbology / Resistance Shop", "Provides plant-based combat gear and support items as Hogwarts resistance escalates."],
                ["Goblin Teller", "Vault Services", "Handles Gringotts access, vault progression, and goblin financial services."],
                ["Mr Borgin", "Dark Curio Shop", "Runs Borgin and Burkes in Knockturn Alley with cursed wares and dark appraisal goods."],
                ["Healer", "Medical Shop", "Offers restorative supplies and medical support tied to St Mungo's treatment and triage progression."],
            ],
        },

        # ================================================================
        # SECTION 11: Custom Systems (corrected)
        # ================================================================
        "systems": [
            {
                "name": "Forbidden Forest Biome",
                "text": (
                    "A custom biome that replaces normal forest spawns with magical creatures. "
                    "Features increased spawn rates and drops Unicorn Blood as a rare exclusive. "
                    "Spawn diversity increases as more wizard bosses are defeated."
                ),
            },
            {
                "name": "Death Eater Invasion",
                "text": (
                    "Custom invasion event. Triggers randomly at night in Hardmode after defeating "
                    "the Basilisk, or manually with a Dark Mark item. Spawns waves of Death Eaters, "
                    "Dementors, and Inferi. Rewards Essence of Magic and rare drops."
                ),
            },
            {
                "name": "Quidditch Cup Season",
                "text": (
                    "A school sports loop built around broom play, scoring, and the Golden "
                    "Snitch. The Quidditch Cup is separate from the House Cup and House "
                    "Renown progression. Snitch chases, "
                    "Quidditch hoops, Madam Hooch support, and match rewards all feed this track."
                ),
            },
            {
                "name": "Triwizard Tournament",
                "text": (
                    "A champion event centered on the Goblet of Fire. The guide treats it as "
                    "a Hogwarts, Durmstrang, and Beauxbatons competition with champion "
                    "selection, task progression, lake-rescue sequences, and tournament rewards."
                ),
            },
            {
                "name": "House Renown System",
                "text": (
                    "Earn renown for your Hogwarts house through combat. Points grant milestone buffs:\n"
                    "- 50 renown: Minor House Buff\n"
                    "- 150 renown: Major House Buff (5 minutes)\n"
                    "- 500 renown: House Champion (massive all-stat boost, resets renown)\n"
                    "Renown decays 1 per 10 seconds to encourage active play."
                ),
                "canon_note": "Canon-inspired: renamed from 'House Points' since canonical points are awarded by professors.",
            },
            {
                "name": "Spell Combo System",
                "text": (
                    "Casting two specific spells in sequence on the same enemy triggers a bonus effect:\n"
                    "1. Stupefy + Incendio = 'Blazing Stun' (AoE fire explosion)\n"
                    "2. Expelliarmus + Sectumsempra = 'Disarming Slash' (massive crit)\n"
                    "3. Protego + any attack = 'Counter-Spell' (reflected damage doubled)\n"
                    "4. Impedimenta + Avada Kedavra = 'Execution' (instant kill non-boss <30% HP)\n"
                    "5. Stupefy + Riddikulus = 'Laughter Shield' (heal 50 HP)\n"
                    "6. Crucio + Fiendfyre = 'Hellfire Torment' (massive DoT stack)"
                ),
            },
            {
                "name": "Daily Wizard Challenge",
                "text": (
                    "A random daily task that rewards Essence of Magic. Changes every real-world day. "
                    "Completing the challenge grants 15-30 Essence + a random buff. "
                    "Check via Daily Prophet item or talking to Ollivander."
                ),
            },
            {
                "name": "Wizard Fishing",
                "text": (
                    "Magical fish and wizard loot added to fishing catches. Scales with fishing power and biome."
                ),
            },
            {
                "name": "Wand Mastery System",
                "text": (
                    "Wands gain power through use rather than crafting upgrades:\n"
                    "- Level 0 (New): Base stats\n"
                    "- Level 1 (Familiar, 100 XP): -5% mana cost\n"
                    "- Level 2 (Attuned, 400 XP): -10% mana cost, +5% damage\n"
                    "- Level 3 (Mastered, 1000 XP): -15% mana cost, +10% damage, golden visual\n"
                    "XP gained: 1 per enemy hit. Persisted per wand in save data.\n"
                    "The old Shadow Elder Wand / Wand of Destiny upgrade path is retired. "
                    "'Wand of Destiny' survives only as Elder Wand mastery flavor text."
                ),
                "canon_note": "Canon-inspired: 'The wand chooses the wizard'  -- loyalty earned through use.",
            },
            {
                "name": "Azkaban's Despair Event",
                "text": (
                    "A late-game survival event themed around the wizard prison Azkaban. Triggered "
                    "manually with an Azkaban Breach Stone after Golem. Floods the area with Dementors "
                    "and Azkaban Guards. Patronus, the Warden's Key, and Ward of Hope consumables are "
                    "the intended counter-mechanics. Light suppression and despair escalation make this "
                    "a survival challenge rather than a generic wave event."
                ),
                "canon_note": "Canon-faithful: Dementors are Azkaban's guards, appearing during dark crises.",
            },
            {
                "name": "Room of Requirement",
                "text": (
                    "A reusable key item that summons a magical room adapting to the player's needs. "
                    "The room detects current state and grants a 3-minute buff:\n"
                    "- Recovery Room (HP < 50%): +12 life regen, +15 def, +10% DR\n"
                    "- Training Room (holding wand): +20% spell dmg, +10 spell crit, +40 max mana\n"
                    "- Vault Room (carrying 10+ gold): luck boost, treasure sense\n"
                    "- Sanctuary Room (default): balanced defensive buffs\n"
                    "In late progression it also serves as the Resistance HQ for D.A. / Hogwarts "
                    "Resistance planning and Battle of Hogwarts staging. Crafted at the Enchanting "
                    "Table. Cannot be used while any Room buff is active."
                ),
                "canon_note": "Canon-faithful: 'I need a place to...'  -- the Room appears when someone has great need.",
            },
            {
                "name": "Diagon Alley and Gringotts",
                "text": (
                    "The Leaky Cauldron acts as the hidden gateway into Diagon Alley. From there, "
                    "Gringotts opens a cart descent into vault encounters, goblin services, and "
                    "treasure-focused progression."
                ),
            },
            {
                "name": "Knockturn Alley",
                "text": (
                    "A darker side street off Diagon Alley tied to Borgin and Burkes. Mr Borgin "
                    "handles cursed trade, dark appraisals, and sinister utility items for players "
                    "leaning into riskier wizard progression."
                ),
            },
            {
                "name": "Whomping Willow and Shrieking Shack Passage",
                "text": (
                    "The Whomping Willow conceals the route to the Shrieking Shack. This secret "
                    "passage loop emphasizes guarded transit, moonward preparation, and hidden "
                    "approach rather than a tourist landmark."
                ),
            },
            {
                "name": "St Mungo's Triage",
                "text": (
                    "A healing and recovery loop centered on St Mungo's and the Healer NPC. It "
                    "focuses on treatment, triage, restorative support, and emergency stabilization "
                    "rather than resurrection."
                ),
            },
            {
                "name": "Forbidden Forest Expeditions",
                "text": (
                    "Forest progression extends through multiple expedition routes, culminating in "
                    "the Thestral Clearing as the fourth expedition loop for late exploration."
                ),
            },
            {
                "name": "D.A. / Hogwarts Resistance",
                "text": (
                    "Late-game resistance content built around Dumbledore's Army, the "
                    "Hogwarts Resistance, castle-side preparation, and rallying defenders "
                    "through Aberforth, Neville, and allied support loops."
                ),
            },
            {
                "name": "Battle of Hogwarts",
                "text": (
                    "The final siege layer where Hogwarts Resistance systems, castle defenses, "
                    "rally buffs, and endgame story progression converge before the Voldemort finale."
                ),
            },
        ],

        # ================================================================
        # SECTION 13: Deathly Hallows
        # ================================================================
        "deathly_hallows": {
            "intro": (
                "The three Deathly Hallows form a hidden set bonus when all are equipped/held simultaneously."
            ),
            "artifacts": [
                "Elder Wand (weapon, held in inventory) - 150 base damage Avada Kedavra",
                "Invisibility Cloak (accessory, equipped) - Invisibility, -400 aggro, +5% damage",
                "Resurrection Stone (accessory, equipped) - +40 max HP, life regen",
            ],
            "master_of_death": (
                "When all three are active, the hidden 'Master of Death' state is awakened as "
                "a world milestone. Effects are survival-oriented: debuff immunities, detection, "
                "reduced aggro, corruption cleansing, moderate stat boosts, and one fate-style "
                "death rescue per Terraria day."
            ),
            "acquisition": [
                "Elder Wand: 100% drop from Lord Voldemort",
                "Invisibility Cloak: unique reward from Dumbledore after Azkaban's Despair + core Horcrux Hunt",
                "Resurrection Stone: awakened from Gaunt's Ring by Dumbledore after Voldemort falls",
            ],
        },

        # ================================================================
        # SECTION 14: Boss Progression
        # ================================================================
        "boss_progression": {
            "intro": "Recommended order for fighting bosses, aligned with Terraria's natural progression:",
            "headers": ["#", "Boss", "HP", "Tier", "Notes"],
            "col_widths": [8, 32, 22, 36, 92],
            "rows": [
                ["1", "Mountain Troll", "2,000 HP", "Pre-Eye of Cthulhu", "First boss. Gear: Oak/Willow/Alder Wand + Wizard Robes."],
                ["2", "Professor Quirrell", "3,500 HP", "Post-Eye of Cthulhu", "Second boss. Gear: Holly/Vine/Phoenix Feather Wand."],
                ["3", "Basilisk", "4,500 HP", "Post-Skeletron", "Unlocks Sword of Gryffindor. Final Pre-HM boss."],
                ["4", "Aragog", "8,000 HP", "Early Hardmode", "Giant spider. Spider Silk materials."],
                ["5", "Fluffy", "18,000 HP", "Post-Mech Bosses", "Three-headed dog. Music is its thematic weakness."],
                ["6", "Hungarian Horntail", "28,000 HP", "Mid Hardmode", "Dragon. Unlocks Dragon Scale armor."],
                ["7", "Fenrir Greyback", "25,000 HP", "Blood Moon", "Werewolf boss. Night-only."],
                ["8", "Dolores Umbridge", "20,000 HP", "Post-Mech Bosses", "The Debuff Boss. High defense, low damage."],
                ["9", "Barty Crouch Jr", "30,000 HP", "Post-Plantera", "Shapeshifter with 3 distinct phases."],
                ["10", "Bellatrix Lestrange", "35,000 HP", "Post-Plantera", "Aggressive duelist."],
                ["11", "Dementor King", "45,000 HP", "Post-Golem", "Penultimate boss. Patronus = +30% dmg bonus."],
                ["12", "Lord Voldemort", "60,000 HP", "Post-Lunatic Cultist", "True Final Boss. Weakened by Horcrux Hunt."],
            ],
            "endgame_goals": [
                "Destroy the core Horcruxes, reclaim the true cloak, and awaken the stone through Dumbledore",
                "Craft Wizengamot armor set (Post-Moon Lord ultimate spell armor)",
                "Master the Elder Wand through the Wand Mastery system",
                "Craft the Philosopher's Stone from all boss materials",
                "Complete the Dark Wizard armor set for max spell damage build",
                "Complete the Spell Combo system (all 6 combos)",
                "Reach House Champion status (500 House Renown)",
            ],
        },

        # ================================================================
        # ENEMIES (with corrected entries)
        # ================================================================
        "enemies": {
            "intro": (
                "51 enemies populate the wizarding world. Enemies are grouped by biome/category. "
                "21 of these are classified as Fantastic Beasts."
            ),
            "headers": ["Enemy", "Dmg", "Def", "HP", "Notes"],
            "groups": {
                "Surface / Forest / Forbidden Forest": {
                    "col_widths": [30, 12, 12, 18, 118],
                    "rows": [
                        ["Bowtruckle", "5", "0", "20", "Passive tree guardian. Fantastic Beast."],
                        ["Puffskein", "0", "0", "15", "Harmless, passive creature. Fantastic Beast."],
                        ["Billywig", "15", "2", "30", "Tiny flying insect. Fantastic Beast."],
                        ["Jarvey", "18", "4", "60", "Aggressive ferret. Fast ground enemy."],
                        ["Knarl", "22", "8", "45", "Spiny hedgehog. Rages when hurt. Fantastic Beast."],
                        ["MagicPixie", "18", "4", "50", "Cornish Pixie. Fast, annoying flyer."],
                        ["Mooncalf", "0", "0", "30", "Passive nocturnal creature. Fantastic Beast."],
                        ["Diricawl", "0", "0", "25", "Teleporting bird. Fantastic Beast."],
                        ["Mandrake", "20", "6", "80", "Screaming plant. Inflicts Confused."],
                        ["Zouwu", "70", "24", "800", "Powerful cat-like beast. Fantastic Beast."],
                        ["Thestral", "40", "16", "300", "Skeletal winged horse. Fantastic Beast."],
                        ["Demiguise", "0", "0", "60", "Invisible creature. Drops Demiguise Hair. Fantastic Beast."],
                        ["Fwooper", "28", "6", "100", "Colorful bird. Fantastic Beast."],
                        ["DuelingDummy", "0", "0", "999,999", "Training dummy. DPS testing."],
                    ],
                },
                "Underground / Caverns": {
                    "col_widths": [30, 12, 12, 18, 118],
                    "rows": [
                        ["Flobberworm", "0", "0", "5", "Completely harmless worm."],
                        ["Horklump", "0", "0", "10", "Mushroom creature. Passive."],
                        ["Streeler", "25", "16", "100", "Giant snail. Poisonous trail."],
                        ["Boggart", "30", "10", "200", "Shapeshifter. Inflicts fear. Weak to Riddikulus."],
                        ["Acromantula", "35", "14", "250", "Giant magical spider."],
                        ["GoblinRebel", "30", "12", "150", "Rebel goblin. Throws coin projectiles."],
                        ["Runespoor", "40", "14", "250", "Three-headed serpent. Fantastic Beast."],
                    ],
                },
                "Sky / Floating Islands": {
                    "col_widths": [30, 12, 12, 18, 118],
                    "rows": [
                        ["Jobberknoll", "0", "0", "20", "Passive sky bird. Fantastic Beast."],
                        ["Occamy", "45", "16", "350", "Serpentine flyer. Fantastic Beast."],
                        ["PeruvianVipertooth", "55", "18", "350", "Small dragon. Fantastic Beast."],
                        ["Thunderbird", "65", "22", "500", "Storm bird. Fantastic Beast."],
                    ],
                },
                "Ocean / Water": {
                    "col_widths": [30, 12, 12, 18, 118],
                    "rows": [
                        ["Grindylow", "25", "8", "120", "Aggressive underwater creature."],
                        ["Merfolk", "35", "12", "200", "Water warrior."],
                    ],
                },
                "Jungle": {
                    "col_widths": [30, 12, 12, 18, 118],
                    "rows": [
                        ["Dugbog", "35", "10", "150", "Swamp creature. Fantastic Beast."],
                        ["BlastEndedSkrewt", "55", "28", "450", "Armored from front. Fantastic Beast."],
                        ["Erumpent", "80", "25", "700", "Explodes on contact. Fantastic Beast."],
                        ["Nundu", "90", "30", "1,500", "Most dangerous beast. Fantastic Beast."],
                    ],
                },
                "Desert": {
                    "col_widths": [30, 12, 12, 18, 118],
                    "rows": [
                        ["CursedMummy", "45", "18", "300", "Applies Dark Curse on hit."],
                        ["Sphinx", "60", "35", "1,200", "Ancient guardian. Fantastic Beast."],
                    ],
                },
                "Snow": {
                    "col_widths": [30, 12, 12, 18, 118],
                    "rows": [
                        ["SnowWraith", "40", "14", "220", "Ice-elemental magical spirit."],
                    ],
                },
                "Dungeon": {
                    "col_widths": [30, 12, 12, 18, 118],
                    "rows": [
                        ["Inferius", "50", "18", "350", "Dark undead creature. Hardmode dungeon."],
                        ["Peeves", "25", "8", "180", "Hogwarts poltergeist. Dungeon-only. Throws objects."],
                    ],
                },
                "Corruption / Crimson": {
                    "col_widths": [30, 12, 12, 18, 118],
                    "rows": [
                        ["CursedSpecter", "60", "18", "450", "Cursed ghost. Shoots Cursed Flame."],
                    ],
                },
                "Hallow": {
                    "col_widths": [30, 12, 12, 18, 118],
                    "rows": [
                        ["Phantom Stag", "55", "20", "400", "Spectral mockery of a Patronus. Mod-original."],
                    ],
                },
                "Underworld": {
                    "col_widths": [30, 12, 12, 18, 118],
                    "rows": [
                        ["Ashwinder", "35", "8", "120", "Fire snake. Drops Ashwinder Egg."],
                        ["MagicalImp", "25", "6", "70", "Shoots fire balls."],
                        ["FireCrab", "45", "22", "280", "Armored shell. Fantastic Beast."],
                    ],
                },
                "Dark Events / Contextual": {
                    "col_widths": [30, 12, 12, 18, 118],
                    "rows": [
                        ["Dementor", "55", "20", "400", "Azkaban's guards. Blood Moon / Invasions / Forbidden Forest / Azkaban event."],
                        ["DeathEater", "60", "25", "500", "Cloaked dark wizard. Invasion / event enemy."],
                        ["Werewolf", "65", "22", "500", "Fast, powerful full moon enemy."],
                        ["Giant", "90", "30", "2,000", "Very slow, devastating."],
                        ["Lethifold", "70", "15", "600", "Living shroud of darkness."],
                        ["Obscurus", "70", "25", "800", "Dark parasitic force (not a beast). Rare."],
                        ["AzkabanGuard", "75", "30", "800", "Prison warden. Azkaban event."],
                    ],
                },
                "Special / Unique": {
                    "col_widths": [30, 12, 12, 18, 118],
                    "rows": [
                        ["Nagini", "55", "20", "3,000", "Voldemort's serpent. Mini-boss. Horcrux Hunt target."],
                        ["Doxy", "22", "2", "35", "Tiny venomous fairy. Swarms."],
                        ["Troll (enemy)", "45", "22", "600", "Cavern troll. Slow but tanky."],
                    ],
                },
            },
        },

        # ================================================================
        # Canon Disclosure
        # ================================================================
        "canon_disclosure": {
            "intro": (
                "The Wizarding World mod draws heavily from the Harry Potter series. "
                "Most content is faithful to the source material, but some mechanics "
                "are adapted or original for gameplay reasons."
            ),
            "categories": [
                {
                    "label": "Canon-faithful",
                    "description": "Directly faithful to books/films",
                    "examples": [
                        "Elder Wand as the single Deathly Hallow wand (not a separate Wand of Destiny item)",
                        "True Invisibility Cloak as a unique, non-craftable heirloom",
                        "Resurrection Stone tied to Gaunt's Ring",
                        "Riddikulus as the anti-Boggart charm (not anti-Dementor)",
                        "Patronus as the primary anti-Dementor defense",
                        "Dementors tied to Azkaban, dark events, and narrative context",
                        "Fluffy's weakness is music/sleep",
                    ],
                },
                {
                    "label": "Canon-inspired adaptations",
                    "description": "Based on canon concepts but adapted for Terraria gameplay",
                    "examples": [
                        "Wand Mastery system (loyalty through use, inspired by 'the wand chooses the wizard')",
                        "House Renown (combat-based; canonical House Points are professor-awarded)",
                        "Reparo repairs magical wards and buffs (canon repairs objects; adapted for gameplay utility)",
                        "Horcrux Hunt weakens Voldemort mechanically (narrative simplification of book 7)",
                        "Spell Combo system (original mechanic inspired by wizard dueling)",
                    ],
                },
                {
                    "label": "Mod-original content",
                    "description": "Original gameplay content not from the source material",
                    "examples": [
                        "Phantom Stag (Hallow biome enemy, not a real corrupted Patronus)",
                        "Room of Requirement as a buff-granting key item",
                        "Dark Arts Corruption meter",
                        "Spell Damage as a custom tModLoader damage class",
                        "Infernal Phoenix Wand (upgrade of Phoenix Feather Wand)",
                    ],
                },
            ],
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Export guide content data")
    parser.add_argument("--check", action="store_true", help="Validate guide_content.json's structure")
    parser.add_argument("--output", type=str, default=None, help="Output file path")
    parser.add_argument("--force", action="store_true",
                        help="Overwrite guide_content.json with this script's older snapshot")
    args = parser.parse_args()

    root = find_repo_root()
    json_path = root / "scripts" / "guide_content.json"

    if args.check:
        with open(json_path, encoding="utf-8") as f:
            content = json.load(f)
    else:
        content = build_guide_content()

    if args.check:
        # Structural validation
        errors = []
        if "wands" not in content:
            errors.append("Missing wands section")
        if "bosses" not in content:
            errors.append("Missing bosses section")
        if len(content["bosses"]["list"]) != 12:
            errors.append(f"Boss count is {len(content['bosses']['list'])}, expected 12")
        if len(content["boss_progression"]["rows"]) != 12:
            errors.append(f"Progression rows is {len(content['boss_progression']['rows'])}, expected 12")

        # Count wand rows
        total_wand_rows = sum(
            len(t["rows"]) for t in content["wands"]["tiers"].values()
        )
        print(f"Wand rows in guide: {total_wand_rows}")
        print(f"Boss entries: {len(content['bosses']['list'])}")
        print(f"Enemy groups: {len(content['enemies']['groups'])}")
        print(f"Town NPC rows: {len(content['town_npcs']['rows'])}")
        print(f"System entries: {len(content['systems'])}")

        if errors:
            for e in errors:
                print(f"  ERROR: {e}")
            sys.exit(1)
        else:
            print("Structure OK")
        return

    if not args.output and json_path.exists() and not args.force:
        sys.exit("guide_content.json is edited by hand now and is newer than this script's snapshot.\n"
                 "Not overwriting it. Use --check to validate it, --output to write the snapshot elsewhere,\n"
                 "or --force to replace the JSON with the old snapshot.")
    output_path = args.output or str(json_path)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=2, ensure_ascii=False)

    print(f"Guide content written to: {output_path}")


if __name__ == "__main__":
    main()
