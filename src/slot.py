from __future__ import annotations

from typing import Iterator, NamedTuple

from src.common import Rot
from src.config import Config


class Slot(NamedTuple):
    x: int
    y: int

    def neighbours(
        self,
    ) -> Iterator[tuple[int, Slot]]:  # order the same as in TileConstraints
        # not used
        if self.x > 0:
            yield 0, Slot(self.x - 1, self.y)
        if self.y > 0:
            yield 1, Slot(self.x, self.y - 1)
        if self.x < Config.GRID_W - 2:
            yield 2, Slot(self.x + 1, self.y)
        if self.y < Config.GRID_W - 2:
            yield 3, Slot(self.x, self.y + 1)

    def __sub__(self, other: Slot) -> Slot:
        x, y = self
        x1, y1 = other
        return Slot(x - x1, y - y1)

    def __add__(self, other):
        return Slot(self.x + other.x, self.y + other.y)

    def __neg__(self) -> Slot:
        return Slot(-self.x, -self.y)

    def rotate(self, rot: Rot) -> Slot:
        rot = rot % 4
        x, y = self
        while rot:
            rot -= 1
            x, y = -y, x
        return Slot(x, y)

    def quadrant(self) -> Rot:
        """
             -y
        III(2)| IV(3)
         -x---O---+x
         II(1)| I(0)
             +y
        """
        rot = Rot(0)
        x, y = self
        if not x | y:
            return Rot(0)
        if y < 0 or y == 0 and x < 0:
            x, y = -self
            rot = Rot(2)
        if x > 0:
            return rot
        else:
            return rot + 1
