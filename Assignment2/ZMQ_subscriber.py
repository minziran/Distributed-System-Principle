import sys
import zmq
import os
import logging
import time

class ZMQ_subscriber():
    def __init__(self,sub_num,broker_IP,topic):

        try:
            logging.basicConfig(filename='Subscriber' + str(sub_num) + '.log', level=logging.DEBUG)
            self.broker_IP = broker_IP
            self.broker_Port = '5557'
            print ("=== Registered topics ", topic,'===')
            self.topic_list  =topic.split(' ')
            self.context = zmq.Context()
            self.socket = self.context.socket(zmq.SUB)
            self.register_sub()
            self.notify()
        except Exception as e:
            print(e)
            print("bring down zmq subscriber")
        finally:
            pass
            self.socket.close()
            self.context.term()


    def register_sub(self):
        addr = "tcp://" + self.broker_IP + ":" + self.broker_Port
        self.socket.connect(addr)
        # socket.connect("tcp://127.0.0.1:5200")
        for key in self.topic_list:
            # print("key "+ key)
            self.socket.setsockopt_string(zmq.SUBSCRIBE, key)
        print("===Already Registered Subscriber===")


    def notify(self):

        while True:
            msg = self.socket.recv_string()
            # print(msg)
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

    ZMQ_subscriber(1,'localhost','Lights Humidity')
    ZMQ_subscriber(2, 'localhost', 'Lights Humidity')

