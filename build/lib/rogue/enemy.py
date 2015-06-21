import random
from .entity import Entity
from .tile   import Tile
from .queue  import queue

class Enemy(Entity):
    """ Enemy class, will attack player etc. """

    def __init__(self, x=0, y=0, health=10, tile=Tile.enemy):
        super().__init__(x=x, y=y, health=health, tile=tile, solid=True,
                         name='goblin', tag='enemy', color_pair=20)

    def update(self, game):
        """ Update the enemy, will move towards the player randomly-ish.
        
        Enemy will move directly towards the player with some chance.
        """

        # Make sure within range of player
        if self.distance(game.player) < 6:
            # Random each direction
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

        # Attack player if in range
        for entity in game.world.get_entities_surrounding(self.x, self.y):
            if entity.tag == 'player':
                # Deal damage to the player
                damage = self.calculate_damage(entity)
                entity.add_health(-damage)
                queue.append("{} hit player with {} for {} hp!".format(self.name,
                self.get_slot("right hand").name, damage))

        super().update(game)

