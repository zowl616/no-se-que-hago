"""Composite Scene 1's AISC sign onto the exterior still BEFORE Seedance so
the warming-light push-in scales the sign with the rest of the scene.
Other scenes feed their stills directly.
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
    return Image.merge("RGBA", (r, g, b, a_soft))


# Stills are 9:16 from nano_banana_2 — ~1664×2912 in 2k mode. We resize to 2160×3840 for 4K
TARGET = (2160, 3840)


def main():
    plain = ["02_beans_macro", "03_pour", "04_room"]
    name_map = {"02_beans_macro": "02", "03_pour": "03", "04_room": "04"}
    for n in plain:
        short = name_map[n]
        img = Image.open(STILLS / f"{short}.png").convert("RGB")
        if img.size != TARGET:
            img = img.resize(TARGET, Image.LANCZOS)
        img.save(OUT / f"{short}.png", format="PNG", optimize=True)
        print(f"  ✓ {OUT / (short + '.png')}")

    # Scene 1 — composite the sign overlay onto the exterior
    bg = Image.open(STILLS / "01.png").convert("RGBA")
    if bg.size != TARGET:
        bg = bg.resize(TARGET, Image.LANCZOS)
    fg = Image.open(OVERLAYS / "01_sign.png").convert("RGBA")
    if fg.size != TARGET:
        fg = fg.resize(TARGET, Image.LANCZOS)
    treated = hand_paint(fg)
    out = Image.alpha_composite(bg, treated).convert("RGB")
    out.save(OUT / "01.png", format="PNG", optimize=True)
    print(f"  ✓ {OUT / '01.png'} (with AISC sign composited)")


if __name__ == "__main__":
    main()
