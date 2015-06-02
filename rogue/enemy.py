from .entity import Entity
from .tile import Tile

class Enemy(Entity):
    """ Enemy class, will attack player etc. """

    def __init__(self, x=0, y=0, health=10, tile=Tile.enemy):
        super().__init__(x=x, y=y, health=health, tile=tile, solid=True, tag='enemy')

