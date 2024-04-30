from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterator, NamedTuple, Self

import pygame
from pygame import Surface
from pygame.transform import rotate

from src.common import Rot
from src.config import Config
from src.resources import SPRITES
from src.slot import Slot
from src.tile_base import TileBase


@dataclass
class TileSpriteMaker:
    slot: Slot
    rot: Rot

    def __call__(self) -> Surface:
        sprite = pygame.Surface((Config.TILE_SIZE, Config.TILE_SIZE))
        sprite.blit(SPRITES.MUNICH, -self.slot * Config.TILE_SIZE)
        return rotate(sprite, 90 * self.rot)


class MunichTileType(NamedTuple):
    left: int
    top: int
    right: int
    bot: int

    def rotate(self, rot: Rot) -> MunichTileType:
        l, t, r, b = self
        while rot:
            rot = rot - 1
            l, t, r, b = b, l, t, r
        return MunichTileType(l, t, r, b)

    def translate(self, pos: Slot) -> Self:
        return MunichTileType(
            self.left + pos.x, self.top + pos.y, self.right - pos.x, self.bot - pos.y
        )

    def match(self, other: MunichTileType, pos: Slot) -> bool:
        if self.translate(pos) == other:
            return True
        rot = -pos.quadrant()
        pos = pos.rotate(rot)
        a = self.rotate(rot)
        b = other.rotate(rot)
        x, y = pos
        return a.right + b.left < x or a.bot + b.top < y


class Tile(TileBase):
    MAX_SIZE = Slot(4, 3)

    def __init__(self, type_: MunichTileType, sprite_fn: Callable[[], Surface]):
        super().__init__()
        self.type = type_
        self._sprite_fn = sprite_fn
        self.small_sprite = None

    def __repr__(self):
        return f'Tile{self.type}'

    def init(self):
        self.sprite = self._sprite_fn()
        self.small_sprite = pygame.transform.scale_by(self.sprite, 1 / 2.1)

    def affected_slots(self) -> Iterator[Slot]:
        typ = self.type
        mx = 4  # max tile size
        for x in range(typ.left - mx, typ.right + 1 + mx):
            for y in range(typ.top - mx, typ.bot + 1 + mx):
                yield Slot(x, y)

    def match(self, other: Tile, pos: Slot) -> bool:
        return self.type.match(other.type, pos)


TILES = [
    Tile(MunichTileType(1, 0, 0, 0), TileSpriteMaker(Slot(0, 0), Rot(0))),
    Tile(MunichTileType(0, 1, 0, 0), TileSpriteMaker(Slot(0, 0), Rot(3))),
    Tile(MunichTileType(0, 0, 1, 0), TileSpriteMaker(Slot(0, 0), Rot(2))),
    Tile(MunichTileType(0, 0, 0, 1), TileSpriteMaker(Slot(0, 0), Rot(1))),
    Tile(MunichTileType(1, 1, 0, 0), TileSpriteMaker(Slot(0, 1), Rot(0))),
    Tile(MunichTileType(0, 1, 1, 0), TileSpriteMaker(Slot(0, 1), Rot(3))),
    Tile(MunichTileType(0, 0, 1, 1), TileSpriteMaker(Slot(0, 1), Rot(2))),
    Tile(MunichTileType(1, 0, 0, 1), TileSpriteMaker(Slot(0, 1), Rot(1))),
]
