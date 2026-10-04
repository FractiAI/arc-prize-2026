"""Transform-search solver for ARC-AGI-2.

Honesty: growing DSL / program library — not fluid AGI.
Reports exact-match task accuracy on public splits only.
"""

from __future__ import annotations

from itertools import permutations
from typing import Any

from arc_prize.grids import (
    GEOMETRIC,
    Grid,
    Transform,
    colors_in,
    crop_to_content,
    gravity,
    majority_color,
    remap_colors,
    replace_color,
    same,
    tile,
    tile_alt_flip_h,
    tile_alt_flip_v,
    tile_checker,
    upscale,
)

Program = tuple[str, Transform]


def _fits(fn: Transform, train_pairs: list[dict[str, Any]]) -> bool:
    try:
        return all(same(fn(p["input"]), p["output"]) for p in train_pairs)
    except Exception:
        return False


def _color_bijection_programs(src: Grid, dst: Grid) -> list[Program]:
    if len(src) != len(dst) or (src and len(src[0]) != len(dst[0])):
        return []
    sc, dc = colors_in(src), colors_in(dst)
    if len(sc) != len(dc) or len(sc) == 0 or len(sc) > 6:
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
    if nx > 8 or ny > 8:
        return []
    return [
        (f"tile:{nx}x{ny}", lambda g, nx=nx, ny=ny: tile(g, nx, ny)),
        (f"tile_alt_flip_h:{nx}x{ny}", lambda g, nx=nx, ny=ny: tile_alt_flip_h(g, nx, ny)),
        (f"tile_alt_flip_v:{nx}x{ny}", lambda g, nx=nx, ny=ny: tile_alt_flip_v(g, nx, ny)),
        (f"tile_checker:{nx}x{ny}", lambda g, nx=nx, ny=ny: tile_checker(g, nx, ny)),
    ]


def _upscale_programs(src: Grid, dst: Grid) -> list[Program]:
    sh, sw = len(src), len(src[0]) if src else 0
    dh, dw = len(dst), len(dst[0]) if dst else 0
    if not sh or not sw or dh % sh or dw % sw:
        return []
    ky, kx = dh // sh, dw // sw
    if kx != ky or kx < 2 or kx > 5:
        return []
    k = kx
    return [(f"upscale:{k}", lambda g, k=k: upscale(g, k))]


def _gravity_programs() -> list[Program]:
    out: list[Program] = []
    for d in ("down", "up", "left", "right"):
        out.append((f"gravity:{d}", lambda g, d=d: gravity(g, d, bg=0)))
        # also try majority-as-bg
        out.append(
            (
                f"gravity:{d}:majbg",
                lambda g, d=d: gravity(g, d, bg=majority_color(g)),
            )
        )
    return out


def _crop_programs() -> list[Program]:
    return [
        ("crop0", lambda g: crop_to_content(g, 0)),
        ("crop_maj", lambda g: crop_to_content(g, majority_color(g))),
    ]


def _single_recolor_programs(src: Grid, dst: Grid) -> list[Program]:
    """src→dst when exactly one color changes and shapes match."""
    if len(src) != len(dst) or (src and len(src[0]) != len(dst[0])):
        return []
    diffs: dict[tuple[int, int], int] = {}
    for r, row in enumerate(src):
        for c, v in enumerate(row):
            if v != dst[r][c]:
                diffs[(v, dst[r][c])] = diffs.get((v, dst[r][c]), 0) + 1
    if len(diffs) != 1:
        return []
    (a, b), _ = next(iter(diffs.items()))
    return [(f"replace:{a}->{b}", lambda g, a=a, b=b: replace_color(g, a, b))]


