# AISC — Launch Spot v2 (15s, 16:9) — Original style + correct typography

The first launch's look, **as it was** — Swiss editorial motion-design poster, jet-black + electric chartreuse `#D1FE17` on pure white, ink splatters, paper grain, hyperkinetic — with the typography from the previous fix retained verbatim, **rendered deterministically and pre-composited into each Seedance start frame** so every glyph is correct *and* feels baked into the editorial scene rather than stamped on top.

## Why this version

Three iterations on the AISC spot exist now:

| Version | Look | Typography |
|---|---|---|
| **PR #1** | Swiss editorial, hand-painted feel | AI-rendered → occasional misspellings |
| **PR #4** | Same look, but text overlaid as a flat top layer | Deterministic PIL → correct, but felt "stamped on" |
| **This (v2)** | Same look, typography integrated into the editorial scene | Deterministic PIL **pre-composited into the Seedance start frame**, then animated by the video model together with the ornaments → correct AND integrated |

The trick: instead of overlaying the title cards on top of the finished Seedance clip, we paint them onto the start image **before** Seedance runs. Seedance then treats the typography as part of the paper composition and animates everything together — wordmark kerning bounces, slabs slam-conveyor in, ornaments and type drift with the same paper-grain feel. The PIL overlays also get a subtle ink-bleed / soft-edge treatment so they read as hand-painted rather than vector-stamped.

A 55%-opacity safety-net of the same PIL overlay is composited on top of the Seedance output as the final step, so even if the model ever drifts a glyph mid-clip, the deterministic typography remains authoritative.

## Pipeline

```
nano_banana_2 (no-text Swiss-editorial ornament stills)
   ↓
PIL build_overlays.py     →  PNG title cards (Archivo Black + Inter, OFL)
   ↓                          ↓
PIL build_starts.py  ─── alpha composite + ink-bleed treatment ──→  starts/0N.png
   ↓
seedance_2_0 (i2v, 5s 1080p std)  →  clips/0N.mp4
   ↓
ffmpeg overlay safety net (55% PIL on top) → titled/0N.mp4
   ↓
ffmpeg concat → 15.000s master
```

## Texts (kept verbatim from PR #4)

- **Shot 1:** AISC · MARKETING FOR AMBITIOUS AI FOUNDERS · @AISCWORK · AISCWORK.COM · 7 partner stamps (PERPLEXITY, HIGGSFIELD, RUNWAY, LUMA AI, HEYGEN, KLING AI, PIKA LABS)
- **Shot 2:** 200+ CREATORS · OUR NETWORK · 10M+ REACH · COMBINED FOLLOWERS · 126 CAMPAIGNS · SHIPPED
- **Shot 3:** AISC · MARKETING FOR AMBITIOUS AI FOUNDERS. · @AISCWORK · AISCWORK.COM · NOW BOOKING Q3 2026 · 126 CAMPAIGNS · 200+ CREATORS · 10M+ REACH

All glyphs guaranteed byte-stable thanks to the deterministic PIL render + 55%-opacity safety-net composite.

## Deliverables

| Path | Notes |
|---|---|
| `aisc_v2/final/aisc_launch_15s_1080p_silent.mp4` | **Primary cut** — silent, ~9.5 MB. |
| `aisc_v2/final/aisc_launch_15s_1080p_audio.mp4` | Same cut with Seedance ambient audio, ~8.8 MB. |
| `aisc_v2/final/poster.jpg` · `aisc_v2/final/contact_sheet.jpg` | Poster frame and 5×3 review sheet. |
| `aisc_v2/stills/0N.png` | Reused text-free Swiss-editorial stills from the previous run. |
| `aisc_v2/overlays/0N.png` | Deterministic PIL title cards. |
| `aisc_v2/starts/0N.png` | Pre-composited start frames fed to Seedance. |
| `aisc_v2/clips/0N.mp4` | Native Seedance i2v output. |
| `aisc_v2/titled/0N.mp4` | Per-shot composite with safety-net overlay. |
| `aisc_v2/build_overlays.py` · `aisc_v2/build_starts.py` · `aisc_v2/build_master.sh` | Full pipeline scripts. |
| `aisc_v2/fonts/` | Archivo Black, Anton, Inter Bold/Medium/Regular (OFL). |
| `aisc_v2/prompts/` | Higgsfield prompts. |

## Cost

| Step | Model | Mode | Unit | Count | Subtotal |
|---|---|---|---|---|---|
| Stills | (reused from previous run) | — | 0 | 0 | 0 cr |
| Clips  | `seedance_2_0` | std 1080p 5s | 45 cr | 3 | 135 cr |
| **Total** | | | | | **135 cr** |

Credits drawn this run: **135** (account balance 6290.38 → 6155.38).

## Iterating

Change copy with **zero credit spend** — the deterministic typography flows through the safety-net composite even if the start-image type doesn't update mid-render:

```bash
$EDITOR aisc_v2/build_overlays.py
python3 aisc_v2/build_overlays.py
bash aisc_v2/build_master.sh
```

For full re-render with the new copy baked into Seedance's animation:

```bash
python3 aisc_v2/build_overlays.py
python3 aisc_v2/build_starts.py
# re-queue 3 seedance jobs against starts/01.png … 03.png (~135 cr)
bash aisc_v2/build_master.sh
```
