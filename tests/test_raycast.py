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

    for a in range(0, 360, 30):
        res = rogue.ray.ray_cast(point=(20, 20), angle=a,
                radius=20, world=world)

        # First item should always be point given to raycast
        assert res[0] == (20, 20)

        # Last item should always be a wall
        x, y = res.pop()
        assert world.get_tile(x, y) == Tile.wall

def test_tiles_visible_in_square_room(world):
    world.add_room(10, 10, rogue.room.rect_room(30, 30))

    res = rogue.ray.ray_cast_circle(point=(20, 20), radius=40, world=world)

    # all tiles should be visible to player
    for x in range(30):
        for y in range(30):
            assert (x + 10, y + 10) in res

def test_entities_visible_to_entity(world):
    entities = []
    entities.append(Entity(x=30, y=30))
    entities.append(Entity(x=26, y=30))
    entities.append(Entity(x=25, y=20))
    entities.append(Entity(x=24, y=80))

    for entity in entities:
        world.add_entity(entity)

    world.add_room(10, 10, rogue.room.rect_room(30, 30))

    res = rogue.ray.ray_cast_circle(point=(20, 20), radius=40, world=world)

    entities_seen = list(map(lambda p: world.get_entity_at(p[0], p[1]), res))

    assert entities[0] in entities_seen
    assert entities[1] in entities_seen
    assert entities[2] in entities_seen
    assert entities[3] not in entities_seen

