"""Transform-search baseline for ARC-AGI-2.

Honesty: starter harness — geometric + tile + color-permutation search.
Not a claim of fluid AGI. Scores will be low until we grow the program library.
"""

from __future__ import annotations

from itertools import permutations
from typing import Any, Callable

from arc_prize.grids import (
    GEOMETRIC,
    Grid,
    Transform,
    colors_in,
    remap_colors,
    same,
    tile,
    tile_alt_flip_h,
    tile_checker,
)

Program = tuple[str, Transform]


def _color_bijection_programs(src: Grid, dst: Grid) -> list[Program]:
    """If shapes match, try color permutations that map src→dst on one pair."""
    if len(src) != len(dst) or (src and len(src[0]) != len(dst[0])):
        return []
    sc, dc = colors_in(src), colors_in(dst)
    if len(sc) != len(dc) or len(sc) > 5:
        return []
    out: list[Program] = []
    for perm in permutations(dc):
        mapping = dict(zip(sc, perm))
        if remap_colors(src, mapping) == dst:
            out.append((f"recolor:{mapping}", lambda g, m=mapping: remap_colors(g, m)))
            break
    return out


def _tile_programs(src: Grid, dst: Grid) -> list[Program]:
    sh, sw = len(src), len(src[0]) if src else 0
    dh, dw = len(dst), len(dst[0]) if dst else 0
    if not sh or not sw or dh % sh or dw % sw:
        return []
    ny, nx = dh // sh, dw // sw
    if nx > 6 or ny > 6:
        return []
    candidates: list[Program] = [
        (f"tile:{nx}x{ny}", lambda g, nx=nx, ny=ny: tile(g, nx, ny)),
        (f"tile_alt_flip_h:{nx}x{ny}", lambda g, nx=nx, ny=ny: tile_alt_flip_h(g, nx, ny)),
        (f"tile_checker:{nx}x{ny}", lambda g, nx=nx, ny=ny: tile_checker(g, nx, ny)),
    ]
    return candidates


def fit_program(train_pairs: list[dict[str, Any]]) -> Program | None:
    """Return first program that fits all training pairs."""
    if not train_pairs:
        return None
    first_in, first_out = train_pairs[0]["input"], train_pairs[0]["output"]
    library: list[Program] = list(GEOMETRIC)
    library.extend(_tile_programs(first_in, first_out))
    library.extend(_color_bijection_programs(first_in, first_out))

    # geometric then recolor
    for gname, gfn in GEOMETRIC:
        for cname, cfn in _color_bijection_programs(gfn(first_in), first_out):
            library.append(
                (
                    f"{gname}+{cname}",
                    lambda g, gfn=gfn, cfn=cfn: cfn(gfn(g)),
                )
            )

    for name, fn in library:
        try:
            if all(same(fn(p["input"]), p["output"]) for p in train_pairs):
                return name, fn
        except Exception:
            continue
    return None


def predict_task(task: dict[str, Any]) -> list[list[Grid]]:
    """Return submission-shaped attempts for each test item: [[{attempt_1, attempt_2}], ...]."""
    prog = fit_program(task.get("train", []))
    attempts: list[list[dict[str, Grid]]] = []
    for test_item in task.get("test", []):
        inp = test_item["input"]
        if prog is None:
            a1 = inp
            a2 = inp
        else:
            a1 = prog[1](inp)
            # second attempt: identity fallback if distinct
            a2 = inp if a1 != inp else (GEOMETRIC[1][1](inp))
        attempts.append([{"attempt_1": a1, "attempt_2": a2}])
    return attempts  # type: ignore[return-value]


def solve_challenges(challenges: dict[str, Any]) -> dict[str, Any]:
    submission: dict[str, Any] = {}
    for tid, task in challenges.items():
        # sample_submission shape: list of {attempt_1, attempt_2} per test item
        prog = fit_program(task.get("train", []))
        rows = []
        for test_item in task.get("test", []):
            inp = test_item["input"]
            if prog is None:
                a1, a2 = inp, inp
            else:
                a1 = prog[1](inp)
                a2 = inp if a1 != inp else GEOMETRIC[1][1](inp)
            rows.append({"attempt_1": a1, "attempt_2": a2})
        submission[tid] = rows
    return submission


def score_split(
    challenges: dict[str, Any], solutions: dict[str, Any]
) -> dict[str, float | int]:
    """Exact-match task accuracy (all test outputs correct on attempt_1)."""
    ok = 0
    total = 0
    for tid, task in challenges.items():
        total += 1
        prog = fit_program(task.get("train", []))
        gold = solutions[tid]
        preds = []
        for test_item in task["test"]:
            if prog is None:
                preds.append(test_item["input"])
            else:
                preds.append(prog[1](test_item["input"]))
        if preds == gold:
            ok += 1
    return {"solved": ok, "total": total, "accuracy": ok / total if total else 0.0}
