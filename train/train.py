"""Controller class for train subsystem."""

from shared import config
from shared.controller import Controller

import logging
from pygame import mixer
import csv
import time
import sox
from pathlib import Path

logger = logging.getLogger()


class Train(Controller):
    """Train controller class."""

    def __init__(self):
        """Initialize."""
        super().__init__()
        self.whoami = "train"
        self.mode = config.MODE_AUTO
        self.enabled = True
        self.filetable = self.__read_filetable()
        self.most_recent = ""
        mixer.init()
        mixer.music.set_volume(float(config.TRAIN_VOLUME))

    """
        SETUP
    """

    def __read_filetable(self):
        """Read filetable into memory."""
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
        #pprint(filetable)
        return filetable

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

    def __act_on_order(self, order):
        """Take action based on order.

        Possible commands:
            - setOff
            - setOn
            - setTrain *direction* *type* *year*
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
        #
        # set on
        # Format: {
        #   "cmd" : "setOn"
        # }
        #
        elif order['cmd'].lower() == "seton":
            self.mode = config.MODE_ON
        #
        # set auto
        # Format: {
        #   "cmd" : "setAuto"
        # }
        #
        elif order['cmd'].lower() == "setauto":
            self.mode = config.MODE_AUTO
        #
        # set train
        # Format: {
        #   "cmd" : "setTrain",
        #   "direction" : *string*,
        #   "type" : *string*
        #   "year" : *year*
        # }
        elif order['cmd'].lower() == "settrain":
            if "direction" not in order or "type" not in order or "year" not in order:
                logging.warning(f"invalid order received: {order}")
                return
            self.set_train(order["direction"], order["type"], order["year"])
        #
        #
        # invalid order
        #
        else:
            logging.warning(f"invalid order received: {order}")

    """
        PLAY STUFF
    """

    def set_train(self, direction, type, year):
        """Play train audio.

        Filename is assembled from passed parameters.
        All train sounds are recorded/edited to move into field from left to right. This default serves as "eastbound." "Westbound" trains have their audio channels reversed.
        """
        logging.debug(f"Setting train: {direction} {type} {year}")
        if self.mode == config.MODE_OFF:
            logging.warning("No action taken when not in ON or AUTO modes. Use setAuto command.")
            return
        filepath = config.TRAIN_AUDIO_DIR
        filename = filepath + self.filetable[f"{year}-{type}"]
        logging.debug(f"Train audio filename: {filename}")
        # confirm file is there
        file = Path(filename)
        if not file.is_file():
            logging.warning(f"Train audio file not found: {filename}")
            return
        # by default, train recordings are recorded left-to-right or eastbound
        # if direction is westbound, swap the channels
        if direction == "westbound":
            # Note that the transform and rewrite takes at least 1/2 a second,
            #  but will probably be fine in this context
            # create transformer
            tfm = sox.Transformer()
            # swap channels
            tfm.swap()
            # create an tmp output file
            tfm.build_file(filename, config.TRAIN_TMP_FILE)
            logging.info("Swapping audio channels for westbound train")
            playfile = config.TRAIN_TMP_FILE
        # if direction is eastbound, we don't have to do anything
        else:
            playfile = filename
        self.most_recent = filename
        logging.info(f"Playing audio: {filename}")
        mixer.music.load(playfile)
        mixer.music.play()

    """
        MAIN LOOP
    """

    def main_loop(self):
        """Get orders and act on them."""
        while True:
            self.__act_on_order(self.receive_order())
            time.sleep(config.TRAIN_LOOP_DELAY)


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
    train = Train()
    train.order_act_loop()


if __name__ == '__main__':
    main()
