import numpy as np
import matplotlib.pyplot as plt


def Plotlog(filename, outputname):
    file = open(filename)
    time_list = []
    interval_list = []
    for line in file:
       temp = line.split(':')[2].split(' ')
       temp0 = float(temp[0])
       temp1 = float(temp[1].replace('\n',''))
       time_list.append(temp0)
       interval_list.append(temp1)


    plt.figure(outputname)

    plt.plot(time_list, interval_list, "blue")
    plt.pause(3)
    plt.savefig(outputname)

    plt.close()


Plotlog('./starTopoZKlog/Subscriber1.log','./starTopoZKlog/STZKSubscriber1.png')
Plotlog('./starTopoZKlog/Subscriber2.log','./starTopoZKlog/STZKSubscriber2.png')
Plotlog('./starTopoZKlog/Subscriber3.log','./starTopoZKlog/STZKSubscriber3.png')

Plotlog('./busTopoZKlog/Subscriber1.log','./busTopoZKlog/BTZKSubscriber1.png')
Plotlog('./busTopoZKlog/Subscriber2.log','./busTopoZKlog/BTZKSubscriber2.png')
Plotlog('./busTopoZKlog/Subscriber3.log','./busTopoZKlog/BTZKSubscriber3.png')
