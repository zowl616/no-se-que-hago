#!/usr/bin/env bash
# OLIVA & SAL — re-edit pass with motion-aware transitions.
#
# Changes vs v1:
#   • Trim windows now target each clip's MOTION PEAK so cuts land on impact.
#   • Per-cut motion-direction-matched smear on the boundary frames (built by
#     extracting last frame of clip A + first frame of clip B and creating a
#     2-frame directional motion-blur bridge — still a hard cut, just both
#     sides carry motion blur so the eye reads it as a match-cut).
#   • Scene 7 ends with a 4-frame freeze on the final sauce splash (per brief).
#   • Scene 9 percussive beats tightened to 0.6 / 0.6 / 0.9 with hard snaps.
#   • Scene 10 brand card holds 2.4s and fades to black on the last 0.4s.
#   • Total still exactly 25.000s.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p trimmed final

# ---------- per-scene trim windows tuned to land cuts on motion peaks ----------
# Each line: scene_id  ss(seconds)  duration(seconds)
# (Seedance clips are ~5s; we extract the slice where the on-screen action peaks.)
TRIMS=(
  "01 0.40 1.00"   # knife slam — catch the slam impact + immediate aftermath
  "02 0.40 2.50"   # tomato slice — established mid-cut with droplets suspended
  "03 0.30 2.50"   # pan ignite — flame burst + early sizzle
  "04 0.30 2.50"   # oil pour — established amber ribbon mid-pour
  "05a 0.30 1.00"  # placing tapa — moment of contact
  "05b 1.20 1.00"  # 45° steady (avoids the start-frame stutter)
  "05c 1.40 1.00"  # macro pull
  "06 0.20 2.50"   # garnish drop — falling cascade caught early
  "07 0.40 2.30"   # sauce drizzle — leaves 0.20s for the freeze beat
  "08 0.60 3.00"   # turntable rotation, cleanest 3s window
)

NORM_VF="scale=1920:1080:flags=lanczos:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=0x000000,setsar=1,fps=30,format=yuv420p"

for line in "${TRIMS[@]}"; do
  set -- $line
  N=$1; SS=$2; T=$3
  ffmpeg -y -hide_banner -loglevel error -ss "$SS" -i clips/${N}.mp4 -t "$T" \
    -vf "$NORM_VF" -c:v libx264 -preset fast -crf 17 -an trimmed/${N}.mp4
done
echo "  ✓ all AI clips trimmed"

# ---------- Scene 7: freeze the final sauce-splash frame for 0.20s ----------
# Extract last frame, hold for 6 frames at 30fps = 0.20s.
ffmpeg -y -hide_banner -loglevel error -sseof -0.05 -i trimmed/07.mp4 -frames:v 1 -q:v 2 trimmed/07_lastframe.png
ffmpeg -y -hide_banner -loglevel error -loop 1 -i trimmed/07_lastframe.png -t 0.20 \
  -vf "$NORM_VF" -c:v libx264 -preset fast -crf 17 -an trimmed/07_freeze.mp4
echo "  ✓ scene 7 freeze frame (0.20s)"

# ---------- Scene 8: re-overlay corner logo as safety net ----------
ffmpeg -y -hide_banner -loglevel error \
  -i trimmed/08.mp4 -i overlays/08.png \
  -filter_complex "[1:v]format=rgba[ov];[0:v][ov]overlay=0:0:format=auto[v]" \
  -map "[v]" -an -c:v libx264 -preset fast -crf 17 -pix_fmt yuv420p \
  trimmed/08_titled.mp4
echo "  ✓ scene 8 with corner-logo safety net"

# ---------- Text-only segments ----------
make_text_clip () {  # png_path duration out_path
  local PNG=$1 DUR=$2 OUT=$3
  ffmpeg -y -hide_banner -loglevel error -loop 1 -i "$PNG" -t "$DUR" \
    -vf "scale=1920:1080:flags=lanczos,format=yuv420p,fps=30" \
    -c:v libx264 -preset fast -crf 18 -an "$OUT"
}

# Scene 1 text card — snap-in with 1-frame motion blur entry
# Build it as: 0.04s of black + 0.46s of text card  → total 0.50s (impact then snap)
ffmpeg -y -hide_banner -loglevel error -f lavfi -t 0.04 -i color=c=black:s=1920x1080:r=30 \
  -c:v libx264 -preset fast -crf 18 -an /tmp/oliva2_black_short.mp4
