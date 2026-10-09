"""Page design shared by the English and Chinese player guides.

The generators decide *what* goes in the guide; this module decides how it
looks: cover, contents, chapter openers, text, tables with item icons, boss
cards and the back cover. Built on fpdf2 (which also brings Pillow).
"""

import hashlib
import logging
import os
import sys

from fpdf import FPDF, FontFace
from fpdf.enums import TableBordersLayout, TableCellFillMode, VAlign, WrapMode, XPos, YPos
from fpdf.util import Padding
from PIL import Image, ImageDraw, ImageFilter

logging.getLogger("fontTools.subset").setLevel(logging.ERROR)  # Apple-only tables dropped when subsetting

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_DIR = os.path.join(ROOT, "tools", "fonts")
ART_DIR = os.path.join(ROOT, "release_assets")
CACHE_DIR = os.path.join(ROOT, "scripts", ".guide_cache")

PAGE_W, PAGE_H = 210, 297
MARGIN = 18
CONTENT_W = PAGE_W - 2 * MARGIN

# Colours (RGB)
INK = (33, 27, 43)
MUTED = (98, 90, 112)
FAINT = (150, 143, 160)
PURPLE = (64, 36, 102)
PURPLE_DEEP = (31, 17, 50)
NIGHT = (19, 12, 30)
GOLD = (176, 128, 40)
GOLD_BRIGHT = (226, 186, 96)
GOLD_SOFT = (249, 242, 226)
LAVENDER = (246, 243, 251)
RULE = (224, 217, 234)
WHITE = (255, 255, 255)


# ---------------------------------------------------------------------------
# Fonts
# ---------------------------------------------------------------------------

