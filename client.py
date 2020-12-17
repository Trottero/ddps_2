"""
This class implements our testing client that we've used to test our implementation
of the chord protocol.
"""

from __future__ import print_function
import logging
import benchmarks

if __name__ == '__main__':
    logging.basicConfig()
    benchmarks.benchmark_performance_writes()
