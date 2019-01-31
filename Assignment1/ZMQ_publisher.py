import zmq
import sys
import csv
import time


def register_pub( ):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    addr = "tcp://" + broker_IP + ":" + broker_Port
    socket.connect(addr)
    return context, socket


def publish():
    while True:

        with open('./test_topic_files/'+topic + '.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                print(', '.join(row))
                socket.send_string(topic+" "+', '.join(row))
                time.sleep(3)

if __name__ == '__main__':
    # broker_IP = 'localhost'
    broker_Port = '5556'

    if len(sys.argv) == 3:
        broker_IP = sys.argv[1]
        topic = sys.argv[2]
    else:
        # Ex.ZMQ_ publisher.py broker_IP Lights
        exit("Run 'ZMQ_publisher.py  broker_IP topic'")

    try:
        context, socket = register_pub()
        publish()

    except Exception as e:
        print(e)
        print("bring down zmq publisher")
    finally:
        pass
        socket.close()
        context.term()








