import pytest
from rogue.world import World
from rogue.tile import Tile
from rogue.entity import Entity

@pytest.fixture
def world():
    return World(width=100, height=100)

@pytest.fixture
def entity():
    return Entity(0, 0, Tile.player)

def test_world_initialize(world):
    assert world.width == 100
    assert world.height == 100

def test_setting_then_getting_tile(world):
    world.set_tile(10, 10, Tile.exit)
    assert world.get_tile(10, 10) == Tile.exit

def test_checking_if_tile_is_wall(world):
    assert not world.is_wall(10, 10)
    world.set_tile(10, 10, Tile.wall)
    assert world.is_wall(10, 10)

def test_getting_out_of_range_tile(world):
    with pytest.raises(IndexError):
        world.get_tile(-10, -10)
        world.get_tile(1000, 1000)

def test_empty_tiles_correct_dimensions(world):
    tiles = world.Empty_Tiles(width=10, height=12, tile=Tile.floor)
    assert len(tiles) == 10 * 12
    assert tiles[(0, 0)] == Tile.floor

def test_random_floor_tile(world):
    world.set_tile(10, 12, Tile.floor)
    p = world.random_floor_tile()
    assert p.x == 10
    assert p.y == 12

def test_random_floor_tile_empty_world(world):
    with pytest.raises(Exception):
        world.random_floor_tile()

def test_added_entity_becomes_added(world, entity):
    world.add_entity(entity)
    assert entity in world.entities
