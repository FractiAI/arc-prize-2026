"""Grid helpers for ARC-AGI-2."""

from __future__ import annotations

from typing import Callable

Grid = list[list[int]]
Transform = Callable[[Grid], Grid]


def copy_grid(g: Grid) -> Grid:
    return [row[:] for row in g]


def same(a: Grid, b: Grid) -> bool:
    return a == b


def height(g: Grid) -> int:
    return len(g)


def width(g: Grid) -> int:
    return len(g[0]) if g else 0


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
    """Tile with alternating vertical bands: identity, flip_h, identity, …"""
    rows_out: Grid = []
    h = len(g)
    for by in range(ny):
        block = flip_h(g) if by % 2 else identity(g)
        for r in range(h):
            rows_out.append(block[r] * nx)
    return rows_out


def tile_alt_flip_v(g: Grid, nx: int, ny: int) -> Grid:
    """Tile with alternating horizontal bands: identity, flip_v, …"""
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
    """Checker of identity / flip_h / flip_v / rot180 blocks."""
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
                fn = fns[by % 3][bx % 3]
                row.extend(fn(g)[r])
            rows_out.append(row)
    return rows_out


def upscale(g: Grid, k: int) -> Grid:
    """Replace each cell with a k×k block of the same color."""
    if k < 2:
        return copy_grid(g)
    out: Grid = []
    for row in g:
        expanded = []
        for v in row:
            expanded.extend([v] * k)
        for _ in range(k):
            out.append(expanded[:])
    return out


def gravity(g: Grid, direction: str = "down", bg: int = 0) -> Grid:
    """Slide non-bg cells to an edge within each column/row."""
    h, w = height(g), width(g)
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
    else:  # left / right
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
    """Tight bbox around non-bg cells; empty → original."""
    coords = [(r, c) for r, row in enumerate(g) for c, v in enumerate(row) if v != bg]
    if not coords:
        return copy_grid(g)
    rs = [r for r, _ in coords]
    cs = [c for _, c in coords]
    r0, r1 = min(rs), max(rs)
    c0, c1 = min(cs), max(cs)
    return [row[c0 : c1 + 1] for row in g[r0 : r1 + 1]]


def replace_color(g: Grid, src: int, dst: int) -> Grid:
    return [[dst if v == src else v for v in row] for row in g]


def remap_colors(g: Grid, mapping: dict[int, int]) -> Grid:
    return [[mapping.get(v, v) for v in row] for row in g]


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


GEOMETRIC: list[tuple[str, Transform]] = [
    ("identity", identity),
    ("rot90", rot90),
    ("rot180", rot180),
    ("rot270", rot270),
    ("flip_h", flip_h),
    ("flip_v", flip_v),
    ("transpose", transpose),
]
