"""
Kaggle Code Competition notebook (Python source).

Upload to Kaggle → New Notebook → attach competition
`arc-prize-2026-arc-agi-2` → Save Version → Submit.

Or paste cells from this file into a notebook. Paths assume Kaggle input mount.
"""

from __future__ import annotations

import json
from itertools import permutations
from pathlib import Path
from typing import Any, Callable

# --- inline minimal solver (self-contained for Kaggle; keep in sync with src/) ---

Grid = list[list[int]]
Transform = Callable[[Grid], Grid]


def copy_grid(g: Grid) -> Grid:
    return [row[:] for row in g]


def same(a: Grid, b: Grid) -> bool:
    return a == b


def rot90(g: Grid) -> Grid:
    return [list(row) for row in zip(*g[::-1])]


def rot180(g: Grid) -> Grid:
    return rot90(rot90(g))


def rot270(g: Grid) -> Grid:
    return rot90(rot90(rot90(g)))


def flip_h(g: Grid) -> Grid:
    return [row[::-1] for row in g]


def flip_v(g: Grid) -> Grid:
    return g[::-1]


def transpose(g: Grid) -> Grid:
    return [list(row) for row in zip(*g)]


def identity(g: Grid) -> Grid:
    return copy_grid(g)


def tile(g: Grid, nx: int, ny: int) -> Grid:
    out: Grid = []
    for _ in range(ny):
        for row in g:
            out.append(row * nx)
    return out


def tile_alt_flip_h(g: Grid, nx: int, ny: int) -> Grid:
    rows_out: Grid = []
    h = len(g)
    for by in range(ny):
        block = flip_h(g) if by % 2 else identity(g)
        for r in range(h):
            rows_out.append(block[r] * nx)
    return rows_out


def tile_alt_flip_v(g: Grid, nx: int, ny: int) -> Grid:
    rows_out: Grid = []
    h = len(g)
    for by in range(ny):
        for r in range(h):
            row: list[int] = []
            for bx in range(nx):
                block = flip_v(g) if bx % 2 else identity(g)
                row.extend(block[r])
            rows_out.append(row)
    return rows_out


def tile_checker(g: Grid, nx: int, ny: int) -> Grid:
    fns = [
        [identity, flip_h, identity],
        [flip_v, rot180, flip_v],
        [identity, flip_h, identity],
    ]
    rows_out: Grid = []
    h = len(g)
    for by in range(ny):
        for r in range(h):
            row: list[int] = []
            for bx in range(nx):
                row.extend(fns[by % 3][bx % 3](g)[r])
            rows_out.append(row)
    return rows_out


def upscale(g: Grid, k: int) -> Grid:
    out: Grid = []
    for row in g:
        expanded = []
        for v in row:
            expanded.extend([v] * k)
        for _ in range(k):
            out.append(expanded[:])
    return out


def gravity(g: Grid, direction: str = "down", bg: int = 0) -> Grid:
    h, w = len(g), len(g[0]) if g else 0
    out = [[bg for _ in range(w)] for _ in range(h)]
    if direction in ("down", "up"):
        for c in range(w):
            vals = [g[r][c] for r in range(h) if g[r][c] != bg]
            if direction == "down":
                start = h - len(vals)
                for i, v in enumerate(vals):
                    out[start + i][c] = v
            else:
                for i, v in enumerate(vals):
                    out[i][c] = v
    else:
        for r in range(h):
            vals = [g[r][c] for c in range(w) if g[r][c] != bg]
            if direction == "right":
                start = w - len(vals)
                for i, v in enumerate(vals):
                    out[r][start + i] = v
            else:
                for i, v in enumerate(vals):
                    out[r][i] = v
    return out


def crop_to_content(g: Grid, bg: int = 0) -> Grid:
    coords = [(r, c) for r, row in enumerate(g) for c, v in enumerate(row) if v != bg]
    if not coords:
        return copy_grid(g)
    rs = [r for r, _ in coords]
    cs = [c for _, c in coords]
    return [row[min(cs) : max(cs) + 1] for row in g[min(rs) : max(rs) + 1]]


def remap_colors(g: Grid, mapping: dict[int, int]) -> Grid:
    return [[mapping.get(v, v) for v in row] for row in g]


def replace_color(g: Grid, src: int, dst: int) -> Grid:
    return [[dst if v == src else v for v in row] for row in g]


def colors_in(g: Grid) -> list[int]:
    seen: set[int] = set()
    ordered: list[int] = []
    for row in g:
        for v in row:
            if v not in seen:
                seen.add(v)
                ordered.append(v)
    return ordered


def majority_color(g: Grid) -> int:
    counts: dict[int, int] = {}
    for row in g:
        for v in row:
            counts[v] = counts.get(v, 0) + 1
    return max(counts, key=counts.get) if counts else 0


