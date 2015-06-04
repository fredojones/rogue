""" Assign keys to functions. """
import curses

""" Views """
def inventory(game):
    curses.echo()
    x, y = 4, 2
    while True:
        game.window.clear()
        for i, item in enumerate(game.player.items):
            game.window.addstr(i + y, x, '{}: {}\n'.format(i+1, item.name))
        
        key = game.window.getkey()

        if key == 'q':
            return
    

""" Dictionary between the key to enter a given function. """
key_functions = {'e': inventory}
