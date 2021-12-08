"""Comms class for all controllers."""

from shared import config

import logging
from datetime import datetime
import os
import json
import requests

logger = logging.getLogger()
logger.setLevel(config.LOG_LEVEL)

class Comms(object):
    """Comm class for all controllers."""

    def __init__(self):
        """Initialize class."""
        self.__order_queue = []
        self.make_controller_table()
        logging.info("Comms initiated")

    def make_controller_table(self):
        self.__controller_table = {}
        for key, value in config.CONTROLLERS.items():
            url = f"http://{value['server']}:{value['port']}/cmd"
            self.__controller_table[key] = url
        # logging.debug(f"controller table: {str(self.__controller_table)}")

    def get_order(self):
        """Get order from queue."""
        #
        # temp solution to getting orders: check .order file
        if os.path.exists(config.ORDER_FILE):
            with open(config.ORDER_FILE) as file:
                order_json = file.read()
            os.remove(config.ORDER_FILE)
            try:
                order = json.loads(order_json)
                self.__order_queue.append(order)
                logging.info(f"Order proper syntax: {order}")
            except:
                logging.warning(f"Order syntax error: {order_json}")
        #
        # we return you to your regularly scheduled code
        if len(self.__order_queue) == 0:
            order = None
        else:
            order = self.__order_queue.pop(0)
            logging.info(f"Reading comms queue: {order}.")
        return order


    def add_order(self, order):
        """Add an order to queue for testing purposes."""
        logging.info(f"Adding order to comms queue: {order}.")
        self.__order_queue.append(order)


    def send_order(self, controller, cmd_obj):
        """Send an arbitrary order to another controller."""
        logging.info(f"Sending command to {controller}: {str(cmd_obj)}")
        server = self.__controller_table[controller]
        try:
            response = requests.post(server, json=cmd_obj, timeout=config.COMMS_TIMEOUT)
            return_val = json.loads(response.text)
        except (requests.exceptions.RequestException, json.decoder.JSONDecodeError) as error:
            return_val = {'status': 'FAIL',
                          'error': str(error)}
        return return_val


def main():
    """Set up test for class."""
    import sys
    logging.basicConfig(filename=sys.stderr,
                        encoding='utf-8',
                        format='%(asctime)s %(levelname)s:%(message)s',
                        level=logging.DEBUG)
    logger = logging.getLogger()
    comms = Comms()


if __name__ == '__main__':
    main()
