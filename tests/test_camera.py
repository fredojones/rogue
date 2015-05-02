import pytest
from rogue.camera import Camera

@pytest.fixture
def camera():
    return Camera(x=100, y=100, width=100, height=100)

def test_camera_initialize(camera):
    assert camera.view.x == 100
    assert camera.view.y == 100
    assert camera.view.width == 100
    assert camera.view.height == 100

