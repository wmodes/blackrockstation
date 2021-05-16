from PyQt5.QtCore import QDir, Qt, QUrl, QTimer
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QMainWindow, QWidget, QPushButton, QApplication,
                             QLabel, QFileDialog, QStyle, QVBoxLayout)
import sys

class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.media_files = [
            "data/Tv Static Noise HD 720p.mp4",
            "data/070_SHARP_Titles_Flower_Titles.mp4",
            "data/072_SHARP_Footage_Shantyboat_Flyby_Titles.mp4",
            "data/1900 Victorian Time Machine - Parade with Brass Bands (Speed Corrected w_ Sound).mp4"
        ]
        self.current_index = 0

        # self.setWindowTitle("PyQt5 Video Player")

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videoWidget = QVideoWidget()

        # self.playButton = QPushButton()
        # self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        # self.playButton.clicked.connect(self.play)

        # self.openButton = QPushButton("Open Video")
        # self.openButton.clicked.connect(self.openFile)

        # widget = QWidget(self)
        # self.setCentralWidget(widget)
        self.setCentralWidget(videoWidget)

        # layout = QVBoxLayout()
        # layout.addWidget(videoWidget)
        # layout.addWidget(self.openButton)
        # layout.addWidget(self.playButton)

        # widget.setLayout(layout)
        # self.mediaPlayer.setVideoOutput(videoWidget)

        self.open_file(self.media_files[self.current_index])
        self.mediaPlayer.play()

        # create a timer to refresh video
        self.timer = QTimer(self)
        self.timer.setInterval(3000)
        self.timer.timeout.connect(self.next_video)

        self.timer.start()

    def open_file(self, filename):
        # fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
        #         QDir.homePath())

        if fileName != '':
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))

    def next_video(self):
        self.current_index += 1
        if self.current_index >= len(self.media_files):
            self.current_index = 0
        self.open_file(self.media_files[self.current_index])
        self.mediaPlayer.play()
        return

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()


app = QApplication(sys.argv)
videoplayer = VideoPlayer()
videoplayer.resize(640, 480)
videoplayer.show()
sys.exit(app.exec_())
