
## Distributed System Principle Assignment 3
==========================
#### Author: Team 2

**Abstract:**

In this assignment, a pub/sub network is established via Mininet and ZeroMQ. 
Zookeeper is utilized to manage broker nodes. Star topology are implemented but there are three broker nodes (it can be more by set the broker node number). 
Multiple publishers and subscribers with various topics can be added into or removed from the network. History and ownership is 
added to out program so that the broker or subscriber can store the history value.
Finally, end-to-end measurements are carried out and the time difference is measured.

**Introduction:**

Mininet is a software emulator for prototyping a large network on a single machine. 
Mininet can be used to quickly create a realistic virtual network running actual kernel, switch and software application code on a personal computer. 
Mininet allows the user to quickly create, interact with, customize and share a software-defined network (SDN) prototype to simulate a network topology that uses Openﬂow switches [1]. 

Apache ZooKeeper is a software project of the Apache Software Foundation. 
It is essentially a centralized service for distributed systems to a hierarchical key-value store, 
which is used to provide a distributed configuration service, synchronization service, and naming registry for large distributed systems. 
ZooKeeper was a sub-project of Hadoop but is now a top-level Apache project in its own right. 
ZooKeeper's architecture supports high availability through redundant services [2].

In this assignment, zookeeper is used to coordinate the broker nodes and carry out the leader election 
when one of brokers is disconnected. In the non-broker mode, the zookeeper's watch mechanism is utilized for 
subscribers to obtain data from publishers.

**Create Network Topologies**

***Star Topology Network***

In this assignment, star topology and bus topology are created. 
Using python file StarTopologyZK.py, a star topology 
(in default case, there will be three publishers, three brokers and three subscribers). 
The command to construct a star topology with broker is: 
       
   ```bash 
     sudo mn --custom StarTopologyZK.py --topo startopoZK
   ```

***Bus Topology Network***

 The command to construct a star topology with broker is: 
 
 ```bash 
     sudo mn --custom BusTopologyZK.py --topo bustopoZK
 ```
 

**Pub/Sub System on Star Topology**

***Zookeeper***

Zookeeper is embeded inside the python scripts, namely ZMQ_broker.py, ZMQ_publisher.py, ZMQ_subscriber.py 
They are executed in the command line interface. The version of zookeeper used in this assignment is kazoo 2.6.1.

**Testing Procedure**

***Broker Mode***

First we use Mininet to create a topology. The command can be found above. Here we choose star topology 
(one may also use the bus topology). The result is shown in Fig 1.

![StarTopo](./Pictures/mininet.jpg)

##### Fig 1 A Star Topology in Mininet

Before testing, we need to start the zookeeper server first. We xterm the first broker, broker1. 
Then we change the directory to the _bin/_ folder of zookeeper (in this case, it is at ~/Documents).
Use command:

 ```bash 
     ./zkServer.sh start
 ```
to start the zookeeper server.

**Note:** This step is critical otherwise brokers cannot connect the zookeeper server. There will be a 
**Connection dropped: socket connection error: Connection refused** ERROR.

The successful result is as Fig 2.

![StartZKServer](./Pictures/zkServer.jpg)

##### Fig 2 Start the Zookeeper Server

Then we navigate back to our assignment folder. 
First we run the scripts on three brokers. The format is as follows:

 ```bash 
     sudo python3 ZMQ_broker.py <broker ID> <IP of zookeeper server> <IP of itself>
 ```
![BrokerRunning](./Pictures/brokerRunning.jpg)

##### Fig 3 Start the brokers

We can see that broker1 becomes the leader broker and broker2 is watching.
Then we can start the publishers and subscribers.

xterm all publishers and subscribers. The command format for publishers is 


 ```bash 
     sudo python3 ZMQ_publisher.py <zkServerIP> <publisherID> <topic> <ownership>
 ```
 The command format for subscribers is 

 ```bash 
     sudo python3 ZMQ_subscriber.py <zkServerIP> <subID> <topic> <historySize>
 ```
 The result of running publishers and subscribers are shown in Fig 4.
 
 ![pubSubRunning](./Pictures/brokermode.jpg)

##### Fig 4 Running Result of Publishers and Subscribers

**History**
The broker can send the history through the history port. The output of history is shown in Fig. 5.

**Note:** Only the message with higher ownership (lower number of ownership, 1 is the highest) is stored. 

![history](./Pictures/history.jpg)
##### Fig 5 History of Message


**Latency Measurement:**
The latency is measured and plotted in Fig. 6.

![latency](./Pictures/STZKSubscriber1.png)
##### Fig 6 Latency of Message
 
**Non-Broker Mode**

To build a non-broker mode network, we use BusTopologyNB.py and StarTopologyNB.py from assignment 1.
The command to build a non-broker bus-topology network is:

 ```bash 
     sudo mn --custom BusTopologyNB.py --topo bustopoNB
 ```

For non-broker star-topology network, the command is:
 ```bash 
     sudo mn --custom StarTopologyNB.py --topo startopoNB
 ```

Then we xterm each publisher and subscriber. In pub1, we first start the zookeeper server in pub1.

We change the directory to the _/bin/_ folder of zookeeper (in this case, it is at ~/Documents).
Use command:

 ```bash 
     ./zkServer.sh start
 ```

Then we navigate the directory back and run the publisher's script. The publisher code for non-broker mode is ZMQ_publisher_NB.py

The command is:

 ```bash 
     sudo python3 ZMQ_publisher_NB <zookeeper IP> <publisher ID> <Topic> <its own IP> <history Size> <ownership>
 ```
 
 The command for subscriber is 
 ```bash
     sudo python3 ZMQ_subscriber.py <zkServerIP> <subID> <topic> <historySize>
```
The non-broker mode is similar therefore will not be discussed in detail.

**Effort of Teammates**
In this assignment, we collaboratively finish all the work. 
Ziran is responsible for broker setup and socket construction.
Xiaoxing modify up zookeeper file system and handle the watch mechanism.
Robert is for non-broker mode and implement the history queue.

**Reference:**

[1] Margaret Rouse. 2013. TechTarget. https://searchnetworking.techtarget.com/definition/ Mininet 

[2] Wikipedia Apache ZooKeeper: https://en.wikipedia.org/wiki/Apache_ZooKeeper 