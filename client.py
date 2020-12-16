"""
This class implements our testing client that we've used to test our implementation
of the chord protocol.
"""

from __future__ import print_function
import logging

import grpc
import multiprocessing as mp
import time

import numpy as np

import shared
import queries


def execute_query(query):
    # Select random host to start the query on.
    hosts = shared.read_hosts()

    random_host = np.random.randint(low=0, high=len(hosts))

    print('Executing query on:', hosts[random_host])
    with grpc.insecure_channel(hosts[random_host]) as channel:
        query(channel)


def basic_kv_test():
    execute_query(queries.run_kv_test)


if __name__ == '__main__':
    logging.basicConfig()
    start_time = time.perf_counter()
    with mp.Pool(2) as p:
        results = [p.apply_async(basic_kv_test, ()) for i in range(2)]
        [res.get(timeout=10) for res in results]
