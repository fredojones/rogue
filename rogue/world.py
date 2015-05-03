import random
from tile import Tile
from collections import namedtuple

class World:
    """ Holds information about the current world. """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.Empty_Tiles(width, height, Tile.clear)

    def set_tile(self, x, y, tile):
        """ Set tile at x, y to tile. """
        self.tiles[y][x] = tile

    def get_tile(self, x, y):
        """ Get tile at x, y. """
        if x < 0 or y < 0 or x > self.width - 1 or y > self.height - 1:
            raise IndexError("Tile out of range")
        return self.tiles[y][x]

    def is_wall(self, x, y):
        """ True if tile at x, y is a wall. """
        return self.get_tile(x, y) == Tile.wall

    def random_floor_tile(self):
        """ Return position of random floor tile. """
        Point = namedtuple("Point", ['x', 'y'])

        # Keep taking random choice of tiles to see if it is a floor tile
        while True:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.get_tile(x, y) == Tile.floor:
                return Point(x, y)

        return Point(0, 0)

    @staticmethod
    def Empty_Tiles(width, height, tile):
        """ Return width x height matrix filled with tile. """
        return [[tile for _ in range(width)] for _ in range(height)]
