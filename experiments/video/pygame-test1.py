import pygame
import cv2
import numpy
pygame.init()

width = 1280
height = 720
window = pygame.display.set_mode((width, height))


class VideoPlayer:
    def __init__(self, surface, x, y, video, play_in_loop=False, mirror_effect=False):
        self.video = video
        self.surface = surface
        self.VideoReader = None
        self.FileOpened = False
        self.x = x
        self.y = y
        self.playInLoop = play_in_loop
        self.open()
        self.FrameResizer = False
        self.mirrorEffect = mirror_effect

    def maintainAspectRatio(self):
        video = cv2.VideoCapture(self.video)
        flag, frame = video.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = numpy.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)
        height = frame.get_height()
        width = frame.get_width()
        self.height = int((self.width * (height/width)))
        video.release()

    def activeMirrorEffact(self):
        self.mirrorEffect = True

    def deactiveMirrorEffact(self):
        self.mirrorEffect = False

    def activeFrameResizer(self, width=600, height=600, aspectRatio=False):
        self.FrameResizer = True
        self.width = width
        self.height = height
        if aspectRatio:
            self.maintainAspectRatio()

    def deactiveFrameResizer(self):
        self.FrameResizer = False

    def open(self):
        try:
            self.VideoReader = cv2.VideoCapture(self.video)
            self.VideoReader.setExceptionMode(False)
        except:
            self.FileOpend = False
            return False
        self.FileOpend = True

    def close(self):
        self.VideoReader.release()
        self.FileOpend = False

    def show(self):
        if self.FileOpend:
            flag, frame = self.VideoReader.read()
            if flag:
                if not self.mirrorEffect:
                    frame = cv2.flip(frame, 1)

                if self.FrameResizer:
                    frame = cv2.resize(frame, (self.width, self.height), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = numpy.rot90(frame)
                frame = pygame.surfarray.make_surface(frame)
                self.surface.blit(frame, (self.x, self.y))
            else:
                self.close()
                if self.playInLoop:
                    self.open()


videoPlayer = VideoPlayer(window, 0, 0, "../data/072_SHARP_Footage_Shantyboat_Flyby_Titles.mp4", True)
videoPlayer.activeFrameResizer(600, aspectRatio=True)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    videoPlayer.show()
    pygame.display.update()
    pygame.time.Clock().tick(30)
