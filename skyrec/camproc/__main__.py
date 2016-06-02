import skyrec

import base64
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

        try:
            if 'image' not in request.data:
                raise Exception('Missing image payload')
            request.data['image'] = base64.b64decode(request.data['image'])
        except Exception as e:
            logging.warning('Invalid payload received, discarding.')
            pipeline.send(MessageOut({'error': str(e)}))
            continue

        # FIXME: do processing and replace with sensible data
        response = skyrec.MessageOut({'cloud_area_fraction': 0.0})

        logging.info('Finished processing request %d, sending response...', requests)
        logging.info('Response payload: %s', response.serialize())
        pipeline.send(response)
        logging.info('Sent response to request %d', requests)
