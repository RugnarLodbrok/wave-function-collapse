from __future__ import annotations

from enum import Enum
from typing import Iterator, NamedTuple

import pygame
from pygame import Surface

from src.config import Config
from src.resources import SPRITES
from src.slot import Slot
from src.tile_base import TileBase


class TileType(Enum):
    TOP = 'top'
    BOT = 'bot'
    LEFT = 'left'
    RIGHT = 'right'
    MT = 'mt'

    def __str__(self):
        return self.value


_MAP = {
    Slot(-1, 0): 0,
    Slot(0, -1): 1,
    Slot(1, 0): 2,
    Slot(0, 1): 3,
}


class TileConstraints(NamedTuple):  # order matters
    left: int
    top: int
    right: int
    bot: int

    def match(self, other: TileConstraints, pos: Slot) -> bool:
        return self[_MAP[pos]] == other[_MAP[-pos]]


class Tile(TileBase):
    def __init__(self, constraints: TileConstraints, type_: TileType):
        super().__init__()
        self.constraints = constraints
        self.type = type_

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
        pygame.transform.scale_by(self.sprite, 0.5, self.small_sprite)

    @staticmethod
    def affected_slots(
        slot: Slot,
    ) -> Iterator[Slot]:  # order the same as in TileConstraints
        if slot.x > 0:
            yield 0, Slot(slot.x - 1, slot.y)
        if slot.y > 0:
            yield 1, Slot(slot.x, slot.y - 1)
        if slot.x < Config.GRID_W - 2:
            yield 2, Slot(slot.x + 1, slot.y)
        if slot.y < Config.GRID_W - 2:
            yield 3, Slot(slot.x, slot.y + 1)


TILES = [
    Tile(TileConstraints(0, 0, 0, 0), TileType.MT),
    Tile(TileConstraints(1, 1, 1, 0), TileType.TOP),
    Tile(TileConstraints(1, 1, 0, 1), TileType.LEFT),
    Tile(TileConstraints(1, 0, 1, 1), TileType.BOT),
    Tile(TileConstraints(0, 1, 1, 1), TileType.RIGHT),
]
