"""Controller class for crossing subsystem."""

from shared import config
from shared.controller import Controller

import logging
import time
import RPi.GPIO as GPIO


logger = logging.getLogger()

class Crossing(Controller):
    """Crossing controller class."""

    def __init__(self):
        """Initialize."""
        super().__init__()
        self.whoami = "Crossing"
        self.status = config.STATE_OFF
        self.init_crossing()
        self.set_crossing()

    """
        SETUP
    """

    def init_crossing(self):
        """Initialize GPIO."""
        GPIO.setmode(config.CROSS_PINOUT_SCHEME)
        GPIO.setup(config.CROSS_PIN, GPIO.OUT)

    """
        REPORTS
    """

    def get_status(self):
        """Full status for controller."""
        return {
            "running" : True,
            "state" : self.onoff(self.status)
        }

    """
        ORDERS
    """

    def __act_on_order(self, order):
        """Take action based on order.

        Possible comnmands:
            - setOn
            - setOff
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
            self.set_off()
        #
        # set on
        # Format: {
        #   "cmd" : "setOn"
        # }
        #
        elif order['cmd'].lower() == "seton":
            self.mode = config.MODE_ON
            self.set_on()
        #
        # invalid order
        #
        else:
            logging.warning(f"invalid order received: {order}")

    """
        ACTIONS
    """

    def set_off(self):
        """Set status off."""
        logging.info("Setting off")
        print("Setting off")
        self.status = config.STATE_OFF
        self.set_crossing()

    def set_on(self):
        """Set status ob."""
        logging.info("Setting on")
        print("Setting on")
        self.status = config.STATE_ON
        self.set_crossing()

    """
        CROSSING
    """

    def set_crossing(self):
        """Set crossing based on status."""
        logging.info(f"Setting crossing: {self.onoff(self.status)}")
        print(f"Setting crossing: {self.onoff(self.status)}")
        if self.status == config.STATE_ON:
            GPIO.output(config.CROSS_PIN, config.GPIO_ON)
        else:
            GPIO.output(config.CROSS_PIN, config.GPIO_OFF)

    """
        MAIN LOOP
    """

    def main_loop(self):
        """Get orders and act on them."""
        while True:
            self.__act_on_order(self.receive_order())
            time.sleep(config.CROSS_LOOP_DELAY)


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
    crossing = Crossing()
    crossing.order_act_loop()


if __name__ == '__main__':
    main()
