import random
from tile import Tile
from collections import namedtuple

class World:
    """ Holds information about the current world.

    Attributes:
    width -- width of the game world
    height -- same for height
    tiles -- dictionary holding the information about tiles in the game
             keys: tuple (x, y) denoting position
             values: Tile object representing tile at that point
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.Empty_Tiles(width, height, Tile.clear)

    def set_tile(self, x, y, tile):
        """ Set tile at x, y to tile.

        Keyword arguments:
        x -- x coordinate at which to set tile
        y -- same for y coordinate
        tile -- Tile object to set the tile to
        """
        self.tiles[(x, y)] = tile

    def get_tile(self, x, y):
        """ Get tile at x, y.

        Keyword arguments:
        x -- x coordinate to get the tile from
        y -- same for y coordinate

        Returns Tile object at that position

        Raises IndexError if accessing a tile that is out of the map
        """
        if x < 0 or y < 0 or x > self.width - 1 or y > self.height - 1:
            raise IndexError("Tile out of range")
        return self.tiles[(x, y)]

    def is_wall(self, x, y):
        """ True if tile at x, y is a wall, otherwise False. """
        return self.get_tile(x, y) == Tile.wall

    def random_floor_tile(self):
        """ Return position of a random floor tile in the game world.

        Returns a namedtuple with attributes (x, y) corresponding to the
        position of the floor tile.

        Raise Exception if no floor tile found.
        """

        if not Tile.floor in self.tiles.values():
            raise Exception("No floor tile found")

        Point = namedtuple("Point", ['x', 'y'])

        # Keep taking random choice of tiles to see if it is a floor tile
        while True:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.get_tile(x, y) == Tile.floor:
                return Point(x, y)


    @staticmethod
    def Empty_Tiles(width, height, tile):
        """ Generate empty 2D world map.

        Keyword arguments:
        width -- width of the desired game world
        height -- same for height
        tile -- Tile object to fill the world with

        Returns dictionary with keys being a tuple (x, y) corresponding
        to the x and y coordinates, and values being the tile at that point.
        """

        tiles = {}
        for x in range(width):
            for y in range(height):
                tiles[(x, y)] = tile

        return tiles

