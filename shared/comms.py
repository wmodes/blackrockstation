"""Comms class for all controllers."""

import shared.config

import logging
import pprint


class Comms(object):
    """Comm class for all controllers."""

    def __init__(self):
        self.__order_queue = []
        logging.info(f"Comms initiated")

    def get_order(self):
        """Get order from queue"""
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
        print(f"Sending command to {controller}: {command}")


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
