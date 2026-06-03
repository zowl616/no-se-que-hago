# AISC — Launch Spot (15s, 16:9)

A polished launch-marketing video for [aiscwork.com](https://aiscwork.com) — "Marketing for ambitious AI founders." Built end-to-end through the [`@higgsfield/cli`](https://github.com/higgsfield-ai/cli) on top of `nano_banana_2` (Nano Banana Pro) for the hero stills and `seedance_2_0` (Seedance 2.0, std mode, 1080p) for image-to-video motion.

## Brief

- **Duration:** 15.000s (3 shots × 5.000s, hard-cut)
- **Format:** 16:9, 1920×1080, 30 fps, H.264 yuv420p, faststart — drops cleanly into an X post (well under the 2:20 / 512MB cap, well above the 32 kb/s minimum)
- **Look:** stark #FFFFFF white paper, jet-black ultra-bold typography, single electric chartreuse `#D1FE17` accent, subtle paper grain, hyperkinetic editorial motion design, no people, no photos
- **Voice:** confident, founder-grade, "the drop engine" — pulled directly from AISC's own positioning ("200+ creators · 10M+ reach · 126 campaigns shipped")

## Shot list

| # | Beat | Duration | Anchor copy | Motion |
|---|---|---|---|---|
| 1 | Wordmark Ignition | 5.0s | **AISC** / "Marketing for ambitious AI founders." | Ink-blot splatter on white → kerning whip-snap on the wordmark → stop-motion stamp cascade of partner-brand wordmarks (Perplexity, Higgsfield, Runway, Luma, HeyGen, Kling, Pika) → centrifugal dispersion with motion-blur trails |
| 2 | Stat Slabs | 5.0s | **200+ CREATORS** / **10M+ REACH** / **126 CAMPAIGNS SHIPPED** | Conveyor slam of three giant typographic rows, each with a bass-thud overshoot bounce, chartreuse underline whip-extends, ticker count-ups settle into the final values |
| 3 | Drop Engine — End Card | 5.0s | **AISC** / "Marketing for ambitious AI founders." / @aiscwork · aiscwork.com / "Now booking Q3 2026" | Sharpie-style arrow draws itself across the canvas into a checkmark → wordmark snaps in with rubberband overshoot → tagline types in below → contact lines fade up |

## Production pipeline

```
Higgsfield CLI (nano_banana_2)        Higgsfield CLI (seedance_2_0)         ffmpeg
─────────────────────────────         ────────────────────────────          ──────
prompts/01_wordmark_ignition.txt  →   assets/stills/01.png  ─┐
prompts/02_stat_slabs.txt         →   assets/stills/02.png  ─┼─ start-image →   3× 5.04s 1080p H.264 clips ──┐
prompts/03_end_card.txt           →   assets/stills/03.png  ─┘   prompts/*_video.txt                          │
                                                                                                              ▼
                                                                                                concat → 15.000s master
                                                                                                ├─ aisc_launch_15s_1080p_silent.mp4   (recommended)
                                                                                                ├─ aisc_launch_15s_1080p_audio.mp4    (Seedance ambient audio retained)
                                                                                                └─ poster.jpg + contact_sheet.jpg
```

## Deliverables

| Path | Notes |
|---|---|
| `assets/final/aisc_launch_15s_1080p_silent.mp4` | **Primary cut** — silent. Recommended for X/social where autoplay is muted by default and copy lives in the post body. ~6.8 MB. |
| `assets/final/aisc_launch_15s_1080p_audio.mp4` | Same cut with Seedance 2.0's auto-generated ambient audio kept (no music bed designed). ~6.2 MB. |
| `assets/final/poster.jpg` | 1920×1080 poster frame (t = 0.5s). Useful as the X card image / link preview. |
| `assets/final/contact_sheet.jpg` | 5×3 contact sheet of the master cut for review. |
| `assets/stills/01.png … 03.png` | Source 2k Nano Banana Pro stills (re-usable as standalone print/social posters). |
| `assets/clips/01.mp4 … 03.mp4` | Original Seedance 2.0 1080p shot files (untrimmed, in case you want to remix). |
| `prompts/*.txt` | Full prompt log — every still and video prompt, ready to tweak and re-run. |

## Cost

| Step | Model | Mode | Unit cost | Count | Total |
|---|---|---|---|---|---|
| Stills | `nano_banana_2` | 16:9, 2k | 2 cr | 3 | 6 cr |
| Clips  | `seedance_2_0`  | 16:9, 5s, 1080p, std | 45 cr | 3 | 135 cr |
| **Total** | | | | | **141 cr** |

(Credit balance after this run: 6675.13 / 6816.13 starting.)

## How to iterate

Any shot can be regenerated independently. To swap, e.g., the stat slabs:

```bash
# Tweak the still prompt
$EDITOR prompts/02_stat_slabs.txt

# Regenerate the still
higgsfield generate create nano_banana_2 \
  --prompt "$(cat prompts/02_stat_slabs.txt)" \
  --aspect_ratio 16:9 --resolution 2k --wait

# Regenerate the clip from the new still
higgsfield generate create seedance_2_0 \
  --prompt "$(cat prompts/02_stat_slabs_video.txt)" \
  --aspect_ratio 16:9 --duration 5 --resolution 1080p --mode std \
  --start-image assets/stills/02.png --wait

# Re-stitch the master
ffmpeg -y -f concat -safe 0 -i /tmp/concat.txt -an -t 15 \
  -vf "fps=30,scale=1920:1080:flags=lanczos,format=yuv420p" \
  -c:v libx264 -preset slow -crf 17 -movflags +faststart -pix_fmt yuv420p \
  assets/final/aisc_launch_15s_1080p_silent.mp4
```

## Suggested launch caption (X)

> AISC — Marketing for ambitious AI founders.
>
> 200+ creators. 10M+ reach. 126 campaigns shipped.
>
> Now booking Q3 2026 → aiscwork.com
