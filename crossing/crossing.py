"""Controller class for crossing subsystem."""

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
OFF = 0
ON = 1
GPIO_OFF = 1
GPIO_ON = 0

logger = logging.getLogger()

TODO: full_report should report state (as should status)

class Crossing(Controller):
    """Crossing controller class."""

    def __init__(self):
        super().__init__()
        self.whoami = "Crossing"
        self.status = OFF
        print(f"Current state: {self.onoff(self.status)}")
        self.init_crossing()
        self.set_crossing()

    """
        SETUP
    """

    def init_crossing(self):
        GPIO.setmode(config.CROSS_PINOUT_SCHEME)
        GPIO.setup(config.CROSS_PIN, GPIO.OUT)

    """
        ORDERS
    """

    def __act_on_order(self, order):
        """
        Takes action based on order.

        Possible comnmands:
            - set on
            - set off
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
            self.set_off()
        #
        # set on
        #
        elif order.startswith("set on"):
            self.set_on()
        #
        # invalid order
        #
        else:
            logging.info(f"invalid order received: {order}")

    """
        ACTIONS
    """

    def set_off(self):
        logging.info("Setting off")
        print("Setting off")
        self.status = OFF
        self.set_crossing()

    def set_on(self):
        logging.info("Setting on")
        print("Setting on")
        self.status = ON
        self.set_crossing()

    """
        CROSSING
    """

    def onoff(self, value):
        return ("on" if value == ON else "off")

    def set_crossing(self):
        logging.info(f"Setting crossing: {self.onoff(self.status)}")
        print(f"Setting crossing: {self.onoff(self.status)}")
        if self.status == ON:
            GPIO.output(config.CROSS_PIN, GPIO_ON)
        else:
            GPIO.output(config.CROSS_PIN, GPIO_OFF)

    """
        MAIN LOOP
    """

    def main_loop(self):
        """
        Gets orders and acts on them
        """
        while True:
            self.__act_on_order(self.receive_order())
            time.sleep(config.CROSS_LOOP_DELAY)


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
    crossing = Crossing()
    crossing.order_act_loop()


if __name__ == '__main__':
    main()
