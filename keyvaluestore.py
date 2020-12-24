import grpc
import numpy as np

import keyvaluestore_pb2_grpc
import keyvaluestore_pb2

import shared
import time
import sys
import math


class KeyValueStore(keyvaluestore_pb2_grpc.KeyValueStoreServicer):
    # This is launched upon launching the server, we initialize the keyvalue store here and the nodes that it should connect to.
    # This also means that we should do the logic of a node joining the circle here
    def __init__(self, hostname, search_type='linear'):
        self.table = {}
        self.search_type = search_type
        self.hostname = hostname
        self.hostname_readable = hostname.split(':')[0]

        hosts = shared.read_hosts()
        self.nodeindex = shared.host_index(self.hostname)

        self.totalnodes = len(hosts)
        self.totalkeys = 10000

        # For now assume static range of keys
        self.keyrange_lower, self.keyrange_upper = self.calculate_range(self.nodeindex, self.totalkeys, self.totalnodes)

        self.fingertable = self.build_finger_table(hosts)
        self.predecessor = hosts[self.nodeindex - 1]

        self.node_summary()

    def build_finger_table(self, hosts):

        table = []

        i = 0
        while len(table) < math.floor(np.log2(self.totalnodes)):
            x = (self.nodeindex + 2**i) % self.totalnodes
            lower, upper = self.calculate_range(x, self.totalkeys, self.totalnodes)
            table.append((hosts[x], lower, upper))
            i += 1
        return table

    def calculate_range(self, index, total_keys, total_nodes):
        return (math.floor(index * total_keys / total_nodes), math.floor((index + 1) * total_keys / total_nodes - 1))

    def GetValues(self, request, context):
        # If it is range of the local key, return it from local
        # We use the upper of the successor here as this node also stores data from it's successor
        if self.is_in_range_of(request.key, self.keyrange_lower, self.fingertable[0][2] + 1):
            value = self.table[request.key]
            return keyvaluestore_pb2.GetResponse(value=value, hops=0)
        else:
            successor = self.find_successor(request.key)
            with grpc.insecure_channel(successor) as channel:
                stub = keyvaluestore_pb2_grpc.KeyValueStoreStub(channel)
                response = stub.GetValues(request)
                response.hops += 1
                return response

    def SetValue(self, request, context):
        # Entry point, current node
        if self.is_in_range_of(request.key, self.keyrange_lower, self.keyrange_upper + 1):
            # Also tell its predecessor that we he has to maintain it's copy
            if request.type != 'replication':
                with grpc.insecure_channel(self.predecessor) as channel:
                    stub = keyvaluestore_pb2_grpc.KeyValueStoreStub(channel)
                    request.type = 'replication'
                    response = stub.SetValue(request)
            # Set our own key
            self.table[request.key] = request.value
            return keyvaluestore_pb2.SetResponse(key=request.key, hops=0)

        # Entry point: predecessor
        elif self.is_in_range_of(request.key, self.fingertable[0][1], self.fingertable[0][2] + 1):
            # if it is in range of the successor, we can update table locally and tell successor to also update
            if request.type != 'replication':
                with grpc.insecure_channel(self.fingertable[0][0]) as channel:
                    stub = keyvaluestore_pb2_grpc.KeyValueStoreStub(channel)
                    request.type = 'replication'
                    response = stub.SetValue(request)
                    # Set our own key
            self.table[request.key] = request.value
            return keyvaluestore_pb2.SetResponse(key=request.key, hops=0)
        else:
            # Else forward it to next node
            response = None
            successor = self.find_successor(request.key)
            try:
                with grpc.insecure_channel(successor) as channel:
                    stub = keyvaluestore_pb2_grpc.KeyValueStoreStub(channel)
                    response = stub.SetValue(request)
            except:
                e = sys.exc_info()[0]
                shared.log(
                    f'An error occured whilst attempting to reach {successor} the following exception was raised:')
                shared.log(f'{e}')
            response.hops += 1
            return response

    def find_successor(self, key):
        """
        Locates the best successor of a given node given a certain key.
        Options are set upon creation of the object, this is done by setting search_type
        Available options are 'linear' and 'finger'
        """
        if self.search_type == 'linear':
            # Linear search always returns next node in line
            return self.fingertable[0][0]
        elif self.search_type == 'finger':
            # Attempt to find the best successor in the finger table:
            prev = None
            for index, (host, lower, upper) in enumerate(self.fingertable):
                # For every succesor, check  if it is
                # 1 In range of the keys of the succesor, we can just return it if that is the case
                if int(key) >= lower and int(key) <= upper:
                    return host
                # 2 In range of the current node and the next node in the list, in this case we return the previous
                # 2.1 Check if the current element is the last element in the list and return last
                if len(self.fingertable) == index + 1:
                    return host
                # 2.2 Check if it is in range of the current node + the next one
                if self.is_in_range_of(key, lower, self.fingertable[index + 1][1]):
                    return host
            # If this loop completes, it means that it was out of range for all of the nodes in the finger table and
            # thus we forward it to the last node known in hte finger table
            # This also should never happen
            shared.log(
                f'There\'s a bug in the iteration of the finger table, this occured for key: {key} on host {self.hostname} with finger table: {self.fingertable}', 'error')
            return self.fingertable[-1][0]
        else:
            shared.log(f'search_type invalid: {self.search_type}')

    def is_in_range_of(self, key, i1, i2):
        """
        Checks if the given key is in range of two numbers, also keeps in mind that it can loop around
        It is done with (i1, i2]
        """
        # First check if nodes are in ascending order
        # i = 50, i_1 = 100
        if i1 < i2:
            # Return simple equation which checks in the range
            return int(key) >= i1 and int(key) < i2
        else:
            # We've located a loop around in the chain, we need to handle this carefully
            # First handlle from node_i to the end of the loop (max key value)
            # i1 .. n
            if int(key) >= i1 and int(key) < self.totalkeys:
                return True
            # Then handle past the looping point
            # 0 .. i_1_l
            if int(key) < i2:
                return True
            return False

    def node_summary(self):
        shared.log('=============================')
        shared.log(f'Summary for node: {self.hostname} ({self.nodeindex})')
        shared.log(f'Key capacity: {len(self.table)}/{self.keyrange_upper - self.keyrange_lower + 1}')
        shared.log(
            f'Key range: [{self.keyrange_lower}-{self.keyrange_upper}], [{self.fingertable[0][1]}-{self.fingertable[0][2]}]')
        shared.log(f'Successor: {self.fingertable[0]}')
        shared.log(f'Predecessor: {self.predecessor}')
        shared.log(f'Finger table: {self.fingertable}')
