import pytest
from rogue.entity import Entity

@pytest.fixture
def entity():
    return Entity(x=100, y=100)

def test_entity_initialize(entity):
    assert entity.x == 100
    assert entity.y == 100

