from arc_prize.grids import tile_checker
from arc_prize.solver import fit_program


def test_tile_checker_fits_known_pattern():
    train = [
        {
            "input": [[7, 9], [4, 3]],
            "output": [
                [7, 9, 7, 9, 7, 9],
                [4, 3, 4, 3, 4, 3],
                [9, 7, 9, 7, 9, 7],
                [3, 4, 3, 4, 3, 4],
                [7, 9, 7, 9, 7, 9],
                [4, 3, 4, 3, 4, 3],
            ],
        }
    ]
    prog = fit_program(train)
    assert prog is not None
    name, fn = prog
    assert "tile_alt_flip_h" in name or "tile" in name
    assert fn(train[0]["input"]) == train[0]["output"]


def test_identity_fit():
    g = [[1, 2], [3, 4]]
    prog = fit_program([{"input": g, "output": g}])
    assert prog is not None
    assert prog[1](g) == g


def test_tile_checker_helper_shape():
    g = [[1, 0], [0, 1]]
    out = tile_checker(g, 3, 3)
    assert len(out) == 6
    assert len(out[0]) == 6
