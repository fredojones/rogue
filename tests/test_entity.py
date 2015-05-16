import pytest
from rogue.entity import Entity
from rogue.world import World
from rogue.item import Item
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
    return World(width=100, height=100)

@pytest.fixture
def item():
    return Item(name='apple', desc='a juicy apple', equippable=False)

@pytest.fixture
def equipment():
    return Item(name='sword', desc='a rusty sword', equippable=True, slot='weapon')

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

def test_calculating_damage(entity):
    damage = entity.calculate_damage(entity)
    assert damage is not None

def test_remove_on_next_update_if_health_negative(entity, world):
    world.add_entity(entity)
    assert entity in world.entities
    entity.health = -1
    game = Dummy_Game()
    game.world = world
    entity.update(game, ' ')
    assert entity not in world.entities
    
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

def test_equipping_non_equipment_raises_error(entity, item):
    with pytest.raises(ValueError): 
        entity.equip(item)

