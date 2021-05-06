"""Controller class for trainaudio subsystem."""

from shared import config
from shared.controller import Controller

import logging
from pprint import pprint
from datetime import datetime, timedelta

logger = logging.getLogger()


class Trainaudio(Controller):
    """Trainaudio controller class."""

    def __init__(self):
        super().__init__()
        self.whoami = "trainaudio"
        self.__read_filetable()

    """
        SETUP
    """

    # TODO: This should be moved to trainaudio controller
    def __read_filetable(self):
        logging.info('Reading file table')
        self.filetable = {}
        with open(config.TRAIN_FILE_TABLE, newline='') as csvfile:
            reader = csv.DictReader(csvfile, config.TRAIN_FILE_FIELDS)
            # skips the header line
            next(reader)
            for row in reader:
                # skip blank lines
                if row['year'] != '':
                    # skip unregistered types
                    if row['traintype'] not in config.TRAIN_TYPES:
                        logger.info(f"skipped unregistered train type: {row['traintype']}")
                        continue
                    # add filename to filetable
                    index = f"{row['year']}-{row['type']}"
                    self.filetable[index] = row['filename']
            pprint(self.filetable)

    """
        ORDERS
    """

    def __receive_orders(self):
        """Receives orders"""
        pass

    def __act_on_orders(arg, orders):
        """Takes action based on orders"""
        pass

    """
        MAIN LOOP
    """

    def main_loop(self):
        """Gets orders and acts on them"""
        pass



def main():
    """For testing the class"""
    import sys
    logging.basicConfig(filename=sys.stderr,
                        encoding='utf-8',
                        format='%(asctime)s %(levelname)s:%(message)s',
                        level=logging.DEBUG)
    logger = logging.getLogger()
    trainaudio = Trainaudio()
    trainaudio.order_act_loop()


if __name__ == '__main__':
    main()
