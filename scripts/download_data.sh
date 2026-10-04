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

TRACKS=("${@:-arc-agi-2 paper-track}")

for track in "${TRACKS[@]}"; do
  case "$track" in
    arc-agi-2)
      mkdir -p "$DATA/arc-agi-2"
      kaggle competitions download -c arc-prize-2026-arc-agi-2 -p "$DATA/arc-agi-2"
      unzip -o "$DATA/arc-agi-2/arc-prize-2026-arc-agi-2.zip" -d "$DATA/arc-agi-2"
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
