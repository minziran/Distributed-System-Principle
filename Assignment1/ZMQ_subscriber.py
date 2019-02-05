import sys
import zmq
import os
import logging
import time

def register_sub(broker_IP, broker_Port, topic):

    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    addr = "tcp://" + broker_IP + ":" + broker_Port
    socket.connect(addr)
    # socket.connect("tcp://127.0.0.1:5200")
    for key in topic:
        # print("key "+ key)
        socket.setsockopt_string(zmq.SUBSCRIBE, key)
    print("===Already Registered Subscriber===")
    return context, socket


def notify(socket):

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
        temp = msg.split(' ')
        info = str(time.time()) + ' ' + str(time.time() - float(temp[1]))
        logging.info(info)


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

    try:
        context, socket = register_sub(broker_IP, broker_Port, topic)
        notify(socket)
    except Exception as e:
        print(e)
        print("bring down zmq subscriber")
    finally:
        pass
        socket.close()
        context.term()

def register_rep(sub_port):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:%s" % sub_port)
    print("===Already Registered Subscriber===")
    return context, socket

def rep_notify(socket,sub_port):
    while True:
        #  Wait for next request from client
        message = socket.recv()
        print("Received request: ", message)
        temp = message.decode().split(' ')
        info =str(time.time()) +' '+ str(time.time()-float(temp[1]))
        logging.info(info)
        # print(temp)
        time.sleep(1)
        socket.send_string("Reply from %s" % sub_port)


def direct_connect():
    # pub_IP = sys.argv[1]
    sub_port = '5556'
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
        context, socket = register_rep(sub_port)
        rep_notify(socket,sub_port)

    except Exception as e:
        print(e)
        print("bring down zmq subscriber")
    finally:
        pass
        socket.close()
        context.term()


if __name__=="__main__":

    logging.basicConfig(filename='Subscriber' + sys.argv[1] + '.log', level=logging.DEBUG)
    # broker_IP = 'localhost'
    if sys.argv[2] == '2':
        broker_mode()
    elif(sys.argv[2] == '1'):
        direct_connect()


