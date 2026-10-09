"""The player guide's chapters, in any language.

build_guide() lays out the whole guide from
    T   the curated content in the target language (same shape as guide_content.json)
    EN  the English content, used to find each table row's sprite
    L   the language's interface strings (chapter titles, labels, cover text)
    S   counts from content_manifest.json
so the English and Chinese guides always have the same chapters, tables and facts.
"""

import os

import guide_data as data
from guide_layout import ART_DIR, MUTED, GuidePDF, boss_portrait

ART = {name: os.path.join(ART_DIR, f"wizardingworld-{name}.png")
       for name in ("poster-vertical", "banner-wide", "cover-16x9")}

# Row labels (English) whose sprite has a different internal name.
ICON_ALIASES = {
    "Nimbus 2000": "Nimbus2000Item", "Nimbus 2001": "Nimbus2001Item", "Firebolt": "FireboltItem",
    "Hippogriff": "HippogriffItem", "Thestral": "ThestralItem",
    "Hedwig": "OwlTreat", "Niffler": "NifflerPouch", "Golden Snitch": "GoldenSnitchItem", "Kneazle": "CatTreats",
    "Baby Dragon": "DragonEgg", "Pygmy Puff": "PygmyPuffItem",
    "Demiguise Weave Cloak": "DemiguiseCloak", "Triwizard Cup": "ChampionsTrophy",
    "Fred and George": "FredAndGeorge", "Kingsley Shacklebolt": "Kingsley", "Remus Lupin": "Lupin",
    "Aberforth Dumbledore": "Aberforth", "Neville Longbottom": "Neville", "Mr Borgin": "MrBorgin",
    "Dueling Dummy Item": "DuelingDummyItem", "Bertie Bott's Beans": "BertieBottsBeans",
    "Mandrake Restorative": "MandrakeRestorative", "Forest Warden's Badge": "ForestWarden",
    "Order of the Phoenix Badge": "OrderBadge", "Prongs Charm": "ProngsCharm", "Padfoot Amulet": "PadfootAmulet",
    "Troll (enemy)": "Troll",
}


def _icons(rows):
    return [data.icon_for(str(r[0]), ICON_ALIASES) for r in rows]


def _armor_icon(set_name):
    """The set's chest piece stands in for the whole set."""
    base = set_name.replace(" ", "")
    for candidate in (base + "Robes", base + "Breastplate", base.replace("Robes", "Robe")):
        if data.sprite(candidate):
            return data.sprite(candidate)
    return None


def _boss_stats(boss, mech_bosses, L):
    mech = mech_bosses.get(boss["id"], {})
    hp = mech.get("lifeMax_base") or mech.get("lifeMax")
    dmg = mech.get("damage_base") or mech.get("damage")
    defense = mech.get("defense_base") or mech.get("defense")
    b = L["boss"]
    return [(b["hp"], f"{hp:,}" if hp else boss["hp"]),
            (b["damage"], str(dmg if dmg is not None else boss["dmg"])),
            (b["defense"], str(defense if defense is not None else boss["def"]))]


def _summon_line(boss_id, L, lang):
    b = L["boss"]
    item = data.summon_item(boss_id)
    name = L.get("item_names", {}).get(item) or data.display_name("Items", item, lang) \
        or data.display_name("Items", item) or item
    recipes = data.recipes(item, lang, vanilla_names=L.get("vanilla_items"))
    if not recipes:
        return b["summon_simple"].format(item=name)
    fmt = lambda n, c: b["count"].format(name=n, n=c) if c > 1 else n  # noqa: E731
    parts = [b["list_sep"].join(fmt(n, c) for n, c in r) for r in recipes]
    return b["summon"].format(item=name, recipe=b["or"].join(parts))


