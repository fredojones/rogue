
from rogue.queue import queue

def test_adding_printing_message():
    queue.append("hello world")
    assert len(queue) == 1
    assert str(queue) == "hello world"
    queue.append("another message")
    assert len(queue) == 2
    assert str(queue) == "hello world\nanother message"
