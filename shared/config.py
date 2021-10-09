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
DEBUG = True
ID_FILE = ".identity"
PKG_ROOT = "blackrockstation"
LOG_FILENAME = "logs/controller.log"
LOG_LEVEL = logging.INFO
ORDER_FILE = ".order"   # temp solution for comms orders
STATE_OFF = 0
STATE_ON = 1
STATE_STOP = 0
STATE_GO = 1
GPIO_OFF = 1
GPIO_ON = 0
MODE_OFF = 0
MODE_ON = 1
MODE_AUTO = -1

# Start
CONTROLLERS = [
    "announce", "crossing", "lights", "radio", "scheduler", "bridge",
    "train", "television"
]

# Controller parent class
VALID_YEARS = ['glitch', '1858', '1888', '1938', '1959', '1982', '2014', '2066', '2110']

# Scheduler class
SCHED_SRV = "https://announce.local:8080"
SCHED_DATA = "scheduler/data/schedule.csv"
SCHED_FIELDS = ['event', 'controller', 'time', 'duration', 'direction', 'traintype', 'variance', 'notes', 'announceid', 'time_since_last']
SCHED_LOOP_DELAY = 0.25
SCHED_DEFAULT_LOG = 100
SCHED_YEARS = [1858, 1888, 1938, 1959, 1982, 2014, 2066, 2110]
SCHED_TIMESLIP_INTERVAL = 26        # time in minutes default=26
SCHED_TIMESLIP_GLITCH = 0.5         # time in minutes
SCHED_PERIODIC = [
    {"controller": "announce", "announceid": "periodic-paging-announcement-1", "times_per_day": 3},
    {"controller": "announce", "announceid": "periodic-paging-announcement-2", "times_per_day": 3},
    {"controller": "announce", "announceid": "periodic-safety-announcement", "times_per_day": 8},
]
SCHED_DEPART_TIME = 1.5      # time in minutes
SCHED_BRIDGE_BEFORE = 3       # time in minutes
SCHED_CROSSING_DELAY = 1     # time in minutes
SCHED_DISPLAY_TRAINS = 14
SCHED_DISPLAY_TIME_FREQ = 1      # approx seconds
SCHED_DISPLAY_SCHED_FREQ = 30      # approx seconds
SCHED_WIN_TIME_HEIGHT = 6
SCHED_WIN_STATUS_HEIGHT = 8
SCHED_TIME_FORMAT = "%b %d, %Y %H:%M:%S"

# Announce class
# ANNOUNCE_SRV = "https://announce.local:8080"
ANNOUNCE_SRV = "https://localhost:8081"
ANNOUNCE_FILE_TABLE = "announce/data/file-table.csv"
ANNOUNCE_AUDIO_DIR = "announce/data/"
ANNOUNCE_GLITCH_DIR = "announce/data/glitch/"
ANNOUNCE_FILE_FIELDS = ['announcement', 'announceid', 'year', 'filename', 'notes']
ANNOUNCE_LOOP_DELAY = 0.25
ANNOUNCE_AUDIO_EXT = ".mp3"
ANNOUNCE_VOLUME = "0.8"

# Crossing class
# CROSS_SRV = "https://crossing.local:8080"
CROSS_SRV = "https://localhost:8082"
CROSS_LOOP_DELAY = 0.25
CROSS_OFF = 0
CROSS_ON = 1
CROSS_PINOUT_SCHEME = GPIO.BCM   # Broadcom pin numbering (NOT Wiring Pin numbering)
CROSS_PIN = 19

# Lights class
# LIGHTS_SRV = "https://lights.local:8080"
LIGHTS_SRV = "https://localhost:8083"
LIGHTS_LOOP_DELAY = 0.25
LIGHTS_GLITCH_LENGTH = 2        # longest glitch in seconds
LIGHTS_TOTAL = 4
LIGHTS_TABLE = {
    "1858": [STATE_ON, STATE_OFF, STATE_OFF, STATE_OFF],
    "1888": [STATE_ON, STATE_OFF, STATE_OFF, STATE_OFF],
    "1938": [STATE_ON, STATE_OFF, STATE_OFF, STATE_OFF],
    "1959": [STATE_ON, STATE_ON, STATE_OFF, STATE_OFF],
    "1982": [STATE_OFF, STATE_ON, STATE_OFF, STATE_OFF],
    "2014": [STATE_OFF, STATE_ON, STATE_OFF, STATE_OFF],
    "2066": [STATE_OFF, STATE_OFF, STATE_OFF, STATE_OFF],
    "2110": [STATE_ON, STATE_OFF, STATE_OFF, STATE_OFF]
}
LIGHT_NAME_TABLE = ["Pendant", "Fluorescent", "Undefined3", "Undefined4"]
LIGHTS_PINOUT_SCHEME = GPIO.BCM   # Broadcom pin numbering (NOT Wiring Pin numbering)
LIGHTS_PIN_TABLE = [19, 20, 21, 26]

# Signal class
# BRIDGE_SRV = "https://bridge.local:8080"
BRIDGE_SRV = "https://localhost:8084"
BRIDGE_LOOP_DELAY = 0.25
BRIDGE_WB_STOP = 0          # Westbound stop signal
BRIDGE_WB_GO = 1            # Westbound go signal
BRIDGE_EB_STOP = 2          # Eastbound stop signal
BRIDGE_EB_GO = 3            # Eastbound go signal
BRIDGE_PINOUT_SCHEME = GPIO.BCM   # Broadcom pin numbering (NOT Wiring Pin numbering)
BRIDGE_PIN_TABLE = [19, 20, 21, 26]

# Train class
# TRAIN_SRV = "https://train.local:8080"
TRAIN_SRV = "https://localhost:8085"
TRAIN_FILE_TABLE = "train/data/file-table.csv"
TRAIN_FILE_FIELDS = ['year', 'type', 'filename']
TRAIN_TYPES = ["freight-through", "freight-stop", "passenger-through", "passenger-stop"]
TRAIN_AUDIO_DIR = "train/data/"
TRAIN_TMP_FILE = "train/data/tmp-audio.mp3"
TRAIN_LOOP_DELAY = 0.25
TRAIN_AUDIO_EXT = ".mp3"
TRAIN_VOLUME = "0.9"

# Radio class
# RADIO_SRV = "https://radio.local:8080"
RADIO_SRV = "https://localhost:8086"
RADIO_AUDIO_DIR = "radio/data/"
RADIO_LOOP_DELAY = 0.25
RADIO_AUDIO_EXT = ".mp3"
RADIO_VOLUME = "0.8"
RADIO_TRANSITION = "radio/data/transition/radio-static-burst.mp3"
RADIO_TRANSITION_LEN = 0.6

# TV class
# TV_SRV = "https://television.local:8080"
TV_SRV = "https://localhost:8087"
TV_VIDEO_DIR = "television/data/"
TV_LOOP_DELAY = 0.25
TV_VIDEO_EXT = ".mp4"
TV_VOLUME = "0.8"
