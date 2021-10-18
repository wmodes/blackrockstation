"""Controller class for television subsystem."""

from shared import config
from shared.controller import Controller

import logging
import time
import os
import glob
import random
import platform
import subprocess
import requests

logger = logging.getLogger()


class Television(Controller):
    """Television controller class."""

    def __init__(self):
        """Initialize."""
        super().__init__()
        self.whoami = "television"
        self.system = self.__determine_platform()
        self.mode = config.MODE_AUTO
        self.current_year = config.SCHED_YEARS[0]
        self.most_recent = ""
        self.video_thread = None

    """
        SETUP
    """

    def __determine_platform(self):
        """
        Determine platform we are running on.

        Returns a short string we can use as an index.
        """
        if 'arm' in platform.platform().lower():
            return "rapsi"
        elif 'darwin' in platform.platform().lower():
            return "macos"

    def __read_files(self):
        """UNUSED: Look for audio files in data directory and construct dict of arrays of possibilities.

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
            "controller" : self.whoami,
            "running" : True,
            "mode" : self.mode2str(self.mode),
            "currentYear" : self.current_year,
            "most-recent" : self.most_recent
        }

    """
        ORDERS
    """

    def act_on_order(self, order):
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
            error = "No command received"
            return_val = {'status': 'FAIL',
                          'error': error}
            return return_val
        if "cmd" not in order:
            error = f"No 'cmd' in order received: '{order}'"
            logging.info(error)
            return_val = {'status': 'FAIL',
                          'error': error}
            return return_val
        #
        # request status
        # Format: {
        #   "cmd" : "reqStatus"
        # }
        #
        if order['cmd'].lower() == "reqstatus":
            return_val = {'status': 'OK',
                       'cmd': 'reqStatus',
                       'results': self.get_status()}
            return return_val
        #
        # request log
        # Format: {
        #   "cmd" : "reqLog",
        #   "qty" : **integer**
        # }
        #
        elif order['cmd'].lower() == "reqlog":
            if "qty" in order:
                results = self.get_logs(order["qty"])
            else:
                results = self.get_logs()
            return_val = {'status': 'OK',
                          'cmd': 'reqLogs',
                          'results': results}
            return return_val
        #
        # set off
        # Format: {
        #   "cmd" : "setOff"
        # }
        #
        elif order['cmd'].lower() == "setoff":
            self.mode = config.MODE_OFF
            self.stop_video()
            return_val = {'status': 'OK',
                          'cmd': 'setOff'}
            return return_val
        #
        # set on
        # Format: {
        #   "cmd" : "setOn"
        # }
        #
        elif order['cmd'].lower() == "seton":
            self.mode = config.MODE_ON
            self.play_new()
            return_val = {'status': 'OK',
                          'cmd': 'setOn'}
            return return_val
        #
        # set auto
        # Format: {
        #   "cmd" : "setAuto"
        # }
        #
        elif order['cmd'].lower() == "setauto":
            self.mode = config.MODE_AUTO
            self.play_new()
            return_val = {'status': 'OK',
                          'cmd': 'setAuto'}
            return return_val
        #
        # set glitch mode
        # Format: {
        #   "cmd" : "setGlitch"
        # }
        #
        elif order['cmd'].lower() == "setglitch":
            if self.mode != config.MODE_AUTO:
                error = "setGlitch ignored when not in AUTO mode. Use setAuto command."
                logging.warning(error)
                return_val = {'status': 'FAIL',
                              'cmd': 'setGlitch',
                              'error': error}
                return return_val
            return_val = self.set_year('glitch')
            return return_val
        #
        # set year
        # Format: {
        #   "cmd" : "setYear",
        #   "year" : *year*
        # }
        #
        elif order['cmd'].lower() == "setyear":
            if "year" not in order:
                error = "No year in order received"
                logging.warning(error)
                return_val = {'status': 'FAIL',
                              'cmd': 'setYear',
                              'error': error}
                return return_val
            return_val = self.set_year(order['year'])
            return return_val
        #
        # help
        #
        elif order['cmd'].lower() == "help":
            cmds = [
                {'cmd': 'setOff'},
                {'cmd': 'setOn'},
                {'cmd': 'setAuto'},
                {'cmd': 'setGlitch'},
                {'cmd': 'setYear',
                 'year': ['1858', '1888', '1938', '1959', '1982', '2014', '2066', '2110']},
                {'cmd': 'reqStatus'},
                {'cmd': 'reqLog',
                 'qty': '10'}
            ]
            return_val = {'status': 'OK',
                          'cmd': 'help',
                          'commands': cmds}
            return return_val
        #
        # invalid order
        #
        else:
            error = f"invalid order received"
            logging.warning(error + ': ' + order['cmd'])
            return_val = {'status': 'FAIL',
                          'cmd': order['cmd'],
                          'error': error}
            return return_val

    """
        PLAY STUFF
    """

    def set_year(self, year):
        """Set year attribute."""
        logging.info(f"Setting year: {year}")
        print(f"Setting year: {year}")
        if str(year) not in config.VALID_YEARS:
            error = f"Invalid year: {year}"
            logging.warning(error)
            return_val = {'status': 'FAIL',
                          'error': error}
            return return_val
        # set current year
        self.current_year = str(year)
        if self.mode != config.MODE_AUTO:
            error = "No action taken when not in AUTO mode. Use setAuto command."
            logging.warning(error)
            return_val = {'status': 'FAIL',
                          'cmd': 'setYear',
                          'error': error}
            return return_val
        self.stop_video()
        self.play_new()
        return_val = {'status': 'OK',
                      'cmd': 'setYear'}
        return return_val

    def play_new(self):
        """Play new video file."""
        full_path = f"{config.TV_VIDEO_DIR}{self.current_year}/"
        logging.info(f"Playing random selections in {full_path}")
        self.play_all_in(full_path)

    def play_all_in(self, path):
        """Spawn thead to play video."""
        args = config.TV_PLATFORM[self.system]["start"]
        args.append(path)
        self.video_thread = subprocess.Popen(args, shell=False)

    def stop_video(self):
        """Stop all currently playing video threads."""
        # args = config.TV_PLATFORM[self.system]["clear"]
        # subprocess.Popen(args, shell=False)
        try:
            results = requests.get(config.TV_CLEAR_URL, timeout=0.5)
        except:
            logging.warning(f"Failed to connect with vlc to clear playlist")
        # args = args.insert(0, "/bin/echo")
        # subprocess.Popen(args, shell=False)
        time.sleep(0.5)
        if self.video_thread:
            self.video_thread.kill()
        else:
            args = config.TV_PLATFORM[self.system]["stop"]
            self.video_thread = subprocess.Popen(args, shell=False)


    """
        MAIN LOOP
    """

    def main_loop(self):
        """Get orders and acts on them."""
        while True:
            self.act_on_order(self.receive_order())
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
