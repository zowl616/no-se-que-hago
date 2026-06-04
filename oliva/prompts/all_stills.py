"""All 10 still prompts in one place — keep DRY."""

COMMON_STYLE_FOOTER = """
GLOBAL STYLE: Ultra-photorealistic cinematic frame, shot as if on Sony FX3 with Cooke S4 primes, shallow depth of field, slight Kodak Vision3 500T film grain, warm cinematic colour grade (crushed blacks, lifted warm highlights, slightly desaturated mid-tones, never oversaturated). Single warm key light from upper-right at ~3200K, soft fill from below, faint atmospheric haze for depth. Palette: warm terracotta, olive green, deep saffron, charred-black cast iron, golden olive oil, rustic wood. Subtle anamorphic horizontal lens flare allowed. Real-looking food (no plastic AI sheen, believable textures). Believable hands (anatomically correct, five fingers, natural grip). No floating ingredients. No duplicated objects. NO TEXT ANYWHERE — do not render any letters, numbers, words, glyphs, captions, watermarks, brand wordmarks, or typography of any kind anywhere in the image. Treat any place where text might go as featureless solid colour.
"""

PROMPTS = {
    "01_knife_slam": """[Image — Scene 1 — Cold Open Knife Slam, 16:9, NO TEXT]

A stark hyper-tight 50mm-equivalent close-up of a polished chef's knife frozen mid-impact, blade-down into a thick olive-wood cutting board. The blade has just made contact with the surface. A frozen halo of pale flour and coarse sea-salt dust explodes radially around the blade in mid-air, suspended like a tiny shockwave. Tiny wood splinters arc outward from the impact point. The wooden chef's-knife handle is held in a believable bare hand entering the frame from the upper-right, anatomically correct (five fingers, natural firm grip). Deep walnut wood grain texture beneath, charred edges where it has been used. Background: deep moody charcoal black wood with strong directional warm key light from upper-right carving the blade with a hot specular highlight and casting a long shadow toward the lower-left.
""" + COMMON_STYLE_FOOTER,

    "02_tomato_slice": """[Image — Scene 2 — Macro Tomato Slice, 16:9, NO TEXT]

Extreme 100mm-macro slow-motion still of a ripe deep-red Mediterranean tomato being sliced cleanly in half by a polished chef's knife. The blade is mid-cut through the centre of the tomato. A halo of bright crimson juice droplets and a few amber tomato seeds is suspended mid-air around the cut, frozen mid-flight. The tomato's two halves are starting to separate, glistening flesh visible inside. The blade's hot specular highlight is razor-sharp. Razor-shallow depth of field, the front of the tomato in tack focus, the rest of the cutting board falling soft. Warm side-light from upper-right.
""" + COMMON_STYLE_FOOTER,

    "03_pan_ignite": """[Image — Scene 3 — Cast-Iron Pan Ignition, 16:9, NO TEXT]

A 35mm-equivalent slight downward-angle still of a black charred cast-iron pan on an open flame, mid-ignition. A controlled bright orange flame burst is rising from the pan in a frozen plume. Three plump garlic cloves and two sprigs of fresh rosemary are mid-fall just above the shimmering golden olive oil pool inside the pan, suspended mid-air with tiny droplets of oil splashing upward to greet them. The oil surface shimmers with a hot wave pattern and starting bubbles. Steam and a slight smoke curl rise from the pan, catching the warm key light from upper-right. Background: deep charcoal blur with warm flame glow.
""" + COMMON_STYLE_FOOTER,

    "04_oil_pour": """[Image — Scene 4 — Olive Oil Pour, 16:9, NO TEXT]

Extreme slow-motion still of golden extra-virgin olive oil pouring in a continuous, perfect amber ribbon from a small clear glass bottle held high in the upper-left of the frame, descending diagonally toward the hot cast-iron pan in the lower-right. The oil ribbon glows amber, lit dramatically from BEHIND so it is luminous translucent gold. A few small detached droplets are suspended along the ribbon. The pan in the lower-right glints with hot oil already inside. The bottle is gripped in a believable bare hand entering the upper-left of the frame (anatomically correct). Background: deep charcoal moody, faint atmospheric haze.
""" + COMMON_STYLE_FOOTER,

    "05a_overhead_plate": """[Image — Scene 5a — Top-Down Plate Placement, 16:9, NO TEXT]

A perfectly top-down (90° overhead) macro still of a bare hand entering the frame from the lower-right, mid-motion gently placing a small SIGNATURE TAPA — a freshly cooked, glistening hero plate of charred Mediterranean prawns over romesco sauce, garnished with fresh parsley and a wedge of charred lemon — onto a warm terracotta-orange ceramic plate (#C66C3A tone). The plate sits on a deep walnut wood table. The hand is anatomically correct (five fingers, natural grip), with a hint of a clean cream apron sleeve at the wrist. Steam curls upward visibly. Warm key light from upper-right.
""" + COMMON_STYLE_FOOTER,

    "05b_45_plate": """[Image — Scene 5b — 45° Plate Side Angle, 16:9, NO TEXT]

A 45° side-front angle still of the same hero tapa already placed on its warm terracotta ceramic plate, framed in the lower-third of the composition with generous warm negative space above. The dish is the charred Mediterranean prawns over romesco with parsley and charred lemon. Glistening sauce sheen, deep grill marks, fresh herb flecks. Steam curling upward. Deep walnut wood table beneath. Warm tungsten key light from upper-right sculpting the textures with deep shadows. Soft warm bokeh in the background.
""" + COMMON_STYLE_FOOTER,

    "05c_macro_texture": """[Image — Scene 5c — Macro Plate Texture, 16:9, NO TEXT]

Extreme 100mm-macro close-up of the surface texture of the hero tapa — charred prawn shell with dark grill marks, vivid red romesco sauce glaze pooling underneath, tiny flakes of sea salt, fresh parsley flecks, herb-oil droplets glistening. Razor-shallow depth of field — only a small slice of the plate is in tack focus. Warm side light raking across the textures from upper-right, bringing out every grain.
""" + COMMON_STYLE_FOOTER,

    "06_garnish_drop": """[Image — Scene 6 — Garnish Drop Slow-Mo, 16:9, NO TEXT]

Extreme 100mm-macro slow-motion still: a frozen vertical cascade of garnish elements falling onto the hero tapa from the upper portion of the frame. Several capers, large flakes of sea salt, and a few fresh parsley leaves are suspended mid-fall, with a couple of capers just bouncing off the dish surface, sending tiny droplets of romesco upward. A faint dusting of olive-oil mist drifts through warm light beams. Razor-shallow depth of field, the falling garnish in tack focus mid-frame, the dish soft below.
""" + COMMON_STYLE_FOOTER,

    "07_sauce_hit": """[Image — Scene 7 — Sauce Drizzle, 16:9, NO TEXT]

A 45° side-mid-shot still of a confident bare hand drizzling a deep crimson-red romesco sauce from a small ceramic spoon across the hero tapa in one swooping motion. The sauce mid-air is a continuous arcing red ribbon with a few droplets visibly splashing free. The plate is in the lower third of the frame, the spoon and hand entering from the upper-right. The hand is anatomically correct. Warm tungsten key light from upper-right, deep shadows on the walnut wood beneath.
""" + COMMON_STYLE_FOOTER,

    "08_hero_rotation": """[Image — Scene 8 — Hero Plate, 16:9, NO TEXT]

A premium editorial 85mm-equivalent hero shot at a low 25° angle of the finished signature tapa on its warm terracotta ceramic plate. Steam visibly rising, dramatic side-rim lighting from the upper-right sculpting every texture (charred prawns, glistening romesco sauce, parsley flakes, charred lemon wedge). The plate is centred on a deep walnut wood table. Razor-shallow depth of field, soft warm bokeh in the background, anamorphic horizontal lens flare across the upper third. A small sprig of rosemary and a tiny ramekin of olive oil sit casually beside the plate. Reserve a clean lower-right corner where a small logo will be composited later.
""" + COMMON_STYLE_FOOTER,
}

if __name__ == "__main__":
    from pathlib import Path
    out_dir = Path(__file__).parent
    for name, prompt in PROMPTS.items():
        (out_dir / f"{name}_still.txt").write_text(prompt)
        print(f"  ✓ {name}_still.txt")
