import curses
from world import World
from camera import Camera
from player import Player
from tile import Tile
from debug import debug

class Game(object):
    """ Curses game. Call run with curses.wrapper to start. """

    def __init__(self):
        """ Setup default game. """
        self.world = World.Dungeon_World(width=1000, height=1000)
        self.camera = Camera()

        self.player = Player(0, 0)
        self.world.add_entity(self.player)

        random_point = self.world.random_floor_tile()
        self.player.x = random_point.x
        self.player.y = random_point.y

        self.camera.center_on(self.player, self.world)

        if not self.camera.is_visible(self.player):
            raise Exception()

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

        key = self.window.getch()
        if key == ord('q'):
            return "quit"

        self.world.update(self, key)




def main():
    game = Game()
    curses.wrapper(game.run)

if __name__ == '__main__':
    main()
