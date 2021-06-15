"""Controller class for television subsystem."""

from shared import config
from shared.controller import Controller

import logging
import pygame
import time
import os
import glob
import random

logger = logging.getLogger()


class Television(Controller):
    """Television controller class."""

    def __init__(self):
        """Initialize."""
        super().__init__()
        self.whoami = "Television"
        self.mode = config.MODE_AUTO
        self.filetable = self.__read_files()
        self.current_year = config.SCHED_YEARS[0]
        self.most_recent = ""
        # used by audio mixer
        # pygame.mixer.init()
        # pygamemixer.music.set_volume(float(config.TV_VOLUME))
        pygame.init()
        clock = pygame.time.Clock()


    """
        SETUP
    """

    def __read_files(self):
        """Look for audio files in data directory and construct dict of arrays of possibilities.

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
        REPORTS
    """

    def get_status(self):
        """Full status for controller."""
        return {
            "running" : True,
            "mode" : self.mode2str(self.mode),
            "currentYear" : self.current_year,
            "most-recent" : self.most_recent
        }

    """
        ORDERS
    """

    def __act_on_order(self, order):
        """
        Take action based on order.

        Possible comnmands:
            - setOff
            - setOn
            - setAuto
            - setGlitch
            - setYear *year*
            - reqStatus
            - reqLog [num_events]
        """
        if not order:
            return
        if "cmd" not in order:
            logging.info(f"No 'cmd' in order received: {order}")
        logging.info(f"Acting on order: {order}")
        #
        # request status
        # Format: {
        #   "cmd" : "reqStatus"
        # }
        #
        if order['cmd'].lower() == "reqstatus":
            print(self.get_status())
        #
        # request log
        # Format: {
        #   "cmd" : "reqLog",
        #   "qty" : **integer**
        # }
        #
        elif order['cmd'].lower() == "reqlog":
            if "qty" in order:
                print(self.get_logs(order["qty"]))
            else:
                print(self.get_logs())
        #
        # set off
        # Format: {
        #   "cmd" : "setOff"
        # }
        #
        elif order['cmd'].lower() == "setoff":
            self.mode = config.MODE_OFF
            self.stop_video()
        #
        # set on
        # Format: {
        #   "cmd" : "setOn"
        # }
        #
        elif order['cmd'].lower() == "seton":
            self.mode = config.MODE_ON
            self.play_new()
        #
        # set auto
        # Format: {
        #   "cmd" : "setAuto"
        # }
        #
        elif order['cmd'].lower() == "setauto":
            self.mode = config.MODE_AUTO
        #
        # set glitch mode
        # Format: {
        #   "cmd" : "setGlitch"
        # }
        #
        elif order['cmd'].lower() == "setglitch":
            self.set_glitch()
        #
        # set year
        # Format: {
        #   "cmd" : "setYear",
        #   "year" : *year*
        # }
        #
        elif order['cmd'].lower() == "setyear":
            if not "year" in order:
                logging.warning(f"invalid order received: {order}")
                return
            self.set_year(order['year'])
        #
        # invalid order
        #
        else:
            logging.warning(f"invalid order received: {order}")

    """
        PLAY STUFF
    """

    def set_glitch(self):
        """Set glitch mode."""
        logging.info("Setting glitch")
        print("Setting glitch")
        self.current_year = "glitch"
        if self.mode != config.MODE_AUTO:
            logging.warning("setGlitch no action taken when not in AUTO mode. Use setAuto command.")
        self.play_new()

    def set_year(self, year):
        """Set year attribute."""
        logging.info(f"Setting year: {year}")
        print(f"Setting year: {year}")
        if str(year) not in config.VALID_YEARS:
            logging.warning("Invalid year: {year}")
            return
        self.current_year = str(year)
        if self.mode != config.MODE_AUTO:
            logging.warning("setYear no action taken when not in AUTO mode. Use setAuto command.")
            return
        self.play_new()

    def play_new(self):
        """Play new video file."""
        filename = random.choice(self.filetable[str(self.current_year)])
        self.most_recent = filename
        logging.info(f"Playing video: {filename}")
        # used by audio mixer
        # pygame.mixer.music.load(filepath + filename)
        # pygame.mixer.music.play()
        movie = pygame.movie.Movie(filename)
        screen = pygame.display.set_mode(movie.get_size())
        movie_screen = pygame.Surface(movie.get_size()).convert()
        movie.set_display(movie_screen)
        movie.play()

    def stop_video(self):
        """Stop currently playing video."""
        pass
        #TODO: Flesh this out

    """
        MAIN LOOP
    """

    def main_loop(self):
        """Get orders and acts on them."""
        while True:
            self.__act_on_order(self.receive_order())
            time.sleep(config.TV_LOOP_DELAY)


    def start(self):
        """Get this party started."""
        logging.info('Starting.')
        self.main_loop()


def main():
    """Test the class."""
    import sys
    logging.basicConfig(filename=sys.stderr,
                        encoding='utf-8',
                        format='%(asctime)s %(levelname)s:%(message)s',
                        level=logging.DEBUG)
    television = Television()
    television.order_act_loop()


if __name__ == '__main__':
    main()
