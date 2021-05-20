"""Controller class for lights subsystem."""

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
GPIO_OFF = 1
GPIO_ON = 0

logger = logging.getLogger()

TODO: full_report should report state (as should status)

class Lights(Controller):
    """Lights controller class."""

    def __init__(self):
        super().__init__()
        self.whoami = "Lights"
        self.enabled = True
        self.glitch_state = config.OFF
        self.current_year = str(config.SCHED_YEARS[0])
        print(f"Current year: {self.current_year}")
        self.init_lights()
        self.set_lights_for_year()

    """
        SETUP
    """

    def init_lights(self):
        GPIO.setmode(config.LIGHTS_PINOUT_SCHEME)
        for light in range(config.LIGHTS_TOTAL):
            GPIO.setup(config.LIGHTS_PIN_TABLE[light], GPIO.OUT)


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
        elif order.startswith("set off"):
            self.enabled = False
        #
        # request on
        #
        elif order.startswith("set on"):
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
        CHECKS
    """

    def check_for_glitch(self):
        """
        Glitch randomly blinks all the lights on and off, by randomly calculating the chances of changing light state in this moment
        """
        if self.current_year != "glitch":
            return
        denominator = config.LIGHTS_GLITCH_LENGTH * (1/config.LIGHTS_LOOP_DELAY)
        # an N in 8 chance
        if random.random() < 1/denominator:
            # lucky you! you get chosen!
            self.glitch_state_change()

    """
        PLAY STUFF
    """

    def set_glitch(self):
        logging.info("Setting glitch")
        print("Setting glitch")
        self.current_year = "glitch"

    def set_year(self, year):
        logging.info(f"Setting year: {year}")
        print(f"Setting year: {year}")
        self.current_year = str(year)
        self.set_lights_for_year()

    """
        LIGHTS
    """

    def onoff(self, value):
        return ("on" if value else "off")

    def set_lights_for_year(self):
        logging.info(f"Setting lights for {self.current_year}: ({config.LIGHTS_TABLE[self.current_year]})")
        print(f"Setting lights for {self.current_year}: ({config.LIGHTS_TABLE[self.current_year]})")
        light_config_this_year = config.LIGHTS_TABLE[self.current_year]
        if self.current_year != "glitch":
            # iterate over light_config
            for light in light_config_this_year:
                self.switch_light_to(light, light_config_this_year[light])

    def glitch_state_change(self):
        # if current state is on, make it off, otherwise make it on
        if self.glitch_state == config.ON:
            self.glitch_state = config.OFF
        else:
            self.glitch_state = config.ON
        print(f"Glitch: {self.onoff(self.glitch_state)}")
        self.switch_all_lights_to(self.glitch_state)

    def switch_all_lights_to(self, status):
        logging.info(f"Switching all lights to {self.onoff(status)}")
        print(f"Switching all lights to {self.onoff(status)}")
        if status == config.ON:
            pin_status = GPIO_ON
        elif status == config.OFF:
            pin_status = GPIO_OFF
        try:
            for light in range(config.LIGHTS_TOTAL):
                GPIO.output(config.LIGHTS_PIN_TABLE[light], pin_status)
        except:
            logging.warning("Failed to switch all lights (GPIO) to {self.onoff(status)}")


    def switch_light_to(self, light, status):
        logging.info(f"Switching light {light} to {self.onoff(status)}")
        print(f"Switching light {light} to {self.onoff(status)}")
        if status == config.ON:
            pin_status = GPIO_ON
        elif status == config.OFF:
            pin_status = GPIO_OFF
        try:
            GPIO.output(config.LIGHTS_PIN_TABLE[light], pin_status)
        except:
            logging.warning(f"Failed to switch light (GPIO): light {light} to {self.onoff(status)}")

    """
        MAIN LOOP
    """

    def main_loop(self):
        """
        Gets orders and acts on them
        """
        while True:
            self.__act_on_order(self.receive_order())
            self.check_for_glitch()
            time.sleep(config.LIGHTS_LOOP_DELAY)


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
    lights = Lights()
    lights.order_act_loop()


if __name__ == '__main__':
    main()
