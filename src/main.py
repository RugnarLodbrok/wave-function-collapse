from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from random import choice
from typing import NamedTuple, Iterator

import pygame
from pygame import Surface

from src.pygame_base import Game, GameObject
from pygame.locals import K_SPACE
from pygame.math import Vector2

from src.resources import SPRITES

W, H = 40, 40


class TileType(Enum):
    TOP = 'top'
    BOT = 'bot'
    LEFT = 'left'
    RIGHT = 'right'
    MT = 'mt'

    def __str__(self):
        return self.value


class Slot(NamedTuple):
    x: int
    y: int

    def neighbours(self) -> Iterator[tuple[int, Slot]]:  # order the same as in TileConstraints
        if self.x > 0:
            yield 0, Slot(self.x - 1, self.y)
        if self.y > 0:
            yield 1, Slot(self.x, self.y - 1)
        if self.x < W - 2:
            yield 2, Slot(self.x + 1, self.y)
        if self.y < H - 2:
            yield 3, Slot(self.x, self.y + 1)


class TileConstraints(NamedTuple):  # order matters
    left: int
    top: int
    right: int
    bot: int

    def match(self, other: TileConstraints, direction_index: int):
        return self[direction_index] == other[(direction_index + 2) % 4]


class Tile:
    def __init__(self, constraints: TileConstraints, type_: TileType):
        self.constraints = constraints
        self.type = type_
        self.sprite = None

    def __repr__(self):
        return f'Tile[{self.type}]'

    def init(self):
        TILE_MAP = {
            TileType.TOP: SPRITES.TOP,
            TileType.BOT: SPRITES.BOT,
            TileType.LEFT: SPRITES.LEFT,
            TileType.RIGHT: SPRITES.RIGHT,
            TileType.MT: SPRITES.MT,
        }
        self.sprite = TILE_MAP[self.type]
        self.small_sprite = Surface((16, 16))
        pygame.transform.scale_by(self.sprite, .5, self.small_sprite)
        _ = 1


TILES = [
    Tile(TileConstraints(0, 0, 0, 0), TileType.MT),
    Tile(TileConstraints(1, 1, 1, 0), TileType.TOP),
    Tile(TileConstraints(1, 1, 0, 1), TileType.LEFT),
    Tile(TileConstraints(1, 0, 1, 1), TileType.BOT),
    Tile(TileConstraints(0, 1, 1, 1), TileType.RIGHT),
]


# def choice(a):
#     return a[0]
#

class Blank:
    def __init__(self):
        self.possibilities = TILES[:]

    def draw(self, screen: Surface, pos: tuple[int, int]):
        pos = Vector2(pos)
        for offset, p in zip(
                (Vector2(0, 0), Vector2(16, 0), Vector2(0, 16), Vector2(16, 16), Vector2(24, 24)),
                reversed(self.possibilities)
        ):
            screen.blit(p.small_sprite, pos + offset)


class Grid(GameObject):
    def __init__(self):
        self.data: list[list[Tile | Blank]] = [[Blank() for _ in range(H)] for _ in range(W)]
        self.active_slots: set[Slot] = set()

    def _chose_best_slot(self) -> Slot:
        slots_per_option_number = defaultdict(list)
        for slot in self.active_slots:
            blank = self.data[slot.x][slot.y]
            if not isinstance(blank, Blank):
                _ = 1
            assert isinstance(blank, Blank)
            slots_per_option_number[len(blank.possibilities)].append(slot)
        slot_w_least_options = slots_per_option_number[min(slots_per_option_number)]
        return choice(slot_w_least_options)

    def step(self):
        if not self.active_slots:
            return
        slot = self._chose_best_slot()
        self._set_tile(slot)

    def set_tile(self, slot: Slot):
        self.active_slots.add(slot)
        self._set_tile(slot)

    def __getitem__(self, item: Slot) -> Tile | Blank:
        return self.data[item.x][item.y]

    def __setitem__(self, key: Slot, value: Tile):
        self.data[key.x][key.y] = value

    def _set_tile(self, slot: Slot):
        assert isinstance(self[slot], Blank)
        if not self[slot].possibilities:
            return
        tile = choice(self[slot].possibilities)
        self[slot] = tile
        self.active_slots.remove(slot)

        for idx, neigh in slot.neighbours():
            blank = self[neigh]
            if isinstance(blank, Blank):
                self.active_slots.add(neigh)
                blank.possibilities = [option for option in blank.possibilities if
                                       tile.constraints.match(option.constraints, idx)]

    def draw(self, screen: Surface):
        tile: Tile | Blank
        for x, column in enumerate(self.data):
            for y, tile in enumerate(column):
                if isinstance(tile, Blank):
                    if Slot(x, y) in self.active_slots:
                        tile.draw(screen, (x * 32, y * 32))
                else:
                    screen.blit(tile.sprite, (x * 32, y * 32))

    def update(self, dt: float) -> None:
        self.step()
def init_tiles():
    for t in TILES:
        t.init()


def main():
    grid = Grid()

    def step(game: Game):
        grid.step()

    game = Game()
    game.objects.append(grid)
    game.key_map[K_SPACE] = step
    game.initialize()
    init_tiles()
    grid.set_tile(Slot(5, 5))
    game.run()


if __name__ == '__main__':
    main()
