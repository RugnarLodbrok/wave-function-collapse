from __future__ import annotations

from typing import Iterator

from pygame import Surface, Vector2

from src.config import Config
from src.slot import Slot


class TileBase:
    def __init__(self):
        self.sprite = None

    def init(self):
        raise NotImplementedError

    def __repr__(self):
        raise NotImplementedError

    def affected_slots(self) -> Iterator[Slot]:
        raise NotImplementedError

    def match(self, other: TileBase, pos: Slot) -> bool:
        raise NotImplementedError

    def draw(self, screen: Surface, pos: Slot):
        screen.blit(self.sprite, pos * Config.TILE_SIZE)


class Blank(TileBase):
    def __init__(self, possibilities: list[Tile]):  # noqa
        self.possibilities = possibilities

    @property
    def sprite(self) -> Surface:
        sprite = Surface((Config.TILE_SIZE, Config.TILE_SIZE))
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
            sprite.blit(p.small_sprite, offset)
        return sprite
