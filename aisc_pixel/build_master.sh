#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Composite each Seedance clip with its deterministic title-card PNG.
# - Shot 1: title card fades in at t=0.4s (after boot animation kicks).
# - Shot 2: scoreboard rows fade in at t=0.4s.
# - Shot 3: end card fades in at t=0.3s.
# Master is exactly 15.000s, 1920x1080, 30fps, H.264 yuv420p, faststart.

mkdir -p titled final

for n in 01 02 03; do
  case $n in
    01) START=0.4 ;;
    02) START=0.4 ;;
    03) START=0.3 ;;
  esac
  FADE=0.4
  ffmpeg -y -hide_banner -loglevel error \
    -i clips/${n}.mp4 -i overlays/${n}.png \
    -filter_complex "[1:v]format=rgba,fade=t=in:st=${START}:d=${FADE}:alpha=1[ov];[0:v][ov]overlay=0:0:format=auto[v]" \
    -map "[v]" -an -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p \
    titled/${n}.mp4
  echo "  ✓ titled/${n}.mp4"
done

cat > /tmp/aisc_pixel_concat.txt <<EOF
file '$(pwd)/titled/01.mp4'
file '$(pwd)/titled/02.mp4'
file '$(pwd)/titled/03.mp4'
EOF

ffmpeg -y -hide_banner -loglevel error \
  -f concat -safe 0 -i /tmp/aisc_pixel_concat.txt -an \
  -t 15.000 \
  -vf "fps=30,scale=1920:1080:flags=lanczos,format=yuv420p" \
  -c:v libx264 -preset slow -crf 17 -profile:v high -level 4.2 \
  -movflags +faststart -pix_fmt yuv420p \
  final/aisc_pixel_launch_15s_1080p_silent.mp4
echo "  ✓ final/aisc_pixel_launch_15s_1080p_silent.mp4"

# Audio variant — keep Seedance ambient audio, normalize sample rate
ffmpeg -y -hide_banner -loglevel error \
  -i titled/01.mp4 \
  -i titled/02.mp4 \
  -i titled/03.mp4 \
  -i clips/01.mp4 \
  -i clips/02.mp4 \
  -i clips/03.mp4 \
  -filter_complex "\
    [0:v]fps=30,scale=1920:1080:flags=lanczos,format=yuv420p,setsar=1[v0]; \
    [1:v]fps=30,scale=1920:1080:flags=lanczos,format=yuv420p,setsar=1[v1]; \
    [2:v]fps=30,scale=1920:1080:flags=lanczos,format=yuv420p,setsar=1[v2]; \
    [3:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[a0]; \
    [4:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[a1]; \
    [5:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[a2]; \
    [v0][a0][v1][a1][v2][a2]concat=n=3:v=1:a=1[outv][outa]" \
  -map "[outv]" -map "[outa]" -t 15.000 \
  -c:v libx264 -preset slow -crf 18 \
  -c:a aac -b:a 192k -ar 48000 \
  -movflags +faststart -pix_fmt yuv420p \
  final/aisc_pixel_launch_15s_1080p_audio.mp4
echo "  ✓ final/aisc_pixel_launch_15s_1080p_audio.mp4"

ffmpeg -y -hide_banner -loglevel error -ss 1.0 -i final/aisc_pixel_launch_15s_1080p_silent.mp4 -frames:v 1 -q:v 2 final/poster.jpg
ffmpeg -y -hide_banner -loglevel error -i final/aisc_pixel_launch_15s_1080p_silent.mp4 -vf "fps=1,scale=480:-1,tile=5x3" -frames:v 1 -q:v 3 final/contact_sheet.jpg
echo "  ✓ final/poster.jpg + final/contact_sheet.jpg"
ls -la final/
