"""Main loop for scheduler subsystem."""

from shared import config
# from shared.controller import Controller

from scheduler.scheduler import Scheduler
# from shared.streamtologger import StreamToLogger

# import sys
import logging
# import pprint
# from datetime import datetime, timedelta


def main():
    """Set up main function."""
    logging.basicConfig(
        filename=config.LOG_FILENAME,
        # encoding='utf-8',
        filemode='a',
        format='%(asctime)s %(levelname)s:%(message)s',
        level=config.LOG_LEVEL)
    logger = logging.getLogger("scheduler")
    whoami = "Scheduler"

    # redirect stdout and stderr to log file - do this before production
    # sys.stdout = StreamToLogger(logger,logging.INFO)
    # sys.stderr = StreamToLogger(logger,logging.ERROR)

    # let's get this party started
    scheduler = Scheduler()

    try:
        scheduler.start()
    except KeyboardInterrupt:
        logging.info(f"{whoami} interrupted.")
        scheduler.stop()
    except:
        logging.exception('Got exception on main handler')
        raise


if __name__ == '__main__':
    main()
