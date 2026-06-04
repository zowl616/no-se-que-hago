"""Render transparent 1920x1080 PNG overlays for the OLIVA & SAL launch.

Most scenes get only a tiny corner watermark; the heavy typographic frames
(Scene 1 text card, Scene 8 corner logo, Scene 9 tagline reveal, Scene 10 brand
card) are rendered fully here. All glyphs deterministic — zero misspellings.
"""
from __future__ import annotations
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent
FONTS = ROOT / "fonts"
OUT = ROOT / "overlays"
OUT.mkdir(exist_ok=True)

W, H = 1920, 1080
WHITE = (245, 240, 230, 255)
SOFT_WHITE = (245, 240, 230, 230)
NEAR_BLACK = (12, 10, 8, 255)
CHARCOAL = (28, 24, 20, 255)
TERRACOTTA = (198, 108, 58, 255)
SAFFRON = (232, 158, 60, 255)
OLIVE = (104, 124, 56, 255)


def f_anton(s): return ImageFont.truetype(str(FONTS / "Anton-Regular.ttf"), s)
def f_archivo(s): return ImageFont.truetype(str(FONTS / "ArchivoBlack-Regular.ttf"), s)
def f_inter(w, s):
    m = {"bold": "Inter-Bold.ttf", "medium": "Inter-Medium.ttf", "regular": "Inter-Regular.ttf"}
    return ImageFont.truetype(str(FONTS / m[w]), s)
def f_playfair(s, italic=False, bold=True):
    if italic: return ImageFont.truetype(str(FONTS / "PlayfairDisplay-Italic.ttf"), s)
    return ImageFont.truetype(str(FONTS / ("PlayfairDisplay-Bold.ttf" if bold else "PlayfairDisplay-Regular.ttf")), s)


def measure(d, s, fnt): return d.textbbox((0, 0), s, font=fnt)


def text_with_halo(img, x, y, s, fnt, color=WHITE, halo=NEAR_BLACK, off=2, halo_alpha=180):
    scratch = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(scratch)
    for dx, dy in [(-off, 0), (off, 0), (0, -off), (0, off),
                   (-off, -off), (off, -off), (-off, off), (off, off)]:
        sd.text((x + dx, y + dy), s, font=fnt, fill=(*halo[:3], halo_alpha))
    img.alpha_composite(scratch)
    ImageDraw.Draw(img).text((x, y), s, font=fnt, fill=color)


def small_corner_label(img, line, fnt, x=80, y=None, color=SOFT_WHITE):
    if y is None: y = H - 80
    d = ImageDraw.Draw(img)
    l, t, r, b = measure(d, line, fnt)
    text_with_halo(img, x - l, y - t, line, fnt, color=color, off=2)


# Scene 1 (knife slam) – minimal slate; the text card is a SEPARATE asset rendered below
def shot_01_slate() -> Path:
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    out = OUT / "01.png"
    img.save(out)  # intentionally empty — knife clip needs no overlay
    return out


