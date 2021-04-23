# announce - a controller for announcement system
# authors:
#   Black Rock Transportation Company <info@blackrocktrainstation.com>
# date: Apr 2021
# license: MIT

# goddamn it, what's the proper way to do this??????
from ..shared import config
from ..shared.controller import Controller
# and how do I run this package properly to test it??

from announce import Announce
import logging
import pprint
from datetime import datetime, timedelta

def main():
    logging.basicConfig(
        filename=config.LOG_FILENAME,
        # encoding='utf-8',
        filemode='a',
        format='%(asctime)s %(levelname)s:%(message)s',
        level=config.LOG_LEVEL
    )
    logger = logging.getLogger("chickenrobot")
    whoami = "Announce"
    # redirect stdout and stderr to log file
    sys.stdout = StreamToLogger(logger,logging.INFO)
    sys.stderr = StreamToLogger(logger,logging.ERROR)
    # logging.debug('This message should go to the log file')
    # logging.info('So should this')
    # logging.warning('And this, too')
    # logging.error('And non-ASCII stuff, too, like Øresund and Malmö')

    # let's get this party started
    announce = Announce()

    try:
       announce.start()
    except KeyboardInterrupt:
        logging.info(whoami . ' interrupted.')
        announce.stop()
    except:
        logging.exception('Got exception on main handler')
        raise

if __name__ == '__main__':
    main()
