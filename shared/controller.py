"""Parent class for all controllers."""

import shared.config
from shared.comms import Comms

import logging
import pprint
from datetime import datetime, timedelta


class Controller(object):
    """Parent class for all controllers."""

    def __init__(self):
        logging.info(f"Controller initiated")
        self.comms = Comms()

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
    logging.basicConfig(filename=sys.stderr,
                        encoding='utf-8',
                        format='%(asctime)s %(levelname)s:%(message)s',
                        level=logging.DEBUG)
    logger = logging.getLogger()
    announce = Announce()
    announce.order_act_loop()


if __name__ == '__main__':
    main()
