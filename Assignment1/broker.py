import zmq
import sys

def main(publisher_Port, subscriber_Port):


    try:
        context = zmq.Context(1)

        # socket facing publisher
        frontend = context.socket(zmq.SUB)
        addr1 = "tcp://*:" + publisher_Port
        frontend.bind(addr1)
        #frontend.connect("tcp://127.0.0.1:5556")
        frontend.setsockopt_string(zmq.SUBSCRIBE, "")
        # socket facing suscriber
        backend = context.socket(zmq.PUB)
        addr2 = "tcp://*:" + subscriber_Port
        backend.bind(addr2)
        print("Broker is already connected...... ")

        events = zmq.device(zmq.FORWARDER, frontend, backend)



    except Exception as e:
        print(e)
        print("bring down zmq device")
    finally:
        pass
        frontend.close()
        backend.close()
        context.term()




if __name__ == '__main__':

    if len(sys.argv) == 3:
        publisher_Port = sys.argv[1]
        subscriber_Port = sys.argv[2]

    else:
        # Ex. ZMQ_broker.py 5556 5200
        exit("Run 'ZMQ_broker.py publisherPort subscriberPort'")



    main(publisher_Port, subscriber_Port)
