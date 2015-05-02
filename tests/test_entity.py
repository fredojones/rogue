import pytest
from rogue.entity import Entity
from rogue.world import World
from rogue.tile import Tile

@pytest.fixture
def entity():
    return Entity(x=100, y=100)

@pytest.fixture
def world():
    return World(width=100, height=100)

def test_entity_initialize(entity):
    assert entity.x == 100
    assert entity.y == 100

def test_move_to_empty_space(entity, world):
    assert entity.move(10, 12, world)
    assert entity.x == 10
    assert entity.y == 12

def test_move_to_occupied_space(entity, world):
    world.set_tile(10, 12, Tile.wall)
    assert not entity.move(10, 12, world)
    assert not entity.x == 10
    assert not entity.y == 12
