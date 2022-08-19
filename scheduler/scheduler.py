"""Controller class for scheduler subsystem."""

from shared import config
from shared.controller import Controller

import logging
from datetime import datetime, timedelta
import csv
from columnar import columnar
import time
import re
import random
import shutil
from curses import wrapper
import pprint

logger = logging.getLogger()
logger.setLevel(config.LOG_LEVEL)

class Scheduler(Controller):
    """Scheduler controller class."""

    def __init__(self):
        """Initialize Scheduler class."""
        super().__init__()
        self.whoami = "scheduler"
        #
        # get event schedule
        self.schedule = []
        self.__read_schedule(self.schedule)
        self.__sort_schedule(self.schedule)
        logging.debug("Schedule:")
        logging.debug(pprint.pformat(self.schedule))
        #
        # get list of audio files
        self.train_file_table = {}
        self.__read_train_file_table(self.train_file_table)
        logging.debug("train_file_table:");
        logging.debug(pprint.pformat(self.train_file_table))
        #
        # get list of announcements
        self.train_announce_files = {}
        self.periodic_announce_events = {}
        self.__read_announce_table(self.train_announce_files, self.periodic_announce_events)
        logging.debug("train_announce_files:");
        logging.debug(pprint.pformat(self.train_announce_files))
        logging.debug("periodic_announce_events:");
        logging.debug(pprint.pformat(self.periodic_announce_events))
        #
        # internal tracking stuff
        self.delayed_events = []
        self.current_year = config.YEARS[0]
        self.last_event = ""
        self.last_timeslip = datetime.now()
        self.cycle_count = 0

    """
        SETUP
    """

    def __read_schedule(self, schedule):
        logging.info('Reading schedule')
        with open(config.SCHED_DATA, newline='') as csvfile:
            reader = csv.DictReader(csvfile,                    config.SCHED_FIELDS, restkey='Extras')
            # skips the header line
            next(reader)
            for row in reader:
                if row['event'] != '':
                    schedule.append(dict(row))

    def __sort_schedule(self, schedule):
        schedule = sorted(
            schedule, key=lambda k: time.strptime(k['time'], "%H:%M"))
        for index in range(len(schedule)):
            schedule[index]["index"] = index

    def __read_train_file_table(self, train_file_table):
        """Read train_file_table into memory."""
        logging.info('Reading file table')
        with open(config.SCHED_TRAIN_FILE_TABLE, newline='') as csvfile:
            reader = csv.DictReader(csvfile, config.SCHED_TRAIN_FILE_FIELDS)
            # skips the header line
            next(reader)
            for row in reader:
                # skip blank lines
                if row['year'] == '':
                    continue
                # add filename to train_file_table
                index = f"{row['year']}-{row['traintype']}"
                train_file_table[index] = {
                    'year': row['year'],
                    'traintype': row['traintype'],
                    'filename': row['filename'],
                    'duration': row['duration']
                }

    def __read_announce_table(self, train_files, periodic_events):
        """Create two file dicts based on a CSV file with lists of possible announcements."""
        logging.info('Reading file table')
        with open(config.SCHED_ANNOUNCE_FILE_TABLE, newline='') as csvfile:
            reader = csv.DictReader(csvfile, config.SCHED_ANNOUNCE_FILE_FIELDS)
            # skips the header line
            next(reader)
            for row in reader:
                # skip blank lines
                if row['announcement'] == '':
                    continue;
                if row['type'] == "train":
                    # create a dict of announcement files indexed by id
                    index = row['announceid']
                    train_files[index] = row['filename']
                elif row['type'] == "periodic":
                    # create a dict of lists indexed by year
                    year = row['year']
                    if year not in periodic_events:
                        periodic_events[year] = []
                    event = {
                        'controller': 'announce',
                        'announcement': row['announcement'],
                        'times_per_day': row['times_per_day'],
                        'announceid': row['announceid'],
                        'filename': row['filename'],
                        'notes': row['notes']
                    }
                    periodic_events[year].append(event)


    """
        REPORTS
    """

    def get_status(self):
        """Full status for controller."""
        return {
            "controller" : self.whoami,
            "running" : True,
            "currentYear" : self.current_year,
            "nextTrain" : self.get_next_train(),
            "nextTimeslip" : self.next_timeslip()
        }

    def get_next_train(self):
        """Return an obj representing next train."""
        return self.get_future_trains(1)[0]

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
            future_list.append(event)
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
                future_list.append(event)
        return future_list

    def display_future_trains(self, n=10):
        """Return human-readable schedule of future trains."""
        event_list = self.get_future_trains(n)
        headers = ['Train', 'Arrival', 'Direction', 'Type', 'Notes']
        # convert dict to array of arrays
        events = []
        for event in event_list:
            if event['controller'] == "train":
                events.append([event['event'], event['time'],
                              event['direction'], event['traintype'], event['notes']])
        if not len(events):
            return
        width = shutil.get_terminal_size().columns - 2
        table = columnar(events, headers, no_borders=True, wrap_max=8, terminal_width=width)
        return str(table)

    def display_train_schedule(self, event_list=None):
        """Return human-readable schedule of all trains."""
        if not event_list:
            event_list = self.schedule
        headers = ['Train', 'Arrival', 'Direction', 'Type', 'Notes']
        # convert dict to array of arrays
        events = []
        for event in event_list:
            if event['controller'] == "train":
                events.append([event['event'], event['time'], event['direction'], event['traintype'], event['notes']])
        if not len(events):
            return
        #table = columnar(events, headers, terminal_width=100, column_sep='│', row_sep='─')
        table = columnar(events, headers, no_borders=True, terminal_width=110, wrap_max=8)
        #table = columnar(events, headers, terminal_width=110, column_sep='|', row_sep='─')
        return str(table)

    """
        ORDERS
    """

    def act_on_order(self, order):
        """
        Take action based on orders.

        Possible comnmands:
            - order *controller* *order*
            - reqTrains [num_events]
            - reqStatus
            - reqLog [num_events]
        """
        if not order:
            error = "No command received"
            return_val = {'status': 'FAIL',
                          'error': error}
            return return_val
        if "cmd" not in order:
            error = f"No 'cmd' in order received: '{order}'"
            logging.info(error)
            return_val = {'status': 'FAIL',
                          'error': error}
            return return_val
        #
        # request future schedule
        # Format: {
        #   "cmd" : "reqTrains",
        #   "qty" : **integer**
        # }
        #
        if order['cmd'].lower() == "reqtrains":
            if "qty" in order:
                results = self.get_future_trains(int(order["qty"]))
            else:
                results = self.get_future_trains()
            return_val = {'status': 'OK',
                       'cmd': 'reqTrains',
                       'results': results}
            return return_val
        #
        # request full train schedule
        # Format: {
        #   "cmd" : "reqAllTrains"
        # }
        #
        if order['cmd'].lower() == "reqalltrains":
            results = self.schedule
            return_val = {'status': 'OK',
                       'cmd': 'reqAllTrains',
                       'results': results}
            return return_val
        #
        # request status
        # Format: {
        #   "cmd" : "reqStatus"
        # }
        #
        elif order['cmd'].lower() == "reqstatus":
            return_val = {'status': 'OK',
                       'cmd': 'reqStatus',
                       'results': self.get_status()}
            return return_val
        #
        # request log
        # Format: {
        #   "cmd" : "reqLog",
        #   "qty" : **integer**
        # }
        #
        elif order['cmd'].lower() == "reqlog":
            if "qty" in order:
                results = self.get_logs(order["qty"])
            else:
                results = self.get_logs()
            return_val = {'status': 'OK',
                          'cmd': 'reqLog',
                          'results': results}
            return return_val
        #
        # send order to other controller
        # Format: {
        #   "cmd" : "order",
        #   "controller" : **str**,
        #   "relay" : **order**
        # }
        elif order['cmd'].lower() == "order":
            if "controller" not in order or "relay" not in order:
                error = "controller or relay values missing"
                logging.warning(error)
                return_val = {'status': 'FAIL',
                              'cmd': 'order',
                              'error': error}
                return return_val
            if order['controller'] not in list(config.CONTROLLERS):
                error = "invalid controller"
                logging.warning(error)
                return_val = {'status': 'FAIL',
                              'cmd': 'order',
                              'error': error,
                              'hint': list(config.CONTROLLERS)}
                return return_val
            results = self.send_order_to_controller(
                order["controller"], order["relay"])
            return_val = {'status': results['status'],
                      'cmd': 'order',
                      'results': results}
            return return_val
        #
        # set year
        # Format: {
        #   "cmd" : "setYear",
        #   "year" : *year*
        # }
        #
        elif order['cmd'].lower() == "setyear":
            if "year" not in order:
                error = "No year in order received"
                logging.warning(error)
                return_val = {'status': 'FAIL',
                              'cmd': 'setYear',
                              'error': error}
                return return_val
            return_val = self.set_year(order['year'])
            return return_val
        #
        # set train
        # Format: {
        #   "cmd" : "setTrain",
        #   "index" : *int*
        # }
        #
        elif order['cmd'].lower() == "settrain":
            if "index" not in order:
                error = "No index in order received"
                logging.warning(error)
                return_val = {'status': 'FAIL',
                              'cmd': 'setTrain',
                              'error': error}
                return return_val
            if order["index"] < 0 or order["index"] > len(self.schedule) - 1:
                error = f"Index in order invalid: {index}"
                logging.warning(error)
                return_val = {'status': 'FAIL',
                              'cmd': 'setTrain',
                              'error': error}
                return return_val
            self.set_train(order['index'])
            return_val = {'status': 'OK',
                          'cmd': 'setTrain'}
            return return_val
        #
        # help
        #
        elif order['cmd'].lower() == "help":
            cmds = [
                {'cmd': 'order',
                 'controller': ["announce", "crossing", "lights", "radio", "scheduler", "bridge",
                 "train", "television"],
                 'order': {'cmd': 'reqStatus'}},
                {'cmd': 'setTrain',
                 'index': 7},
                {'cmd': 'setYear',
                 'year': ['1858', '1888', '1938', '1959', '1982', '2014', '2066', '2110']},
                {'cmd': 'reqTrains',
                 'qty': '5'},
                {'cmd': 'reqAllTrains'},
                {'cmd': 'reqStatus'},
                {'cmd': 'reqLog',
                 'qty': '10'}
            ]
            return_val = {'status': 'OK',
                          'cmd': 'help',
                          'commands': cmds}
            return return_val
        #
        # invalid order
        #
        else:
            error = "invalid order received"
            logging.warning(error + ': ' + order['cmd'])
            return_val = {'status': 'FAIL',
                          'cmd': order['cmd'],
                          'error': error}
            return return_val


    def send_order_to_controller(self, controller, cmd_obj):
        """Send an arbitrary order to another controller."""
        now_dt = datetime.now()
        results = self.comms.send_order(controller, cmd_obj)
        if results["status"] == 'FAIL':
            logging.warning(f"order to {controller} failed: {results['error']}")
        return results


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

    def next_train(self):
        time_str = self.get_next_train()["time"]
        next_dt = self.str2dt(time_str)
        now_dt = datetime.now()
        time_delta = next_dt - now_dt
        secs = time_delta.total_seconds()
        hrs = int(secs // 3600)
        mins = int((secs % 3600) // 60)
        secs = int(secs % 60)
        return f"{hrs}:{mins:02d}:{secs:02d}"

    def next_timeslip(self):
        next = self.last_timeslip + timedelta(minutes=config.SCHED_TIMESLIP_INTERVAL)
        now_dt = datetime.now()
        time_delta = next - now_dt
        min = int(time_delta.total_seconds() // 60)
        sec = int(time_delta.total_seconds() % 60)
        return f"{min}:{sec:02d}"

    """
        TIME CHECKS
    """

    def check_for_scheduled_event(self):
        """
        Check for scheduled event and send command to appropriate controller.

        Matches now() in H:M format with train schedule arrival time and records last event to prevent bounce. Note: Two events shouldn't share the same time.
        """
        # TODO: Implement variance
        # search through train schedule for time that matches H:M
        now_t = datetime.now().time()
        for event in self.schedule:
            # if this event matches current time
            if now_t.strftime("%H:%M") == event["time"]:
                # if scheduled event already happened, return
                if self.last_event == event:
                    return
                # record this event as last_event
                self.last_event = event
                # make event happen
                if event['controller'] == "train":
                    self.add_extra_train_info(event)
                    self.trigger_train(event)
                else:
                    self.trigger_event(event)
                break

    def check_for_timeslip(self):
        """Check to see if it is time for a timeslip."""
        now_dt = datetime.now()
        # prevent bounce: if the time in H:M is the same as the last timeslip, return
        if now_dt.strftime("%H:%M") == self.last_timeslip.strftime("%H:%M"):
            return
        next_timeslip = self.last_timeslip + timedelta(minutes=config.SCHED_TIMESLIP_INTERVAL)
        if now_dt > next_timeslip:
            self.trigger_timeslip()

    def check_for_delayed_events(self):
        """Check if it is time for delayed events."""
        now_dt = datetime.now()
        for event in self.delayed_events:
            # logging.debug(f"Delayed event: Now: {now_dt.strftime('%H:%M:%S')}, Time: {event['time_dt'].strftime('%H:%M:%S')}, Delta: {now_delta.strftime('%H:%M:%S')}")
            if now_dt > event['time_dt']:
                self.trigger_event(event)
                self.delayed_events.remove(event)

    def check_for_random_events(self):
        """
        Check if it is time for random events.

        Randomly calculate the chances of any of a list of events happening /right now/
        """
        # # calculate number of dice rolls in a day / faces on die
        # die_faces = 24 * 60 * 60 * (1/config.SCHED_LOOP_DELAY)
        # # roll the dice
        # dice_results = random.random() * die_faces
        # # set an index
        # index = 0
        # # logging.debug(f"Looking at {len(self.periodic_announce_events[self.current_year])} periodic events for {self.current_year}")
        # # figure out which event (if any) the dice indicate
        # for event in self.periodic_announce_events[self.current_year]:
        #     # examaine a range at the low end of the possible die_faces
        #     min = index
        #     max = index + int(event['times_per_day'])
        #     # logging.debug(f"Event between {min} and {max}: {event}")
        #     if dice_results >=min and dice_results <= max:
        #         # lucky you! you get chosen!
        #         logging.debug("announce event chosen:")
        #         logging.debug(pprint.pformat(event))
        #         self.trigger_event(event)
        #         # only one winner at a time, thank you
        #         break
        #     index += int(event['times_per_day'])
        #
        denominator = 24 * 60 * 60 * (1/config.SCHED_LOOP_DELAY)
        for event in config.SCHED_PERIODIC:
            # an N in 345600 chance
            if random.random() < event["times_per_day"]/denominator:
                # lucky you! you get chosen!
                self.trigger_event(event)
                # only one winner at a time, thank you
                break

    """
        PLAY STUFF
    """

    def set_year(self, year):
        """Set year attribute."""
        logging.info(f"Setting year: {year}")
        if str(year) not in config.VALID_YEARS:
            error = f"Invalid year: {year}"
            logging.warning(error)
            return_val = {'status': 'FAIL',
                          'error': error}
            return return_val
        self.trigger_timeslip(year)
        return_val = {'status': 'OK',
                      'cmd': 'setYear'}
        return return_val

    def set_train(self, index):
        event = self.schedule[index]
        if event['controller'] == "train":
            self.add_extra_train_info(event)
            self.trigger_train(event)
        else:
            self.trigger_event(event)

    """
        EVENTS
    """

    def delay_event(self, event):
        """
        Add an event to the delayed queue.

        The time is a key within the object.
        """
        self.delayed_events.append(event)

    def trigger_event(self, event):
        """Constuct order from basic event info and send to appropriate controller."""
        if event['controller'] == "train":
            # send command to train controller
            #   form: set train *direction* *traintype* *year*
            order = {
                "cmd" : "setTrain",
                "direction" :  event['direction'],
                "traintype" : event['traintype'],
                "year" : self.current_year
            }
            self.send_order_to_controller("train", order)
        elif event['controller'] == "announce":
            # send command to announce controller
            #   form: set announce *id* *year*
            order = {
                "cmd" : "setAnnounce",
                "announceid" : event['announceid']
            }
            self.send_order_to_controller("announce", order)
        elif event['controller'] == "crossing":
            # send command to crossing controller
            #   form:
            #       set on
            #       set off
            if event['event'] == "on":
                order = {
                    "cmd" : "stateOn"
                }
            elif event['event'] == "off":
                order = {
                    "cmd" : "stateOff"
                }
            #TODO: Convert above to True/False?
            self.send_order_to_controller("crossing", order)
        elif event['controller'] == "bridge":
            # send command to bridge controller
            #   form:
            #       set go *direction*
            #       set stop
            if event['event'] == "stop":
                order = {
                    "cmd" : "setStop"
                }
            elif event['event'] == "go":
                order = {
                    "cmd" : "setGo",
                    "direction" : event['direction']
                }
            self.send_order_to_controller("bridge", order)
        elif re.search('radio|television|lights', event['controller']):
            # send command to radio, tv, or lights controller
            #   form:
            #       set glitch
            #       set year *year*
            if event['event'] == "glitch":
                order = {
                    "cmd" : "setGlitch"
                }
            elif event['event'] == "year":
                order = {
                    "cmd" : "setYear",
                    "year" : self.current_year
                }
            else:
                return
            self.send_order_to_controller(event['controller'], order)

    def add_extra_train_info(self, train_event):
        train_event['year'] = self.current_year
        index = f"{self.current_year}-{train_event['traintype']}"
        train_event['duration'] = self.train_file_table[index]['duration']

    def trigger_train(self, train_event):
        """
        Trigger the events that happen with a train.

        train_event comes from the schedule
        duration comes from the train_file_table

        train_event: {
            'time_dt': time_dt,
            'direction': direction,
            'traintype': traintype,
            'announceid': announceid,
            'year': current_year,
            'duration': duration
        }
        """
        logging.debug("Here's what that event looks like:");
        logging.debug(pprint.pformat(train_event));
        # let's calculate the timing of some things to schedule the next few events
        now_dt = datetime.now()
        # time_announce_arrival = now_dt
        # time_signal_is_go = now_dt
        time_we_hear_train = now_dt + \
            timedelta(seconds=config.SCHED_BRIDGE_DELAY_ON_SEC)
        time_crossing_is_on = time_we_hear_train  + \
            timedelta(seconds=config.SCHED_CROSSING_DELAY_SEC)
        time_departure_announce = time_we_hear_train + \
            timedelta(seconds=float(train_event['duration'])) - timedelta(seconds=config.SCHED_BOARDING_ANNOUNCE_SEC)
        time_signal_is_stop = time_we_hear_train + \
            timedelta(seconds=float(train_event['duration'])) - timedelta(seconds=config.SCHED_BRIDGE_DELAY_OFF_SEC)
        time_crossing_is_off = time_we_hear_train + \
            timedelta(seconds=float(train_event['duration'])) - timedelta(seconds=config.SCHED_CROSSING_DELAY_SEC)
        logging.debug(f"duration: {train_event['duration']}")
        logging.debug(f"time_we_hear_train: {time_we_hear_train}")
        logging.debug(f"time_crossing_is_on: {time_crossing_is_on}")
        logging.debug(f"time_departure_announce: {time_departure_announce}")
        logging.debug(f"time_signal_is_stop: {time_signal_is_stop}")
        logging.debug(f"time_crossing_is_off: {time_crossing_is_off}")
        #
        # 1) BRIDGE signal turns green as soon as train enters the
        #   block, i.e., several minutes before we can hear it
        self.delay_event({
            "controller": "bridge",
            "event": "go",
            "direction": train_event['direction'],
            "time_dt": datetime.now() + timedelta(seconds=1)
        })
        #
        # 2) ANNOUNCE arrival as train is approaching station
        #   i.e., we when begin to hear it
        if train_event['announceid'] != "":
            self.delay_event({
                "controller": "announce",
                "announceid": f"{self.current_year}-{train_event['announceid']}-announce-arrival",
                "time_dt": datetime.now() + timedelta(seconds=15)
            })
        #
        # 3) TRAINAUDIO starts
        train_event['time_dt'] = time_we_hear_train
        self.delay_event(train_event)
        #
        # 4) CROSSING comes on as soon as train nears crossing
        #   i.e., some minutes after we can hear it
        self.delay_event({
            "controller": "crossing",
            "event": "on",
            "time_dt": time_crossing_is_on
        })
        #
        # 5) ANNOUNCE departure before train leaves station
        #   i.e., about 2 monutes before it is gone
        if train_event['announceid'] != "":
            self.delay_event({
                "controller": "announce",
                "announceid": f"{self.current_year}-{train_event['announceid']}-announce-departure",
                "time_dt": time_departure_announce
            })
        #
        # 6) BRIDGE signal turns red as soon as the train passes the
        #   station, i.e., some minutes before end of duration
        self.delay_event({
            "controller": "bridge",
            "event": "stop",
            "direction": train_event['direction'],
            "time_dt": time_signal_is_stop
        })
        #
        # 7) CROSSING turns off as soon as the train passes
        # i.e., at the end of the train's duration
        self.delay_event({
            "controller": "crossing",
            "event": "off",
            "time_dt": time_crossing_is_off
        })


    def trigger_timeslip(self, year=None):
        """Trigger a timeslip event and the things that go with it."""
        if year:
            self.current_year = year;
        else:
            # # find out what the index of the current year is
            # index = config.YEARS.index(int(self.current_year))
            # # increment one
            # index += 1
            # # make sure we don't have index overrun
            # if index >= len(config.YEARS):
            #     index = 0
            # self.current_year = config.YEARS[index]
            #
            # now we pick years at random, but prevent a repeat
            new_year = self.current_year
            while new_year == self.current_year:
                new_year = random.choice(config.YEARS)
            self.current_year = new_year
        # record the time of the timeslip to prevent bounce
        self.last_timeslip = datetime.now()
        logging.info(f"Timeslip to {self.current_year}")
        # trigger glitch events and schedule year event
        for controller in ["radio", "television", "lights"]:
            self.delay_event({
                "controller": controller,
                "event": "glitch",
                "time_dt": datetime.now() + timedelta(seconds=1)
            })
            self.delay_event({
                "controller": controller,
                "event": "year",
                "time_dt": datetime.now() + timedelta(seconds=config.SCHED_TIMESLIP_GLITCH)
            })


    """
        MAIN LOOP
    """

    def main_loop(self):
        """Get orders and acts on them."""
        while True:
            self.act_on_order(self.receive_order())
            self.check_for_delayed_events()
            self.check_for_timeslip()
            self.check_for_random_events()
            self.check_for_scheduled_event()
            time.sleep(config.SCHED_LOOP_DELAY)

    def start(self):
        """Get the party started."""
        logging.info('Starting.')
        time.sleep(1)
        self.trigger_timeslip()
        self.main_loop()

def main():
    """Test the class."""
    import sys
    logging.basicConfig(filename=sys.stderr,
                        encoding='utf-8',
                        format='%(asctime)s %(levelname)s:%(message)s',
                        level=logging.DEBUG)
    scheduler = Scheduler()
    scheduler.order_act_loop()


if __name__ == '__main__':
    main()