def candidate_programs(train_pairs: list[dict[str, Any]]) -> list[Program]:
    first_in, first_out = train_pairs[0]["input"], train_pairs[0]["output"]
    library: list[Program] = list(GEOMETRIC)
    library.extend(_tile_programs(first_in, first_out))
    library.extend(_upscale_programs(first_in, first_out))
    library.extend(_gravity_programs())
    library.extend(_crop_programs())
    library.extend(_color_bijection_programs(first_in, first_out))
    library.extend(_single_recolor_programs(first_in, first_out))

    # geometric ∘ recolor / upscale ∘ geometric
    for gname, gfn in GEOMETRIC:
        for cname, cfn in _color_bijection_programs(gfn(first_in), first_out):
            library.append((f"{gname}+{cname}", lambda g, gfn=gfn, cfn=cfn: cfn(gfn(g))))
        for uname, ufn in _upscale_programs(gfn(first_in), first_out):
            library.append((f"{gname}+{uname}", lambda g, gfn=gfn, ufn=ufn: ufn(gfn(g))))
        for tname, tfn in _tile_programs(gfn(first_in), first_out):
            library.append((f"{gname}+{tname}", lambda g, gfn=gfn, tfn=tfn: tfn(gfn(g))))

    # crop then geometric
    for cname, cfn in _crop_programs():
        cropped = cfn(first_in)
        for gname, gfn in GEOMETRIC:
            if same(gfn(cropped), first_out):
                library.append(
                    (f"{cname}+{gname}", lambda g, cfn=cfn, gfn=gfn: gfn(cfn(g)))
                )

    # gravity then geometric
    for gvname, gvfn in _gravity_programs():
        moved = gvfn(first_in)
        for gname, gfn in GEOMETRIC:
            if same(gfn(moved), first_out):
                library.append(
                    (f"{gvname}+{gname}", lambda g, gvfn=gvfn, gfn=gfn: gfn(gvfn(g)))
                )

    return library


def fit_programs(train_pairs: list[dict[str, Any]], limit: int = 8) -> list[Program]:
    """Return up to `limit` programs that fit all training pairs."""
    if not train_pairs:
        return []
    found: list[Program] = []
    seen: set[str] = set()
    for name, fn in candidate_programs(train_pairs):
        if name in seen:
            continue
        if _fits(fn, train_pairs):
            found.append((name, fn))
            seen.add(name)
            if len(found) >= limit:
                break
    return found


def fit_program(train_pairs: list[dict[str, Any]]) -> Program | None:
    found = fit_programs(train_pairs, limit=1)
    return found[0] if found else None


def _attempts_for_input(inp: Grid, programs: list[Program]) -> dict[str, Grid]:
    if not programs:
        return {"attempt_1": inp, "attempt_2": inp}
    a1 = programs[0][1](inp)
    if len(programs) > 1:
        a2 = programs[1][1](inp)
    else:
        a2 = inp if a1 != inp else GEOMETRIC[1][1](inp)
    return {"attempt_1": a1, "attempt_2": a2}


def solve_challenges(challenges: dict[str, Any]) -> dict[str, Any]:
    submission: dict[str, Any] = {}
    for tid, task in challenges.items():
        programs = fit_programs(task.get("train", []), limit=2)
        rows = [_attempts_for_input(t["input"], programs) for t in task.get("test", [])]
        submission[tid] = rows
    return submission


def score_split(
    challenges: dict[str, Any], solutions: dict[str, Any]
) -> dict[str, float | int]:
    """Exact-match task accuracy (all test outputs correct on attempt_1 or attempt_2)."""
    ok = 0
    ok_a1 = 0
    total = 0
    for tid, task in challenges.items():
        total += 1
        programs = fit_programs(task.get("train", []), limit=2)
        gold = solutions[tid]
        preds_a1 = []
        preds_a2 = []
        for test_item in task["test"]:
            att = _attempts_for_input(test_item["input"], programs)
            preds_a1.append(att["attempt_1"])
            preds_a2.append(att["attempt_2"])
        if preds_a1 == gold:
            ok += 1
            ok_a1 += 1
        elif preds_a2 == gold:
            ok += 1
    return {
        "solved": ok,
        "solved_attempt_1": ok_a1,
        "total": total,
        "accuracy": ok / total if total else 0.0,
    }
