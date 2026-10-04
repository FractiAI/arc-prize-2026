# ARC Prize 2026 — FractiAI

Standalone competition repo for **ARC-AGI-2**, **ARC-AGI-3**, and the **Paper track**.  
Not part of `psw.vibelandia.sing13` (SING 13). Operator: SynthOBS / FractiAI · Player 1 creator seat.

**Repo:** https://github.com/FractiAI/arc-prize-2026

| Track | Kaggle | Status |
|---|---|---|
| ARC-AGI-2 | [arc-prize-2026-arc-agi-2](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2) | Joined · code lane |
| ARC-AGI-3 | [arc-prize-2026-arc-agi-3](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3) | Joined · agent lane (`ARC_API_KEY`) |
| Paper track | [arc-prize-2026-paper-track](https://www.kaggle.com/competitions/arc-prize-2026-paper-track) | Joined · writeup lane |

## Progress (2026-10-04)

Living detail: [`PROGRESS.md`](PROGRESS.md)

| Milestone | State |
|---|---|
| Own GitHub repo | **done** — `FractiAI/arc-prize-2026` |
| Kaggle joins (2 · 3 · paper) | **done** |
| Download / eval / build CLI | **done** |
| DSL solver v1 (tile · upscale · gravity · crop · recolor) | **done** |
| Training exact-match | **30 / 1000 (3.0%)** ← was 1.8% |
| Evaluation exact-match | **0 / 120 (0%)** |
| Kaggle Notebook submit source | **done** — `notebooks/arc_agi_2_submit.py` |
| AGI-3 official kit setup script | **done** — `scripts/setup_agi3.sh` |
| Live AGI-3 agent run | **blocked** — need `ARC_API_KEY` from [three.arcprize.org](https://three.arcprize.org/) |
| Leaderboard submit (AGI-2) | **next** — upload Notebook (CLI submit returned 403) |
| Paper PDF | **outline only** |

### Next up
1. Submit AGI-2 via Kaggle Notebook (`notebooks/README.md`)
2. Set `ARC_API_KEY` and run `./scripts/setup_agi3.sh` + random agent smoke
3. Grow DSL / object priors until evaluation > 0
4. Draft paper body from `paper/DRAFT_OUTLINE.md`

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Kaggle auth (prefer file; never commit the token)
mkdir -p ~/.kaggle
echo "$KAGGLE_API_TOKEN" > ~/.kaggle/access_token
chmod 600 ~/.kaggle/access_token

./scripts/download_data.sh
```

## Evaluate

```bash
PYTHONPATH=src python3 -m arc_prize.cli eval --split training
PYTHONPATH=src python3 -m arc_prize.cli eval --split evaluation
```

## Submit ARC-AGI-2 (Notebook — preferred)

See [`notebooks/README.md`](notebooks/README.md). Code Competitions reject direct CLI file upload (403 observed).

CLI build (local JSON only):

```bash
PYTHONPATH=src python3 -m arc_prize.cli build --split test --out submissions/submission.json
```

## ARC-AGI-3

```bash
export ARC_API_KEY=...   # from https://three.arcprize.org/
./scripts/setup_agi3.sh
cd vendor/ARC-AGI-3-Agents && uv sync && uv run main.py --agent=random --game=ls20
```

Kaggle token ≠ ARC API key. Both are required for the full AGI-3 loop.

## Layout

```
src/arc_prize/          # loaders · DSL solver · CLI
notebooks/              # Kaggle Code Competition submit source
competitions/           # per-track notes
paper/                  # paper-track draft outline
scripts/                # download · submit · AGI-3 setup
data/                   # local dumps (gitignored JSON)
vendor/                 # official AGI-3 kit (gitignored)
PROGRESS.md             # dated progress log
```

## Honesty

DSL transform search is plumbing + a public-split score.  
Catalog keys (Φ_EGS · Infinite Octaves · Soft Story) are **not** ARC proofs. SuperAI Layer language from SING 13 stays a composition template — not claimed AGI.

→ ∞^∞
