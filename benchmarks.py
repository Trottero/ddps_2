from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

from time import sleep
import numpy as np
import time

import queries
import multiprocessing as mp
import shared


def query_wrapper(i):
    shared.log(f'Executing {i}', 'client')
    ms, hops = queries.execute_query(queries.run_kv_writes)
    shared.log(f'Finished: {i} in {ms}s', 'client')
    return ms, hops


def benchmark_performance_writes():
    """
        Performance benchmark, returns the average time it takes for a write query to complete. 
        It also measures the average hops it took to reach the destination node
    """
    start = time.perf_counter()
    results = []
    with ThreadPoolExecutor(100) as workers:
        results = [workers.submit(query_wrapper, i) for i in range(10)]
    shared.log(f'Benchmark finished in {time.perf_counter() - start}s')
    # Convert to 2d array
    r_2d = np.array([list(i.result()) for i in results])
    shared.log(f'Average job running time: {np.mean(r_2d[:, 0]) * 1000}ms; average hops: {np.mean(r_2d[:, 1])}')
