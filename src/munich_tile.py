from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, NamedTuple, Self

import pygame
from pygame.transform import rotate

from src.common import Rot
from src.config import Config
from src.resources import SPRITES
from src.slot import Slot
from src.tile_base import TileBase


@dataclass
class TileSetTransform:
    slot: Slot
    rot: Rot

    def get_sprite(self):
        sprite = pygame.Surface((Config.TILE_SIZE, Config.TILE_SIZE))
        sprite.blit(SPRITES.MUNICH, -self.slot)
        return rotate(sprite, 90 * self.rot)


_TRANSFORMS = {
    (1, 0, 0, 0): TileSetTransform(Slot(0, 0), Rot(0)),
    (0, 1, 0, 0): TileSetTransform(Slot(0, 0), Rot(3)),
    (0, 0, 1, 0): TileSetTransform(Slot(0, 0), Rot(2)),
    (0, 0, 0, 1): TileSetTransform(Slot(0, 0), Rot(1)),
}


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


class Tile(TileBase):
    MAX_SIZE = Slot(4, 3)

    def __init__(self, left: int, top: int, right: int, bot: int):
        super().__init__()
        self.type = MunichTileType(left, top, right, bot)

    def __repr__(self):
        return f'Tile{self.type}'

    def init(self):
        self.sprite = _TRANSFORMS[self.type].get_sprite()
        self.small_sprite = pygame.transform.scale_by(self.sprite, 1 / 2.1)

    def affected_slots(self) -> Iterator[Slot]:
        typ = self.type
        mx = 4  # max tile size
        for x in range(typ.left - mx, typ.right + 1 + mx):
            for y in range(typ.top - mx, typ.bot + 1 + mx):
                yield Slot(x, y)

    def match(self, other: Tile, pos: Slot) -> bool:
        if self.type.translate(pos) == other.type:
            return True
        rot = -pos.quadrant()
        pos = pos.rotate(rot)
        a = self.type.rotate(rot)
        b = other.type.rotate(rot)
        x, y = pos
        return a.right + b.left < x or a.bot + b.top < y


TILES = [
    Tile(1, 0, 0, 0),
    Tile(0, 1, 0, 0),
    Tile(0, 0, 1, 0),
    Tile(0, 0, 0, 1),
]
