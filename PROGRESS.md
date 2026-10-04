# Progress log — FractiAI ARC Prize 2026

Living status for Player 1. Newest first.

## 2026-10-04 — ARC_API_KEY accepted; AGI-3 smoke OK

### Done
- Configured `ARC_API_KEY` in local vendor `.env` (gitignored; not committed)
- `uv run main.py --agent=random --game=ls20` completed via three.arcprize.org
- Scorecard: https://arcprize.org/scorecards/dc651d43-585f-4893-bd8a-0382a2fb7bff (0 score — random baseline)

### Next
- Replace random agent with FractiAI policy agent
- Player 1 still needs one-click AGI-2 kernel Submit if not done

## 2026-10-04 — kernel ran on Kaggle; submit needs one UI click

### Done
- Pushed private kernel `prudenciomendez/fractiai-arc-agi-2-dsl-v1` (v2 **Complete**)
- Output: `submission.json` (240 tasks) on Kaggle working dir
- Plain-language explainer: `docs/WHAT_IS_A_KAGGLE_NOTEBOOK.md`

### Blocked
- `kaggle competitions submit -k …` → **403 CreateCodeSubmission** (limits show 1 remaining today)
- Player 1 must click **Submit to Competition** on the kernel page while logged in
- `ARC_API_KEY` still unset in agent env (Kaggle token ≠ ARC API key)

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
