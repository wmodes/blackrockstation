"""Controller class for console subsystem."""

from shared import config
from shared.controller import Controller
from console.display import Display

import logging
from datetime import datetime, timedelta
import csv
from columnar import columnar
import time
import re
import random
import shutil
import curses
import re

logger = logging.getLogger()
logger.setLevel(config.LOG_LEVEL)

class Console(Controller):
    """Console controller class."""

    MODE_GENERAL = "general"
    MODE_DETAIL = "detail"
    MODES = [MODE_GENERAL, MODE_DETAIL]

    def __init__(self):
        """Initialize Console class."""
        super().__init__()
        self.whoami = "console"
        self.mode = 0
        self.schedule = []
        self.current_logs = ""
        self.current_year = None
        self.next_timeslip = None
        self.next_train = None
        self.cycle_count = 0
        self.display = Display()

    """
        SETUP
    """

    """
        REPORTS
    """

    def get_future_trains(self, n=10):
        """Return array of objects representing future trains.

        We do this in a few steps:
        1) Interate through train schedule until we find the item just after the current now() time
        2) Add each item to a list
        3) If we have n items already, we can stop, but
        4) If we hit the end of the records before n items,
        5) We iterate from the beginning of the schedule appending items to our list until we either get n items or hit where we started
        """
        future_list = []
        # search through train schedule for time that matches H:M
        now_dt = datetime.now()
        for event in self.schedule:
            # if this event is not a train event, skip
            if event["controller"] != "train":
                continue
            # if this event is already in the past, skip
            if self.str2dt(event["time"], False) < now_dt:
                continue
            # all the following events are in the future
            # if we have n events, stop
            if len(future_list) >= n:
                break
            # since complex datatypes are passed by ref and we want
            # to be able to change it later without affecting orig
            # data structure, we copy it
            future_list.append(event.copy())
        # if we don't have
        if len(future_list) < n:
            for event in self.schedule:
                # if this event is not a train event, skip
                if event["controller"] != "train":
                    continue
                # if this event is not in the past, stop (i.e., we've wrapped around)
                if self.str2dt(event["time"], False) > now_dt:
                    break
                # if we have n events, stop
                if len(future_list) >= n:
                    break
                # copy it
                future_list.append(event.copy())
        # corrections and fixes
        for item in future_list:
            item['time'] = self.format_time_str(item['time'])
        return future_list
        #return self.display_train_schedule(future_list)

    def construct_disp_sched(self, event_list):
        """Filter a full event list into just what we want to display."""
        # convert dict to array of arrays
        events = []
        for event in event_list:
            if event['controller'] == "train":
                # lets abbreviate some STUFF
                # direction
                dir = event['direction']
                if dir.lower().startswith('e'):
                    event['direction'] = "E"
                else:
                    event['direction'] = "W"
                # type
                type = event['traintype']
                newtype = type[0].upper()
                if '-' in type:
                    newtype += '-'
                    newtype += type[type.find('-')+1].upper()
                event['traintype'] = newtype
                events.append([event['event'], event['time'],
                              event['direction'], event['traintype'], event['notes']])
        return events

    def tabulate_data(self, data):
        """Take data in form of list and make a structured table."""
        scr_width = shutil.get_terminal_size().columns
        max_col_width = (scr_width - 18) // 2
        # df = pd.DataFrame(data)
        # df.columns = ['TRAIN', 'ARRIVE', 'DIR', 'TYPE', 'NOTES']
        # return df.to_string(
        #     formatters=self.format_align_left(df, ['TRAIN', 'NOTES']),
        #     index=False,
        #     justify="left",
        #     max_colwidth=max_col_width)
        headers = ['TRAIN', 'ARRIVE', 'DIR', 'TYPE', 'NOTES']
        justify = ['l', 'l', 'c', 'l', 'l']
        table = columnar(
            data,
            headers,
            justify=justify,
            no_borders=True,
            max_column_width=max_col_width,
            wrap_max=8,
            terminal_width=scr_width,
            column_sep='')
        # convert to array
        table_array = str(table).split('\n')
        # drop first and third line
        table_array.pop(0)
        table_array.pop(1)
        # remove two spaces at beginning of each line
        for i in range(len(table_array)):
            table_array[i] = table_array[i][2:]
        # put back together again
        table = '\n'.join(table_array)
        return table

    def display_future_trains(self):
        """Return human-readable schedule of future trains."""
        event_list = self.get_future_trains(config.CONSOLE_DISPLAY_TRAINS)
        headers = ['Train', 'Arrive', 'Dir', 'Type', 'Notes']
        # convert dict to array of arrays
        events = self.construct_disp_sched(event_list)
        if not len(events):
            return
        table = self.tabulate_data(events)
        return str(table)

    def display_train_details(self):
        """Return human-readable detail of future trains."""
        event_list = self.get_future_trains(config.CONSOLE_DISPLAY_TRAINS)
        # print ("display_train_details():  "  + str(event_list))
        if not len(event_list):
            return
        # next train
        next = event_list[0]
        output = "NEXT TRAIN\n"
        output += f"{next['event']}\n"
        output += f"Arrival: {next['time']}\t"
        output += f"Type: {next['traintype']}\t"
        output += f"Dir: {next['direction']}\n"
        output += self.break_nicely(f"Notes: {next['notes']}", config.CONSOLE_LINE_LEN)
        # next passenger train
        next = [item for item in event_list if item.get('traintype')=='passenger-stop'][0]
        if next:
            output += "\n\nNEXT PASSENGER STOP\n"
            output += f"{next['event']}\n"
            output += f"Arrival: {next['time']}\t"
            output += f"Type: {next['traintype']}\t"
            output += f"Dir: {next['direction']}\n"
            output += self.break_nicely(f"Notes: {next['notes']}", config.CONSOLE_LINE_LEN)
        return output

    def format_logs(self, raw_logs):
        """Take raw logs and format them for display."""
        logs = raw_logs.split('\n')
        for i in range(len(logs)):
            logs[i] = re.sub(r"^.*scheduler: ", "", logs[i])
        return '\n'.join(logs)

    def break_nicely(self, text, length):
        if len(text) <= length:
            return text
        # split at length
        line1 = text[:length]
        rest = text[length:]
        # look for last space
        pos = line1.rfind(' ')
        # if there is no space in line1, don't try to break nicely
        if pos != -1:
            # else break at the space
            line1_nice = line1[:pos]
            rest = line1[pos+1:] + rest
        return line1_nice + '\n' + self.break_nicely(rest, length)

    """
        ORDERS
    """

    def get_scheduler_status(self):
        """Get status from scheduler and assign locals.
        Here's the data we'll get back from a reqStatus:
            {
              "cmd": "reqStatus",
              "results": {
                "controller": "scheduler",
                "currentYear": 1982,
                "nextTimeslip": "13:17",
                "nextTrain": {
                  "announceid": "",
                  "controller": "train",
                  "direction": "eastbound",
                  "duration": "3",
                  "event": "Afternoon Express Oakland to SLC",
                  "index": 18,
                  "notes": "Leaves Oakland 4pm. Express is 18hrs w BRC about 1/3 of the way. Comes through BRC at 10pm.",
                  "time": "22:13",
                  "time_since_last": "2:25",
                  "traintype": "passenger-through",
                  "variance": "30"
                },
                "running": true
              },
              "status": "OK"
            }
        """
        controller = "scheduler"
        cmd_obj = {"cmd": "reqStatus"}
        results = self.comms.send_order(controller, cmd_obj)
        if results["status"] == 'FAIL':
            logging.warning(f"order to {controller} failed: {results['error']}")
            self.current_year = None
            self.next_timeslip = None
            self.next_train = None
            return
        self.current_year = results["results"]["currentYear"]
        next_timeslip_txt = results["results"]["nextTimeslip"]
        self.next_timeslip = self.str_delta_plus_now(next_timeslip_txt)
        next_train_txt = results["results"]["nextTrain"]["time"]
        self.next_train = self.str2dt(next_train_txt)

    def get_scheduler_trains(self):
        """Get trains from scheduler and assign locals.
        Here's the data we'll get back from a reqStatus:
        {
          "cmd": "reqAllTrains",
          "results": [
            {
              "announceid": "",
              "controller": "train",
              "direction": "eastbound",
              "duration": "3",
              "event": "Night Through Freight (hot)",
              "index": 0,
              "notes": "Through freight to points east",
              "time": "0:20",
              "time_since_last": "--",
              "traintype": "freight-through",
              "variance": "45"
            },
            {
              "announceid": "",
              "controller": "train",
              "direction": "westbound",
              "duration": "3",
              "event": "Night Through Freight (hot)",
              "index": 1,
              "notes": "Through freight to the coast",
              "time": "1:30",
              "time_since_last": "1:10",
              "traintype": "freight-through",
              "variance": "45"
            }
          ],
          "status": "OK"
        }
        """
        controller = "scheduler"
        cmd_obj = {"cmd":"reqAllTrains"}
        results = self.comms.send_order(controller, cmd_obj)
        if results["status"] == 'FAIL':
            logging.warning(f"order to {controller} failed: {results['error']}")
            return
        self.schedule = results["results"]

    def get_scheduler_logs(self):
        """Get logs from scheduler.
        Here's the data we'll get back from a reqStatus:
            {
              "cmd": "reqLog",
              "results": "2021-11-24 09:58:18,313 scheduler: INFO: 192.168.86.242 - - [24/Nov/2021 09:58:18] \"POST /cmd HTTP/1.1\" 200 -\n2021-11-24 09:58:19,769 scheduler: INFO: 192.168.86.242 - - [24/Nov/2021 09:58:19] \"POST /cmd HTTP/1.1\" 200 -\n2021-11-24 09:58:20,238 scheduler: INFO: 192.168.86.242 - - [24/Nov/2021 09:58:20] \"OPTIONS /cmd HTTP/1.1\" 200 -",
              "status": "OK"
            }
        """
        controller = "scheduler"
        cmd_obj = {"cmd":"reqLog","qty":config.CONSOLE_DISPLAY_LOGS}
        results = self.comms.send_order(controller, cmd_obj)
        if results["status"] == 'FAIL':
            logging.warning(f"order to {controller} failed: {results['error']}")
            return
        self.current_logs = results["results"]


    """
        TIME HELPERS
    """

    def str2dt(self, time_str, is_next=True):
        """
        Given a time string, returns the next matching datetime.

        Params:
            time_str (str) representing a time in %H:%M format
            is_next (bool) whether today's datetime (False) or the next datetime (True) should be found
        """
        now_dt = datetime.now()
        tomorrow_dt = now_dt + timedelta(days=1)
        try:
            nexttime_t = datetime.strptime(time_str, '%H:%M').time()
            nexttime_dt = datetime.combine(now_dt, nexttime_t)
            if is_next:
                time_delta = nexttime_dt - now_dt
                if time_delta.total_seconds() < 0:
                    nexttime_dt = datetime.combine(tomorrow_dt, nexttime_t)
        except:
            logging.warning(f"Bad date: {time_str}")
            nexttime_dt = tomorrow_dt
        return nexttime_dt

    def format_time_str(self, time_str):
        time_dt = self.str2dt(time_str)
        return time_dt.strftime(config.CONSOLE_SHORT_TIME_FORMAT)

    def str_delta_plus_now(self, delta_str):
        """
        Given a delta string in MM:SS format, add it to now and return timedate objects.
        """
        min, sec = delta_str.split(':')
        now_dt = datetime.now()
        delta = timedelta(minutes=int(min), seconds=int(sec))
        return now_dt + delta


    """
        DISPLAY
    """

    def check_for_display(self):
        if not self.display.screen_avail:
            self.display.try_to_init()

    def draw_status_display(self):
        self.display.display_status()

    def update_time_display(self):
        self.display.display_time(self.next_train, self.next_timeslip, self.current_year)

    def update_sched_display(self):
        if self.MODES[self.mode] == self.MODE_GENERAL:
        # if self.mode == 0:
            sched_str = self.display_future_trains()
        elif self.MODES[self.mode] == self.MODE_DETAIL:
        # elif self.mode == 1:
            sched_str = self.display_train_details()
        # just in case we don't get anything, we don't want to
        # freak out downstream
        if sched_str == None:
            sched_str = ""
        self.display.display_sched(sched_str)

    def update_status_display(self):
        formatted_logs = self.format_logs(self.current_logs)
        self.display.display_status(formatted_logs)

    def update_display(self):
        # CHECK FOR DISPLAY
        # we should run this after how many cycles?
        update_check_count = round(config.CONSOLE_DISPLAY_CHECK_FREQ / config.CONSOLE_LOOP_DELAY)
        if self.cycle_count % update_check_count == 0:
            self.check_for_display()
        #
        # CHECK FOR TIME UPDATE
        # we should run this after how many cycles?
        update_time_count = round(config.CONSOLE_DISPLAY_TIME_FREQ / config.CONSOLE_LOOP_DELAY)
        if self.cycle_count % update_time_count == 0:
            self.update_time_display()
        #
        # CHECK FOR SCHEDULE UPDATE
        # we should run this after how many cycles?
        update_sched_count = round(config.CONSOLE_DISPLAY_SCHED_FREQ / config.CONSOLE_LOOP_DELAY)
        if self.cycle_count % update_sched_count == 0:
            self.update_sched_display()
        #
        # CHECK FOR STATUS UPDATE
        # we should run this after how many cycles?
        update_sched_count = round(config.CONSOLE_DISPLAY_STATUS_FREQ / config.CONSOLE_LOOP_DELAY)
        if self.cycle_count % update_sched_count == 0:
            self.update_status_display()


    """
        MAIN LOOP
    """

    def update_data(self):
        # CHECK FOR STATUS UPDATE
        # we should run this after how many cycles?
        update_time_count = round(config.CONSOLE_UPDATE_STATUS_FREQ / config.CONSOLE_LOOP_DELAY)
        if self.cycle_count % update_time_count == 0:
            self.get_scheduler_status()
        #
        # CHECK FOR SCHEDULE UPDATE
        # we should run this after how many cycles?
        update_sched_count = round(config.CONSOLE_UPDATE_SCHED_FREQ / config.CONSOLE_LOOP_DELAY)
        if self.cycle_count % update_sched_count == 0:
            self.get_scheduler_trains()
        #
        # CHECK FOR STATUS UPDATE
        # we should run this after how many cycles?
        update_sched_count = round(config.CONSOLE_UPDATE_STATUS_FREQ / config.CONSOLE_LOOP_DELAY)
        if self.cycle_count % update_sched_count == 0:
            self.get_scheduler_logs()

    def check_for_input(self):
        key = self.display.is_keypress()
        if key:
            self.mode += 1
            if self.mode >= len(self.MODES):
                self.mode = 0
            self.cycle_count = 0
            logging.info(f"Display mode changed to {self.MODES[self.mode]}")
            self.update_display()

    def main_loop(self):
        """Get orders and acts on them."""
        while True:
            self.update_data()
            self.update_display()
            # waits this long checking for keypress
            self.check_for_input()
            # no need to sleep
            time.sleep(config.CONSOLE_LOOP_DELAY)
            # increment counter
            self.cycle_count += 1

    def get_this_party_started(self):
        """Get the party started."""
        logging.info(f'{self.whoami} starting.')
        time.sleep(1)
        self.update_display()
        self.draw_status_display()
        self.main_loop()

    def start(self):
        # call this inside of a curses wrapper to prevent
        # our screen from getting hosed when/if we exit
        try:
            curses.wrapper(self.get_this_party_started())
        except KeyboardInterrupt:
            curses.nocbreak()
            try:
                self.display.screen.keypad(False)
            except:
                pass
            curses.echo()
            curses.endwin()

def main():
    """Test the class."""
    import sys
    logging.basicConfig(filename=sys.stderr,
                        encoding='utf-8',
                        format='%(asctime)s %(levelname)s:%(message)s',
                        level=logging.DEBUG)
    console = Console()
    console.order_act_loop()


if __name__ == '__main__':
    main()
