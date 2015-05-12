import random
from .tile import Tile

class Entity(object):
    """ Base entity class.

    Attributes:
    x -- x position in world space
    y -- y position in world space
    health -- hp left
    tile -- character representing the object
    solid -- whether entity is solid, i.e. whether this space can be moved into
             by other solid entities
    """
    def __init__(self, x, y, health=100, tile=Tile.clear, solid=False):
        self.x = x
        self.y = y
        self.health = health
        self.tile = tile
        self.solid = solid

    def move(self, x, y, world):
        """ Move to non-wall space x, y, in the world.

        Keyword arguments:
        x -- coordinate to move to along the x axis
        y -- same for the y axis
        world -- the current game World object

        Returns True if moved, False otherwise
        """

        # Non-solid entities can move anywhere!
        if not self.solid:
            self.x = x
            self.y = y
            return True

        if world.is_wall(x, y):
            return False

        # Don't allow movement into solid entity
        entity = world.get_entity_at(x, y)
        if entity is not None and entity.solid:
            return False

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

    def attack(self):
        """ Calculate the attack of the entity. Default to 1 """
        return 1

    def defense(self):
        """ Calculate the defense of the entity. Default to 1 """
        return 1

    def calculate_damage(self, entity):
        """ Calculate attack damage done to other entity, based on
            attack and defense.
        """
        damage = random.uniform(0.6, 2) * self.attack() - entity.defense()
        return damage if damage > 0 else 0

    def __str__(self):
        return self.tile

