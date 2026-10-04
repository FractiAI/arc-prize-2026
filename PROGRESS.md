# Progress log — FractiAI ARC Prize 2026

Living status for Player 1. Newest first.

## 2026-10-04 — harness v1 (solver grow + notebook + AGI-3 setup)

### Done
- Standalone repo created: https://github.com/FractiAI/arc-prize-2026
- Joined all three Kaggle tracks (AGI-2 · AGI-3 · Paper)
- ARC-AGI-2 DSL expanded: geometry · tile variants · upscale · gravity · crop · recolor · short compositions
- Dual-attempt submission (attempt_1 / attempt_2 from top fitting programs)
- Kaggle Notebook source: `notebooks/arc_agi_2_submit.py` (+ `notebooks/README.md`)
- AGI-3 setup script: `scripts/setup_agi3.sh` (clones official kit; needs `ARC_API_KEY`)
- Paper outline: `paper/DRAFT_OUTLINE.md`

### Scores (exact task match on public splits)
| Split | Before (v0) | After (v1) |
|---|---|---|
| training | 18/1000 (1.8%) | **30/1000 (3.0%)** |
| evaluation | 0/120 (0%) | **0/120 (0%)** |

### Blocked / next
- [ ] Kaggle Notebook submit of AGI-2 (CLI submit 403 — Code Competition)
- [ ] `ARC_API_KEY` from https://three.arcprize.org/ for live AGI-3 agent runs
- [ ] Grow DSL / object-centric priors toward eval > 0
- [ ] Paper-track draft → PDF checklist

### Honesty
Public-split exact match ≠ private leaderboard. Catalog Soft Story ≠ ARC proof.
