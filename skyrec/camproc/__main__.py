import skyrec.camproc

import logging
import argparse


if __name__ == '__main__':
    requests = 0

    logging.basicConfig(format='%(asctime)s: (%(levelname)s) %(message)s',
                        datefmt='%Y-%m-%dT%H:%M:%S%Z',
                        level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=str, help='ZeroMQ socket for communication')
    args = parser.parse_args()

    logging.info('Starting camproc')
    pipeline = skyrec.camproc.DataPipeline(args.source)
    pipeline.setup()
    logging.info('Now processing data from %s', pipeline.source)

    while True:
        logging.info('Waiting for request...')
        request = pipeline.recv_request()
        requests += 1
        logging.info('Received request %d, now processing...', requests)
        response = skyrec.camproc.DataResponse()
        logging.info('Finished processing request %d, sending response...', requests)
        pipeline.send_response(response)
        logging.info('Sent response to request %d', requests)
