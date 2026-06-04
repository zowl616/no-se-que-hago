"""Render transparent 1920x1080 PNG title-card overlays for the cinematic
Honest Greens reel.

Scene 5 carries the full editorial brand reveal (Playfair Display).
Other scenes get only minimal corner / title cues (deterministic, no
misspellings, low-contrast white-on-warm).
"""
from __future__ import annotations
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent
FONTS = ROOT / "fonts"
OUT = ROOT / "overlays"
OUT.mkdir(exist_ok=True)

W, H = 1920, 1080
WHITE = (245, 240, 230, 235)
GOLD = (220, 175, 110, 255)
NEAR_BLACK = (12, 18, 22, 255)
SUBTLE = (230, 220, 200, 180)


def f_playfair_bold(s): return ImageFont.truetype(str(FONTS / "PlayfairDisplay-Bold.ttf"), s)
def f_playfair_italic(s): return ImageFont.truetype(str(FONTS / "PlayfairDisplay-Italic.ttf"), s)
def f_playfair_reg(s): return ImageFont.truetype(str(FONTS / "PlayfairDisplay-Regular.ttf"), s)
def f_inter(w, s):
    m = {"bold": "Inter-Bold.ttf", "medium": "Inter-Medium.ttf", "regular": "Inter-Regular.ttf"}
    return ImageFont.truetype(str(FONTS / m[w]), s)


def measure(d, s, fnt): return d.textbbox((0, 0), s, font=fnt)


def text_with_halo(img, x, y, s, fnt, color=WHITE, halo=NEAR_BLACK, off=2, halo_alpha=110):
    scratch = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(scratch)
    for dx, dy in [(-off, 0), (off, 0), (0, -off), (0, off),
                   (-off, -off), (off, -off), (-off, off), (off, off)]:
        sd.text((x + dx, y + dy), s, font=fnt, fill=(*halo[:3], halo_alpha))
    img.alpha_composite(scratch)
    ImageDraw.Draw(img).text((x, y), s, font=fnt, fill=color)


def small_corner_label(img, line, fnt, x=80, y=None):
    if y is None: y = H - 100
    d = ImageDraw.Draw(img)
    l, t, r, b = measure(d, line, fnt)
    text_with_halo(img, x - l, y - t, line, fnt, color=SUBTLE, halo=NEAR_BLACK, off=2)


def shot1_exterior() -> Path:
    """Sign on the door panel + faint scene tag."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Tracked-caps "HONEST GREENS" placed roughly where the AI's blank sign panel
    # is most likely (upper-centre area above the doors). Letter-spaced like a
    # restaurant sign. Two-tone: subtle warm white over a deep-green underplate
    # (the real sign panel will already be deep forest green).
    sign = "H O N E S T   G R E E N S"
    sign_f = f_inter("bold", 48)
    l, t, r, b = measure(d, sign, sign_f)
    sw = r - l
    text_with_halo(img, (W - sw) // 2 - l, 200 - t, sign, sign_f,
                   color=(245, 240, 230, 250), halo=NEAR_BLACK, off=2, halo_alpha=200)

    # Tiny scene-tag bottom-left, like editorial film slate
    tag_f = f_inter("medium", 22)
    small_corner_label(img, "01 — THE ROOM", tag_f, x=80, y=H - 80)

    out = OUT / "01.png"
    img.save(out)
    return out


def shot2_chef() -> Path:
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    tag_f = f_inter("medium", 22)
    small_corner_label(img, "02 — THE HANDS", tag_f, x=80, y=H - 80)
    out = OUT / "02.png"
    img.save(out)
    return out


def shot3_dining() -> Path:
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    tag_f = f_inter("medium", 22)
    small_corner_label(img, "03 — THE GUESTS", tag_f, x=80, y=H - 80)
    out = OUT / "03.png"
    img.save(out)
    return out


def shot4_hero_dish() -> Path:
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    tag_f = f_inter("medium", 22)
    small_corner_label(img, "04 — THE PLATE", tag_f, x=80, y=H - 80)
    out = OUT / "04.png"
    img.save(out)
    return out


def shot5_brand_card() -> Path:
    """Full editorial brand reveal — Playfair Display + Inter."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Eyebrow
    eyebrow = "C H E F   D R I V E N   ·   R E A L   F O O D"
    eb_f = f_inter("medium", 22)
    le, te, re_, be = measure(d, eyebrow, eb_f)
    text_with_halo(img, (W - (re_ - le)) // 2 - le, 280 - te, eyebrow, eb_f,
                   color=GOLD, halo=NEAR_BLACK, off=1, halo_alpha=120)

    # Big editorial wordmark
    title = "Honest Greens"
    title_f = f_playfair_bold(150)
    lt, tt, rt, bt = measure(d, title, title_f)
    title_w, title_h = rt - lt, bt - tt
    title_y = 320
    text_with_halo(img, (W - title_w) // 2 - lt, title_y - tt, title, title_f,
                   color=(248, 244, 234, 255), halo=NEAR_BLACK, off=2, halo_alpha=140)

    # Italic tagline
    tag = "Real food, served real."
    tag_f = f_playfair_italic(46)
    lg, tg, rg, bg = measure(d, tag, tag_f)
    text_with_halo(img, (W - (rg - lg)) // 2 - lg, title_y + title_h + 40 - tg,
                   tag, tag_f, color=(238, 230, 215, 240), halo=NEAR_BLACK, off=1, halo_alpha=120)

    # Thin gold rule
    rule_y = title_y + title_h + 40 + (bg - tg) + 40
    rule_w = 240
    d.rectangle(((W - rule_w) // 2, rule_y, (W + rule_w) // 2, rule_y + 2), fill=GOLD)

    # Now serving / cities line
    cities = "MADRID  ·  BARCELONA  ·  LISBON  ·  PARIS"
    city_f = f_inter("medium", 26)
    lc, tc, rc, bc = measure(d, cities, city_f)
    text_with_halo(img, (W - (rc - lc)) // 2 - lc, rule_y + 30 - tc, cities, city_f,
                   color=(228, 218, 200, 230), halo=NEAR_BLACK, off=1, halo_alpha=120)

    # Handle + URL stacked
    handle_f = f_inter("medium", 22)
    handle = "@HONESTGREENS   ·   HONESTGREENS.COM"
    lh, th_, rh, bh = measure(d, handle, handle_f)
    text_with_halo(img, (W - (rh - lh)) // 2 - lh, rule_y + 80 - th_, handle, handle_f,
                   color=(220, 210, 192, 220), halo=NEAR_BLACK, off=1, halo_alpha=120)

    # Soft footer (tiny)
    foot = "n o   a d d i t i v e s   ·   n o   p r e s e r v a t i v e s   ·   n o   r e f i n e d   s u g a r s"
    foot_f = f_inter("regular", 18)
    lf, tf, rf, bf = measure(d, foot, foot_f)
    text_with_halo(img, (W - (rf - lf)) // 2 - lf, H - 90 - tf, foot, foot_f,
                   color=(195, 188, 170, 200), halo=NEAR_BLACK, off=1, halo_alpha=110)

    out = OUT / "05.png"
    img.save(out)
    return out


def main():
    for p in (shot1_exterior(), shot2_chef(), shot3_dining(), shot4_hero_dish(), shot5_brand_card()):
        print(f"  ✓ {p}  {p.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
