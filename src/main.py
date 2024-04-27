from __future__ import annotations

from src.grid import Blank, run_wave_function_collapse
from src.t_tile import TILES

if __name__ == '__main__':
    run_wave_function_collapse(lambda x, y: Blank(TILES[:]))
