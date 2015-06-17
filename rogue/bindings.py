""" Assign keys to functions. """
from . import views
from .queue import queue
from .keys import Keys
from functools import partial

def get_loot(game):
    """ Get loot from corpse. """
    x, y = game.player.x, game.player.y

    entities = game.world.get_entities_at(x, y)
    try:
        if entities[1].tag == 'corpse':
            corpse = entities[1]
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
    return 'quit'

def move(game, dirn):
    player = game.player

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


""" Dictionary between the key to enter a given function. """
key_functions = {'e': views.inventory,
                 'c': views.character,
                 ';': get_loot,
                 't': wait,
                 '?': views.help_general,
                 'q': quit,
                 
                 Keys.up:         partial(move, dirn='up'),
                 Keys.down:       partial(move, dirn='down'),
                 Keys.left:       partial(move, dirn='left'),
                 Keys.right:      partial(move, dirn='right'),
                 Keys.up_left:    partial(move, dirn='upleft'),
                 Keys.down_left:  partial(move, dirn='downleft'),
                 Keys.up_right:   partial(move, dirn='upright'),
                 Keys.down_right: partial(move, dirn='downright')}

