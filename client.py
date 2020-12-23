"""
This class implements our testing client that we've used to test our implementation
of the chord protocol.
"""

from __future__ import print_function
import logging
import benchmarks
import numpy as np

if __name__ == '__main__':
    np.random.seed(42)
    logging.basicConfig()
    benchmarks.benchmark_performance_writes()
