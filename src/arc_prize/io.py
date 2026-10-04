"""Load ARC-AGI-2 JSON dumps."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA = REPO_ROOT / "data" / "arc-agi-2"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def data_dir(root: Path | None = None) -> Path:
    return Path(root) if root else DEFAULT_DATA


def load_challenges(split: str, root: Path | None = None) -> dict[str, Any]:
    """split: training | evaluation | test"""
    name = {
        "training": "arc-agi_training_challenges.json",
        "evaluation": "arc-agi_evaluation_challenges.json",
        "test": "arc-agi_test_challenges.json",
    }[split]
    return load_json(data_dir(root) / name)


def load_solutions(split: str, root: Path | None = None) -> dict[str, Any]:
    name = {
        "training": "arc-agi_training_solutions.json",
        "evaluation": "arc-agi_evaluation_solutions.json",
    }[split]
    return load_json(data_dir(root) / name)


def load_sample_submission(root: Path | None = None) -> dict[str, Any]:
    return load_json(data_dir(root) / "sample_submission.json")
