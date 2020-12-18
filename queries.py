import time
import numpy as np
import keyvaluestore_pb2
import keyvaluestore_pb2_grpc
import string
import shared
import grpc
import sys


def execute_query(query):
    """
    Simple query runner, automatically wraps the function in an instance for a random host
    """
    host = shared.random_host()

    with grpc.insecure_channel(host) as channel:
        return query(channel)


def run_kv_test(channel):
    """
    Simple function which tests basic retrieval / storage of keys
    Returns Average time for a query and average amount of hops
    """
    start_time = time.perf_counter()
    stub = keyvaluestore_pb2_grpc.KeyValueStoreStub(channel)
    r1 = stub.SetValue(keyvaluestore_pb2.SetRequest(key='1', value='banaan 1'))
    r2 = stub.GetValues(keyvaluestore_pb2.GetRequest(key='1'))
    hops = (r1.hops + r2.hops) / 2

    return (time.perf_counter() - start_time / 2, hops)


def run_kv_writes(channel):
    """
    Simple function which performs a write on a random index with a random value
    """
    base = [x for x in string.digits + string.ascii_letters]

    key = np.random.randint(low=0, high=10000)
    value = "".join(np.random.choice(base, size=10))

    start_time = time.perf_counter()
    stub = keyvaluestore_pb2_grpc.KeyValueStoreStub(channel)
    r1 = stub.SetValue(keyvaluestore_pb2.SetRequest(key=str(key), value=value))
    return (time.perf_counter() - start_time, r1.hops)


def run_kv_reads(channel):
    """
    Performs a single read on a random hash
    """
    key = np.random.randint(low=0, high=10000)

    start_time = time.perf_counter()
    stub = keyvaluestore_pb2_grpc.KeyValueStoreStub(channel)
    r1 = stub.GetValues(keyvaluestore_pb2.GetRequest(key=str(key)))

    return (time.perf_counter() - start_time, r1.hops)
