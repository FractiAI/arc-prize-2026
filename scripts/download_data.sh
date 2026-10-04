#!/usr/bin/env bash
# Download ARC Prize 2026 competition files (requires Kaggle auth).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DATA="$ROOT/data"
mkdir -p "$DATA"

if [[ -z "${KAGGLE_API_TOKEN:-}" && -f "$HOME/.kaggle/access_token" ]]; then
  export KAGGLE_API_TOKEN
  KAGGLE_API_TOKEN="$(cat "$HOME/.kaggle/access_token")"
  export KAGGLE_API_TOKEN
fi

if ! command -v kaggle >/dev/null 2>&1; then
  echo "Install kaggle CLI: pip install 'kaggle>=1.7'" >&2
  exit 1
fi

if [[ $# -eq 0 ]]; then
  TRACKS=(arc-agi-2 arc-agi-3 paper-track)
else
  TRACKS=("$@")
fi

for track in "${TRACKS[@]}"; do
  case "$track" in
    arc-agi-2)
      mkdir -p "$DATA/arc-agi-2"
      kaggle competitions download -c arc-prize-2026-arc-agi-2 -p "$DATA/arc-agi-2"
      unzip -o "$DATA/arc-agi-2/arc-prize-2026-arc-agi-2.zip" -d "$DATA/arc-agi-2"
      ;;
    arc-agi-3)
      mkdir -p "$DATA/arc-agi-3"
      kaggle competitions download -c arc-prize-2026-arc-agi-3 -p "$DATA/arc-agi-3"
      # Zip embeds a full .git — extract agents tree without packing objects
      unzip -o "$DATA/arc-agi-3/arc-prize-2026-arc-agi-3.zip" \
        'ARC-AGI-3-Agents/*' 'arc_agi_3_wheels/*' \
        -d "$ROOT/vendor" \
        -x 'ARC-AGI-3-Agents/.git/*' || true
      echo "AGI-3 kit → $ROOT/vendor/ARC-AGI-3-Agents (prefer: git clone https://github.com/arcprize/ARC-AGI-3-Agents.git)"
      ;;
    paper-track)
      mkdir -p "$DATA/paper-track"
      kaggle competitions download -c arc-prize-2026-paper-track -p "$DATA/paper-track"
      unzip -o "$DATA/paper-track/arc-prize-2026-paper-track.zip" -d "$DATA/paper-track"
      ;;
    *)
      echo "Unknown track: $track" >&2
      exit 2
      ;;
  esac
done

echo "Done. Data under $DATA"