# Scene 1 end text card — stand-alone full-frame asset, used as a separate clip
def shot_01_text_card() -> Path:
    img = Image.new("RGBA", (W, H), (8, 6, 4, 255))  # near-black with slight warmth
    d = ImageDraw.Draw(img)
    line = "C O M I N G   T H I S   S E A S O N ."
    fnt = f_inter("medium", 60)
    l, t, r, b = measure(d, line, fnt)
    d.text(((W - (r - l)) // 2 - l, (H - (b - t)) // 2 - t - 20), line, font=fnt, fill=WHITE)
    out = OUT / "01_textcard.png"
    img.save(out)
    return out


def _empty_corner(name: str) -> Path:
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    out = OUT / f"{name}.png"
    img.save(out)
    return out


def shot_08_corner_logo() -> Path:
    """Subtle white logo lower-right at 40% opacity for the rotation hero."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    name = "OLIVA & SAL"
    fnt = f_anton(58)
    l, t, r, b = measure(d, name, fnt)
    pad_x = 24
    x = W - (r - l) - 80 - l
    y = H - (b - t) - 80 - t
    # Render at 40% opacity
    color = (255, 250, 240, 102)  # 40% of 255
    halo_color = (10, 8, 6, 90)
    scratch = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(scratch)
    for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
        sd.text((x + dx, y + dy), name, font=fnt, fill=halo_color)
    img.alpha_composite(scratch)
    ImageDraw.Draw(img).text((x, y), name, font=fnt, fill=color)
    out = OUT / "08.png"
    img.save(out)
    return out


# Scene 9 — three percussive tagline frames (text-only, charcoal background)
def shot_09_tagline_frames():
    """Three full-frame text cards, one for each beat."""
    bg = (28, 24, 20, 255)  # warm charcoal (not pure black)
    lines = ["NEW.", "SEASONAL.", "ONLY AT OLIVA & SAL."]
    paths = []
    for i, text in enumerate(lines, 1):
        img = Image.new("RGBA", (W, H), bg)
        # Add subtle "linen" noise via faint speckle pattern
        # (small overhead — skip for speed)
        d = ImageDraw.Draw(img)
        # Editorial sans-serif, generous letter-spacing
        size = 220 if i < 3 else 150
        # For long line, use smaller size
        if i == 3:
            size = 130
        spaced = "  ".join(list(text)) if i < 3 else "   ".join(text.split())
        # Actually keep tracked-cap by inserting hair-spaces between letters
        spaced = "   ".join(text)  # works for any length
        fnt = f_anton(size)
        l, t, r, b = measure(d, spaced, fnt)
        if r - l > W - 200:
            # rescale fit
            for s in range(size, 60, -10):
                fnt = f_anton(s)
                l, t, r, b = measure(d, spaced, fnt)
                if r - l <= W - 200:
                    break
        d.text(((W - (r - l)) // 2 - l, (H - (b - t)) // 2 - t), spaced, font=fnt, fill=WHITE)
        out = OUT / f"09_{i}.png"
        img.save(out)
        paths.append(out)
    return paths


# Scene 10 — final brand card
def shot_10_brand_card() -> Path:
    img = Image.new("RGBA", (W, H), (28, 24, 20, 255))  # warm charcoal
    d = ImageDraw.Draw(img)

    # Tiny eyebrow
    eyebrow = "M E D I T E R R A N E A N   T A P A S"
    eb_f = f_inter("medium", 22)
    le, te, re_, be = measure(d, eyebrow, eb_f)
    text_with_halo(img, (W - (re_ - le)) // 2 - le, 280 - te, eyebrow, eb_f,
                   color=SAFFRON, halo=NEAR_BLACK, off=1, halo_alpha=110)

    # Big logo
    name = "OLIVA & SAL"
    name_f = f_anton(220)
    ln, tn, rn, bn = measure(d, name, name_f)
    nw, nh = rn - ln, bn - tn
    name_y = 320
    text_with_halo(img, (W - nw) // 2 - ln, name_y - tn, name, name_f,
                   color=WHITE, halo=NEAR_BLACK, off=2, halo_alpha=150)

    # Italic tagline
    tag = "olive · salt · fire."
    tag_f = f_playfair(46, italic=True)
    lg, tg, rg, bg = measure(d, tag, tag_f)
    text_with_halo(img, (W - (rg - lg)) // 2 - lg, name_y + nh + 30 - tg, tag, tag_f,
                   color=(238, 230, 215, 240), halo=NEAR_BLACK, off=1, halo_alpha=120)

    # Saffron rule
    rule_y = name_y + nh + 30 + (bg - tg) + 35
    rule_w = 280
    d.rectangle(((W - rule_w) // 2, rule_y, (W + rule_w) // 2, rule_y + 3), fill=SAFFRON)

    # Launch line
    launch = "LAUNCHING 15 SEPTEMBER 2026"
    launch_f = f_inter("bold", 32)
    ll, tl, rl, bl = measure(d, launch, launch_f)
    text_with_halo(img, (W - (rl - ll)) // 2 - ll, rule_y + 30 - tl, launch, launch_f,
                   color=WHITE, halo=NEAR_BLACK, off=1, halo_alpha=120)

    # Address
    addr = "Calle de la Cava Baja 22  ·  Madrid"
    addr_f = f_inter("medium", 26)
    la, ta, ra, ba = measure(d, addr, addr_f)
    text_with_halo(img, (W - (ra - la)) // 2 - la, rule_y + 80 - ta, addr, addr_f,
                   color=(220, 210, 192, 230), halo=NEAR_BLACK, off=1, halo_alpha=120)

    # Handle
    handle = "@olivaysal"
    handle_f = f_inter("medium", 26)
    lh, th_, rh, bh = measure(d, handle, handle_f)
    text_with_halo(img, (W - (rh - lh)) // 2 - lh, rule_y + 130 - th_, handle, handle_f,
                   color=(220, 210, 192, 230), halo=NEAR_BLACK, off=1, halo_alpha=120)

    out = OUT / "10.png"
    img.save(out)
    return out


def main():
    paths = [
        shot_01_slate(),
        shot_01_text_card(),
        _empty_corner("02"),
        _empty_corner("03"),
        _empty_corner("04"),
        _empty_corner("05a"),
        _empty_corner("05b"),
        _empty_corner("05c"),
        _empty_corner("06"),
        _empty_corner("07"),
        shot_08_corner_logo(),
        *shot_09_tagline_frames(),
        shot_10_brand_card(),
    ]
    for p in paths:
        print(f"  ✓ {p}  {p.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
