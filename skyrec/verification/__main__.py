import argparse
import dateutil.parser
import logging
import pandas
import csv
import os
import sys
import base64
import math

import skyrec


class VerificationData(object):
    def __init__(self, data):
        [setattr(self, key, value) for key, value in data.items()]

    def make_request_message(self):
        with open(self.path, 'rb') as image:
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


def cloud_area_fraction_to_octal(cloud_area_fraction):
    return math.floor((cloud_area_fraction / 100) * 8)


def octal_to_percent(octal):
    return (octal * 100) / 8


def unserialize_datetime(dt):
    return dateutil.parser.parse(dt)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s: (%(levelname)s) %(message)s',
                        datefmt='%Y-%m-%dT%H:%M:%S%Z',
                        level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument('addr', type=str, help='ZeroMQ bind address')
    parser.add_argument('csv', type=str, help='CSV file containing input data')
    parser.add_argument('--path', type=str, help='Path to prepend to source images', default='.', required=False)
    parser.add_argument('--verbose', type=bool, help='Print entire table of values after processing', default=False, required=False)
    args = parser.parse_args()

    pipeline = skyrec.DataReqPipeline(args.addr)
    index = []
    datas = []

    for line in line_from_csv(args.csv):
        line['path'] = os.path.realpath(os.path.join(args.path, line['filename']))
        vdata = VerificationData(line)
        logging.debug('Start processing %s', vdata.filename)
        logging.debug(line)
        request = vdata.make_request_message()
        pipeline.send(request)
        response = pipeline.recv()

        dt = unserialize_datetime(line['timestamp'])
        data = {
            'timestamp': dt,
            'hour': dt.hour,
            'skyrec': cloud_area_fraction_to_octal(response.data['cloud_area_fraction']),
            'arome': int(line['AROME']),
            'observed': int(line['observed']),
        }
        data['distance_skyrec_arome'] = abs(data['arome'] - data['skyrec'])
        data['distance_skyrec_observed'] = abs(data['observed'] - data['skyrec'])
        data['distance_arome_observed'] = abs(data['arome'] - data['observed'])

        index.append(line['filename'])
        datas.append(data)

    frame = pandas.DataFrame(datas, index)
    frame.sort_values('timestamp')

    if args.verbose:
        frame.to_string(buf=sys.stdout, columns=None, justify='left')
        print()

    logging.info('Processed a total of %d images from %s to %s', len(index), frame['timestamp'][0], frame['timestamp'][-1])

    logging.info('Mean error skyrec vs. AROME         : %.1f%%', octal_to_percent(frame['distance_skyrec_arome'].mean()))
    logging.info('Mean error skyrec vs. observation   : %.1f%%', octal_to_percent(frame['distance_skyrec_observed'].mean()))
    logging.info('Mean error AROME vs. observation    : %.1f%%', octal_to_percent(frame['distance_arome_observed'].mean()))

    logging.info('Median error skyrec vs. AROME       : %.1f%%', octal_to_percent(frame['distance_skyrec_arome'].median()))
    logging.info('Median error skyrec vs. observation : %.1f%%', octal_to_percent(frame['distance_skyrec_observed'].median()))
    logging.info('Median error AROME vs. observation  : %.1f%%', octal_to_percent(frame['distance_arome_observed'].median()))