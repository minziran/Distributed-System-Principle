"""
CS 6381 Assignment 2
Author: Team 2
"""
from kazoo.client import KazooClient
import logging
import typing


logging.basicConfig()


class ZKAssigment(KazooClient):
    def __init__(self):
        KazooClient.__init__(self)
        self.start()

    def create_brokers(self, _num: int=3):
        for i in range(_num):
            path = "/brokers/" + f"zbroker{i}"
            data = "/"
            self.create_nodes(path, data)

    def create_pubs(self, _num: int=3):
        for i in range(_num):
            path = "/" + f"zpub{i}"
            data = "/"
            self.create_nodes(path, data)

    def create_subs(self, _num: int=3):
        for i in range(_num):
            path = "/" + f"zsub{i}"
            data = "/"
            self.create_nodes(path, data)

    def create_nodes(self, path: str = "/test_znode", data: str = None):
        if data is None:
            self.create(path, makepath=True)
        else:
            bData = data.encode("utf-8")
            self.create(path, bData, makepath=True)

    def check_exists(self, path: str = "/test_znode") -> bool:
        if self.exists(path):
            print(path + " znode exists\n")
            return True
        else:
            return False

    def delete_node(self, path: str = "/test_node"):
        if self.check_exists(path):
            print("Znode at " + path + " is found!\n")
            self.delete(path)
            print("Znode at " + path + " is already deleted!\n")
        else:
            print("Znode at " + path + " does not exist\n")

    def stop_kazoo(self):
        self.stop()

    def __del__(self):
        self.stop()


test = ZKAssigment()
# test.create_brokers(3)
#
# test.create_pubs(3)
# test.create_subs(3)

# clean up

for num in range(0, 3):
    test.delete_node(f"/brokers/zbroker{num}")
    test.delete_node(f"/zsub{num}")
    test.delete_node(f"/zpub{num}")


test.delete_node("/brokers")

test.stop_kazoo()
