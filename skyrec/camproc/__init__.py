import zmq


class DataRequest(object):
    def __init__(self, msg):
        pass


class DataResponse(object):
    def __init__(self):
        pass


class DataPipeline(object):
    def __init__(self, source):
        self.source = source

    def setup(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.connect(self.source)

    def recv_request(self):
        msg = self.socket.recv()
        req = DataRequest(msg)
        return req
