#!/usr/bin/env bash
# Build the OLIVA & SAL 25s tapas launch master.
#
# Scene timing (25.000s total):
#   Scene 1  (0.0–1.5)  knife slam clip (1.0s)  +  scene-1 text card (0.5s)
#   Scene 2  (1.5–4.0)  tomato slice clip (2.5s)
#   Scene 3  (4.0–6.5)  pan ignite clip (2.5s)
#   Scene 4  (6.5–9.0)  oil pour clip (2.5s)
#   Scene 5  (9.0–12.0) plating triple-cut: 5a (1.0s) + 5b (1.0s) + 5c (1.0s)
#   Scene 6  (12.0–14.5) garnish drop (2.5s)
#   Scene 7  (14.5–17.0) sauce hit (2.5s)
#   Scene 8  (17.0–20.0) hero rotation with corner logo (3.0s)
#   Scene 9  (20.0–22.5) tagline reveal: NEW (0.7s) + SEASONAL (0.7s) + ONLY AT (1.1s)
#   Scene 10 (22.5–25.0) brand card (2.5s, fade-to-black on final beat)
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p trimmed final

# --- Trim each AI clip to its required length, taking the most useful slice ---
# Take frames near the start for impact-driven scenes (1, 2, 6) and the middle
# for sustained ones (the rest). Format normalised to 1920x1080 30fps yuv420p.
TRIM_DEFS=(
  "01 0.0 1.0"
  "02 0.5 2.5"
  "03 0.5 2.5"
  "04 0.5 2.5"
  "05a 0.0 1.0"
  "05b 0.5 1.0"
  "05c 1.0 1.0"
  "06 0.0 2.5"
  "07 0.5 2.5"
  "08 0.5 3.0"
)
for def in "${TRIM_DEFS[@]}"; do
  set -- $def
  N=$1; SS=$2; T=$3
  ffmpeg -y -hide_banner -loglevel error -ss $SS -i clips/${N}.mp4 -t $T \
    -vf "scale=1920:1080:flags=lanczos:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=0x000000,setsar=1,fps=30,format=yuv420p" \
    -c:v libx264 -preset fast -crf 17 -an trimmed/${N}.mp4
done
echo "  ✓ all AI clips trimmed"

# --- Scene 8: composite the corner logo as a safety-net top overlay too ---
ffmpeg -y -hide_banner -loglevel error \
  -i trimmed/08.mp4 -i overlays/08.png \
  -filter_complex "[1:v]format=rgba,colorchannelmixer=aa=1.0[ov];[0:v][ov]overlay=0:0:format=auto[v]" \
  -map "[v]" -an -c:v libx264 -preset fast -crf 17 -pix_fmt yuv420p \
  trimmed/08_titled.mp4
echo "  ✓ scene 8 with logo safety-net"

# --- Generate text-only scene clips from PNG title cards (looped → mp4) ---
make_text_clip () {  # png_path duration out_path
  local PNG=$1 DUR=$2 OUT=$3
  ffmpeg -y -hide_banner -loglevel error -loop 1 -i "$PNG" -t "$DUR" \
    -vf "scale=1920:1080:flags=lanczos,format=yuv420p,fps=30" \
    -c:v libx264 -preset fast -crf 18 -an "$OUT"
}

# Scene 1 text card (0.5s)
make_text_clip overlays/01_textcard.png 0.5 trimmed/01_text.mp4
echo "  ✓ scene 1 text card"

# Scene 9 tagline reveal — three percussive frames
# Each frame snaps in: we render 0.05s of black, then hold the frame for ~0.65s, then black for 0.05s
# Simpler: hold each frame for its allotted slice. NEW 0.7s, SEASONAL 0.7s, ONLY AT 1.1s = 2.5s
make_text_clip overlays/09_1.png 0.7 trimmed/09_1.mp4
make_text_clip overlays/09_2.png 0.7 trimmed/09_2.mp4
make_text_clip overlays/09_3.png 1.1 trimmed/09_3.mp4
echo "  ✓ scene 9 tagline reveal"

# Scene 10 brand card (2.5s) with fade-to-black on the final 0.4s
ffmpeg -y -hide_banner -loglevel error -loop 1 -i overlays/10.png -t 2.5 \
  -vf "scale=1920:1080:flags=lanczos,format=yuv420p,fps=30,fade=t=out:st=2.1:d=0.4:color=black" \
  -c:v libx264 -preset fast -crf 18 -an trimmed/10.mp4
echo "  ✓ scene 10 brand card with fade-to-black"

# --- Concat in order ---
cat > /tmp/oliva_concat.txt <<EOF
file '$(pwd)/trimmed/01.mp4'
file '$(pwd)/trimmed/01_text.mp4'
file '$(pwd)/trimmed/02.mp4'
file '$(pwd)/trimmed/03.mp4'
file '$(pwd)/trimmed/04.mp4'
file '$(pwd)/trimmed/05a.mp4'
file '$(pwd)/trimmed/05b.mp4'
file '$(pwd)/trimmed/05c.mp4'
file '$(pwd)/trimmed/06.mp4'
file '$(pwd)/trimmed/07.mp4'
file '$(pwd)/trimmed/08_titled.mp4'
file '$(pwd)/trimmed/09_1.mp4'
file '$(pwd)/trimmed/09_2.mp4'
file '$(pwd)/trimmed/09_3.mp4'
file '$(pwd)/trimmed/10.mp4'
EOF

