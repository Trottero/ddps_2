"""
This class serves as the main server which will be running on every node.
Upon launching, it calls the KeyValueStore() constructor, this will initialize the
Node further.
"""

from concurrent import futures
import logging
import sys
import grpc
import shared

import keyvaluestore_pb2
import keyvaluestore_pb2_grpc
import keyvaluestore


def serve(nodeId, port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    keyvaluestore_pb2_grpc.add_KeyValueStoreServicer_to_server(keyvaluestore.KeyValueStore(f'{nodeId}:{port}'), server)

    server.add_insecure_port(f'{nodeId}:{port}')
    server.start()
    shared.log(f'Started GRPC server on port: {port}')
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    if len(sys.argv) < 3:
        print("Failed to start server, argument missing!")
        print(f"Usage: python {sys.argv[0].split('/')[-1]} <HOSTNAME> <PORT>")
        sys.exit()
    serve(sys.argv[1], sys.argv[2])
