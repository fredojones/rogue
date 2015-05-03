""" Functions to generate tile based rooms. """
from tile import Tile


def square_room(width, height):
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


