import json
from pdb import *

class Item:
    """ Holds information about item.

    Attributes:
    name -- item name
    desc -- item description

    kind -- item type

    equippable -- true if item is equippable
    slot -- if equippable, this is the slot the item will be equipped in;
            things are equippable in right hand by default, for hilarity

    throwable -- true if item is throwable
    quantity -- if throwable, how many is left

    stats -- dictionary of item stats, must have attack if equippable

    durability -- how many more hits the item can be used for (-1 if invuln)
    """

    def __init__(self, name=None, desc=None, kind=None,
                 equippable=None, slot=None,
                 throwable=None, quantity=None,
                 stats=None, durability=None):

        if name is None: name = ''
        if desc is None: desc = ''
        if kind is None: kind = 'weapon'
        if equippable is None: equippable = True
        if slot is None: slot = 'right hand'
        if throwable is None: throwable = False
        if quantity is None: quantity = 1
        if stats is None: stats = {"attack": 0}
        if durability is None: durability = -1

        self.name = name
        self.desc = desc
        self.kind = kind
        self.equippable = equippable
        self.slot = slot
        self.throwable = throwable
        self.quantity = quantity
        self.stats = stats
        self.durability = durability

    @classmethod
    def get_all_json(cls, json_file):
        decoded = json.load(json_file)
        
        items = {}

        for item in decoded['items']:
            name = item.get('name')
            desc = item.get('desc')
            kind = item.get('kind')
            equippable = item.get('equippable')
            slot = item.get('slot')
            throwable = item.get('throwable')
            stats = item.get('stats')
            durability = item.get('durability')

            items[name] = cls(name, desc, kind, equippable, slot,
                              throwable, None, stats, durability)
       
        return items

unarmed = Item(name='fists', desc='your fists', kind='weapon', equippable=True,
               slot='right hand', stats={'attack':8}, durability=-1)

