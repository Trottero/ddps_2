import grpc
import keyvaluestore_pb2_grpc
import keyvaluestore_pb2

import shared
import time
import os


class KeyValueStore(keyvaluestore_pb2_grpc.KeyValueStoreServicer):
    # This is launched upon launching the server, we initialize the keyvalue store here and the nodes that it should connect to.
    # This also means that we should do the logic of a node joining the circle here
    def __init__(self, hostname):
        self.fingertable = []
        self.table = {}
        self.hostname = hostname
        self.hostname_readable = hostname.split(':')[0]

        hosts = shared.read_hosts()
        self.nodeindex = shared.host_index(self.hostname)

        self.totalnodes = len(hosts)
        self.totalkeys = 1000
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
            return keyvaluestore_pb2.GetResponse(value=value, hops=0)
        else:
            successor = self.find_successor(request.key)
            start = time.perf_counter()
            with grpc.insecure_channel(successor) as channel:
                shared.log(f'RPC channel set up in: {time.perf_counter() - start} from {self.hostname} -> {successor}')
                stub = keyvaluestore_pb2_grpc.KeyValueStoreStub(channel)
                response = stub.GetValues(request)
                response.hops += 1
                return response

    def SetValue(self, request, context):
        if self.is_in_range(request.key):
            self.table[request.key] = request.value
            return keyvaluestore_pb2.SetResponse(key=request.key, hops=0)
        else:
            # Else forward it to next node
            shared.log('Forwarding to another node since key is out of range!')

            with grpc.insecure_channel(self.find_successor(request.key)) as channel:
                stub = keyvaluestore_pb2_grpc.KeyValueStoreStub(channel)
                response = stub.SetValue(request)
                response.hops += 1
                return response

    def is_in_range(self, key):
        return int(key) >= self.keyrange_lower and int(key) <= self.keyrange_upper

    def find_successor(self, key):
        return self.successor
        # Easy way to debug nodes

    def node_summary(self):
        shared.log('=============================')
        shared.log(f'Summary for node: {self.hostname} ({self.nodeindex})')
        shared.log(f'Key capacity: {len(self.table)}/{self.keyrange_upper - self.keyrange_lower + 1}')
        shared.log(f'Key range: [{self.keyrange_lower}-{self.keyrange_upper}]')
        shared.log(f'Successor: {self.successor}')
        shared.log(f'Predecessor: {self.predecessor}')
