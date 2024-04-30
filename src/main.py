from __future__ import annotations

from random import shuffle, seed

from src.grid import Blank, run_wave_function_collapse
from src.munich_tile import TILES


def foo(x, y):
    tiles = TILES[:]
    shuffle(tiles)
    return Blank(tiles)


if __name__ == '__main__':
    seed(123)

    run_wave_function_collapse(foo)
