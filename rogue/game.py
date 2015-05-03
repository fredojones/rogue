import curses
from world import World
from camera import Camera

class Game:
    """ Curses game. Call run with curses.wrapper to start. """

    def __init__(self):
        """ Setup default game. """
        self.world = World(width=1000, height=1000)
        self.camera = Camera()

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




def main():
    game = Game()
    curses.wrapper(game.run)

if __name__ == '__main__':
    main()
