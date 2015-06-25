import random, math
from .tile import Tile
from . import item as _item

class InventoryError(Exception):
    """ Raised on inventory related errors. """
    pass

class EquipmentError(Exception):
    """ Raised on equipment related errors. """
    pass

class Entity(object):
    """ Base entity class.

    Attributes:
    x -- x position in world space
    y -- y position in world space
    layer -- draw order, lower gets drawn on top
    health -- hp left
    max_health -- maximum hp the entity can have

    dead -- whether or not entity should update

    tile -- character representing the object
    color_pair -- color pair number as set by curses
    solid -- whether entity is solid, i.e. whether this space can be moved
             into by other solid entities

    name -- name of the entity
    tag -- tag to use to identify types of entity (e.g. 'enemy' or 'player')

    exp -- current experience of the entity
    levels -- list containing how much exp is needed for each level

    defense -- defensive power of entity

    items -- list of items held by entity
    equipment -- dictionary of equipped items {"slot": Item}
    """

    def __init__(self, x=0, y=0, health=100, max_health=None, tile=Tile.clear,
                 solid=False, tag='', name='entity', layer=0, color_pair=0):
        self.x = x
        self.y = y
        self.layer = layer
        self.health = health
        self.tile = tile
        self.color_pair = color_pair
        self.solid = solid
        self.name = name
        self.tag = tag

        if max_health is None:
            self.max_health = health

        self.dead = False

        # Generate default levelling scale
        difference = 10
        self.levels = []

        # Exp needed for level is square of the level multiplied by difference
        for level in range(1000):
            self.levels.append(level**2 * difference)

        self.exp = self.levels[10]

        self.attack = 10
        self.defense = 6

        self.items = []
        self.equipment = {}

        # Equip fists
        self.equipment[_item.unarmed.slot] = _item.unarmed

    def level(self):
        """ Calculate the entities level from current exp.
        
        Return the level for which the entities current exp is greater than
        (or equal to) that level, but less than is required for the level
        above it. If the current exp is higher than any level, return the
        highest level.

        Raises ValueError if self.exp is negative
        """

        if self.exp < 0:
            raise ValueError("exp must be positive")

        if self.exp >= self.levels[len(self.levels) - 1]:
            return len(self.levels) - 1

        for level, exp_needed in enumerate(self.levels):
            if self.exp >= exp_needed and self.exp < self.levels[level + 1]:
                return level

        return 0

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

    def distance(self, entity):
        """ Calculate the absolute distance between this and the other entity. """
        return math.sqrt(math.pow(self.x - entity.x, 2) +
                         math.pow(self.y - entity.y, 2))

    def random_floor_tile(self, world):
        """ Place the entity on a random floor tile in the world. """
        p = world.random_floor_tile()
        self.x = p.x
        self.y = p.y

    def update(self, game):
        """ Update the entity.

        Keyword arguments:
        game -- current Game object representing game state
        key -- key pressed this frame
        """
        # Turn into corpse if entity dies
        if self.health <= 0:
            self.name = "Corpse of {}".format(self.name)
            self.solid = False
            self.tile = Tile.corpse
            self.tag = "corpse"
            self.layer = 1
            self.dead = True

    def calculate_damage(self, entity):
        """ Calculate attack damage done to other entity, using modified
            FF's algorithm.
        """
        weapon_damage = self.get_slot("right hand").stats["attack"]
        attacker = self.level() / 2 + weapon_damage
        defender = entity.defense
        return math.floor(((random.random() + 1) * attacker) - defender)

    def add_health(self, hp):
        """ Add hp to the entities health, capping at max health.

        hp can be negative to subtract health, which can go below zero.
        """
        self.health += hp

        if self.health > self.max_health:
            self.health = self.max_health

    def add_item(self, item):
        """ Add item to the entity's inventory. """
        if item == _item.unarmed:
            raise InventoryError("Cannot add fists to inventory")
        self.items.append(item)

    def remove_item(self, item):
        """ Remove item from the entity's inventory. """
        self.items.remove(item)

    def equip(self, item):
        """ Equip non-fist item into slot given by item.slot
        
        Also adds (not unarmed) item if not already in inventory.

        Raises ValueError if the item isn't an equipment, or
        if item == unarmed tries to be equipped
        """
        if item == _item.unarmed:
            raise EquipmentError("Cannot equip fists")
        if not item.equippable:
            raise EquipmentError("Item not equippable")
        if item not in self.items:
            self.add_item(item)

        self.equipment[item.slot] = item

    def unequip(self, item):
        """ Unequip given item. """
        if item == _item.unarmed:
            raise EquipmentError("Cannot unequip fists")

        if item.slot in self.equipment:
            del self.equipment[item.slot]

        # Reset to fists
        self.equipment[item.slot] = _item.unarmed

    def eat(self, item):
        """ Eat the given object with kind='food' raising the player's hp. """
        if item not in self.items:
            raise InventoryError("Food must be in inventory to be eaten")
        if item.kind != 'food':
            raise ValueError("Cannot eat non-food item")
       
        self.health += item.stats['hp']
        self.remove_item(item)

    def get_slot(self, slot):
        """ Get equipment from given slot.
        
        Returns None if nothing equipped in slot.
        """
        return self.equipment.get(slot, None)

    def get_loot(self):
        """ Get random sublist of entity's items. """
        if len(self.items) == 1:
            num_loot = 1
        elif len(self.items) > 1:
            num_loot = random.randint(1, 2)
        else:
            return []

        return random.sample(self.items, num_loot)

    def __str__(self):
        return self.tile

