"""Composite typography overlays onto AI stills with subtle ink-bleed,
producing starts/0N.png to feed into Seedance.

Scene 1 gets the sign + slate baked in (so push-in scales the sign with the scene).
Scenes 2/3/4 get only the small slate tag baked in.
Scene 5 gets the full brand reveal baked in (motion model treats the typography
as part of the scene, deepening the editorial feel).
"""
from pathlib import Path
from PIL import Image, ImageFilter

ROOT = Path(__file__).parent
STILLS = ROOT / "stills"
OVERLAYS = ROOT / "overlays"
OUT = ROOT / "starts"
OUT.mkdir(exist_ok=True)


def hand_paint(overlay):
    if overlay.mode != "RGBA":
        overlay = overlay.convert("RGBA")
    r, g, b, a = overlay.split()
    a_soft = a.filter(ImageFilter.GaussianBlur(radius=0.7))
    softened = Image.merge("RGBA", (r, g, b, a_soft))
    a_bleed = a.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(radius=2.0))
    shadow = Image.new("RGBA", overlay.size, (0, 0, 0, 0))
    shadow_color = Image.new("RGBA", overlay.size, (0, 0, 0, 60))
    shadow.paste(shadow_color, mask=a_bleed)
    return Image.alpha_composite(shadow, softened)


def main():
    for n in ("01", "02", "03", "04", "05"):
        bg = Image.open(STILLS / f"{n}.png").convert("RGBA")
        if bg.size != (1920, 1080):
            bg = bg.resize((1920, 1080), Image.LANCZOS)
        fg = Image.open(OVERLAYS / f"{n}.png").convert("RGBA")
        if fg.size != (1920, 1080):
            fg = fg.resize((1920, 1080), Image.LANCZOS)
        treated = hand_paint(fg)
        out = Image.alpha_composite(bg, treated).convert("RGB")
        out.save(OUT / f"{n}.png", format="PNG", optimize=True)
        print(f"  ✓ {OUT / (n + '.png')}")


if __name__ == "__main__":
    main()
