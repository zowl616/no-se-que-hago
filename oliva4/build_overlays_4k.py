"""Render all OLIVA & SAL title cards at native 4K (3840×2160) with the
catchier new script.

CATCHIER COPY (replaces v3):
  Scene 1 text card:  "TAPAS, BUT WITH FIRE."   (was: "COMING THIS SEASON.")
  Scene 9 three-beat reveal:
    1) "MORE FIRE."          (was: "NEW.")
    2) "MORE FLAVOR."        (was: "SEASONAL.")
    3) "ONLY AT OLIVA & SAL." (kept)
  Scene 10 brand card:
    italic tagline: "Small plates. Big fire."     (was: "olive · salt · fire.")
    rest of brand info kept verbatim.

Scene 8 corner logo also re-rendered at 4K so it overlays sharply.
"""
from __future__ import annotations
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent
FONTS = ROOT / "fonts"
OUT = ROOT / "overlays"
OUT.mkdir(exist_ok=True)

W, H = 3840, 2160  # 4K

# Palette
PAPER = (250, 247, 239, 255)
INK = (16, 14, 12, 255)
GRAY = (90, 84, 76, 255)
SAFFRON = (210, 145, 50, 255)
WHITE = (245, 240, 230, 255)
NEAR_BLACK = (8, 6, 4, 255)
CHARCOAL = (28, 24, 20, 255)


def f_anton(s): return ImageFont.truetype(str(FONTS / "Anton-Regular.ttf"), s)
def f_archivo(s): return ImageFont.truetype(str(FONTS / "ArchivoBlack-Regular.ttf"), s)
def f_inter(w, s):
    m = {"bold": "Inter-Bold.ttf", "medium": "Inter-Medium.ttf", "regular": "Inter-Regular.ttf"}
    return ImageFont.truetype(str(FONTS / m[w]), s)
def f_playfair(s, italic=False, bold=True):
    if italic: return ImageFont.truetype(str(FONTS / "PlayfairDisplay-Italic.ttf"), s)
    return ImageFont.truetype(str(FONTS / ("PlayfairDisplay-Bold.ttf" if bold else "PlayfairDisplay-Regular.ttf")), s)


def measure(d, s, fnt): return d.textbbox((0, 0), s, font=fnt)


def draw_centered(img, y, s, fnt, color):
    d = ImageDraw.Draw(img)
    l, t, r, b = measure(d, s, fnt)
    d.text(((W - (r - l)) // 2 - l, y - t), s, font=fnt, fill=color)
    return r - l, b - t


# Scene 1 cold-open text card — bold editorial sans on near-black, generous letter spacing
def shot_01_text_card() -> Path:
    img = Image.new("RGBA", (W, H), (8, 6, 4, 255))
    line = "T A P A S ,   B U T   W I T H   F I R E ."
    fnt = f_inter("medium", 120)
    draw_centered(img, (H - 120) // 2, line, fnt, WHITE)
    out = OUT / "01_textcard.png"
    img.save(out)
    return out


# Scene 9 three percussive frames — warm charcoal background, generous spacing
def shot_09_tagline_frames():
    bg = (28, 24, 20, 255)
    lines = ["MORE FIRE.", "MORE FLAVOR.", "ONLY AT OLIVA & SAL."]
    paths = []
    for i, text in enumerate(lines, 1):
        img = Image.new("RGBA", (W, H), bg)
        spaced = "   ".join(text)
        # auto-fit
        for s in (440, 380, 320, 280, 240, 200, 160, 130):
            fnt = f_anton(s)
            d = ImageDraw.Draw(img)
            l, t, r, b = measure(d, spaced, fnt)
            if r - l <= W - 400:
                break
        d = ImageDraw.Draw(img)
        l, t, r, b = measure(d, spaced, fnt)
        d.text(((W - (r - l)) // 2 - l, (H - (b - t)) // 2 - t), spaced, font=fnt, fill=WHITE)
        out = OUT / f"09_{i}.png"
        img.save(out)
        paths.append(out)
    return paths


# Scene 10 brand card — warm-white paper, Playfair Display Bold, NEW catchy tagline
def shot_10_brand_card() -> Path:
    img = Image.new("RGBA", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Eyebrow saffron tracked-caps
    eyebrow = "M E D I T E R R A N E A N   T A P A S"
    eb_f = f_inter("medium", 44)
    draw_centered(img, 500, eyebrow, eb_f, SAFFRON)

    # Big editorial wordmark — Playfair Display Bold
    name = "Oliva & Sal"
    name_f = f_playfair(440, bold=True)
    name_w, name_h = draw_centered(img, 640, name, name_f, INK)

    # Italic tagline (NEW catchy version)
    tag = "Small plates.  Big fire."
    tag_f = f_playfair(100, italic=True)
    draw_centered(img, 640 + name_h + 100, tag, tag_f, GRAY)

    # Saffron rule
    rule_y = 640 + name_h + 100 + 140
    rule_w = 560
    d.rectangle(((W - rule_w) // 2, rule_y, (W + rule_w) // 2, rule_y + 6), fill=SAFFRON)

    # Launch line
    launch_y = rule_y + 100
    draw_centered(img, launch_y, "LAUNCHING 15 SEPTEMBER 2026", f_inter("bold", 64), INK)

    # Address & handle
    addr_y = launch_y + 130
    draw_centered(img, addr_y, "Calle de la Cava Baja 22  ·  Madrid", f_inter("medium", 52), GRAY)
    draw_centered(img, addr_y + 100, "@olivaysal", f_inter("medium", 52), GRAY)

    # Subtle warm vignette
    vignette = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vd = ImageDraw.Draw(vignette)
    cx, cy = W // 2, H // 2
    max_r = int((W ** 2 + H ** 2) ** 0.5 / 2)
    for i in range(0, 30):
        a = int(2 + i * 1.2)
        r = max_r - i * (max_r // 30)
        vd.ellipse((cx - r, cy - int(r * H / W), cx + r, cy + int(r * H / W)), outline=(80, 60, 30, a), width=20)
    img.alpha_composite(vignette)

    out = OUT / "10.png"
    img.save(out)
    return out


# Scene 8 corner logo at 4K
def shot_08_corner_logo() -> Path:
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    name = "OLIVA & SAL"
    fnt = f_anton(116)
    d = ImageDraw.Draw(img)
    l, t, r, b = measure(d, name, fnt)
    x = W - (r - l) - 160 - l
    y = H - (b - t) - 160 - t
    color = (255, 250, 240, 102)  # 40% opacity
    halo_color = (10, 8, 6, 90)
    scratch = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(scratch)
    for dx, dy in [(-4, 0), (4, 0), (0, -4), (0, 4)]:
        sd.text((x + dx, y + dy), name, font=fnt, fill=halo_color)
    img.alpha_composite(scratch)
    ImageDraw.Draw(img).text((x, y), name, font=fnt, fill=color)
    out = OUT / "08.png"
    img.save(out)
    return out


def main():
    paths = [
        shot_01_text_card(),
        *shot_09_tagline_frames(),
        shot_10_brand_card(),
        shot_08_corner_logo(),
    ]
    for p in paths:
        print(f"  ✓ {p}  {p.stat().st_size:,} bytes  ({W}x{H})")


if __name__ == "__main__":
    main()
