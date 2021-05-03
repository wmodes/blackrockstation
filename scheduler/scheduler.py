"""Controller class for scheduler subsystem."""

from shared import config
from shared.controller import Controller

import logging
import pprint
from datetime import datetime, timedelta
import csv
import time
from columnar import columnar

logger = logging.getLogger()


class Scheduler(Controller):
    """Scheduler controller class."""

    def __init__(self):
        super(Scheduler, self).__init__()
        self.__read_schedule()
        self.__sort_schedule()

    def __read_schedule(self):
        logging.info('Reading schedule.')
        self.schedule = []
        with open(config.SCHED_DATA, newline='') as csvfile:
            reader = csv.DictReader(csvfile, config.SCHED_FIELDS)
            for row in reader:
                if row['event'] != '':
                    self.schedule.append(row)
            del self.schedule[0]

    def __sort_schedule(self):
        self.schedule = sorted(
            self.schedule, key=lambda k: time.strptime(k['arrival'], "%H:%M"))

    def print_schedule(self):
        sched = self.schedule
        headers = ['Train', 'Arrival', 'Variance', 'Direction', 'Type']
        # convert dict to array of arrays
        events = []
        for event in self.schedule:
            events.append([event['event'], event['arrival'],
                          event['variance'], event['direction'], event['type']])
        #table = columnar(events, headers, terminal_width=100, column_sep='│', row_sep='─')
        table = columnar(events, headers, no_borders=True, terminal_width=100)
        print(table)

    def status(self):
        """Brief one-liner status"""
        pass

    def logs(self):
        """Recent log of activity"""
        pass

    def report(self):
        """Full multi-line readable report of activity"""
        pass

    def __receive_orders(self):
        """Receives orders"""
        pass

    def __ack_orders(self):
        """Acknowledges orders received"""

    def __act_on_orders(arg, orders):
        """Takes action based on orders"""
        pass

    def order_act_loop(self):
        """Gets orders and acts on them"""
        pass

    def start(self):
        print("Scheduler: starting")
        logging.info('Starting.')
        self.print_schedule()

    def stop(self):
        logging.info('Stopping.')
        pass


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
