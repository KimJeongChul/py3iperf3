import logging
import asyncio
import time
import os

from py3iperf3.iperf3_client import Iperf3Client

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(asctime)s %(message)s')

if __name__ == '__main__':
    logging.info('Starting program')
    loop = asyncio.get_event_loop()

    params = {
        'server_address':'127.0.0.1',
        'server_port':5201,
    }

    client = Iperf3Client(loop=loop)
    test = client.create_test(test_parameters=params)

    if os.name == 'nt':
        def wakeup():
            # Call again later
            loop.call_later(0.5, wakeup)
        loop.call_later(0.5, wakeup)

    try:
        loop.call_soon(client.run_all_tests)
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    logging.info('Closing client')
    client.stop_all_tests()
    loop.close()
    logging.shutdown()
