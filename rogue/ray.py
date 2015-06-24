""" Simple ray caster. Cast a ray from a point to find each square the
    ray intersects, etc. """

import math
from collections import namedtuple

from .tile import Tile


def ray_cast(point, angle, world):
    """ Return list of tiles and list of entities intersected by a ray shot out from
        point at angle, the lists being sorted by the order the tiles
        are intersected.

        Stops when at a clear tile.

        Returns the lists grouped in a tuple (tiles, entities)

        The list of tiles is a list of tuples with the first element being a
        tuple point (x, y) and the second element being the tile.

        The list of entities will just be a plain list of entities.

    Keyword Arguments:
    point -- point at which to raycast from
    angle -- angle in degrees at which to shoot the ray, 0 being +x axis
    world -- current world
    """

    Result = namedtuple("Result", ['tiles', 'entities'])
    res = Result(tiles=[], entities=[])

    # TODO: Handle angle properly, right now it can't handle multiples of 90 deg
    slope = math.tan(math.radians(angle))
    
    if angle == 0:
        slope = 0
    if angle % 90 == 0:
        pass

    x = 0
    while True:
        # Minus since y axis becomes more negative as we go up the axes
        y = -math.floor(slope * x)

        # Get tiles and entities at this point
        x1, y1 = x + point.x, y + point.y

        if world.get_tile(x1, y1) == Tile.clear:
            break

        res.tiles.append(((x1, y1), world.get_tile(x1, y1)))
        res.entities.extend(world.get_entities_at(x1, y1))

        x += 1

    return res

