# announce - a controller for announcement system
# authors:
#   Wes Modes <wmodes@gmail.com>
#   Brandon Kinman <Brandon@kinmantech.org>
# date: Apr 2021
# license: MIT

# goddamn it, what's the proper way to do this??????
from ..shared import config
from ..shared.controller import Controller
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

def main():
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
