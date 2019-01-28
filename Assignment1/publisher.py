import zmq
import random
import sys
import time

port = "5556"
IPAddr = "129.114.111.157"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

context = zmq.Context()
socket = context.socket(zmq.PUB)
print("tcp://" + IPAddr + ":"+ port)
socket.bind("tcp://" + IPAddr + ":"+ port)

while True:
    topic = random.randrange(9999,10005)
    messagedata = random.randrange(1,215) - 80
    print (topic, messagedata)
    socket.send((topic, messagedata))
    time.sleep(1)