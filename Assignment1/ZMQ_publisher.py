import zmq
import sys
import csv
import time


def main(broker_IP, broker_Port, topic):



    try:
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        addr = "tcp://" + broker_IP + ":" +broker_Port
        socket.connect(addr)

        while True:
            socket.send_string(topic + " " + 'Hello World')
            # with open(topic + '.csv', newline='') as csvfile:
            #     spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            #     for row in spamreader:
            #         print(', '.join(row))
            #         socket.send_string(topic+" "+', '.join(row))
            #         time.sleep(int(rate))
    except Exception as e:
        print(e)
        print("bring down zmq publisher")
    finally:
        pass
        socket.close()
        context.term()



if __name__ == '__main__':
    broker_IP = 'localhost'
    broker_Port = '5556'
    if len(sys.argv) == 2:
        topic = sys.argv[1]

    else:
        # Ex.ZMQ_ publisher.py Lights
        exit("Run 'ZMQ_publisher.py  topic'")

    main(broker_IP, broker_Port, topic)




