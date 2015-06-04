""" Assign keys to functions. """
from . import views

def get_loot(game):
    """ Get loot from corpse. """
    pass

""" Dictionary between the key to enter a given function. """
key_functions = {'e': views.inventory,
                 ';': get_loot}

