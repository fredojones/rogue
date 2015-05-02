import pytest
from rogue.world import World
from rogue.tile import Tile

@pytest.fixture
def world():
    return World(width=100, height=100)

def test_world_initialize(world):
    assert world.width == 100
    assert world.height == 100

def test_setting_then_getting_tile(world):
    world.set_tile(10, 10, Tile.exit)
    assert world.get_tile(10, 10) == Tile.exit

def test_getting_out_of_range_tile(world):
    with pytest.raises(IndexError):
        world.get_tile(-10, -10)
        world.get_tile(1000, 1000)
