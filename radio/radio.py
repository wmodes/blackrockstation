"""Controller class for radio subsystem."""

from shared import config
from shared.controller import Controller

import logging
import pygame
import time
import os
import glob
import random

logger = logging.getLogger()

class Radio(Controller):
    """Radio controller class."""

    def __init__(self):
        """Initialize."""
        super().__init__()
        self.whoami = "radio"
        self.mode = config.MODE_AUTO
        self.filetable = self.__read_files()
        self.current_year = config.SCHED_YEARS[0]
        self.most_recent = ""
        # used by audio mixer
        pygame.mixer.init()
        pygame.mixer.music.set_volume(float(config.RADIO_VOLUME))
        #pprint(self.filetable)

    """
        SETUP
    """

    def __read_files(self):
        """
        Find data files.

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
        data_subdirs = next(os.walk(config.RADIO_AUDIO_DIR))[1]
        # find all the files in each subdir
        #pat = re.compile(config.RADIO_AUDIO_REGEX)
        for subdir in data_subdirs:
            full_subdir = config.RADIO_AUDIO_DIR + subdir + '/'
            filelist = glob.glob(full_subdir + '*' + config.RADIO_AUDIO_EXT)
            #file_dict[subdir] = [ s for s in filelist if pat.match(s) ]
            file_dict[subdir] = filelist
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
            return(str(return_val))
        if "cmd" not in order:
            error = f"No 'cmd' in order received: '{order}'"
            logging.info(error)
            return_val = {'status': 'FAIL',
                          'error': error}
            return(str(return_val))
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
            return(str(return_val))
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
            return(str(return_val))
        #
        # set off
        # Format: {
        #   "cmd" : "setOff"
        # }
        #
        elif order['cmd'].lower() == "setoff":
            self.mode = config.MODE_OFF
            self.stop_audio()
            return_val = {'status': 'OK',
                          'cmd': 'setOff'}
            return(str(return_val))
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
            return(str(return_val))
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
            return(str(return_val))
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
                return(str(return_val))
            self.set_glitch()
            return_val = {'status': 'OK',
                          'cmd': 'setGlitch'}
            return(str(return_val))
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
                return(str(return_val))
            results = self.set_year(order['year'])
            return(str(results))
        #
        # invalid order
        #
        else:
            error = f"invalid order received"
            logging.warning(error + ': ' + order['cmd'])
            return_val = {'status': 'FAIL',
                          'cmd': order['cmd'],
                          'error': error}
            return(str(return_val))

    """
        CHECKS
    """

    def check_for_new_audio(self):
        """Check if it is time for new audio."""
        if not pygame.mixer.music.get_busy():
            self.play_new()

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
            return_val = {'status':'FAIL',
                          'error':'invalid year'}
            return(return_val)
        self.current_year = str(year)
        if self.mode != config.MODE_AUTO:
            error = "setYear no action taken when not in AUTO mode. Use setAuto command."
            logging.warning(error)
            return_val = {'status': 'FAIL',
                          'cmd': 'setYear',
                          'error': error}
        self.play_new()
        return_val = {'status': 'OK',
                      'cmd': 'setYear'}
        return(return_val)

    def play_new(self):
        """Play new audio file."""
        # print(f"choices: {self.filetable[str(self.current_year)]}")
        filename = random.choice(self.filetable[str(self.current_year)])
        self.most_recent = filename
        logging.info(f"Playing audio: {filename}")
        print(f"Playing audio: {filename}")
        # used by audio mixer
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

    def stop_audio(self):
        """Stop all audio output."""
        logging.info("Stopping audio")
        print("Stopping audio")
        # used by audio mixer
        pygame.mixer.music.pause()



    """
        MAIN LOOP
    """

    def main_loop(self):
        """Get orders and acts on them."""
        while True:
            self.act_on_order(self.receive_order())
            if self.mode != config.MODE_OFF:
                self.check_for_new_audio()
            time.sleep(config.RADIO_LOOP_DELAY)


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
    radio = Radio()
    radio.order_act_loop()


if __name__ == '__main__':
    main()
