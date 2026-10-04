"""CLI entrypoints for download / eval / submission build."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from arc_prize.io import REPO_ROOT, load_challenges, load_solutions
from arc_prize.solver import score_split, solve_challenges


def download_main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Download ARC Prize 2026 datasets")
    parser.add_argument(
        "--tracks",
        nargs="+",
        default=["arc-agi-2", "paper-track"],
        choices=["arc-agi-2", "paper-track"],
    )
    args = parser.parse_args(argv)
    script = REPO_ROOT / "scripts" / "download_data.sh"
    cmd = ["bash", str(script), *args.tracks]
    raise SystemExit(subprocess.call(cmd))


def eval_main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Evaluate transform-search baseline")
    parser.add_argument(
        "--split",
        default="training",
        choices=["training", "evaluation"],
    )
    parser.add_argument("--data-root", type=Path, default=None)
    args = parser.parse_args(argv)
    challenges = load_challenges(args.split, args.data_root)
    solutions = load_solutions(args.split, args.data_root)
    result = score_split(challenges, solutions)
    print(json.dumps({"split": args.split, **result}, indent=2))


def build_submission_main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Build ARC-AGI-2 submission JSON")
    parser.add_argument(
        "--split",
        default="test",
        choices=["test", "evaluation", "training"],
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=REPO_ROOT / "submissions" / "submission.json",
    )
    parser.add_argument("--data-root", type=Path, default=None)
    args = parser.parse_args(argv)
    challenges = load_challenges(args.split, args.data_root)
    submission = solve_challenges(challenges)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(submission), encoding="utf-8")
    print(f"wrote {args.out} ({len(submission)} tasks)")


if __name__ == "__main__":
    # python -m arc_prize.cli eval|build|download
    if len(sys.argv) < 2:
        print("usage: python -m arc_prize.cli [download|eval|build] ...", file=sys.stderr)
        raise SystemExit(2)
    cmd, rest = sys.argv[1], sys.argv[2:]
    {"download": download_main, "eval": eval_main, "build": build_submission_main}[cmd](rest)
