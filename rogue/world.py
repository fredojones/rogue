from tile import Tile

class World:
    """ Holds information about the current world. """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.Empty_Tiles(width, height, Tile.floor)

    def set_tile(self, x, y, tile):
        """ Set tile at x, y to tile. """
        self.tiles[y][x] = tile

    def get_tile(self, x, y):
        """ Get tile at x, y. """
        if x < 0 or y < 0 or x > self.width or y > self.height:
            raise IndexError("Tile out of range")
        return self.tiles[y][x]

    def is_wall(self, x, y):
        """ True if tile at x, y is a wall. """
        return self.get_tile(x, y) == Tile.wall

    @staticmethod
    def Empty_Tiles(width, height, tile):
        """ Return width x height matrix filled with tile. """
        return [[tile for _ in range(width)] for _ in range(height)]
