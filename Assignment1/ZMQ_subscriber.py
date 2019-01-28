import os
import sys

import zmq
import psutil
import logging



def main(broker_IP, broker_Port, topic):
    try:
        context = zmq.Context()
        socket= context.socket(zmq.SUB)
        addr = "tcp://" + broker_IP + ":" +broker_Port
        socket.connect(addr)
        # socket.connect("tcp://127.0.0.1:5200")
        for key in topic:
            socket.setsockopt_string(zmq.SUBSCRIBE, key)

        # topicfilter = "Lights"
        # socket.setsockopt_string(zmq.SUBSCRIBE, topicfilter)



        while True:

            msg= socket.recv_string()
            # print(msg)
            temp = msg.split(' ', 1)
            topic = temp[0]
            temp1 = temp[1]
            # print(topic)
            # print(time)
            # print(value)
            print(topic,temp1)




    except Exception as e:
        print(e)
        print("bring down zmq subscriber")
    finally:
        pass
        socket.close()
        context.term()





if __name__=="__main__":


    broker_IP = 'localhost'
    broker_Port = '5557'
    topic = []
    topic_num = len(sys.argv) - 1
    for key in range(1,topic_num+1):
        # print (key)
        # print(sys.argv[key+2])
        topic.append(sys.argv[key])

    print(topic)

    # # Ex.ZMQ_subsciber.py  Lights Humidity Temperature
    # exit("Run 'ZMQ_subscriber.py BrokerIP BrokerPort topic1 topic2 topic3.....'")

    main(broker_IP, broker_Port, topic)
