
class Item:
    """ Holds information about item.

    Attributes:
    name -- item name
    desc -- item description

    equippable -- true if item is equippable
    slot -- if equippable, this is the slot it will be equipped in
    """

    def __init__(self, name, desc="", equippable=False, slot=None):
        self.name = name
        self.desc = desc
        self.equippable = equippable
        self.slot = slot

