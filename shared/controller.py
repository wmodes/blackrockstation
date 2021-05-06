"""Parent class for all controllers."""

from shared import config
from shared.comms import Comms

import logging
import pprint
from datetime import datetime, timedelta


class Controller(object):
    """Parent class for all controllers."""

    def __init__(self):
        logging.info(f"Controller initiated")
        self.comms = Comms()
        self.whoami = ""

    """
        REPORTS
    """

    def report_status(self):
        """Brief one-liner status"""
        return f"{self.whoami} is running."

    def tail(self, f, window=1):
        """
        Returns the last `window` lines of file `f` as a list of bytes.
        """
        if window == 0:
            return b''
        BUFSIZE = 1024
        f.seek(0, 2)
        end = f.tell()
        nlines = window + 1
        data = []
        while nlines > 0 and end > 0:
            i = max(0, end - BUFSIZE)
            nread = min(end, BUFSIZE)
            f.seek(i)
            chunk = f.read(nread)
            data.append(chunk)
            nlines -= chunk.count(b'\n')
            end -= nread
        return b'\n'.join(b''.join(reversed(data)).splitlines()[-window:])

    def report_logs(self, num=config.SCHED_DEFAULT_LOG):
        """
        Recent log of activity.
        """
        with open(config.LOG_FILENAME, 'rb') as file:
            logs = self.tail(file, num).decode('utf-8')
        return(f"RECENT LOGS\n===========\n{logs}")

    def full_report(self):
        """
        Full multi-line readable report of activity.
        """
        report = self.report_status() + "\n\n"
        report += self.report_logs(10)
        return report

    """
        ORDERS
    """

    def receive_order(self):
        """
        Receives orders.
        """
        order = self.comms.get_order()
        if not order:
            return None
        return order

    """
        MAIN LOOP
    """

    def start(self):
        logging.info('Starting.')
        self.main_loop()


    def stop(self):
        logging.info('Stopping.')
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
