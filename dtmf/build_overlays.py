"""Render transparent 1920x1080 PNG title-card overlays for DTMF merch launch.

Palette: cream #FFF5DA + sky-blue #4090C4 + jet black.
Typography rendered deterministically with PIL (Archivo Black + Inter), so the
final video has zero misspellings.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).parent
FONTS = ROOT / "fonts"
OUT = ROOT / "overlays"
OUT.mkdir(exist_ok=True)

W, H = 1920, 1080
BLACK = (15, 15, 15, 255)
SKY = (64, 144, 196, 255)
CREAM = (255, 245, 218, 255)


def f_archivo(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONTS / "ArchivoBlack-Regular.ttf"), size=size)


def f_anton(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONTS / "Anton-Regular.ttf"), size=size)


def f_inter(weight: str, size: int) -> ImageFont.FreeTypeFont:
    weight_map = {"bold": "Inter-Bold.ttf", "medium": "Inter-Medium.ttf", "regular": "Inter-Regular.ttf"}
    return ImageFont.truetype(str(FONTS / weight_map[weight]), size=size)


def measure(d: ImageDraw.ImageDraw, s: str, fnt: ImageFont.FreeTypeFont):
    return d.textbbox((0, 0), s, font=fnt)


def stamp_box(img: Image.Image, x: int, y: int, text: str, fnt: ImageFont.FreeTypeFont, fill=BLACK,
              pad_x: int = 18, pad_y: int = 12, border: int = 4, angle: float = 0):
    scratch = Image.new("RGBA", (1200, 200), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scratch)
    l, t, r, b = sd.textbbox((40, 40), text, font=fnt)
    w_, h_ = r - l, b - t
    sd.rectangle((l - pad_x, t - pad_y, r + pad_x, b + pad_y), outline=fill, width=border)
    sd.text((40, 40), text, font=fnt, fill=fill)
    cropped = scratch.crop((l - pad_x - 4, t - pad_y - 4, r + pad_x + 4, b + pad_y + 4))
    if angle:
        cropped = cropped.rotate(angle, resample=Image.BICUBIC, expand=True)
    img.alpha_composite(cropped, dest=(x, y))


def shot1_hero_tee() -> Path:
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    stamp_box(img, 90, 90, "DROP 01", f_archivo(64), fill=BLACK, angle=-7)

    title_f = f_anton(220)
    title = "DEBÍ TIRAR"
    title2 = "MÁS FOTOS"
    l1, t1, r1, b1 = measure(d, title, title_f)
    l2, t2, r2, b2 = measure(d, title2, title_f)
    base_y = H - 360
    d.text((100 - l1, base_y - t1), title, font=title_f, fill=BLACK)
    d.text((100 - l2, base_y + (b1 - t1) - 30 - t2), title2, font=title_f, fill=BLACK)

    bar_y = base_y + (b1 - t1) + (b2 - t2) - 10
    d.rectangle((100, bar_y + 10, 100 + max(r1 - l1, r2 - l2), bar_y + 18), fill=SKY)

    sub = "WORLD TOUR MERCH  ·  CARIBBEAN COLLECTION"
    sub_f = f_inter("medium", 30)
    l3, t3, r3, b3 = measure(d, sub, sub_f)
    d.text((100 - l3, bar_y + 38 - t3), sub, font=sub_f, fill=BLACK)

    out = OUT / "01.png"
    img.save(out)
    return out


def shot2_collection() -> Path:
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    head = "THE DROP"
    head_f = f_archivo(110)
    l, t, r, b = measure(d, head, head_f)
    head_w = r - l
    d.text(((W - head_w) // 2 - l, 80 - t), head, font=head_f, fill=BLACK)
    bar_w = head_w + 80
    d.rectangle(((W - bar_w) // 2, 80 + (b - t) + 18, (W + bar_w) // 2, 80 + (b - t) + 26), fill=SKY)

    sub = "TEE  ·  HOODIE  ·  CAP"
    sub_f = f_inter("medium", 38)
    l2, t2, r2, b2 = measure(d, sub, sub_f)
    d.text(((W - (r2 - l2)) // 2 - l2, 80 + (b - t) + 60 - t2), sub, font=sub_f, fill=BLACK)

    items = [
        ("CLASSIC TEE", "$45 USD", 320),
        ("PALMA HOODIE", "$95 USD", 960),
        ("CAP", "$35 USD", 1600),
    ]
    name_f = f_inter("bold", 32)
    price_f = f_inter("medium", 28)
    base_y = H - 220
    for name, price, cx in items:
        ln, tn, rn, bn = measure(d, name, name_f)
        d.text((cx - (rn - ln) // 2 - ln, base_y - tn), name, font=name_f, fill=BLACK)
        lp, tp, rp, bp = measure(d, price, price_f)
        d.text((cx - (rp - lp) // 2 - lp, base_y + 50 - tp), price, font=price_f, fill=SKY)

    cta_f = f_archivo(72)
    cta = "AVAILABLE NOW"
    lc, tc, rc, bc = measure(d, cta, cta_f)
    d.text(((W - (rc - lc)) // 2 - lc, H - 110 - tc), cta, font=cta_f, fill=BLACK)

    out = OUT / "02.png"
    img.save(out)
    return out


def shot3_end_card() -> Path:
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    title_f = f_anton(280)
    title = "DTMF"
    l, t, r, b = measure(d, title, title_f)
    tw, th = r - l, b - t
    base_x = W - tw - 160 - l
    base_y = (H - th) // 2 - 130 - t
    d.text((base_x, base_y), title, font=title_f, fill=BLACK)
    right_edge = base_x + l + tw

    full = "DEBÍ TIRAR MÁS FOTOS"
    full_f = f_inter("bold", 38)
    lf, tf, rf, bf = measure(d, full, full_f)
    d.text((right_edge - (rf - lf) - lf, base_y + th + 30 - tf), full, font=full_f, fill=BLACK)

    bar_y = base_y + th + 95
    bar_w = 380
    d.rectangle((right_edge - bar_w, bar_y, right_edge, bar_y + 8), fill=SKY)

    cta = "SHOP THE DROP"
    cta_f = f_archivo(70)
    lc, tc, rc, bc = measure(d, cta, cta_f)
    d.text((right_edge - (rc - lc) - lc, bar_y + 30 - tc), cta, font=cta_f, fill=BLACK)

    url = "DEBITIRARMASFOTOS.COM"
    url_f = f_inter("bold", 32)
    lu, tu, ru, bu = measure(d, url, url_f)
    d.text((right_edge - (ru - lu) - lu, bar_y + 30 + (bc - tc) + 30 - tu), url, font=url_f, fill=SKY)

    out_now = "OUT NOW"
    on_f = f_archivo(50)
    lo, to_, ro, bo = measure(d, out_now, on_f)
    d.text((right_edge - (ro - lo) - lo, bar_y + 30 + (bc - tc) + 100 - to_), out_now, font=on_f, fill=BLACK)

    foot = "TEE  ·  HOODIE  ·  CAP  ·  VINYL  ·  WORLD TOUR"
    ff = f_inter("medium", 24)
    lff, tff, rff, bff = measure(d, foot, ff)
    d.text((100 - lff, H - 80 - tff), foot, font=ff, fill=BLACK)

    out = OUT / "03.png"
    img.save(out)
    return out


def main():
    for p in (shot1_hero_tee(), shot2_collection(), shot3_end_card()):
        print(f"  ✓ {p}  {p.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
