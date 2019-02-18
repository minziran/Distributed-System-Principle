"""
CS 6381 Assignment 2
Author: Team 2
Regulation in this file:
All binary are encoded in utf-8
Naming Rules:

All methods and fields names are underscore-seperated
All variables use camelCase naming method

"""
from kazoo.client import KazooClient
import logging
from typing import List

logging.basicConfig()


class ZKAssigment(object):
    def __init__(self):
        self.zk = KazooClient()
        self.zk.start()
        self.brokers_path: str = "/brokers/"
        self.broker_num: int = 0
        self.pub_path = "/"
        self.sub_path = "/"
        self.election = None

    def create_brokers(self, _num: int = 3):
        for i in range(_num):
            path = self.brokers_path + f"zbroker{i}"
            data = f"zbroker{i}"
            self.create_nodes(path, data)
            self.broker_num += 1

    def create_pubs(self, _num: int = 3):
        for i in range(_num):
            path = self.pub_path + f"zpub{i}"
            data = f"zpub{i}"
            self.create_nodes(path, data)

    def create_subs(self, _num: int = 3):
        for i in range(_num):
            path = self.sub_path + f"zsub{i}"
            data = f"zsub{i}"
            self.create_nodes(path, data)

    def create_nodes(self, path: str = "/test_znode", data: str = None):
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
            print("Znode at " + path + " is found!\n")
            self.zk.delete(path)
            print("Znode at " + path + " is already deleted!\n")
        else:
            print("Znode at " + path + " does not exist\n")

    # A method for broker watching. If one of the broker dies,
    # elect a new leader broker
    def watch_brokers(self):
        @self.zk.ChildrenWatch(self.brokers_path)
        def watch_handler(_brokers):
            if len(_brokers) < self.broker_num and len(_brokers) > 0:
                # check if the leader is down
                # Find out who is down

                self.election = self.zk.Election(self.brokers_path, "brokerLeader")
                leaderList: List[str] = self.election.contenders()
                newLeader: str = leaderList[-1]

                # set the data to the /brokers znode
                self.zk.set(self.brokers_path[0: -1], newLeader.encode("utf-8"))
                print(self.zk.get(self.brokers_path[0: -1])[0])
                print("The leader broker is changed!\n")

    def stop_kazoo(self):
        self.zk.stop()

    def __del__(self):
        self.zk.stop()


if __name__ == "__main__":
    test = ZKAssigment()
    test.create_brokers(3)

    test.create_pubs(3)
    test.create_subs(3)

    test.watch_brokers()
    test.delete_node("/brokers/zbroker1")

    # clean up

    for num in range(0, 3):
        test.delete_node(f"/brokers/zbroker{num}")
        test.delete_node(f"/zsub{num}")
        test.delete_node(f"/zpub{num}")

    test.delete_node("/brokers")

    test.stop_kazoo()
