import json
import zmq
import base64
import dateutil.parser
import math


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


class ImageRequestData(object):
    def __init__(self, data):
        [setattr(self, key, value) for key, value in data.items()]

    def make_request_message(self):
        with open(self.path, 'rb') as image:
            data = {
                'image': base64.b64encode(image.read()).decode('ascii')
            }
        message = MessageOut(data)
        return message


def cloud_area_fraction_to_octal(cloud_area_fraction):
    return math.floor((cloud_area_fraction / 100) * 8)


def cloud_area_fraction_to_symbol(cloud_area_fraction):
   # Sun
   if cloud_area_fraction < 0.13:
      return 1
   # Partly cloudy
   elif cloud_area_fraction < 0.38:
      return 2
   # Mostly cloudy
   elif cloud_area_fraction < 0.86:
      return 3
   # Cloudy
   else:
      return 4


def octal_to_symbol(octal):
   cloud_area_fraction = octal_to_percent(octal) / 100
   return cloud_area_fraction_to_symbol(cloud_area_fraction)


def octal_to_percent(octal):
    return (octal * 100) / 8


def unserialize_datetime(dt):
    return dateutil.parser.parse(dt)
