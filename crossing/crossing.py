"""Controller class for crossing subsystem."""

from shared import config
from shared.controller import Controller

import logging
import time
import RPi.GPIO as GPIO


logger = logging.getLogger()
logger.setLevel(config.LOG_LEVEL)

class Crossing(Controller):
    """Crossing controller class."""

    def __init__(self):
        """Initialize."""
        super().__init__()
        self.whoami = "crossing"
        self.status = config.STATE_OFF
        self.mode = config.MODE_AUTO
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
            "controller" : self.whoami,
            "running" : True,
            "mode" : self.mode2str(self.mode),
            "state" : self.onoff(self.status)
        }

    """
        ORDERS
    """

    def act_on_order(self, order):
        """Take action based on order.

        Possible comnmands:
            - setOn
            - setOff
            - setAuto
            - stateOn
            - stateOff
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
            self.status = config.STATE_OFF
            self.set_crossing()
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
            self.status = config.STATE_ON
            self.set_crossing()
            return_val = {'status': 'OK',
                          'cmd': 'setOn'}
            return return_val
        #
        # set on
        # Format: {
        #   "cmd" : "setAuto"
        # }
        #
        elif order['cmd'].lower() == "setauto":
            self.mode = config.MODE_AUTO
            self.status = config.STATE_OFF
            self.set_crossing()
            return_val = {'status': 'OK',
                          'cmd': 'setOn'}
            return return_val
        #
        # state off
        # Format: {
        #   "cmd" : "stateOff"
        # }
        #
        elif order['cmd'].lower() == "stateoff":
            if self.mode != config.MODE_AUTO:
                error = "stateOff ignored when not in AUTO mode. Use setAuto command."
                logging.warning(error)
                return_val = {'status': 'FAIL',
                              'cmd': 'stateOff',
                              'error': error}
                return return_val
            self.status = config.STATE_OFF
            self.set_crossing()
            return_val = {'status': 'OK',
                          'cmd': 'stateOff'}
            return return_val
        #
        # state on
        # Format: {
        #   "cmd" : "stateOn"
        # }
        #
        elif order['cmd'].lower() == "stateon":
            if self.mode != config.MODE_AUTO:
                error = "stateOn ignored when not in AUTO mode. Use setAuto command."
                logging.warning(error)
                return_val = {'status': 'FAIL',
                              'cmd': 'stateOn',
                              'error': error}
                return return_val
            self.status = config.STATE_ON
            self.set_crossing()
            return_val = {'status': 'OK',
                          'cmd': 'stateOn'}
            return return_val
        #
        # help
        #
        elif order['cmd'].lower() == "help":
            cmds = [
                {'cmd': 'setOff'},
                {'cmd': 'setOn'},
                {'cmd': 'setAuto'},
                {'cmd': 'stateOff'},
                {'cmd': 'stateOn'},
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
        CROSSING
    """

    def set_crossing(self):
        """Set crossing based on status."""
        logging.info(f"Setting crossing: {self.onoff(self.status)}")
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
            self.act_on_order(self.receive_order())
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
