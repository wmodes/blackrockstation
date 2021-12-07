#!/usr/bin/env python3
#
# Simple threaded media player to play media files in a playlist directory using Raspberry Pi's omxplayer.
#
# Original author @sabjorn
#   adapted from https://github.com/sabjorn/omxPlaylist
# Adapted and extended by @wmodes
#   https://github.com/wmodes/omxPlaylist

# from omxplaylist import OmxPlaylist

import sys, argparse, logging, random, signal

from os import listdir
from os.path import isfile, join, splitext

import subprocess

import threading
from time import sleep

# player = "/home/pi/blackrockstation/omxplaylist/omxplaylist.py"
# opt = ["--loop", "--random"]
# playlist = "/home/pi/blackrockstation/experiments/audio/playlist/"
# cmd = [player] + opt + [playlist]

# for testing on the mac
import platform
if 'arm' in platform.platform().lower():
    omx_command = ['/usr/bin/omxplayer', "-p", "-o", "local"]
elif 'darwin' in platform.platform().lower():
    # afplay only plays audio, sadly. No equivalent of omxplayer
    omx_command = ['/usr/bin/afplay']

class MediaThread(threading.Thread):
    """
    Threaded media player.

    Thinking about how I want to use this thing. I want to be able to:
        * Use it like VLC
        * Instantiate one instance of this
        * Send it playlists, and have it start playing
        * Stop it when I want

    Behind the scenes, that means it will have to:
        * Start a threaded player
        * Kill the old thread when I give it a new playlist
    """

    def __init__(self, playlistdir=None, random=False, loop=False, autoplay=False, debug=False, options=[]):
        # constants - better to put in external config file
        self.support_formats = [".3g2", ".3gp", ".aac", ".aiff", ".alac", ".ape", ".avi", ".dsd", ".flac", ".m4a", ".mj2", ".mkv", ".mov", ".mp3", ".mp4", ".mpc", ".mpeg", ".mqa", ".ofr", ".ogg", ".opus", ".wav", ".wv"]
        # super(MediaThread, self).__init__()
        # # WTF does this do? I honestly don't know.
        # self._stop_event = threading.Event()
        # passed parameters
        self.playlistdir = playlistdir
        self.random = random
        self.loop = loop
        self.autoplay = autoplay
        self.debug = debug
        self.options = options
        # internal flags and vars
        self._playlist_index = 0
        self._thread_obj = None
        self._thread_pgid = None
        # if this is a new playlist, create it
        if playlistdir:
            self._new_playlist()
        if self.autoplay:
            self.play()

    def play(self, playlistdir=None, random=None, loop=None, debug=None):
        """Start the player with or without a specified playlist."""
        #
        # All options are optional. player.play() will start existing
        # playlist if there is one.
        #
        # Or you can specify a new playlist.
        #
        # There is no autoplay option, because player.play() will start
        # playing immediately.
        #
        # optional passed parameters
        if playlistdir != None:
            self.playlistdir = playlistdir
        if random != None:
            self.random = random
        if loop != None:
            self.loop = loop
        if debug != None:
            self.debug = debug
        # kill the player if we have one
        self._stop_player()
        # if this is a new playlist, create it
        if playlistdir:
            self._new_playlist()
        # start the new player
        self._play_playlist()

    def _new_playlist(self):
        """Generate a list of files in the playlistdir folder, in random order if necessary."""
        inpath = self.playlistdir
        self.playlist = [f for f in listdir(inpath) if isfile(join(inpath, f)) and splitext(f)[1] in self.support_formats]
        self._playlist_index = 0
        if self.random:
            random.shuffle(self.playlist)

    def stop(self):
        self._stop_player()

    def _play_playlist(self):
        """Handle playing playlists."""
        #
        # Under what conditions might we get here?
        #     * No playlist has been defined (unlikely)
        #     * It is a brand new playlist and we need to play it
        #     * Previous play was interrupted, and now we just need to resume
        #
        # What needs to happen?
        #     * Shuffle a new playlist if random is True
        #     * Work through playlist starting a threaded external player
        #       for each media file
        #     * Check for new flags triggering a stop or new playlist
        #     * Check for end of currently playing media file
        #     * Start new media file if ready
        #     * If at end of playlist and if loop is True, start all over
        #
        # rare case of no playlist
        if not self.playlist:
            return
        for f in self.playlist:
            full_path = self.playlistdir + "/" + f
            full_command = omx_command + self.options + [full_path]
            if self.debug:
                stdout = subprocess.PIPE
                stderr = subprocess.STDERR
            else:
                stdout = subprocess.DEVNULL
                stderr = subprocess.DEVNULL
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

    def _stop_player(self):
        if (self._thread_obj):
            self._thread_obj.exit()
            # print(self._thread_obj.native_id)
            # os.killpg(self._thread_obj.native_id, signal.SIGTERM)

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

    player = MediaThread(args.directory, args.random, args.loop, args.autoplay, args.debug, args.remaining)
