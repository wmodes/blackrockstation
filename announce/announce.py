"""Controller class for announcement subsystem."""

from shared import config
from shared.controller import Controller

import logging
from pygame import mixer
import csv
import time
import glob
import random

logger = logging.getLogger()


class Announce(Controller):
    """Announcements controller class."""

    def __init__(self):
        """Initialize."""
        super().__init__()
        self.whoami = "announce"
        self.mode = config.MODE_AUTO
        self.glitchtable = self.__read_files()
        self.filetable = self.__read_filetable()
        self.most_recent = ""
        mixer.init()
        mixer.music.set_volume(float(config.ANNOUNCE_VOLUME))

    """
        SETUP
    """

    def __read_filetable(self):
        """Read file with list of possible announcements."""
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

    def __read_files(self):
        """
        Find data files.

        Look for audio files in data directory and construct array of possibilities.
            ["glitch-file1.mp4", "glitch-file2.mp4"]
        Note that if you add files, you will have to restart the controller.
        """
        # create a list of file
        full_subdir = config.ANNOUNCE_GLITCH_DIR
        file_list = glob.glob(full_subdir + '*' + config.ANNOUNCE_AUDIO_EXT)
        return file_list

    """
        REPORTS
    """

    def get_status(self):
        """Full status for controller."""
        return {
            "controller" : self.whoami,
            "running" : True,
            "mode" : self.mode2str(self.mode),
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
            - setAnnounce *id* *year*
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
        logging.info(f"Acting on order: {order}")
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
        # set announce
        # Format: {
        #   "cmd" : "setAnnounce",
        #   "announceid" : *string*,
        #   "year" : *year*
        # }
        elif order['cmd'].lower() == "setannounce":
            if "announceid" not in order or "year" not in order:
                error = f"invalid order received: {order}"
                logging.warning(error)
                return_val = {'status': 'FAIL',
                              'cmd': 'setGlitch',
                              'error': error}
                return(str(return_val))
            results = self.set_announce(order['announceid'], order['year'])
            return(str(results))
        #
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
        PLAY STUFF
    """

    def set_glitch(self):
        """Play glitch audio."""
        logging.info("Setting glitch")
        print("Setting glitch")
        if self.mode != config.MODE_AUTO:
            logging.warning("setGlitch no action taken when not in AUTO mode. Use setAuto command.")
            return
        filename = random.choice(self.glitchtable)
        self.most_recent = filename
        logging.info(f"Playing audio: {filename}")
        print(f"Playing audio: {filename}")
        # used by audio mixer
        mixer.music.load(filename)
        mixer.music.play()

    def set_announce(self, announceid, year):
        """Play announcement."""
        if str(year) not in config.VALID_YEARS:
            error = f"Invalid year: {year}"
            logging.warning(error + ': ' + order['cmd'])
            return_val = {'status': 'FAIL',
                          'cmd': 'setAnnounce',
                          'error': error}
            return(str(return_val))
        if self.mode == config.MODE_OFF:
            error = "No action taken when not in ON or AUTO modes. Use setAuto command."
            logging.warning(error + ': ' + order['cmd'])
            return_val = {'status': 'FAIL',
                          'cmd': 'setAnnounce',
                          'error': error}
            return(str(return_val))
        filepath = config.ANNOUNCE_AUDIO_DIR
        filename = f"{str(year)}-{announceid}{config.ANNOUNCE_AUDIO_EXT}"
        self.most_recent = filepath + filename
        logging.info(f"Playing audio: {filepath}{filename}")
        mixer.music.load(filepath + filename)
        mixer.music.play()
        return_val = {'status': 'OK',
                      'cmd': 'setAnnounce',
                      'file': filepath + filename}
        return(return_val)

    def stop_audio(self):
        """Stop all audio output."""
        logging.info("Stopping audio")
        print("Stopping audio")
        # used by audio mixer
        mixer.music.pause()

    """
        MAIN LOOP
    """

    def main_loop(self):
        """Get orders and act on them."""
        while True:
            self.act_on_order(self.receive_order())
            time.sleep(config.ANNOUNCE_LOOP_DELAY)


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
    announce = Announce()
    announce.order_act_loop()


if __name__ == '__main__':
    main()
