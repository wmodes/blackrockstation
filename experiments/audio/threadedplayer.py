import threading
import subprocess
import os

class ThreadedPlayer(threading.Thread):

    NEW_PLAYLIST = 'new playlist'
    STOP_PLAYING = 'stop'
    EXIT = 'exit'
    SIG_INT = 2

    def __init__(self, player_command, group=None, name=None):
        super().__init__(group=group, target=None, name=name)
        self.m_cv = threading.Condition()
        self.m_command = None
        self.m_args = None
        self.m_player = None
        if isinstance(player_command, str):
            self.m_player_command = player_command.split(' ')
        else:
            self.m_player_command = player_command

    def run(self):
        """Override the base class run() method"""
        while True:
            with self.m_cv:
                self.m_cv.wait_for(lambda: self.m_command is not None)
                if self.m_command == ThreadedPlayer.EXIT:
                    self._stop_playing()
                    return
                if self.m_command == ThreadedPlayer.STOP_PLAYING:
                    self._stop_playing()
                if self.m_command == ThreadedPlayer.NEW_PLAYLIST:
                    self._play(self.m_args)

                self.m_command = None
                self.m_args = None

    def play(self, playlist):
        """Tell the player to play a new playlist

        This method can be called from any thread. If the player is already playing
        something it is interrupted

        Args:
        playlist str what to play
        """
        with self.m_cv:
            self.m_args = playlist
            self.m_command = ThreadedPlayer.NEW_PLAYLIST
            self.m_cv.notify()

    def stop(self):
        """Tell the player to stop playing

        This method can be called from any thread. If the player is not already playing
        nothing happens
        """
        with self.m_cv:
            self.m_command = ThreadedPlayer.STOP_PLAYING
            self.m_cv.notify()

    def exit(self):
        """Tell the player to stop playing and exit the controlling thread.

        This method can be called from any thread. After calling exit no more commands
        are listened to.
        """
        with self.m_cv:
            self.m_command = ThreadedPlayer.EXIT
            self.m_cv.notify()

    def _stop_playing(self):
        """Implementation of stopping the player process

        Only called by ThreadedPlayer.run()
        """
        if self.m_player:
            self.m_player.send_signal(ThreadedPlayer.SIG_INT)
            self.m_player = None

    def _play(self, playlist):
        """Implementation of making a player process

        Only called by ThreadedPlayer.run()

        Args:
            playlist the directory name the player uses as a list
        """
        self._stop_playing()
        argv = self.m_player_command + [playlist]
        self.m_player = subprocess.Popen(argv, stderr=subprocess.DEVNULL)


if __name__ == '__main__':

    from time import sleep

    # we pass the playlist player and it's options to the class when we instantiate it.
    command = './omxplaylist.py --loop --random --autoplay --debug'
    pl = ThreadedPlayer(command)
    # this starts the thread (but not the player)
    pl.start()

    print("Starting playlist.")
    playlist_dir = "data"
    # this starts the player, which given the --autoplay flag should start playing
    pl.play(playlist_dir)
    print("Playliist started, control returns to calling program...")

    sleep(10)

    print("Playing new playlist...")
    playlist_dir = "data"
    # because we use the --random flag the player may start with a different file
    pl.play(playlist_dir)
    print("New playlist started...")

    sleep(5)

    print("Stopping playlist...")
    pl.stop()
    print("Playlist stopped...")

    sleep(5)

    print("Playing playlist...")
    playlist_dir = "data"
    pl.play(playlist_dir)
    print("New playlist started...")

    sleep(5)

    print("Stopping playlist...")
    pl.stop()
    print("Playlist stopped.")

    os._exit(0)
    # import code
    # code.interact(local=locals())
