""" Assign keys to functions. """
from functools import partial

from . import views
from .queue import queue
from .world import World
from .tile import Tile


def get_loot(game):
    """ Get loot from corpse that player is standing on. """
    x, y = game.player.x, game.player.y

    entities = game.world.get_entities_at(x, y)
    try:
        for entity in entities:
            if entity.tag == 'corpse':
                corpse = entity
                break
        # If no corpse found, return
        else:
            return
    except IndexError:
        return

    items = corpse.get_loot()
    for item in items:
        game.player.add_item(item)
        queue.append("picked up a {}".format(item.name))

    corpse.items.clear()

def wait(game):
    """ Wait for a tick to generate some health. """
    game.player.add_health(round(game.player.max_health / 10))
    queue.append("Rested for 1 tick...")

def quit(game):
    """ Ask the player if they want to quit or not. """
    queue.append("Are you sure you want to quit? (y/n)")
    queue.draw(game.window)

    while True:
        key = game.window.getkey()
        queue.clear()

        if key == 'y':
            return 'quit'
        elif key == 'n':
            return None
        else:
            queue.append("Please enter y or n")
            queue.draw(game.window)


def move(game, dirn):
    """ Issue a player.attack_move(..) command in the direction given by dirn.

        Where dirn is 'up' for up, 'left' for left, 'upleft' for up left etc.
    """
    player = game.player

    # Don't move if dead
    if player.dead:
        return

    if dirn == 'up':
        player.attack_move(player.x, player.y - 1, game.world)
    if dirn == 'down':
        player.attack_move(player.x, player.y + 1, game.world)
    if dirn == 'left':
        player.attack_move(player.x - 1, player.y, game.world)
    if dirn == 'right':
        player.attack_move(player.x + 1, player.y, game.world)
    if dirn == 'upleft':
        player.attack_move(player.x - 1, player.y - 1, game.world)
    if dirn == 'downleft':
        player.attack_move(player.x - 1, player.y + 1, game.world)
    if dirn == 'upright':
        player.attack_move(player.x + 1, player.y - 1, game.world)
    if dirn == 'downright':
        player.attack_move(player.x + 1, player.y + 1, game.world)

def up_floor(game):
    """ Move the player up a world if they are on an up tile and not on lowest floor. """
    if game.world.get_tile(game.player.x, game.player.y) == Tile.up:
        if game.world_index > 0:
            game.world_index -= 1
        else:
            return quit(game)

def down_floor(game):
    """ Move the player down a world if they are on an down tile and not on highest floor. """
    if game.world.get_tile(game.player.x, game.player.y) == Tile.down:
        game.world_index += 1

        # Generate new world if it doesn't exist yet
        if game.world == None:
            # The first room of this new world will be where the player
            # currently is
            game.world = World.Dungeon_World(width=1000, height=1000,
                    room_x = game.player.x - 2, room_y = game.player.y - 2)
            # Put exit where the player is
            game.world.set_tile(game.player.x, game.player.y, Tile.up)

            # Add player to the new world
            game.world.add_entity(game.player)

def open_door(game):
    """ Open door if player is standing adjacent to it (can also be done
        by walking into the door). """
    tiles = game.world.get_tiles_surrounding(game.player.x, game.player.y)

    for p, tile in tiles.items():
        if tile == Tile.door:
            game.world.set_tile(*p, tile=Tile.door_open)

def close_door(game):
    """ Close door if player is standing adjacent to it. """
    tiles = game.world.get_tiles_surrounding(game.player.x, game.player.y)

    for p, tile in tiles.items():
        if tile == Tile.door_open:
            game.world.set_tile(*p, tile=Tile.door)

""" Dictionary between the key to enter a given function. """
key_functions = {'e': views.inventory,
                 'c': views.character,
                 ';': get_loot,
                 '.': wait,
                 '?': views.help_general,
                 'q': quit,

                 '<': up_floor,
                 '>': down_floor,

                 'O': open_door,
                 'C': close_door,

                 'k':         partial(move, dirn='up'),
                 'KEY_UP':    partial(move, dirn='up'),
                 'j':         partial(move, dirn='down'),
                 'KEY_DOWN':  partial(move, dirn='down'),
                 'h':         partial(move, dirn='left'),
                 'KEY_LEFT':  partial(move, dirn='left'),
                 'l':         partial(move, dirn='right'),
                 'KEY_RIGHT': partial(move, dirn='right'),
                 'y':         partial(move, dirn='upleft'),
                 'b':         partial(move, dirn='downleft'),
                 'u':         partial(move, dirn='upright'),
                 'n':         partial(move, dirn='downright')}
