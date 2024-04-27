import pytest

from src.munich_tile import Tile
from src.slot import Slot


@pytest.mark.parametrize(
    ('tile', 'other_tile', 'slot', 'match'), [
        (Tile(0, 0, 0, 0), Tile(0, 0, 0, 0), Slot(1, 0), True),
        (Tile(1, 0, 0, 0), Tile(0, 0, 0, 0), Slot(1, 0), True),
        (Tile(1, 0, 0, 0), Tile(0, 0, 0, 0), Slot(-1, 0), False),
        (Tile(1, 0, 0, 0), Tile(0, 0, 0, 0), Slot(0, 1), True),
        (Tile(1, 1, 0, 0), Tile(0, 0, 0, 0), Slot(0, -1), False),
        (Tile(1, 1, 0, 0), Tile(0, 0, 0, 0), Slot(0, 1), True),
        (Tile(1, 0, 0, 0), Tile(0, 0, 1, 0), Slot(-1, 0), True),
        (Tile(1, 0, 0, 0), Tile(0, 1, 0, 0), Slot(-1, -1), True),
    ]
)
def test_match(tile, other_tile, slot, match):
    assert tile.match(other_tile, slot) == match
