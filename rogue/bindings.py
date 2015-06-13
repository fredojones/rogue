""" Assign keys to functions. """
from . import views
from .queue import queue
from .keys import Keys

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

def quit(game):
    return 'quit'

""" Dictionary between the key to enter a given function. """
key_functions = {'e': views.inventory,
                 'c': views.character,
                 ';': get_loot,
                 '?': views.help_general,
                 'q': quit}

