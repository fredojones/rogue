import pytest
from collections import namedtuple

import rogue.ray
import rogue.room
from rogue.entity import Entity
from rogue.world import World
from rogue.tile import Tile

@pytest.fixture
def world():
    return World(width=200, height=200)


def test_raycast_in_room(world):
    world.add_room(10, 10, rogue.room.rect_room(20, 20))

    entity = Entity(x=20, y=15)
    world.add_entity(entity)

    Point = namedtuple("Point", ['x', 'y'])
    res = rogue.ray.ray_cast(Point(20, 20), 70, world)

    # Last item should be a wall
    assert res.tiles[len(res.tiles) - 1][1] == Tile.wall
    assert res.tiles[len(res.tiles) - 2][1] == Tile.floor

    # There should be 5 tiles seen
    assert len(res.tiles) == 5

    # The entity should be seen
    #assert entity in res.entities
