"""Render 4K vertical (2160×3840, 9:16) PNG overlays for AISC coffee shop launch.

  - Scene 1: AISC sign overlay positioned where the brass panel sits above the door.
              Composited onto the still BEFORE Seedance so the warming-light
              push-in scales the sign with the rest of the frame.
  - Scene 5: tagline reveal — "A new ritual." then "In the heart of Madrid."
              Two stand-alone full-frame cards on warm cream paper.
  - Scene 6: brand card on deep amber — AISC logo + opening line + address + handle.

All typography deterministic — Playfair Display Bold for AISC + tagline, Inter
for supporting copy. Same letterforms across Scene 1 sign and Scene 6 logo.
"""
from __future__ import annotations
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent
FONTS = ROOT / "fonts"
OUT = ROOT / "overlays"
OUT.mkdir(exist_ok=True)

W, H = 2160, 3840  # 4K vertical 9:16

# Palette
CREAM = (245, 235, 218, 255)        # Scene 5 paper
WALNUT = (74, 48, 32, 255)          # Scene 5 text
AMBER = (76, 42, 22, 255)           # Scene 6 background (deep amber-warm)
LIGHT_CREAM = (250, 240, 224, 255)  # Scene 6 logo cream
SOFT_CREAM = (220, 200, 175, 255)   # Scene 6 secondary
SAFFRON = (210, 145, 50, 255)
NEAR_BLACK = (8, 6, 4, 255)
BRASS = (190, 140, 70, 255)


def f_playfair_bold(s): return ImageFont.truetype(str(FONTS / "PlayfairDisplay-Bold.ttf"), s)
def f_playfair_italic(s): return ImageFont.truetype(str(FONTS / "PlayfairDisplay-Italic.ttf"), s)
def f_playfair_reg(s): return ImageFont.truetype(str(FONTS / "PlayfairDisplay-Regular.ttf"), s)
def f_inter(w, s):
    m = {"bold": "Inter-Bold.ttf", "medium": "Inter-Medium.ttf", "regular": "Inter-Regular.ttf"}
    return ImageFont.truetype(str(FONTS / m[w]), s)


def measure(d, s, fnt): return d.textbbox((0, 0), s, font=fnt)


def draw_centered(img, y, s, fnt, color):
    d = ImageDraw.Draw(img)
    l, t, r, b = measure(d, s, fnt)
    d.text(((W - (r - l)) // 2 - l, y - t), s, font=fnt, fill=color)
    return r - l, b - t


# Scene 1 — AISC sign overlay positioned where the brass panel sits above the door.
# We expect the AI's brass panel to be in the upper third, roughly centred horizontally.
# Tracked-caps editorial Playfair Display Bold rendered in dark brass-walnut over
# the panel area.
def shot_01_sign() -> Path:
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Sign text — match the Scene 6 logo proportions exactly
    name = "AISC"
    fnt = f_playfair_bold(150)
    l, t, r, b = measure(d, name, fnt)
    name_w, name_h = r - l, b - t
    # Position roughly upper-third of the 9:16 frame, centred horizontally
    x = (W - name_w) // 2 - l
    y = int(H * 0.33) - name_h // 2 - t
    # Render in deep walnut to read against polished brass
    d.text((x, y), name, font=fnt, fill=(45, 28, 18, 235))
    out = OUT / "01_sign.png"
    img.save(out)
    return out


# Scene 5 — two-line tagline reveal on cream paper
def shot_05_tagline_a() -> Path:
    """First card: 'A new ritual.' centred."""
    img = Image.new("RGBA", (W, H), CREAM)
    line = "A new ritual."
    fnt = f_playfair_italic(220)
    draw_centered(img, H // 2 - 100, line, fnt, WALNUT)
    out = OUT / "05_a.png"
    img.save(out)
    return out


def shot_05_tagline_b() -> Path:
    """Second card: 'A new ritual.' (held) + 'In the heart of Madrid.' (added below)."""
    img = Image.new("RGBA", (W, H), CREAM)
    a_fnt = f_playfair_italic(220)
    b_fnt = f_playfair_italic(140)
    # Line 1 — kept centred slightly above middle
    a_w, a_h = draw_centered(img, H // 2 - 220, "A new ritual.", a_fnt, WALNUT)
    # Line 2 — smaller, below
    draw_centered(img, H // 2 + 80, "In the heart of Madrid.", b_fnt, WALNUT)
    out = OUT / "05_b.png"
    img.save(out)
    return out


# Scene 6 — final brand card on deep amber
def shot_06_brand_card() -> Path:
    img = Image.new("RGBA", (W, H), AMBER)
    d = ImageDraw.Draw(img)

    # Big AISC logo — Playfair Display Bold, must match Scene 1 sign letterforms
    name = "AISC"
    name_f = f_playfair_bold(680)
    name_w, name_h = draw_centered(img, H // 2 - 380, name, name_f, LIGHT_CREAM)

    # Opening line
    line1 = "Opening September 2026  ·  Madrid"
    l1_f = f_playfair_reg(80)
    draw_centered(img, H // 2 + 180, line1, l1_f, SOFT_CREAM)

    # Saffron rule
    rule_y = H // 2 + 360
    rule_w = 480
    d.rectangle(((W - rule_w) // 2, rule_y, (W + rule_w) // 2, rule_y + 6), fill=SAFFRON)

    # Address + handle on a single line, smaller, contrasting clean sans
    line2 = "Calle de Hermosilla 42  ·  @aisc_madrid"
    l2_f = f_inter("medium", 56)
    draw_centered(img, rule_y + 100, line2, l2_f, SOFT_CREAM)

    out = OUT / "06_brand_card.png"
    img.save(out)
    return out


def main():
    for p in (shot_01_sign(), shot_05_tagline_a(), shot_05_tagline_b(), shot_06_brand_card()):
        print(f"  ✓ {p}  {p.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
