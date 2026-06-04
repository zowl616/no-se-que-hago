"""Render transparent 1920x1080 PNG title-card overlays for the Honest Greens
restaurant-style launch (Alboroto pattern: stick to brand colors and real photos).

Palette: deep-forest-green #1F4D3A + warm cream #F1ECDC + jet black + warm-gold #E8B662.
Type: Anton + Archivo Black + Inter (OFL).
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


def text_with_halo(img, x, y, s, fnt, color=BLACK, halo=CREAM, off=3, halo_alpha=210):
    scratch = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(scratch)
    for dx, dy in [(-off, 0), (off, 0), (0, -off), (0, off),
                   (-off, -off), (off, -off), (-off, off), (off, off)]:
        sd.text((x + dx, y + dy), s, font=fnt, fill=(*halo[:3], halo_alpha))
    img.alpha_composite(scratch)
    ImageDraw.Draw(img).text((x, y), s, font=fnt, fill=color)


def stamp_box(img, x, y, text, fnt, fill=BLACK, pad_x=18, pad_y=12, border=4, angle=0):
    scratch = Image.new("RGBA", (1400, 200), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scratch)
    l, t, r, b = sd.textbbox((40, 40), text, font=fnt)
    sd.rectangle((l - pad_x, t - pad_y, r + pad_x, b + pad_y), outline=fill, width=border)
    sd.text((40, 40), text, font=fnt, fill=fill)
    cropped = scratch.crop((l - pad_x - 4, t - pad_y - 4, r + pad_x + 4, b + pad_y + 4))
    if angle:
        cropped = cropped.rotate(angle, resample=Image.BICUBIC, expand=True)
    img.alpha_composite(cropped, dest=(x, y))


def shot1_real_food_hero() -> Path:
    """Sit on top of the actual HG summer-plate photo. White halos so the type
    pops on the busy real food image."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Hand-stamped diagonal "EAT REAL." in the upper-left, chartreuse outline stamp
    stamp_box(img, 80, 80, "EAT REAL.", f_archivo(64), fill=CREAM, angle=-7)

    # Big Anton wordmark hookline along the bottom
    h1 = "HONEST"
    h2 = "GREENS."
    head_f = f_anton(220)
    l1, t1, r1, b1 = measure(d, h1, head_f)
    base_y = H - 360
    text_with_halo(img, 100 - l1, base_y - t1, h1, head_f, color=CREAM, halo=BLACK, off=3, halo_alpha=210)
    l2, t2, r2, b2 = measure(d, h2, head_f)
    text_with_halo(img, 100 - l2, base_y + (b1 - t1) - 30 - t2, h2, head_f, color=CREAM, halo=BLACK, off=3, halo_alpha=210)

    bar_y = base_y + (b1 - t1) + (b2 - t2) - 5
    d.rectangle((100, bar_y + 10, 100 + max(r1 - l1, r2 - l2), bar_y + 18), fill=GOLD)

    sub = "REAL FOOD REVOLUTION  ·  CHEF DRIVEN  ·  SEASONAL"
    sub_f = f_inter("medium", 30)
    l3, t3, r3, b3 = measure(d, sub, sub_f)
    text_with_halo(img, 100 - l3, bar_y + 38 - t3, sub, sub_f, color=CREAM, halo=BLACK, off=2, halo_alpha=200)

    out = OUT / "01.png"
    img.save(out)
    return out


