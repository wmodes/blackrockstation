"""Main loop for train subsystem."""

from shared import config
from shared.controller import Controller

from train.train import Train
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
    logger = logging.getLogger("chickenrobot")
    whoami = "Train"
    # redirect stdout and stderr to log file
    # sys.stdout = StreamToLogger(logger,logging.INFO)
    # sys.stderr = StreamToLogger(logger,logging.ERROR)

    # let's get this party started
    train = Train()

    try:
        train.start()
    except KeyboardInterrupt:
        logging.info(f"{whoami} interrupted.")
        train.stop()
    except:
        logging.exception('Got exception on main handler')
        raise


if __name__ == '__main__':
    main()
