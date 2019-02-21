import zmq
import csv
import time
import socket
from kazoo.client import KazooClient

class ZMQ_publihser():

    def __init__(self,broker_IP,topic):

        try:
            self.broker_Port = '5556'
            self.broker_IP = broker_IP
            self.topic = topic
            self.context = zmq.Context()
            self.socket = self.context.socket(zmq.PUB)
            self.path = '/brokers'
            self.zk_object = KazooClient(hosts='127.0.0.1:2181')
            self.zk_object.start()
            self.register_pub()
            self.publish()
        except Exception as e:
            print(e)
            print("bring down zmq publisher")
        finally:
            pass
            self.socket.close()
            self.context.term()

    def register_pub(self):
        addr = "tcp://" + self.broker_IP + ":" + self.broker_Port
        self.socket.connect(addr)
        print("===Already Register Publisher===")


    def publish(self):
        while True:

            @self.zk_objcet.DataWatch(self.path)
            def watch_node(bData, event):
                if event != None:
                        print(event.type)
                        if (event.type == "CHANGED"): #reconnect once the election happend, change to the new leader
                            self.socket.close()
                            self.context.term()
                            time.sleep(2)
                            self.context = zmq.Context()
                            self.socket = self.context.socket(zmq.PUB)

                            # Connet to the broker
                            bData = self.zk_object.get(self.path) 
                            address = data.split(",")
                            self.connect_addr = "tcp://" + self.broker + ":"+ address[0]
                            print(self.connect_addr)
                            self.socket.connect(self.connect_addr)
            
            with open('./test_topic_files/' + self.topic + '.csv', newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for row in spamreader:
                    print(', '.join(row))
                    self.socket.send_string(self.topic + " " +str(time.time()) + ' ' + ', '.join(row))
                    time.sleep(3)



if __name__ == '__main__':
    ZMQ_publihser('localhost','Lights')
