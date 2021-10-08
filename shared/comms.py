"""Comms class for all controllers."""

from shared import config

import logging
# import pprint
from datetime import datetime
import os
import json
import requests

class Comms(object):
    """Comm class for all controllers."""

    def __init__(self):
        """Initialize class."""
        self.__order_queue = []
        self.__controller_table = {
            "announce": config.ANNOUNCE_SRV,
            "crossing": config.CROSS_SRV,
            "lights": config.LIGHTS_SRV,
            "radio": config.RADIO_SRV,
            "scheduler": config.SCHED_SRV,
            "bridge": config.BRIDGE_SRV,
            "train": config.ANNOUNCE_SRV,
            "television": config.TV_SRV
        }
        logging.info("Comms initiated")

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
                print(f"Order proper syntax: {order}")
            except:
                logging.warning(f"Order syntax error: {order_json}")
                print(f"Order syntax error: {order_json}")
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
        print(f"{datetime.now().strftime('%H:%M:%S')} Sending command to {controller}: {str(cmd_obj)}")
        server = self.__controller_table[controller]
        try:
            return_val = requests.post(server, json=cmd_obj)
        except requests.exceptions.RequestException as error:
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
