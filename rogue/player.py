from .entity import Entity
from .tile import Tile

class Player(Entity):
    """ Player class controlled by the user.

    Attributes:
    items -- list containing items held by player """

    def __init__(self, x, y):
        self.items = []
        super(Player, self).__init__(x, y, Tile.player)

    def update(self, game, key):
        """ Update the game for the player, moving them depending
            on the key pressed. """

        if key == ord('i'):
            self.move(self.x, self.y - 1, game.world)
        if key == ord(','):
            self.move(self.x, self.y + 1, game.world)
        if key == ord('j'):
            self.move(self.x - 1, self.y, game.world)
        if key == ord('l'):
            self.move(self.x + 1, self.y, game.world)
        if key == ord('u'):
            self.move(self.x - 1, self.y - 1, game.world)
        if key == ord('m'):
            self.move(self.x - 1, self.y + 1, game.world)
        if key == ord('o'):
            self.move(self.x + 1, self.y - 1, game.world)
        if key == ord('.'):
            self.move(self.x + 1, self.y + 1, game.world)

        game.camera.center_on(self, game.world)

    def add_item(self, item):
        self.items.append(item)
