import pytest, io
from rogue.item import Item
from pdb import *

@pytest.fixture
def sample_json():
    return io.StringIO("""
        {
          "items" : [
          {
            "name" : "worn axe",
            "kind" : "weapon",
            "equippable" : true,
            "stats" : {
              "attack" : 10
            },
            "durability" : 200
          },
          {
            "name" : "apple",
            "kind" : "food",
            "equippable" : false,
            "stats" : {
              "attack" : 1,
              "hp" : 20
            },
            "durability" : 2
          }
            ]
        }
        """)

def test_getting_items(sample_json):
    items = Item.get_all_json(sample_json)
    assert items['worn axe'].name == "worn axe"
    assert items['worn axe'].kind == "weapon"
    assert items['worn axe'].stats["attack"] == 10
    assert items['worn axe'].equippable == True
    assert items['apple'].name == "apple"
    assert items['apple'].kind == "food"
    assert items['apple'].equippable == False
    assert items['apple'].stats["hp"] == 20
    assert items['apple'].durability == 2
