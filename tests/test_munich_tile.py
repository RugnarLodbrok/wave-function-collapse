import pytest

from src.munich_tile import MunichTileType
from src.slot import Slot


@pytest.mark.parametrize(
    ('tile', 'other_tile', 'slot', 'match'),
    [
        (MunichTileType(0, 0, 0, 0), MunichTileType(0, 0, 0, 0), Slot(1, 0), True),
        (MunichTileType(1, 0, 0, 0), MunichTileType(0, 0, 0, 0), Slot(1, 0), True),
        (MunichTileType(1, 0, 0, 0), MunichTileType(0, 0, 0, 0), Slot(-1, 0), False),
        (MunichTileType(1, 0, 0, 0), MunichTileType(0, 0, 0, 0), Slot(0, 1), True),
        (MunichTileType(1, 1, 0, 0), MunichTileType(0, 0, 0, 0), Slot(0, -1), False),
        (MunichTileType(1, 1, 0, 0), MunichTileType(0, 0, 0, 0), Slot(0, 1), True),
        (MunichTileType(1, 0, 0, 0), MunichTileType(0, 0, 1, 0), Slot(-1, 0), True),
        (MunichTileType(1, 0, 0, 0), MunichTileType(0, 1, 0, 0), Slot(-1, -1), True),
    ],
)
def test_match(tile, other_tile, slot, match):
    assert tile.match(other_tile, slot) == match
