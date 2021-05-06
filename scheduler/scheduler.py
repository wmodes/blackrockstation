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

logger = logging.getLogger()


class Scheduler(Controller):
    """Scheduler controller class."""

    def __init__(self):
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
            reader = csv.DictReader(csvfile, config.SCHED_FIELDS)
            # skips the header line
            next(reader)
            for row in reader:
                if row['event'] != '':
                    self.schedule.append(row)


    def __sort_schedule(self):
        self.schedule = sorted(
            self.schedule, key=lambda k: time.strptime(k['time'], "%H:%M"))

    """
        REPORTS
    """

    def full_report(self):
        """
        Full multi-line readable report of activity.
        """
        report = self.report_status() + "\n"
        report += self.report_current_year() + "\n\n"
        report += self.report_next_train() + "\n"
        report += self.report_logs(10) + "\n"
        return report

    def report_current_year(self):
        return (f"Current year is {self.current_year}.")

    def report_next_train(self):
        return (f"NEXT TRAIN\n==========\n{self.future_trains(1)}")

    def display_train_schedule(self, event_list=None):
        if not event_list:
            event_list = self.schedule
        headers = ['Train', 'Arrival', 'Var', 'Direction', 'Type', 'Notes']
        # convert dict to array of arrays
        events = []
        for event in event_list:
            if event['controller'] == "trainaudio":
                events.append([event['event'], event['time'],
                              event['variance'], event['direction'], event['traintype'], event['notes']])
        if not len(events):
            return
        #table = columnar(events, headers, terminal_width=100, column_sep='│', row_sep='─')
        table = columnar(events, headers, no_borders=True, terminal_width=110, wrap_max=8)
        #table = columnar(events, headers, terminal_width=110, column_sep='|', row_sep='─')
        return table

    def future_trains(self, n=10):
        future_list = []
        # search through train schedule for time that matches H:M
        now = datetime.now().time()
        for event in self.schedule:
            # if this event is not a train event, skip
            if event["controller"] != "trainaudio":
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
                if event["controller"] != "trainaudio":
                    continue
                # if this event is not in the past, stop (i.e., we've wrapped around)
                if datetime.strptime(event["time"], "%H:%M").time() > now:
                    break
                # if we have n events, stop
                if len(future_list) >= n:
                    break
                future_list.append(event)
        return self.display_train_schedule(future_list)

    """
        ORDERS
    """

    def __act_on_order(arg, order):
        """
        Takes action based on orders

        Possible comnmands:
            - *controller* *order*
            - request future [num_events]
            - request status
            - request log [num_events]
            - request report
        """
        if not order:
            return
        logging.debug(f"Acting on order: {order}")
        #
        # request future schedule
        #
        if order.startswith("request future"):
            order_list = order.split()
            if len(order_list) > 2:
                self.future(order_list[2])
            else:
                self.future()
        #
        # request status
        #
        elif order.startswith("request status"):
            self.report_status()
        #
        # request log
        #
        elif order.startswith("request log"):
            order_list = order.split()
            if len(order_list) > 2:
                self.report_logs(order_list[2])
            else:
                self.report_logs()
        #
        # request status
        #
        elif order.startswith("request report"):
            self.full_report()
        #
        # send order to other controller
        #
        elif list(filter(order.startswith, config.CONTROLLERS)) != []:
            order_list = order.split()
            controller = order_list.pop(0)
            order = ' '.join(order_list)
            self.send_order_to_controller(controller, order)
        #
        # invalid order
        #
        else:
            logging.info(f"invalid order received: {order}")


    def send_order_to_controller(self, controller, command):
        """
        Send an arbitrary order to another controller.
        """
        self.comms.send_order(controller, command)

    """
        TIME CHECKS
    """

    def check_for_scheduled_event(self):
        """
        check for scheduled event and send command to appropriate controller. Matches now() in H:M format with train schedule arrival time and records last event to prevent bounce. Note: Two events shouldn't share the same time.
        """
        # TODO: Implement variance
        # search through train schedule for time that matches H:M
        now = datetime.now().time()
        for event in self.schedule:
            # if this event matches current time
            if now.strftime("%H:%M") == event["time"]:
                # if scheduled event already happened, return
                if self.last_event == event['event'] + event["time"]:
                    return
                # record this event as last_event
                self.last_event = event['event'] + event["time"]
                # make event happen
                self.trigger_event(event)
                break


    def check_for_timeslip(self):
        now = datetime.now()
        # prevent bounce: if the time in H:M is the same as the last timeslip, return
        if now.strftime("%H:%M") == self.last_timeslip.strftime("%H:%M"):
            return
        next_timeslip_min = self.last_timeslip + timedelta(minutes=config.SCHED_TIMESLIP_INTERVAL)
        next_timeslip_max = next_timeslip_min + timedelta(minutes=config.SCHED_TIMESLIP_DELTA)
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

    def delay_event(self, event):
        self.delayed_events.append(event)

    def check_for_delayed_events(self):
        now = datetime.now()
        now_delta = now + timedelta(minutes=config.SCHED_TIMESLIP_DELTA)
        for event in self.delayed_events:
            if now < event['time'] < now_delta:
                self.trigger_event(event)
                self.delayed_events.remove(event)

    def check_for_random_events(self):
        """
        randomly calculate the chances of any of a list of events happening /right now/
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

    def trigger_event(self, event):
        """
        Constuct order and send to appropriate controller.
        """
        if event['controller'] == "trainaudio":
            # send command to trainaudio controller
            #   form: set train *direction* *traintype* *year*
            order = f"set train {event['direction']} {event['traintype']} {self.current_year}"
            self.comms.send_order("trainaudio", order)
        elif event['controller'] == "announce":
            # send command to announce controller
            #   form: set announce *id* *year*
            order = f"set announce {event['announceid']} {self.current_year}"
            self.comms.send_order("announce", order)
        elif re.search('radio|television|lights', event['controller']):
            # send command to radio, tv, or lights controller
            #   form:
            #       set glitch
            #       set year *year*
            if event['event'] == "glitch":
                order = "set glitch"
            elif event['event'] == "year":
                order = f"set year {self.current_year}"
            else:
                return
            self.comms.send_order(event['controller'], order)

    def trigger_timeslip(self):
        logging.info(f"Timeslip to {self.current_year}")
        print(f"Timeslip to {self.current_year}")
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
        """Gets orders and acts on them"""
        while True:
            self.__act_on_order(self.receive_order())
            self.check_for_delayed_events()
            self.check_for_timeslip()
            self.check_for_random_events()
            self.check_for_scheduled_event()
            time.sleep(config.SCHED_LOOP_DELAY)


    def start(self):
        logging.info('Starting.')
        print(self.full_report())
        self.trigger_timeslip()
        self.main_loop()



def main():
    """For testing the class"""
    import sys
    logging.basicConfig(filename=sys.stderr,
                        encoding='utf-8',
                        format='%(asctime)s %(levelname)s:%(message)s',
                        level=logging.DEBUG)
    logger = logging.getLogger()
    scheduler = Scheduler()
    scheduler.order_act_loop()


if __name__ == '__main__':
    main()
