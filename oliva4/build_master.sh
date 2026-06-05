#!/usr/bin/env bash
# OLIVA & SAL v4 — 4K master with catchier on-screen script.
# Lanczos-upscales each 1080p Seedance clip to 3840×2160, composites the 4K
# overlay PNGs on top, concatenates with the v2 motion-peak trim windows.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p trimmed final

# 4K target. fps held at 30 to keep ffmpeg + concat clean.
NORM_VF="scale=3840:2160:flags=lanczos:force_original_aspect_ratio=decrease,pad=3840:2160:(ow-iw)/2:(oh-ih)/2:color=0x000000,setsar=1,fps=30,format=yuv420p"

# Trim windows from v2 (motion-peak-matched)
TRIMS=(
  "01 0.40 1.00"
  "02 0.40 2.50"
  "03 0.30 2.50"
  "04 0.30 2.50"
  "05a 0.30 1.00"
  "05b 1.20 1.00"
  "05c 1.40 1.00"
  "06 0.20 2.50"
  "07 0.40 2.30"
  "08 0.60 3.00"
)

for line in "${TRIMS[@]}"; do
  set -- $line
  N=$1; SS=$2; T=$3
  ffmpeg -y -hide_banner -loglevel error -ss "$SS" -i clips/${N}.mp4 -t "$T" \
    -vf "$NORM_VF" -c:v libx264 -preset fast -crf 18 -an trimmed/${N}.mp4
done
echo "  ✓ all AI clips trimmed and lanczos-upscaled to 4K"

# Scene 7 freeze frame at 4K
ffmpeg -y -hide_banner -loglevel error -sseof -0.05 -i trimmed/07.mp4 -frames:v 1 -q:v 2 trimmed/07_lastframe.png
ffmpeg -y -hide_banner -loglevel error -loop 1 -i trimmed/07_lastframe.png -t 0.20 \
  -vf "$NORM_VF" -c:v libx264 -preset fast -crf 18 -an trimmed/07_freeze.mp4
echo "  ✓ scene 7 freeze frame"

# Scene 8 corner-logo safety net at 4K
ffmpeg -y -hide_banner -loglevel error \
  -i trimmed/08.mp4 -i overlays/08.png \
  -filter_complex "[1:v]format=rgba[ov];[0:v][ov]overlay=0:0:format=auto[v]" \
  -map "[v]" -an -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p \
  trimmed/08_titled.mp4
echo "  ✓ scene 8 with corner logo"

make_text_clip () {  # png_path duration out_path
  local PNG=$1 DUR=$2 OUT=$3
  ffmpeg -y -hide_banner -loglevel error -loop 1 -i "$PNG" -t "$DUR" \
    -vf "scale=3840:2160:flags=lanczos,format=yuv420p,fps=30" \
    -c:v libx264 -preset fast -crf 18 -an "$OUT"
}

# Scene 1 text card with 0.04s black snap-in
ffmpeg -y -hide_banner -loglevel error -f lavfi -t 0.04 -i color=c=black:s=3840x2160:r=30 \
  -c:v libx264 -preset fast -crf 18 -an /tmp/oliva4_black_short.mp4
make_text_clip overlays/01_textcard.png 0.46 /tmp/oliva4_text01.mp4
printf "file '%s'\nfile '%s'\n" /tmp/oliva4_black_short.mp4 /tmp/oliva4_text01.mp4 > /tmp/oliva4_text01_list.txt
ffmpeg -y -hide_banner -loglevel error -f concat -safe 0 -i /tmp/oliva4_text01_list.txt -c copy trimmed/01_text.mp4
echo "  ✓ scene 1 text card"

# Scene 9 with black-flash snap-ins
build_text_with_flash () {
  local PNG=$1 DUR=$2 OUT=$3
  local CARD_DUR
  CARD_DUR=$(awk "BEGIN { printf \"%.3f\", $DUR - 0.04 }")
  make_text_clip "$PNG" "$CARD_DUR" /tmp/oliva4_card_only.mp4
  ffmpeg -y -hide_banner -loglevel error -f lavfi -t 0.04 -i color=c=black:s=3840x2160:r=30 \
    -c:v libx264 -preset fast -crf 18 -an /tmp/oliva4_blackflash.mp4
  printf "file '%s'\nfile '%s'\n" /tmp/oliva4_blackflash.mp4 /tmp/oliva4_card_only.mp4 > /tmp/oliva4_card_list.txt
  ffmpeg -y -hide_banner -loglevel error -f concat -safe 0 -i /tmp/oliva4_card_list.txt -c copy "$OUT"
}
build_text_with_flash overlays/09_1.png 0.60 trimmed/09_1.mp4
build_text_with_flash overlays/09_2.png 0.60 trimmed/09_2.mp4
build_text_with_flash overlays/09_3.png 1.30 trimmed/09_3.mp4
echo "  ✓ scene 9 tagline reveal"

