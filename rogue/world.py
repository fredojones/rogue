import random
from . import room
from .tile import Tile
from .enemy import Enemy
from collections import namedtuple

class World(object):
    """ Holds information about the current world.

    Attributes:
    width -- width of the game world
    height -- same for height

    tiles -- dictionary holding the information about tiles in the game
             keys: tuple (x, y) denoting position
             values: Tile object representing tile at that point

    tiles_seen -- set of (x, y) points that have been seen at some point,
                  tiles at these points will be rendered in grey.

    entities -- list of Entity object in the world

    dark -- true if the world is dark, i.e. shorter "render" distance
    """

    def __init__(self, width, height, default_tile=Tile.clear, dark=False):
        self.width = width
        self.height = height
        self.tiles = self.Empty_Tiles(width, height, default_tile)
        self.dark = dark
        self.tiles_seen = set()
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

        Probably best not to use this but instead cache all the floor tiles,
        or else pretty slow for a large world.

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

    def get_entities_of_tag(self, tag):
        """ Get list of entities with tag `tag`. If none, empty list. """
        return list(filter(lambda entity: entity.tag == tag, self.entities))
        
    def get_tiles_surrounding(self, x, y):
        """ Get dict of [(x, y) : Tile] in the 8 squares surrounding x, y. """
        result = {}
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                # Skip square at (x, y)
                if dx == 0 and dy == 0:
                    continue
                result[(x + dx, y + dy)] = self.get_tile(x + dx, y + dy)
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
    def Dungeon_World(World, width, height, room_x, room_y):
        """ Generate new dungeon with randomly generated features.

        Returns new World object.

        Keyword Arguments:
        width -- width of game world
        height -- height of game world
        room_x -- x position of first room added
        room_y -- y position of first room added
        """

        def get_walls(origin, tiles):
            """ Get list of points corresponding to the walls added
                by added the room tiles at origin.

            Keyword arguments:
            walls -- list of points corresponding to walls in the world
            origin -- tuple (x, y) at which to "add" room
            tiles -- dict where key is point and value is tile at that point

            return new list of points corresponding to walls
            """

            res = []
            for p, tile in tiles.items():
                if tile == Tile.wall:
                    # Transform into world coordinates from the room coordinates
                    p1 = (p[0] + origin[0], p[1] + origin[1])
                    res.append(p1)

            return res

        def pick_random_wall(walls):
            """ Choose a random wall tile that is adjacent (non-diagonal)
                to a clear (empty space) tile.

                walls is a list of points corresponding to walls in the world.

                Return a tuple of the wall tile, and the direction
                toward the clear tile.

                Return False if no walls found that are adjacent to clear tile
            """

            def direction_to_clear_tile(point):
                """ Return direction 'N', 'S', 'E', 'W' towards SINGLE clear tile.

                Return None if no clear tile found or if more than 1 found. """
                x, y = point

                tiles = [world.get_tile(x + 1, y), world.get_tile(x - 1, y),
                         world.get_tile(x, y + 1), world.get_tile(x, y - 1)]

                # Don't allow more than 1 clear tile
                if len(list(filter(lambda x: x == Tile.clear, tiles))) > 1:
                    return None

                if world.get_tile(x, y - 1) == Tile.clear:
                    return 'N'
                if world.get_tile(x, y + 1) == Tile.clear:
                    return 'S'
                if world.get_tile(x + 1, y) == Tile.clear:
                    return 'E'
                if world.get_tile(x - 1, y) == Tile.clear:
                    return 'W'
                return None

            # Loop through each wall until wall is found that is
            # adjacent to a clear tile, then return the direction and wall
            for _ in range(100):
                wall = random.choice(walls)
                dirn = direction_to_clear_tile(wall)
                if dirn is not None:
                    return (wall, dirn)
            else:
                return False


        # Number of attempts to add a new feature
        MAX_ITERS = 1000

        # Initialize the new world, with a random chance to be a "dark" world
        if random.random() > 0.8:
            dark = True
        else:
            dark = False

        world = World(width, height, dark=dark)

        """ List of lists of points corresponding to walls in the game

        Each list in this list corresponds to walls of a feature (room, corridor, etc.)

        What happens is each time a feature is generated, its list of wall tiles is
        appended to this list. When we want to get a random wall tile to extend
        a feature from we first choose a random list of wall tiles, and then
        get the random wall tile from that list. This gives us an equal
        chance of choosing a corridor and a room; there is usually
        more chance of picking a room as they generally have more wall tiles.
        """
        walls = []

        # Add initial room in center of map
        r = room.rect_room(8, 6)
        walls.append(get_walls((room_x, room_y), r))
        world.add_room(room_x, room_y, r)
        world.set_tile(room_x + 2, room_y + 2, Tile.up)

        # Generate the world!
        for _ in range(MAX_ITERS):
            # Pick random feature to pick random wall from
            wallslist = random.choice(walls)
            walldirn = pick_random_wall(wallslist)

            # Skip if no walldirn found
            if not walldirn:
                continue

            x1, y1 = walldirn[0]

            if random.random() > 0.2:
                # build room
                width = random.randrange(5, 12)
                height = random.randrange(5, 12)
                r = room.rect_room(width, height)

                def fits_in_space(start, direction, room):
                    x1, y1 = start

                    for point, tile in room.items():
                        x, y = point
                        if world.get_tile(x1 + x, y1 + y) != Tile.clear:
                            return False

                    return True

                direction = walldirn[1]

                # Allow single space gap depending on direction
                # and put the entrance half way along the room
                if direction == 'N':
                    x_offs = -width // 2
                    y_offs = -2
                if direction == 'S':
                    x_offs = -width // 2
                    y_offs = +2
                if direction == 'E':
                    y_offs = -height // 2
                    x_offs = +2
                if direction == 'W':
                    y_offs = -height // 2
                    x_offs = -2

                # If the room fits, add it
                if fits_in_space((x1 + x_offs, y1 + y_offs), direction, r):
                    # Add the room
                    world.add_room(x1 + x_offs, y1 + y_offs, r)

                    # Patch up the gap with a corridor
                    world.add_room(x1, y1, room.cardinal_corridor(direction, 3))

                    # Add new walls to the walls list
                    walls.append(get_walls((x1 + x_offs, y1 + y_offs), r))

            else:
                # build corridor
                length = random.randrange(6, 14)
                corridor = room.cardinal_corridor(walldirn[1], length)

                def fits_in_space(start, direction, length, corridor):
                    x1, y1 = start

                    for point, tile in corridor.items():
                        # Allow start and end and wall
                        # tiles to overlap with other tiles
                        if tile == Tile.wall:
                            continue

                        if direction == 'E' or direction == 'W':
                            if point[0] == 0 or point[0] == length:
                                continue

                        if direction == 'N' or direction == 'S':
                            if point[1] == 0 or point[1] == length:
                                continue

                        x, y = point
                        if world.get_tile(x1 + x, y1 + y) != Tile.clear:
                            return False

                    return True

                if fits_in_space((x1, y1), walldirn[1], length, corridor):
                    # Add the corridor
                    world.add_room(x1, y1, corridor)

                    # Sometimes add a door connecting the room to the corridor
                    if random.random() > 0.4:
                        world.set_tile(x1, y1, Tile.door)

                    # Add new walls to the walls list
                    walls.append(get_walls((x1, y1), corridor))


        # Patch up all gaps into the outside "world"
        for point, tile in world.tiles.items():
            x, y = point

            # If tile is floor and adjacent to a clear tile, patch the clear tile
            if tile == Tile.floor:
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        # Skip if out of range
                        if (x + dx < 0 or y + dy < 0 or
                            x + dx > world.width - 1 or y + dy > world.height - 1):
                            continue

                        if world.get_tile(x + dx, y + dy) == Tile.clear:
                            world.set_tile(x + dx, y + dy, Tile.wall)


        # Get random floor tiles
        floor_tiles = list(map(lambda x: x[0],
            filter(lambda x: x[1] == Tile.floor, world.tiles.items())))
        random.shuffle(floor_tiles)

        # Add a few random entrances and exits
        for _ in range(5):
            x, y = floor_tiles.pop()
            world.set_tile(x, y, Tile.down)
            x, y = floor_tiles.pop()
            world.set_tile(x, y, Tile.up)

        # Add some enemies
        for _ in range(40):
            enemy = Enemy()
            enemy.x, enemy.y = floor_tiles.pop()
            world.add_entity(enemy)

        return world
