"""Controller class for scheduler subsystem."""

from shared import config
from shared.controller import Controller

import logging
import pprint
from datetime import datetime, timedelta

logger = logging.getLogger()

class Scheduler(Controller):
    """Scheduler controller class."""

    def __init__(self):
        super(Scheduler, self).__init__()

    def status(self):
        """Brief one-liner status"""
        pass

    def logs(self):
        """Recent log of activity"""
        pass

    def report(self):
        """Full multi-line readable report of activity"""
        pass

    def __receive_orders(self):
        """Receives orders"""
        pass

    def __ack_orders(self):
        """Acknowledges orders received"""

    def __act_on_orders(arg, orders):
        """Takes action based on orders"""
        pass

    def order_act_loop(self):
        """Gets orders and acts on them"""
        pass

    def start(self):
        print ("Scheduler: starting")
        logging.info('Starting.')
        pass

    def stop(self):
        logging.info('Stopping.')
        pass

def main():
    """For testing the class"""
    import sys
    logging.basicConfig(
        filename=sys.stderr,
        encoding='utf-8',
        format='%(asctime)s %(levelname)s:%(message)s',
        level=logging.DEBUG
    )
    logger = logging.getLogger()
    scheduler = Scheduler()
    scheduler.order_act_loop()

if __name__ == '__main__':
    main()
