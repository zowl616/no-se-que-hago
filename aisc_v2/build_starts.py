"""Composite deterministic typography PNGs onto the AI-generated text-free
ornament stills, with a light ink-bleed / hand-painted treatment so the type
feels baked into the editorial paper composition (not flat-stamped on top).

The composited result is then fed into Seedance 2.0 as `--start-image` so the
video model treats the entire frame — typography and ornaments together — as
one cohesive scene and applies motion to all of it.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageFilter, ImageOps

ROOT = Path(__file__).parent
STILLS = ROOT / "stills"
OVERLAYS = ROOT / "overlays"
OUT = ROOT / "starts"
OUT.mkdir(exist_ok=True)


def hand_paint(overlay: Image.Image) -> Image.Image:
    """Apply a subtle ink-bleed treatment so the type integrates with the paper background.

    Steps:
      1. Slight gaussian blur on the alpha (softens crisp vector edges).
      2. A faint dilated darker shadow underneath (simulates ink soaking into paper).
      3. Combine: shadow first, then the slightly-softened type on top.
    """
    if overlay.mode != "RGBA":
        overlay = overlay.convert("RGBA")
    r, g, b, a = overlay.split()

    # Soften edges
    a_soft = a.filter(ImageFilter.GaussianBlur(radius=1.0))
    softened = Image.merge("RGBA", (r, g, b, a_soft))

    # Dilated, darker shadow underneath (very subtle ink bleed)
    a_bleed = a.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(radius=2.0))
    shadow = Image.new("RGBA", overlay.size, (0, 0, 0, 0))
    shadow_color = Image.new("RGBA", overlay.size, (10, 10, 10, 80))
    shadow.paste(shadow_color, mask=a_bleed)

    out = Image.alpha_composite(shadow, softened)
    return out


def composite_one(still_path: Path, overlay_path: Path, out_path: Path) -> None:
    bg = Image.open(still_path).convert("RGBA")
    if bg.size != (1920, 1080):
        bg = bg.resize((1920, 1080), Image.LANCZOS)
    fg = Image.open(overlay_path).convert("RGBA")
    if fg.size != (1920, 1080):
        fg = fg.resize((1920, 1080), Image.LANCZOS)
    treated = hand_paint(fg)
    final = Image.alpha_composite(bg, treated).convert("RGB")
    final.save(out_path, format="PNG", optimize=True)


def main():
    for n in ("01", "02", "03"):
        composite_one(STILLS / f"{n}.png", OVERLAYS / f"{n}.png", OUT / f"{n}.png")
        print(f"  ✓ {OUT / (n + '.png')}")


if __name__ == "__main__":
    main()
