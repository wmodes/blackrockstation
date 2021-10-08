"""Controller class for scheduler subsystem."""

from shared import config
from shared.controller import Controller

import logging
from pprint import pprint
from datetime import datetime, timedelta
import csv
from columnar import columnar
import time
import re
import random

# TODO: All reports and status should return objects to easily passs to source.

logger = logging.getLogger()

class Scheduler(Controller):
    """Scheduler controller class."""

    def __init__(self):
        """Initialize Scheduler class."""
        super().__init__()
        self.whoami = "scheduler"
        self.__read_schedule()
        self.__sort_schedule()
        self.delayed_events = []
        self.current_year = config.SCHED_YEARS[0]
        self.last_event = ""
        self.last_timeslip = datetime.now()

    """
        SETUP
    """

    def __read_schedule(self):
        logging.info('Reading schedule')
        self.schedule = []
        with open(config.SCHED_DATA, newline='') as csvfile:
            reader = csv.DictReader(csvfile,                    config.SCHED_FIELDS,restkey='Extras')
            # skips the header line
            next(reader)
            for row in reader:
                if row['event'] != '':
                    self.schedule.append(dict(row))


    def __sort_schedule(self):
        self.schedule = sorted(
            self.schedule, key=lambda k: time.strptime(k['time'], "%H:%M"))

    """
        REPORTS
    """

    def get_status(self):
        """Full status for controller."""
        return {
            "controller" : self.whoami,
            "running" : True,
            "currentYear" : self.current_year,
            "nextTrain" : self.get_next_train()
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
        now = datetime.now().time()
        for event in self.schedule:
            # if this event is not a train event, skip
            if event["controller"] != "train":
                continue
            # if this event is already in the past, skip
            if datetime.strptime(event["time"], "%H:%M").time() < now:
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
                if datetime.strptime(event["time"], "%H:%M").time() > now:
                    break
                # if we have n events, stop
                if len(future_list) >= n:
                    break
                future_list.append(event)
        return future_list
        #return self.display_train_schedule(future_list)

    def display_train_schedule(self, event_list=None):
        """Return human-readable schedule of future trains."""
        if not event_list:
            event_list = self.schedule
        headers = ['Train', 'Arrival', 'Var', 'Direction', 'Type', 'Notes']
        # convert dict to array of arrays
        events = []
        for event in event_list:
            if event['controller'] == "train":
                events.append([event['event'], event['time'],
                              event['variance'], event['direction'], event['traintype'], event['notes']])
        if not len(events):
            return
        #table = columnar(events, headers, terminal_width=100, column_sep='│', row_sep='─')
        table = columnar(events, headers, no_borders=True, terminal_width=110, wrap_max=8)
        #table = columnar(events, headers, terminal_width=110, column_sep='|', row_sep='─')
        return table

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
                results = self.get_future_trains(order["qty"])
            else:
                results = self.get_future_trains()
            return_val = {'status': 'OK',
                       'cmd': 'reqTrains',
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
                          'cmd': 'reqLogs',
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
            if order['controller'] not in config.CONTROLLERS:
                error = "invalid controller"
                logging.warning(error)
                return_val = {'status': 'FAIL',
                              'cmd': 'order',
                              'error': error,
                              'hint': config.CONTROLLERS}
                return return_val
            results = self.send_order_to_controller(
                order["controller"], order["relay"])
            return_val = {'status': results['status'],
                      'cmd': 'order',
                      'results': results}
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
                {'cmd': 'reqTrains',
                 'qty': '5'},
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
        return self.comms.send_order(controller, cmd_obj)

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
        now = datetime.now().time()
        for event in self.schedule:
            # if this event matches current time
            if now.strftime("%H:%M") == event["time"]:
                # if scheduled event already happened, return
                if self.last_event == event:
                    return
                # record this event as last_event
                self.last_event = event
                # make event happen
                if event['controller'] == "train":
                    self.trigger_train(event)
                else:
                    self.trigger_event(event)
                break


    def check_for_timeslip(self):
        """Check to see if it is time for a timeslip."""
        now = datetime.now()
        # prevent bounce: if the time in H:M is the same as the last timeslip, return
        if now.strftime("%H:%M") == self.last_timeslip.strftime("%H:%M"):
            return
        next_timeslip_min = self.last_timeslip + timedelta(minutes=config.SCHED_TIMESLIP_INTERVAL)
        next_timeslip_max = next_timeslip_min + timedelta(minutes=config.SCHED_TIME_DELTA)
        if next_timeslip_min < now < next_timeslip_max:
            # find out what the index of the current year is
            index = config.SCHED_YEARS.index(self.current_year)
            # increment one
            index += 1
            # make sure we don't have index overrun
            if index >= len(config.SCHED_YEARS):
                index = 0
            self.current_year = config.SCHED_YEARS[index]
            # record the time of the timeslip to prevent bounce
            self.last_timeslip = now
            self.trigger_timeslip()

    def check_for_delayed_events(self):
        """Check if it is time for delayed events."""
        now = datetime.now()
        now_delta = now + timedelta(minutes=config.SCHED_TIME_DELTA)
        for event in self.delayed_events:
            if now < event['time'] < now_delta:
                self.trigger_event(event)
                self.delayed_events.remove(event)

    def check_for_random_events(self):
        """
        Check if it is time for random events.

        Randomly calculate the chances of any of a list of events happening /right now/
        """
        denominator = 24 * 60 * 60 * (1/config.SCHED_LOOP_DELAY)
        for event in config.SCHED_PERIODIC:
            # an N in 345600 chance
            if random.random() < event["times_per_day"]/denominator:
                # lucky you! you get chosen!
                self.trigger_event(event)
                # only one winner at a time, thank you
                break

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
        """Constuct order and send to appropriate controller."""
        #TODO: Convert orders to objects
        if event['controller'] == "train":
            # send command to train controller
            #   form: set train *direction* *traintype* *year*
            order = {
                "cmd" : "setTrain",
                "direction" :  event['direction'],
                "traintype" : event['traintype'],
                "year" : self.current_year
            }
            self.comms.send_order("train", order)
        elif event['controller'] == "announce":
            # send command to announce controller
            #   form: set announce *id* *year*
            order = {
                "cmd" : "setAnnounce",
                "announceid" : event['announceid'],
                "year" : self.current_year
            }
            self.comms.send_order("announce", order)
        elif event['controller'] == "crossing":
            # send command to crossing controller
            #   form:
            #       set on
            #       set off
            if event['event'] == "on":
                order = {
                    "cmd" : "setOn"
                }
            elif event['event'] == "off":
                order = {
                    "cmd" : "setOff"
                }
            #TODO: Convert above to True/False?
            self.comms.send_order("crossing", order)
        elif event['controller'] == "signal":
            # send command to signal controller
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
            self.comms.send_order("signal", order)
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
            self.comms.send_order(event['controller'], order)

    def trigger_train(self, train_event):
        """
        Trigger the events that happen with a train.

        train_event comes from the schedule
        """
        # let's calculate the timing of some things to schedule the next few events
        now = datetime.now()
        # time_announce_arrival = now
        # time_signal_is_go = now
        time_we_hear_train = now +  timedelta(minutes=config.SCHED_BRIDGE_BEFORE)
        time_crossing_is_on = time_we_hear_train  + timedelta(minutes=config.SCHED_CROSSING_DELAY)
        time_departure_announce = time_we_hear_train + timedelta(minutes=float(train_event['duration'])/2)
        time_signal_is_stop = time_we_hear_train + timedelta(minutes=float(train_event['duration'])) - timedelta(minutes=config.SCHED_DEPART_TIME)
        time_crossing_is_off = time_we_hear_train + timedelta(minutes=float(train_event['duration'])) - timedelta(minutes=config.SCHED_CROSSING_DELAY)
        #
        # 1) SIGNAL turns green as soon as train enters the block
        #   i.e., several minutes before we can hear it
        self.trigger_event({
            "controller": "signal",
            "event": "go",
            "direction": train_event['direction']
        })
        #
        # 2) ANNOUNCE arrival when train approached station
        #   i.e., we when begin to hear it
        if train_event['announceid'] != "":
            self.delay_event({
                "controller": "announce",
                "announceid": train_event['announceid'] + "-arrival",
                "time": time_we_hear_train
            })
        #
        # 3) TRAINAUDIO starts
        train_event['time'] = time_we_hear_train
        self.delay_event(train_event)
        #
        # 4) CROSSING comes on as soon as train nears crossing
        #   i.e., some minutes after we can hear it
        self.delay_event({
            "controller": "crossing",
            "event": "on",
            "time": time_crossing_is_on
        })
        #
        # 5) ANNOUNCE departure before train leaves station
        #   i.e., halfway through duration
        if train_event['announceid'] != "":
            self.delay_event({
                "controller": "announce",
                "announceid": train_event['announceid'] + "-departure",
                "time": time_departure_announce
            })
        #
        # 6) SIGNAL turns red as soon as the train passes the station
        #   i.e., some minutes before end of duration
        self.delay_event({
            "controller": "signal",
            "event": "stop",
            "direction": train_event['direction'],
            "time": time_signal_is_stop
        })
        #
        # 7) CROSSING turns off as soon as the train passes
        # i.e., at the end of the train's duration
        self.delay_event({
            "controller": "crossing",
            "event": "off",
            "time": time_crossing_is_off
        })


    def trigger_timeslip(self):
        """Trigger a timeslip event and the things that go with it."""
        logging.info(f"Timeslip to {self.current_year}")
        # trigger glitch events and schedule year event
        for controller in ["radio", "television", "lights"]:
            self.trigger_event({
                "controller": controller,
                "event": "glitch"
            })
            self.delay_event({
                "controller": controller,
                "event": "year",
                "time": datetime.now() + timedelta(minutes=config.SCHED_TIMESLIP_GLITCH)
            })
        #pprint(self.delayed_events)

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
