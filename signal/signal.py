"""Controller class for signal subsystem."""

from shared import config
from shared.controller import Controller

import logging
import time
import RPi.GPIO as GPIO


logger = logging.getLogger()

class Signal(Controller):
    """Signal controller class."""

    def __init__(self):
        """Initialize."""
        super().__init__()
        self.whoami = "Signal"
        self.eastbound = config.STATE_STOP
        self.westbound = config.STATE_STOP
        print(f"Current state: Westbound is {self.stopgo(self.westbound)}, Eastbound is {self.stopgo(self.eastbound)}")
        self.init_signals()
        self.set_signals()

    """
        SETUP
    """

    def init_signals(self):
        """Initialize signal GPIO."""
        GPIO.setmode(config.SIGNAL_PINOUT_SCHEME)
        for signal_pin in range(len(config.SIGNAL_PIN_TABLE)):
            GPIO.setup(signal_pin, GPIO.OUT)

    """
        REPORTS
    """

    def get_status(self):
        """Full status for controller."""
        return {
            "running" : True,
            "state" : {
                "eastbound" : self.stopgo(self.eastbound),
                "westbound" : self.stopgo(self.westbound)
            }
        }

    """
        ORDERS
    """

    def __act_on_order(self, order):
        """
        Take action based on order.

        Possible comnmands:
            - setGo *direction*
            - setStop
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
        # set stop
        # Format: {
        #   "cmd" : "setStop"
        # }
        #
        elif order['cmd'].lower() == "setstop":
            self.set_stop()
        #
        # set go
        # Format: {
        #   "cmd" : "setGo"
        #   "direction" : **string**
        # }
        #
        elif order['cmd'].lower() == "setgo":
            if "direction" not in order:
                logging.warning(f"invalid order received: {order}")
                return
            self.set_go(order['direction'])
        #
        # invalid order
        #
        else:
            logging.warning(f"invalid order received: {order}")


    """
        PLAY STUFF
    """

    def set_stop(self):
        """Set signals to stio for all directions."""
        logging.info("Setting stop")
        print("Setting stop")
        self.eastbound = config.STATE_STOP
        self.westbound = config.STATE_STOP
        self.set_signals()

    def set_go(self, direction):
        """Set signals to go for given direction."""
        logging.info(f"Setting go {direction}")
        print(f"Setting go {direction}")
        if direction.lower().startswith("e"):
             self.eastbound = config.STATE_GO
             self.westbound = config.STATE_STOP
        elif direction.startswith("w"):
             self.westbound = config.STATE_GO
             self.eastbound = config.STATE_STOP
        self.set_signals()

    """
        SIGNAL
    """

    def set_signals(self):
        """Set signals based on current status."""
        logging.info(f"Setting signal: Westbound is {self.stopgo(self.westbound)}, Eastbound is {self.stopgo(self.eastbound)}")
        print(f"Setting signal: Westbound is {self.stopgo(self.westbound)}, Eastbound is {self.stopgo(self.eastbound)}")
        if self.westbound == config.STATE_GO:
            GPIO.output(config.SIGNAL_PIN_TABLE[config.SIGNAL_WB_STOP], config.GPIO_OFF)
            GPIO.output(config.SIGNAL_PIN_TABLE[config.SIGNAL_WB_GO], config.GPIO_ON)
        else:
            GPIO.output(config.SIGNAL_PIN_TABLE[config.SIGNAL_WB_STOP], config.GPIO_ON)
            GPIO.output(config.SIGNAL_PIN_TABLE[config.SIGNAL_WB_GO], config.GPIO_OFF)
        if self.eastbound == config.STATE_GO:
            GPIO.output(config.SIGNAL_PIN_TABLE[config.SIGNAL_EB_STOP], config.GPIO_OFF)
            GPIO.output(config.SIGNAL_PIN_TABLE[config.SIGNAL_EB_GO], config.GPIO_ON)
        else:
            GPIO.output(config.SIGNAL_PIN_TABLE[config.SIGNAL_EB_STOP], config.GPIO_ON)
            GPIO.output(config.SIGNAL_PIN_TABLE[config.SIGNAL_EB_GO], config.GPIO_OFF)

    """
        MAIN LOOP
    """

    def main_loop(self):
        """Get orders and acts on them."""
        while True:
            self.__act_on_order(self.receive_order())
            time.sleep(config.SIGNAL_LOOP_DELAY)


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
    signal = Signal()
    signal.order_act_loop()


if __name__ == '__main__':
    main()
