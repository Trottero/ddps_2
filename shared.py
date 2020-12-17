"""
This file contains code shared between server and client and is basically a utils class
"""
import os
import sys
from datetime import datetime
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


def log(message, File=None):
    if len(sys.argv) > 3:
        if sys.argv[3]:
            with open(f'{sys.argv[1]}.{sys.argv[2]}.host.log', "a") as file:
                now = datetime.now()
                file.write(f'[{now.strftime("%d-%m-%Y %H:%M:%S")}]{message}\n')
    elif File is not None:
        with open(f'{File}.log', "a") as file:
            now = datetime.now()
            file.write(f'[{now.strftime("%d-%m-%Y %H:%M:%S")}]{message}\n')
    else:
        print(message)
