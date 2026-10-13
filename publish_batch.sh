#!/usr/bin/env bash
# usage: publish_batch.sh NN [NN...]
# Copies raw plates from the local workspace (fg_final.png used as fg), builds each card into v2/deck,
# runs the frame QA for those cards, commits and pushes to GitHub Pages.
set -euo pipefail
REPO="$(cd "$(dirname "$0")" && pwd)"
SRC_RAW="${SRC_RAW:-/workspace/tarot-app/tecnotaro-parallax/v2/raw}"
[ $# -ge 1 ] || { echo "usage: $0 NN [NN...]"; exit 1; }
cd "$REPO"; git pull --rebase --autostash -q
built=()
for n in "$@"; do
  nn=$(printf %02d "$((10#$n))")
  d=$(ls -d "$SRC_RAW/$nn"-* 2>/dev/null | head -1) || true
  [ -n "$d" ] || { echo "no raw for $nn"; exit 1; }
  slug=$(basename "$d"); dst="v2/raw/$slug"; mkdir -p "$dst"
  for l in bg mid figure; do [ -f "$d/$l.png" ] && cp "$d/$l.png" "$dst/"; done
  if [ -f "$d/fg_final.png" ]; then cp "$d/fg_final.png" "$dst/fg.png"; elif [ -f "$d/fg.png" ]; then cp "$d/fg.png" "$dst/"; fi
  for x in frame.png depth.json; do [ -f "$d/$x" ] && cp "$d/$x" "$dst/"; done
  python3 v2/src/v2_build_card.py "$((10#$nn))" --force --key auto --root v2
  built+=("$((10#$nn))")
done
PORT=${PORT:-8931}
python3 -m http.server $PORT --bind 127.0.0.1 >/dev/null 2>&1 & SP=$!; trap 'kill $SP 2>/dev/null' EXIT; sleep 1
for i in "${built[@]}"; do python3 tools/frame_qa.py "http://127.0.0.1:$PORT/v2" v2/deck "$i-$i" | tee -a /tmp/frame-qa-batch.txt; done
git add v2 publish_batch.sh
git commit -qm "v2: publish real layers for cards $*"
git push -q
echo "Live: https://alexandrerangel.github.io/tecnotaro-parallax-test/v2/#${built[0]}"
