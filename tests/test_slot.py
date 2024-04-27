import pytest

from src.slot import Slot


@pytest.mark.parametrize(
    ('slot', 'quadrant'), [
        (Slot(0, 0), 0),
        (Slot(1, 0), 0),
        (Slot(1, 1), 0),
        (Slot(0, 1), 1),
        (Slot(-1, 1), 1),
        (Slot(-1, 0), 2),
        (Slot(-1, -1), 2),
        (Slot(0, -1), 3),
        (Slot(1, -1), 3),
    ]
)
def test_quadrant(slot, quadrant):
    assert slot.quadrant() == quadrant


@pytest.mark.parametrize(
    ('slot', 'result'),[
        (Slot(0, 0), Slot(0, 0)),
        (Slot(1, 0), Slot(1, 0)),
        (Slot(1, 1), Slot(1, 1)),
        (Slot(0, 1), Slot(1, 0)),
        (Slot(-1, 1), Slot(1, 1)),
        (Slot(-1, 0), Slot(1, 0)),
        (Slot(-1, -1), Slot(1, 1)),
        (Slot(0, -1), Slot(1, 0)),
        (Slot(1, -1), Slot(1, 1)),
    ]
)
def test_rotate(slot, result):
    quadrant = slot.quadrant()
    assert slot.rotate(-quadrant) == result
