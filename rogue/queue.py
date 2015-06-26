

class Queue():
    """ Message queue to send messages to the player.

    Attributes:
    (x, y) -- on-screen position at which to draw queue to
    lines  -- number of lines to draw from the message queue
    """

    def __init__(self, x=0, y=0, lines=7):
        self.x = x
        self.y = y
        self.lines = lines
        self.messages = []

    def set_position(self, x, y):
        """ Set queue to on-screen position x, y. """
        self.x, self.y = x, y

    def append(self, message):
        """ Push a new string into the message queue. """
        self.messages.append(message)

    def draw(self, window, lines=5):
        """ Print `self.lines` messages to the screen
            at position (self.x, self.y)

        Keyword arguments:
        window -- curses window to draw to
        """

        # Get the last "lines" messages
        for i, message in enumerate(reversed(self.messages[-lines:])):
            window.addstr(self.y + i, self.x, '{}\n'.format(message))

    def clear(self):
        """ Clear all of the messages. """
        self.messages.clear()

    def __str__(self):
        return '\n'.join(self.messages)

    def __len__(self):
        return len(self.messages)


""" Default message queue instance. """
queue = Queue()
