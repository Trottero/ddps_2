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
        results = [workers.submit(query_wrapper, i) for i in range(10000)]
    stop = time.perf_counter() - start
    # Convert to 2d array
    r_2d = np.array([list(i.result()) for i in results])

    avg_job_time = np.mean(r_2d[:, 0]) * 1000
    avg_hops = np.mean(r_2d[:, 1])
    filename = f'benchmark_performance_writes_{int(round(time.time()))}'
    # Save it to a persitent file
    shared.log(f'{avg_job_time} {avg_hops}', filename)
    for q in r_2d:
        shared.log(f'{q[0]} {q[1]}', filename)

    # Notify user using terminal that the benchmark has finished
    shared.log(f'Benchmark finished in {stop}s')
    shared.log(f'Average job running time: {avg_job_time}ms; average hops: {avg_hops}')
