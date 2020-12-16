import grpc
import keyvaluestore_pb2_grpc
import keyvaluestore_pb2

import shared

import os


class KeyValueStore(keyvaluestore_pb2_grpc.KeyValueStoreServicer):
    # This is launched upon launching the server, we initialize the keyvalue store here and the nodes that it should connect to.
    # This also means that we should do the logic of a node joining the circle here
    def __init__(self, hostname):
        self.fingertable = []
        self.table = {}
        self.hostname = hostname

        hosts = shared.read_hosts()
        self.nodeindex = shared.host_index(self.hostname)

        self.totalnodes = len(hosts)
        self.totalkeys = 100
        # For now assume static range of keys
        self.keyrange_lower = self.nodeindex * self.totalkeys / self.totalnodes
        self.keyrange_upper = (self.nodeindex + 1) * self.totalkeys / self.totalnodes - 1

        self.successor = hosts[(self.nodeindex + 1) % self.totalnodes]
        self.predecessor = hosts[self.nodeindex - 1]

        self.node_summary()

    def GetValues(self, request, context):
        # If it is range of the local key, return it from local
        if self.is_in_range(request.key):
            value = self.table[request.key]
            return keyvaluestore_pb2.GetResponse(value=value)
        else:
            print('Forwarding to another node since key is out of range!')
            with grpc.insecure_channel(self.find_successor()) as channel:
                stub = keyvaluestore_pb2_grpc.KeyValueStoreStub(channel)
                return stub.GetValues(request)

    def SetValue(self, request, context):
        if self.is_in_range(request.key):
            self.table[request.key] = request.value
            return keyvaluestore_pb2.SetResponse(key=request.key)
        else:
            # Else forward it to next node
            print('Forwarding to another node since key is out of range!')
            with grpc.insecure_channel(self.find_successor()) as channel:
                stub = keyvaluestore_pb2_grpc.KeyValueStoreStub(channel)
                return stub.SetValue(request)

    def is_in_range(self, key):
        return int(key) >= self.keyrange_lower and int(key) <= self.keyrange_upper

    def find_successor(self, key):
        return self.successor
        # Easy way to debug nodes

    def node_summary(self):
        print('=============================')
        print(f'Summary for node: {self.hostname} ({self.nodeindex})')
        print(f'Key capacity: {len(self.table)}/{self.keyrange_upper - self.keyrange_lower + 1}')
        print(f'Key range: [{self.keyrange_lower}-{self.keyrange_upper}]')
        print(f'Successor: {self.successor}')
        print(f'Predecessor: {self.predecessor}')
