""" Views accessible by key bindings. """
import curses

CURSOR = '->'

def help_inventory(game):
    """ Print inventory help to screen. """
    game.window.clear()

    res = """Inventory screen

    up and down to select item

    e to equip item
    l to examine

    ? -- this help
    """

    game.window.addstr(res)
    game.window.getch()


def inventory(game):
    # Offsets for list
    x, y = 6, 2
    # Currently selected item
    selection = 0
    # Max number of items shown at once
    max_items = 10
    # Number of items scrolled through so far
    scrolled = 0

    while True:
        game.window.clear()

        # Draw selection cursor
        game.window.addstr(y + selection - scrolled, x - 4, CURSOR)

        # Get items between current scroll amount and max_scroll
        items = list(enumerate(game.player.items))[scrolled:scrolled+max_items]

        # List each item in inventory
        for i, item in items:
            game.window.addstr(i + y - scrolled, x, '{}: {}\n'.format(i, item.name))

            # If equipped, put a little star next to if
            if game.player.get_slot('right hand') == item:
                game.window.addstr(i + y - scrolled, x - 2, '*')
        
        key = game.window.getkey()

        if key == 'KEY_UP':
            if selection > 0:
                selection -= 1

            # If the user tries to go above the screen, scroll up by one
            if selection < scrolled:
                scrolled -= 1


        if key == 'KEY_DOWN':
            if selection < len(game.player.items) - 1:
                selection += 1
            
            # If the user tries to go below the screen, scroll down by one
            if selection > scrolled + max_items - 1:
                scrolled += 1


        if key == 'q':
            break

        if key == '?':
            help_inventory(game)
            continue

        if key == 'e':
            # Equip the item selected
            game.player.equip(game.player.items[selection])

        if key == 'l':
            # Print the item name and description
            item = game.player.items[int(selection)]
            game.window.addstr(10, 2, '{}\n\n{}'.format(item.name, item.desc))
            game.window.getkey()


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
    game.window.addstr(9, 1, "j  k  l")
    game.window.addstr(10, 1, "m     .")

    game.window.addstr(12, 1, "move towards enemies to attack them")
    
    game.window.addstr(14, 1, "press e to enter inventory view")
    game.window.addstr(15, 1, "press ? for help")
    game.window.addstr(15, 1, "press q to quit")

    game.window.getch()



