
"""
This module contains a bare-bones VLC player class to play videos.
Adapted  from an example by Saveliy Yusufov, Columbia University, sy2685@columbia.edu
"""

import os
import sys
import platform

from PyQt5 import QtWidgets, QtGui, QtCore
import vlc

class Player(QtWidgets.QMainWindow):
    """Stripped-down PyQt5-based media player class
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
        #
        # in fullscreen mode, videos show up in the bottom left corner
        # self.showFullScreen()
        #
        # in this window, videos are scaled only when window is manually resized
        #self.resize(680, 420)
        self.showFullScreen()
        #
        self.init_ui()

        # VLC prep stuff
        #
        # VLC Options
        vlc_options = [
            "--embedded-video",
            #"--no-audio",
            "--no-autoscale",
            "--fullscreen",
            "--video-on-top",
            "--no-video-title-show",
            "--random",
            "--verbose -1",
            "--canvas-aspect 3:4",
            "--crop=3:4",
            "--qt-video-autoresize",    # Resize interface to the native video size
            #"--canvas-pad"
        ]
        # Create a basic vlc instance
        self.instance = vlc.Instance(" ".join(vlc_options))
        # later used to store media object, for now blank
        self.media = None
        # Create an empty vlc media player
        self.player = self.instance.media_player_new()
        # set aspect ratio - nope, stretches video not crops
        # self.player.video_set_aspect_ratio("4:3")
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
        self.timer.setInterval(3000)
        self.timer.timeout.connect(self.next_video)

        self.timer.start()

    def init_ui(self):
        """Set up the user interface
        """
        if platform.system() == "Darwin":  # for MacOS
            self.videoframe = QtWidgets.QMacCocoaViewContainer(0)
        else:
            self.videoframe = QtWidgets.QFrame()
        # set videoframe color
        # self.palette = self.videoframe.palette()
        # self.palette.setColor(QtGui.QPalette.Window, QtGui.QColor(0, 0, 0))
        # self.videoframe.setPalette(self.palette)
        # self.videoframe.setAutoFillBackground(True)
        #
        # How do I set aspectRatioMode = KeepAspectRatioByExpanding
        #
        self.setCentralWidget(self.videoframe)

    def open_file(self, filename):
        """Open a media file in a MediaPlayer
        """
        if not filename:
            return
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


def main():
    """Entry point for our simple vlc player
    """
    app = QtWidgets.QApplication(sys.argv)

    player = Player()
    player.show()

    # _ = Client("localhost", 10000, data_queue)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
