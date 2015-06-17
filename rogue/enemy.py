import random
from .entity import Entity
from .tile import Tile

class Enemy(Entity):
    """ Enemy class, will attack player etc. """

    def __init__(self, x=0, y=0, health=10, tile=Tile.enemy):
        super().__init__(x=x, y=y, health=health, tile=tile, solid=True,
                         name='goblin', tag='enemy')

    def update(self, game):
        """ Update the enemy, will move towards the player randomly-ish.
        
        Enemy will move directly towards the player with some chance.
        """

        if random.random() > 0.3:
            if game.player.x > self.x:
                self.move(self.x + 1, self.y, game.world)
        if random.random() > 0.3:
            if game.player.x < self.x:
                self.move(self.x - 1, self.y, game.world)
        if random.random() > 0.3:
            if game.player.y > self.y:
                self.move(self.x, self.y + 1, game.world)
        if random.random() > 0.3:
            if game.player.y < self.y:
                self.move(self.x, self.y - 1, game.world)

        super().update(game)

