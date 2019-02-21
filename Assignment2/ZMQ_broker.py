import zmq
import sys
import time
from kazoo.client import *

class ZMQ_broker:
    def __init__(self, id, server_IP, my_IP):
        # try:
            self.ID = id
            self.address = my_IP
            self.publisher_Port = '5556'
            self.subscriber_Port = '5557'
            self.server_address = server_IP + ':2181'
            self.zk_node = KazooClient(hosts=self.server_address)
            self.leader_flag = False

            self.context = None

            self.frontend = None

            self.backend = None

            self.create_ZKCli()

            # self.events = zmq.device(zmq.FORWARDER, self.frontend, self.backend)

        # except Exception as e:
        #     print(e)
        #     print("bring down zmq device")
        # finally:
        #     pass
        #     self.frontend.close()
        #     self.backend.close()
        #     self.context.term()

    def start_broker(self):
        self.context = zmq.Context(1)
        # socket facing publisher
        self.frontend = self.context.socket(zmq.SUB)
        addr1 = "tcp://*:" + self.publisher_Port
        self.frontend.bind(addr1)
        # frontend.connect("tcp://127.0.0.1:5556")
        self.frontend.setsockopt_string(zmq.SUBSCRIBE, "")
        # socket facing suscriber
        self.backend = self.context.socket(zmq.PUB)
        addr2 = "tcp://*:" + self.subscriber_Port
        self.backend.bind(addr2)
        print("Broker is already connected...... ")

        self.events = zmq.device(zmq.FORWARDER, self.frontend, self.backend)

    def create_ZKCli(self):

        if self.zk_node.state != KazooState.CONNECTED:
            self.zk_node.start()
        while self.zk_node.state != KazooState.CONNECTED:
            pass

        if self.zk_node.exists('/Brokers') is None:
            self.zk_node.create(path='/Brokers', value=b'', ephemeral=False, makepath=True)
        while self.zk_node.exists('/Brokers') is None:
            pass

        my_path = '/Brokers/' + str(self.ID) #ID int
        self.zk_node.create(path=my_path, value=b'', ephemeral=True, makepath=True)
        while self.zk_node.exists(my_path) is None:
            pass

        leader_path = '/Leader'
        if self.zk_node.exists(leader_path):
            self.leader_flag = False
            self.watch_mode()
        else:

            self.zk_node.create(leader_path, value=self.address.encode('utf-8'), ephemeral=True, makepath=True)
            while self.zk_node.exists(path=leader_path) is None:
                pass
            self.leader_flag = True
            self.start_broker()


    def win_election(self):
        leader_path = '/Leader'
        if self.zk_node.exists(path=leader_path) is None:
            self.zk_node.create(leader_path, value=self.address.encode('utf-8'), ephemeral=True, makepath=True)
        while self.zk_node.exists(path=leader_path) is None:
            pass

        self.leader_flag = True
        self.start_broker()

    def watch_mode(self):

        election_path = '/Brokers/'
        leader_path = '/Leader'

        @self.zk_node.DataWatch(path=leader_path)
        def watch_leader(data, state):
            if self.zk_node.exists(path=leader_path) is None:
                time.sleep(5)
                election = self.zk_node.Election(election_path, self.ID)
                election.run(self.win_election)



if __name__ == '__main__':

    ZMQ_broker(int(sys.argv[1]), 'localhost', sys.argv[2])
    # ZMQ_broker(sys.arg[2], 'localhost', '10.0.0.2')
