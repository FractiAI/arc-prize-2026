#!/usr/bin/env bash
# Build + submit ARC-AGI-2 prediction file.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ -z "${KAGGLE_API_TOKEN:-}" && -f "$HOME/.kaggle/access_token" ]]; then
  KAGGLE_API_TOKEN="$(cat "$HOME/.kaggle/access_token")"
  export KAGGLE_API_TOKEN
fi

python -m arc_prize.cli build --split test --out "$ROOT/submissions/submission.json"
MSG="${1:-FractiAI transform-search baseline}"
kaggle competitions submit \
  -c arc-prize-2026-arc-agi-2 \
  -f "$ROOT/submissions/submission.json" \
  -m "$MSG"
echo "Submitted. Check: kaggle competitions submissions -c arc-prize-2026-arc-agi-2"
