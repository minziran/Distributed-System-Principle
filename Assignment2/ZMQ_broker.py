import zmq
import sys

class ZMQ_broker:
    def __init__(self):
        try:
            self.publisher_Port = '5556'
            self.subscriber_Port = '5557'
            self.context = zmq.Context(1)
            # socket facing publisher
            self.frontend = self.context.socket(zmq.SUB)
            addr1 = "tcp://*:" + self.publisher_Port
            self.frontend.bind(addr1)
            # frontend.connect("tcp://127.0.0.1:5556")
            self.frontend.setsockopt_string(zmq.SUBSCRIBE, "")
            # socket facing suscriber
            self.backend = self.context.socket(zmq.PUB)
            addr2 = "tcp://*:" + self.subscriber_Port
            self.backend.bind(addr2)
            print("Broker is already connected...... ")

            self.events = zmq.device(zmq.FORWARDER, self.frontend, self.backend)

        except Exception as e:
            print(e)
            print("bring down zmq device")
        finally:
            pass
            self.frontend.close()
            self.backend.close()
            self.context.term()





if __name__ == '__main__':

    ZMQ_broker()

