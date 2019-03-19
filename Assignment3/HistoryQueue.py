'''
A class for storing the message history.

'''

from collections import deque
from itertools import islice
from typing import Dict


class subHistory:
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
        :param _num: the number of history need to get
        :return: an iterable
        '''
        # If the buffer is too small
        if _num > self.max_size:
            print("The history buffer is not large enough!\n")
            return

        # If the messages are not enough
        if _num > len(self.msg_queue):
            print("There is not enough messages!\n")
            return

        return islice(self.msg_queue, 0, _num)


class HistoryQueue:
    def __init__(self, _maxSize):
        self.topic_history: Dict[str, subHistory] = dict()
        self.max_size = _maxSize

    def push_history(self, _topic, _message):

        if not(_topic in self.topic_history):
            self.topic_history[_topic] = subHistory(self.max_size)

        self.topic_history[_topic].push_message(_message)

    def get_history(self, _topic, _history_num):
        if not(_topic in self.topic_history):
            print("No history in this topic! \n")
            return
        else:
            return list(self.topic_history[_topic].get_message(_history_num))

    def get_all_history(self):
        result = str()
        for key in self.topic_history.keys():
            localHis = ",".join(list(self.topic_history[key].msg_queue))
            result = result + key + "#" + localHis + "&"

        return result

    def input_all_history(self, history_str):
        if history_str is None:
            print("the history is empty")
            return

        # Clean the dictionary
        self.topic_history.clear()

        historyList = history_str.split('&')
        for item in historyList:
            localHis = item.split('#')
            topic = localHis[0]
            self.topic_history[topic] = subHistory(self.max_size)

            content = localHis[1].split(',')
            for element in content:
                self.topic_history[topic].push_message(element)


if __name__ == "__main__":
    test = HistoryQueue(5)

    test.push_history('1', '2')
    print(list(test.get_history('1', 1)))
    test.get_history('1', 3)
    test.get_history('2', 1)
