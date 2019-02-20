"""
CS 6381 Assignment 2
Author: Team 2
Regulation in this file:
All binary are encoded in utf-8

Description:
A class to create znodes for publishers and subscribers and brokers

Naming Rules:

All methods and fields names are underscore-seperated
All variables use camelCase naming method

"""
from kazoo.client import KazooClient
import logging
from typing import List

logging.basicConfig()


class ZKMidware(object):
    def __init__(self):
        self.zk = KazooClient()
        self.brokers_path: str = "/brokers"
        self.pub_path = "/"
        self.sub_path = "/"
        self.broker_num: int = 0
        self.pub_num: int = 0
        self.sub_num = 0
        self.election = None

    def start_zk(self):
        self.zk.start()

    def create_brokers(self, _num: int = 3):
        for i in range(_num):
            broker_IP = str()
            broker_port = str()
            path = self.brokers_path + "/" + f"zbroker{i}"
            data = f"zbroker{i}" + "," + broker_IP + "," + broker_port
            self.create_nodes(path, data)
            self.broker_num += 1

    def create_pubs(self, _num: int = 3):
        for i in range(_num):
            pub_IP = str()
            pub_port = str()
            path = self.pub_path + f"zpub{i}"
            data = f"zpub{i}" + "," + pub_IP + "," + pub_port
            self.create_nodes(path, data)

    def create_subs(self, _num: int = 3):
        for i in range(_num):
            sub_IP = str()
            sub_port = str()
            path = self.sub_path + f"zsub{i}"
            data = f"zsub{i}" + "," + sub_IP + "," + sub_port
            self.create_nodes(path, data)

    def create_nodes(self, path: str = "/test_znode", data: str = None):
        if self.zk.exists(path):
            return
        else:
            if data is None:
                self.zk.create(path, makepath=True)
            else:
                bData = data.encode("utf-8")
                self.zk.create(path, bData, makepath=True)

    def check_exists(self, path: str = "/test_znode") -> bool:
        if self.zk.exists(path):
            print(path + " znode exists\n")
            return True
        else:
            return False

    def delete_node(self, path: str = "/test_node"):
        if self.check_exists(path):
            self.zk.delete(path)
            print("Znode at " + path + " is already deleted!\n")
        else:
            print("Znode at " + path + " does not exist\n")

    # A method for broker watching. If one of the broker dies,
    # elect a new leader broker
    def brokers_watch(self):
        @self.zk.ChildrenWatch(self.brokers_path + "/")
        def broker_watch_handler(_brokers):
            if self.broker_num > len(_brokers) > 0:
                # check if the leader is down
                # Find out who is down

                self.election = self.zk.Election(self.brokers_path + "/", "brokerLeader")
                leaderList: List[str] = self.election.contenders()
                newLeader: str = leaderList[-1]

                # set the data to the /brokers znode
                self.zk.set(self.brokers_path, newLeader.encode("utf-8"))
                print(self.zk.get(self.brokers_path)[0].decode("utf-8") + " becomes the new leader")

    def pubsub_watch(self):
        @self.zk.DataWatch(self.brokers_path)
        def pubsub_watch_handler(bData, status):
            if bData:
                print("The data is: " + bData.decode("utf-8") + ".\n")

            if status:
                print("The status is: " + str(status) + ".\n")

    def stop_kazoo(self):
        self.zk.stop()

    def clean_up(self, num):
        for num in range(0, num):
            self.delete_node(f"/brokers/zbroker{num}")
            self.delete_node(f"/zsub{num}")
            self.delete_node(f"/zpub{num}")

        self.delete_node("/brokers")

    def __del__(self):
        self.zk.stop()


if __name__ == "__main__":
    test = ZKMidware()
    test.start_zk();
    test.create_brokers(3)

    test.create_pubs(3)
    test.create_subs(3)

    test.brokers_watch()

    test.delete_node("/brokers/zbroker1")

    test.pubsub_watch()

    # clean up
    test.clean_up(3)
