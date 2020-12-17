"""
This class implements our testing client that we've used to test our implementation
of the chord protocol.
"""

from __future__ import print_function
import numpy as np
import logging
import time

import grpc
import multiprocessing as mp

import shared
import queries


def basic_kv_test():
    queries.execute_query(queries.run_kv_test)


if __name__ == '__main__':
    logging.basicConfig()
    start_time = time.perf_counter()
    with mp.Pool(2) as p:
        results = [p.apply_async(basic_kv_test, ()) for i in range(2)]
        [res.get(timeout=10) for res in results]
