
class Entity:
    """ Base entity class. """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, x, y, world):
        """ Move to non-wall space x, y, in world.
            returns true if moved, false otherwise """

        if world.is_wall(x, y):
            return False
        else:
            self.x = x
            self.y = y
            return True