def shot2_collection() -> Path:
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    head = "+100 PLATES,"
    head2 = "ZERO COMPROMISE."
    head_f = f_anton(140)
    l1, t1, r1, b1 = measure(d, head, head_f)
    text_with_halo(img, 80 - l1, 90 - t1, head, head_f, color=GREEN, halo=CREAM, off=2, halo_alpha=200)
    l2, t2, r2, b2 = measure(d, head2, head_f)
    text_with_halo(img, 80 - l2, 90 + (b1 - t1) - 35 - t2, head2, head_f, color=GREEN, halo=CREAM, off=2, halo_alpha=200)

    bar_y = 90 + (b1 - t1) + (b2 - t2) - 15
    d.rectangle((80, bar_y, 80 + max(r1 - l1, r2 - l2), bar_y + 8), fill=GOLD)

    sub = "GARDEN BOWLS  ·  BREAKFAST  ·  COFFEE & DRINKS  ·  SWEET CORNER"
    sub_f = f_inter("bold", 28)
    ls, ts, rs, bs = measure(d, sub, sub_f)
    text_with_halo(img, 80 - ls, bar_y + 28 - ts, sub, sub_f, color=BLACK, halo=CREAM, off=2, halo_alpha=200)

    foot = "to share."
    foot_f = f_inter("medium", 32)
    lf, tf, rf, bf = measure(d, foot, foot_f)
    text_with_halo(img, 80 - lf, H - 100 - tf, foot, foot_f, color=BLACK, halo=CREAM, off=2, halo_alpha=200)

    # Top-right small brand mark (no text — tracked caps)
    mark = "HONEST GREENS ®"
    mark_f = f_inter("bold", 22)
    lm, tm, rm, bm = measure(d, mark, mark_f)
    text_with_halo(img, W - 80 - (rm - lm) - lm, 80 - tm, mark, mark_f, color=GREEN, halo=CREAM, off=2, halo_alpha=200)

    out = OUT / "02.png"
    img.save(out)
    return out


def shot3_end_card() -> Path:
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    title = "HONEST"
    title2 = "GREENS."
    title_f = f_anton(220)
    lt, tt, rt, bt = measure(d, title, title_f)
    base_x = W - max(rt - lt, 600) - 140 - lt
    base_y = (H - (bt - tt) * 2) // 2 - 80 - tt
    text_with_halo(img, base_x, base_y, title, title_f, color=CREAM, halo=BLACK, off=2, halo_alpha=180)
    lt2, tt2, rt2, bt2 = measure(d, title2, title_f)
    text_with_halo(img, base_x, base_y + (bt - tt) - 30 - tt2 + tt, title2, title_f, color=CREAM, halo=BLACK, off=2, halo_alpha=180)

    right_edge = base_x + lt + max(rt - lt, rt2 - lt2)

    tag = "REAL FOOD REVOLUTION."
    tag_f = f_inter("bold", 38)
    lg, tg, rg, bg = measure(d, tag, tag_f)
    text_with_halo(img, right_edge - (rg - lg) - lg, base_y + (bt - tt) * 2 - 10 - tg, tag, tag_f, color=GOLD, halo=BLACK, off=1, halo_alpha=180)

    bar_y = base_y + (bt - tt) * 2 - 10 + (bg - tg) + 30
    d.rectangle((right_edge - 380, bar_y, right_edge, bar_y + 8), fill=GOLD)

    cta = "ORDER NOW"
    cta_f = f_archivo(56)
    lc, tc, rc, bc = measure(d, cta, cta_f)
    text_with_halo(img, right_edge - (rc - lc) - lc, bar_y + 28 - tc, cta, cta_f, color=CREAM, halo=BLACK, off=2, halo_alpha=180)

    url = "HONESTGREENS.COM"
    url_f = f_inter("bold", 30)
    lu, tu, ru, bu = measure(d, url, url_f)
    text_with_halo(img, right_edge - (ru - lu) - lu, bar_y + 28 + (bc - tc) + 28 - tu, url, url_f, color=CREAM, halo=BLACK, off=1, halo_alpha=180)

    foot = "EAT REAL  ·  CHEF DRIVEN  ·  NO ADDITIVES  ·  NO PRESERVATIVES"
    foot_f = f_inter("medium", 22)
    lff, tff, rff, bff = measure(d, foot, foot_f)
    text_with_halo(img, 80 - lff, H - 80 - tff, foot, foot_f, color=CREAM, halo=BLACK, off=1, halo_alpha=180)

    out = OUT / "03.png"
    img.save(out)
    return out


def main():
    for p in (shot1_real_food_hero(), shot2_collection(), shot3_end_card()):
        print(f"  ✓ {p}  {p.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
