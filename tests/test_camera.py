import pytest
from rogue.camera import Camera
from rogue.entity import Entity
from rogue.world import World

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

