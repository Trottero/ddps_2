"""
This file contains code shared between server and client and is basically a utils class
"""
import os


def read_hosts():
    dirname = os.path.dirname(__file__)
    hostpath = os.path.join(dirname, 'hosts')
    return [l.strip() for l in open(hostpath).readlines()]


def host_index(host):
    hosts = read_hosts()
    return hosts.index(host)
