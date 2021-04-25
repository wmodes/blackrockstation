"""Settings for all controllers."""

import os, sys
if sys.platform == "darwin":
    # OS X
    import fake_rpi
    sys.modules['RPi'] = fake_rpi.RPi  # Fake RPi
    sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO  # Fake GPIO
    # sys.modules['smbus'] = fake_rpi.smbus # Fake smbus (I2C)
import RPi.GPIO as GPIO
import logging

# Shared config
PKG_ROOT = "blackrockstation"
LOG_FILENAME = "logs/controller.log"
LOG_LEVEL = logging.INFO

# Controller parent class

# Scheduler class

# Announce class

# Crossing class

# Lights class

# Signal class

# Trainaudio class

# Radio class

# TV class
