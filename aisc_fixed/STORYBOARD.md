# AISC — Launch Spot, Fixed Typography (15s, 16:9)

Same launch style and brief as the original [PR #1](https://github.com/zowl616/no-se-que-hago/pull/1) — **stark white motion-design, jet-black + electric chartreuse `#D1FE17`, ink splatters, paper grain, hyperkinetic typography** — re-rendered with the typography fix from the pixel-game pass: **every word is rendered deterministically, zero misspellings.**

- **Duration:** 15.000s (3 shots × 5.000s, hard cut)
- **Format:** 16:9, 1920×1080, 30 fps, H.264 yuv420p, faststart
- **Type:** Archivo Black (oversized headlines) + Inter Bold/Medium/Regular (tagline, contact, foot) — Google Fonts OFL, rasterised by PIL, composited via ffmpeg overlay
- **Look:** identical to the original launch spot — Swiss editorial motion-design poster on pure white

## What changed vs. the original

| | Original PR #1 | This PR |
|---|---|---|
| Visual style | Stark white motion design with jet black + chartreuse | **Same** |
| Brief & metrics | 200+ creators / 10M+ reach / 126 campaigns / Now booking Q3 2026 | **Same** |
| Duration / format | 15s, 16:9, 1080p | **Same** |
| Pipeline for ornaments | `nano_banana_2` → `seedance_2_0` | **Same** |
| Pipeline for typography | AI rendered all text → occasional glyph drift | **PIL with real fonts → byte-stable** |

The AI is now asked to produce *only* the ink splatters, motion-blur trails, chartreuse accent bars, sharpie arrow, and abstract corner ornaments — every prompt explicitly forbids text, letters, numbers, words, glyphs, or partial letterforms. PIL handles all typography on top.

## Pipeline

```
nano_banana_2 (no-text Swiss-editorial ornaments)
   ↓
seedance_2_0 (5s 1080p std image-to-video)
   ↓
PIL build_overlays.py (Archivo Black + Inter, 1920×1080 transparent PNG title cards)
   ↓
ffmpeg overlay (0.4–0.6s alpha fade-in per shot)
   ↓
ffmpeg concat → 15.000s master
```

## Shot list

| # | Beat | AI ornaments | Typography overlay |
|---|---|---|---|
| 1 | **Wordmark Ignition** (5s) | Black ink-splatter explosion, abstract ink-stamp shapes whip in/out of corners with motion-blur, chartreuse spark dots | "AISC" (Archivo Black 360pt) / "MARKETING FOR AMBITIOUS AI FOUNDERS" / "@AISCWORK · AISCWORK.COM" / 7 partner-brand stamps (PERPLEXITY, HIGGSFIELD, RUNWAY, LUMA AI, HEYGEN, KLING AI, PIKA LABS) tilted around the corners |
| 2 | **Stat Slabs** (5s) | Two horizontal chartreuse accent bars whip-extend in the gutters; corner speckles drift; subtle parallax tilt | "200+ CREATORS" / "10M+ REACH" / "126 CAMPAIGNS" with chartreuse underline + label sub-line |
| 3 | **End Card** (5s) | Hand-drawn black sharpie arrow draws into a checkmark on the left half; chartreuse highlight runs in parallel; corner speckles | "AISC" (large, right) / "MARKETING FOR AMBITIOUS AI FOUNDERS." / chartreuse bar / "@AISCWORK" / "AISCWORK.COM" / "NOW BOOKING Q3 2026" / foot stats line |

## Deliverables

| Path | Notes |
|---|---|
| `aisc_fixed/final/aisc_launch_15s_1080p_silent.mp4` | **Primary cut** — silent, ~8.2 MB. Recommended for X autoplay. |
| `aisc_fixed/final/aisc_launch_15s_1080p_audio.mp4` | Same cut with Seedance ambient audio retained, ~7.7 MB. |
| `aisc_fixed/final/poster.jpg` | 1920×1080 poster frame. |
| `aisc_fixed/final/contact_sheet.jpg` | 5×3 contact sheet. |
| `aisc_fixed/stills/01-03.png` | Source `nano_banana_2` no-text Swiss-editorial stills. |
| `aisc_fixed/clips/01-03.mp4` | Untrimmed Seedance 2.0 5s clips (no text). |
| `aisc_fixed/titled/01-03.mp4` | Per-shot composites with deterministic overlay applied. |
| `aisc_fixed/overlays/01-03.png` | Transparent 1920×1080 PIL title cards. |
| `aisc_fixed/build_overlays.py` | PIL script — edit strings, sizes, positions here. |
| `aisc_fixed/build_master.sh` | ffmpeg pipeline — composite + concat. |
| `aisc_fixed/fonts/` | Archivo Black, Anton, Inter Bold/Medium/Regular (OFL). |
| `aisc_fixed/prompts/` | Higgsfield prompts (no-text constraint baked in). |

## Cost

| Step | Model | Mode | Unit | Count | Subtotal |
|---|---|---|---|---|---|
| Stills | `nano_banana_2` | 16:9 2k | 2 cr | 3 | 6 cr |
| Clips  | `seedance_2_0`  | std 1080p 5s | 45 cr | 3 | 135 cr |
| **Total** | | | | | **141 cr** |

Credits drawn: **141** (account balance 6431.38 → 6290.38).

## Iterating

Change copy with **zero credit spend**:

```bash
$EDITOR aisc_fixed/build_overlays.py
python3 aisc_fixed/build_overlays.py
bash aisc_fixed/build_master.sh
```

Re-render an ornament shot:

```bash
$EDITOR aisc_fixed/prompts/02_stat_slabs_video.txt
higgsfield generate create seedance_2_0 \
  --prompt "$(cat aisc_fixed/prompts/02_stat_slabs_video.txt)" \
  --aspect_ratio 16:9 --duration 5 --resolution 1080p --mode std \
  --start-image aisc_fixed/stills/02.png --wait
# replace aisc_fixed/clips/02.mp4 with the new download, then:
bash aisc_fixed/build_master.sh
```

## Suggested launch caption (X)

> AISC — Marketing for ambitious AI founders.
>
> 200+ creators · 10M+ reach · 126 campaigns shipped.
>
> Now booking Q3 2026 → aiscwork.com
