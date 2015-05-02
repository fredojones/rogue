from enum import Enum

class Tile(Enum):
    """ Character representation of each tile. """
    wall  = '#'
    floor = '.'
    clear = ' '
    exit  = '<'
