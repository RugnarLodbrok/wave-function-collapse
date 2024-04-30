from __future__ import annotations

from random import seed, shuffle

from pygame.locals import K_SPACE, K_r

from src.grid import Blank, Grid
from src.munich_tile import TILES
from src.pygame_base import Game
from src.slot import Slot


def foo(x, y):
    tiles = TILES[:]
    shuffle(tiles)
    return Blank(tiles)


class App:
    def __init__(self):
        self.grid = None
        self.game = Game(fill=None)

    def run(self):
        self.game.initialize()
        self.init_tiles()
        self.reset()
        self.game.run()

    @staticmethod
    def init_tiles():
        for t in TILES:
            t.init()

    def reset(self):
        self.game.key_map.clear()
        del self.game.objects[:]
        self.grid = Grid(tile_fn=foo)
        self.grid.active_slots.add(Slot(9, 9))
        self.game.key_map[K_SPACE] = lambda _: self.grid.step()
        self.game.key_map[K_r] = lambda _: self.reset()
        self.game.objects.append(self.grid)


if __name__ == '__main__':
    seed(123)
    App().run()
