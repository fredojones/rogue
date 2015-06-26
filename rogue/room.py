""" Functions to generate tile based features. """
from .tile import Tile


def rect_room(width, height):
    """ Generate width x height room.

    Return a dictionary, {(x, y): Tile} """

    room = {}

    for x in range(width):
        for y in range(height):
            # Add the walls on the outside of the room
            if y == 0 or x == 0 or x == width - 1 or y == height - 1:
                room[(x, y)] = Tile.wall
            else:
                room[(x, y)] = Tile.floor

    return room

def cardinal_corridor(dirn, length):
    """ Generate a corridor in direction dirn for distance length.

    Keyword arguments:
    start -- the initial point of the corridor
    dirn -- 'N' for up, 'S' for down, 'E' for right, 'W' for left
    length -- distance to extend corridor for
    """
    room = {}

    if dirn == 'N':
        for y in range(length):
            room[(-1, -y)] = Tile.wall
            room[( 0, -y)] = Tile.floor
            room[(+1, -y)] = Tile.wall
        return room

    if dirn == 'S':
        for y in range(length):
            room[(-1, +y)] = Tile.wall
            room[( 0, +y)] = Tile.floor
            room[(+1, +y)] = Tile.wall
        return room

    if dirn == 'E':
        for x in range(length):
            room[(+x, -1)] = Tile.wall
            room[(+x,  0)] = Tile.floor
            room[(+x, +1)] = Tile.wall
        return room

    if dirn == 'W':
        for x in range(length):
            room[(-x, -1)] = Tile.wall
            room[(-x,  0 )] = Tile.floor
            room[(-x, +1)] = Tile.wall
        return room
