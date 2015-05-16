import json
from pdb import *

class Item:
    """ Holds information about item.

    Attributes:
    name -- item name
    desc -- item description

    kind -- item type

    equippable -- true if item is equippable
    slot -- if equippable, this is the slot it will be equipped in
            things are equippable in right hand by default, for hilarity

    stats -- dictionary of item stats, must have attack if equippable

    durability -- how many more hits the item can be used for
    """

    def __init__(self, name=None, desc=None, kind=None,
                 equippable=None, slot=None,
                 stats=None, durability=None):

        if name is None: name = ''
        if desc is None: desc = ''
        if kind is None: kind = 'weapon'
        if equippable is None: equippable = True
        if slot is None: slot = 'right hand'
        if stats is None: stats = {"attack": 0}

        self.name = name
        self.desc = desc
        self.kind = kind
        # needed to cast 'false' to True
        self.equippable = bool(equippable == True) 
        self.slot = slot
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
            stats = item.get('stats')
            durability = item.get('durability')

            items[name] = (cls(name, desc, kind, equippable, slot, stats, durability))
       
        return items
