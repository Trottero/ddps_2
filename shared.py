"""
This file contains code shared between server and client and is basically a utils class
"""
import os
import sys
import numpy as np


def read_hosts():
    dirname = os.path.dirname(__file__)
    hostpath = os.path.join(dirname, 'hosts')
    return [l.strip() for l in open(hostpath).readlines()]


def host_index(host):
    hosts = read_hosts()
    return hosts.index(host)


def random_host():
    hosts = read_hosts()
    random_host = np.random.randint(low=0, high=len(hosts))
    return hosts[random_host]


def log(message):
    if len(sys.argv) > 3:
        if sys.argv[3]:
            with open(f'{sys.argv[1]}.{sys.argv[2]}.host.log', "a") as file:
                file.write(message + '\n')
    else:
        print(message)
