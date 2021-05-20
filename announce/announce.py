"""Controller class for announcement subsystem."""

from shared import config
from shared.controller import Controller

import logging
from pprint import pprint
from datetime import datetime, timedelta
from pygame import mixer
import csv
import time

logger = logging.getLogger()


class Announce(Controller):
    """Announcements controller class."""

    def __init__(self):
        super().__init__()
        self.whoami = "announce"
        self.enabled = True
        self.filetable = self.__read_filetable()
        mixer.init()
        mixer.music.set_volume(float(config.ANNOUNCE_VOLUME))

    """
        SETUP
    """

    def __read_filetable(self):
        logging.info('Reading file table')
        filetable = {}
        with open(config.ANNOUNCE_FILE_TABLE, newline='') as csvfile:
            reader = csv.DictReader(csvfile, config.ANNOUNCE_FILE_FIELDS)
            # skips the header line
            next(reader)
            for row in reader:
                # skip blank lines
                if row['announcement'] == '':
                    continue;
                index = row['announceid']
                filetable[index] = row['filename']
        return filetable

    """
        ORDERS
    """

    def __act_on_order(self, order):
        """
        Takes action based on order.

        Possible comnmands:
            - set off
            - set on
            - set glitch
            - set announce *id* *year*
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
        # set off
        #
        elif order.startswith("set off"):
            self.enabled = False
        #
        # set on
        #
        elif order.startswith("set on"):
            self.enabled = True
        #
        # set glitch
        #
        elif order.startswith("set glitch"):
            self.set_glitch()
        #
        # set announce
        #
        elif order.startswith("set announce"):
            order_list = order.split()
            announceid = order_list[2]
            year = int(order_list[3])
            self.set_announce(announceid, year)
        #
        # invalid order
        #
        else:
            logging.info(f"invalid order received: {order}")

    """
        PLAY STUFF
    """

    def set_glitch(self):
        pass

    def set_announce(self, announceid, year):
        filepath = config.ANNOUNCE_AUDIO_DIR
        filename = f"{str(year)}-{announceid}{config.ANNOUNCE_AUDIO_EXT}"
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
            time.sleep(config.ANNOUNCE_LOOP_DELAY)


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
    announce = Announce()
    announce.order_act_loop()


if __name__ == '__main__':
    main()