def build_guide(*, T, EN, L, S, mech_bosses, lang="en", cjk=False, toc_pages=None):
    creatures = sum(len(g["rows"]) for g in T["enemies"]["groups"].values())
    objectives = len(T["enemies"]["objects"])
    F, C, SEC = L["facts"], L["chapters"], L["sections"]

    pdf = GuidePDF(running_title=L["running_title"], cjk=cjk,
                   labels={"contents": L["contents"]["title"], "chapter": L["chapter_label"]})
    pdf.set_title(L["pdf_title"])
    pdf.set_author("Xinyue (Lily) Feng")
    pdf.set_subject(L["pdf_subject"])
    pdf.set_lang(L["lang"])

    pdf.cover(art=ART["poster-vertical"], title=L["cover"]["title"], subtitle=L["cover"]["subtitle"],
              kicker=L["cover"]["kicker"],
              facts=[(S["bosses"], F["bosses"]), (S["wands_active"], F["wands"]), (creatures, F["creatures"]),
                     (S["accessories"], F["accessories"]), (S["town_npcs"], F["town_npcs"])],
              footnote=L["cover"]["footnote"])
    pdf.contents_page(intro=L["contents"]["intro"], pages=toc_pages)

    # 1. Getting started -----------------------------------------------------
    gs = T["getting_started"]
    pdf.chapter(1, C["1"], gs["welcome"], art=ART["cover-16x9"], focus_x=0.5)
    pdf.stat_grid([(S["bosses"], F["bosses"]), (S["wands_active"], F["wands"]), (creatures, F["creatures"]),
                   (S["accessories"], F["accessories"]), (S["armor_sets"], F["armor_sets"]),
                   (S["potions"], F["potions"]), (S["town_npcs"], F["town_npcs"]), (3, F["languages"])])
    pdf.section(SEC["how_to_use"])
    pdf.para(gs["how_to_use"])
    pdf.section(SEC["install"])
    pdf.bullets(gs["install"], numbered=True)
    pdf.note(gs["install_note"])
    pdf.section(SEC["first_steps"])
    pdf.bullets(gs["first_steps"], numbered=True)
    pdf.callout(L["callouts"]["helpers_title"], gs["helpers"])
    pdf.section(SEC["core_ideas"])
    for title, key in L["core_ideas"]:
        pdf.subheading(title)
        pdf.para(gs[key])
    pdf.section(SEC["settings"])
    pdf.data_table(L["settings_headers"], gs["settings"], [60, 40])
    pdf.note(gs["settings_note"])

    # 2. The boss route ------------------------------------------------------
    prog = T["boss_progression"]
    pdf.chapter(2, C["2"], prog["intro"], art=ART["banner-wide"], focus_x=0.12)
    pdf.data_table(prog["headers"], prog["rows"], prog["col_widths"],
                   icons=[data.boss_head(b["id"]) for b in EN["bosses"]["list"]],
                   aligns=["C", "L", "R", "L", "L"], bold_first=False)
    pdf.callout(L["callouts"]["final_battle_title"], L["callouts"]["final_battle_text"], tone="purple")
    pdf.section(SEC["endgame_goals"])
    pdf.bullets(prog["endgame_goals"] + [L["endgame_extra"].format(pets=S["pets"], mounts=S["mounts"])])

    # 3. Bosses ----------------------------------------------------------------
    bosses = T["bosses"]
    pdf.chapter(3, C["3"], bosses["intro"], art=ART["banner-wide"], focus_x=0.88)
    for i, (b, b_en) in enumerate(zip(bosses["list"], EN["bosses"]["list"]), 1):
        sheet, cols, frames = data.boss_sheet(b_en["id"])
        pdf.boss_card(
            number=i, name=b["name"], portrait=boss_portrait(sheet, cols, frames), bookmark=b["name"],
            stats=_boss_stats(b_en, mech_bosses, L),
            requirement=L["boss"]["requirement"].format(tier=b["tier"], requirement=b["requirement"]),
            summon=_summon_line(b_en["id"], L, lang),
            blocks=[(L["boss"]["phases"], b["phases"]), (L["boss"]["drops"], b["drops"]),
                    (L["boss"]["expert"], b["expert"])],
        )

    # 4. Wands -----------------------------------------------------------------
    wands = T["wands"]
    pdf.chapter(4, C["4"], wands["intro"], art=ART["cover-16x9"], focus_x=0.52)
    for tier_key in ["tier1", "tier2", "tier3", "tier4", "tier5"]:
        tier = wands["tiers"][tier_key]
        pdf.section(tier["name"].replace(" - ", ": "))
        pdf.data_table(wands["headers"], tier["rows"], tier["col_widths"],
                       icons=_icons(EN["wands"]["tiers"][tier_key]["rows"]),
                       aligns=["L", "L", "R", "R", "R", "R", "L", "L"])
    pdf.note(wands["upgrade_note"].lstrip("* "))
    pdf.note(wands["utility_note"])

    # 5. Armor and house weapons ------------------------------------------------
    armor, weapons = T["armor"], T["house_weapons"]
    pdf.chapter(5, C["5"], armor["intro"], art=ART["banner-wide"], focus_x=0.35)
    pdf.section(SEC["armor_sets"].format(n=S["armor_sets"]))
    pdf.data_table(armor["headers"], armor["rows"], armor["col_widths"],
                   icons=[_armor_icon(r[0]) for r in EN["armor"]["rows"]], aligns=["L", "L", "C", "R", "L", "L"])
    pdf.section(SEC["house_weapons"])
    pdf.para(weapons["intro"])
    pdf.data_table(weapons["headers"], weapons["rows"], weapons["col_widths"],
                   icons=_icons(EN["house_weapons"]["rows"]), aligns=["L", "L", "L", "R", "R", "R", "L"])

    # 6. Accessories -------------------------------------------------------------
    acc = T["accessories"]
    pdf.chapter(6, C["6"], acc["intro"], art=ART["cover-16x9"], focus_x=0.2)
    for group, group_en in zip(acc["groups"], EN["accessories"]["groups"]):
        pdf.section(L["count_title"].format(name=group["name"], n=len(group["rows"])))
        pdf.data_table(acc["headers"], group["rows"], acc["col_widths"], icons=_icons(group_en["rows"]))

    # 7. Potions and consumables -------------------------------------------------
    pdf.chapter(7, C["7"], T["potions"]["intro"], art=ART["banner-wide"], focus_x=0.62)
    pdf.section(SEC["potions"].format(n=S["potions"]))
    pdf.data_table(T["potions"]["headers"], T["potions"]["rows"], T["potions"]["col_widths"],
                   icons=_icons(EN["potions"]["rows"]), aligns=["L", "C", "L"])
    for key, title in (("foods", SEC["foods"]), ("utility_items", SEC["utility"])):
        pdf.section(title)
        pdf.data_table(T[key]["headers"], T[key]["rows"], T[key]["col_widths"], icons=_icons(EN[key]["rows"]))

    # 8. Mounts, pets and minions -------------------------------------------------
    pdf.chapter(8, C["8"], T["mounts"]["intro"], art=ART["cover-16x9"], focus_x=0.15)
    for key, title in (("mounts", SEC["mounts"].format(n=S["mounts"])), ("pets", SEC["pets"].format(n=S["pets"])),
                       ("minions", SEC["minions"])):
        block = T[key]
        pdf.section(title)
        if key != "mounts":
            pdf.para(block["intro"])
        pdf.data_table(block["headers"], block["rows"], block["col_widths"], icons=_icons(EN[key]["rows"]))

    # 9. Enemies ---------------------------------------------------------------------
    enemies = T["enemies"]
    pdf.chapter(9, C["9"], enemies["intro"], art=ART["banner-wide"], focus_x=0.97)
    for (biome, group), group_en in zip(enemies["groups"].items(), EN["enemies"]["groups"].values()):
        pdf.section(biome.replace(" / ", " and "))
        pdf.data_table(enemies["headers"], group["rows"], group["col_widths"],
                       icons=[data.npc_icon(r[0], ICON_ALIASES) for r in group_en["rows"]], aligns=["L", "R", "R", "R", "L"])
    pdf.section(SEC["objectives"].format(n=objectives))
    pdf.para(enemies["objects_intro"])
    pdf.data_table(enemies["objects_headers"], enemies["objects"], enemies["objects_col_widths"],
                   aligns=["L", "R", "L"])

    # 10. Town NPCs ----------------------------------------------------------------------
    npcs = T["town_npcs"]
    pdf.chapter(10, C["10"], npcs["intro"], art=ART["banner-wide"], focus_x=0.75)
    pdf.data_table(npcs["headers"], npcs["rows"], npcs["col_widths"],
                   icons=[data.npc_icon(r[0], ICON_ALIASES) for r in EN["town_npcs"]["rows"]])

    # 11. Systems and events --------------------------------------------------------------
    pdf.chapter(11, C["11"], L["systems_intro"].format(n=len(T["systems"])), art=ART["banner-wide"], focus_x=0.5)
    for system in T["systems"]:
        pdf.subheading(system["name"], min_space=26)
        pdf.para(system["text"])
        if system.get("canon_note"):
            pdf.note(system["canon_note"])

    # 12. Crafting materials ----------------------------------------------------------------
    mats = T["crafting_materials"]
    pdf.chapter(12, C["12"], mats["intro"], art=ART["cover-16x9"], focus_x=0.85)
    pdf.data_table(mats["headers"], mats["rows"], mats["col_widths"], icons=_icons(EN["crafting_materials"]["rows"]))

    # 13. The Deathly Hallows -----------------------------------------------------------------
    dh = T["deathly_hallows"]
    pdf.chapter(13, C["13"], dh["intro"], art=ART["poster-vertical"], focus_x=0.5)
    pdf.section(SEC["artifacts"])
    pdf.icon_row([(data.sprite(internal), label)
                  for internal, label in zip(("ElderWand", "InvisibilityCloak", "ResurrectionStone"), L["hallows"])])
    pdf.bullets(dh["artifacts"])
    pdf.section(SEC["master_of_death"])
    pdf.para(dh["master_of_death"])
    pdf.section(SEC["obtain"])
    pdf.bullets(dh["acquisition"])

    # 14. Canon notes ------------------------------------------------------------------------------
    cd = T["canon_disclosure"]
    pdf.chapter(14, C["14"], cd["intro"], art=ART["banner-wide"], focus_x=0.25)
    for cat in cd["categories"]:
        pdf.section(cat["label"])
        pdf.para(cat["description"], color=MUTED)
        pdf.bullets(cat["examples"])

    # Back cover ------------------------------------------------------------------------------------
    counts = dict(S, creatures=creatures)
    back = L["back"]
    pdf.back_cover(art=ART["banner-wide"], title=back["title"], lines=[line.format(**counts) for line in back["lines"]],
                   quote=back["quote"], credit=back["credit"], legal=back["legal"])
    return pdf


def render(output_path, **kwargs):
    """Build twice: the first pass measures the contents so page numbers and links are exact."""
    toc_pages = build_guide(**kwargs).measure_toc_pages()
    pdf = build_guide(toc_pages=toc_pages, **kwargs)
    pdf.output(output_path)
    return pdf
