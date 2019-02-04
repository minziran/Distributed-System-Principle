# Assignment 1 Readme - Team 2

### Single Broker-based Publish-Subscribe using ZMQ and Mininet

To start off with, we defined two topologies, a bus and star topology. These are defined in the files, **BusTopology.py** and **StarTopology.py**. There are graphical examples shown below:

Bus Topology                                                             |  Star Topology
:-----------------------------------------------------------------------:|:------------------------------------------------------------------------------:
<img src="/Assignment1/Pictures/Bus.PNG" height="400" width="400" ></a>  | <img src="/Assignment1/Pictures/Star.PNG" height="400" width="400" ></a>


We then wrote code for the broker, subscriber, and publisher which are contained in the files: **ZMQ_broker.py**, **ZMQ_subscriber.py** and **ZMQ_publisher.py**. We next wrote some input files that define which topology we will use, how many publishers and subscribers there will be, and which **test_topic_file** we will use for each publisher and subscriber. We included 6 input files for various different scenarios. 

The program that connects it all together is **PubSubApplication.py**. It's functionality is to grab the input file we specify and create the network based upon the file. It also specifies which hosts in mininet are the broker, publishers, and subscribers. 

### Running the code

To run the code, follow the steps described below:

1. Open Virtual Machine with mininet and pyzmq installed
2. Open a terminal
3. Clone our repository:

  ```git clone https://github.com/minziran/Distributed-System-Principle.git```
  
4. Go into the correct directory

  ```cd Distributed-System-Principle/Assignment1/```
  
5. Run the program (N is numbers 1-6)

  ```sudo python PubSubApplication.py test_topic_file/InputFileN```
 