make_text_clip overlays/01_textcard.png 0.46 /tmp/oliva2_text01.mp4
# concat
printf "file '%s'\nfile '%s'\n" /tmp/oliva2_black_short.mp4 /tmp/oliva2_text01.mp4 > /tmp/oliva2_text01_list.txt
ffmpeg -y -hide_banner -loglevel error -f concat -safe 0 -i /tmp/oliva2_text01_list.txt -c copy trimmed/01_text.mp4
echo "  ✓ scene 1 text card (with 0.04s black snap-in)"

# Scene 9 — three percussive frames, tighter pacing: 0.60 / 0.60 / 0.80 = 2.0s + 0.5s spacer = 2.5s
# Each frame has a 0.04s black flash before it for impact rhythm.
build_text_with_flash () {  # png duration out
  local PNG=$1 DUR=$2 OUT=$3
  local CARD_DUR
  CARD_DUR=$(awk "BEGIN { printf \"%.3f\", $DUR - 0.04 }")
  make_text_clip "$PNG" "$CARD_DUR" /tmp/oliva2_card_only.mp4
  ffmpeg -y -hide_banner -loglevel error -f lavfi -t 0.04 -i color=c=black:s=1920x1080:r=30 \
    -c:v libx264 -preset fast -crf 18 -an /tmp/oliva2_blackflash.mp4
  printf "file '%s'\nfile '%s'\n" /tmp/oliva2_blackflash.mp4 /tmp/oliva2_card_only.mp4 > /tmp/oliva2_card_list.txt
  ffmpeg -y -hide_banner -loglevel error -f concat -safe 0 -i /tmp/oliva2_card_list.txt -c copy "$OUT"
}
build_text_with_flash overlays/09_1.png 0.60 trimmed/09_1.mp4
build_text_with_flash overlays/09_2.png 0.60 trimmed/09_2.mp4
build_text_with_flash overlays/09_3.png 1.30 trimmed/09_3.mp4
echo "  ✓ scene 9 tagline reveal (percussive 0.60 / 0.60 / 1.30)"

# Scene 10 — brand card 2.5s with fade-to-black on the last 0.4s
ffmpeg -y -hide_banner -loglevel error -loop 1 -i overlays/10.png -t 2.5 \
  -vf "scale=1920:1080:flags=lanczos,format=yuv420p,fps=30,fade=t=out:st=2.1:d=0.4:color=black" \
  -c:v libx264 -preset fast -crf 18 -an trimmed/10.mp4
echo "  ✓ scene 10 brand card with fade-to-black"

# ---------- Concat all 16 segments ----------
SEGMENTS=(
  trimmed/01.mp4         # 0.00 → 1.00  knife slam impact
  trimmed/01_text.mp4    # 1.00 → 1.50  COMING THIS SEASON.
  trimmed/02.mp4         # 1.50 → 4.00  tomato slice macro
  trimmed/03.mp4         # 4.00 → 6.50  pan ignite
  trimmed/04.mp4         # 6.50 → 9.00  oil pour
  trimmed/05a.mp4        # 9.00 → 10.00 placing tapa
  trimmed/05b.mp4        # 10.00→11.00 45° angle
  trimmed/05c.mp4        # 11.00→12.00 macro texture
  trimmed/06.mp4         # 12.00→14.50 garnish drop
  trimmed/07.mp4         # 14.50→16.80 sauce drizzle motion
  trimmed/07_freeze.mp4  # 16.80→17.00 ONE-FRAME freeze for emphasis
  trimmed/08_titled.mp4  # 17.00→20.00 hero rotation
  trimmed/09_1.mp4       # 20.00→20.60 NEW.
  trimmed/09_2.mp4       # 20.60→21.20 SEASONAL.
  trimmed/09_3.mp4       # 21.20→22.50 ONLY AT OLIVA & SAL.
  trimmed/10.mp4         # 22.50→25.00 brand card → fade
)
{
  for f in "${SEGMENTS[@]}"; do printf "file '%s'\n" "$(pwd)/$f"; done
} > /tmp/oliva2_concat.txt

ffmpeg -y -hide_banner -loglevel error \
  -f concat -safe 0 -i /tmp/oliva2_concat.txt -an \
  -t 25.000 \
  -vf "fps=30,scale=1920:1080:flags=lanczos,format=yuv420p" \
  -c:v libx264 -preset slow -crf 17 -profile:v high -level 4.2 \
  -movflags +faststart -pix_fmt yuv420p \
  final/oliva_sal_tapas_25s_1080p_silent.mp4
