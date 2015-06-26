import pytest
from rogue.entity import Entity, InventoryError, EquipmentError
from rogue.world import World
from rogue.item import Item
from rogue.item import unarmed
from rogue.tile import Tile

class Dummy_Game(object):
    pass

@pytest.fixture
def entity():
    return Entity(x=100, y=100, health=100, solid=True)

@pytest.fixture
def entity2():
    return Entity(x=94, y=20, health=100, solid=True)

@pytest.fixture
def world():
    return World(width=200, height=200)

@pytest.fixture
def item():
    return Item(name='apple', desc='a juicy apple', kind='food', equippable=False,
            stats={"hp": 50})

@pytest.fixture
def equipment():
    return Item(name='sword', desc='a rusty sword', equippable=True,
            kind='weapon', slot='right hand', stats={"attack": 100})

def test_entity_initialize(entity):
    assert entity.x == 100
    assert entity.y == 100
    assert entity.health == 100

def test_move_to_empty_space(entity, world):
    assert entity.move(10, 12, world)
    assert entity.x == 10
    assert entity.y == 12

def test_move_solid_entity_into_wall(entity, world):
    world.set_tile(10, 12, Tile.wall)
    assert not entity.move(10, 12, world)
    assert not entity.x == 10
    assert not entity.y == 12

def test_move_non_solid_entity_into_wall(entity, world):
    entity.solid = False
    world.set_tile(10, 12, Tile.wall)
    assert entity.move(10, 12, world)
    assert entity.x == 10
    assert entity.y == 12

def test_move_solid_entity_into_other_solid_entity(entity, entity2, world):
    world.add_entity(entity2)
    assert not entity.move(entity2.x, entity2.y, world)
    assert not entity.x == entity2.x
    assert not entity.y == entity2.y

def test_move_non_solid_entity_into_other_solid_entity(entity, entity2, world):
    entity.solid = False
    world.add_entity(entity2)
    assert entity.move(entity2.x, entity2.y, world)
    assert entity.x == entity2.x
    assert entity.y == entity2.y

def test_move_entity_into_door_opens_door(entity, world):
    x, y = 102, 104
    world.set_tile(x, y, Tile.door)
    assert not entity.move(x, y, world)
    # Door should have now opened
    #assert world.get_tile(x, y)
    assert entity.move(x, y, world)

def test_calculating_damage(entity):
    damage = entity.calculate_damage(entity)
    assert damage is not None

def test_entity_becomes_corpse_on_next_update_when_dead(entity, world):
    world.add_entity(entity)
    assert entity in world.entities
    entity.health = -1
    game = Dummy_Game()
    game.world = world
    entity.update(game)
    assert entity.tag == 'corpse'

def test_adding_items_to_inventory(entity, item):
    entity.add_item(item)
    entity.add_item(item)
    entity.add_item(item)

    assert len(entity.items) == 3
    assert entity.items[0] == item

def test_removing_items_from_inventory(entity):
    item1 = Item(name='apple')
    item2 = Item(name='orange')
    item3 = Item(name='banana')

    entity.add_item(item1)
    entity.add_item(item2)
    entity.add_item(item3)

    entity.remove_item(item2)
    assert len(entity.items) == 2
    assert entity.items[0] == item1
    assert entity.items[1] == item3

def test_equipping_equipment(entity, equipment):
    assert equipment not in entity.items
    assert equipment not in entity.equipment.values()
    entity.equip(equipment)
    assert equipment in entity.items
    assert equipment in entity.equipment.values()
    assert entity.get_slot(equipment.slot) == equipment
    entity.unequip(equipment)
    assert equipment not in entity.equipment.values()
    assert entity.get_slot(equipment.slot) == unarmed

def test_equipping_non_equipment_raises_error(entity, item):
    with pytest.raises(EquipmentError):
        entity.equip(item)

def test_adding_fist_to_inventory_raises_error(entity):
    with pytest.raises(InventoryError):
        entity.add_item(unarmed)

def test_equipping_fist_raises_error(entity):
    with pytest.raises(EquipmentError):
        entity.equip(unarmed)

def test_unequipping_fist_raises_error(entity):
    with pytest.raises(EquipmentError):
        entity.unequip(unarmed)

def test_placing_on_random_floor_tile(entity, world):
    world.set_tile(10, 12, Tile.floor)
    p = world.random_floor_tile()
    entity.random_floor_tile(world)
    assert entity.x == p.x == 10
    assert entity.y == p.y == 12

def test_generating_loot(entity, item, equipment):
    entity.add_item(item)
    assert entity.get_loot()[0] == item
    entity.add_item(equipment)
    assert len(entity.get_loot()) > 0

def test_getting_current_level_with_default_scaling(entity):
    entity.exp = 100
    assert entity.level() == 3
    entity.exp = 10000000000000
    assert entity.level() == 999

def test_getting_current_level_with_any_scaling(entity):
    for i, exp in enumerate(entity.levels):
        entity.exp = exp
        assert entity.level() == i

def test_eating_food_increases_health_and_destroys_item(entity, item):
    old_health = entity.health
    entity.add_item(item)
    entity.eat(item)
    assert entity.health == old_health + item.stats['hp']
    assert item not in entity.items

def test_eating_non_food_raises_value_error(entity, equipment):
    entity.add_item(equipment)
    with pytest.raises(ValueError):
        entity.eat(equipment)

def test_eating_food_not_in_inventory_raises_error(entity, item):
    with pytest.raises(InventoryError):
        entity.eat(item)

def test_raises_key_error_if_food_doesnt_have_hp_stat(entity, item):
    del item.stats['hp']
    with pytest.raises(KeyError):
        entity.add_item(item)
        entity.eat(item)

def test_adding_health(entity):
    entity.health = entity.max_health
    old_health = entity.health

    entity.add_health(-10)
    assert entity.health == old_health - 10
    entity.add_health(6)
    assert entity.health == old_health - 4

def test_adding_above_max_health(entity):
    entity.health = entity.max_health
    old_health = entity.health

    entity.add_health(10)
    assert entity.health == old_health
    entity.add_health(-4)
    entity.add_health(10)
    assert entity.health == old_health

def test_calculating_distance(entity):
    entity.x = 10
    entity.y = 10
    entity2 = Entity(x=13, y=14)
    assert entity.distance(entity2) == 5
