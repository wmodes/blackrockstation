"""Controller class for television subsystem."""

from shared import config
from shared.controller import Controller

import logging
from pprint import pprint
from datetime import datetime, timedelta
import pygame
import csv
import time
import os
import glob
import random

logger = logging.getLogger()


class Television(Controller):
    """Television controller class."""

    def __init__(self):
        super().__init__()
        self.whoami = "television"
        self.enabled = True
        self.filetable = self.__read_files()
        self.current_year = "config.SCHED_YEARS[0]"
        # used by audio mixer
        # pygame.mixer.init()
        # pygamemixer.music.set_volume(float(config.TV_VOLUME))
        pygame.init()
        clock = pygame.time.Clock()


    """
        SETUP
    """

    def __read_files(self):
        """
        Look for audio files in data directory and construct dict of arrays of possibilities.
        {
            "glitch": ["glitch-file1.mp4", "glitch-file2.mp4"],
            "1888": ["1888-file1.mp4", "1888-file2.mp4"],
            . . .
        }
        Note that if you add files, you will have to restart the controller.
        """
        # create a dict of files
        file_dict = {}
        # find all the subdirs in the data dir
        data_subdirs = next(os.walk(config.TV_VIDEO_DIR))[1]
        # find all the files in each subdir
        for subdir in data_subdirs:
            full_subdir = config.TV_VIDEO_DIR + subdir
            file_list = glob.glob(full_subdir + '/*' + config.TV_VIDEO_EXT)
            file_dict[subdir] = file_list
        return file_dict


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
            - set year *year*
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
        # set glitch
        #
        elif order.startswith("set glitch"):
            self.set_glitch()
        #
        # set year
        #
        elif order.startswith("set year"):
            order_list = order.split()
            year = order_list[2]
            self.set_year(year)
        #
        # invalid order
        #
        else:
            logging.info(f"invalid order received: {order}")

    """
        PLAY STUFF
    """

    def set_glitch(self):
        logging.info("Setting glitch")
        print("Setting glitch")
        self.current_year = "glitch"
        self.play_new()

    def set_year(self, year):
        logging.info(f"Setting year: {year}")
        print(f"Setting year: {year}")
        self.current_year = str(year)
        self.play_new()

    def play_new(self):
        filename = random.choice(self.filetable[str(self.current_year)])
        logging.info(f"Playing video: {filename}")
        # used by audio mixer
        # pygame.mixer.music.load(filepath + filename)
        # pygame.mixer.music.play()
        movie = pygame.movie.Movie(filename)
        screen = pygame.display.set_mode(movie.get_size())
        movie_screen = pygame.Surface(movie.get_size()).convert()
        movie.set_display(movie_screen)
        movie.play()

    """
        MAIN LOOP
    """

    def main_loop(self):
        """Gets orders and acts on them"""
        while True:
            self.__act_on_order(self.receive_order())
            time.sleep(config.TV_LOOP_DELAY)


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
    television = Television()
    television.order_act_loop()


if __name__ == '__main__':
    main()
