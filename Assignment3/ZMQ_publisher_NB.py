from kazoo.client import *
import zmq
import csv
import time
import sys
from HistoryQueue import HistoryQueue


class ZMQ_publihser_NB():

    def __init__(self, server_IP, pub_ID, topic, my_IP, ownership, _his_size):
        self.ID = pub_ID
        self.topic = topic
        self.ownership = ownership
        self.hist_size = _his_size
        self.history = HistoryQueue(_his_size)
        self.isConnected = False
        self.server_address = server_IP + ':2181'
        self.IP = my_IP
        # self.sub_IP = None
        # self.sub_address = None

        self.context = None
        self.socket = None

        try:
            self.zk_node = KazooClient(hosts=self.server_address)
            self.create_ZKCli()
            self.register_rep()

        except Exception as e:
            print(e)
            print("bring down zmq publisher")
        finally:
            pass
            temp = self.zk_node.get('/Publishers').__getitem__(0).decode('utf-8')
            my_info = self.IP + ' ' + self.topic
            print(temp)
            temp = temp.replace(my_info, '')
            temp = temp.replace(' ', '')
            # print("After_temp", temp)
            self.zk_node.set(path='/Publishers', value=str(temp).encode('utf-8'))

            if self.socket:
                self.socket.close()

            if self.context:
                self.context.term()

    def create_ZKCli(self):

        if self.zk_node.state != KazooState.CONNECTED:
            self.zk_node.start()
        while self.zk_node.state != KazooState.CONNECTED:
            pass

        znode_path = '/Publishers/' + str(self.ID)

        temp = self.IP + ' ' + self.topic
        # self.zk_node.set( path = '/Publishers',value =str(temp).encode('utf-8') )
        self.zk_node.create(path=znode_path, value=b'', ephemeral=True, makepath=True)
        # print("(_)")
        print(self.zk_node.get('/Publishers').__getitem__(0).decode('utf-8'))  # value at index [0]
        if self.zk_node.get('/Publishers').__getitem__(0).decode('utf-8') is '':
            # print(True)
            self.zk_node.set(path='/Publishers', value=str(temp).encode('utf-8'))
        else:
            # print("$_$")
            temp_1 = self.zk_node.get('/Publishers').__getitem__(0).decode('utf-8') + " " + temp
            self.zk_node.set(path='/Publishers', value=str(temp_1).encode('utf-8'))

        while self.zk_node.exists(znode_path) is None:
            pass

    def register_rep(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind("tcp://*:%s" % '5556')
        print("===Already Register Publisher===")
        self.publish()

    def publish(self):
        while True:
            with open('./test_topic_files/' + self.topic + '.csv', newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for row in spamreader:
                    # construct a string containing the topic, the message and the ownership
                    temp_message = ','.join(row)
                    self.history.push_history(self.topic, temp_message)

                    temp_message = str(self.ownership) + "#" + self.topic + "#" + temp_message
                    print(temp_message)

                    self.socket.send_string(temp_message)
                    time.sleep(3)


if __name__ == '__main__':
    # ZMQ_publihser_NB('127.0.0.1', 1, 'Lights','127.0.0.1',1)
    if len(sys.argv) < 6:
        print("python3 ZMQ_publisher_NB.py serverIP publisherID topic localIP ownership historySize")
        exit(0)

    ZMQ_publihser_NB(sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4], int(sys.argv[5]), int(sys.argv[6]))
