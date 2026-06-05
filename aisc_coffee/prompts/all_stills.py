"""4 still prompts for the AISC coffee shop launch — vertical 9:16."""

COMMON_FOOTER = """
GLOBAL STYLE: Ultra-photorealistic cinematic still, vertical 9:16 framing, shot as if on Sony FX3 with Cooke S4 primes, shallow depth of field, slight Kodak Vision3 film grain (250D for daylight, 500T for interiors), warm cinematic colour grade — warm shadows, lifted golden highlights, slightly desaturated mid-tones, never oversaturated. Single warm key light (golden hour to soft morning), faint atmospheric haze for cinematic depth. Anamorphic horizontal lens flare allowed but extremely subtle. Real-looking food, real-looking beans, real-looking espresso, believable hands (anatomically correct, five fingers, natural grip, no warping), realistic skin tones. No floating ingredients, no duplicated objects. NO TEXT ANYWHERE — do not render any letters, numbers, words, glyphs, captions, watermarks, brand wordmarks, or typography of any kind anywhere in the image. Treat the brass sign panel and any other surface where text might go as featureless solid colour.
"""

PROMPTS = {
    "01_exterior": """[Image — Scene 1 — Cobblestone Madrid Exterior, 9:16 VERTICAL, NO TEXT]

Vertical 9:16 cinematic still, 35mm-equivalent slight low-angle three-quarter view of a quiet cobblestone street in central Madrid at pre-dawn / blue hour, the very first sliver of golden sunrise just beginning to break across the upper-third of the frame. Empty, peaceful, no people on the street. The composition fills the vertical frame with the wooden shopfront door of a small specialty coffee shop, slightly off-centre, the door closed.

Above the wooden door, mounted on the cream limestone facade, hangs a discreet rectangular BRASS SIGN PANEL (about a third the width of the door) — featureless polished brass, completely empty (no logo, no text, no marks of any kind on it). A small thin brass pendant lamp hangs nearby, unlit. The wooden door has dark walnut grain and a small brass handle.

Surrounding architectural detail typical of central Madrid: pale cream limestone walls with subtle vertical scoring, wrought-iron balconies with small potted geraniums on the upper edge of frame, polished cobblestones reflecting the soft pre-dawn blue, a hint of an old gas lamp glow at the far edge.

Cool blue-grey shadow tones dominate the scene with the very first warm gold sunrise touch on the upper edge of the brass sign and the top of the door — the moment before full sunrise. Subtle atmospheric haze for cinematic depth.
""" + COMMON_FOOTER,

    "02_beans_macro": """[Image — Scene 2 — Espresso Beans Cascade Macro, 9:16 VERTICAL, NO TEXT]

Vertical 9:16 extreme macro slow-motion still, 100mm macro at f/2.8. The frame is filled with freshly roasted espresso beans cascading from a clear glass canister (visible at the top of the frame, tilted) into the dark walnut hopper of a polished brass grinder (visible in soft focus at the bottom of the frame). The beans are caught mid-fall, suspended in the centre of the frame — each bean has visible oil sheen, deep mahogany-brown colour, a few droplets of warm tungsten light catching their curves. Some beans bouncing softly off the rim of the hopper.

Razor-shallow depth of field — only a small slice of beans is in tack focus, the canister and hopper dissolving into warm honey bokeh. Hands of a barista visible at the very edge of the upper frame, a clean linen shirt sleeve cuffed at the wrist gripping the canister, anatomically correct (five fingers, natural grip).

Background: warm walnut wood and brass blurred into bokeh, a single warm tungsten side-light from the upper-right sculpting the beans with deep shadows. Mood: ceremonial, careful, like watching tea being prepared in a Kyoto room.
""" + COMMON_FOOTER,

    "03_pour": """[Image — Scene 3 — Espresso Pour Macro, 9:16 VERTICAL, NO TEXT]

Vertical 9:16 cinematic still, 50mm at f/2.0, shallow depth of field. The frame is dominated by the close-up of a barista's bare hands (visible from elbow down, wrists prominent, NO face visible — the framing is below the face line) operating a polished brass espresso machine. The portafilter is locked in, and a steady golden stream of espresso is pulling into a small white ceramic cup positioned on a brass weighing scale. Crema is forming on the surface in golden ribbons, swirling visibly. Soft visible columns of steam rise from the cup, catching the warm side light from the upper-right.

The brass espresso machine fills the upper third of the frame with polished metal catching warm specular highlights. The barista wears a clean cream linen shirt cuffed at the wrists, anatomically correct hands (five fingers, natural firm grip on the machine).

Background slightly out of focus: dark walnut wooden shelves with a few amber-glass bottles, a brass weighing scale visible just behind the cup, a small terracotta pot with eucalyptus springs softly silhouetted. Single-source warm tungsten light from upper-right, deeply tactile, deeply intentional.
""" + COMMON_FOOTER,

    "04_room": """[Image — Scene 4 — Coffee Shop Interior, 9:16 VERTICAL, NO TEXT]

Vertical 9:16 cinematic still, 35mm at f/2.0, gimbal-stabilised wide interior of a small specialty coffee shop in central Madrid in soft late-morning golden light. About 30 square metres, intimate and neighborhood-scale.

Compose for the vertical frame: at the centre-right, a long warm dark-walnut bar with a polished brass espresso machine taking pride of place. Behind it, dark walnut wooden shelves with a few clear glass canisters of beans, amber-glass syrup bottles, and a small brass weighing scale. To the left of the bar, two empty wooden bar stools with woven seats. Beneath them, terracotta floor tiles in a warm earthy red.

To the foreground left, a small wooden side table with an open laptop (closed enough that no screen is visible) and a glass-domed pastry stand with two fresh pastries inside (a croissant and a small crusty buttery loaf). A small ceramic vase with a sprig of fresh eucalyptus or olive branches sits beside the pastries. Above the table, a small cluster of green hanging plants softens the upper-left corner.

Large iron-framed windows on the right side of the frame let warm late-morning sunlight pool on the terracotta floor. Subtle atmospheric haze in the air, a hint of steam visible in the warm light beam. The aesthetic is Aesop store meets Madrid neighborhood café — refined, lived-in, NOT industrial, NOT Starbucks. No people in the frame.
""" + COMMON_FOOTER,
}

if __name__ == "__main__":
    from pathlib import Path
    out_dir = Path(__file__).parent
    for name, prompt in PROMPTS.items():
        (out_dir / f"{name}_still.txt").write_text(prompt)
        print(f"  ✓ {name}_still.txt")
