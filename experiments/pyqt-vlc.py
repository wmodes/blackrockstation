# importing vlc module
import vlc

# importing time module
import time

import sys


audio = "data/stereo-test.mp3"
video = "data/Tv Static Noise HD 720p.mp4"

# creating vlc media player object
media_player = vlc.MediaPlayer()

if sys.platform == "darwin":
    from PyQt5 import QtCore, QtGui, QtWidgets
    from PyQt5.QtMultimediaWidgets import QVideoWidget

    # app = QtWidgets.QApplication(sys.argv)
    # window = QtWidgets.QMainWindow()
    # button = QtWidgets.QPushButton("Hello, PyQt!")
    # window.setCentralWidget(button)
    # window.show()
    # app.exec_()

    # vlcApp =QtGui.QApplication(sys.argv)
    # vlcWidget = QtGui.QFrame()
    # vlcWidget.resize(700,700)
    # vlcWidget.show()
    # player.set_nsobject(vlcWidget.winId())

    app = QtWidgets.QApplication(sys.argv)
    window = QVideoWidget()
    # window = QtWidgets.QFrame()
    window.resize(700,700)
    window.show()
    app.exec_()
    media_player.set_nsobject(window.winId())

# media object
media = vlc.Media(video)

# setting media to the media player
media_player.set_media(media)

# setting video scale
media_player.video_set_scale(0.6)

# start playing video
media_player.play()

# wait so the video can be played for 5 seconds
# irrespective for length of video
time.sleep(15)

# getting track
value = media_player.audio_output_device_enum()

# printing value
print("Audio Output Devices: ")
print(value)
