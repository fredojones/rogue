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
    """ Display the game inventory.

    Allows player to manipulate items and equipment etc.
    """

    # Offset for displaying list on-screen
    x, y = 6, 2
    # Currently selected item
    selection = 0
    # Max number of items shown at once
    max_items = 10
    # Number of items scrolled through so far
    scrolled = 0
    # Offset for messages
    x_msg, y_msg = 2, max_items + 4

    game.window.clear()
    while True:
        # Draw selection cursor
        game.window.addstr(y + selection - scrolled, x - 4, CURSOR)

        # Get items between current scroll amount and max_items
        items = list(enumerate(game.player.items))[scrolled:scrolled+max_items]

        # Print each item in inventory
        for i, item in items:
            game.window.addstr(i + y - scrolled, x, '{}: {}\n'.format(i, item.name))

            # If equipped, put a little star next to the item
            if game.player.get_slot('right hand') == item:
                game.window.addstr(i + y - scrolled, x - 2, '*')
        
        key = game.window.getkey()

        if key == 'k':
            if selection > 0:
                selection -= 1

            # If the user tries to go above the screen, scroll up by one
            if selection < scrolled:
                scrolled -= 1

            game.window.clear()

        if key == 'j':
            if selection < len(game.player.items) - 1:
                selection += 1
            
            # If the user tries to go below the screen, scroll down by one
            if selection > scrolled + max_items - 1:
                scrolled += 1

            game.window.clear()

        if key == 'e':
            # Equip the selected item
            if game.player.items[selection].equippable:
                game.player.equip(game.player.items[selection])
                game.window.clear()
            else:
                game.window.addstr(y_msg, x_msg, "Cannot equip non-equippable item")

        if key == 'c':
            # Eat the selected item
            if game.player.items[selection].kind == 'food':
                heal = game.player.items[selection].stats['hp']
                game.player.eat(game.player.items[selection])

                # Put selection cursor back to an item
                selection -= 1
                game.window.clear()
            else:
                game.window.addstr(y_msg, x_msg, "Cannot eat non-food item")

        if key == 'l':
            # Print the item name and description
            item = game.player.items[int(selection)]
            game.window.addstr(y_msg, x_msg, '{}\n\n{}'.format(item.name, item.desc))

        if key == 'q':
            break

        if key == '?':
            help_inventory(game)
            continue

def character(game):
    """ Display information about the player character. """

    while True:
        game.window.clear()

        game.window.addstr('{} the level {} adventurer'.format(game.player.name,
            game.player.level()))

        game.window.addstr('\n\nWielding a {} in the right hand'.format(
            game.player.get_slot('right hand').name))

        game.window.addstr('\n\n{} hp'.format(game.player.health))

        key = game.window.getkey()

        if key == 'q':
            break

def hud(game):
    """ Heads up display shown during game. """

    # Offsets for where to start drawing the HUD
    x, y = game.camera.view.width + 2, 2

    # Display basic player info
    game.window.addstr(y, x, '{} the level {} adventurer'.format(
        game.player.name, game.player.level()))

    # Render health bar using a linear interpolation of the health to max_health
    bar_width = 15
    hearts_full = round((game.player.health / game.player.max_health) * bar_width)

    # Use = to represent life, - to represent lack of life
    bar = 'hp: {}{} {}/{}'.format('=' * hearts_full, '-' * (bar_width - hearts_full),
            game.player.health, game.player.max_health)

    game.window.addstr(y + 2, x, bar) 

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



