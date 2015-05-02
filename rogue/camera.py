from rect import Rect

class Camera:
    """ Draws the current view to the main game screen. """

    def __init__(self, x=0, y=0, width=50, height=15):
        self.view = Rect(x, y, width, height)

    def draw(self, window, world):
        """ Render world tiles to window. """
        for i in range(self.view.width):
            for j in range(self.view.height):
                tile = ord(world.get_tile(i, j))
                window.addch(j, i, ord(world.get_tile(i, j)))

