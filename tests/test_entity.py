import pytest
from rogue.entity import Entity
from rogue.world import World
from rogue.tile import Tile

@pytest.fixture
def entity():
    return Entity(x=100, y=100, health=100, solid=True)

@pytest.fixture
def entity2():
    return Entity(x=94, y=20, health=100, solid=True)

@pytest.fixture
def world():
    return World(width=100, height=100)

def test_entity_initialize(entity):
    assert entity.x == 100
    assert entity.y == 100
    assert entity.health == 100

def test_move_to_empty_space(entity, world):
    assert entity.move(10, 12, world)
    assert entity.x == 10
    assert entity.y == 12

def test_move_solid_entity_into_wall(entity, world):
    world.set_tile(10, 12, Tile.wall)
    assert not entity.move(10, 12, world)
    assert not entity.x == 10
    assert not entity.y == 12

def test_move_non_solid_entity_into_wall(entity, world):
    entity.solid = False
    world.set_tile(10, 12, Tile.wall)
    assert entity.move(10, 12, world)
    assert entity.x == 10
    assert entity.y == 12

def test_move_solid_entity_into_other_solid_entity(entity, entity2, world):
    world.add_entity(entity2)
    assert not entity.move(entity2.x, entity2.y, world)
    assert not entity.x == entity2.x
    assert not entity.y == entity2.y

def test_move_non_solid_entity_into_other_solid_entity(entity, entity2, world):
    entity.solid = False
    world.add_entity(entity2)
    assert entity.move(entity2.x, entity2.y, world)
    assert entity.x == entity2.x
    assert entity.y == entity2.y

def test_calculating_damage(entity):
    damage = entity.calculate_damage(entity)
    assert damage is not None
