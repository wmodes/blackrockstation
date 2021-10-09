"""Display class for scheduler subsystem."""

from shared import config
import logging
import curses
from datetime import datetime

logger = logging.getLogger()

class Display(object):
    """Display controller class."""

    def __init__(self):
        """Initialize Display class."""
        self.screen = curses.initscr()
        self.scr_height = curses.LINES - 1
        self.scr_width = curses.COLS - 1
        #
        # create time window
        self.time_win_y_origin = 0
        self.time_win_x_origin = 0
        self.time_win_height = config.SCHED_WIN_TIME_HEIGHT
        self.time_win_width = self.scr_width
        self.time_win_wrap = curses.newwin(
            self.time_win_height, self.time_win_width,
            self.time_win_y_origin, self.time_win_x_origin)
        self.time_win_wrap.box(0,0);
        self.time_win = curses.newwin(
            self.time_win_height-2, self.time_win_width-2,
            self.time_win_y_origin+1, self.time_win_x_origin+1)
        #
        # create status window
        self.status_win_y_origin = self.scr_height - config.SCHED_WIN_STATUS_HEIGHT
        self.status_win_x_origin = 0
        self.status_win_height = config.SCHED_WIN_STATUS_HEIGHT
        self.status_win_width = self.scr_width
        self.status_win_wrap = curses.newwin(
            self.status_win_height, self.status_win_width,
            self.status_win_y_origin, self.status_win_x_origin)
        self.status_win_wrap.box(0,0);
        self.status_win = curses.newwin(
            self.status_win_height-2, self.status_win_width-2,
            self.status_win_y_origin+1, self.status_win_x_origin+1)
        self.status_win.scrollok(True)
        #
        # create schedule window
        self.sched_win_y_origin = self.time_win_height
        self.sched_win_x_origin = 0
        self.sched_win_height = self.scr_height - self.time_win_height - self.status_win_height
        self.sched_win_width = self.scr_width
        self.sched_win_wrap = curses.newwin(
            self.sched_win_height, self.sched_win_width,
            self.sched_win_y_origin, self.sched_win_x_origin)
        self.sched_win_wrap.box(0,0);
        self.sched_win = curses.newwin(
            self.sched_win_height-2, self.sched_win_width-2,
            self.sched_win_y_origin+1, self.sched_win_x_origin+1)
        #
        # self.screen.clear()
        # self.screen.refresh()
        # self.time_win.refresh()
        # self.sched_win.refresh()

    def update(self):
        self.screen.clear()
        self.time_win.refresh()

    def display_sched(self, text):
        self.sched_win.clear
        self.sched_win_wrap.refresh()
        str_array = text.splitlines()
        for i in range(min(len(str_array), self.sched_win_height-3)):
            # print(str_array[i])
            self.sched_win.addstr(i, 0, str_array[i])
        self.sched_win.refresh()

    def display_time(self, traintime, timeslip, year):
        now = datetime.now()
        date_str = now.strftime(config.SCHED_TIME_FORMAT)
        self.time_win.clear
        self.time_win_wrap.refresh()
        self.time_win.addstr(0, 1, f"Current: {date_str}       ")
        self.time_win.addstr(1, 1, f"Next Train: {traintime}       ")
        self.time_win.addstr(2, 1, f"Est Timeslip: {timeslip}      ")
        self.time_win.addstr(3, 1, f"Current Year: {year}      ")
        self.time_win.refresh()

    def display_status(self, text=None):
        self.status_win.clear
        self.status_win_wrap.refresh()
        if text:
            self.status_win.addstr(config.SCHED_WIN_STATUS_HEIGHT-3, 1, text+'\n')
        self.status_win.refresh()
