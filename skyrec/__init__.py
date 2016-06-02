import json
import zmq


class MessageBase(object):
    def __init__(self, data={}):
        self.data = data

    def serialize(self):
        return json.dumps(self.data)

    def unserialize(self, data):
        self.data = json.loads(data)


class MessageIn(MessageBase):
    pass


class MessageOut(MessageBase):
    pass


class DataPipeline(object):
    def __init__(self, addr):
        self.addr = addr
        self.setup()

    def setup(self):
        raise NotImplementedError('Please implement the setup() method.')

    def recv(self):
        msg = self.socket.recv_json()
        req = MessageIn()
        req.unserialize(msg)
        return req

    def send(self, dataresponse):
        if not isinstance(dataresponse, MessageOut):
            raise RuntimeError('You must provide a response object of type MessageOut, not %s' % type(dataresponse))
        msg = dataresponse.serialize()
        self.socket.send_json(msg)


class DataReqPipeline(DataPipeline):
    def setup(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.bind(self.addr)


class DataRepPipeline(DataPipeline):
    def setup(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.connect(self.addr)
