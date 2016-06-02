import argparse
import logging
import csv

import skyrec


class VerificationData(object):
    def __init__(self, data):
        [setattr(self, key, value) for key, value in data.items()]


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
    args = parser.parse_args()

    pipeline = skyrec.DataReqPipeline(args.addr)

    for line in line_from_csv(args.csv):
        vdata = VerificationData(line)
        logging.info('Should process %s', vdata.filename)
        logging.info(line)
        request = skyrec.MessageOut('PING')
        pipeline.send(request)
        response = pipeline.recv()
