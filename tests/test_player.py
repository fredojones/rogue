import pytest
from rogue.player import Player
from rogue.enemy  import Enemy
from rogue.world  import World
from rogue.tile   import Tile
from rogue.keys   import Keys
from rogue.camera import Camera
from rogue.bindings import key_functions

class Dummy_Game(object):
    pass

@pytest.fixture
def camera():
    return Camera()

@pytest.fixture
def player():
    return Player(0, 0)

@pytest.fixture
def world():
    return World(width=100, height=100)

@pytest.fixture
def game():
    game = Dummy_Game()
    game.world = world()
    game.camera = camera()
    game.player = player()
    return game

"""
@pytest.fixture
def enemy():
    return Enemy(2, 2)
"""

def test_player_properly_initialized(player):
    assert player.tile == Tile.player

"""
    UNRELIABLE test as calculate_damage sometimes returns zero (so no damage done) 
def test_moving_to_enemy_deals_damage_to_enemy(player, enemy, world):
    world.add_entity(player)
    world.add_entity(enemy)
    old_health = enemy.health
    player.attack_move(enemy.x, enemy.y, world)
    new_health = enemy.health
    assert new_health < old_health
"""

def test_moving_into_empty_space(game):
    key_functions.get(Keys.down)(game)
    assert game.player.y == 1

def test_moving_into_occupied_space(game):
    game.world.set_tile(0, 1, Tile.wall)
    key_functions.get(Keys.down)(game)
    assert game.player.y == 0

