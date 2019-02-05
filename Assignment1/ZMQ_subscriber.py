import sys
import zmq
import os
import logging
import time

def register_sub(broker_IP, broker_Port, topic):

    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    addr = "tcp://" + broker_IP + ":" + broker_Port
    if sys.argv[2] == '2':
        socket.connect(addr)
    else:
        socket.bind(addr)
    # socket.connect("tcp://127.0.0.1:5200")
    for key in topic:
        # print("key "+ key)
        socket.setsockopt_string(zmq.SUBSCRIBE, key)
    print("===Already Register Subscriber===")
    return context, socket


def notify(socket):
    # print("In notify")
    while True:
        msg = socket.recv_string()
        # print(msg)
        temp = msg.split(' ', 1)
        topic = temp[0]
        temp1 = temp[1]
        # print(topic)
        # print(time)
        # print(value)
        print(msg)
        logging.info(time.time()+msg)


def broker_mode():
    broker_IP = sys.argv[3]
    broker_Port = '5557'
    topic = []
    topic_num = len(sys.argv) - 4
    for key in range(4, topic_num + 4):
        # print (key)
        # print(sys.argv[key+2])
        topic.append(sys.argv[key])
    # print(topic)

    # Ex.ZMQ_subsciber.py sub1 1 broker_IP Lights Humidity Temperature
    # exit("Run 'ZMQ_subscriber.py subsciber_name mode BrokerIP topic1 topic2 topic3.....'")
    logging.basicConfig(filename='Subscriber' + sys.argv[1]+'.log', level=logging.debug())
    try:
        context, socket = register_sub(broker_IP, broker_Port, topic)
        socket.bind()
        notify(socket)
    except Exception as e:
        print(e)
        print("bring down zmq subscriber")
    finally:
        pass
        socket.close()
        context.term()

def direct_connect():
    pub_IP = sys.argv[1]
    pub_Port = '5557'
    topic = []
    topic_num = len(sys.argv) - 2
    for key in range(2, topic_num + 2):
        # print (key)
        # print(sys.argv[key+2])
        topic.append(sys.argv[key])
    # print(topic)

    # Ex.ZMQ_subsciber.py sub1 1 Lights Humidity Temperature
    # exit("Run 'ZMQ_subscriber.py subsciber_name mode BrokerIP topic1 topic2 topic3.....'")

    logging.basicConfig(filename='Subscriber'+ sys.argv[2]+'.log', level=logging.DEBUG)
    try:
        context, socket = register_sub(pub_IP, pub_Port, topic)
        notify(socket)

    except Exception as e:
        print(e)
        print("bring down zmq subscriber")
    finally:
        pass
        socket.close()
        context.term()


if __name__=="__main__":
    # broker_IP = 'localhost'
    if sys.argv[2] == '2':
        broker_mode()
    elif(sys.argv[2] == '1'):
        direct_connect()


