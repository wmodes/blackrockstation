from ffpyplayer.player import MediaPlayer
import time

filename = "../data/070_SHARP_Titles_Flower_Titles.mp4"

player = MediaPlayer(filename)
val = ''
while val != 'eof':
    frame, val = player.get_frame()
    if val != 'eof' and frame is not None:
        img, t = frame
        # display img
