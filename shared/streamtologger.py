# streamtologger - redirect writes to a logger
# author: Wes Modes <wmodes@gmail.com>
# date: Oct 2020
# license: MIT


class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """

    def __init__(self, logger, level):
        self.logger = logger
        self.level = level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            if line != '\n':
                self.logger.log(self.level, line.rstrip())

    def flush(self):
        pass
