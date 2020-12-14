import keyvaluestore_pb2_grpc
import keyvaluestore_pb2


class KeyValueStore(keyvaluestore_pb2_grpc.KeyValueStoreServicer):
    # This is launched upon launching the server, we initialize the keyvalue store here and the nodes that it should connect to.
    # This also means that we should do the logic of a node joining the circle here
    def __init__(self, nodenumber):
        self.fingertable = []
        self.table = {}

        pass

    def GetValues(self, request, context):
        value = self.table[request.key]
        return keyvaluestore_pb2.GetResponse(value=value)

    def SetValue(self, request, context):
        self.table[request.key] = request.value
        return keyvaluestore_pb2.SetResponse(key=request.key)

    def IsInRange(self, key):

        pass
