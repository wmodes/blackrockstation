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

# Start
CONTROLLERS = [
    "announce", "crossing", "lights", "radio", "scheduler", "signal",
    "trainaudio", "television"
]

# Controller parent class

# Scheduler class
SCHED_DATA = "scheduler/data/schedule.csv"
SCHED_FIELDS = ['event', 'controller', 'time', 'duration', 'direction', 'traintype', 'variance', 'notes', 'announceid']
SCHED_LOOP_DELAY = 0.25
SCHED_DEFAULT_LOG = 100
SCHED_YEARS = [1858, 1888, 1938, 1959, 1982, 2014, 2066, 2110]
SCHED_TIMESLIP_INTERVAL = 26     # time in minutes
SCHED_TIMESLIP_DELTA = 0.25     # time in minutes
SCHED_TIMESLIP_GLITCH = 0.5       # time in minutes
SCHED_PERIODIC = [
    {"controller": "announce", "announceid": "periodic-paging-announcement-1", "times_per_day": 3},
    {"controller": "announce", "announceid": "periodic-paging-announcement-2", "times_per_day": 3},
    {"controller": "announce", "announceid": "periodic-safety-announcement", "times_per_day": 8},
]
SCHED_DEPART_TIME = 1.5   # time in minutes

# Announce class

# Crossing class

# Lights class

# Signal class

# Trainaudio class
TRAIN_FILE_TABLE = "scheduler/data/file-table.csv"
TRAIN_TYPES = ["freight-through", "freight-stop", "passenger-through", "passenger-stop"]
TRAIN_FILE_FIELDS = ['year', 'type', 'filename']
TRAIN_AUDIO_DIR = "scheduler/audio/"

# Radio class

# TV class
