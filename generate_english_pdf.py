"""
Wizarding World - Player Guide PDF Generator (English)

Where the content comes from:
    scripts/content_manifest.json    counts            (scripts/scan_content.py)
    scripts/mechanical_data/*.json   boss stats         (scripts/export_mechanical_data.py)
    scripts/guide_content.json       curated text and tables, maintained by hand
    the mod's source + localization  summon items, recipes and sprites (scripts/guide_data.py)
The chapters live in scripts/guide_build.py and the page design in scripts/guide_layout.py;
both are shared with the Chinese guide.

Usage:
    python scripts/scan_content.py            # refresh the manifest first
    python scripts/export_mechanical_data.py
    python generate_english_pdf.py            # writes WizardingWorld_Guide_EN.pdf
    python generate_english_pdf.py --output path/to/out.pdf
"""

import argparse
import json
import os
import sys

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_SCRIPT_DIR, "scripts"))

from guide_build import render  # noqa: E402


def _load(rel, hint):
    path = os.path.join(_SCRIPT_DIR, "scripts", rel)
    if not os.path.exists(path):
        sys.exit(f"ERROR: scripts/{rel} not found.\nRun  {hint}  first.")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


MANIFEST = _load("content_manifest.json", "python scripts/scan_content.py")
S = MANIFEST["summary"]  # shorthand for counts
G = _load("guide_content.json", "git checkout scripts/guide_content.json")  # curated guide content
MECH_BOSSES = {b["id"]: b for b in _load("mechanical_data/bosses.json", "python scripts/export_mechanical_data.py")}

DOT = "  ·  "

# Interface strings. Everything else comes from guide_content.json.
LABELS = {
    "lang": "en",
    "running_title": "Wizarding World · Player Guide",
    "pdf_title": "Wizarding World: Player Guide",
    "pdf_subject": "Player guide for Wizarding World, a Harry Potter mod for Terraria (tModLoader)",
    "cover": {
        "kicker": "PLAYER GUIDE", "title": "Wizarding World", "subtitle": "A Harry Potter mod for Terraria",
        "footnote": f"For tModLoader 1.4.4+{DOT}Release candidate{DOT}Numbers generated from the mod's source",
    },
    "facts": {"bosses": "Bosses", "wands": "Wands", "creatures": "Creatures", "accessories": "Accessories",
              "town_npcs": "Town NPCs", "armor_sets": "Armor sets", "potions": "Potions", "languages": "Languages"},
    "contents": {"title": "Contents",
                 "intro": "Chapters 1 and 2 walk you through the game; the rest is reference. "
                          "Every entry below is a link."},
    "chapter_label": "Chapter",
    "chapters": {"1": "Getting Started", "2": "The Boss Route", "3": "Bosses", "4": "Wands & Spells",
                 "5": "Armor & House Weapons", "6": "Accessories", "7": "Potions & Consumables",
                 "8": "Mounts, Pets & Minions", "9": "Enemies", "10": "Town NPCs", "11": "Systems & Events",
                 "12": "Crafting Materials", "13": "The Deathly Hallows", "14": "Canon & Mod-Original"},
    "sections": {
        "how_to_use": "How to use this guide", "install": "Installing the mod", "first_steps": "Your first steps",
        "core_ideas": "Core ideas", "settings": "Mod settings", "endgame_goals": "Endgame goals",
        "armor_sets": "Armor sets ({n})", "house_weapons": "House signature weapons (4)",
        "potions": "Potions ({n})", "foods": "Foods and sweets", "utility": "Utility items",
        "mounts": "Mounts ({n})", "pets": "Pets ({n})", "minions": "Summon weapons (3)",
        "objectives": "Event objectives ({n})", "artifacts": "The three artifacts",
        "master_of_death": "Master of Death", "obtain": "How to obtain them",
    },
    "count_title": "{name} ({n})",
    "core_ideas": [["The Hogwarts Letter", "hogwarts_letter"], ["The Enchanting Table", "enchanting_table"],
                   ["The Wizard Tower", "wizard_tower"], ["Spell Damage", "spell_damage"],
                   ["The Forbidden Forest", "forbidden_forest"]],
    "settings_headers": ["Setting", "Range"],
    "callouts": {
        "helpers_title": "Not sure where to go next?",
        "final_battle_title": "Before the final battle",
        "final_battle_text": "Destroy the Horcruxes and hunt down Nagini first: every Horcrux you destroy weakens "
                             "Lord Voldemort. After him, the Deathly Hallows epilogue begins (Chapter 13).",
    },
    "endgame_extra": "Collect all {pets} pets and {mounts} mounts",
    "boss": {
        "hp": "HP", "damage": "Damage", "defense": "Defense",
        "phases": "Phases", "drops": "Drops", "expert": "Expert mode",
        "requirement": "{tier}. {requirement}",
        "summon": "Summon with: {item}, crafted at an Enchanting Table from {recipe}.",
        "summon_simple": "Summon with: {item}.",
        "count": "{name} x{n}", "list_sep": ", ", "or": " or ",
    },
    "systems_intro": "{n} systems run alongside the bosses: events, a sports season, a tournament, quest lines "
                     "in Diagon Alley and beyond, and the Battle of Hogwarts.",
    "hallows": ["Elder Wand", "Invisibility Cloak", "Resurrection Stone"],
    "back": {
        "title": "Wizarding World",
        "lines": ["{bosses} bosses" + DOT + "{wands_active} wands" + DOT + "{creatures} creatures" + DOT
                  + "{accessories} accessories",
                  "{armor_sets} armor sets" + DOT + "{potions} potions" + DOT + "{mounts} mounts" + DOT
                  + "{pets} pets" + DOT + "{town_npcs} town NPCs",
                  "English, Simplified Chinese and Traditional Chinese" + DOT + "tModLoader 1.4.4+"],
        "quote": "“After all this time?”  “Always.”",
        "credit": "Created by Xinyue (Lily) Feng" + DOT + "github.com/SamSi0322/WizardingWorld",
        "legal": "An unofficial, non-commercial fan project. Harry Potter names and characters are trademarks of "
                 "Warner Bros. Entertainment Inc. and J.K. Rowling; Terraria is © Re-Logic. Not affiliated "
                 "with or endorsed by any of them.",
    },
}

# ===========================================================================
# Output
# ===========================================================================
_parser = argparse.ArgumentParser(description="Generate Wizarding World English Guide PDF")
_parser.add_argument("--output", type=str, default=None, help="Output PDF path")
_args, _ = _parser.parse_known_args()

output_path = _args.output or os.path.join(_SCRIPT_DIR, "WizardingWorld_Guide_EN.pdf")
pdf = render(output_path, T=G, EN=G, L=LABELS, S=S, mech_bosses=MECH_BOSSES, lang="en")
print(f"PDF generated: {output_path}")
print(f"Total pages: {pdf.page_no()}")
print(f"Counts from manifest: {S['cs_files']} C# | {S['bosses']} bosses | {S['wands_active']} wands | {S['accessories']} acc")
