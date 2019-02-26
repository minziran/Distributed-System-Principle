import sys
import zmq
import os
import logging
import time
from kazoo.client import *
import random


class ZMQ_subscriber():
    def __init__(self, server_IP, sub_ID, topic):

        try:
            logging.basicConfig(filename='Subscriber' + str(sub_ID) + '.log', level=logging.DEBUG)
            self.ID = sub_ID
            self.pub_IP = None
            self.pub_Port = '5556'
            self.isConnected = False
            self.server_address = server_IP + ':2181'
            self.zk_node = KazooClient(hosts=self.server_address)
            print ("===  topics ", topic,'===')
            self.topic = topic
            self.IP_topic = {}
            self.create_ZKCli()

        except Exception as e:
            print(e)
            print("bring down zmq subscriber")
        finally:
            pass
            self.socket.close()
            self.context.term()





    def create_ZKCli(self):

        self.zk_node.start(timeout=9999999)
        while self.zk_node.state != KazooState.CONNECTED:
            pass

        znode_path = '/Subscribers/' + str(self.ID)
        self.zk_node.create(path=znode_path, value=b'', ephemeral=True, makepath=True)
        while self.zk_node.exists(znode_path) is None:
            pass

        pub_path = '/Publishers'
        while self.zk_node.exists(pub_path) is None:
            pass
        data, state = self.zk_node.get(pub_path)
        # print("^_^", state)
        # print(data.decode("utf-8"))
        temp= data.decode("utf-8").split(' ')
        for index, key in enumerate(temp):
            # print("Index, key ", index, key)
            if index%2 == 1:
                if key not in self.IP_topic:
                    self.IP_topic[key] = temp[index - 1]
                else:
                    self.IP_topic[key] = self.IP_topic[key] + ' ' + temp[index - 1]
            else:
                pass

        @self.zk_node.DataWatch(path=pub_path)
        def watch_pub(data, state):
            if state is None:
                self.isConnected = False
                print('===Lost connection===')
            elif self.isConnected is False:
                # print("(_) ", self.IP_topic)
                temp_list = self.IP_topic[self.topic].split(' ')
                random_index = random.randint(0, len(temp_list))
                self.pub_IP = temp_list[random_index]
                self.register_sub()



    def register_sub(self):
        # print("In register_sub")
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        # print("PUB_IP PUB_PORT",self.pub_IP, self.pub_Port)
        addr = "tcp://" + self.pub_IP + ":" + self.pub_Port
        self.socket.connect(addr)
        # socket.connect("tcp://127.0.0.1:5200")
        # for key in self.topic_list:
        #     # print("key "+ key)
        #     self.socket.setsockopt_string(zmq.SUBSCRIBE, key)
        self.socket.setsockopt_string(zmq.SUBSCRIBE, self.topic)
        print("===Already Registered Subscriber===")
        self.notify()

    def notify(self):

        while True:
            print('In notify')
            msg = self.socket.recv_string()
            print(msg)
            temp = msg.split(' ', 1)
            topic = temp[0]
            temp1 = temp[1]
            # print(topic)
            # print(time)
            # print(value)
            print(msg)
            temp = msg.split(' ')
            info = str(time.time()) + ' ' + str(time.time() - float(temp[1]))
            logging.info(info)


if __name__=="__main__":

    ZMQ_subscriber(sys.argv[1], int(sys.argv[2]),sys.argv[3])
    # ZMQ_subscriber('127.0.0.1', 1, 'Lights')

