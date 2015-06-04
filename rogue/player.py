from .entity import Entity
from .tile   import Tile
from .keys   import Keys
from .queue  import queue

class Player(Entity):
    """ Player class controlled by the user. """

    def __init__(self, x=0, y=0):
        super().__init__(x, y, tile=Tile.player, solid=True,
                         tag='player', name='player')
        
    def attack_move(self, x, y, world):
        """ Moves as normal but also attacks enemy if enemy is in square
            being moved to.
        """
        # Deal damage if moving into enemy
        entity = world.get_entity_at(x, y)
        if entity is not None and entity.tag == 'enemy':
            # Player deals damage
            damage = self.calculate_damage(entity)
            entity.health -= damage
            queue.append("hit {} with {} for {} hp!".format(entity.name,
                self.get_slot("right hand").name, damage))

            # Enemy deals damage
            damage = entity.calculate_damage(self)
            self.health -= damage
            queue.append("{} hit player for {} hp!".format(entity.name, damage))


        self.move(x, y, world)

    def update(self, game, key):
        """ Update the game for the player, moving them depending
            on the key pressed. """

        if key == Keys.up:
            self.attack_move(self.x, self.y - 1, game.world)
        if key == Keys.down:
            self.attack_move(self.x, self.y + 1, game.world)
        if key == Keys.left:
            self.attack_move(self.x - 1, self.y, game.world)
        if key == Keys.right:
            self.attack_move(self.x + 1, self.y, game.world)
        if key == Keys.up_left:
            self.attack_move(self.x - 1, self.y - 1, game.world)
        if key == Keys.down_left:
            self.attack_move(self.x - 1, self.y + 1, game.world)
        if key == Keys.up_right:
            self.attack_move(self.x + 1, self.y - 1, game.world)
        if key == Keys.down_right:
            self.attack_move(self.x + 1, self.y + 1, game.world)

        game.camera.center_on(self, game.world)

        super().update(game, key)

