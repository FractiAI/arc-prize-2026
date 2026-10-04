#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENDOR="$ROOT/vendor/ARC-AGI-3-Agents"
SRC="$ROOT/agi3/fracti_explore.py"
[[ -d "$VENDOR/agents/templates" ]] || { echo "Run ./scripts/setup_agi3.sh first" >&2; exit 1; }
cp "$SRC" "$VENDOR/agents/templates/fracti_explore.py"
python3 - <<PY
from pathlib import Path
p = Path("$VENDOR/agents/__init__.py")
text = p.read_text()
if "FractiExplore" not in text:
    text = text.replace(
        "from .templates.random_agent import Random",
        "from .templates.random_agent import Random\nfrom .templates.fracti_explore import FractiExplore",
    )
    text = text.replace('"Random",', '"Random",\n    "FractiExplore",')
    p.write_text(text)
    print("patched", p)
else:
    print("already patched", p)
PY
echo "OK — uv run main.py --agent=fractiexplore --game=ls20"
