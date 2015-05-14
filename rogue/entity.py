import random
from .tile import Tile

class Entity(object):
    """ Base entity class.

    Attributes:
    x -- x position in world space
    y -- y position in world space
    health -- hp left

    tile -- character representing the object
    solid -- whether entity is solid, i.e. whether this space can be moved
             into by other solid entities

    tag -- tag to use to identify types of entity (e.g. 'enemy' or 'player')

    attack -- attacking power of entity
    defense -- defensive power of entity

    items -- list of items held by entity
    equipment -- dictionary of equipped items {"slot": Item}
    """
    def __init__(self, x, y, health=100, tile=Tile.clear, solid=False, tag=''):
        self.x = x
        self.y = y
        self.health = health
        self.tile = tile
        self.solid = solid
        self.tag = tag
        self.items = []
        self.equipment = {}

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
        if self.health <= 0:
            game.world.remove_entity(self)

    @property
    def attack(self):
        """ Calculate the attack of the entity. Default to 1 """
        return 1

    @property
    def defense(self):
        """ Calculate the defense of the entity. Default to 1 """
        return 1

    def calculate_damage(self, entity):
        """ Calculate attack damage done to other entity, based on
            attack and defense.
        """
        damage = random.uniform(0.6, 2) * self.attack - entity.defense
        return damage if damage > 0 else 0

    def add_item(self, item):
        """ Add item to the entity's inventory. """
        self.items.append(item)

    def remove_item(self, item):
        """ Remove item from the entity's inventory. """
        self.items.remove(item)

    def equip(self, item):
        """ Equip item into slot given by item.slot
        
        Also adds item if not already in inventory.

        Raises ValueError if the item isn't an equipment
        """
        if not item.equippable:
            raise ValueError("Item not equippable")
        if item not in self.items:
            self.add_item(item)

        self.equipment[item.slot] = item

    def get_slot(self, slot):
        """ Get equipment from given slot. """
        return self.equipment[slot]

    def __str__(self):
        return self.tile

