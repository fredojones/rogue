import pytest
from rogue.player import Player
from rogue.item   import Item

@pytest.fixture
def player():
    return Player(0, 0)

@pytest.fixture
def item():
    return Item(name='apple', desc='a tasty apple')


def test_adding_items_to_inventory(player):
    player.add_item(item)
    player.add_item(item)
    player.add_item(item)

    assert len(player.items) == 3
    assert player.items[0] == item

