import curses
from .tile   import Tile
from .world  import World
from .enemy  import Enemy
from .debug  import debug
from .camera import Camera
from .player import Player
from .keys   import Keys
from .queue  import queue
from .item   import Item

class Game(object):
    """ Curses game. Call run with curses.wrapper to start. """

    def __init__(self):
        """ Setup default game. """
        self.world = World.Dungeon_World(width=1000, height=1000)
        self.camera = Camera()

        # Get all items
        self.items = Item.get_all_json(open("rogue/data/items.json"))

        self.player = Player()
        self.player.random_floor_tile(self.world)
        self.player.equip(self.items['sword of azereon'])
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
        queue.draw(self.window, x=3, y=20)

        key = chr(self.window.getch())
        if key == Keys.quit:
            return "quit"

        self.world.update(self, key)



def main():
    game = Game()
    curses.wrapper(game.run)

if __name__ == '__main__':
    main()
