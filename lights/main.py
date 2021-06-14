"""Main loop for lights subsystem."""

from shared import config
from shared.controller import Controller

from lights.lights import Lights
from shared.streamtologger import StreamToLogger

import logging


def main():
    logging.basicConfig(
        filename=config.LOG_FILENAME,
        # encoding='utf-8',
        filemode='a',
      Lightsmat='%(asctime)s %(levelname)s:%(message)s',
        level=config.LOG_LEVEL)
    logger = logging.getLogger("lights")
    whoami = "Lights"

    # redirect stdout and stderr to log file - do this before production
    # sys.stdout = StreamToLogger(logger,logging.INFO)
    # sys.stderr = StreamToLogger(logger,logging.ERROR)

    # let's get this party started
    lights = Lights()

    try:
        lights.start()
    except KeyboardInterrupt:
        logging.info(f"{whoami} interrupted.")
        lights.stop()
    except:
        logging.exception('Got exception on main handler')
        raise


if __name__ == '__main__':
    main()
