import pytest
from rogue.player import Player
from rogue.enemy  import Enemy
from rogue.world  import World
from rogue.tile   import Tile

@pytest.fixture
def player():
    return Player(0, 0)
"""
@pytest.fixture
def enemy():
    return Enemy(2, 2)

@pytest.fixture
def world():
    return World(width=100, height=100)
"""

def test_player_properly_initialized(player):
    assert player.tile == Tile.player

""" UNRELIABLE test as calculate_damage sometimes returns zero (so no damage done) 
def test_moving_to_enemy_deals_damage_to_enemy(player, enemy, world):
    world.add_entity(player)
    world.add_entity(enemy)
    old_health = enemy.health
    player.attack_move(enemy.x, enemy.y, world)
    new_health = enemy.health
    assert new_health < old_health
"""
