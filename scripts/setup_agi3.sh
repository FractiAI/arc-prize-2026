#!/usr/bin/env bash
# Clone / refresh official ARC-AGI-3 agent kit and verify ARC_API_KEY.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENDOR="$ROOT/vendor/ARC-AGI-3-Agents"

if [[ ! -d "$VENDOR/.git" ]]; then
  mkdir -p "$ROOT/vendor"
  rm -rf "$VENDOR"
  git clone --depth 1 https://github.com/arcprize/ARC-AGI-3-Agents.git "$VENDOR"
else
  git -C "$VENDOR" pull --ff-only || true
fi

if [[ ! -f "$VENDOR/.env" ]]; then
  cp "$VENDOR/.env.example" "$VENDOR/.env"
  echo "Created $VENDOR/.env — set ARC_API_KEY from https://three.arcprize.org/"
fi

if [[ -n "${ARC_API_KEY:-}" ]]; then
  # inject without printing
  if grep -q '^ARC_API_KEY=' "$VENDOR/.env"; then
    sed -i "s|^ARC_API_KEY=.*|ARC_API_KEY=${ARC_API_KEY}|" "$VENDOR/.env"
  else
    echo "ARC_API_KEY=${ARC_API_KEY}" >> "$VENDOR/.env"
  fi
  echo "ARC_API_KEY present in vendor .env"
else
  if grep -q '^ARC_API_KEY=your_arc_api_key_here' "$VENDOR/.env" 2>/dev/null || \
     grep -q '^ARC_API_KEY=$' "$VENDOR/.env" 2>/dev/null; then
    echo "WARNING: ARC_API_KEY not set. Get one at https://three.arcprize.org/" >&2
  else
    echo "ARC_API_KEY appears configured in vendor .env"
  fi
fi

echo "Next:"
echo "  cd $VENDOR"
echo "  # install uv if needed: https://docs.astral.sh/uv/"
echo "  uv sync"
echo "  uv run main.py --agent=random --game=ls20"
