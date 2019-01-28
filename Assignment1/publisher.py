import zmq
import random
import sys
import time
import socket

port = "5557"
IPAddr = "localhost"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

context = zmq.Context()
socket = context.socket(zmq.PUB)
# print("tcp://" + IPAddr + ":"+ port)
socket.bind("tcp://127.0.0.1:"+ port)
socket.connect("tcp://129.114.111.157:"+port)

for num in range(0, 100):
    topic = "Hello"
    messagedata = "World!"
    print (topic, messagedata)
    socket.send_string(topic+messagedata)
    time.sleep(1)
