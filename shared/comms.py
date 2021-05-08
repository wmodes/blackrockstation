"""Comms class for all controllers."""

from shared import config

import logging
import pprint
from datetime import datetime
import os

class Comms(object):
    """Comm class for all controllers."""

    def __init__(self):
        self.__order_queue = []
        logging.info(f"Comms initiated")

    def get_order(self):
        """Get order from queue"""
        #
        # temp solution to getting orders: check .order file
        if os.path.exists(config.ORDER_FILE):
            with open(config.ORDER_FILE) as file:
                orders = file.readlines()
            os.remove(config.ORDER_FILE)
            self.__order_queue += orders
        #
        # we return you to your regularly scheduled code
        if len(self.__order_queue) == 0:
            order = None
        else:
            order = self.__order_queue.pop(0)
            logging.info(f"Reading comms queue: {order}.")
        return order


    def add_order(self, order):
        """Add an order to queue for testing purposes"""
        logging.info(f"Adding order to comms queue: {order}.")
        self.__order_queue.append(order)


    def send_order(self, controller, command):
        """Send an arbitrary order to another controller"""
        logging.info(f"Sending command to {controller}: {command}")
        print(f"{datetime.now().strftime('%H:%M:%S')} Sending command to {controller}: {command}")


def main():
    import sys
    logging.basicConfig(filename=sys.stderr,
                        encoding='utf-8',
                        format='%(asctime)s %(levelname)s:%(message)s',
                        level=logging.DEBUG)
    logger = logging.getLogger()
    comms = Comms()


if __name__ == '__main__':
    main()
