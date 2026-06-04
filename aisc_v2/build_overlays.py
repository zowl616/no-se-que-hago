"""Render transparent 1920x1080 PNG title-card overlays for each motion-design shot.

Typography is rendered deterministically here (Archivo Black for oversized
headlines + Inter for body), so the final video has zero risk of AI-introduced
misspellings. Each overlay PNG is composited onto its corresponding Seedance
clip in `build_master.sh`.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent
FONTS = ROOT / "fonts"
OUT = ROOT / "overlays"
OUT.mkdir(exist_ok=True)

W, H = 1920, 1080
BLACK = (10, 10, 10, 255)
CHARTREUSE = (209, 254, 23, 255)


def f_archivo(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONTS / "ArchivoBlack-Regular.ttf"), size=size)


def f_inter(weight: str, size: int) -> ImageFont.FreeTypeFont:
    weight_map = {"bold": "Inter-Bold.ttf", "medium": "Inter-Medium.ttf", "regular": "Inter-Regular.ttf"}
    return ImageFont.truetype(str(FONTS / weight_map[weight]), size=size)


def text_size(d: ImageDraw.ImageDraw, s: str, fnt: ImageFont.FreeTypeFont) -> tuple[int, int, int, int]:
    return d.textbbox((0, 0), s, font=fnt)


def draw_centered(d: ImageDraw.ImageDraw, s: str, y: int, fnt: ImageFont.FreeTypeFont, color=BLACK):
    l, t, r, b = text_size(d, s, fnt)
    d.text(((W - (r - l)) // 2 - l, y - t), s, font=fnt, fill=color)


def shot1_wordmark_ignition() -> Path:
    """AISC + tagline + handle + 7 partner-brand wordmark stamps scattered around."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    title = "AISC"
    title_f = f_archivo(360)
    l, t, r, b = text_size(d, title, title_f)
    title_w, title_h = r - l, b - t
    title_x = (W - title_w) // 2 - l
    title_y = (H - title_h) // 2 - 80 - t
    d.text((title_x, title_y), title, font=title_f, fill=BLACK)

    tag = "MARKETING FOR AMBITIOUS AI FOUNDERS"
    tag_f = f_inter("medium", 38)
    l2, t2, r2, b2 = text_size(d, tag, tag_f)
    d.text(((W - (r2 - l2)) // 2 - l2, title_y + title_h + 50 - t2), tag, font=tag_f, fill=BLACK)

    handle = "@AISCWORK   ·   AISCWORK.COM"
    handle_f = f_inter("regular", 26)
    l3, t3, r3, b3 = text_size(d, handle, handle_f)
    d.text(((W - (r3 - l3)) // 2 - l3, title_y + title_h + 110 - t3), handle, font=handle_f, fill=BLACK)

    stamps = [
        ("PERPLEXITY", 200, 130, -8),
        ("HIGGSFIELD", 1500, 110, 6),
        ("RUNWAY", 1620, 230, -4),
        ("LUMA AI", 100, 260, 9),
        ("HEYGEN", 1450, 880, -6),
        ("KLING AI", 250, 920, 4),
        ("PIKA LABS", 900, 940, -2),
    ]
    stamp_f = f_inter("bold", 28)
    for word, sx, sy, angle in stamps:
        scratch = Image.new("RGBA", (560, 80), (0, 0, 0, 0))
        sd = ImageDraw.Draw(scratch)
        sd.text((10, 10), word, font=stamp_f, fill=BLACK)
        l4, t4, r4, b4 = sd.textbbox((10, 10), word, font=stamp_f)
        sd.rectangle((l4 - 12, t4 - 8, r4 + 12, b4 + 8), outline=BLACK, width=3)
        rotated = scratch.rotate(angle, resample=Image.BICUBIC, expand=True)
        img.alpha_composite(rotated, dest=(sx, sy))

    out = OUT / "01.png"
    img.save(out)
    return out


def shot2_stat_slabs() -> Path:
    """Three giant stat headlines stacked vertically with chartreuse underlines."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    stats = [
        ("200+ CREATORS", "OUR NETWORK"),
        ("10M+ REACH", "COMBINED FOLLOWERS"),
        ("126 CAMPAIGNS", "SHIPPED"),
    ]
    headline_f = f_archivo(140)
    label_f = f_inter("medium", 28)

    row_h = 270
    top = (H - row_h * len(stats)) // 2 + 60

    for i, (head, label) in enumerate(stats):
        y = top + i * row_h
        l, t, r, b = text_size(d, head, headline_f)
        head_w, head_h = r - l, b - t
        x = (W - head_w) // 2 - l
        d.text((x, y - t), head, font=headline_f, fill=BLACK)

        bar_y = y + head_h + 18
        bar_x_start = (W - head_w) // 2
        bar_x_end = bar_x_start + head_w
        d.rectangle((bar_x_start, bar_y, bar_x_end, bar_y + 6), fill=CHARTREUSE)

        l2, t2, r2, b2 = text_size(d, label, label_f)
        lw = r2 - l2
        d.text(((W - lw) // 2 - l2, bar_y + 22 - t2), label, font=label_f, fill=BLACK)

    out = OUT / "02.png"
    img.save(out)
    return out


def shot3_end_card() -> Path:
    """End card — AISC big on right + tagline + contact + booking + small foot stats."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    title = "AISC"
    title_f = f_archivo(360)
    l, t, r, b = text_size(d, title, title_f)
    title_w, title_h = r - l, b - t
    base_x = W - title_w - 140 - l
    base_y = (H - title_h) // 2 - 110 - t
    d.text((base_x, base_y), title, font=title_f, fill=BLACK)

    right_edge = base_x + l + title_w

    tag = "MARKETING FOR AMBITIOUS AI FOUNDERS."
    tag_f = f_inter("medium", 32)
    l2, t2, r2, b2 = text_size(d, tag, tag_f)
    d.text((right_edge - (r2 - l2) - l2, base_y + t + title_h + 40 - t2), tag, font=tag_f, fill=BLACK)

    bar_y = base_y + t + title_h + 105
    bar_w = 320
    d.rectangle((right_edge - bar_w, bar_y, right_edge, bar_y + 6), fill=CHARTREUSE)

    handle_f = f_inter("regular", 26)
    handle_lines = ["@AISCWORK", "AISCWORK.COM"]
    cy = bar_y + 30
    for line in handle_lines:
        l3, t3, r3, b3 = text_size(d, line, handle_f)
        d.text((right_edge - (r3 - l3) - l3, cy - t3), line, font=handle_f, fill=BLACK)
        cy += 38

    booking = "NOW BOOKING Q3 2026"
    booking_f = f_inter("bold", 36)
    l4, t4, r4, b4 = text_size(d, booking, booking_f)
    d.text((right_edge - (r4 - l4) - l4, cy + 20 - t4), booking, font=booking_f, fill=BLACK)

    foot = "126 CAMPAIGNS  ·  200+ CREATORS  ·  10M+ REACH"
    foot_f = f_inter("medium", 22)
    l5, t5, r5, b5 = text_size(d, foot, foot_f)
    fy = H - 80 - t5
    d.text((100 - l5, fy), foot, font=foot_f, fill=BLACK)

    out = OUT / "03.png"
    img.save(out)
    return out


def main():
    paths = [shot1_wordmark_ignition(), shot2_stat_slabs(), shot3_end_card()]
    for p in paths:
        print(f"{p}  {p.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
