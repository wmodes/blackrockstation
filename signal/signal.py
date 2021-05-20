"""Controller class for signal subsystem."""

from shared import config
from shared.controller import Controller

import logging
from pprint import pprint
from datetime import datetime, timedelta
import csv
import time
import os
import glob
import random
import re
import RPi.GPIO as GPIO

# CONSTANTS
STOP = 0
GO = 1
GPIO_OFF = 1
GPIO_ON = 0

logger = logging.getLogger()

TODO: full_report should report state (as should status)

class Signal(Controller):
    """Signal controller class."""

    def __init__(self):
        super().__init__()
        self.whoami = "Signal"
        self.eastbound = STOP
        self.westbound = STOP
        print(f"Current state: Westbound is {self.stopgo(self.westbound)}, Eastbound is {self.stopgo(self.eastbound)}")
        self.init_signals()
        self.set_signals()

    """
        SETUP
    """

    def init_signals(self):
        GPIO.setmode(config.SIGNAL_PINOUT_SCHEME)
        for signal_pin in range(len(config.SIGNAL_PIN_TABLE)):
            GPIO.setup(signal_pin, GPIO.OUT)

    """
        ORDERS
    """

    def __act_on_order(self, order):
        """
        Takes action based on order.

        Possible comnmands:
            - set go *direction*
            - set stop
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
        # set glitch
        #
        elif order.startswith("set stop"):
            self.set_stop()
        #
        # set year
        #
        elif order.startswith("set go"):
            order_list = order.split()
            direction = order_list[2]
            self.set_go(direction)
        #
        # invalid order
        #
        else:
            logging.info(f"invalid order received: {order}")

    """
        PLAY STUFF
    """

    def set_stop(self):
        logging.info("Setting stop")
        print("Setting stop")
        self.eastbound = STOP
        self.westbound = STOP
        self.set_signals()

    def set_go(self, direction):
        logging.info(f"Setting go {direction}")
        print(f"Setting go {direction}")
        if direction.startswith("e"):
             self.eastbound = GO
             self.westbound = STOP
        elif direction.startswith("w"):
             self.westbound = GO
             self.eastbound = STOP
        self.set_signals()

    """
        SIGNAL
    """

    def stopgo(self, value):
        return ("go" if value == GO else "stop")

    def set_signals(self):
        logging.info(f"Setting signal: Westbound is {self.stopgo(self.westbound)}, Eastbound is {self.stopgo(self.eastbound)}")
        print(f"Setting signal: Westbound is {self.stopgo(self.westbound)}, Eastbound is {self.stopgo(self.eastbound)}")
        if self.westbound == GO:
            GPIO.output(config.SIGNAL_PIN_TABLE[config.SIGNAL_WB_STOP], GPIO_OFF)
            GPIO.output(config.SIGNAL_PIN_TABLE[config.SIGNAL_WB_GO], GPIO_ON)
        else:
            GPIO.output(config.SIGNAL_PIN_TABLE[config.SIGNAL_WB_STOP], GPIO_ON)
            GPIO.output(config.SIGNAL_PIN_TABLE[config.SIGNAL_WB_GO], GPIO_OFF)
        if self.eastbound == GO:
            GPIO.output(config.SIGNAL_PIN_TABLE[config.SIGNAL_EB_STOP], GPIO_OFF)
            GPIO.output(config.SIGNAL_PIN_TABLE[config.SIGNAL_EB_GO], GPIO_ON)
        else:
            GPIO.output(config.SIGNAL_PIN_TABLE[config.SIGNAL_EB_STOP], GPIO_ON)
            GPIO.output(config.SIGNAL_PIN_TABLE[config.SIGNAL_EB_GO], GPIO_OFF)

    """
        MAIN LOOP
    """

    def main_loop(self):
        """
        Gets orders and acts on them
        """
        while True:
            self.__act_on_order(self.receive_order())
            time.sleep(config.SIGNAL_LOOP_DELAY)


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
    signal = Signal()
    signal.order_act_loop()


if __name__ == '__main__':
    main()
