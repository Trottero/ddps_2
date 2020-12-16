
import keyvaluestore_pb2
import keyvaluestore_pb2_grpc


def run_kv_test(channel):
    """
    Simple function which tests basic retrieval / storage of keys
    """
    stub = keyvaluestore_pb2_grpc.KeyValueStoreStub(channel)
    response = stub.SetValue(keyvaluestore_pb2.SetRequest(key='1', value='banaan 1'))
    print('Response.key: ', response.key)
    response = stub.GetValues(keyvaluestore_pb2.GetRequest(key='1'))
    print('Response.value:', response.value)
