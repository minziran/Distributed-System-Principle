from kazoo.client import *
import zmq
import csv
import time
import sys


class ZMQ_publihser_NB():

    def __init__(self,server_IP,pub_ID,topic,my_IP,ownership):

        try:
            self.ID = pub_ID
            self.topic = topic
            self.ownership = ownership
            self.isConnected = False
            self.server_address = server_IP + ':2181'
            self.zk_node = KazooClient(hosts=self.server_address)
            self.IP = my_IP
            # self.sub_IP = None
            # self.sub_address = None

            self.context = None
            self.socket = None
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
            temp = temp.replace(' ','')
            # print("After_temp", temp)
            self.zk_node.set(path='/Publishers', value=str(temp).encode('utf-8'))
            self.socket.close()
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
        print(self.zk_node.get('/Publishers').__getitem__(0).decode('utf-8')) # value at index [0]
        if self.zk_node.get('/Publishers').__getitem__(0).decode('utf-8') is '':
            # print(True)
            self.zk_node.set(path='/Publishers', value=str(temp).encode('utf-8'))
        else:
            # print("$_$")
            temp_1 = self.zk_node.get('/Publishers').__getitem__(0).decode('utf-8') + " " + temp
            self.zk_node.set( path = '/Publishers',value =str(temp_1).encode('utf-8') )

        while self.zk_node.exists(znode_path) is None:
            pass

        #
        # sub_path = '/Subscribers'
        # while self.zk_node.exists(sub_path) is None:
        #     pass
        # data, state = self.zk_node.get(sub_path)
        # self.sub_IP = data.decode("utf-8")
        #
        # @self.zk_node.DataWatch(path=sub_path)
        # def watch_leader(data, state):
        #     if state is None:
        #         self.isConnected = False
        #         print('===Lost connection===')
        #     elif self.isConnected is False:
        #         self.sub_address = data.decode("utf-8")
        #         self.socket = None
        #         self.register_pub()



    def register_rep(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind("tcp://*:%s" % '5556')
        print("===Already Register Publisher===")
        self.publish()

    def publish(self):
    	history = 5
        while True:
            with open('./test_topic_files/' + self.topic + '.csv', newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for row in spamreader:
                    self.socket.send_string(self.topic + " " +str(time.time()) + ' ' + self.ownership + history + ', '.join(row))
                    print(', '.join(row))
                    time.sleep(3)



if __name__ == '__main__':
    # ZMQ_publihser_NB('127.0.0.1', 1, 'Lights','127.0.0.1',1)
    ZMQ_publihser_NB(sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4], int(sys.argv[5]))
