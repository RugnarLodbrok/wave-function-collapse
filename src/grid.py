from __future__ import annotations

from collections import defaultdict
from random import choice
from typing import Callable

from pygame import Surface
from pygame.locals import K_SPACE

from src.config import Config
from src.munich_tile import TILES
from src.pygame_base import Game, GameObject
from src.slot import Slot
from src.tile_base import Blank
from src.tile_base import TileBase as Tile


class Grid(GameObject):
    def __init__(self, tile_fn: Callable[[int, int], Tile]):
        self.data: list[list[Tile]] = [
            [tile_fn(x, y) for y in range(Config.GRID_H)] for x in range(Config.GRID_W)
        ]
        self.active_slots: set[Slot] = set()
        self.draw_once_queue: set[Slot] = set()

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

    def __getitem__(self, item: Slot) -> Tile:
        return self.data[item.x][item.y]

    def __setitem__(self, key: Slot, value: Tile):
        self.data[key.x][key.y] = value

    def _set_tile(self, slot: Slot):
        tile = self[slot]
        assert isinstance(tile, Blank)
        if not tile.possibilities:
            return  # todo: raise
        tile = tile.possibilities[0]
        self[slot] = tile
        self.active_slots.remove(slot)
        self.draw_once_queue.add(slot)

        for offset in tile.affected_slots():
            other_slot = slot + offset
            if (
                other_slot.x < 0
                or other_slot.y < 0
                or other_slot.x >= Config.GRID_W
                or other_slot.y >= Config.GRID_H
            ):
                continue
            blank = self[other_slot]
            if not isinstance(blank, Blank):
                continue
            self.active_slots.add(other_slot)
            blank.possibilities = [
                option for option in blank.possibilities if tile.match(option, offset)
            ]

    def draw(self, screen: Surface):
        tile: Tile | Blank
        for x, column in enumerate(self.data):
            for y, tile in enumerate(column):
                slot = Slot(x, y)
                if slot in self.draw_once_queue:
                    self.draw_once_queue.remove(slot)
                elif slot not in self.active_slots:
                    continue
                tile.draw(screen, slot)
                # if isinstance(tile, Blank):
                #     if Slot(x, y) in self.active_slots:
                #         tile.draw(screen, (x * Config.TILE_SIZE, y * Config.TILE_SIZE))
                # else:
                #     screen.blit(
                #         tile.sprite, (x * Config.TILE_SIZE, y * Config.TILE_SIZE)
                #     )

    def update(self, dt: float) -> None:
        self.step()
        # pass


def init_tiles():
    for t in TILES:
        t.init()


def run_wave_function_collapse(blank_fn: Callable[[int, int], Blank | Tile]):
    grid = Grid(blank_fn)

    def step(game: Game):
        grid.step()

    game = Game()
    game.fill = None
    game.objects.append(grid)
    game.key_map[K_SPACE] = step
    game.initialize()
    init_tiles()
    grid.active_slots.add(Slot(9, 9))
    game.run()
