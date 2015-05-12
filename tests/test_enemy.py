import pytest
from rogue.enemy import Enemy

@pytest.fixture
def enemy():
    return Enemy(x=100, y=100)


