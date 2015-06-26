""" Simple ray caster. Cast a ray from a point to find each square the
    ray intersects, etc. """

import math
from collections import namedtuple

from .tile import Tile


def ray_cast(point, angle, radius, world):
    """ Return a list of (x, y) tuple points which the ray passes through.
        Stops when at a wall tile, door tile, or radius is reached.
        Result will be sorted by tile visited first.

    Keyword Arguments:
    point  -- (x, y) point at which to raycast from
    angle  -- angle in degrees at which to shoot the ray, 0 being straight up
    radius -- integer radius at which to stop casting the ray
    world  -- current world
    """

    res = []

    # Adjacent over hypotenuse (x coordinate)
    o_h = math.sin(angle)
    # Opposite over hypotenuse (y coordinate)
    a_h = math.cos(angle)

    for h in range(radius):
       x, y = round(o_h * h), round(a_h * h)

       # Transform to world space
       x1, y1 = x + point[0], y + point[1]

       res.append((x1, y1))

       # Break if we've gotten to a wall
       tile = world.get_tile(x1, y1)
       if tile == Tile.wall or tile == Tile.door:
           break

    return res

def ray_cast_circle(point, radius, world, step=1):
    """ Return the set of unique (x, y) tuple points which rays shot out at equal angle
        intervals `step` from a given point `point` intersect.
    """

    res = []

    for a in range(0, 360, step):
        res.extend(ray_cast(point=point, radius=radius, angle=a, world=world))

    # Ignore duplicates
    return set(res)
