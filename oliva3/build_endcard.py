"""Render the new Scene 10 brand card on a warm-white background with a
refined editorial-serif typography pivot (Playfair Display Bold + Italic).

Replaces the old Anton-on-charcoal end card with a Bon-Appétit / Cereal-magazine
feel — pure paper, jet black, single saffron accent rule.
"""
from __future__ import annotations
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent
FONTS = ROOT / "fonts"
OUT = ROOT / "overlays" / "10.png"
W, H = 1920, 1080

# Warm-white paper, not pure #FFFFFF — slightly cream for a premium magazine feel
PAPER = (250, 247, 239, 255)
INK = (16, 14, 12, 255)
GRAY = (90, 84, 76, 255)
SAFFRON = (210, 145, 50, 255)


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


def main():
    img = Image.new("RGBA", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Tiny eyebrow tracked-caps in saffron
    eyebrow = "M E D I T E R R A N E A N   T A P A S"
    eb_f = f_inter("medium", 22)
    draw_centered(img, 250, eyebrow, eb_f, SAFFRON)

    # Big editorial wordmark — Playfair Display Bold (was Anton)
    name = "Oliva & Sal"
    name_f = f_playfair_bold(220)
    name_w, name_h = draw_centered(img, 320, name, name_f, INK)

    # Italic tagline — Playfair Display Italic
    tag = "olive · salt · fire."
    tag_f = f_playfair_italic(50)
    draw_centered(img, 320 + name_h + 50, tag, tag_f, GRAY)

    # Thin saffron rule
    rule_y = 320 + name_h + 50 + 70
    rule_w = 280
    d.rectangle(((W - rule_w) // 2, rule_y, (W + rule_w) // 2, rule_y + 3), fill=SAFFRON)

    # Launch line
    launch_y = rule_y + 50
    draw_centered(img, launch_y, "LAUNCHING 15 SEPTEMBER 2026", f_inter("bold", 32), INK)

    # Address & handle
    addr_y = launch_y + 65
    draw_centered(img, addr_y, "Calle de la Cava Baja 22  ·  Madrid", f_inter("medium", 26), GRAY)
    draw_centered(img, addr_y + 50, "@olivaysal", f_inter("medium", 26), GRAY)

    # Subtle warm vignette around the edges using a radial darkening
    vignette = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vd = ImageDraw.Draw(vignette)
    # Approximate a vignette by drawing concentric ellipses with rising alpha at the edges
    cx, cy = W // 2, H // 2
    max_r = int((W ** 2 + H ** 2) ** 0.5 / 2)
    for i in range(0, 30):
        # Outer ring darker, inner transparent
        a = int(2 + i * 1.2)  # very light
        r = max_r - i * (max_r // 30)
        vd.ellipse((cx - r, cy - int(r * H / W), cx + r, cy + int(r * H / W)), outline=(80, 60, 30, a), width=10)
    img.alpha_composite(vignette)

    img.save(OUT)
    print(f"  ✓ {OUT}  {OUT.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
