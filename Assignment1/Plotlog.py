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




Plotlog('./starTopoNBlog/Subscriber1.log','./starTopoNBlogPlot/Subscriber1.png')
Plotlog('./starTopoNBlog/Subscriber2.log','./starTopoNBlogPlot/Subscriber2.png')
Plotlog('./starTopoNBlog/Subscriber3.log','./starTopoNBlogPlot/Subscriber3.png')

Plotlog('./starTopoBrokerlog/Subscriber1.log','./starTopoBrokerlogPlot/Subscriber1.png')
Plotlog('./starTopoBrokerlog/Subscriber2.log','./starTopoBrokerlogPlot/Subscriber2.png')
Plotlog('./starTopoBrokerlog/Subscriber3.log','./starTopoBrokerlogPlot/Subscriber3.png')

Plotlog('./busTopoNBlog/Subscriber1.log','./busTopoNBlogPlot/Subscriber1.png')
Plotlog('./busTopoNBlog/Subscriber2.log','./busTopoNBlogPlot/Subscriber2.png')
Plotlog('./busTopoNBlog/Subscriber3.log','./busTopoNBlogPlot/Subscriber3.png')

Plotlog('./busTopoBrokerlog/Subscriber1.log','./busTopoBrokerlogPlot/Subscriber1.png')
Plotlog('./busTopoBrokerlog/Subscriber2.log','./busTopoBrokerlogPlot/Subscriber2.png')
Plotlog('./busTopoBrokerlog/Subscriber3.log','./busTopoBrokerlogPlot/Subscriber3.png')