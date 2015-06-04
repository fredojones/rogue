""" Views accessible by key bindings. """
import curses

def help_inventory(game):
    """ Print inventory help to screen. """
    game.window.clear()

    res = """Inventory screen

    e # -- equip item #
    l # -- examine item #

    # is item number in list

    ? -- this help
    """

    game.window.addstr(res)
    game.window.getch()


def inventory(game):
    curses.echo()
    curses.curs_set(1)

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
            break

        if strin == '?':
            help_inventory(game)
            continue

        """ Accept a string like 'e 9' to equip the 10th item on the list """
        strin = strin.split()

        try:
            int(strin[1])
        except (IndexError, ValueError):
            game.window.addstr(19, 2, 'bad input')
            game.window.getkey()
            continue

        try:
            if strin[0] == 'e':
                # Equip the item selected
                game.player.equip(game.player.items[int(strin[1])])
            elif strin[0] == 'l':
                # Print the item name and description
                item = game.player.items[int(strin[1])]
                game.window.addstr(10, 2, '{}\n\n{}'.format(item.name, item.desc))
                game.window.getkey()
        except IndexError:
            game.window.addstr(19, 2, 'item number out of range')
            game.window.getkey()
            continue

    curses.noecho()
    curses.curs_set(0)


def help_general(game):
    """ Help in world view. """
    game.window.clear()

    game.window.addstr(1, 1, "Movement controls:")
    game.window.addstr(2, 1, "u: up, ul: up left, dr: down right, etc.")
    
    game.window.addstr(3, 1, "ul u ur")
    game.window.addstr(4, 1, "l     r")
    game.window.addstr(5, 1, "dl d dr")

    game.window.addstr(7, 1, "Corresponds to")

    game.window.addstr(8, 1, "u  i  o")
    game.window.addstr(9, 1, "j     l")
    game.window.addstr(10, 1, "m  ,  .")

    game.window.addstr(12, 1, "move towards enemies to attack them")
    
    game.window.addstr(14, 1, "press e to enter inventory view")
    game.window.addstr(15, 1, "press ? for help")
    game.window.addstr(15, 1, "press q to quit")

    game.window.getch()



