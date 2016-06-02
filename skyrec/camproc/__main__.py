import skyrec

import logging
import argparse


if __name__ == '__main__':
    requests = 0

    logging.basicConfig(format='%(asctime)s: (%(levelname)s) %(message)s',
                        datefmt='%Y-%m-%dT%H:%M:%S%Z',
                        level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument('addr', type=str, help='ZeroMQ socket for communication')
    args = parser.parse_args()

    logging.info('Starting camproc')
    pipeline = skyrec.DataRepPipeline(args.addr)
    logging.info('Now processing data from %s', pipeline.addr)

    while True:
        logging.info('Waiting for request...')
        request = pipeline.recv()
        requests += 1
        logging.info('Received request %d, now processing...', requests)
        logging.info('Request payload: %s', request.serialize())
        response = skyrec.MessageOut('PONG')
        logging.info('Finished processing request %d, sending response...', requests)
        logging.info('Response payload: %s', response.serialize())
        pipeline.send(response)
        logging.info('Sent response to request %d', requests)
