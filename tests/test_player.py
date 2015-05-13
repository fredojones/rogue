import pytest
from rogue.player import Player
from rogue.tile   import Tile

@pytest.fixture
def player():
    return Player(0, 0)

def test_player_properly_initialized(player):
    assert player.tile == Tile.player

