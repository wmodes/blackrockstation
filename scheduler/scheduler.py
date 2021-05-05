"""Controller class for scheduler subsystem."""

from shared import config
from shared.controller import Controller

import logging
from pprint import pprint
from datetime import datetime, timedelta
import csv
from columnar import columnar
import time

logger = logging.getLogger()


class Scheduler(Controller):
    """Scheduler controller class."""

    def __init__(self):
        super(Scheduler, self).__init__()
        self.__read_schedule()
        self.__sort_schedule()
        self.__read_filetable()
        self.current_year = config.SCHED_YEARS[0]

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


    def __read_filetable(self):
        logging.info('Reading file table')
        self.filetable = {}
        with open(config.SCHED_FILE_TABLE, newline='') as csvfile:
            reader = csv.DictReader(csvfile, config.SCHED_FILE_FIELDS)
            # skips the header line
            next(reader)
            for row in reader:
                # skip blank lines
                if row['year'] != '':
                    # skip unregistered types
                    if row['type'] not in config.SCHED_TYPES:
                        logger.info(f"skipped unregistered type: {row['type']}")
                        continue
                    # add filename to filetable
                    index = f"{row['year']}-{row['type']}"
                    self.filetable[index] = row['filename']
            pprint(self.filetable)


    def status(self):
        """Brief one-liner status"""
        print("Scheduler is running.")


    def tail(f, window=1):
        """
        Returns the last `window` lines of file `f` as a list of bytes.
        """
        if window == 0:
            return b''
        BUFSIZE = 1024
        f.seek(0, 2)
        end = f.tell()
        nlines = window + 1
        data = []
        while nlines > 0 and end > 0:
            i = max(0, end - BUFSIZE)
            nread = min(end, BUFSIZE)
            f.seek(i)
            chunk = f.read(nread)
            data.append(chunk)
            nlines -= chunk.count(b'\n')
            end -= nread
        return b'\n'.join(b''.join(reversed(data)).splitlines()[-window:])


    def logs(self, num=config.SCHED_DEFAULT_LOG):
        """Recent log of activity"""
        with open(config.LOG_FILENAME, 'rb') as file:
            logs = tail(file, num).decode('utf-8')
        print(logs)


    def report(self):
        """Full multi-line readable report of activity"""
        self.status()
        self.logs(10)


    def future(self):
        pass


    def send_order_to_controller(self):
        pass


    def check_for_timeslip(self):
        pass


    def check_for_scheduled_train(self):
        pass


    def __receive_orders(self):
        """Receives orders"""
        order = self.comms.get_order()
        if not order:
            return None
        return order


    def __act_on_order(arg, order):
        """Takes action based on orders

        Possible comnmands:
            - *controller* *order*
            - request future [num_events]
            - request status
            - request log [num_events]
            - request report
        """
        if not order:
            return
        logging.debug(f"acting on order: {order}")
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
            self.status()
        #
        # request log
        #
        elif order.startswith("request log"):
            order_list = order.split()
            if len(order_list) > 2:
                self.logs(order_list[2])
            else:
                self.logs()
        #
        # request status
        #
        elif order.startswith("request report"):
            self.report()
        #
        # send order to other controller
        #
        elif list(filter(order.startswith, config.CONTROLLERS)) != []:
            self.send_order_to_controller(order)
        #
        # invalid order
        #
        else:
            logging.info(f"invalid order received: {order}")


    def order_act_loop(self):
        """Gets orders and acts on them"""
        while True:
            self.__act_on_order(self.__receive_orders())
            self.check_for_timeslip()
            self.check_for_scheduled_train()
            time.sleep(config.SCHED_LOOP_DELAY)


    def start(self):
        logging.info('Starting.')
        self.print_schedule()
        self.order_act_loop()


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
