from BusTopology import BusTopology
from StarTopology import StarTopology

def main():
    pub_num = 3
    sub_num = 3
    topo_type = 'bus'
    if topo_type == 'bus':
        topo = BusTopology(pub_num,sub_num)
    elif topo_type == 'star':
        topo = StarTopology(pub_num,sub_num)
    else:
        exit("Could not find mached topology. 'bus' and 'star' are provided")

if __name__ == '__main__':
    main()