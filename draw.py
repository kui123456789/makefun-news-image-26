"""Draw the front page for news-image-20261126.

Builds a 1024x1024 newspaper-style front page with PIL shapes only:
a masthead, a date line, six story panels in a 2x3 grid, each with a
small drawn pictorial illustration, a headline and a short summary,
plus a footnote naming the reporting window. No external assets.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (248, 244, 233)
INK = (26, 26, 26)
NAVY = (22, 35, 63)
GOLD = (217, 164, 65)
RED = (166, 28, 28)
PANEL_BG = (255, 253, 246)
PANEL_EDGE = (201, 194, 174)
GREY = (90, 86, 76)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_OBLIQUE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf"

_ALT_SERIF_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
_ALT_SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
_ALT_SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
_ALT_SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def _font(path, alt, size):
    for p in (path, alt):
        try:
            return ImageFont.truetype(p, size)
        except (OSError, IOError):
            continue
    return ImageFont.load_default(size=size)


def serif_bold(size):
    return _font(SERIF_BOLD, _ALT_SERIF_BOLD, size)


def serif(size):
    return _font(SERIF, _ALT_SERIF, size)


def sans_bold(size):
    return _font(SANS_BOLD, _ALT_SANS_BOLD, size)


def sans(size):
    return _font(SANS, _ALT_SANS, size)


def sans_oblique(size):
    return _font(SANS_OBLIQUE, _ALT_SANS, size)


def wrap_text(draw, text, font, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for word in words[1:]:
            trial = cur + " " + word
            if draw.textlength(trial, font=font) <= max_width:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def draw_lines(draw, lines, font, x, y, fill, line_h, max_lines=None):
    if max_lines is not None:
        lines = lines[:max_lines]
    for i, line in enumerate(lines):
        draw.text((x, y + i * line_h), line, font=font, fill=fill)
    return y + len(lines) * line_h


# ---------------------------------------------------------------- stories

STORIES = [
    {
        "kicker": "MIDDLE EAST",
        "headline": "Tankers ablaze in the Strait of Hormuz",
        "summary": "Two oil tankers hit naval mines and caught fire in the strait, Iran's Guard said.",
        "source": "Source: Just Security, 25 Nov",
        "art": "tanker",
    },
    {
        "kicker": "MIDDLE EAST",
        "headline": "Houthis strike Saudi Arabia's biggest refinery",
        "summary": "Yemen's Houthis said they struck Saudi Arabia's Ras Tanura oil refinery; fires reported.",
        "source": "Source: Just Security, 25 Nov",
        "art": "refinery",
    },
    {
        "kicker": "SPACE",
        "headline": "First Pakistani astronaut reaches Tiangong",
        "summary": "Shenzhou-24 docked with Tiangong, carrying Pakistan's first astronaut to orbit.",
        "source": "Source: Xinhua, 25 Nov",
        "art": "rocket",
    },
    {
        "kicker": "PACIFIC",
        "headline": "Australia and Solomons sign security pact",
        "summary": "Canberra and Honiara signed a treaty barring foreign military bases in the Solomons.",
        "source": "Source: Just Security, 25 Nov",
        "art": "treaty",
    },
    {
        "kicker": "EGYPT",
        "headline": "Cairo tanker fire kills at least 31",
        "summary": "A fuel tanker overturned on Cairo's Ring Road; the fire killed at least 31 people.",
        "source": "Source: Associated Press, 25 Nov",
        "art": "fire",
    },
    {
        "kicker": "COLOMBIA",
        "headline": "All hostages freed in Cartagena siege",
        "summary": "Troops stormed a Cartagena supermarket and freed all hostages after a day-long siege.",
        "source": "Source: Associated Press, 25 Nov",
        "art": "rescue",
    },
]

# ---------------------------------------------------------------- art


def _flame(d, cx, base, w, h, colors=((255, 140, 0), (255, 69, 0), (255, 215, 0))):
    """A simple three-layer flame centred at cx, sitting on base."""
    for i, col in enumerate(colors):
        f = 1.0 - i * 0.28
        fw, fh = w * f, h * f
        d.polygon(
            [
                (cx - fw / 2, base),
                (cx - fw * 0.32, base - fh * 0.55),
                (cx, base - fh),
                (cx + fw * 0.30, base - fh * 0.5),
                (cx + fw / 2, base),
            ],
            fill=col,
        )


def _sea_sky(d, x, y, s):
    d.rectangle([x, y, x + s, y + s * 0.45], fill=(188, 214, 232))
    d.rectangle([x, y + s * 0.45, x + s, y + s], fill=(31, 78, 121))
    for wx in range(0, s, 26):
        d.arc([x + wx, y + s * 0.52, x + wx + 24, y + s * 0.66], 0, 180,
              fill=(120, 170, 205), width=2)
        d.arc([x + wx + 8, y + s * 0.72, x + wx + 32, y + s * 0.86], 0, 180,
              fill=(120, 170, 205), width=2)


def _art_tanker(d, x, y, s):
    _sea_sky(d, x, y, s)
    # tanker hull and deck
    d.rectangle([x + 14, y + 78, x + 132, y + 100], fill=(40, 40, 48))
    d.rectangle([x + 14, y + 70, x + 132, y + 80], fill=(178, 34, 34))
    d.rectangle([x + 96, y + 52, x + 112, y + 70], fill=(220, 220, 220))
    d.rectangle([x + 98, y + 44, x + 110, y + 52], fill=(40, 40, 48))
    # cargo hatches
    for hx in (26, 52, 78):
        d.rectangle([x + hx, y + 62, x + hx + 18, y + 70], fill=(120, 120, 128))
    # fire on the deck
    _flame(d, x + 52, y + 64, 34, 44)
    # naval mine in the water
    mx, my = x + 112, y + 122
    d.ellipse([mx - 11, my - 11, mx + 11, my + 11], fill=(20, 20, 20))
    for ang in range(0, 360, 45):
        import math
        dx = math.cos(math.radians(ang)) * 15
        dy = math.sin(math.radians(ang)) * 15
        d.line([mx + dx * 0.7, my + dy * 0.7, mx + dx, my + dy],
               fill=(20, 20, 20), width=3)
    d.ellipse([mx - 4, my - 4, mx + 4, my + 4], fill=(90, 90, 90))


def _art_refinery(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(232, 176, 106))
    d.ellipse([x + 96, y + 8, x + 138, y + 50], fill=(255, 214, 130))
    # distillation towers
    d.rectangle([x + 18, y + 52, x + 42, y + 132], fill=(90, 90, 96))
    d.rectangle([x + 50, y + 70, x + 74, y + 132], fill=(70, 70, 78))
    d.rectangle([x + 84, y + 44, x + 104, y + 132], fill=(110, 110, 116))
    for tx in (18, 50, 84):
        d.rectangle([x + tx - 3, y + 40, x + tx + 27, y + 46], fill=(60, 60, 66))
    # horizontal pipes
    d.rectangle([x + 10, y + 112, x + 138, y + 120], fill=(60, 60, 66))
    d.rectangle([x + 10, y + 132, x + 138, y + 148], fill=(58, 52, 46))
    # flare flame and smoke
    _flame(d, x + 94, y + 46, 30, 40)
    d.ellipse([x + 116, y + 18, x + 136, y + 38], fill=(120, 120, 120))
    d.ellipse([x + 126, y + 6, x + 144, y + 24], fill=(140, 140, 140))


def _art_rocket(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(16, 24, 48))
    # stars
    for sx, sy, r in ((12, 14, 2), (34, 30, 1), (120, 12, 2), (132, 44, 1),
                      (20, 100, 1), (128, 96, 2), (60, 8, 1), (100, 118, 1)):
        d.ellipse([x + sx - r, y + sy - r, x + sx + r, y + sy + r],
                  fill=(255, 255, 255))
    # earth arc at the bottom, kept inside the illustration box
    d.ellipse([x + 4, y + 118, x + 144, y + 148], fill=(46, 110, 180))
    d.ellipse([x + 4, y + 118, x + 144, y + 148], outline=(140, 200, 240), width=2)
    d.ellipse([x + 30, y + 128, x + 66, y + 142], fill=(70, 150, 90))
    # rocket body
    cx = x + 74
    d.polygon([(cx, y + 14), (cx - 14, y + 48), (cx + 14, y + 48)],
              fill=(178, 34, 34))
    d.rectangle([cx - 14, y + 48, cx + 14, y + 96], fill=(240, 240, 235))
    d.rectangle([cx - 14, y + 62, cx + 14, y + 70], fill=(178, 34, 34))
    d.polygon([(cx - 14, y + 96), (cx - 26, y + 112), (cx - 14, y + 104)],
              fill=(178, 34, 34))
    d.polygon([(cx + 14, y + 96), (cx + 26, y + 112), (cx + 14, y + 104)],
              fill=(178, 34, 34))
    d.ellipse([cx - 6, y + 34, cx + 6, y + 46], fill=(120, 190, 230),
              outline=(40, 40, 48), width=2)
    _flame(d, cx, y + 112, 26, 30)


def _art_treaty(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(226, 232, 238))
    # Australia flag card (left, tilted look via offset)
    d.rectangle([x + 10, y + 30, x + 82, y + 92], fill=(0, 40, 104),
                outline=(255, 255, 255), width=2)
    d.polygon([(x + 10, y + 30), (x + 46, y + 30), (x + 10, y + 66)],
              fill=(178, 34, 34))
    d.polygon([(x + 82, y + 92), (x + 46, y + 92), (x + 82, y + 56)],
              fill=(178, 34, 34))
    for sx, sy in ((66, 46), (66, 76), (52, 60), (74, 60)):
        d.ellipse([x + sx - 3, y + sy - 3, x + sx + 3, y + sy + 3],
                  fill=(255, 255, 255))
    # Solomon Islands flag card (right)
    d.rectangle([x + 66, y + 56, x + 138, y + 118], fill=(0, 90, 160),
                outline=(255, 255, 255), width=2)
    d.polygon([(x + 66, y + 118), (x + 138, y + 56), (x + 138, y + 66),
               (x + 66, y + 118)], fill=(252, 209, 22))
    d.polygon([(x + 66, y + 118), (x + 138, y + 118), (x + 138, y + 66)],
              fill=(0, 130, 70))
    for sx, sy in ((80, 70), (94, 64), (108, 70), (122, 64), (88, 80)):
        d.ellipse([x + sx - 2, y + sy - 2, x + sx + 2, y + sy + 2],
                  fill=(255, 255, 255))
    # gold seal
    d.ellipse([x + 56, y + 96, x + 92, y + 132], fill=(217, 164, 65),
              outline=(140, 100, 20), width=2)
    d.ellipse([x + 64, y + 104, x + 84, y + 124], outline=(140, 100, 20), width=2)
    d.text((x + 70, y + 108), "OK", font=sans_bold(13), fill=(90, 60, 10))


def _art_fire(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(240, 226, 200))
    # road
    d.rectangle([x, y + 108, x + s, y + s], fill=(90, 90, 96))
    for lx in range(0, s, 30):
        d.rectangle([x + lx, y + 126, x + lx + 16, y + 130], fill=(250, 220, 80))
    # tanker truck: cab + cylindrical tank
    d.rectangle([x + 14, y + 76, x + 96, y + 106], fill=(200, 200, 200),
                outline=(60, 60, 60), width=2)
    d.ellipse([x + 14, y + 76, x + 34, y + 106], fill=(210, 210, 210),
              outline=(60, 60, 60), width=2)
    d.polygon([(x + 96, y + 78), (x + 122, y + 78), (x + 130, y + 106),
               (x + 96, y + 106)], fill=(178, 34, 34))
    d.rectangle([x + 104, y + 82, x + 118, y + 92], fill=(188, 214, 232))
    d.ellipse([x + 30, y + 102, x + 46, y + 118], fill=(20, 20, 20))
    d.ellipse([x + 104, y + 102, x + 120, y + 118], fill=(20, 20, 20))
    # big fire above the tank
    _flame(d, x + 60, y + 78, 56, 62)
    _flame(d, x + 92, y + 78, 34, 40)
    # smoke
    d.ellipse([x + 40, y + 8, x + 66, y + 30], fill=(110, 110, 110))
    d.ellipse([x + 58, y + 2, x + 84, y + 22], fill=(130, 130, 130))
    d.ellipse([x + 78, y + 10, x + 100, y + 28], fill=(110, 110, 110))


def _art_rescue(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(214, 230, 240))
    # supermarket building
    d.rectangle([x + 12, y + 52, x + 136, y + 128], fill=(250, 250, 245),
                outline=(60, 60, 60), width=2)
    d.rectangle([x + 12, y + 52, x + 136, y + 70], fill=(0, 110, 90))
    d.text((x + 22, y + 54), "MARKET", font=sans_bold(13), fill=(255, 255, 255))
    for wx in (24, 58, 92):
        d.rectangle([x + wx, y + 80, x + wx + 26, y + 104], fill=(150, 200, 230),
                    outline=(60, 60, 60), width=1)
    d.rectangle([x + 64, y + 104, x + 84, y + 128], fill=(120, 90, 60))
    # shield badge with check
    d.polygon([(x + 108, y + 8), (x + 138, y + 18), (x + 138, y + 40),
               (x + 123, y + 56), (x + 108, y + 40)], fill=(0, 130, 70),
              outline=(255, 255, 255), width=2)
    d.line([(x + 114, y + 32), (x + 121, y + 40), (x + 133, y + 24)],
           fill=(255, 255, 255), width=4)
    # small figures walking out (rescued people)
    for fx in (30, 52, 74):
        d.ellipse([x + fx, y + 112, x + fx + 8, y + 120], fill=(40, 40, 48))
        d.rectangle([x + fx + 1, y + 120, x + fx + 7, y + 134],
                    fill=(40, 120, 180))


ART = {
    "tanker": _art_tanker,
    "refinery": _art_refinery,
    "rocket": _art_rocket,
    "treaty": _art_treaty,
    "fire": _art_fire,
    "rescue": _art_rescue,
}

# ---------------------------------------------------------------- page


def build_image():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 118], fill=NAVY)
    title_font = serif_bold(64)
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=title_font)
    d.text(((W - tw) / 2, 12), title, font=title_font, fill=(255, 255, 255))
    d.rectangle([40, 92, W - 40, 94], fill=GOLD)
    date_font = sans_bold(23)
    date_line = "THURSDAY, 26 NOVEMBER 2026"
    dw = d.textlength(date_line, font=date_font)
    d.text(((W - dw) / 2, 96 - 4 + 4), date_line, font=date_font, fill=GOLD)

    # ---- standfirst bar ----
    stand_font = sans_bold(17)
    stand = "SIX STORIES FROM AROUND THE WORLD  \u00b7  25\u201326 NOVEMBER 2026"
    sw = d.textlength(stand, font=stand_font)
    d.text(((W - sw) / 2, 128), stand, font=stand_font, fill=RED)
    d.line([18, 152, W - 18, 152], fill=INK, width=2)

    # ---- story grid: 2 columns x 3 rows ----
    margin = 18
    gap = 14
    top = 162
    panel_w = (W - 2 * margin - gap) // 2
    panel_h = 268
    row_gap = 12

    kicker_font = sans_bold(16)
    head_font = serif_bold(25)
    summ_font = sans(18)
    src_font = sans_oblique(14)

    for i, st in enumerate(STORIES):
        col = i % 2
        row = i // 2
        px = margin + col * (panel_w + gap)
        py = top + row * (panel_h + row_gap)

        d.rectangle([px, py, px + panel_w, py + panel_h], fill=PANEL_BG,
                    outline=PANEL_EDGE, width=2)
        # kicker
        d.text((px + 12, py + 9), st["kicker"], font=kicker_font, fill=RED)
        d.line([px + 12, py + 32, px + panel_w - 12, py + 32],
               fill=PANEL_EDGE, width=1)

        # illustration, left
        art_x, art_y, art_s = px + 12, py + 42, 148
        d.rectangle([art_x, art_y, art_x + art_s, art_y + art_s],
                    outline=PANEL_EDGE, width=1)
        ART[st["art"]](d, art_x, art_y, art_s)

        # headline, right of the illustration
        hx = px + 172
        hw = panel_w - 172 - 12
        head_lines = wrap_text(d, st["headline"], head_font, hw)
        draw_lines(d, head_lines, head_font, hx, py + 44, INK, 31,
                   max_lines=3)

        # summary, full width under the illustration
        sx = px + 12
        sw_ = panel_w - 24
        summ_lines = wrap_text(d, st["summary"], summ_font, sw_)
        draw_lines(d, summ_lines, summ_font, sx, py + 196, INK, 23,
                   max_lines=2)

        # source line
        d.text((px + 12, py + panel_h - 20), st["source"], font=src_font,
               fill=GREY)

    # ---- footnote ----
    foot_font = sans(15)
    foot = ("All six stories happened or were first reported on 25\u201326 November 2026.  "
            "Sources: Just Security, Xinhua, Associated Press.")
    fw = d.textlength(foot, font=foot_font)
    d.text(((W - fw) / 2, 1002), foot, font=foot_font, fill=GREY)

    return img


if __name__ == "__main__":
    build_image().save("entry.png")
