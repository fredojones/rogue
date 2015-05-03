import pytest
from rogue.camera import Camera
from rogue.entity import Entity

@pytest.fixture
def camera():
    return Camera(x=100, y=100, width=100, height=100)

@pytest.fixture
def entity():
    return Entity(x=20, y=20)

def test_camera_initialize(camera):
    assert camera.view.x == 100
    assert camera.view.y == 100
    assert camera.view.width == 100
    assert camera.view.height == 100

def test_entity_on_screen(camera, entity):
    assert not camera.is_visible(entity)
    entity.x = 110
    entity.y = 120
    assert camera.is_visible(entity)

def test_camera_center_on_entity_makes_entity_visible(camera, entity):
    assert not camera.is_visible(entity)
    camera.center_on(entity)
    assert camera.is_visible(entity)

def test_screen_to_world_coords(camera):
    screen = camera.screen_to_world(80, 50)
    assert screen == (180, 150)

def test_world_to_screen_coords(camera):
    screen = camera.world_to_screen(140, 200)
    assert screen == (40, 100)
