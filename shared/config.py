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
ORDER_FILE = ".order"   # temp solution for comms orders

# Start
CONTROLLERS = [
    "announce", "crossing", "lights", "radio", "scheduler", "signal",
    "train", "television"
]

# Controller parent class

# Scheduler class
SCHED_DATA = "scheduler/data/schedule.csv"
SCHED_FIELDS = ['event', 'controller', 'time', 'duration', 'direction', 'traintype', 'variance', 'notes', 'announceid']
SCHED_LOOP_DELAY = 0.25
SCHED_DEFAULT_LOG = 100
SCHED_YEARS = [1858, 1888, 1938, 1959, 1982, 2014, 2066, 2110]
SCHED_TIMESLIP_INTERVAL = 26        # time in minutes
SCHED_TIME_DELTA = 0.24999          # time in minutes
SCHED_TIMESLIP_GLITCH = 0.5         # time in minutes
SCHED_PERIODIC = [
    {"controller": "announce", "announceid": "periodic-paging-announcement-1", "times_per_day": 3},
    {"controller": "announce", "announceid": "periodic-paging-announcement-2", "times_per_day": 3},
    {"controller": "announce", "announceid": "periodic-safety-announcement", "times_per_day": 8},
]
SCHED_DEPART_TIME = 1.5      # time in minutes
SCHED_SIGNAL_BEFORE = 3       # time in minutes
SCHED_CROSSING_DELAY = 1     # time in minutes

# Announce class
ANNOUNCE_FILE_TABLE = "announce/data/file-table.csv"
ANNOUNCE_FILE_FIELDS = ['announcement', 'announceid', 'year', 'filename', 'notes']
ANNOUNCE_AUDIO_DIR = "announce/data/"
ANNOUNCE_LOOP_DELAY = 0.25
ANNOUNCE_AUDIO_EXT = ".mp3"
ANNOUNCE_VOLUME = "0.8"

# Crossing class

# Lights class

# Signal class

# Train class
TRAIN_FILE_TABLE = "train/data/file-table.csv"
TRAIN_FILE_FIELDS = ['year', 'type', 'filename']
TRAIN_TYPES = ["freight-through", "freight-stop", "passenger-through", "passenger-stop"]
TRAIN_AUDIO_DIR = "train/data/"
TRAIN_LOOP_DELAY = 0.25
TRAIN_AUDIO_EXT = ".mp3"
TRAIN_VOLUME = "0.9"

# Radio class

# TV class
