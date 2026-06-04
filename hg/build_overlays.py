"""Render transparent 1920x1080 PNG title-card overlays for Honest Greens launch.
Palette: deep-forest-green #1F4D3A + warm cream #F1ECDC + jet black + sun-gold #E8B662.
Type: Anton + Archivo Black + Inter (OFL). Halos for legibility on busy food photography.
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
GREEN = (31, 77, 58, 255)
CREAM = (241, 236, 220, 255)
GOLD = (232, 182, 98, 255)
WHITE = (255, 255, 255, 255)


def f_archivo(s): return ImageFont.truetype(str(FONTS / "ArchivoBlack-Regular.ttf"), s)
def f_anton(s): return ImageFont.truetype(str(FONTS / "Anton-Regular.ttf"), s)
def f_inter(w, s):
    m = {"bold": "Inter-Bold.ttf", "medium": "Inter-Medium.ttf", "regular": "Inter-Regular.ttf"}
    return ImageFont.truetype(str(FONTS / m[w]), s)


def measure(d, s, fnt): return d.textbbox((0, 0), s, font=fnt)


def text_with_halo(img, x, y, s, fnt, color=BLACK, halo=CREAM, off=3):
    scratch = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(scratch)
    for dx, dy in [(-off, 0), (off, 0), (0, -off), (0, off),
                   (-off, -off), (off, -off), (-off, off), (off, off)]:
        sd.text((x + dx, y + dy), s, font=fnt, fill=(*halo[:3], 210))
    img.alpha_composite(scratch)
    ImageDraw.Draw(img).text((x, y), s, font=fnt, fill=color)


def shot1_hero() -> Path:
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    eyebrow = "HONEST GREENS  ·  CHEF DRIVEN REAL FOOD"
    eb_f = f_inter("bold", 30)
    le, te, re_, be = measure(d, eyebrow, eb_f)
    text_with_halo(img, 100 - le, 100 - te, eyebrow, eb_f, color=GREEN)

    h1 = "EAT REAL."
    head_f = f_anton(280)
    l1, t1, r1, b1 = measure(d, h1, head_f)
    text_with_halo(img, 100 - l1, 165 - t1, h1, head_f, color=GREEN)

    bar_y = 165 + (b1 - t1) + 18
    d.rectangle((100, bar_y, 700, bar_y + 10), fill=GOLD)

    sub = "REAL FOOD REVOLUTION"
    sub_f = f_inter("bold", 38)
    ls, ts, rs, bs = measure(d, sub, sub_f)
    text_with_halo(img, 100 - ls, bar_y + 32 - ts, sub, sub_f, color=BLACK)

    foot = "CHEF DRIVEN  ·  SEASONAL  ·  NO ADDITIVES  ·  NO PRESERVATIVES  ·  NO REFINED SUGARS"
    foot_f = f_inter("medium", 24)
    lf, tf, rf, bf = measure(d, foot, foot_f)
    text_with_halo(img, 100 - lf, H - 80 - tf, foot, foot_f, color=BLACK)

    out = OUT / "01.png"
    img.save(out)
    return out


def shot2_collection() -> Path:
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    head = "REAL FOOD REVOLUTION."
    head_f = f_archivo(96)
    lh, th, rh, bh = measure(d, head, head_f)
    head_w = rh - lh
    text_with_halo(img, (W - head_w) // 2 - lh, 70 - th, head, head_f, color=GREEN)

    bar_w = head_w + 100
    d.rectangle(((W - bar_w) // 2, 70 + (bh - th) + 18, (W + bar_w) // 2, 70 + (bh - th) + 26), fill=GOLD)

    sub = "GARDEN BOWLS  ·  BREAKFAST  ·  COFFEE & DRINKS"
    sub_f = f_inter("bold", 32)
    ls, ts, rs, bs = measure(d, sub, sub_f)
    text_with_halo(img, (W - (rs - ls)) // 2 - ls, 70 + (bh - th) + 52 - ts, sub, sub_f, color=BLACK)

    items = [
        ("GARDEN BOWL", "SEASONAL & FRESH", 320),
        ("BREAKFAST", "REAL & WHOLESOME", 960),
        ("HONEST BEANS", "SPECIALTY COFFEE", 1600),
    ]
    name_f = f_inter("bold", 30)
    label_f = f_inter("medium", 24)
    base_y = H - 200
    for name, label, cx in items:
        ln, tn, rn, bn = measure(d, name, name_f)
        text_with_halo(img, cx - (rn - ln) // 2 - ln, base_y - tn, name, name_f, color=GREEN)
        ll, tl, rl, bl = measure(d, label, label_f)
        text_with_halo(img, cx - (rl - ll) // 2 - ll, base_y + 44 - tl, label, label_f, color=BLACK)

    cta = "ORDER NOW"
    cta_f = f_archivo(60)
    lc, tc, rc, bc = measure(d, cta, cta_f)
    text_with_halo(img, (W - (rc - lc)) // 2 - lc, H - 100 - tc, cta, cta_f, color=GREEN)

    out = OUT / "02.png"
    img.save(out)
    return out


def shot3_end_card() -> Path:
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    title = "HONEST GREENS"
    title_f = f_anton(180)
    lt, tt, rt, bt = measure(d, title, title_f)
    tw, th_ = rt - lt, bt - tt
    base_x = W - tw - 120 - lt
    base_y = 230 - tt
    text_with_halo(img, base_x, base_y, title, title_f, color=GREEN)
    right_edge = base_x + lt + tw

    sub = "EAT REAL."
    sub_f = f_anton(140)
    ls, ts, rs, bs = measure(d, sub, sub_f)
    text_with_halo(img, right_edge - (rs - ls) - ls, base_y + tt + th_ + 30 - ts, sub, sub_f, color=GREEN)

    bar_y = base_y + tt + th_ + 30 + (bs - ts) + 30
    d.rectangle((right_edge - 380, bar_y, right_edge, bar_y + 10), fill=GOLD)

    cta = "ORDER NOW"
    cta_f = f_archivo(60)
    lc, tc, rc, bc = measure(d, cta, cta_f)
    text_with_halo(img, right_edge - (rc - lc) - lc, bar_y + 30 - tc, cta, cta_f, color=BLACK)

    url = "HONESTGREENS.COM"
    url_f = f_inter("bold", 32)
    lu, tu, ru, bu = measure(d, url, url_f)
    text_with_halo(img, right_edge - (ru - lu) - lu, bar_y + 30 + (bc - tc) + 28 - tu, url, url_f, color=BLACK)

    sayings = "REAL FOOD  ·  REAL FLAVORS  ·  REAL PEOPLE"
    s_f = f_inter("medium", 28)
    lss, tss, rss, bss = measure(d, sayings, s_f)
    text_with_halo(img, (W - (rss - lss)) // 2 - lss, H - 90 - tss, sayings, s_f, color=BLACK)

    out = OUT / "03.png"
    img.save(out)
    return out


def main():
    for p in (shot1_hero(), shot2_collection(), shot3_end_card()):
        print(f"  ✓ {p}  {p.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
