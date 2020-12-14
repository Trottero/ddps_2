"""
This class implements our testing client that we've used to test our implementation
of the chord protocol.
"""

from __future__ import print_function
import logging

import grpc
import multiprocessing as mp
import time

import keyvaluestore_pb2
import keyvaluestore_pb2_grpc


def run_kv_test():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = keyvaluestore_pb2_grpc.KeyValueStoreStub(channel)
        response = stub.SetValue(keyvaluestore_pb2.SetRequest(key='1', value='banaan 1'))
        print('Response.key: ', response.key)
        response = stub.GetValues(keyvaluestore_pb2.GetRequest(key='1'))
        print('Response.value:', response.value)


if __name__ == '__main__':
    logging.basicConfig()
    start_time = time.perf_counter()
    run_kv_test()
    with mp.Pool(2) as p:
        results = [p.apply_async(run_kv_test, ()) for i in range(2)]
        [res.get(timeout=10) for res in results]
