"""Facts the player guides read straight from the mod's source.

Anything here is derived from the C# code and the localization files, so the
guides cannot drift from the game: boss summon items and their recipes, item
display names, and the sprites used as icons and portraits.
"""

import os
import re
from functools import lru_cache

import hjson_lite

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Route order, internal names. Matches the summon gates in WizardConditions.cs.
BOSS_IDS = [
    "TrollBoss", "QuirrellBoss", "BasiliskBoss", "AragogBoss", "FluffyBoss", "HorntailBoss",
    "UmbridgeBoss", "FenrirBoss", "BellatrixBoss", "BartyCrouchBoss", "DementorKingBoss", "VoldemortBoss",
]

# Sprite-sheet layout of the boss art (columns per row), from WizardingBossArtDrawSystem.cs.
BOSS_ART_COLUMNS = {"BasiliskBoss": 3}

_LOC_FILES = {
    "en": "en-US_Mods.WizardingWorld.hjson",
    "zh": "zh-Hans_Mods.WizardingWorld.hjson",
}


@lru_cache(maxsize=None)
def localization(lang):
    return hjson_lite.load(os.path.join(ROOT, "Localization", _LOC_FILES[lang]))


def display_name(kind, internal, lang="en"):
    """DisplayName of a mod item/NPC as the game shows it, or None."""
    loc = localization(lang)
    for key in (f"Mods.WizardingWorld.{kind}.{internal}.DisplayName", f"{kind}.{internal}.DisplayName"):
        value = loc.get(key)
        if value:
            return hjson_lite.clean(value)
    return None


def vanilla_name(item_id):
    """ItemID.SoulofNight -> 'Soul of Night'."""
    words = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", item_id)
    return re.sub(r"\b(\w+?)of\b", r"\1 of", words).replace("  ", " ")


@lru_cache(maxsize=None)
def _source_index():
    """Map class name -> .cs path for everything under Content/."""
    index = {}
    for base, _dirs, files in os.walk(os.path.join(ROOT, "Content")):
        for f in files:
            if f.endswith(".cs"):
                index[f[:-3]] = os.path.join(base, f)
    return index


def source_of(internal):
    path = _source_index().get(internal)
    if not path:
        return ""
    with open(path, encoding="utf-8") as f:
        return f.read()


_INGREDIENT = re.compile(
    r"AddIngredient\(\s*(?:ItemID\.(\w+)|ModContent\.ItemType<(?:[\w.]+\.)?(\w+)>\(\))\s*(?:,\s*(\d+))?\s*\)")


def recipes(internal, lang="en", vanilla_names=None):
    """Every recipe of a mod item as [(ingredient name, count), ...] lists."""
    src = source_of(internal)
    out = []
    for chunk in src.split("CreateRecipe(")[1:]:
        chunk = chunk.split(".Register()")[0]
        items = []
        for vanilla, mod, count in _INGREDIENT.findall(chunk):
            if vanilla:
                name = (vanilla_names or {}).get(vanilla) or vanilla_name(vanilla)
            else:
                name = display_name("Items", mod, lang) or vanilla_name(mod)
            items.append((name, int(count or 1)))
        if items:
            out.append(items)
    return out


def summon_item(boss_id):
    """Internal name of the item that summons a boss (TrollBoss -> TrollSummonItem)."""
    return boss_id[:-4] + "SummonItem" if boss_id.endswith("Boss") else None


# ---------------------------------------------------------------------------
# Sprites
# ---------------------------------------------------------------------------

@lru_cache(maxsize=None)
def _png_index():
    """Lower-cased sprite name -> path. Item and NPC sprites only (no tiles, buffs or projectiles)."""
    index = {}
    for sub in ("Items", "NPCs", "Pets", "Mounts"):
        for base, _dirs, files in os.walk(os.path.join(ROOT, "Content", sub)):
            for f in files:
                if f.endswith(".png") and "_" not in f:
                    index.setdefault(f[:-4].lower(), os.path.join(base, f))
    return index


def sprite(internal):
    return _png_index().get(internal.lower())


def internal_name(display):
    """Best-effort 'Hufflepuff's Mace' -> 'HufflepuffsMace'."""
    return re.sub(r"[^A-Za-z0-9]", "", display.replace("&", "And"))


def icon_for(display, aliases=None):
    """Sprite path for a row label shown in a guide table, if one exists."""
    key = (aliases or {}).get(display) or internal_name(display)
    for candidate in (key, key + "Item", key + "Wand", key + "MountItem", key + "PetItem", key + "Summon"):
        path = sprite(candidate)
        if path:
            return path
    return None


def _npc_internal(display):
    loc = localization("en")
    wanted = display.strip().lower()
    for key, value in loc.items():
        if key.endswith(".DisplayName") and ".NPCs." in "." + key and value.strip().lower() == wanted:
            return key.split(".")[-2]
    return internal_name(display)


def npc_icon(display, aliases=None):
    """(sprite path, frame count) for an enemy or town NPC row, or None."""
    internal = (aliases or {}).get(display) or _npc_internal(display)
    path = sprite(internal)
    if not path or os.sep + "NPCs" + os.sep not in path:
        return None
    m = re.search(r"npcFrameCount\[Type\]\s*=\s*(\d+)", source_of(internal))
    return path, int(m.group(1)) if m else 1


def boss_head(boss_id):
    """The small map icon tModLoader shows for a boss."""
    folder = os.path.dirname(sprite(boss_id) or "")
    path = os.path.join(folder, boss_id + "_Head_Boss.png")
    return path if os.path.exists(path) else None


def boss_sheet(boss_id):
    """(path, columns, frame_count) for a boss's art sheet."""
    path = sprite(boss_id)
    src = source_of(boss_id)
    m = re.search(r"npcFrameCount\[Type\]\s*=\s*(\d+)", src)
    return path, BOSS_ART_COLUMNS.get(boss_id, 4), int(m.group(1)) if m else 1
