import sys
import zmq

def register_sub():

    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    addr = "tcp://" + broker_IP + ":" + broker_Port
    socket.connect(addr)
    # socket.connect("tcp://127.0.0.1:5200")
    for key in topic:
        # print("key "+ key)
        socket.setsockopt_string(zmq.SUBSCRIBE, key)

    return context, socket

def notify():
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


if __name__=="__main__":


    # broker_IP = 'localhost'
    broker_IP = sys.argv[1]
    broker_Port = '5557'
    topic = []
    topic_num = len(sys.argv) - 2
    for key in range(2,topic_num+2):
        # print (key)
        # print(sys.argv[key+2])
        topic.append(sys.argv[key])
    # print(topic)

    # # Ex.ZMQ_subsciber.py  broker_IP Lights Humidity Temperature
    # exit("Run 'ZMQ_subscriber.py BrokerIP topic1 topic2 topic3.....'")

    try:
        context, socket =register_sub()
        notify()

    except Exception as e:
        print(e)
        print("bring down zmq subscriber")
    finally:
        pass
        socket.close()
        context.term()