GEOMETRIC = [
    ("identity", identity),
    ("rot90", rot90),
    ("rot180", rot180),
    ("rot270", rot270),
    ("flip_h", flip_h),
    ("flip_v", flip_v),
    ("transpose", transpose),
]


def _fits(fn, train_pairs):
    try:
        return all(same(fn(p["input"]), p["output"]) for p in train_pairs)
    except Exception:
        return False


def candidate_programs(train_pairs):
    first_in, first_out = train_pairs[0]["input"], train_pairs[0]["output"]
    lib = list(GEOMETRIC)
    sh, sw = len(first_in), len(first_in[0]) if first_in else 0
    dh, dw = len(first_out), len(first_out[0]) if first_out else 0
    if sh and sw and dh % sh == 0 and dw % sw == 0:
        ny, nx = dh // sh, dw // sw
        if nx <= 8 and ny <= 8:
            lib += [
                (f"tile:{nx}x{ny}", lambda g, nx=nx, ny=ny: tile(g, nx, ny)),
                (f"tile_alt_flip_h:{nx}x{ny}", lambda g, nx=nx, ny=ny: tile_alt_flip_h(g, nx, ny)),
                (f"tile_alt_flip_v:{nx}x{ny}", lambda g, nx=nx, ny=ny: tile_alt_flip_v(g, nx, ny)),
                (f"tile_checker:{nx}x{ny}", lambda g, nx=nx, ny=ny: tile_checker(g, nx, ny)),
            ]
        if nx == ny and 2 <= nx <= 5:
            k = nx
            lib.append((f"upscale:{k}", lambda g, k=k: upscale(g, k)))
    for d in ("down", "up", "left", "right"):
        lib.append((f"gravity:{d}", lambda g, d=d: gravity(g, d, 0)))
    lib.append(("crop0", lambda g: crop_to_content(g, 0)))
    sc, dc = colors_in(first_in), colors_in(first_out)
    if len(first_in) == len(first_out) and first_in and len(first_in[0]) == len(first_out[0]):
        if 0 < len(sc) == len(dc) <= 6:
            for perm in permutations(dc):
                mapping = dict(zip(sc, perm))
                if remap_colors(first_in, mapping) == first_out:
                    lib.append((f"recolor:{mapping}", lambda g, m=mapping: remap_colors(g, m)))
                    break
    for gname, gfn in GEOMETRIC:
        gin = gfn(first_in)
        if sh and sw and len(first_out) % len(gin) == 0 and len(first_out[0]) % len(gin[0]) == 0:
            ny, nx = len(first_out) // len(gin), len(first_out[0]) // len(gin[0])
            if nx <= 8 and ny <= 8:
                lib.append((f"{gname}+tile:{nx}x{ny}", lambda g, gfn=gfn, nx=nx, ny=ny: tile(gfn(g), nx, ny)))
    return lib


def fit_programs(train_pairs, limit=2):
    found = []
    for name, fn in candidate_programs(train_pairs):
        if _fits(fn, train_pairs):
            found.append((name, fn))
            if len(found) >= limit:
                break
    return found


def solve_challenges(challenges: dict[str, Any]) -> dict[str, Any]:
    submission = {}
    for tid, task in challenges.items():
        programs = fit_programs(task.get("train", []), limit=2)
        rows = []
        for test_item in task.get("test", []):
            inp = test_item["input"]
            if not programs:
                a1 = a2 = inp
            else:
                a1 = programs[0][1](inp)
                a2 = programs[1][1](inp) if len(programs) > 1 else (inp if a1 != inp else rot90(inp))
            rows.append({"attempt_1": a1, "attempt_2": a2})
        submission[tid] = rows
    return submission


def _find_data_dir() -> Path:
    """Locate arc-agi_test_challenges.json on Kaggle or locally."""
    named = [
        Path("/kaggle/input/arc-prize-2026-arc-agi-2"),
        Path("/kaggle/input/arc-agi-2"),
        Path(__file__).resolve().parents[1] / "data" / "arc-agi-2",
    ]
    for p in named:
        if (p / "arc-agi_test_challenges.json").exists():
            return p
    root = Path("/kaggle/input")
    if root.exists():
        hits = sorted(root.rglob("arc-agi_test_challenges.json"))
        if hits:
            print("resolved data via rglob:", hits[0].parent)
            return hits[0].parent
        # debug mount layout for next fix
        print("kaggle input tree:")
        for p in sorted(root.rglob("*"))[:80]:
            print(" ", p)
    raise SystemExit("test challenges not found under /kaggle/input or local data/")


def main() -> None:
    data_dir = _find_data_dir()
    challenges = json.loads((data_dir / "arc-agi_test_challenges.json").read_text())
    submission = solve_challenges(challenges)

    out = Path("/kaggle/working/submission.json")
    if not out.parent.exists():
        out = Path("submission.json")
    out.write_text(json.dumps(submission))
    print(f"wrote {out} tasks={len(submission)}")


if __name__ == "__main__":
    main()
