#!/usr/bin/env bash
# AISC Coffee — 15s vertical (1080×1920 → 4K 2160×3840) cinematic launch.
#
# 6 scenes chained with 0.4s smooth cross-dissolves (xfade=transition=fade)
# per the brief's "smooth motivated transitions" rule:
#
#   Scene 1 (0.0–2.5)   exterior dawn push-in
#   Scene 2 (2.5–5.5)   beans macro cascade
#   Scene 3 (5.5–8.5)   espresso pour
#   Scene 4 (8.5–11.5)  interior gimbal track
#   Scene 5 (11.5–13.5) tagline reveal (cream paper)
#   Scene 6 (13.5–15.0) brand card (deep amber, fades to warm black)
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p trimmed final

# Each AI clip needs +0.4s extra duration to feed the cross-dissolve at its trailing edge,
# and the next scene needs +0.4s extra at its leading edge — except the very first/last segments.
# Net visible per scene after dissolves:
#   1: 2.5  2: 3.0  3: 3.0  4: 3.0  5: 2.0  6: 1.5
# Source segment durations needed (with overlap):
#   1: 2.7  (2.5 visible + 0.2 trailing into dissolve)
#   2: 3.4  (0.2 leading + 3.0 + 0.2 trailing)
#   3: 3.4
#   4: 3.4
#   5: 2.4  (0.2 leading + 2.0 + 0.2 trailing)
#   6: 1.7  (0.2 leading + 1.5 visible)
# Total source: 2.7 + 3.4*3 + 2.4 + 1.7 = 17.0s
# After 5 cross-dissolves of 0.4s each: 17.0 - 5*0.4 = 15.0s ✓

# 4K vertical normalise: 2160x3840
NORM_VF="scale=2160:3840:flags=lanczos:force_original_aspect_ratio=decrease,pad=2160:3840:(ow-iw)/2:(oh-ih)/2:color=0x000000,setsar=1,fps=30,format=yuv420p"

# AI clip trims (each Seedance render is ~4s; we extract the cleanest motion window)
TRIMS=(
  "01 0.40 2.70"
  "02 0.30 3.40"
  "03 0.30 3.40"
  "04 0.30 3.40"
)
for line in "${TRIMS[@]}"; do
  set -- $line
  N=$1; SS=$2; T=$3
  ffmpeg -y -hide_banner -loglevel error -ss "$SS" -i clips/${N}.mp4 -t "$T" \
    -vf "$NORM_VF" -c:v libx264 -preset fast -crf 18 -an trimmed/${N}.mp4
done
echo "  ✓ 4 AI clips trimmed and lanczos-upscaled to 4K vertical"

# Build text scenes from PIL PNGs
make_text_clip () {  # png_path duration out_path
  local PNG=$1 DUR=$2 OUT=$3
  ffmpeg -y -hide_banner -loglevel error -loop 1 -i "$PNG" -t "$DUR" \
    -vf "scale=2160:3840:flags=lanczos,format=yuv420p,fps=30" \
    -c:v libx264 -preset fast -crf 18 -an "$OUT"
}

# Scene 5 — two cross-faded tagline cards.
# We render this as a SINGLE 2.4s clip:
#   first 0.7s: "A new ritual." only (overlay 05_a)
#   then dissolve to "A new ritual." + "In the heart of Madrid." (overlay 05_b)
#   hold for the rest of the duration
make_text_clip overlays/05_a.png 1.05 /tmp/aisccof_05_a.mp4   # 0.7 visible + 0.35 dissolve start (we'll overlap)
make_text_clip overlays/05_b.png 1.75 /tmp/aisccof_05_b.mp4   # 1.4 visible + 0.35 dissolve carry
# Cross-dissolve between A and B internally (0.35s overlap → 1.05 + 1.75 - 0.35 = 2.45 ≈ 2.4)
ffmpeg -y -hide_banner -loglevel error \
  -i /tmp/aisccof_05_a.mp4 -i /tmp/aisccof_05_b.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=fade:duration=0.35:offset=0.70,format=yuv420p[v]" \
  -map "[v]" -an -t 2.4 \
  -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p trimmed/05.mp4
echo "  ✓ scene 5 tagline reveal (built with internal A→B cross-dissolve)"

# Scene 6 — brand card, 1.7s, ends with fade-to-black on the last 0.4s
ffmpeg -y -hide_banner -loglevel error -loop 1 -i overlays/06_brand_card.png -t 1.7 \
  -vf "scale=2160:3840:flags=lanczos,format=yuv420p,fps=30,fade=t=out:st=1.3:d=0.4:color=black" \
  -c:v libx264 -preset fast -crf 18 -an trimmed/06.mp4
echo "  ✓ scene 6 brand card with fade-to-black"