ffmpeg -y -hide_banner -loglevel error \
  -f concat -safe 0 -i /tmp/oliva_concat.txt -an \
  -t 25.000 \
  -vf "fps=30,scale=1920:1080:flags=lanczos,format=yuv420p" \
  -c:v libx264 -preset slow -crf 17 -profile:v high -level 4.2 \
  -movflags +faststart -pix_fmt yuv420p \
  final/oliva_sal_tapas_25s_1080p_silent.mp4
echo "  ✓ final/oliva_sal_tapas_25s_1080p_silent.mp4"

# Audio variant — keep Seedance ambient bed for AI scenes; text scenes silent
# Easier path: per-scene, mux audio for AI scenes, leave silent for text scenes,
# then concat with audio. Use anullsrc for silent text frames.
audio_def () {  # in.mp4 out.mp4
  local IN=$1 OUT=$2
  if ffprobe -v error -select_streams a:0 -show_entries stream=codec_type "$IN" | grep -q 'codec_type=audio'; then
    ffmpeg -y -hide_banner -loglevel error -i "$IN" -c copy "$OUT"
  else
    DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$IN")
    ffmpeg -y -hide_banner -loglevel error -i "$IN" \
      -f lavfi -t "$DUR" -i "anullsrc=channel_layout=stereo:sample_rate=48000" \
      -c:v copy -c:a aac -b:a 192k -shortest "$OUT"
  fi
}

# Scene 8 audio: take from the original clip, pair with titled video
ffmpeg -y -hide_banner -loglevel error \
  -i trimmed/08_titled.mp4 -i clips/08.mp4 \
  -ss 0.5 -t 3.0 \
  -map 0:v -map 1:a \
  -c:v copy -c:a aac -b:a 192k -ar 48000 \
  -shortest \
  trimmed/08_titled_aud.mp4 || true

# For each AI scene, build _aud.mp4 by re-trimming to keep audio in sync
build_ai_with_audio () { # n ss t
  local N=$1 SS=$2 T=$3
  ffmpeg -y -hide_banner -loglevel error -ss "$SS" -i clips/${N}.mp4 -t "$T" \
    -vf "scale=1920:1080:flags=lanczos:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=0x000000,setsar=1,fps=30,format=yuv420p" \
    -c:v libx264 -preset fast -crf 17 \
    -c:a aac -b:a 192k -ar 48000 \
    trimmed/${N}_aud.mp4
}
build_ai_with_audio 01 0.0 1.0
build_ai_with_audio 02 0.5 2.5
build_ai_with_audio 03 0.5 2.5
build_ai_with_audio 04 0.5 2.5
build_ai_with_audio 05a 0.0 1.0
build_ai_with_audio 05b 0.5 1.0
build_ai_with_audio 05c 1.0 1.0
build_ai_with_audio 06 0.0 2.5
build_ai_with_audio 07 0.5 2.5

# Scene 8 with logo + audio
ffmpeg -y -hide_banner -loglevel error -ss 0.5 -i clips/08.mp4 -i overlays/08.png -t 3.0 \
  -filter_complex "[0:v]scale=1920:1080:flags=lanczos:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=0x000000,setsar=1,fps=30,format=yuv420p[bg];[1:v]format=rgba[ov];[bg][ov]overlay=0:0:format=auto[v]" \
  -map "[v]" -map "0:a" -c:v libx264 -preset fast -crf 17 -c:a aac -b:a 192k -ar 48000 \
  trimmed/08_aud.mp4

# Silent text scenes (with silent audio track)
for IN in trimmed/01_text.mp4 trimmed/09_1.mp4 trimmed/09_2.mp4 trimmed/09_3.mp4 trimmed/10.mp4; do
  OUT="${IN%.mp4}_aud.mp4"
  DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$IN")
  ffmpeg -y -hide_banner -loglevel error -i "$IN" \
    -f lavfi -t "$DUR" -i "anullsrc=channel_layout=stereo:sample_rate=48000" \
    -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest "$OUT"
done

cat > /tmp/oliva_concat_aud.txt <<EOF
file '$(pwd)/trimmed/01_aud.mp4'
file '$(pwd)/trimmed/01_text_aud.mp4'
file '$(pwd)/trimmed/02_aud.mp4'
file '$(pwd)/trimmed/03_aud.mp4'
file '$(pwd)/trimmed/04_aud.mp4'
file '$(pwd)/trimmed/05a_aud.mp4'
file '$(pwd)/trimmed/05b_aud.mp4'
file '$(pwd)/trimmed/05c_aud.mp4'
file '$(pwd)/trimmed/06_aud.mp4'
file '$(pwd)/trimmed/07_aud.mp4'
file '$(pwd)/trimmed/08_aud.mp4'
file '$(pwd)/trimmed/09_1_aud.mp4'
file '$(pwd)/trimmed/09_2_aud.mp4'
file '$(pwd)/trimmed/09_3_aud.mp4'
file '$(pwd)/trimmed/10_aud.mp4'
EOF

# Need to normalise streams for safe concat
ffmpeg -y -hide_banner -loglevel error \
  -f concat -safe 0 -i /tmp/oliva_concat_aud.txt \
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
