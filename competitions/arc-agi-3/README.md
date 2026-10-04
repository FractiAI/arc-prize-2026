# ARC Prize 2026 — ARC-AGI-3

- Competition: https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3
- Agent docs: https://three.arcprize.org/docs
- Official kit: https://github.com/arcprize/ARC-AGI-3-Agents
- Deadline: 2026-11-02
- Purse: $850,000

## Auth (two keys — do not mix)

| Key | Where | Purpose |
|---|---|---|
| `KAGGLE_API_TOKEN` | Kaggle settings | Download competition zip / Kaggle submit |
| `ARC_API_KEY` | https://three.arcprize.org/ | Live ARC-AGI-3 agent API |

The Kaggle token alone cannot drive the AGI-3 agent loop.

## Local loop

```bash
./scripts/download_data.sh arc-agi-3
# Prefer cloning the official kit (keeps us on upstream):
git clone https://github.com/arcprize/ARC-AGI-3-Agents.git vendor/ARC-AGI-3-Agents
cd vendor/ARC-AGI-3-Agents
cp .env.example .env
# set ARC_API_KEY=... in .env
uv run main.py --agent=random --game=ls20
```

A partial extract may already exist under `vendor/ARC-AGI-3-Agents/` from the Kaggle zip (gitignored zip; vendor may be local-only). Prefer the GitHub clone for day-to-day work.

## Honesty

Random / template agents are plumbing. FractiAI custom agents will live under `src/arc_prize/agi3/` when we grow past the starter kit — still measured by ARC-AGI-3 scores, not catalog Soft Story.
