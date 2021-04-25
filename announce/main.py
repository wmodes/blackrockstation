"""Main loop for announcement subsystem."""

from shared import config
from shared.controller import Controller

from announce.announce import Announce
from shared.streamtologger import StreamToLogger

import sys
import logging
import pprint
from datetime import datetime, timedelta


def main():
    logging.basicConfig(
        filename=config.LOG_FILENAME,
        # encoding='utf-8',
        filemode='a',
        format='%(asctime)s %(levelname)s:%(message)s',
        level=config.LOG_LEVEL)
    logger = logging.getLogger("announce")
    whoami = "Announce"

    # redirect stdout and stderr to log file - do this before production
    # sys.stdout = StreamToLogger(logger,logging.INFO)
    # sys.stderr = StreamToLogger(logger,logging.ERROR)

    # let's get this party started
    announce = Announce()

    try:
        announce.start()
    except KeyboardInterrupt:
        logging.info(f"%s interrupted." % whoami)
        announce.stop()
    except:
        logging.exception('Got exception on main handler')
        raise


if __name__ == '__main__':
    main()
