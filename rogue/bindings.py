""" Assign keys to functions. """
import curses

""" Views """
def inventory(game):
    curses.echo()
    x, y = 4, 2
    while True:
        game.window.clear()

        # List each item in inventory
        for i, item in enumerate(game.player.items):
            game.window.addstr(i + y, x, '{}: {}\n'.format(i, item.name))

            # If equipped, put a little star next to if
            if game.player.get_slot('right hand') == item:
                game.window.addstr(i + y, x - 2, '*')
        
        strin = game.window.getstr(20, 2).decode().strip()

        if strin == 'q':
            return

        """ Accept a string like 'e 9' to equip the 10th item on the list """
        strin = strin.split()

        try:
            int(strin[1])
        except (IndexError, ValueError):
            game.window.addstr(19, 2, 'bad input')
            game.window.getkey()
            continue


        if strin[0] == 'e':
            try:
                # Equip the item selected
                game.player.equip(game.player.items[int(strin[1])])
            except IndexError:
                game.window.addstr(19, 2, 'item number out of range')
                game.window.getkey()
                continue


""" Dictionary between the key to enter a given function. """
key_functions = {'e': inventory}
