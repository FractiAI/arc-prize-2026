#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
"$ROOT/scripts/setup_agi3.sh" >/dev/null
"$ROOT/scripts/install_agi3_agent.sh"
cd "$ROOT/vendor/ARC-AGI-3-Agents"
GAMES="${1:-ls20,vc33,su15,lp85,sp80,re86,wa30,ka59,lf52,s5i5}"
export PATH="$HOME/.local/bin:$PATH"
uv run main.py --agent=fractiexplore --game="$GAMES"
