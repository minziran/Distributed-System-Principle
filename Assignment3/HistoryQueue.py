'''
A class for storing the message history.

'''

from collections import deque
from itertools import islice


class HistoryQueue:
    def __init__(self, _maxSize):
        self.msg_queue = deque()
        self.max_size = _maxSize

    def push_message(self, _text):
        if len(self.msg_queue) == self.max_size:
            self.msg_queue.pop()

        self.msg_queue.appendleft(_text)

    def get_message(self, _num=1):
        '''
        A method for get history
        :param _num:
        :return: an iterable
        '''
        # If the buffer is too small
        if _num > self.max_size:
            print("The history buffer is not large enough!")
            return

        # If the messages are not enough
        if _num > len(self.msg_queue):
            print("There is not enough messages!")
            return

        return islice(self.msg_queue, 0, _num)


if __name__ == "__main__":
    test = HistoryQueue(5)

    for i in range(0, 20):
        test.push_message(i)

    print(list(test.msg_queue))
    print(list(test.get_message(3)))
    test.get_message(7)
