import curses, os
from copy import deepcopy

from .tile   import Tile
from .world  import World
from .enemy  import Enemy
from .camera import Camera
from .player import Player
from .queue  import queue
from .item   import Item
from . import bindings
from . import views
from . import colors


class Game(object):
    """ Main game class. Call run with curses.wrapper to start. """

    def __init__(self):
        # Get all items
        items_file = os.path.join(os.path.dirname(__file__), 'data/items.json')
        self.items = Item.get_all_json(open(items_file))

        # Set the queue screen position
        queue.set_position(3, 20)
        queue.lines = 7

        """ World setup. """
        # Current floor in the game, 0 is the first floor, the index for self.worlds
        self.world_index = 0

        # Dict containing each world in the game
        self.worlds = {}

        # Setup the first world
        self.worlds[0] = World.Dungeon_World(width=1000, height=1000,
                room_x = 500, room_y = 500)

        self.camera = Camera()

        # Setup the player
        self.player = Player()
        #self.player.random_floor_tile(self.world)
        self.player.x = self.world.width//2 + 2
        self.player.y = self.world.height//2 + 2

        self.player.equip(deepcopy(self.items['steel longsword']))
        self.player.add_item(deepcopy(self.items['worn axe']))
        self.player.add_item(deepcopy(self.items['apple']))
        self.world.add_entity(self.player)

        self.camera.center_on(self.player, self.world)

        # Make sure player is visible
        if not self.camera.is_visible(self.player):
            raise Exception()

        # Equip all enemies with knives
        for entity in self.world.entities:
            if entity.tag == 'enemy':
                entity.equip(deepcopy(self.items['rusty knife']))

    def run(self, window):
        """ Run main curses game with curses window. """
        self.window = window
        self.window.keypad(1)
        curses.curs_set(0)
        colors.start_colors()

        while True:
            if self.update() == "quit":
                return

    def update(self):
        self.camera.draw(self.window, self.world, point=(self.player.x, self.player.y))

        # Draw heads up display
        views.hud(self)

        # Refresh the messages on screen
        queue.draw(self.window)

        key = self.window.getkey()

        # Get function depending on key pressed
        fn = bindings.key_functions.get(key)
        # Only execute if function exists for that key
        if fn is not None:
            res = fn(self)
            if res == 'quit':
                return 'quit'

        self.world.update(self)
        self.window.clear()

    @property
    def world(self):
        """ Get the current game world at world_index.

        Return None of no world at self.world_index.
        """
        return self.worlds.get(self.world_index)

    @world.setter
    def world(self, value):
        """ Set the current world at world_index. """
        self.worlds[self.world_index] = value


def main():
    game = Game()
    curses.wrapper(game.run)

if __name__ == '__main__':
    main()
