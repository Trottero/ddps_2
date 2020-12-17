import numpy as np

import queries


def benchmark_performance_writes():
    """
        Performance benchmark, returns the average time it takes for a write query to complete. 
        It also measures the average hops it took to reach the destination node
    """
    queries.execute_query(queries.run_kv_writes)
