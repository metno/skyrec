import argparse
import logging
import csv
import os
import base64

import skyrec


class VerificationData(object):
    def __init__(self, data):
        [setattr(self, key, value) for key, value in data.items()]

    def make_request_message(self):
        with open(self.filename, 'rb') as image:
            data = {
                'image': base64.b64encode(image.read()).decode('ascii')
            }
        message = skyrec.MessageOut(data)
        return message


def line_from_csv(path):
    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            yield row


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s: (%(levelname)s) %(message)s',
                        datefmt='%Y-%m-%dT%H:%M:%S%Z',
                        level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument('addr', type=str, help='ZeroMQ bind address')
    parser.add_argument('csv', type=str, help='CSV file containing input data')
    parser.add_argument('--path', type=str, help='Path to prepend to source images', default='.', required=False)
    args = parser.parse_args()

    pipeline = skyrec.DataReqPipeline(args.addr)

    for line in line_from_csv(args.csv):
        line['filename'] = os.path.realpath(os.path.join(args.path, line['filename']))
        vdata = VerificationData(line)
        logging.info('Start processing %s', vdata.filename)
        logging.info(line)
        request = vdata.make_request_message()
        pipeline.send(request)
        response = pipeline.recv()
