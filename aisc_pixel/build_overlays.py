"""Render transparent 1920x1080 PNG title-card overlays for each pixel-style shot.

Typography is rendered deterministically here (with the bundled Press Start 2P
TTF), so the final video has zero risk of AI-introduced misspellings.

Each overlay PNG is then composited onto the corresponding Seedance clip
in the ffmpeg pipeline (see aisc_pixel/build_master.sh).
"""
from __future__ import annotations

import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent
FONT_PATH = ROOT / "fonts" / "PressStart2P-Regular.ttf"
OUT_DIR = ROOT / "overlays"
OUT_DIR.mkdir(exist_ok=True)

W, H = 1920, 1080
BLACK = (10, 10, 10, 255)
CHARTREUSE = (209, 254, 23, 255)
WHITE = (255, 255, 255, 255)


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_PATH), size=size)


def text_size(draw: ImageDraw.ImageDraw, s: str, f: ImageFont.FreeTypeFont) -> tuple[int, int]:
    l, t, r, b = draw.textbbox((0, 0), s, font=f)
    return r - l, b - t


def draw_centered(draw: ImageDraw.ImageDraw, s: str, y: int, f: ImageFont.FreeTypeFont, color=BLACK):
    w, _ = text_size(draw, s, f)
    draw.text(((W - w) // 2, y), s, font=f, fill=color)


def draw_box_shadow(draw: ImageDraw.ImageDraw, s: str, x: int, y: int, f: ImageFont.FreeTypeFont,
                    fg=BLACK, shadow=CHARTREUSE, offset: int = 8):
    """Draw chunky pixel shadow under text (offset chartreuse, then black on top)."""
    draw.text((x + offset, y + offset), s, font=f, fill=shadow)
    draw.text((x, y), s, font=f, fill=fg)


def shot1_boot() -> Path:
    """AISC title screen — big AISC + tagline + PRESS START."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    title_f = font(220)
    sub_f = font(40)
    blink_f = font(36)

    title = "AISC"
    title_w, title_h = text_size(d, title, title_f)
    title_x = (W - title_w) // 2
    title_y = (H - title_h) // 2 - 70
    draw_box_shadow(d, title, title_x, title_y, title_f, fg=BLACK, shadow=CHARTREUSE, offset=10)

    sub = "MARKETING FOR AMBITIOUS AI FOUNDERS"
    sw, sh = text_size(d, sub, sub_f)
    d.text(((W - sw) // 2, title_y + title_h + 60), sub, font=sub_f, fill=BLACK)

    blink = "* PRESS START *"
    bw, bh = text_size(d, blink, blink_f)
    d.text(((W - bw) // 2, H - 130), blink, font=blink_f, fill=BLACK)

    out = OUT_DIR / "01.png"
    img.save(out)
    return out


def shot2_scoreboard() -> Path:
    """Three stat rows. Generous left margin so AI icons can live there."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    stat_f = font(110)
    label_f = font(32)

    stats = [
        ("200+", "CREATORS"),
        ("10M+", "REACH"),
        ("126", "CAMPAIGNS SHIPPED"),
    ]
    row_h = 250
    top = (H - row_h * len(stats)) // 2 + 20
    x_text = 540

    for i, (num, label) in enumerate(stats):
        y = top + i * row_h
        draw_box_shadow(d, num, x_text, y, stat_f, fg=BLACK, shadow=CHARTREUSE, offset=8)
        d.text((x_text + 10, y + 130), label, font=label_f, fill=BLACK)

    out = OUT_DIR / "02.png"
    img.save(out)
    return out


def shot3_endcard() -> Path:
    """End card — AISC big on right, tagline, contact, booking note."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    title_f = font(220)
    tag_f = font(28)
    contact_f = font(28)
    booking_f = font(34)

    title = "AISC"
    tw, th = text_size(d, title, title_f)
    base_x = W - tw - 140
    base_y = (H - th) // 2 - 80
    draw_box_shadow(d, title, base_x, base_y, title_f, fg=BLACK, shadow=CHARTREUSE, offset=10)

    tag1 = "MARKETING FOR"
    tag2 = "AMBITIOUS AI FOUNDERS"
    tag1_w, _ = text_size(d, tag1, tag_f)
    tag2_w, _ = text_size(d, tag2, tag_f)
    d.text((base_x + tw - tag1_w, base_y + th + 30), tag1, font=tag_f, fill=BLACK)
    d.text((base_x + tw - tag2_w, base_y + th + 70), tag2, font=tag_f, fill=BLACK)

    contact_lines = [
        "@AISCWORK",
        "AISCWORK.COM",
    ]
    cy = base_y + th + 140
    for line in contact_lines:
        lw, _ = text_size(d, line, contact_f)
        d.text((base_x + tw - lw, cy), line, font=contact_f, fill=BLACK)
        cy += 40

    booking = "NOW BOOKING Q3 2026"
    bw, _ = text_size(d, booking, booking_f)
    d.text((base_x + tw - bw, cy + 30), booking, font=booking_f, fill=CHARTREUSE)
    d.text((base_x + tw - bw, cy + 30), booking, font=booking_f, fill=BLACK)

    out = OUT_DIR / "03.png"
    img.save(out)
    return out


def main():
    paths = [shot1_boot(), shot2_scoreboard(), shot3_endcard()]
    for p in paths:
        st = p.stat()
        print(f"{p}  {st.st_size:,} bytes")


if __name__ == "__main__":
    main()
