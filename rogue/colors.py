""" Functions and constants for handling curses color. """
import curses

COLOR_ORANGE = 10

def start_colors():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    curses.init_color(COLOR_ORANGE, 600, 400, 250)
    curses.init_pair(3, COLOR_ORANGE, curses.COLOR_BLACK)

