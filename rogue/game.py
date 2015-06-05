import curses
from copy import deepcopy

from .tile   import Tile
from .world  import World
from .enemy  import Enemy
from .camera import Camera
from .player import Player
from .keys   import Keys
from .queue  import queue
from .item   import Item
from . import bindings


class Game(object):
    """ Main game class. Call run with curses.wrapper to start. """

    def __init__(self):
        """ Setup default game. """
        self.world = World.Dungeon_World(width=1000, height=1000)
        self.camera = Camera()

        # Get all items
        self.items = Item.get_all_json(open("rogue/data/items.json"))

        self.player = Player()
        self.player.random_floor_tile(self.world)
        self.player.equip(deepcopy(self.items['steel longsword']))
        for _ in range(19):
            self.player.add_item(deepcopy(self.items['worn axe']))
        self.world.add_entity(self.player)

        self.camera.center_on(self.player, self.world)

        # Make sure player is visible
        if not self.camera.is_visible(self.player):
            raise Exception()

        # Generate some enemies!
        for _ in range(10):
            enemy = Enemy()
            enemy.random_floor_tile(self.world)
            self.world.add_entity(enemy)
            enemy.equip(self.items['rusty knife'])


    def run(self, window):
        """ Run main curses game with curses window. """
        self.window = window
        self.window.keypad(1)
        curses.curs_set(0)

        while True:
            if self.update() == "quit":
                return

    def update(self):
        self.camera.draw(self.window, self.world)

        # Refresh the messages on screen
        queue.draw(self.window, x=3, y=20, lines=7)

        key = self.window.getkey()
       
        # Get function depending on key pressed
        fn = bindings.key_functions.get(key)
        # Only execute if function exists for that key
        if fn is not None:
            res = fn(self)
            if res == 'quit':
                return 'quit'

        self.world.update(self, key)
        self.window.clear()



def main():
    game = Game()
    curses.wrapper(game.run)

if __name__ == '__main__':
    main()
