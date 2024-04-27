from __future__ import annotations

from typing import Iterator

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
