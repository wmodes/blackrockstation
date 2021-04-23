# announce - a controller for announcement system
# authors: Wes Modes <wmodes@gmail.com>
# date: Apr 2021
# license: MIT

# this fucker. How's this supposed to be???
import shared.config

import logging
import pprint
from datetime import datetime, timedelta

class Controller(object):
    """Parent class for all controllers."""

    def __init__(self, arg):
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
