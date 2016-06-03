import zmq
import logging


def main():
    logging.basicConfig(format='%(asctime)s: (%(levelname)s) %(message)s',
                        datefmt='%Y-%m-%dT%H:%M:%S%Z',
                        level=logging.INFO)

    url_worker = "tcp://*:22222"
    url_client = "tcp://*:29999"

    # Prepare our context and sockets
    context = zmq.Context.instance()

    # Socket to talk to clients
    logging.info('Listening for client requests on %s', url_client)
    clients = context.socket(zmq.ROUTER)
    clients.bind(url_client)

    # Socket to talk to workers
    logging.info('Listening for worker offers on %s', url_worker)
    workers = context.socket(zmq.DEALER)
    workers.bind(url_worker)

    # Proxy requests
    logging.info('Now proxying requests')
    zmq.proxy(clients, workers)

    # We never get here but clean up anyhow
    clients.close()
    workers.close()
    context.term()


if __name__ == "__main__":
    main()
