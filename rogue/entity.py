
class Entity:
    """ Base entity class.

    Attributes:
    x -- x position in world space
    y -- y position in world space
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

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
