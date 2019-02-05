import zmq
import os
import csv
import time
import sys


def register_pub():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    addr = "tcp://" + broker_IP + ":" + broker_Port
    socket.connect(addr)
    print("===Already Register Publisher===")
    return context, socket


def publish():
    while True:

        with open('./test_topic_files/' + topic + '.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                print(', '.join(row))
                socket.send_string(topic + " " +str(time.time()) + ' ' + ', '.join(row))
                time.sleep(3)

def req_register(broker_IP, sub_port):
    context = zmq.Context()
    print("Connecting to server...")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://"+broker_IP+":"+sub_port)
    return context,socket

def req_send():
    #  Do 10 requests, waiting each time for a response
    with open('./test_topic_files/' + topic + '.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            print(', '.join(row))
            socket.send_string(topic + " " + str(time.time())+ ' '  + ', '.join(row))
            print('Sending '+ topic + " " + str(time.time()) + ' '  +', '.join(row))
            time.sleep(3)
            message = socket.recv()
            # print("Received reply ",  "[", message, "]")
    # for request in range(1, 10):
    #     print("Sending request ", request, "...")
    #     socket.send_string("Hello")
    #     #  Get the reply.
    #     message = socket.recv()
    #     print("Received reply ", request, "[", message, "]")message

if __name__ == '__main__':
    # broker_IP = 'localhost'
    broker_Port = '5556'

    if len(sys.argv) == 4:
        broker_IP = sys.argv[1]
        mode = sys.argv[2]
        topic = sys.argv[3]
    else:
        # Ex.ZMQ_ publisher.py broker_IP Lights
        exit("Run 'ZMQ_publisher.py  broker_IP topic'")

    try:
        if mode == '2':
            context, socket = register_pub()
            publish()
        else:
            context,socket = req_register(broker_IP,broker_Port)
            req_send()

    except Exception as e:
        print(e)
        print("bring down zmq publisher")
    finally:
        pass
        socket.close()
        context.term()
