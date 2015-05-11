from .tile import Tile

class Entity(object):
    """ Base entity class.

    Attributes:
    x -- x position in world space
    y -- y position in world space
    tile -- character representing the object
    """
    def __init__(self, x, y, tile=Tile.clear):
        self.x = x
        self.y = y
        self.tile = tile

    def move(self, x, y, world):
        """ Move to non-wall space x, y, in the world.

        Keyword arguments:
        x -- coordinate to move to along the x axis
        y -- same for the y axis
        world -- the current game World object

        Returns True if moved, False otherwise
        """

        if world.is_wall(x, y):
            return False
        else:
            self.x = x
            self.y = y
            return True

    def update(self, game, key):
        """ Update the entity.

        Keyword arguments:
        game -- current Game object representing game state
        key -- key pressed this frame
        """
        pass

    def __str__(self):
        return self.tile