def _cjk_candidates():
    """(regular, regular_index, bold, bold_index) font files to try, best first."""
    env = os.environ.get("WW_CJK_FONT")
    if env:
        yield env, int(os.environ.get("WW_CJK_FONT_INDEX", 0)), os.environ.get("WW_CJK_FONT_BOLD", env), \
            int(os.environ.get("WW_CJK_FONT_BOLD_INDEX", os.environ.get("WW_CJK_FONT_INDEX", 0)))
    windows = [os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts"), "/mnt/c/Windows/Fonts"]
    for d in windows:
        yield os.path.join(d, "msyh.ttc"), 0, os.path.join(d, "msyhbd.ttc"), 0      # Microsoft YaHei
        yield os.path.join(d, "simhei.ttf"), 0, os.path.join(d, "simhei.ttf"), 0     # SimHei
    yield "/System/Library/Fonts/STHeiti Light.ttc", 1, "/System/Library/Fonts/STHeiti Medium.ttc", 1  # Heiti SC
    yield "/System/Library/Fonts/Hiragino Sans GB.ttc", 0, "/System/Library/Fonts/Hiragino Sans GB.ttc", 2
    noto = "/usr/share/fonts/opentype/noto"
    yield os.path.join(noto, "NotoSansCJK-Regular.ttc"), "SC", os.path.join(noto, "NotoSansCJK-Bold.ttc"), "SC"
    yield "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc", 0, "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc", 0


def _collection_index(path, wanted):
    """Index of the Simplified Chinese face inside a Noto CJK collection."""
    if isinstance(wanted, int):
        return wanted
    from fontTools.ttLib import TTCollection
    for i, font in enumerate(TTCollection(path).fonts):
        if wanted in (font["name"].getDebugName(1) or ""):
            return i
    return 0


def find_cjk_font():
    for regular, ri, bold, bi in _cjk_candidates():
        if os.path.exists(regular):
            if not os.path.exists(bold):
                bold, bi = regular, ri
            return regular, _collection_index(regular, ri), bold, _collection_index(bold, bi)
    sys.exit("ERROR: no Chinese font found. Set WW_CJK_FONT to a .ttf/.ttc/.otf file "
             "(on Ubuntu: sudo apt-get install fonts-noto-cjk).")


# ---------------------------------------------------------------------------
# Chinese line breaking
# ---------------------------------------------------------------------------

_NO_LINE_START = set("、，。．・：；！？）」』】〕〉》”’…—～%％,.:;!?)]}")
_NO_LINE_END = set("（「『【〔〈《“‘([{")


def _is_cjk(ch):
    o = ord(ch)
    return 0x2E80 <= o <= 0x9FFF or 0xF900 <= o <= 0xFAFF or 0xFF00 <= o <= 0xFFEF or 0x3000 <= o <= 0x303F


def cjk_tokens(text):
    """Pieces that may not be split: one Chinese character (with any closing punctuation after it
    and opening punctuation before it) or one Latin word with its trailing space."""
    tokens, cur = [], ""
    for ch in text:
        if ch.isspace():
            cur += ch
            tokens.append(cur)
            cur = ""
        elif ch in _NO_LINE_START:
            if cur:
                cur += ch
            elif tokens:
                tokens[-1] += ch
            else:
                cur = ch
        elif _is_cjk(ch):
            if cur and cur[-1] not in _NO_LINE_END:
                tokens.append(cur)
                cur = ""
            cur += ch
        else:
            if cur and _is_cjk(cur[-1]) and cur[-1] not in _NO_LINE_END:
                tokens.append(cur)
                cur = ""
            cur += ch
    if cur:
        tokens.append(cur)
    return tokens


# ---------------------------------------------------------------------------
# Images (processed once, cached under scripts/.guide_cache)
# ---------------------------------------------------------------------------

def _cached(name, src_paths, params, build):
    os.makedirs(CACHE_DIR, exist_ok=True)
    h = hashlib.sha1(repr(params).encode())
    for p in src_paths:
        h.update(p.encode())
        h.update(str(os.path.getmtime(p)).encode())
    path = os.path.join(CACHE_DIR, f"{name}-{h.hexdigest()[:12]}{os.path.splitext(name)[1] or '.png'}")
    if not os.path.exists(path):
        build(path)
    return path


def _cover_crop(img, w, h, focus_x=0.5, focus_y=0.5):
    """Scale and crop img to exactly w x h, keeping the focus point in view."""
    scale = max(w / img.width, h / img.height)
    img = img.resize((round(img.width * scale), round(img.height * scale)), Image.LANCZOS)
    left = min(max(0, round(img.width * focus_x - w / 2)), img.width - w)
    top = min(max(0, round(img.height * focus_y - h / 2)), img.height - h)
    return img.crop((left, top, left + w, top + h))


def _shade(img, stops):
    """Darken img with vertical alpha stops [(y_fraction, alpha 0-255), ...] of NIGHT."""
    w, h = img.size
    mask = Image.new("L", (1, h))
    for y in range(h):
        t = y / max(1, h - 1)
        for (t0, a0), (t1, a1) in zip(stops, stops[1:]):
            if t0 <= t <= t1:
                a = a0 + (a1 - a0) * ((t - t0) / (t1 - t0) if t1 > t0 else 0)
                mask.putpixel((0, y), int(a))
                break
    overlay = Image.new("RGB", (w, h), NIGHT)
    return Image.composite(overlay, img, mask.resize((w, h)))


def art_page(src, stops, focus=(0.5, 0.5), px=(1240, 1754)):
    """Full-page artwork (A4 at 150 dpi) with gradient shading baked in."""
    def build(path):
        img = _cover_crop(Image.open(src).convert("RGB"), *px, *focus)
        _shade(img, stops).save(path, quality=86, optimize=True)
    return _cached("page.jpg", [src], (stops, focus, px), build)


def art_strip(src, focus_x, height_mm=64, stops=((0, 40), (0.45, 70), (1, 235))):
    """Full-width banner for a chapter opener."""
    px = (1240, round(1240 * height_mm / PAGE_W))

    def build(path):
        img = _cover_crop(Image.open(src).convert("RGB"), *px, focus_x, 0.45)
        _shade(img, stops).save(path, quality=84, optimize=True)
    return _cached("strip.jpg", [src], (focus_x, height_mm, stops), build)


def pixel_icon(src, box=64, frames=1):
    """Item sprite scaled up with hard pixel edges, padded to a square.

    For NPC sheets (frames stacked vertically) only the first frame is used.
    """
    def build(path):
        img = Image.open(src).convert("RGBA")
        if frames > 1:
            img = img.crop((0, 0, img.width, img.height // frames))
        bbox = img.getbbox()
        if bbox:
            img = img.crop(bbox)
        k = max(1, min(box // max(img.width, 1), box // max(img.height, 1)))
        if k == 0 or img.width * k > box or img.height * k > box:
            img.thumbnail((box, box), Image.NEAREST)
        else:
            img = img.resize((img.width * k, img.height * k), Image.NEAREST)
        canvas = Image.new("RGBA", (box, box), (0, 0, 0, 0))
        canvas.paste(img, ((box - img.width) // 2, (box - img.height) // 2), img)
        canvas.save(path, optimize=True)
    return _cached("icon.png", [src], (box, frames), build)


def boss_portrait(sheet, columns, frames, px=(560, 640)):
    """First animation frame of a boss sheet on a night-sky card."""
    def build(path):
        img = Image.open(sheet).convert("RGBA")
        rows = (frames + columns - 1) // columns
        fw, fh = img.width // columns, img.height // rows
        frame = img.crop((0, 0, fw, fh))
        bbox = frame.getbbox()
        if bbox:
            frame = frame.crop(bbox)
        w, h = px
        bg = Image.new("RGB", px, NIGHT)
        glow = Image.new("L", px, 0)
        ImageDraw.Draw(glow).ellipse((w * 0.08, h * 0.12, w * 0.92, h * 0.96), fill=120)
        glow = glow.filter(ImageFilter.GaussianBlur(w // 7))
        bg = Image.composite(Image.new("RGB", px, (70, 44, 104)), bg, glow)
        frame.thumbnail((int(w * 0.86), int(h * 0.84)), Image.LANCZOS)
        bg.paste(frame, ((w - frame.width) // 2, h - frame.height - int(h * 0.06)), frame)
        bg.save(path, quality=88, optimize=True)
    return _cached("boss.jpg", [sheet], (columns, frames, px), build)


# ---------------------------------------------------------------------------
# The document
# ---------------------------------------------------------------------------

class GuidePDF(FPDF):
    """A4 guide with a running header, page numbers, outline and themed blocks."""

    def __init__(self, *, running_title, cjk=False, labels=None):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.cjk = cjk
        self.labels = {"contents": "Contents", "chapter": "Chapter", "page": "Page"}
        self.labels.update(labels or {})
        self.running_title = running_title
        self.chapter_name = ""
        self.plain_page = True   # no header/footer (covers, chapter art)
        self._reuse_page = False  # the ToC placeholder leaves an empty page behind
        self.set_margins(MARGIN, 24, MARGIN)
        self.set_auto_page_break(True, margin=20)
        self.set_creator("Wizarding World guide generator (fpdf2)")
        self._register_fonts()

    def multi_cell(self, w, h=None, text="", *args, **kwargs):
        # Chinese has no spaces to wrap at, so break the lines here (following the usual rules for
        # punctuation) and hand fpdf2 finished lines; the PDF keeps clean, searchable text.
        if self.cjk and text:
            pad = Padding.new(kwargs.get("padding", 0))
            avail = (w or self.w - self.r_margin - self.x) - pad.left - pad.right
            avail -= (0 if pad.left else self.c_margin) + (0 if pad.right else self.c_margin)
            text = self._cjk_lines(str(text), avail - 0.4)
        return super().multi_cell(w, h, text, *args, **kwargs)

    def _cjk_lines(self, text, width):
        lines = []
        for paragraph in text.split("\n"):
            line = ""
            for tok in cjk_tokens(paragraph):
                if not line or self.get_string_width((line + tok).rstrip()) <= width:
                    line += tok
                else:
                    lines.append(line.rstrip())
                    line = tok.lstrip()
            lines.append(line.rstrip())
        return "\n".join(lines)

    # -- fonts ---------------------------------------------------------------
    def _register_fonts(self):
        f = lambda name: os.path.join(FONT_DIR, name)
        self.add_font("Display", "", f("PlayfairDisplay-SemiBold.ttf"))
        self.add_font("Display", "B", f("PlayfairDisplay-Bold.ttf"))
        self.add_font("Display", "I", f("PlayfairDisplay-MediumItalic.ttf"))
        if self.cjk:
            regular, ri, bold, bi = find_cjk_font()
            self.cjk_font_file = regular
            self.add_font("Body", "", regular, collection_font_number=ri)
            self.add_font("Body", "B", bold, collection_font_number=bi)
            self.add_font("Body", "I", regular, collection_font_number=ri)
            self.heading_family = "Body"
        else:
            self.add_font("Body", "", f("IBMPlexSans-Regular.ttf"))
            self.add_font("Body", "B", f("IBMPlexSans-SemiBold.ttf"))
            self.add_font("Body", "I", f("IBMPlexSans-Italic.ttf"))
            self.heading_family = "Display"

    def body(self, size=9.6, style=""):
        self.set_font("Body", style, size)

    def heading_font(self, size, style="B"):
        self.set_font(self.heading_family, style if self.heading_family == "Display" or style == "B" else "B", size)

    # -- page furniture ------------------------------------------------------
    def header(self):
        if self.plain_page:
            return
        self.set_y(11)
        self.set_text_color(*GOLD)
        self.body(6.8, "B")
        self.set_char_spacing(0 if self.cjk else 1.1)
        self.cell(CONTENT_W / 2, 4, self.running_title if self.cjk else self.running_title.upper())
        self.set_char_spacing(0)
        self.set_text_color(*FAINT)
        self.body(7.2)
        self.cell(CONTENT_W / 2, 4, self.chapter_name, align="R")
        self.set_draw_color(*RULE)
        self.set_line_width(0.25)
        self.line(MARGIN, 16.5, PAGE_W - MARGIN, 16.5)
        self.set_y(24)

    def footer(self):
        if self.plain_page:
            return
        self.set_y(-13)
        self.body(7.6)
        self.set_text_color(*FAINT)
        self.cell(0, 5, str(self.page_no()), align="C")

    def new_page(self, plain=False):
        self.plain_page = plain
        if self._reuse_page:
            self._reuse_page = False
            self.set_y(self.t_margin)
            return
        self.add_page()

    def space_left(self):
        return self.page_break_trigger - self.get_y()

    def keep(self, mm):
        """Start a new page unless at least `mm` of vertical space remains."""
        if self.space_left() < mm:
            self.new_page()

    # -- cover & back cover --------------------------------------------------
    def cover(self, *, art, title, subtitle, kicker, facts, footnote):
        self.new_page(plain=True)
        self.set_auto_page_break(False)
        self.image(art_page(art, ((0, 235), (0.30, 120), (0.52, 10), (0.70, 60), (1, 245)), focus=(0.5, 0.5)),
                   0, 0, PAGE_W, PAGE_H)
        self.set_text_color(*GOLD_BRIGHT)
        self.set_xy(0, 26)
        self.body(9, "B")
        self.set_char_spacing(0 if self.cjk else 3)
        self.cell(PAGE_W, 6, kicker, align="C")
        self.set_char_spacing(0)
        self.set_xy(0, 36)
        self.set_font("Display", "B", 46)
        self.cell(PAGE_W, 20, title, align="C")
        self.set_xy(0, 58)
        self.set_text_color(240, 234, 248)
        if self.cjk:
            self.body(15)
        else:
            self.set_font("Display", "I", 17)
        self.cell(PAGE_W, 9, subtitle, align="C")
        # facts row near the bottom
        self.set_draw_color(*GOLD_BRIGHT)
        self.set_line_width(0.35)
        self.line(PAGE_W / 2 - 30, 238, PAGE_W / 2 + 30, 238)
        cols = len(facts)
        cell_w = 150 / cols
        x0 = (PAGE_W - 150) / 2
        for i, (value, label) in enumerate(facts):
            self.set_xy(x0 + i * cell_w, 244)
            self.set_text_color(*WHITE)
            self.set_font("Display", "B", 19)
            self.cell(cell_w, 9, str(value), align="C")
            self.set_xy(x0 + i * cell_w, 253.5)
            self.set_text_color(214, 204, 230)
            self.body(6.8, "B")
            self.set_char_spacing(0 if self.cjk else 0.8)
            self.cell(cell_w, 4, label if self.cjk else label.upper(), align="C")
            self.set_char_spacing(0)
        self.set_xy(0, 276)
        self.set_text_color(186, 176, 204)
        self.body(7.6)
        self.cell(PAGE_W, 4, footnote, align="C")
        self.set_auto_page_break(True, margin=20)

    def back_cover(self, *, art, title, lines, quote, credit, legal):
        self.new_page(plain=True)
        self.set_auto_page_break(False)
        self.image(art_page(art, ((0, 90), (0.38, 150), (0.55, 238), (1, 250)), focus=(0.5, 0.35)), 0, 0, PAGE_W, PAGE_H)
        y = 176
        self.set_xy(0, y)
        self.set_text_color(*GOLD_BRIGHT)
        self.set_font("Display", "B", 28)
        self.cell(PAGE_W, 12, title, align="C")
        y += 16
        self.set_text_color(226, 218, 238)
        for line in lines:
            self.set_xy(0, y)
            self.body(9.4)
            self.cell(PAGE_W, 5, line, align="C")
            y += 6
        if quote:
            self.set_xy(0, y + 8)
            self.set_text_color(196, 186, 214)
            if self.cjk:
                self.body(10)
            else:
                self.set_font("Display", "I", 12)
            self.cell(PAGE_W, 6, quote, align="C")
        self.set_xy(30, 252)
        self.set_text_color(214, 204, 230)
        self.body(8.4, "B")
        self.multi_cell(PAGE_W - 60, 4.6, credit, align="C")
        self.set_xy(30, self.get_y() + 2)
        self.set_text_color(160, 150, 180)
        self.body(6.9)
        self.multi_cell(PAGE_W - 60, 3.6, legal, align="C")
        self.set_auto_page_break(True, margin=20)

    # -- contents --------------------------------------------------------------
    def contents_page(self, intro=None, pages=None):
        """Contents with page numbers. pages=None measures (the ToC may grow); pass the
        measured count on a second build so page numbers and links stay exact."""
        self.new_page()
        self.chapter_name = self.labels["contents"]
        self.set_text_color(*PURPLE_DEEP)
        self.heading_font(26)
        self.cell(0, 14, self.labels["contents"], new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        if intro:
            self.set_text_color(*MUTED)
            self.body(9.6)
            self.multi_cell(0, 5, intro, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(4)
        self.insert_toc_placeholder(self._render_toc, pages=pages or 1, allow_extra_pages=pages is None)
        self._reuse_page = True

    def measure_toc_pages(self):
        """Render a measuring build and report how many pages its contents needed."""
        before = len(self.pages)
        self.output()
        return 1 + len(self.pages) - before

    def _render_toc(self, pdf, outline):
        for entry in outline:
            if entry.level > 1:
                continue
            link = pdf.add_link(page=entry.page_number)
            if entry.level == 0:
                pdf.ln(2.2)
                pdf.set_text_color(*PURPLE_DEEP)
                pdf.heading_font(12.5, "B")
                h = 7.2
            else:
                pdf.set_text_color(*MUTED)
                pdf.body(8.8)
                h = 5
            name = entry.name
            indent = 0 if entry.level == 0 else 8
            num = str(entry.page_number)
            pdf.set_x(MARGIN + indent)
            name_w = pdf.get_string_width(name)
            num_w = pdf.get_string_width(num)
            pdf.cell(name_w + 1, h, name, link=link)
            # dotted leader
            x1, x2 = pdf.get_x() + 1.5, PAGE_W - MARGIN - num_w - 2
            if x2 > x1:
                pdf.set_draw_color(*RULE)
                pdf.set_line_width(0.3)
                pdf.set_dash_pattern(dash=0.3, gap=1.2)
                pdf.line(x1, pdf.get_y() + h * 0.72, x2, pdf.get_y() + h * 0.72)
                pdf.set_dash_pattern()
            pdf.set_x(PAGE_W - MARGIN - num_w - 1)
            pdf.cell(num_w + 1, h, num, align="R", link=link, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # -- chapters & headings ---------------------------------------------------
    def chapter(self, number, title, intro=None, *, art=None, focus_x=0.5):
        """Chapter opener: banner art with the title over it, then an intro line."""
        self.new_page(plain=True)
        self.chapter_name = title
        strip_h = 64
        self.image(art_strip(art or os.path.join(ART_DIR, "wizardingworld-banner-wide.png"), focus_x, strip_h),
                   0, 0, PAGE_W, strip_h)
        self.start_section(title, level=0)
        self.set_xy(MARGIN, strip_h - 26)
        self.set_text_color(*GOLD_BRIGHT)
        self.body(8, "B")
        self.set_char_spacing(0 if self.cjk else 2.2)
        label = f"{self.labels['chapter']} {number}" if not self.cjk else self.labels["chapter"].format(number)
        self.cell(0, 5, label if self.cjk else label.upper(), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_char_spacing(0)
        self.set_text_color(*WHITE)
        self.heading_font(27)
        self.cell(0, 13, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_y(strip_h + 9)
        if intro:
            self.set_text_color(*MUTED)
            if self.cjk:
                self.body(10.6)
            else:
                self.set_font("Display", "I", 12.2)
            self.multi_cell(0, 6.2 if not self.cjk else 6.4, intro, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.ln(3)
        # later pages of this chapter get the running header
        self.plain_page = False

    def section(self, title, *, min_space=34):
        self.keep(min_space)
        if self.get_y() > 30:
            self.ln(3.5)
        self.start_section(title, level=1)
        self.set_fill_color(*GOLD)
        self.rect(MARGIN, self.get_y() + 1.6, 1.2, 6.2, style="F")
        self.set_x(MARGIN + 4)
        self.set_text_color(*PURPLE_DEEP)
        self.heading_font(15 if not self.cjk else 13.5)
        self.cell(0, 9, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1.2)

    def subheading(self, title, *, min_space=22):
        self.keep(min_space)
        self.ln(1.5)
        self.set_text_color(*PURPLE)
        self.body(10.4, "B")
        self.cell(0, 6, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(0.6)

    # -- text ------------------------------------------------------------------
    def para(self, text, *, size=9.6, color=INK, gap=2.2, align="J"):
        self.set_text_color(*color)
        self.body(size)
        self.multi_cell(0, size * 0.53 if not self.cjk else size * 0.6, text, align=align if not self.cjk else "L",
                        new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(gap)

    def note(self, text):
        self.para(text, size=8.4, color=MUTED, gap=2)

    def bullets(self, items, *, size=9.4, numbered=False, gap=1.0):
        line_h = size * 0.53 if not self.cjk else size * 0.6
        for i, item in enumerate(items, 1):
            self.keep(line_h * 2)
            y = self.get_y()
            self.set_text_color(*GOLD)
            self.body(size, "B")
            marker = f"{i}." if numbered else "\u2022"
            self.set_xy(MARGIN + 1, y)
            self.cell(6, line_h, marker)
            self.set_text_color(*INK)
            self.body(size)
            self.set_xy(MARGIN + 7, y)
            self.multi_cell(CONTENT_W - 7, line_h, item, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.ln(gap)
        self.ln(1.2)

    def callout(self, title, text, *, tone="gold"):
        fill, bar = (GOLD_SOFT, GOLD) if tone == "gold" else (LAVENDER, PURPLE)
        size = 9.0
        line_h = size * 0.53 if not self.cjk else size * 0.6
        self.body(size)
        inner_w = CONTENT_W - 12
        text_h = self.multi_cell(inner_w, line_h, text, dry_run=True, output="HEIGHT")
        h = text_h + (7.5 if title else 0) + 7
        self.keep(h + 4)
        x, y = MARGIN, self.get_y() + 1
        self.set_fill_color(*fill)
        self.rect(x, y, CONTENT_W, h, style="F", round_corners=True, corner_radius=2)
        self.set_fill_color(*bar)
        self.rect(x, y, 1.4, h, style="F")
        self.set_xy(x + 7, y + 3.5)
        if title:
            self.set_text_color(*PURPLE_DEEP)
            self.body(9.6, "B")
            self.cell(inner_w, 5.5, title, new_x=XPos.LEFT, new_y=YPos.NEXT)
            self.ln(1.5)
            self.set_x(x + 7)
        self.set_text_color(*INK)
        self.body(size)
        self.multi_cell(inner_w, line_h, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_y(y + h + 4)

    def icon_row(self, items, *, size=16):
        """A centred row of large item sprites with captions. items = [(sprite, caption), ...]."""
        gap = 22
        total = len(items) * size + (len(items) - 1) * gap
        self.keep(size + 14)
        x = (PAGE_W - total) / 2
        y = self.get_y() + 2
        for src, caption in items:
            if src:
                self.image(pixel_icon(src, box=96), x, y, size, size)
            self.set_xy(x - gap / 2, y + size + 1.5)
            self.set_text_color(*PURPLE_DEEP)
            self.body(8, "B")
            self.cell(size + gap, 4.5, caption, align="C")
            x += size + gap
        self.set_y(y + size + 9)

    def stat_grid(self, facts, *, cols=4):
        """Tiles of big numbers with small labels."""
        rows = (len(facts) + cols - 1) // cols
        gap = 3
        w = (CONTENT_W - gap * (cols - 1)) / cols
        h = 19
        self.keep(rows * (h + gap) + 2)
        y0 = self.get_y() + 1
        for i, (value, label) in enumerate(facts):
            r, c = divmod(i, cols)
            x, y = MARGIN + c * (w + gap), y0 + r * (h + gap)
            self.set_fill_color(*LAVENDER)
            self.rect(x, y, w, h, style="F", round_corners=True, corner_radius=2)
            self.set_xy(x, y + 2.5)
            self.set_text_color(*PURPLE)
            self.set_font("Display", "B", 19)
            self.cell(w, 9, str(value), align="C")
            self.set_xy(x, y + 12)
            self.set_text_color(*MUTED)
            self.body(6.8, "B")
            self.set_char_spacing(0 if self.cjk else 0.7)
            self.cell(w, 4, label if self.cjk else label.upper(), align="C")
            self.set_char_spacing(0)
        self.set_y(y0 + rows * (h + gap) + 2)

    # -- tables ----------------------------------------------------------------
    def data_table(self, headers, rows, widths, *, icons=None, aligns=None, size=8.0, bold_first=True):
        """Zebra table with a dark header row; optional sprite icon before each row."""
        if icons is not None:
            headers = [""] + list(headers)
            widths = [8.5] + list(widths)
            aligns = ["C"] + list(aligns or ["L"] * (len(headers) - 1))
        aligns = aligns or ["L"] * len(headers)
        widths = self._fit_columns(headers, rows, widths, size, icon_col=icons is not None)
        self.keep(22)
        self.body(size)
        line_h = size * 0.5 if not self.cjk else size * 0.56
        head = FontFace(family="Body", emphasis="BOLD", size_pt=size - 0.6, color=WHITE, fill_color=PURPLE_DEEP)
        first = FontFace(family="Body", emphasis="BOLD", size_pt=size, color=PURPLE_DEEP)
        self.set_draw_color(*RULE)
        self.set_line_width(0.2)
        self.set_text_color(*INK)
        self.set_fill_color(*WHITE)   # odd rows inherit the current fill colour
        with self.table(col_widths=widths, width=CONTENT_W, align="L", line_height=line_h,
                        headings_style=head, borders_layout=TableBordersLayout.HORIZONTAL_LINES,
                        cell_fill_color=LAVENDER, cell_fill_mode=TableCellFillMode.EVEN_ROWS,
                        padding=(1.5, 1.6, 1.5, 1.6), v_align=VAlign.M, text_align=aligns,
                        wrapmode=WrapMode.WORD, repeat_headings=1) as table:
            hr = table.row()
            for h in headers:
                hr.cell(h)
            for i, row in enumerate(rows):
                r = table.row()
                if icons is not None:
                    icon = icons[i]
                    if icon:
                        src, frames = icon if isinstance(icon, tuple) else (icon, 1)
                        r.cell(img=pixel_icon(src, frames=frames), img_fill_width=True)
                    else:
                        r.cell("")
                for j, value in enumerate(row):
                    if j == 0 and bold_first:
                        r.cell(str(value), style=first)
                    else:
                        r.cell(str(value))
        self.ln(3.5)

    def _fit_columns(self, headers, rows, weights, size, icon_col=False):
        """Column widths (mm) summing to CONTENT_W, never narrower than the longest word."""
        pad = 4.2  # cell padding (3.2) + the line-breaking margin used for Chinese
        mins = []
        for j, h in enumerate(headers):
            if icon_col and j == 0:
                mins.append(weights[0])
                continue
            self.body(size - 0.6, "B")
            longest = max((self.get_string_width(w) for w in str(h).split()), default=0)
            for r in rows:
                value = str(r[j - 1 if icon_col else j])
                self.body(size, "B" if (j == (1 if icon_col else 0)) else "")
                words = list(value) if self.cjk and not value.isascii() else value.split()
                longest = max([longest] + [self.get_string_width(w) for w in words])
            mins.append(longest + pad)
        total_w = sum(weights)
        target = [w * CONTENT_W / total_w for w in weights]
        if sum(mins) >= CONTENT_W:
            return [max(t, m) * CONTENT_W / sum(max(t, m) for t, m in zip(target, mins)) for t, m in zip(target, mins)]
        # grow the columns that are below their minimum, take the space from the others pro rata
        widths = [max(t, m) for t, m in zip(target, mins)]
        excess = sum(widths) - CONTENT_W
        while excess > 0.01:
            slack = [w - m for w, m in zip(widths, mins)]
            room = sum(s for s in slack if s > 0)
            if room <= 0:
                break
            widths = [w - excess * (s / room) if s > 0 else w for w, s in zip(widths, slack)]
            excess = sum(widths) - CONTENT_W
        return widths

    # -- boss card -------------------------------------------------------------
    def boss_card(self, *, number, name, portrait, stats, requirement, summon, blocks, bookmark=None):
        """Portrait on the left, stats and text on the right. blocks = [(label, text), ...]."""
        port_w, port_h = 50, 57
        text_x = MARGIN + port_w + 7
        text_w = CONTENT_W - port_w - 7
        size = 8.8
        line_h = size * 0.52 if not self.cjk else size * 0.6
        # measure
        self.body(size)
        body_h = 0
        for label, text in blocks:
            body_h += 5 + self.multi_cell(text_w, line_h, text, dry_run=True, output="HEIGHT") + 2.2
        req_h = self.multi_cell(text_w, line_h, requirement, dry_run=True, output="HEIGHT") if requirement else 0
        sum_h = self.multi_cell(text_w, line_h, summon, dry_run=True, output="HEIGHT") if summon else 0
        head_h = 9 + 9.5 + (req_h + 2 if requirement else 0) + (sum_h + 2 if summon else 0)
        card_h = max(port_h, head_h + body_h) + 2
        self.keep(card_h + 6)
        if bookmark:
            self.start_section(bookmark, level=1)
        y = self.get_y() + 1
        # portrait
        self.image(portrait, MARGIN, y, port_w, port_h)
        self.set_xy(MARGIN, y + 2)
        self.set_text_color(*GOLD_BRIGHT)
        self.set_font("Display", "B", 13)
        self.cell(10, 6, f"{number:02d}", align="C")
        # name
        self.set_xy(text_x, y)
        self.set_text_color(*PURPLE_DEEP)
        self.heading_font(16)
        self.cell(text_w, 9, name, new_x=XPos.LEFT, new_y=YPos.NEXT)
        # stat chips
        cx = text_x
        cy = self.get_y() + 0.5
        for label, value in stats:
            self.body(6.6, "B")
            lw = self.get_string_width(label if self.cjk else label.upper())
            self.body(8.6, "B")
            vw = self.get_string_width(value)
            chip_w = lw + vw + 7
            self.set_fill_color(*LAVENDER)
            self.rect(cx, cy, chip_w, 6.6, style="F", round_corners=True, corner_radius=1.6)
            self.set_xy(cx + 2.2, cy + 0.9)
            self.set_text_color(*MUTED)
            self.body(6.6, "B")
            self.cell(lw + 1.2, 4.8, label if self.cjk else label.upper())
            self.set_text_color(*PURPLE_DEEP)
            self.body(8.6, "B")
            self.cell(vw + 1, 4.8, value)
            cx += chip_w + 2.2
        self.set_xy(text_x, cy + 9.5)
        for text, color in ((requirement, GOLD), (summon, MUTED)):
            if text:
                self.set_x(text_x)
                self.set_text_color(*color)
                self.body(size, "B" if color == GOLD else "")
                self.multi_cell(text_w, line_h, text, new_x=XPos.LEFT, new_y=YPos.NEXT)
                self.ln(2)
        for label, text in blocks:
            self.set_x(text_x)
            self.set_text_color(*PURPLE)
            self.body(7, "B")
            self.set_char_spacing(0 if self.cjk else 0.8)
            self.cell(text_w, 5, label if self.cjk else label.upper(), new_x=XPos.LEFT, new_y=YPos.NEXT)
            self.set_char_spacing(0)
            self.set_x(text_x)
            self.set_text_color(*INK)
            self.body(size)
            self.multi_cell(text_w, line_h, text, new_x=XPos.LEFT, new_y=YPos.NEXT)
            self.ln(2.2)
        end = max(self.get_y(), y + port_h)
        self.set_draw_color(*RULE)
        self.set_line_width(0.25)
        self.line(MARGIN, end + 3, PAGE_W - MARGIN, end + 3)
        self.set_y(end + 7)
