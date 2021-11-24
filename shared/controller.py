"""Parent class for all controllers."""

from shared import config
from shared.comms import Comms

import logging
# import pprint
# from datetime import datetime, timedelta

logger = logging.getLogger()

class Controller(object):
    """Parent class for all controllers."""

    def __init__(self):
        """Initialize controller."""
        logging.info("Controller initiated")
        self.comms = Comms()
        self.whoami = ""

    """
        REPORTS
    """

    def get_status(self):
        """Brief one-liner status."""
        return f"{self.whoami} is running."

    def tail(self, f, window=1):
        """Return the last `window` lines of file `f` as a list of bytes."""
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

    def get_logs(self, num=config.SCHED_DEFAULT_LOG):
        """Recent log of activity."""
        with open(config.LOG_DIR + self.whoami + ".log", 'rb') as file:
            logs = self.tail(file, int(num)).decode('utf-8')
        return(logs)

    def mode2str(self, mode):
        """Convert mode to string."""
        if mode == config.MODE_OFF:
            return "off"
        elif mode == config.MODE_ON:
            return "on"
        elif mode == config.MODE_AUTO:
            return "auto"
        else:
            return "unknown"

    def stopgo(self, state):
        """Convert constants to go/stop text."""
        if state == config.STATE_GO:
            return "go"
        elif state == config.STATE_STOP:
            return "stop"
        else:
            return "unknown"

    def onoff(self, state):
        """Convert boolean to off/on."""
        if state == config.STATE_ON:
            return "on"
        elif state == config.STATE_OFF:
            return "off"
        else:
            return "unknown"



    """
        ORDERS
    """

    def receive_order(self):
        """Receive orders."""
        order = self.comms.get_order()
        if not order:
            return None
        return order

    """
        MAIN LOOP
    """

    def start(self):
        """Get the party started."""
        logging.info('Starting.')
        self.main_loop()


    def stop(self):
        """Stop the controller."""
        logging.info('Stopping.')
        pass


def main():
    """Test the controller class."""
    import sys
    logging.basicConfig(filename=sys.stderr,
                        encoding='utf-8',
                        format='%(asctime)s %(levelname)s:%(message)s',
                        level=logging.DEBUG)
    controller = Controller()
    controller.start()


if __name__ == '__main__':
    main()
