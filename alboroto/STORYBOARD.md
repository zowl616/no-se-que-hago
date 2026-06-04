# Alboroto Restaurant — Launch Spot (15s, 16:9)

A catchy, hooky launch-marketing video for [alborotorestaurant.es](https://alborotorestaurant.es) — Bilbao restaurant at Poza 45 with **+100 dishes** (pizzas, wraps, sushi, sándwiches). Tagline: **"Pedir sin miedo, disfrutar sin normas."**

Built end-to-end through `@higgsfield/cli`, **using the actual photos and brand colours from the site** as the visual anchors. No invented food, no invented logo.

## Brief

- **Duration:** 15.000s (3 shots × 5.000s, hard-cut)
- **Format:** 16:9, 1920×1080, 30 fps, H.264 yuv420p, faststart — drops directly into an X / Instagram / Reels / TikTok-landscape post
- **Palette:** warm amber gold `#ebb01f` (the site's `theme-color`) + cream-white `#FAF6EE` + jet black, with subtle paper grain
- **Tone:** appetite-driving, hooky restaurant-brand, hyperkinetic editorial typography

## Shot list

| # | Beat | Source | Anchor copy | Motion |
|---|---|---|---|---|
| 1 | **Hooky Food Hero** (5s) | Their actual `alboroto-home.jpg` (1920×1080) used directly as start frame | "PEDIR SIN MIEDO" / "DISFRUTAR SIN NORMAS" | Slow cinematic 1.10× push-in on the dishes, steam rising, oils glistening, soft light wisps; bold Spanish typography whip-snaps in with amber underline streaks |
| 2 | **Variety Collage** (5s) | nano_banana_2 composite of their three square food photos (`alboroto-home-02.jpg`, `-03.jpg`, `-05.jpg`) into a 16:9 editorial layout | "+100 PLATOS" / "PIZZAS · WRAPS · SUSHI · SÁNDWICHES" / "para compartir." | Stamp-in cards with rubberband overshoot, amber keylines whip-extend, headline kerning bounce, type-writer subline, gentle 1.05× push-in on the hero card |
| 3 | **End Card / CTA** (5s) | nano_banana_2 layout using their actual `alboroto-log-retina.png` logo | Logo / "PEDIR SIN MIEDO, DISFRUTAR SIN NORMAS" / **"RESERVA YA"** / "POZA 45 · BILBAO" / "+34 944 97 87 43" / "alborotorestaurant.es" | Logo rubberband-snap, tagline type-in with amber underline whip, "RESERVA YA" stamp-in, contact lines cascade-fade |

## Production pipeline

```
alboroto/source_photos/                 nano_banana_2 (Nano Banana Pro)        seedance_2_0 / kling3_0          ffmpeg
─────────────────────────              ───────────────────────────────         ─────────────────────────         ──────
alboroto-home.jpg ────────────────────────────────────────────────── start-image ─→ Shot 1 (seedance 5s 1080p) ─┐
alboroto-home-02.jpg + -03 + -05  ─→ stills/02.png ────────────────── start-image ─→ Shot 2 (seedance 5s 1080p) ─┼─ concat → 15.000s master
alboroto-log-retina.png           ─→ stills/03.png ────────────────── start-image ─→ Shot 3 (kling3_0 5s)*      ─┘
                                                                                                                 │
                                                                                                                 ├─ alboroto_launch_15s_1080p_silent.mp4   (recommended)
                                                                                                                 ├─ alboroto_launch_15s_1080p_audio.mp4
                                                                                                                 ├─ poster.jpg + contact_sheet.jpg
```

*Shot 3 was originally rendered with `seedance_2_0` and got a false-positive NSFW flag (the system flagged the typographic end-card composition for unrelated reasons). The same start image was re-rendered through `kling3_0` and passed cleanly. Visually equivalent end-card animation; transparent here for traceability.*

## Deliverables

| Path | Notes |
|---|---|
| `alboroto/final/alboroto_launch_15s_1080p_silent.mp4` | **Primary cut** — silent, ~10.4 MB. Recommended for X / Instagram autoplay where copy lives in the post body. |
| `alboroto/final/alboroto_launch_15s_1080p_audio.mp4` | Same cut with the AI-generated ambient audio bed retained, ~9.4 MB. |
| `alboroto/final/poster.jpg` | 1920×1080 poster frame (`t = 1.2s`). Useful as the X card image / link preview. |
| `alboroto/final/contact_sheet.jpg` | 5×3 contact sheet of the master cut for review. |
| `alboroto/source_photos/*` | Original photos and logo downloaded from `alborotorestaurant.es`. |
| `alboroto/stills/02.png … 03.png` | nano_banana_2 composites used as start frames for shots 2 and 3. |
| `alboroto/clips/01.mp4 … 03.mp4` | Original Seedance/Kling 5s shot files (untrimmed). |
| `alboroto/prompts/*.txt` | Full prompt log — every still and video prompt, ready to tweak and re-run. |

## Cost

| Step | Model | Mode | Unit | Count | Subtotal |
|---|---|---|---|---|---|
| Stills | `nano_banana_2` | 16:9 2k, with `input_images` | 2 cr | 2 | 4 cr |
| Shot 1 | `seedance_2_0` | std 1080p 5s | 45 cr | 1 | 45 cr |
| Shot 2 | `seedance_2_0` | std 1080p 5s | 45 cr | 1 | 45 cr |
| Shot 3 (retry) | `kling3_0` | std 5s | 10 cr | 1 | 10 cr |
| Shot 3 (initial, NSFW false-positive) | `seedance_2_0` | std 1080p 5s | — | 1 | 0 cr (not charged) |
| **Total** | | | | | **≈ 104 cr** |

(Credit balance after this run: **6572.38** / 6675.13 starting → ~103 cr drawn.)

## How to iterate

```bash
# Re-render any shot from a tweaked prompt
$EDITOR alboroto/prompts/02_variety_video.txt
higgsfield generate create seedance_2_0 \
  --prompt "$(cat alboroto/prompts/02_variety_video.txt)" \
  --aspect_ratio 16:9 --duration 5 --resolution 1080p --mode std \
  --start-image alboroto/stills/02.png --wait

# Re-stitch the master after any clip change
ffmpeg -y \
  -i alboroto/clips/01.mp4 -i alboroto/clips/02.mp4 -i alboroto/clips/03.mp4 \
  -filter_complex "[0:v]fps=30,scale=1920:1080:flags=lanczos:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=0xFAF6EE,setsar=1,format=yuv420p[v0]; \
                   [1:v]fps=30,scale=1920:1080:flags=lanczos:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=0xFAF6EE,setsar=1,format=yuv420p[v1]; \
                   [2:v]fps=30,scale=1920:1080:flags=lanczos:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=0xFAF6EE,setsar=1,format=yuv420p[v2]; \
                   [v0][v1][v2]concat=n=3:v=1:a=0[outv]" \
  -map "[outv]" -an -t 15 \
  -c:v libx264 -preset slow -crf 17 -movflags +faststart -pix_fmt yuv420p \
  alboroto/final/alboroto_launch_15s_1080p_silent.mp4
```

## Suggested launch caption

> Alboroto. **Pedir sin miedo, disfrutar sin normas.**
>
> +100 platos para compartir. Pizzas, wraps, sushi, sándwiches.
>
> Poza 45, Bilbao · Reserva ya → alborotorestaurant.es
