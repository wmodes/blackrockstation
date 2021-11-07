"""Display class for scheduler subsystem."""

from shared import config
import logging
import curses
from datetime import datetime
import time

logger = logging.getLogger()

class Display(object):
    """Display controller class."""

    def __init__(self):
        # TODO: check for terminal before initiating curses
        # TODO: better error handling if terminal disconnected
        # TODO: periodically check for terminal and init if found
        # TODO: make sure if not term, all the methods fail gracefully
        try:
            self.init_screen()
            self.screen_avail = True;
        except:
            logging.info("No screen found, continuing without it")
            self.screen_avail = False;

    def init_screen(self):
        """Initialize Display class."""
        self.screen = curses.initscr()
        curses.start_color()
        curses.use_default_colors()
        curses.curs_set(2)
        self.scr_height = curses.LINES - 1
        self.scr_width = curses.COLS - 1
        #
        # create time window
        self.time_win_y_origin = 0
        self.time_win_x_origin = 0
        self.time_win_height = config.SCHED_WIN_TIME_HEIGHT
        self.time_win_width = self.scr_width + 1
        self.time_win_wrap = curses.newwin(
            self.time_win_height, self.time_win_width,
            self.time_win_y_origin, self.time_win_x_origin)
        self.time_win_wrap.border();
        self.time_win = curses.newwin(
            self.time_win_height-2, self.time_win_width-2,
            self.time_win_y_origin+1, self.time_win_x_origin+1)
        #
        # create status window
        self.status_win_y_origin = self.scr_height - config.SCHED_WIN_STATUS_HEIGHT
        self.status_win_x_origin = 0
        self.status_win_height = config.SCHED_WIN_STATUS_HEIGHT
        self.status_win_width = self.scr_width + 1
        self.status_win_wrap = curses.newwin(
            self.status_win_height, self.status_win_width,
            self.status_win_y_origin, self.status_win_x_origin)
        self.status_win_wrap.border();
        self.status_win = curses.newwin(
            self.status_win_height-2, self.status_win_width-2,
            self.status_win_y_origin+1, self.status_win_x_origin+1)
        self.status_win.scrollok(True)
        #
        # create schedule window
        self.sched_win_y_origin = self.time_win_height - 1
        self.sched_win_x_origin = 0
        self.sched_win_height = self.scr_height - self.time_win_height - self.status_win_height + 2
        self.sched_win_width = self.scr_width + 1
        self.sched_win_wrap = curses.newwin(
            self.sched_win_height, self.sched_win_width,
            self.sched_win_y_origin, self.sched_win_x_origin)
        self.sched_win_wrap.border();
        self.sched_win = curses.newwin(
            self.sched_win_height-2, self.sched_win_width-2,
            self.sched_win_y_origin+1, self.sched_win_x_origin+1)
        #
        self.fix1_vert = self.time_win_y_origin + self.time_win_height
        self.fix2_vert = self.status_win_y_origin

    def update(self):
        if ! self.screen_avail:
            return
        self.screen.clear()
        self.time_win.refresh()

    def display_sched(self, text):
        if ! self.screen_avail:
            return
        self.sched_win.clear
        self.sched_win_wrap.clear
        self.sched_win_wrap.addch(0, 0, curses.ACS_LTEE)
        self.sched_win_wrap.addch(0, curses.COLS - 1, curses.ACS_RTEE)
        self.sched_win_wrap.addch(self.sched_win_height-1, 0, curses.ACS_LTEE)
        self.sched_win_wrap.addch(self.sched_win_height-1, curses.COLS - 2, curses.ACS_RTEE)
        self.sched_win_wrap.refresh()
        # self.corner_fix()
        str_array = text.splitlines()
        for i in range(min(len(str_array), self.sched_win_height-3)):
            # print(str_array[i])
            if i == 3:
                attr = curses.A_REVERSE
            else:
                attr = curses.A_NORMAL
            self.sched_win.addstr(i, 0, str_array[i], attr)
            self.sched_win.refresh()
            time.sleep(config.SCHED_LOOP_DELAY/4)
        self.sched_win.refresh()

    def display_time(self, traintime, timeslip, year):
        if ! self.screen_avail:
            return
        now = datetime.now()
        date_str = now.strftime(config.SCHED_TIME_FORMAT)
        self.time_win.clear
        self.time_win_wrap.clear
        # self.time_win_wrap.addch(self.time_win_height-1, 0, curses.ACS_LTEE)
        # self.time_win_wrap.addch(self.time_win_height-1, curses.COLS - 2, curses.ACS_RTEE)
        self.time_win_wrap.refresh()
        # self.corner_fix()
        self.time_win.addstr(0, 1, f"Current: {date_str}       ", curses.A_BOLD)
        self.time_win.addstr(1, 1, f"Next Train: {traintime}       ")
        self.time_win.addstr(2, 1, f"Est Timeslip: {timeslip}      ")
        self.time_win.addstr(3, 1, f"Current Year: {year}      ")
        self.time_win.refresh()

    def display_status(self, text=None):
        if ! self.screen_avail:
            return
        self.status_win.clear
        self.status_win_wrap.clear
        self.status_win_wrap.addch(0, 0, curses.ACS_LTEE)
        self.status_win_wrap.addch(0, curses.COLS - 1, curses.ACS_RTEE)
        self.status_win_wrap.refresh()
        # self.corner_fix()
        if text:
            self.status_win.addstr(config.SCHED_WIN_STATUS_HEIGHT-3, 1, text+'\n')
        self.status_win.refresh()

    def corner_fix(self):
        self.screen.addch(self.fix1_vert, 0, curses.ACS_LTEE)
        self.screen.addch(self.fix1_vert, curses.COLS - 1, curses.ACS_RTEE)
        self.screen.addch(self.fix2_vert, 0, curses.ACS_LTEE)
        self.screen.addch(self.fix2_vert, curses.COLS - 1, curses.ACS_RTEE)
        self.screen.refresh()
