#!/usr/bin/env bash
# Build the AISC v2 launch master from the seedance clips.
# Each clip already has the typography baked in (because we composited the
# overlay onto the start image *before* feeding to Seedance), so we only need
# to concat. We also re-overlay a tiny 30%-opacity copy of the original PIL
# overlay on top as a "safety net" — this guarantees that if Seedance ever
# drifts a glyph, the deterministic typography is still visible in the final.
set -euo pipefail

cd "$(dirname "$0")"

mkdir -p titled final

for n in 01 02 03; do
  ffmpeg -y -hide_banner -loglevel error \
    -i clips/${n}.mp4 -i overlays/${n}.png \
    -filter_complex "[1:v]format=rgba,colorchannelmixer=aa=0.55[ov];[0:v][ov]overlay=0:0:format=auto[v]" \
    -map "[v]" -an -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p \
    titled/${n}.mp4
  echo "  ✓ titled/${n}.mp4"
done

cat > /tmp/aisc_v2_concat.txt <<EOF
file '$(pwd)/titled/01.mp4'
file '$(pwd)/titled/02.mp4'
file '$(pwd)/titled/03.mp4'
EOF

ffmpeg -y -hide_banner -loglevel error \
  -f concat -safe 0 -i /tmp/aisc_v2_concat.txt -an \
  -t 15.000 \
  -vf "fps=30,scale=1920:1080:flags=lanczos,format=yuv420p" \
  -c:v libx264 -preset slow -crf 17 -profile:v high -level 4.2 \
  -movflags +faststart -pix_fmt yuv420p \
  final/aisc_launch_15s_1080p_silent.mp4
echo "  ✓ final/aisc_launch_15s_1080p_silent.mp4"

ffmpeg -y -hide_banner -loglevel error \
  -i titled/01.mp4 -i titled/02.mp4 -i titled/03.mp4 \
  -i clips/01.mp4 -i clips/02.mp4 -i clips/03.mp4 \
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
  final/aisc_launch_15s_1080p_audio.mp4
echo "  ✓ final/aisc_launch_15s_1080p_audio.mp4"

ffmpeg -y -hide_banner -loglevel error -ss 1.0 -i final/aisc_launch_15s_1080p_silent.mp4 -frames:v 1 -q:v 2 final/poster.jpg
ffmpeg -y -hide_banner -loglevel error -i final/aisc_launch_15s_1080p_silent.mp4 -vf "fps=1,scale=480:-1,tile=5x3" -frames:v 1 -q:v 3 final/contact_sheet.jpg
echo "  ✓ final/poster.jpg + final/contact_sheet.jpg"
ls -la final/
