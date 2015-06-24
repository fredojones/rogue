import pytest
from rogue.camera import Camera
from rogue.entity import Entity
from rogue.world import World
import rogue.room

@pytest.fixture
def camera():
    return Camera(x=100, y=100, width=100, height=100)

@pytest.fixture
def entity():
    return Entity(x=20, y=20)

@pytest.fixture
def world():
    return World(width=200, height=200)

def test_camera_initialize(camera):
    assert camera.view.x == 100
    assert camera.view.y == 100
    assert camera.view.width == 100
    assert camera.view.height == 100

def test_entity_on_screen(camera, entity):
    entity.x = 50
    entity.y = 120
    assert not camera.is_visible(entity)
    entity.x = 120
    entity.y = 50
    assert not camera.is_visible(entity)
    entity.x = 110
    entity.y = 120
    assert camera.is_visible(entity)

def test_camera_center_on_entity_makes_entity_visible(camera, entity, world):
    assert not camera.is_visible(entity)
    camera.center_on(entity, world)
    assert camera.is_visible(entity)

def test_camera_center_on_cant_make_camera_out_of_bounds(camera, entity, world):
    entity.x = 10
    entity.y = 10
    camera.center_on(entity, world)

    assert camera.view.x >= 0
    assert camera.view.y >= 0

    entity.x = 180
    entity.y = 180
    camera.center_on(entity, world)

    assert camera.view.x + camera.view.width <= world.width
    assert camera.view.y + camera.view.height <= world.height

def test_screen_to_world_coords(camera):
    screen = camera.screen_to_world(80, 50)
    assert screen == (180, 150)

def test_world_to_screen_coords(camera):
    screen = camera.world_to_screen(140, 200)
    assert screen == (40, 100)

def test_tiles_visible_to_entity(camera, entity, world):
    entity.x, entity.y = 20, 20
    world.add_room(10, 10, rogue.room.rect_room(30, 30))

    # all tiles should be visible to player
    seen_tiles = camera.tiles_seen_by(world, entity)
    assert world.tiles == seen_tiles

def test_entity_visible_to_entity(camera, entity, world):
    seen_entities = camera.entities_seen_by(world, entity)
    assert entity in seen_entities

def test_entities_visible_to_entity(camera, entity, world):
    entity.x, entity.y = 20, 20

    entities = []
    entities.append(Entity(x=30, y=30))
    entities.append(Entity(x=26, y=30))
    entities.append(Entity(x=25, y=20))
    entities.append(Entity(x=24, y=80))

    for entity in entities:
        world.add_entity(entities)

    world.add_room(10, 10, rogue.room.rect_room(30, 30))

    seen_entities = camera.entities_seen_by(world, entity)

    # All entities should be visible except the fourth one
    for i, entity in enumerate(entities):
        if i == 3:
            assert entity not in seen_entities
        else:
            assert entity in seen_entities

