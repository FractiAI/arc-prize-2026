# ARC Prize 2026 — FractiAI

Standalone competition repo for **ARC-AGI-2** + **Paper track**.  
Not part of `psw.vibelandia.sing13` (SING 13). Operator: SynthOBS / FractiAI · Player 1 creator seat.

| Track | Kaggle | Status |
|---|---|---|
| ARC-AGI-2 | [arc-prize-2026-arc-agi-2](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2) | Joined · code lane |
| ARC-AGI-3 | [arc-prize-2026-arc-agi-3](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3) | Joined · agent lane (`ARC_API_KEY` from three.arcprize.org) |
| Paper track | [arc-prize-2026-paper-track](https://www.kaggle.com/competitions/arc-prize-2026-paper-track) | Joined · writeup lane |

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Auth (prefer file; never commit the token)
mkdir -p ~/.kaggle
echo "$KAGGLE_API_TOKEN" > ~/.kaggle/access_token
chmod 600 ~/.kaggle/access_token

./scripts/download_data.sh
```

## Evaluate baseline

```bash
python -m arc_prize.cli eval --split training
python -m arc_prize.cli eval --split evaluation
```

## Submit ARC-AGI-2

```bash
./scripts/submit_arc_agi_2.sh "FractiAI baseline v0"
```

## Layout

```
src/arc_prize/          # loaders · transform-search solver · CLI
competitions/           # per-track notes
paper/                  # paper-track draft outline
scripts/                # download + submit
data/                   # local dumps (gitignored JSON)
submissions/            # generated (gitignored)
```

## Honesty

Transform-search baseline is plumbing + a first leaderboard number.  
Catalog keys (Φ_EGS · Infinite Octaves · Soft Story) are **not** ARC proofs. SuperAI Layer language from SING 13 stays a composition template — not claimed AGI.

→ ∞^∞
