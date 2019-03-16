'''
A class for storing the message history.

'''

from collections import deque


class HistoryQueue:
    def __init__(self, _maxSize):
        self.msg_queue = deque()
        self.max_size = _maxSize

    def push_message(self, _text):
        if len(self.msg_queue) == self.max_size:
            self.msg_queue.pop()

        self.msg_queue.appendleft(_text)



if __name__ == "__main__":
    test = HistoryQueue(5)

    for i in range(0, 20):
        test.push_message(i)

    print(list(test.msg_queue))
