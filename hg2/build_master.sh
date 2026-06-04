#!/usr/bin/env bash
# Cinematic 5-scene reel: 5 × 5s native Seedance clips, trimmed to 3s each,
# safety-net overlay applied, concatenated to exactly 15.000s.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p trimmed titled final

# Trim each clip to its 3s window. We keep the middle 3s of each 5s clip so the
# motion lands in the centre of each scene and we avoid the warm-up / wind-down
# frames at the ends. (Seedance min duration is 4s, so we must over-render then trim.)
for n in 01 02 03 04 05; do
  ffmpeg -y -hide_banner -loglevel error -ss 1.0 -i clips/${n}.mp4 -t 3.0 \
    -vf "scale=1920:1080:flags=lanczos:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=0x0c1216,setsar=1,fps=30,format=yuv420p" \
    -c:v libx264 -preset fast -crf 17 -an trimmed/${n}.mp4
  echo "  ✓ trimmed/${n}.mp4"
done

# Safety-net overlay (50% opacity) so any glyph drift mid-clip is overruled by the
# deterministic PIL typography.
for n in 01 02 03 04 05; do
  ffmpeg -y -hide_banner -loglevel error \
    -i trimmed/${n}.mp4 -i overlays/${n}.png \
    -filter_complex "[1:v]format=rgba,colorchannelmixer=aa=0.50[ov];[0:v][ov]overlay=0:0:format=auto[v]" \
    -map "[v]" -an -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p \
    titled/${n}.mp4
  echo "  ✓ titled/${n}.mp4"
done

cat > /tmp/hg2_concat.txt <<EOF
file '$(pwd)/titled/01.mp4'
file '$(pwd)/titled/02.mp4'
file '$(pwd)/titled/03.mp4'
file '$(pwd)/titled/04.mp4'
file '$(pwd)/titled/05.mp4'
EOF

ffmpeg -y -hide_banner -loglevel error \
  -f concat -safe 0 -i /tmp/hg2_concat.txt -an \
  -t 15.000 \
  -vf "fps=30,scale=1920:1080:flags=lanczos,format=yuv420p" \
  -c:v libx264 -preset slow -crf 17 -profile:v high -level 4.2 \
  -movflags +faststart -pix_fmt yuv420p \
  final/honestgreens_cinematic_15s_1080p_silent.mp4
echo "  ✓ final/honestgreens_cinematic_15s_1080p_silent.mp4"

# Audio variant — keep Seedance ambient bed across all five trimmed clips
for n in 01 02 03 04 05; do
  ffmpeg -y -hide_banner -loglevel error -ss 1.0 -i clips/${n}.mp4 -t 3.0 \
    -i overlays/${n}.png \
    -filter_complex "[0:v]scale=1920:1080:flags=lanczos:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=0x0c1216,setsar=1,fps=30,format=yuv420p[bg];[1:v]format=rgba,colorchannelmixer=aa=0.50[ov];[bg][ov]overlay=0:0:format=auto[v]" \
    -map "[v]" -map "0:a" -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p \
    -c:a aac -b:a 192k -ar 48000 \
    trimmed/${n}_aud.mp4
done

ffmpeg -y -hide_banner -loglevel error \
  -i trimmed/01_aud.mp4 -i trimmed/02_aud.mp4 -i trimmed/03_aud.mp4 -i trimmed/04_aud.mp4 -i trimmed/05_aud.mp4 \
  -filter_complex "\
    [0:v]setsar=1[v0];[1:v]setsar=1[v1];[2:v]setsar=1[v2];[3:v]setsar=1[v3];[4:v]setsar=1[v4]; \
    [0:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[a0]; \
    [1:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[a1]; \
    [2:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[a2]; \
    [3:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[a3]; \
    [4:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[a4]; \
    [v0][a0][v1][a1][v2][a2][v3][a3][v4][a4]concat=n=5:v=1:a=1[outv][outa]" \
  -map "[outv]" -map "[outa]" -t 15.000 \
  -c:v libx264 -preset slow -crf 18 \
  -c:a aac -b:a 192k -ar 48000 \
  -movflags +faststart -pix_fmt yuv420p \
  final/honestgreens_cinematic_15s_1080p_audio.mp4
echo "  ✓ final/honestgreens_cinematic_15s_1080p_audio.mp4"

ffmpeg -y -hide_banner -loglevel error -ss 12.5 -i final/honestgreens_cinematic_15s_1080p_silent.mp4 -frames:v 1 -q:v 2 final/poster.jpg
ffmpeg -y -hide_banner -loglevel error -i final/honestgreens_cinematic_15s_1080p_silent.mp4 -vf "fps=1,scale=480:-1,tile=5x3" -frames:v 1 -q:v 3 final/contact_sheet.jpg
echo "  ✓ poster + contact sheet"
ls -la final/
