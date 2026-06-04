"""Composite Scene 8 corner-logo overlay onto its still BEFORE Seedance so the
logo participates in the rotation. Other scenes feed their stills directly.
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
    return softened


def main():
    # Scenes 1, 2, 3, 4, 5a, 5b, 5c, 6, 7 → just copy still as start image (no overlay)
    plain = ["01", "02", "03", "04", "05a", "05b", "05c", "06", "07"]
    for n in plain:
        img = Image.open(STILLS / f"{n}.png").convert("RGB")
        if img.size != (1920, 1080):
            img = img.resize((1920, 1080), Image.LANCZOS)
        img.save(OUT / f"{n}.png", format="PNG", optimize=True)
        print(f"  ✓ {OUT / (n + '.png')}")

    # Scene 8 → composite the corner logo onto the still
    bg = Image.open(STILLS / "08.png").convert("RGBA")
    if bg.size != (1920, 1080):
        bg = bg.resize((1920, 1080), Image.LANCZOS)
    fg = Image.open(OVERLAYS / "08.png").convert("RGBA")
    if fg.size != (1920, 1080):
        fg = fg.resize((1920, 1080), Image.LANCZOS)
    treated = hand_paint(fg)
    out = Image.alpha_composite(bg, treated).convert("RGB")
    out.save(OUT / "08.png", format="PNG", optimize=True)
    print(f"  ✓ {OUT / '08.png'} (with logo composited)")


if __name__ == "__main__":
    main()
