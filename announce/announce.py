"""Controller class for announcement subsystem."""

# goddamn it, what's the proper way to do this??????
# given that we want to run announce/main.py to also to test the class?
from blackrockstation.shared import config
from blackrockstation.shared.controller import Controller
# and how do I run this package properly to test it??

import logging
import pprint
from datetime import datetime, timedelta

logger = logging.getLogger()

class Announce(Controller):
    """Announcements controller class."""

    def __init__(self, arg):
        super(Announce, self).__init__()
        self.arg = arg

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
    announce = Announce()
    announce.order_act_loop()

if __name__ == '__main__':
    main()
