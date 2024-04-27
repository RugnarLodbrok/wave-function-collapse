from __future__ import annotations

from collections import defaultdict
from random import choice
from typing import Callable

from pygame import Surface
from pygame.locals import K_SPACE
from pygame.math import Vector2

from src.config import Config
from src.pygame_base import Game, GameObject
from src.slot import Slot
from src.t_tile import TILES, Tile


class Blank:
    def __init__(self, possibilities: list[Tile]):
        self.possibilities = possibilities

    def draw(self, screen: Surface, pos: tuple[int, int]):
        pos = Vector2(pos)
        for offset, p in zip(
            (
                Vector2(0, 0),
                Vector2(Config.TILE_SIZE // 2, 0),
                Vector2(0, Config.TILE_SIZE // 2),
                Vector2(Config.TILE_SIZE // 2, Config.TILE_SIZE // 2),
                Vector2(3 * Config.TILE_SIZE // 2, 3 * Config.TILE_SIZE // 2),
            ),
            reversed(self.possibilities),
        ):
            screen.blit(p.small_sprite, pos + offset)


class Grid(GameObject):
    def __init__(self, tile_fn: Callable[[int, int], Blank | Tile]):
        self.data: list[list[Tile | Blank]] = [
            [tile_fn(x, y) for y in range(Config.GRID_H)] for x in range(Config.GRID_W)
        ]
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
            return  # todo: raise
        tile = choice(
            self[slot].possibilities
        )  # todo: take first, rely on initial shuffle
        self[slot] = tile
        self.active_slots.remove(slot)

        for idx, other_slot in tile.affected_slots(slot):
            blank = self[other_slot]
            if not isinstance(blank, Blank):
                continue
            self.active_slots.add(other_slot)
            blank.possibilities = [
                option
                for option in blank.possibilities
                if tile.constraints.match(option.constraints, other_slot - slot)
            ]

    def draw(self, screen: Surface):
        tile: Tile | Blank
        for x, column in enumerate(self.data):
            for y, tile in enumerate(column):
                if isinstance(tile, Blank):
                    if Slot(x, y) in self.active_slots:
                        tile.draw(screen, (x * Config.TILE_SIZE, y * Config.TILE_SIZE))
                else:
                    screen.blit(
                        tile.sprite, (x * Config.TILE_SIZE, y * Config.TILE_SIZE)
                    )

    def update(self, dt: float) -> None:
        self.step()


def init_tiles():
    for t in TILES:
        t.init()


def run_wave_function_collapse(blank_fn: Callable[[int, int], Blank | Tile]):
    grid = Grid(blank_fn)

    def step(game: Game):
        grid.step()

    game = Game()
    game.objects.append(grid)
    game.key_map[K_SPACE] = step
    game.initialize()
    init_tiles()
    grid.set_tile(Slot(5, 5))
    game.run()
