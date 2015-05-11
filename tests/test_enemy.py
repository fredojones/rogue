import pytest
from rogue.enemy import Enemy

@pytest.fixture
def enemy():
    return Enemy(x=100, y=100)

def test_enemy_initialize(enemy):
    assert enemy.x == 100
    assert enemy.y == 100
    assert enemy.health == 100

