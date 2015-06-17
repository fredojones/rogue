import pytest
from rogue.enemy  import Enemy
from rogue.world  import World
from rogue.player import Player
from rogue.camera import Camera

class Dummy_Game(object):
    pass

@pytest.fixture
def camera():
    return Camera()

@pytest.fixture
def player():
    return Player(x=100, y=102)

@pytest.fixture
def world():
    return World(width=200, height=200)

@pytest.fixture
def enemy():
    return Enemy(x=100, y=100)

@pytest.fixture
def game():
    game = Dummy_Game()
    game.world = world()
    game.camera = camera()
    game.player = player()
    game.enemy = enemy()
    game.world.add_entity(game.player)
    game.world.add_entity(game.enemy)
    return game

""" unstable because we use a random() > 0.3 predicate
    in the enemy update

def test_enemy_moves_towards_player(game):
    game.world.update(game)
    assert game.enemy.x == 100
    assert game.enemy.y == 101

    game.player.x = 102
    game.player.y = 100

    game.world.update(game)

    assert game.enemy.x == 101
    assert game.enemy.y == 100
""" 
