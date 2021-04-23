# config.py - settings for all controllers
# author: Wes Modes <wmodes@gmail.com>
# date: Apr 2021
# license: MIT

import os, sys
from dotenv import load_dotenv
load_dotenv()
if sys.platform == "darwin":
    # OS X
    import fake_rpi
    sys.modules['RPi'] = fake_rpi.RPi     # Fake RPi
    sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO # Fake GPIO
    # sys.modules['smbus'] = fake_rpi.smbus # Fake smbus (I2C)
import RPi.GPIO as GPIO
import logging

# Controller parent class
LOG_FILENAME = "logs/cr.log"
LOG_LEVEL = logging.INFO

# Scheduler class


# Announce class


# Crossing class


# Lights class


# Signal class


# Trainaudio class


# Radio class


# TV class
