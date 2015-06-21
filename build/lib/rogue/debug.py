import pdb, curses

def debug():
    curses.nocbreak()
    curses.echo()
    curses.endwin()
    import pdb; pdb.set_trace()
