import random
import zmq
import sys
import time
from kazoo.client import *
from threading import *
from HistoryQueue import HistoryQueue


class ZMQ_broker:
    def __init__(self, id, server_IP, my_IP):
        # try:
            self.ID = id
            self.address = my_IP
            self.publisher_Port = '5556'
            self.subscriber_Port = '5557'
            self.server_address = server_IP + ':2181'
            self.history_Port = '5558'
            self.ownership_dic = {}
            self.zk_node = KazooClient(hosts=self.server_address)
            self.leader_flag = False
            self.syc_socket  = None
            self.lock = Lock()
            self.history_queue = HistoryQueue(100)
            self.context = None

            self.frontend = None

            self.backend = None

            # def func():
            #
            #     try:
            #
            #
            #         history_context = zmq.Context()
            #         history_socket = history_context.socket(zmq.REP)
            #         history_socket.bind("tcp://*:%s" % self.history_Port)
            #
            #         print("Binded history")
            #         while True:
            #
            #             message = history_socket.recv_string()
            #
            #             self.lock.acquire()
            #             temp = self.history_queue.get_history(int(message))
            #             self.lock.release()
            #             # print(temp)
            #             if temp is None:
            #                 # print("No history")
            #                 history_socket.send_string("No recent history")
            #             else:
            #                 print(" Reply ", str(list(temp)))
            #                 history_socket.send_string(str(list(temp)))
            #
            #
            #
            #
            #     except Exception as e:
            #         print(e)
            #         print("bring down history thread")
            #     finally:
            #         history_socket.close()
            #         history_context.term()
            #
            # t = Thread(target=func())
            #
            # t.start()
            self.create_ZKCli()


    def start_broker(self):
        def func():

            try:

                history_context = zmq.Context()
                history_socket = history_context.socket(zmq.REP)

                history_socket.bind("tcp://*:%s" % self.history_Port)

                print("Binded history")
                while True:
                    print("shdjhsakh")
                    message = history_socket.recv_string()

                    self.lock.acquire()
                    temp = self.history_queue.get_history(int(message))
                    self.lock.release()
                    # print(temp)
                    if temp is None:
                        print("No history")
                        history_socket.send_string("No recent history")
                    else:
                        print(" Reply ", str(list(temp)))
                        history_socket.send_string(str(list(temp)))


            except Exception as e:
                print(e)
                print("bring down history thread")
            finally:
                history_socket.close()
                history_context.term()


        history_tread = Thread(target=func())
        Thread.setDaemon(history_tread, True)
        history_tread.start()
        print("********")
        time.sleep(5)
        print("+++++++")

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

        while True:
            print("In while true")
            msg = self.frontend.recv_string()
            # print ("In while True", msg)
            temp_list = msg.split(' ')

            temp_topic = temp_list[0]
            temp_ownership = temp_list.pop(1)
            temp_ID = temp_list.pop(2)
            current_owner = 0
            if temp_topic not in self.ownership_dic:
                s = temp_ownership + ' ' + temp_ID
                self.ownership_dic[temp_topic] = s
                current_owner = temp_ownership
            else:
                if int(temp_ownership) > int(self.ownership_dic[temp_topic].split(' ')[0]) :
                    continue
                else:
                    s = temp_ownership + ' ' + temp_ID
                    self.ownership_dic[temp_topic] = s
                    current_owner = temp_ownership
            msg  = ' '.join(temp_list)

            print("Current topic  ", temp_topic)
            print("Current ownership ", current_owner)

            # print(msg)
            self.lock.acquire()
            self.history_queue.push_history(msg)
            self.lock.release()

            self.backend.send_string(msg)
        #self.events = zmq.device(zmq.FORWARDER, self.frontend, self.backend)
        

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

        my_path = '/Brokers/' + str(self.ID) #ID int

        if self.zk_node.exists(my_path) is None:
            self.zk_node.create(path=my_path, value=b'', ephemeral=True, makepath=True)
        while self.zk_node.exists(my_path) is None:
            pass

        leader_path = '/Leader'
        if self.zk_node.exists(leader_path):
            self.leader_flag = False
            # self.watch_mode()
            def func():

                try:

                    data, state = self.zk_node.get(leader_path)
                    temp_IP = data.decode("utf-8")
                    syn_context = zmq.Context()
                    syn_socket = syn_context.socket(zmq.PULL)
                    syn_socket.setsockopt(zmq.RCVTIMEO, 30000)
                    syn_socket.connect('tcp://' + temp_IP + ':' + "5559")

                    print("In pull data")
                    while self.leader_flag is False:
                        msg = syn_socket.recv_string()
                        print("SHOW MSG ", msg)
                        msg_list = msg.split("###")
                        self.lock.acquire()
                        self.history_queue.msg_queue = msg_list[0]
                        self.history_queue.max_size = int(msg_list[1])
                        self.ownership_dic = msg_list[2]
                        self.lock.release()
                except Exception as e:
                    print(e)
                    print("bring down pull data")
                finally:
                    syn_socket.close()
                    syn_context.term()

            t = Thread(target=func)
            Thread.setDaemon(t, True)
            t.start()

            self.watch_mode()
        else:

            self.zk_node.create(leader_path, value=self.address.encode('utf-8'), ephemeral=True, makepath=True)
            while self.zk_node.exists(path=leader_path) is None:
                pass
            self.leader_flag = True


            def func():

                try:

                    syn_context = zmq.Context()
                    syn_socket = syn_context.socket(zmq.PUSH)
                    syn_socket.bind("tcp://*" + ':' + '5559')

                    print("In push data")

                    while self.leader_flag is False:
                        pass
                    while True:
                        str = self.history_queue.msg_queue.__str__()+ "###" + str(self.history_queue.max_size) + "###" +self.ownership_dic.__str__()
                        syn_socket.send_string(str)
                        print("eeee")

                except Exception as e:
                    print(e)
                    print("bring down push data")
                finally:
                    syn_socket.close()
                    syn_context.term()

            t = Thread(target=func)
            Thread.setDaemon(t, True)
            t.start()
            time.sleep(10)

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

    #ZMQ_broker(int(sys.argv[1]), sys.argv[2], sys.argv[3])
    # ZMQ_broker(sys.arg[2], 'localhost', '10.0.0.2')  id, server_IP, my_IP
    ZMQ_broker(1, '127.0.0.1', '127.0.0.1')
