import sys
import zmq
import os
import logging
import time
from kazoo.client import *

class ZMQ_subscriber():
    def __init__(self, server_IP, sub_ID,topic):

        try:
            logging.basicConfig(filename='Subscriber' + str(sub_ID) + '.log', level=logging.DEBUG)
            self.ID = sub_ID
            self.broker_IP = None
            self.broker_Port = '5557'
            self.isConnected = False
            self.server_address = server_IP + ':2181'
            self.zk_node = KazooClient(hosts=self.server_address)
            print ("===  topics ", topic,'===')
            self.topic_list  =topic.split(' ')
            self.context = None
            self.socket = None
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

        leader_path = '/Leader'
        while self.zk_node.exists(leader_path) is None:
            pass
        data, state = self.zk_node.get(leader_path)
        self.broker_IP = data.decode("utf-8")

        @self.zk_node.DataWatch(path=leader_path)
        def watch_leader(data, state):
            if state is None:
                self.isConnected = False
                print('===Lost connection===')
            elif self.isConnected is False:
                self.leader_address = data.decode("utf-8")
                self.register_sub()



    def register_sub(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        addr = "tcp://" + self.broker_IP + ":" + self.broker_Port
        self.socket.connect(addr)
        # socket.connect("tcp://127.0.0.1:5200")
        for key in self.topic_list:
            # print("key "+ key)
            self.socket.setsockopt_string(zmq.SUBSCRIBE, key)
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

    ZMQ_subscriber('localhost', 1,'Lights Humidity')
    ZMQ_subscriber('localhost', 2, 'Lights Humidity')

