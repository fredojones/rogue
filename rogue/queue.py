

class Queue():
    """ Message queue to send messages to the player. """
    messages = []

    def append(self, message):
        """ Push a new string into the message queue. """
        self.messages.append(message)

    def draw(self, window, x, y, lines=5):
        """ Print the current messages to the curses window
            in a box at point (x, y)

        Keyword arguments:
        window -- curses window to draw to
        x, y   -- screen coordinates to draw to
        lines  -- number of messages to print
        """

        # Get the last "lines" messages
        for i, message in enumerate(self.messages[-lines:]):
            window.addstr(y + i, x, '{}\n'.format(message))


    def __str__(self):
        return '\n'.join(self.messages)

    def __len__(self):
        return len(self.messages)


""" Module-level global representing default message queue. """
queue = Queue()
