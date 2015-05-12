from .entity import Entity
from .tile import Tile

class Player(Entity):
    """ Player class controlled by the user.

    Attributes:
    items -- list containing items held by player """

    def __init__(self, x, y):
        self.items = []
        super(Player, self).__init__(x, y, tile=Tile.player, solid=True)

    def attack_move(self, x, y, world):
        """ Moves as normal but also attacks enemy if enemy is in square
            being moved to.
        """

        # Deal damage if moving into enemy
        entity = world.get_entity_at(x, y)
        if entity is not None and entity.tag == 'enemy':
            entity.health -= self.calculate_damage(entity)

        self.move(x, y, world)

    def update(self, game, key):
        """ Update the game for the player, moving them depending
            on the key pressed. """

        if key == ord('i'):
            self.attack_move(self.x, self.y - 1, game.world)
        if key == ord(','):
            self.attack_move(self.x, self.y + 1, game.world)
        if key == ord('j'):
            self.attack_move(self.x - 1, self.y, game.world)
        if key == ord('l'):
            self.attack_move(self.x + 1, self.y, game.world)
        if key == ord('u'):
            self.attack_move(self.x - 1, self.y - 1, game.world)
        if key == ord('m'):
            self.attack_move(self.x - 1, self.y + 1, game.world)
        if key == ord('o'):
            self.attack_move(self.x + 1, self.y - 1, game.world)
        if key == ord('.'):
            self.attack_move(self.x + 1, self.y + 1, game.world)

        game.camera.center_on(self, game.world)

        super().update(game, key)

    def add_item(self, item):
        self.items.append(item)
