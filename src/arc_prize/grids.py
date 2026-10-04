"""Grid helpers for ARC-AGI-2."""

from __future__ import annotations

from typing import Callable

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


def tile_checker(g: Grid, nx: int, ny: int) -> Grid:
    """3×3-style checker of identity / flip_h / flip_v / rot180 blocks."""
    blocks = [
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
                fn = blocks[by % 3][bx % 3]
                row.extend(fn(g)[r])
            rows_out.append(row)
    return rows_out


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


GEOMETRIC: list[tuple[str, Transform]] = [
    ("identity", identity),
    ("rot90", rot90),
    ("rot180", rot180),
    ("rot270", rot270),
    ("flip_h", flip_h),
    ("flip_v", flip_v),
    ("transpose", transpose),
]
