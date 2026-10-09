"""
巫师世界 (Wizarding World) — 中文玩家指南 PDF 生成器

The Chinese guide has the same chapters and facts as the English one:
    scripts/content_manifest.json    counts            (scripts/scan_content.py)
    scripts/mechanical_data/*.json   boss stats         (scripts/export_mechanical_data.py)
    scripts/guide_content.json       structure, numbers and the English text
    scripts/zh_translations.json     Chinese text: 'ui' strings and 'guide', which mirrors guide_content.json
Cells left null in zh_translations.json (numbers, rarities, durations) come from guide_content.json,
so stats are maintained in one place. Chapters: scripts/guide_build.py; page design: scripts/guide_layout.py.

Needs a Chinese font. Found automatically on Windows (Microsoft YaHei / SimHei), macOS (Heiti SC) and
Linux (Noto Sans CJK: sudo apt-get install fonts-noto-cjk); or set WW_CJK_FONT=/path/to/font.ttc.

Usage:
    python scripts/scan_content.py
    python scripts/export_mechanical_data.py
    python generate_chinese_pdf.py            # writes WizardingWorld_Guide_ZH.pdf
    python generate_chinese_pdf.py --output path/to/out.pdf
"""

import argparse
import json
import os
import re
import sys

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_SCRIPT_DIR, "scripts"))

from guide_build import render  # noqa: E402


def _load(rel, hint):
    path = os.path.join(_SCRIPT_DIR, "scripts", rel)
    if not os.path.exists(path):
        sys.exit(f"ERROR: scripts/{rel} not found.\n{hint}")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


MANIFEST = _load("content_manifest.json", "Run  python scripts/scan_content.py  first.")
S = MANIFEST["summary"]
EN = _load("guide_content.json", "Restore it from git.")
ZH = _load("zh_translations.json", "This file holds the curated Chinese text of the guide.")
MECH_BOSSES = {b["id"]: b for b in _load("mechanical_data/bosses.json", "Run  python scripts/export_mechanical_data.py  first.")}


def merge(en, zh, path=""):
    """English structure with the Chinese text laid over it; null keeps the English value."""
    if zh is None:
        return en
    if isinstance(en, dict) and isinstance(zh, dict):
        if path.endswith("groups") and list(en) != list(zh):      # groups keyed by translated names
            return {zk: merge(ev, zv, f"{path}.{zk}") for (ek, ev), (zk, zv) in zip(en.items(), zh.items())}
        return {k: merge(v, zh.get(k), f"{path}.{k}") for k, v in en.items()}
    if isinstance(en, list) and isinstance(zh, list):
        if len(en) != len(zh):
            sys.exit(f"ERROR: zh_translations.json is out of date at {path}: "
                     f"{len(zh)} entries, guide_content.json has {len(en)}.")
        return [merge(a, b, f"{path}[{i}]") for i, (a, b) in enumerate(zip(en, zh))]
    return zh


T = merge(EN, ZH["guide"], "guide")

# Rarities and durations follow the English (code-checked) values.
RARITY, UNITS = ZH["ui"]["rarity"], ZH["ui"]["durations"]
for tier in T["wands"]["tiers"].values():
    for row in tier["rows"]:
        row[6] = RARITY.get(row[6], row[6])
for group in T["accessories"]["groups"]:
    for row in group["rows"]:
        row[1] = RARITY.get(row[1], row[1])
for row in T["potions"]["rows"]:
    row[1] = UNITS.get(row[1]) or re.sub(r"(\d+) min", r"\1 " + UNITS["min"], row[1])

# Anything still in English is a translation gap: report it rather than fail.
_ALLOWED = re.compile(r"^[\d\s,.+\-%/x×()<>:#]*$|^(HP|Boss|NPC|N/A|tModLoader.*|Wizarding World.*)$")


def gaps(en, zh, path=""):
    if isinstance(en, dict):
        for (ek, ev), (zk, zv) in zip(en.items(), zh.items()):
            if ek in ("col_widths", "overview_col_widths", "objects_col_widths", "id", "_meta", "hp", "dmg", "def"):
                continue
            yield from gaps(ev, zv, f"{path}.{zk}")
    elif isinstance(en, list):
        for i, (a, b) in enumerate(zip(en, zh)):
            yield from gaps(a, b, f"{path}[{i}]")
    elif isinstance(en, str) and en == zh and re.search(r"[A-Za-z]", en) and not _ALLOWED.match(en):
        yield f"{path}: {en[:60]}"


missing = list(gaps(EN, T, "guide"))
for line in missing[:20]:
    print("WARNING untranslated:", line)

# ===========================================================================
# Output
# ===========================================================================
_parser = argparse.ArgumentParser(description="Generate Wizarding World Chinese Guide PDF")
_parser.add_argument("--output", type=str, default=None, help="Output PDF path")
_args, _ = _parser.parse_known_args()

output_path = _args.output or os.path.join(_SCRIPT_DIR, "WizardingWorld_Guide_ZH.pdf")
pdf = render(output_path, T=T, EN=EN, L=ZH["ui"], S=S, mech_bosses=MECH_BOSSES, lang="zh", cjk=True)
print(f"PDF generated: {output_path}")
print(f"Total pages: {pdf.page_no()}  |  Chinese font: {os.path.basename(pdf.cjk_font_file)}")
print(f"Counts from manifest: {S['bosses']} 个Boss | {S['wands_base_combat']} 根战斗魔杖 | "
      f"{S['wands_active']} 根魔杖 | {S['accessories']} 件饰品 | untranslated cells: {len(missing)}")
