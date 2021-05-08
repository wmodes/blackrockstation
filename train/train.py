"""Controller class for train subsystem."""

from shared import config
from shared.controller import Controller

import logging
from pprint import pprint
from datetime import datetime, timedelta
from pygame import mixer
import csv
import time

logger = logging.getLogger()


class Train(Controller):
    """Train controller class."""

    def __init__(self):
        super().__init__()
        self.whoami = "train"
        self.enabled = True
        self.filetable = self.__read_filetable()
        mixer.init()
        mixer.music.set_volume(float(config.TRAIN_VOLUME))

    """
        SETUP
    """

    def __read_filetable(self):
        logging.info('Reading file table')
        filetable = {}
        with open(config.TRAIN_FILE_TABLE, newline='') as csvfile:
            reader = csv.DictReader(csvfile, config.TRAIN_FILE_FIELDS)
            # skips the header line
            next(reader)
            for row in reader:
                # skip blank lines
                if row['year'] == '':
                    continue
                # add filename to filetable
                index = f"{row['year']}-{row['type']}"
                filetable[index] = row['filename']
        pprint(filetable)
        return filetable

    """
        ORDERS
    """

    def __act_on_order(self, order):
        """Takes action based on order.

        Possible commands:
            - set off
            - set on
            - set train *direction* *type* *year*
            - request status
            - request log [num_events]
            - request report
        """
        if not order:
            return
        logging.debug(f"Acting on order: {order}")
        #
        # request status
        #
        if order.startswith("request status"):
            print(self.report_status())
        #
        # request log
        #
        elif order.startswith("request log"):
            order_list = order.split()
            if len(order_list) > 2:
                print(self.report_logs(int(order_list[2])))
            else:
                print(self.report_logs())
        #
        # request status
        #
        elif order.startswith("request report"):
            print(self.full_report())
        #
        # request off
        #
        elif order.startswith("request off"):
            self.enabled = False
        #
        # request on
        #
        elif order.startswith("request on"):
            self.enabled = True
        #
        # set train
        #   set train *direction* *type* *year*
        #
        elif order.startswith("set train"):
            order_list = order.split()
            direction = order_list[2]
            type = order_list[3]
            year = int(order_list[4])
            self.set_train(direction, type, year)
        #
        # invalid order
        #
        else:
            logging.info(f"invalid order received: {order}")

    """
        PLAY STUFF
    """

    def set_train(self, direction, type, year):
        logging.debug(f"Setting train: {direction} {type} {year}")
        filepath = config.TRAIN_AUDIO_DIR
        filename = self.filetable[f"{year}-{type}"]
        logging.debug(f"Train audio filename: {filename}")
        logging.info(f"Playing audio: {filename}")
        mixer.music.load(filepath + filename)
        mixer.music.play()

    """
        MAIN LOOP
    """

    def main_loop(self):
        """Gets orders and acts on them"""
        while True:
            self.__act_on_order(self.receive_order())
            time.sleep(config.TRAIN_LOOP_DELAY)


    def start(self):
        logging.info('Starting.')
        print(self.full_report)
        self.main_loop()


def main():
    """For testing the class"""
    import sys
    logging.basicConfig(filename=sys.stderr,
                        encoding='utf-8',
                        format='%(asctime)s %(levelname)s:%(message)s',
                        level=logging.DEBUG)
    logger = logging.getLogger()
    train = Train()
    train.order_act_loop()


if __name__ == '__main__':
    main()
