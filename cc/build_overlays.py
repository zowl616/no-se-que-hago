"""Render transparent 1920x1080 PNG title-card overlays for Cold Culture
SUMMER 26 launch.

Palette: jet black + warm cream #F4ECDC + sun-gold #E8B662 highlights.
Typography rendered deterministically with PIL (Anton + Archivo Black + Inter).
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent
FONTS = ROOT / "fonts"
OUT = ROOT / "overlays"
OUT.mkdir(exist_ok=True)

W, H = 1920, 1080
BLACK = (15, 15, 15, 255)
CREAM = (244, 236, 220, 255)
GOLD = (232, 182, 98, 255)
WHITE = (255, 255, 255, 255)


def f_archivo(size): return ImageFont.truetype(str(FONTS / "ArchivoBlack-Regular.ttf"), size=size)
def f_anton(size): return ImageFont.truetype(str(FONTS / "Anton-Regular.ttf"), size=size)
def f_inter(weight, size):
    m = {"bold": "Inter-Bold.ttf", "medium": "Inter-Medium.ttf", "regular": "Inter-Regular.ttf"}
    return ImageFont.truetype(str(FONTS / m[weight]), size=size)


def measure(d, s, fnt): return d.textbbox((0, 0), s, font=fnt)


def text_with_shadow(img, x, y, s, fnt, color=BLACK, shadow=WHITE, offset=3):
    """Black text on bright beach can blow out — add a subtle white halo."""
    if shadow:
        scratch = Image.new("RGBA", img.size, (0, 0, 0, 0))
        sd = ImageDraw.Draw(scratch)
        for dx, dy in [(-offset, 0), (offset, 0), (0, -offset), (0, offset),
                       (-offset, -offset), (offset, -offset), (-offset, offset), (offset, offset)]:
            sd.text((x + dx, y + dy), s, font=fnt, fill=(*shadow[:3], 200))
        img.alpha_composite(scratch)
    d = ImageDraw.Draw(img)
    d.text((x, y), s, font=fnt, fill=color)


def shot1_hero() -> Path:
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    eyebrow = "SUMMER 26  ·  COLD CULTURE™"
    eb_f = f_inter("bold", 30)
    le, te, re_, be = measure(d, eyebrow, eb_f)
    text_with_shadow(img, 100 - le, 100 - te, eyebrow, eb_f, color=BLACK)

    head_f = f_anton(220)
    h1, h2 = "HOT TAKES,", "COLD CULTURE."
    l1, t1, r1, b1 = measure(d, h1, head_f)
    text_with_shadow(img, 100 - l1, 165 - t1, h1, head_f)
    l2, t2, r2, b2 = measure(d, h2, head_f)
    text_with_shadow(img, 100 - l2, 165 + (b1 - t1) - 30 - t2, h2, head_f)

    bar_y = 165 + (b1 - t1) + (b2 - t2) - 5
    d.rectangle((100, bar_y, 700, bar_y + 8), fill=GOLD)

    sub = "THE SUMMER 26 COLLECTION"
    sub_f = f_inter("bold", 36)
    ls, ts, rs, bs = measure(d, sub, sub_f)
    text_with_shadow(img, 100 - ls, bar_y + 30 - ts, sub, sub_f)

    cities = "MADRID  ·  MILAN  ·  PARIS  ·  AMSTERDAM  ·  BARCELONA  ·  VALENCIA"
    c_f = f_inter("medium", 26)
    lc, tc, rc, bc = measure(d, cities, c_f)
    text_with_shadow(img, 100 - lc, H - 90 - tc, cities, c_f)

    out = OUT / "01.png"
    img.save(out)
    return out


def shot2_collection() -> Path:
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    head = "WORN BY THE WORLD"
    head_f = f_archivo(96)
    lh, th, rh, bh = measure(d, head, head_f)
    head_w = rh - lh
    text_with_shadow(img, (W - head_w) // 2 - lh, 70 - th, head, head_f)

    bar_w = head_w + 100
    d.rectangle(((W - bar_w) // 2, 70 + (bh - th) + 16, (W + bar_w) // 2, 70 + (bh - th) + 24), fill=GOLD)

    sub = "SUMMER 26  ·  THE NEW DROP"
    sub_f = f_inter("bold", 32)
    ls, ts, rs, bs = measure(d, sub, sub_f)
    text_with_shadow(img, (W - (rs - ls)) // 2 - ls, 70 + (bh - th) + 50 - ts, sub, sub_f)

    looks = [
        ("LOOK 01", "STARS TEE", 320),
        ("LOOK 02", "ASTRO HOODIE", 960),
        ("LOOK 03", "CASINO POLO", 1600),
    ]
    look_f = f_inter("bold", 28)
    name_f = f_inter("medium", 26)
    base_y = H - 200
    for code, name, cx in looks:
        lc, tc, rc, bc = measure(d, code, look_f)
        text_with_shadow(img, cx - (rc - lc) // 2 - lc, base_y - tc, code, look_f)
        ln, tn, rn, bn = measure(d, name, name_f)
        text_with_shadow(img, cx - (rn - ln) // 2 - ln, base_y + 44 - tn, name, name_f)

    cta = "AVAILABLE NOW"
    cta_f = f_archivo(60)
    lc, tc, rc, bc = measure(d, cta, cta_f)
    text_with_shadow(img, (W - (rc - lc)) // 2 - lc, H - 100 - tc, cta, cta_f)

    out = OUT / "02.png"
    img.save(out)
    return out


def shot3_end_card() -> Path:
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    title = "COLD CULTURE™"
    title_f = f_anton(180)
    lt, tt, rt, bt = measure(d, title, title_f)
    tw, th_ = rt - lt, bt - tt
    base_x = W - tw - 120 - lt
    base_y = 240 - tt
    text_with_shadow(img, base_x, base_y, title, title_f)

    right_edge = base_x + lt + tw

    line1 = "WORLDWIDE STREETWEAR"
    line2 = "AN INTERNATIONAL MOVEMENT"
    line_f = f_inter("bold", 36)
    l1, t1, r1, b1 = measure(d, line1, line_f)
    text_with_shadow(img, right_edge - (r1 - l1) - l1, base_y + tt + th_ + 30 - t1, line1, line_f)
    l2, t2, r2, b2 = measure(d, line2, line_f)
    text_with_shadow(img, right_edge - (r2 - l2) - l2, base_y + tt + th_ + 80 - t2, line2, line_f)

    bar_y = base_y + tt + th_ + 145
    d.rectangle((right_edge - 360, bar_y, right_edge, bar_y + 8), fill=GOLD)

    cta = "SUMMER 26 — OUT NOW"
    cta_f = f_archivo(64)
    lc, tc, rc, bc = measure(d, cta, cta_f)
    text_with_shadow(img, right_edge - (rc - lc) - lc, bar_y + 28 - tc, cta, cta_f)

    url = "COLDCULTUREWORLDWIDE.COM"
    url_f = f_inter("bold", 32)
    lu, tu, ru, bu = measure(d, url, url_f)
    text_with_shadow(img, right_edge - (ru - lu) - lu, bar_y + 28 + (bc - tc) + 30 - tu, url, url_f)

    sayings = "INSPIRING CREATIVITY  ·  EXPRESSION  ·  WORLDWIDE CITIES"
    s_f = f_inter("medium", 26)
    ls, ts, rs, bs = measure(d, sayings, s_f)
    text_with_shadow(img, (W - (rs - ls)) // 2 - ls, H - 90 - ts, sayings, s_f)

    out = OUT / "03.png"
    img.save(out)
    return out


def main():
    for p in (shot1_hero(), shot2_collection(), shot3_end_card()):
        print(f"  ✓ {p}  {p.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
