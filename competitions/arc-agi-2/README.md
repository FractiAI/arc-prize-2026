# ARC Prize 2026 — ARC-AGI-2

- Competition: https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2
- Deadline: 2026-11-02
- Purse: $700,000
- Format: JSON grid puzzles · 2 attempts per test item

## Local loop

```bash
./scripts/download_data.sh arc-agi-2
python -m arc_prize.cli eval --split training
python -m arc_prize.cli eval --split evaluation
./scripts/submit_arc_agi_2.sh "message"
```

## Honesty

Baseline is transform search (geometry · tile · recolor). Useful for plumbing + first board score — not a fluid-intelligence claim.
