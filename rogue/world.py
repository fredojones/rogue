import random
from . import room
from .tile import Tile
from collections import namedtuple

class World(object):
    """ Holds information about the current world.

    Attributes:
    width -- width of the game world
    height -- same for height
    tiles -- dictionary holding the information about tiles in the game
             keys: tuple (x, y) denoting position
             values: Tile object representing tile at that point
    entities -- list of Entity object in the world
    """

    def __init__(self, width, height, tile=Tile.clear):
        self.width = width
        self.height = height
        self.tiles = self.Empty_Tiles(width, height, tile)
        self.entities = []

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
        """ Return position of a random unoccupied floor tile in the world.

        Returns a namedtuple with attributes (x, y) corresponding to the
        position of the unoccupied floor tile (a floor tile without an entity on it).

        Raise Exception if no unoccupied floor tile found.
        """

        if not Tile.floor in self.tiles.values():
            raise ValueError("No floor tile found")

        Point = namedtuple("Point", ['x', 'y'])

        # Get list all unoccupied floor tiles positions (floor tiles
        # with no entities on them)
        floor_tiles = []
        for (x, y), tile in self.tiles.items():
            if tile == Tile.floor and self.get_entity_at(x, y) == None:
                floor_tiles.append(Point(x, y))

        if len(floor_tiles) == 0:
            raise ValueError("No unoccupied floor tiles")

        # Take random unoccupied floor tile
        return random.choice(floor_tiles)


    def add_entity(self, entity):
        """ Add entity object to the game. """
        self.entities.append(entity)

    def get_entity_at(self, x, y):
        """ Get first found entity at position x, y. If none return None """
        for entity in self.entities:
            if entity.x == x and entity.y == y:
                return entity
        return None

    def get_entities_at(self, x, y):
        """ Get list of entities at position x, y. If none return empty list """
        result = []
        for entity in self.entities:
            if entity.x == x and entity.y == y:
                result.append(entity)
        return result

    def get_entities_surrounding(self, x, y):
        """ Get list of entities in the 8 squares surrounding x, y.

        Return empty list of none found.
        """
        result = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                # Skip square at (x, y)
                if dx == 0 and dy == 0:
                    continue
                result.extend(self.get_entities_at(x + dx, y + dy))
        return result

    def remove_entity(self, entity):
        """ Remove given entity from the world. """
        self.entities.remove(entity)

    def add_room(self, x, y, room):
        """ Add room onto game tiles at specified (x, y) with top left
            corner of the room there.

        Keyword Arguments:
        x -- x coordinate to add room at (TOP LEFT corner of room)
        y -- same for y
        room -- Dictionary {(x, y): Tile} containing room tile info
        """
        for (i, j), tile in room.items():
            self.set_tile(i + x, j + y, tile)


    def update(self, game):
        """ Update the world and all entities in it.

        Keyword arguments:
        game -- current Game object, representing game state
        """
        # Don't update dead entities
        for entity in self.entities:
            if not entity.dead:
                entity.update(game)


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

    @classmethod
    def Dungeon_World(World, width, height):
        """ Generate new dungeon with randomly generated rooms.

        Returns new World object.
        """
        world = World(width, height)

        world.add_room(10, 10, room.square_room(20, 20))

        return world
