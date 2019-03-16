from collections import deque


class HistoryQueue:
    def __init__(self, _maxSize=1):
        self.msg_queue = deque()
        self.max_size = _maxSize

    def push_message(self, _text):
        if len(self.msg_queue) > self.max_size:
            self.msg_queue.pop()
            self.msg_queue.appendleft(_text)