# ---------- Chain all 6 segments with 0.4s smooth cross-dissolves ----------
# Offsets are cumulative on the running concatenated output:
#   seg 1 length = 2.7, transition starts at 2.7-0.4 = 2.3
#   net after 1+2 = 2.7 + 3.4 - 0.4 = 5.7  → next offset = 5.7 - 0.4 = 5.3
#   net after +3 = 5.7 + 3.4 - 0.4 = 8.7  → next offset = 8.3
#   net after +4 = 8.7 + 3.4 - 0.4 = 11.7 → next offset = 11.3
#   net after +5 = 11.7 + 2.4 - 0.4 = 13.7 → next offset = 13.3
#   net after +6 = 13.7 + 1.7 - 0.4 = 15.0 ✓

ffmpeg -y -hide_banner -loglevel error \
  -i trimmed/01.mp4 -i trimmed/02.mp4 -i trimmed/03.mp4 -i trimmed/04.mp4 -i trimmed/05.mp4 -i trimmed/06.mp4 \
  -filter_complex "\
    [0:v][1:v]xfade=transition=fade:duration=0.4:offset=2.3[v01]; \
    [v01][2:v]xfade=transition=fade:duration=0.4:offset=5.3[v012]; \
    [v012][3:v]xfade=transition=fade:duration=0.4:offset=8.3[v0123]; \
    [v0123][4:v]xfade=transition=fade:duration=0.4:offset=11.3[v01234]; \
    [v01234][5:v]xfade=transition=fade:duration=0.4:offset=13.3[v]" \
  -map "[v]" -an \
  -t 15.000 \
  -c:v libx264 -preset slow -crf 18 -profile:v high -level 5.1 \
  -movflags +faststart -pix_fmt yuv420p \
  final/aisc_coffee_15s_4k_silent.mp4
echo "  ✓ final/aisc_coffee_15s_4k_silent.mp4"

# Audio variant — preserve Seedance ambient bed for AI scenes; text scenes silent
build_ai_with_audio () {
  local N=$1 SS=$2 T=$3
  ffmpeg -y -hide_banner -loglevel error -ss "$SS" -i clips/${N}.mp4 -t "$T" \
    -vf "$NORM_VF" -c:v libx264 -preset fast -crf 18 \
    -c:a aac -b:a 192k -ar 48000 trimmed/${N}_aud.mp4
}
for line in "${TRIMS[@]}"; do
  set -- $line
  build_ai_with_audio $1 $2 $3
done

# Scene 5 + 6 as silent audio tracks
for IN in trimmed/05.mp4 trimmed/06.mp4; do
  OUT="${IN%.mp4}_aud.mp4"
  DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$IN")
  ffmpeg -y -hide_banner -loglevel error -i "$IN" \
    -f lavfi -t "$DUR" -i "anullsrc=channel_layout=stereo:sample_rate=48000" \
    -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest "$OUT"
done

ffmpeg -y -hide_banner -loglevel error \
  -i trimmed/01_aud.mp4 -i trimmed/02_aud.mp4 -i trimmed/03_aud.mp4 -i trimmed/04_aud.mp4 -i trimmed/05_aud.mp4 -i trimmed/06_aud.mp4 \
  -filter_complex "\
    [0:v][1:v]xfade=transition=fade:duration=0.4:offset=2.3[v01]; \
    [v01][2:v]xfade=transition=fade:duration=0.4:offset=5.3[v012]; \
    [v012][3:v]xfade=transition=fade:duration=0.4:offset=8.3[v0123]; \
    [v0123][4:v]xfade=transition=fade:duration=0.4:offset=11.3[v01234]; \
    [v01234][5:v]xfade=transition=fade:duration=0.4:offset=13.3[v]; \
    [0:a][1:a]acrossfade=d=0.4[a01]; \
    [a01][2:a]acrossfade=d=0.4[a012]; \
    [a012][3:a]acrossfade=d=0.4[a0123]; \
    [a0123][4:a]acrossfade=d=0.4[a01234]; \
    [a01234][5:a]acrossfade=d=0.4[a]" \
  -map "[v]" -map "[a]" \
  -t 15.000 \
  -c:v libx264 -preset slow -crf 19 -profile:v high -level 5.1 \
  -c:a aac -b:a 192k -ar 48000 \
  -movflags +faststart -pix_fmt yuv420p \
  final/aisc_coffee_15s_4k_audio.mp4
echo "  ✓ final/aisc_coffee_15s_4k_audio.mp4"

# Poster + contact sheet
ffmpeg -y -hide_banner -loglevel error -ss 13.5 -i final/aisc_coffee_15s_4k_silent.mp4 -frames:v 1 -q:v 2 final/poster.jpg
ffmpeg -y -hide_banner -loglevel error -i final/aisc_coffee_15s_4k_silent.mp4 -vf "fps=0.5,scale=540:-1,tile=2x4" -frames:v 1 -q:v 3 final/contact_sheet.jpg
echo "  ✓ poster + contact sheet"
ls -la final/
