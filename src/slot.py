from __future__ import annotations

from typing import Iterator, NamedTuple

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

    def __neg__(self) -> Slot:
        return Slot(-self.x, -self.y)
