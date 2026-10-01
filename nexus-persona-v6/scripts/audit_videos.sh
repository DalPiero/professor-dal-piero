#!/usr/bin/env bash
# Auditoria local sem IA nem reconhecimento facial. Requer ffmpeg e ffprobe.
set -euo pipefail
if [[ $# -ne 2 ]]; then echo "USO: bash audit_videos.sh video1.mp4 video2.mp4" >&2; exit 2; fi
for bin in ffmpeg ffprobe; do command -v "$bin" >/dev/null || { echo "Falta: $bin" >&2; exit 2; }; done
out="${PWD}/AUDITORIA_NEXUS_PERSONA"
mkdir -p "$out"
for i in 1 2; do
  file="${!i}"; test -s "$file" || { echo "Arquivo não encontrado: $file" >&2; exit 2; }
  dst="$out/filme_$i"; mkdir -p "$dst"
  ffprobe -v error -show_format -show_streams -of json "$file" > "$dst/metadados.json"
  ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$file" | tr -d '\r' > "$dst/duracao.txt"
  duration=$(cat "$dst/duracao.txt")
  python3 - "$duration" "$dst" <<'PY'
import sys
dur=float(sys.argv[1]);folder=sys.argv[2]
open(folder+'/amostras.txt','w').write('\n'.join('%.3f'%(dur*x) for x in (.05,.2,.35,.5,.65,.8,.95)))
PY
  n=0
  while IFS= read -r t; do
    n=$((n+1))
    ffmpeg -hide_banner -loglevel error -ss "$t" -i "$file" -frames:v 1 -vf "scale=640:-2" -y "$dst/quadro_$(printf '%02d' "$n").jpg" 
  done < "$dst/amostras.txt"
  ffmpeg -hide_banner -i "$file" -vn -af volumedetect -f null - 2> "$dst/volume.log" || true
  ffmpeg -hide_banner -i "$file" -vf "blackdetect=d=0.35:pix_th=0.12" -an -f null - 2> "$dst/blackdetect.log" || true
done
echo "Auditoria técnica salva em $out. Inspecione os sete quadros de cada filme e escute os vídeos para avaliar o lip sync real."
