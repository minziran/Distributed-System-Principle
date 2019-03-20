import zmq
import csv
import time
import socket
import sys
from kazoo.client import *

class ZMQ_publihser():

    def __init__(self, server_IP, pub_ID, topic, ownership):

        try:
            self.ID =pub_ID
            self.broker_Port = '5556'
            self.broker_IP = None
        
            self.ownership_list = ownership.split(',')
            self.isConnected = False
            self.server_address = server_IP + ':2181'
            self.zk_node = KazooClient(hosts=self.server_address)

            self.topic_list = topic.split(',')

            self.context = None
            self.socket = None
            self.create_ZKCli()

        except Exception as e:
            print(e)
            print("bring down zmq publisher")
        finally:
            pass
            self.socket.close()
            self.context.term()


    def create_ZKCli(self):

        if self.zk_node.state != KazooState.CONNECTED:
            self.zk_node.start()
        while self.zk_node.state != KazooState.CONNECTED:
            pass

        znode_path = '/Publishers/' + str(self.ID)
        self.zk_node.create(path=znode_path, value=str(self.ID).encode('utf-8'), ephemeral=True, makepath=True)
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
                self.socket = None
                self.register_pub()



    def register_pub(self):
        print("In register_pub")
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        addr = "tcp://" + self.broker_IP + ":" + self.broker_Port
        self.socket.connect(addr)
        print("===Already Register Publisher===")
        self.publish()

    def publish(self):
        print(self.topic_list)
        for key in self.topic_list:
            # while True:
                with open('./test_topic_files/' + key + '.csv', newline='') as csvfile:
                    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                    for row in spamreader:

                        self.socket.send_string(key + " " + self.ownership_list[self.topic_list.index(key)] + ' ' + str(time.time())+ ' '+str(self.ID) + ' ' + str(row))
                        print(key + " " + self.ownership_list[self.topic_list.index(key)] + ' ' + str(time.time())+' ' +str(self.ID) + ' ' + str(row))
                        time.sleep(3)



if __name__ == '__main__':

    ZMQ_publihser(sys.argv[1], int(sys.argv[2]),sys.argv[3],sys.argv[4])
    # server_IP, pub_ID, topic, ownership
    #ZMQ_publihser('127.0.0.1', 1, 'Lights', 1)