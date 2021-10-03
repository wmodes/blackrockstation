"""Controller class for lights subsystem."""

from shared import config
from shared.controller import Controller

import logging
import time
import random
import RPi.GPIO as GPIO

logger = logging.getLogger()

class Lights(Controller):
    """Lights controller class."""

    def __init__(self):
        """Initialize."""
        super().__init__()
        self.whoami = "lights"
        self.mode = config.MODE_AUTO
        self.light_model = []
        self.glitch_state = config.STATE_OFF
        self.current_year = str(config.SCHED_YEARS[0])
        print(f"Current year: {self.current_year}")
        self.init_lights()
        self.set_lights_for_year()

    """
        SETUP
    """

    def init_lights(self):
        """Initialize lighting system."""
        self.light_model = [config.STATE_OFF] * config.LIGHTS_TOTAL
        GPIO.setmode(config.LIGHTS_PINOUT_SCHEME)
        for light in range(config.LIGHTS_TOTAL):
            GPIO.setup(config.LIGHTS_PIN_TABLE[light], GPIO.OUT)

    """
        REPORTS
    """

    def get_status(self):
        """Full status for controller."""
        lights_status = []
        for light_num in range(config.LIGHTS_TOTAL):
            lights_status.append({
                "number" : light_num,
                "name" : config.LIGHT_NAME_TABLE[light_num],
                "state" : self.onoff(self.light_model[light_num])
            })
        return {
            "controller" : self.whoami,
            "running" : True,
            "mode" : self.mode2str(self.mode),
            "currentYear" : self.current_year,
            "lights" : lights_status
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
            self.switch_all_lights_to(config.STATE_OFF)
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
            self.switch_all_lights_to(config.STATE_ON)
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
            self.set_year(self.current_year)
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
            self.set_glitch()
            return_val = {'status': 'OK',
                          'cmd': 'setGlitch'}
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
        CHECKS
    """

    def check_for_glitch(self):
        """
        Glitch randomly blinks all the lights on and off.

        Randomly calculates the chances of changing light state in this moment
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
        """Set glitch mode by setting year attribute."""
        logging.info("Setting glitch")
        print("Setting glitch")
        self.current_year = "glitch"

    def set_year(self, year):
        """Set year attribute."""
        logging.info(f"Setting year: {year}")
        print(f"Setting year: {year}")
        if str(year) not in config.VALID_YEARS:
            logging.warning("Invalid year: {year}")
            return_val = {'status':'FAIL',
                          'error':'invalid year'}
            return return_val
        self.current_year = str(year)
        if self.mode != config.MODE_AUTO:
            error = "setYear no action taken when not in AUTO mode. Use setAuto command."
            logging.warning(error)
            return_val = {'status': 'FAIL',
                          'cmd': 'setYear',
                          'error': error}
            return(return_val)
        self.set_lights_for_year()
        return_val = {'status': 'OK',
                      'cmd': 'setYear'}
        return return_val

    """
        LIGHTS
    """

    def set_lights_for_year(self):
        """Set appropriate lights for current year."""
        light_config_for_year = config.LIGHTS_TABLE[self.current_year]
        logging.info(f"Setting lights for {self.current_year}: ({light_config_for_year})")
        print(f"Setting lights for {self.current_year}: ({light_config_for_year})")
        if self.current_year == "glitch":
            return
        # iterate over light_config
        for light_num in range(config.LIGHTS_TOTAL):
            self.switch_light_to(light_num, light_config_for_year[light_num])
            self.light_model[light_num] = light_config_for_year[light_num]

    def glitch_state_change(self):
        """Toggle glitch state."""
        # if current state is on, make it off, otherwise make it on
        if self.glitch_state == config.STATE_ON:
            self.glitch_state = config.STATE_OFF
        else:
            self.glitch_state = config.STATE_ON
        print(f"Glitch: {self.onoff(self.glitch_state)}")
        self.switch_all_lights_to(self.glitch_state)

    def switch_all_lights_to(self, status):
        """Set all lights to on/off."""
        logging.info(f"Switching all lights to {self.onoff(status)}")
        print(f"Switching all lights to {self.onoff(status)}")
        if status == config.STATE_ON:
            pin_status = config.GPIO_ON
        elif status == config.STATE_OFF:
            pin_status = config.GPIO_OFF
        try:
            for light in range(config.LIGHTS_TOTAL):
                GPIO.output(config.LIGHTS_PIN_TABLE[light], pin_status)
                self.light_model[light] = status
        except:
            logging.warning("Failed to switch all lights (GPIO) to {self.onoff(status)}")

    def switch_light_to(self, light, status):
        """
        Set a particular light to on/off.

        light (integer) specifies the light number
        """
        logging.info(f"Switching light {light} to {self.onoff(status)}")
        print(f"Switching light {light} to {self.onoff(status)}")
        if status == config.STATE_ON:
            pin_status = config.GPIO_ON
        elif status == config.STATE_OFF:
            pin_status = config.GPIO_OFF
        try:
            GPIO.output(config.LIGHTS_PIN_TABLE[light], pin_status)
            self.light_model[light] = status
        except:
            logging.warning(f"Failed to switch light (GPIO): light {light} to {self.onoff(status)}")

    """
        MAIN LOOP
    """

    def main_loop(self):
        """Get orders and act on them."""
        while True:
            self.act_on_order(self.receive_order())
            self.check_for_glitch()
            time.sleep(config.LIGHTS_LOOP_DELAY)


    def start(self):
        """Get the party started."""
        logging.info('Starting.')
        self.main_loop()


def main():
    """Test the class."""
    import sys
    logging.basicConfig(filename=sys.stderr,
                        encoding='utf-8',
                        format='%(asctime)s %(levelname)s:%(message)s',
                        level=logging.DEBUG)
    lights = Lights()
    lights.order_act_loop()


if __name__ == '__main__':
    main()
