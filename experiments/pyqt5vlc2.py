#
# PyQt5-based video-sync example for VLC Python bindings
# Copyright (C) 2009-2010 the VideoLAN team
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston MA 02110-1301, USA.
#
"""
This module contains a bare-bones VLC player class to play videos.

Author: Saveliy Yusufov, Columbia University, sy2685@columbia.edu
Date: 25 January 2019
"""

import os
import sys
import platform

from PyQt5 import QtWidgets, QtGui, QtCore
import vlc
# from network import Client


class Player(QtWidgets.QMainWindow):
    """Stripped-down PyQt5-based media player class to sync with "master" video.
    """

    def __init__(self, master=None):
        QtWidgets.QMainWindow.__init__(self, master)

        self.media_files = [
            "data/Tv Static Noise HD 720p.mp4",
            "data/070_SHARP_Titles_Flower_Titles.mp4",
            "data/072_SHARP_Footage_Shantyboat_Flyby_Titles.mp4",
            "data/1900 Victorian Time Machine - Parade with Brass Bands (Speed Corrected w_ Sound).mp4"
        ]
        self.current_index = 0

        # PyQy prep stuff
        #
        # set fullscreen mode (we could do this after the object, but let's do this early)
        #self.showFullScreen()
        self.resize(680, 420)
        self.setWindowTitle("Mini Player")
        self.init_ui()

        # VLC prep stuff
        #
        # VLC Options
        vlc_options = [
            "--embedded-video",
            "--no-audio",
            "--autoscale",
            #"--fullscreen",
            "--video-on-top",
            "--no-video-title-show",
            "--random",
            "--verbose -1",
            "--canvas-aspect 3:4",
            "--no-canvas-padd"
        ]
        # Create a basic vlc instance
        self.instance = vlc.Instance(" ".join(vlc_options))
        # later used to store media object, for now blank
        self.media = None
        # Create an empty vlc media player
        self.player = self.instance.media_player_new()
        # self.mediaplayer = vlc.MediaPlayer()
        # Set to fullscreen
        #self.player.set_fullscreen(True)
        #
        # The media player has to be 'connected' to the QFrame (otherwise the
        # video would be displayed in it's own window). This is platform
        # specific, so we must give the ID of the QFrame (or similar object) to
        # vlc. Different platforms have different functions for this
        if platform.system() == "Linux":  # for Linux using the X Server
            self.player.set_xwindow(int(self.videoframe.winId()))
        elif platform.system() == "Windows":  # for Windows
            self.player.set_hwnd(int(self.videoframe.winId()))
        elif platform.system() == "Darwin":  # for MacOS
            self.player.set_nsobject(int(self.videoframe.winId()))

        # load media
        self.open_file(self.media_files[self.current_index])

        # create a timer to refresh video
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.next_video)

        self.timer.start()

    def init_ui(self):
        """Set up the user interface
        """
        self.window = QtWidgets.QWidget(self)
        self.setCentralWidget(self.window)

        p = self.window.palette()
        p.setColor(QtGui.QPalette.Window, QtGui.QColor(0, 0, 0))
        self.window.setPalette(p)
        self.window.setAutoFillBackground(True)

        # In this widget, the video will be drawn
        if platform.system() == "Darwin":  # for MacOS
            self.videoframe = QtWidgets.QMacCocoaViewContainer(0)
        else:
            self.videoframe = QtWidgets.QFrame()

        self.palette = self.videoframe.palette()
        self.palette.setColor(QtGui.QPalette.Window, QtGui.QColor(0, 0, 0))
        self.videoframe.setPalette(self.palette)
        self.videoframe.setAutoFillBackground(True)

        self.vboxlayout = QtWidgets.QVBoxLayout()
        self.vboxlayout.addWidget(self.videoframe)
        self.window.setLayout(self.vboxlayout)


    def open_file(self, filename):
        """Open a media file in a MediaPlayer
        """
        # dialog_txt = "Choose Media File"
        # filename = QtWidgets.QFileDialog.getOpenFileName(self, dialog_txt, os.path.expanduser('~'))
        if not filename[0]:
            return

        # here

        # getOpenFileName returns a tuple, so use only the actual file name
        self.media = self.instance.media_new(filename)

        # Put the media in the media player
        self.player.set_media(self.media)

        # Parse the metadata of the file
        self.media.parse()

        # Start playing the video as soon as it loads
        self.player.play()

    def next_video(self):
        self.current_index += 1
        if self.current_index >= len(self.media_files):
            self.current_index = 0
        self.open_file(self.media_files[self.current_index])
        return

    def update_ui(self):

        try:
            val = self.data_queue.get(block=False)
        except queue.Empty:
            return

        print("data_queue got value")

        if val == '<':
            self.player.set_rate(self.player.get_rate() * 0.5)
            return
        if val == '>':
            self.player.set_rate(self.player.get_rate() * 2)
            return
        if val == 'P':
            self.player.play()
            return
        if val == 'p':
            self.player.pause()
            return
        if val == 'S':
            self.player.stop()
            return
        if val == 'n':
            self.current_index += 1
            if self.current_index >= len(self.media_files):
                current_index = 0
            self.open_file(self.media_files[self.current_index])
            return

        val = int(val)
        if val != self.player.get_time():
            self.player.set_time(val)


def main():
    """Entry point for our simple vlc player
    """
    app = QtWidgets.QApplication(sys.argv)

    player = Player()
    player.show()
    # player.resize(680, 420)
    # player.showFullScreen()

    # _ = Client("localhost", 10000, data_queue)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
