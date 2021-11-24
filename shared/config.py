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
DEBUG = False
ID_FILE = ".identity"
PKG_ROOT = "blackrockstation"
LOG_DIR = "logs/"
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
COMMS_TIMEOUT = 1

# Start
CONTROLLERS = {
	"scheduler":  {"port": 8080,
                   "server": "brs-scheduler.local"},
	"announce":   {"port": 8081,
                   "server": "brs-announce.local"},
	"bridge":     {"port": 8082,
                   "server": "brs-bridge.local"},
	"crossing":   {"port": 8083,
                   "server": "brs-crossing.local"},
	"lights":     {"port": 8084,
                   "server": "brs-lights.local"},
	"radio":      {"port": 8085,
                   "server": "brs-radio.local"},
	"train":      {"port": 8086,
                   "server": "brs-train.local"},
	"television": {"port": 8087,
                   "server": "brs-television.local"}
}


# Controller parent class
VALID_YEARS = ['glitch', '1858', '1888', '1938', '1959', '1982', '2014', '2066', '2110']

# Scheduler class
SCHED_DATA = "scheduler/data/schedule.csv"
SCHED_FIELDS = ['event', 'controller', 'time', 'duration', 'direction', 'traintype', 'variance', 'notes', 'announceid', 'time_since_last']
SCHED_LOOP_DELAY = 0.25
SCHED_DEFAULT_LOG = 100
SCHED_YEARS = [1938, 1959, 1982, 2014, 2066, 2110, 1858, 1888]
SCHED_TIMESLIP_INTERVAL = 14        # time in minutes default=26
SCHED_TIMESLIP_GLITCH = 31         # time in seeconds
SCHED_PERIODIC = [
    {"controller": "announce", "announceid": "periodic-announcement-1", "times_per_day": 3},
    {"controller": "announce", "announceid": "periodic-announcement-2", "times_per_day": 3},
    {"controller": "announce", "announceid": "periodic-announcement-3", "times_per_day": 6},
    {"controller": "announce", "announceid": "periodic-announcement-4", "times_per_day": 6}
]
SCHED_DEPART_TIME = 1.5      # time in minutes
SCHED_BRIDGE_BEFORE = 2       # time in minutes
SCHED_CROSSING_DELAY = 0.5     # time in minutes

# Console class
CONSOLE_LOOP_DELAY = 0.25
CONSOLE_DISPLAY_TRAINS = 14         # max number of trains to display
CONSOLE_DISPLAY_LOGS = 8           # max number of logs to display
CONSOLE_TIME_FORMAT = "%a %b %d, %Y %H:%M:%S"
CONSOLE_UPDATE_STATUS_FREQ = 1      # seconds to update status
CONSOLE_UPDATE_SCHED_FREQ = 30      # seconds to update sched
CONSOLE_UPDATE_STATUS_FREQ = 30       # seconds to update logs
CONSOLE_DISPLAY_CHECK_FREQ = 5      # sec between attempts to init display
CONSOLE_DISPLAY_TIME_FREQ = 1       # sec to update time display
CONSOLE_DISPLAY_SCHED_FREQ = 30     # seconds to update sched display
CONSOLE_DISPLAY_STATUS_FREQ = 30      # seconds to update logs display
CONSOLE_WIN_TIME_HEIGHT = 6
CONSOLE_WIN_STATUS_HEIGHT = 8

# Announce class
ANNOUNCE_FILE_TABLE = "announce/data/file-table.csv"
ANNOUNCE_AUDIO_DIR = "announce/data/"
ANNOUNCE_GLITCH_DIR = "announce/data/glitch/"
ANNOUNCE_FILE_FIELDS = ['announcement', 'announceid', 'year', 'filename', 'notes']
ANNOUNCE_LOOP_DELAY = 0.25
ANNOUNCE_AUDIO_EXT = ".mp3"
ANNOUNCE_VOLUME = "0.8"

# Signal class
BRIDGE_LOOP_DELAY = 0.25
BRIDGE_WB_STOP = 0          # Westbound stop signal
BRIDGE_WB_GO = 1            # Westbound go signal
BRIDGE_EB_STOP = 2          # Eastbound stop signal
BRIDGE_EB_GO = 3            # Eastbound go signal
BRIDGE_PINOUT_SCHEME = GPIO.BCM   # Broadcom pin numbering (NOT Wiring Pin numbering)
BRIDGE_PIN_TABLE = [19, 20, 21, 26]

# Crossing class
CROSS_LOOP_DELAY = 0.25
CROSS_OFF = 0
CROSS_ON = 1
CROSS_PINOUT_SCHEME = GPIO.BCM   # Broadcom pin numbering (NOT Wiring Pin numbering)
CROSS_PIN = 19

# Lights class
LIGHTS_LOOP_DELAY = 0.25
LIGHTS_GLITCH_LENGTH = 2        # longest glitch in seconds
LIGHTS_TOTAL = 4
LIGHTS_TABLE = {
    "glitch": [STATE_ON, STATE_ON, STATE_ON, STATE_ON],
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

# Radio class
RADIO_AUDIO_DIR = "radio/data/"
RADIO_LOOP_DELAY = 0.25
RADIO_AUDIO_EXT = ".mp3"
RADIO_VOLUME = 0.8
RADIO_TRANSITION = "radio/data/transition/radio-static-burst.mp3"
RADIO_TRANSITION_LEN = 0.6

# Train class
TRAIN_FILE_TABLE = "train/data/file-table.csv"
TRAIN_FILE_FIELDS = ['year', 'traintype', 'filename']
TRAIN_TYPES = ["freight-through", "freight-stop", "passenger-through", "passenger-stop"]
TRAIN_AUDIO_DIR = "train/data/"
TRAIN_TMP_FILE = "train/data/tmp-audio.mp3"
TRAIN_LOOP_DELAY = 0.25
TRAIN_AUDIO_EXT = ".mp3"
TRAIN_VOLUME = 1.0

# TV class
TV_VIDEO_DIR = "television/data/"
TV_LOOP_DELAY = 0.25
TV_VIDEO_EXT = ".mp4"
TV_VOLUME = "0.8"
# extra options to enable extra http interface
# "--extraintf", "http", "--http-host", "localhost", "--http-port", "9090", "--http-password", "vlc"
# curl 'http://:vlc@localhost:9090/requests/status.xml?command=in_play&input=television/data/1959'
# curl 'http://:vlc@localhost:9090/requests/status.xml?command=pl_empty'
TV_DEFAULT_VID = "tv-static-noise-720p.mp4"
TV_PLATFORM = {
    "raspi": {
        "start": ["/usr/bin/cvlc", "--playlist-autostart", "--video-on-top", "--random", "--loop", "--fullscreen", "--no-video-title", "--autoscale", "--extraintf", "http", "--http-host", "localhost", "--http-port", "9090", "--http-password", "vlc"],
        "stop": ["killall", "vlc"]
    },
    "macos": {
        "start": ["/usr/local/bin/vlc", "--playlist-autostart", "--video-on-top", "--random", "--loop", "--fullscreen", "--no-video-title", "--autoscale", "--extraintf", "http", "--http-host", "localhost", "--http-port", "9090", "--http-password", "vlc"],
        "stop": ["/usr/bin/killall", "vlc"],
    }
}
TV_URL = {
    "clear": "http://:vlc@localhost:9090/requests/status.xml?command=pl_empty",
    "enqueue": "http://:vlc@localhost:9090/requests/status.xml?command=in_play&input="
}

if sys.platform == "darwin":
    # OS X
    RADIO_VOLUME = 0.03
