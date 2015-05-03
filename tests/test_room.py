import rogue.room as room
from rogue.tile import Tile


def test_generating_square_room():
    width, height = 10, 12
    square = room.square_room(10, 12)
    assert len(square.values()) == width * height
    assert square[(0, 0)] == Tile.wall
    assert square[(0, 1)] == Tile.wall
    assert square[(1, 1)] == Tile.floor
    assert square[(width - 1, height - 1)] == Tile.wall
