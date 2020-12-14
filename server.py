"""
This class serves as the main server which will be running on every node.
Upon launching, it calls the KeyValueStore() constructor, this will initialize the
Node further
"""

from concurrent import futures
import logging
import sys
import grpc

import keyvaluestore_pb2
import keyvaluestore_pb2_grpc
import keyvaluestore


def serve(nodeId):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    keyvaluestore_pb2_grpc.add_KeyValueStoreServicer_to_server(keyvaluestore.KeyValueStore(nodeId), server)

    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    if len(sys.argv) < 2:
        print("Failed to start server, argument missing!")
        print(f"Usage: python {sys.argv[0].split('/')[-1]} <HOSTNAME>")
        sys.exit()
    serve(sys.argv[1])
