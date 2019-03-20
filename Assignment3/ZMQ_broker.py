import random
import zmq
import sys
import time
from kazoo.client import *
from threading import *


class ZMQ_broker:
    def __init__(self, id, server_IP, my_IP):

        self.ID = id
        self.address = my_IP
        self.publisher_Port = '5556'
        self.subscriber_Port = '5557'
        self.server_address = server_IP + ':2181'
        self.history_Port = '5558'

        self.zk_node = KazooClient(hosts=self.server_address)
        self.leader_flag = False

        self.lock = Lock()

        self.context = None

        self.frontend = None

        self.backend = None

        self.create_ZKCli()

    def start_broker(self):
        self.context = zmq.Context(1)
        # socket facing publisher
        self.frontend = self.context.socket(zmq.SUB)
        addr1 = "tcp://*:" + self.publisher_Port
        self.frontend.bind(addr1)

        self.frontend.setsockopt_string(zmq.SUBSCRIBE, "")

        self.backend = self.context.socket(zmq.PUB)
        addr2 = "tcp://*:" + self.subscriber_Port
        self.backend.bind(addr2)
        print("Broker is already connected...... ")

        while True:
            # print("In while true")
            msg = self.frontend.recv_string()

            temp_list = msg.split(' ')
            temp_topic = temp_list[0]
            temp_msg = temp_list[4]
            temp_time = temp_list[2]
            temp_ID = temp_list[3]
            temp_ownership = temp_list.pop(1)

            send_flag = False
            topic_path = '/Topics/' + temp_topic

            if self.zk_node.exists(topic_path):
                data, state = self.zk_node.get(topic_path)
                pre_ownership = data.decode("utf-8").split(' ')[0]
                # print('preownership '+ pre_ownership)
                if int(pre_ownership) >= int(temp_ownership):
                    send_flag = True
                    temp_str = temp_ownership + ' ' + data.decode("utf-8").split(' ')[1] + ' ' + temp_ID
                    # print('temp_msg ' + temp_str)
                    self.zk_node.set(path=topic_path, value=temp_str.encode('utf-8'))
                else:
                    send_flag = False

            else:
                temp_str = temp_ownership + ' ' + '0' + ' ' + temp_ID
                self.zk_node.create(path=topic_path, value=temp_str.encode('utf-8'), ephemeral=False, makepath=True)
                send_flag = True
            while self.zk_node.exists(topic_path) is None:
                pass
            print('Temp list ' + temp_topic + ' ' + temp_msg)
            if send_flag is True:
                msg = temp_topic + ' ' + temp_msg + ' ' + temp_time
                print('msg ' + msg)

                data, state = self.zk_node.get(topic_path)
                count = int(data.decode("utf-8").split(' ')[1]) + 1
                temp_str = temp_ownership + ' ' + str(count) + ' ' + temp_ID
                self.zk_node.set(path=topic_path, value=temp_str.encode('utf-8'))
                msg_path = topic_path + '/' + str(count)
                # print('msg_path ' + msg_path)

                self.zk_node.create(path=msg_path, value=msg.encode('utf-8'), ephemeral=False, makepath=True)
                while self.zk_node.exists(msg_path) is None:
                    pass

                self.backend.send_string(msg)

            else:
                continue

    def create_ZKCli(self):
        print("In Create ZKCli")
        if self.zk_node.state != KazooState.CONNECTED:
            self.zk_node.start()
        while self.zk_node.state != KazooState.CONNECTED:
            pass

        if self.zk_node.exists('/Brokers') is None:
            self.zk_node.create(path='/Brokers', value=b'', ephemeral=False, makepath=True)
        while self.zk_node.exists('/Brokers') is None:
            pass

        if self.zk_node.exists('/Topics') is None:
            self.zk_node.create(path='/Topics', value=b'', ephemeral=False, makepath=True)
        while self.zk_node.exists('/Topics') is None:
            pass

        my_path = '/Brokers/' + str(self.ID)  # ID int

        if self.zk_node.exists(my_path) is None:
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
        print("In win election")
        leader_path = '/Leader'
        if self.zk_node.exists(path=leader_path) is None:
            self.zk_node.create(leader_path, value=self.address.encode('utf-8'), ephemeral=True, makepath=True)
        while self.zk_node.exists(path=leader_path) is None:
            pass

        self.leader_flag = True

        self.start_broker()


    def watch_mode(self):
        print("In watch mode")
        election_path = '/Brokers/'
        leader_path = '/Leader'

        @self.zk_node.DataWatch(path=leader_path)
        def watch_leader(data, state):
            print("In watch leader")
            while True:
                if self.zk_node.exists(path=leader_path) is None:
                    # print("In if none")
                    time.sleep(random.randint(0, 3))
                    if self.zk_node.exists(path=leader_path) is None:
                        print("1")
                        election = self.zk_node.Election(election_path, self.ID)
                        print(election.lock.contenders())
                        election.run(self.win_election)
                        if self.leader_flag == True:
                            election.lock.cancel()
                    else:
                        break


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("python3 ZMQ_broker.py brokerID zkServerIP localIP")
        exit(0)

    ZMQ_broker(int(sys.argv[1]), sys.argv[2], sys.argv[3])
    # ZMQ_broker(sys.arg[2], 'localhost', '10.0.0.2')  id, server_IP, my_IP
    # ZMQ_broker(1, '127.0.0.1', '127.0.0.1')
