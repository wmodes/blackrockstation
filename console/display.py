"""Display class for scheduler subsystem."""

from shared import config
import logging
import curses
from datetime import datetime
import time

logger = logging.getLogger()
logger.setLevel(config.LOG_LEVEL)

class Display(object):
    """Display controller class."""

    def __init__(self):
        # DONE: check for terminal before initiating curses
        # DONE: better error handling if terminal disconnected
        # DONE: periodically check for terminal and init if found
        # DONE: make sure if not term, all the methods fail gracefully
        self.screen_avail = None;
        self.try_to_init()

    def try_to_init(self):
        try:
            self.init_screen()
            self.screen_avail = True;
            logging.info("screen found, displaying")
        except:
            if self.screen_avail == None:
                logging.info("no screen found, continuing without it")
            self.screen_avail = False;

    def init_screen(self):
        """Initialize Display class."""
        self.screen = curses.initscr()
        # curses.start_color()
        # curses.use_default_colors()
        curses.curs_set(2)
        self.scr_height = curses.LINES #- 1
        self.scr_width = curses.COLS #- 1
        #
        # create time window
        #
        self.time_win_y_origin = 0
        self.time_win_x_origin = 0
        self.time_win_height = config.CONSOLE_WIN_TIME_HEIGHT
        self.time_win_width = self.scr_width
        # wrapper with lines
        self.time_win_wrap = curses.newwin(
            self.time_win_height, self.time_win_width,
            self.time_win_y_origin, self.time_win_x_origin)
        self.time_win_wrap.border();
        self.time_win_wrap.clear
        self.time_win_wrap.refresh()
        # left panel
        self.time_win_lt = curses.newwin(
            self.time_win_height-2, (self.time_win_width-2)//2,
            self.time_win_y_origin+1, self.time_win_x_origin+1)
        # right panel
        self.time_win_rt = curses.newwin(
            self.time_win_height-2, (self.time_win_width-3)//2,
            self.time_win_y_origin+1, self.time_win_x_origin+self.time_win_width//2)
        #
        # create status window
        #
        self.status_win_y_origin = self.scr_height - config.CONSOLE_WIN_STATUS_HEIGHT
        self.status_win_x_origin = 0
        self.status_win_height = config.CONSOLE_WIN_STATUS_HEIGHT
        self.status_win_width = self.scr_width #+ 1
        # wrapper with lines
        self.status_win_wrap = curses.newwin(
            self.status_win_height, self.status_win_width,
            self.status_win_y_origin, self.status_win_x_origin)
        self.status_win_wrap.border();
        self.status_win_wrap.clear
        self.status_win_wrap.refresh()
        # inner panel
        self.status_win = curses.newwin(
            self.status_win_height-2, self.status_win_width-2,
            self.status_win_y_origin+1, self.status_win_x_origin+1)
        self.status_win.scrollok(True)
        #
        # create schedule window
        #
        self.sched_win_y_origin = self.time_win_height - 1
        self.sched_win_x_origin = 0
        self.sched_win_height = self.scr_height - self.time_win_height - self.status_win_height + 2
        self.sched_win_width = self.scr_width #+ 1
        # wrapper with lines
        self.sched_win_wrap = curses.newwin(
            self.sched_win_height, self.sched_win_width,
            self.sched_win_y_origin, self.sched_win_x_origin)
        self.sched_win_wrap.border();
        self.sched_win_wrap.clear
        self.sched_win_wrap.refresh()
        # inner panel
        self.sched_win = curses.newwin(
            self.sched_win_height-2, self.sched_win_width-4,
            self.sched_win_y_origin+1, self.sched_win_x_origin+2)
        #
        self.fix1_vert = self.time_win_y_origin + self.time_win_height
        self.fix2_vert = self.status_win_y_origin
        self.corner_fix()
        # keyboard init
        # read keys and only display them under certain circumstances
        curses.noecho()
        # read keys and only display them under certain circumstances
        curses.cbreak()
        # instead of returning special keys as multibyte escape sequences,
        # return a special values, e.g., curses.KEY_LEFT
        self.screen.keypad(True)
        # Make getch() and getkey() non-blocking, i.e, not wait for input
        self.time_win_rt.nodelay(True)

    def stop_screen(self):
        logging.debug("stop_screen() called")
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.endwin()

    # def update(self):
    #     if not self.screen_avail:
    #         return
    #     self.screen.clear()
    #     self.time_win.refresh()

    def display_sched(self, text):
        if not self.screen_avail:
            return
        self.sched_win.clear
        self.sched_win.refresh()
        # self.sched_win_wrap.clear
        # self.sched_win_wrap.refresh()
        # self.corner_fix()
        str_array = text.splitlines()
        for i in range(min(len(str_array), self.sched_win_height-3)):
            if i == 1:
                attr = curses.A_REVERSE
            else:
                attr = curses.A_NORMAL
            self.sched_win.addstr(i, 0, str_array[i], attr)
            self.sched_win.refresh()
            # time.sleep(config.CONSOLE_LOOP_DELAY/4)
        self.sched_win.refresh()

    def display_time(self, next_train, next_timeslip, current_year):
        if not self.screen_avail:
            return
        # format current time
        now_dt = datetime.now()
        date_str = self.time2txt(now_dt)
        # current year
        if current_year:
            current_year_str = current_year
        else:
            current_year_str = "???"
        # format timeslip
        if next_timeslip:
            timeslip_delta = next_timeslip - now_dt
            timeslip_str = self.delta2txt(timeslip_delta)
        else:
            timeslip_str = "???"
        # format next train time
        if next_train:
            train_delta = next_train - now_dt
            train_str = self.delta2txt(train_delta)
        else:
            train_str = "???"
        # clear the time window
        self.time_win_lt.clear
        self.time_win_rt.clear
        #
        # left panel
        self.time_win_lt.addstr(0, 1, f"Current Time: {date_str}  ", curses.A_BOLD)
        self.time_win_lt.addstr(1, 1, f"Current Year: {current_year_str}  ")
        self.time_win_lt.refresh()
        #
        # right panel
        self.time_win_rt.addstr(0, 1, f"Time Until Timeslip: {timeslip_str}  ")
        self.time_win_rt.addstr(1, 1, f"Time Until Next Train: {train_str}  ")
        self.time_win_rt.refresh()

    def display_status(self, text=None):
        if not self.screen_avail:
            return
        self.status_win.clear
        # self.status_win_wrap.clear
        # self.status_win_wrap.refresh()
        # self.corner_fix()
        if text:
            self.status_win.addstr(config.CONSOLE_WIN_STATUS_HEIGHT-3, 1, text)
        self.status_win.refresh()

    def corner_fix(self):
        self.sched_win_wrap.addch(0, 0, curses.ACS_LTEE)
        self.sched_win_wrap.addch(0, curses.COLS - 1, curses.ACS_RTEE)
        self.sched_win_wrap.addch(self.sched_win_height-1, 0, curses.ACS_LTEE)
        self.sched_win_wrap.addch(self.sched_win_height-1, curses.COLS - 2, curses.ACS_RTEE)
        self.sched_win_wrap.refresh()
        #
        self.status_win_wrap.addch(0, 0, curses.ACS_LTEE)
        self.status_win_wrap.addch(0, curses.COLS - 1, curses.ACS_RTEE)
        self.status_win_wrap.refresh()
        # self.screen.addch(self.fix1_vert, 0, curses.ACS_LTEE)
        # self.screen.addch(self.fix1_vert, curses.COLS - 1, curses.ACS_RTEE)
        # self.screen.addch(self.fix2_vert, 0, curses.ACS_LTEE)
        # self.screen.addch(self.fix2_vert, curses.COLS - 1, curses.ACS_RTEE)

    #
    # input
    #
    def is_keypress(self):
        if not self.screen_avail:
            return None
        key = self.time_win_rt.getch()
        if not key == curses.ERR:
            return key
        # if not curses.ERR
        # if key == curses.KEY_ENTER or key == ord(' '):
        #    return key
        return None

    #
    # Time Helpers
    #
    def delta2txt(self, delta):
        s = delta.seconds
        hrs, rem = divmod(s, 3600)
        min, sec = divmod(rem, 60)
        return f"{hrs:02d}:{min:02d}:{sec:02d}"

    def time2txt(self, time_dt):
        return time_dt.strftime(config.CONSOLE_LONG_TIME_FORMAT)