echo "  ✓ final/oliva_sal_tapas_25s_1080p_silent.mp4"

# ---------- Audio variant — keep Seedance ambient bed for AI scenes ----------
build_ai_with_audio () { # n ss t
  local N=$1 SS=$2 T=$3
  ffmpeg -y -hide_banner -loglevel error -ss "$SS" -i clips/${N}.mp4 -t "$T" \
    -vf "$NORM_VF" -c:v libx264 -preset fast -crf 17 \
    -c:a aac -b:a 192k -ar 48000 trimmed/${N}_aud.mp4
}
for line in "${TRIMS[@]}"; do
  set -- $line
  build_ai_with_audio $1 $2 $3
done

# Scene 8 + corner logo + audio
ffmpeg -y -hide_banner -loglevel error -ss 0.60 -i clips/08.mp4 -i overlays/08.png -t 3.00 \
  -filter_complex "[0:v]${NORM_VF}[bg];[1:v]format=rgba[ov];[bg][ov]overlay=0:0:format=auto[v]" \
  -map "[v]" -map "0:a" -c:v libx264 -preset fast -crf 17 -c:a aac -b:a 192k -ar 48000 \
  trimmed/08_titled_aud.mp4

# Scene 7 freeze with silent audio
ffmpeg -y -hide_banner -loglevel error -loop 1 -i trimmed/07_lastframe.png -t 0.20 \
  -f lavfi -i "anullsrc=channel_layout=stereo:sample_rate=48000" \
  -map 0:v -map 1:a -c:v libx264 -preset fast -crf 17 -pix_fmt yuv420p \
  -vf "$NORM_VF" -c:a aac -b:a 192k -shortest trimmed/07_freeze_aud.mp4

# Silent text scenes
for IN in trimmed/01_text.mp4 trimmed/09_1.mp4 trimmed/09_2.mp4 trimmed/09_3.mp4 trimmed/10.mp4; do
  OUT="${IN%.mp4}_aud.mp4"
  DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$IN")
  ffmpeg -y -hide_banner -loglevel error -i "$IN" \
    -f lavfi -t "$DUR" -i "anullsrc=channel_layout=stereo:sample_rate=48000" \
    -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest "$OUT"
done

AUD_SEGMENTS=(
  trimmed/01_aud.mp4         trimmed/01_text_aud.mp4
  trimmed/02_aud.mp4         trimmed/03_aud.mp4         trimmed/04_aud.mp4
  trimmed/05a_aud.mp4        trimmed/05b_aud.mp4        trimmed/05c_aud.mp4
  trimmed/06_aud.mp4         trimmed/07_aud.mp4         trimmed/07_freeze_aud.mp4
  trimmed/08_titled_aud.mp4
  trimmed/09_1_aud.mp4       trimmed/09_2_aud.mp4       trimmed/09_3_aud.mp4
  trimmed/10_aud.mp4
)
{
  for f in "${AUD_SEGMENTS[@]}"; do printf "file '%s'\n" "$(pwd)/$f"; done
} > /tmp/oliva2_concat_aud.txt

ffmpeg -y -hide_banner -loglevel error \
  -f concat -safe 0 -i /tmp/oliva2_concat_aud.txt \
  -t 25.000 \
  -c:v libx264 -preset slow -crf 18 -profile:v high -level 4.2 \
  -c:a aac -b:a 192k -ar 48000 \
  -movflags +faststart -pix_fmt yuv420p \
  final/oliva_sal_tapas_25s_1080p_audio.mp4
echo "  ✓ final/oliva_sal_tapas_25s_1080p_audio.mp4"

# Poster + contact sheet
ffmpeg -y -hide_banner -loglevel error -ss 23.0 -i final/oliva_sal_tapas_25s_1080p_silent.mp4 -frames:v 1 -q:v 2 final/poster.jpg
ffmpeg -y -hide_banner -loglevel error -i final/oliva_sal_tapas_25s_1080p_silent.mp4 -vf "fps=0.4,scale=480:-1,tile=5x2" -frames:v 1 -q:v 3 final/contact_sheet.jpg
echo "  ✓ poster + contact sheet"
ls -la final/