# Scene 10 brand card 2.5s with fade-to-black
ffmpeg -y -hide_banner -loglevel error -loop 1 -i overlays/10.png -t 2.5 \
  -vf "scale=3840:2160:flags=lanczos,format=yuv420p,fps=30,fade=t=out:st=2.1:d=0.4:color=black" \
  -c:v libx264 -preset fast -crf 18 -an trimmed/10.mp4
echo "  ✓ scene 10 brand card"

SEGMENTS=(
  trimmed/01.mp4 trimmed/01_text.mp4
  trimmed/02.mp4 trimmed/03.mp4 trimmed/04.mp4
  trimmed/05a.mp4 trimmed/05b.mp4 trimmed/05c.mp4
  trimmed/06.mp4 trimmed/07.mp4 trimmed/07_freeze.mp4 trimmed/08_titled.mp4
  trimmed/09_1.mp4 trimmed/09_2.mp4 trimmed/09_3.mp4 trimmed/10.mp4
)
{
  for f in "${SEGMENTS[@]}"; do printf "file '%s'\n" "$(pwd)/$f"; done
} > /tmp/oliva4_concat.txt

ffmpeg -y -hide_banner -loglevel error \
  -f concat -safe 0 -i /tmp/oliva4_concat.txt -an \
  -vf "fps=30,scale=3840:2160:flags=lanczos,format=yuv420p,tpad=stop_mode=clone:stop_duration=1" \
  -t 25.000 \
  -c:v libx264 -preset slow -crf 18 -profile:v high -level 5.1 \
  -movflags +faststart -pix_fmt yuv420p \
  final/oliva_sal_tapas_25s_4k_silent.mp4
echo "  ✓ final/oliva_sal_tapas_25s_4k_silent.mp4"

# Audio variant — preserve Seedance ambient bed for AI scenes
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

ffmpeg -y -hide_banner -loglevel error -ss 0.60 -i clips/08.mp4 -i overlays/08.png -t 3.00 \
  -filter_complex "[0:v]${NORM_VF}[bg];[1:v]format=rgba[ov];[bg][ov]overlay=0:0:format=auto[v]" \
  -map "[v]" -map "0:a" -c:v libx264 -preset fast -crf 18 -c:a aac -b:a 192k -ar 48000 \
  trimmed/08_titled_aud.mp4

ffmpeg -y -hide_banner -loglevel error -loop 1 -i trimmed/07_lastframe.png -t 0.20 \
  -f lavfi -i "anullsrc=channel_layout=stereo:sample_rate=48000" \
  -map 0:v -map 1:a -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p \
  -vf "$NORM_VF" -c:a aac -b:a 192k -shortest trimmed/07_freeze_aud.mp4

for IN in trimmed/01_text.mp4 trimmed/09_1.mp4 trimmed/09_2.mp4 trimmed/09_3.mp4 trimmed/10.mp4; do
  OUT="${IN%.mp4}_aud.mp4"
  DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$IN")
  ffmpeg -y -hide_banner -loglevel error -i "$IN" \
    -f lavfi -t "$DUR" -i "anullsrc=channel_layout=stereo:sample_rate=48000" \
    -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest "$OUT"
done

AUD_SEGMENTS=(
  trimmed/01_aud.mp4 trimmed/01_text_aud.mp4
  trimmed/02_aud.mp4 trimmed/03_aud.mp4 trimmed/04_aud.mp4
  trimmed/05a_aud.mp4 trimmed/05b_aud.mp4 trimmed/05c_aud.mp4
  trimmed/06_aud.mp4 trimmed/07_aud.mp4 trimmed/07_freeze_aud.mp4 trimmed/08_titled_aud.mp4
  trimmed/09_1_aud.mp4 trimmed/09_2_aud.mp4 trimmed/09_3_aud.mp4 trimmed/10_aud.mp4
)
{ for f in "${AUD_SEGMENTS[@]}"; do printf "file '%s'\n" "$(pwd)/$f"; done; } > /tmp/oliva4_concat_aud.txt

ffmpeg -y -hide_banner -loglevel error \
  -f concat -safe 0 -i /tmp/oliva4_concat_aud.txt \
  -vf "tpad=stop_mode=clone:stop_duration=1" -af "apad=pad_dur=1" \
  -t 25.000 \
  -c:v libx264 -preset slow -crf 19 -profile:v high -level 5.1 \
  -c:a aac -b:a 192k -ar 48000 \
  -movflags +faststart -pix_fmt yuv420p \
  final/oliva_sal_tapas_25s_4k_audio.mp4
echo "  ✓ final/oliva_sal_tapas_25s_4k_audio.mp4"

# 4K poster + contact sheet
ffmpeg -y -hide_banner -loglevel error -ss 23.0 -i final/oliva_sal_tapas_25s_4k_silent.mp4 -frames:v 1 -q:v 2 final/poster.jpg
ffmpeg -y -hide_banner -loglevel error -i final/oliva_sal_tapas_25s_4k_silent.mp4 -vf "fps=0.4,scale=960:-1,tile=5x2" -frames:v 1 -q:v 3 final/contact_sheet.jpg
echo "  ✓ poster + contact sheet"
ls -la final/
