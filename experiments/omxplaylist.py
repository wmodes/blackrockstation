#!/usr/bin/env python3
#
# Simple class-based media player to play media files in a playlist directory using Raspberry Pi's omxplayer.
#
# Original author @sabjorn
#   adapted from https://github.com/sabjorn/omxPlaylist
# Adapted and extended by @wmodes
#   https://github.com/wmodes/omxPlaylist

# import modules used here -- sys is a very standard one
import sys, argparse, logging, random

from os import listdir
from os.path import isfile, join, splitext

import subprocess

# for testing on the mac
import platform
if 'arm' in platform.platform().lower():
    omx_command = ['/usr/bin/omxplayer', "-p", "-o", "local"]
elif 'darwin' in platform.platform().lower():
    # afplay only plays audio, sadly. No equivalent of omxplayer
    omx_command = ['/usr/bin/afplay']

class OmxPlaylist(object):
    """Plays all of the media files in a directory with omxplayer."""

    def __init__(self, playlistdir=None, random=False, loop=False, autoplay=False, debug=False, omxoptions=[]):
        # constants - better to put in external config file
        self.support_formats = [".3g2", ".3gp", ".aac", ".aiff", ".alac", ".ape", ".avi", ".dsd", ".flac", ".m4a", ".mj2", ".mkv", ".mov", ".mp3", ".mp4", ".mpc", ".mpeg", ".mqa", ".ofr", ".ogg", ".opus", ".wav", ".wv"]
        # passed parameters
        self.playlistdir = playlistdir
        self.random = random
        self.loop = loop
        self.omxoptions = omxoptions
        self.autoplay = autoplay
        self.debug = debug
        # create playlist
        self.generatePlaylist()
        if autoplay:
            self.play()

    def play(self):
        # get started
        self.play_playlist()
        while self.loop:
            play_playlist()

    def generatePlaylist(self):
        inpath = self.playlistdir
        self.playlist = [f for f in listdir(inpath) if isfile(join(inpath, f)) and splitext(f)[1] in self.support_formats]

    def play_playlist(self):
        if self.random:
            random.shuffle(self.playlist)

        for f in self.playlist:
            full_path = self.playlistdir + "/" + f
            full_command = omx_command + self.omxoptions + [full_path]

            stdout = subprocess.PIPE
            if self.debug:
                stdout = False

            proc = None
            try:
                logging.debug("playing: {0}".format(full_path))
                proc = subprocess.run(full_command, check=True, stdin=subprocess.PIPE, stdout=stdout, close_fds=True)
            except KeyboardInterrupt:
                if proc is not None:
                    proc.kill()
                logging.info("Keyboard Interrupt")
                sys.exit()
            except Exception as e:
                logging.exception(e)


if __name__ == '__main__':
    # use argparse to specify options
    parser = argparse.ArgumentParser(
        description="Plays all of the media files in a directory with omxplayer.",
        epilog="As an alternative to the commandline, params can be placed in a file, one per line, and specified on the commandline like '%(prog)s @params.conf'.",
        fromfile_prefix_chars='@')
    parser.add_argument(
        '-l',
        '--loop',
        dest='loop', action='store_const',
        const=True, default=False,
        help='loop the playlist')
    parser.add_argument(
        '-r',
        '--random',
        dest='random', action='store_const',
        const=True, default=False,
        help='play playlist in random order')
    parser.add_argument(
        "directory",
        help="specify playlist directory",
        metavar="playlist_dir")
    parser.add_argument(
        "-d",
        "--debug",
        dest='debug', action='store_const',
        const=True, default=False,
        help="increase output verbosity")
    parser.add_argument(
        "-a",
        "--autoplay",
        dest='autoplay', action='store_const',
        const=True, default=False,
        help="start playing immediately")
    parser.add_argument(
        'remaining',
        help="catch all other arguments to be passed to OMXplayer",
        nargs=argparse.REMAINDER)
    args = parser.parse_args()

    # Setup logging
    if args.debug:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

    player = OmxPlaylist(args.directory, args.random, args.loop, args.autoplay, args.debug, args.remaining)
